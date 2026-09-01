"""Exact rule-column generation for finite multiclass minimax testing.

This module solves the same finite common-support problem as the direct
``K * S``-variable primal LP, but it never presents those variables to the
linear-programming solver.  A deterministic rule assigns one class to every
observation-support node.  The convex hull of all such rules is exactly the
product of the nodewise probability simplices, so a mixture of deterministic
rules represents every randomized decision and introduces no approximation.

The restricted master contains one variable per generated deterministic rule
and one worst-risk variable.  Its member-constraint dual weights price a new
rule in closed form: at support node ``s``, choose the class maximizing

``sum_j lambda[k, j] * P[k][j, s]``.

The restricted-master risk is a primal upper bound for the full finite LP.
For every globally normalized nonnegative ``lambda``,

``1 - sum_s max_k sum_j lambda[k, j] * P[k][j, s]``

is a full-dual lower bound.  Their explicitly recomputed gap is therefore a
rigorous stopping certificate.  Exact duplicate rows are removed only inside
the numerical master; errors and dual weights are returned in the original
member layout, so duplicate frequency cannot change the represented problem.

Only observable probability laws enter this module.  It has no topology,
nuisance-coordinate, model, flux, or prior interface.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
import time
from typing import Sequence

import numpy as np
from scipy import sparse
from scipy.optimize import linprog

from .composite_mid_minimax import (
    DEFAULT_LP_TOLERANCE,
    DEFAULT_ROW_SUM_TOLERANCE,
    MinimaxNumericalError,
)


def _readonly_float(values: np.ndarray | Sequence[float]) -> np.ndarray:
    result = np.array(values, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _readonly_int(values: np.ndarray | Sequence[int]) -> np.ndarray:
    result = np.array(values, dtype=int, copy=True)
    result.setflags(write=False)
    return result


def _class_labels(count: int, labels: Sequence[str] | None) -> tuple[str, ...]:
    if labels is None:
        result = tuple(f"class_{index}" for index in range(count))
    else:
        result = tuple(str(value) for value in labels)
    if (
        len(result) != count
        or len(set(result)) != count
        or any(not value for value in result)
    ):
        raise ValueError(
            "class labels must be nonempty, unique, and align with classes"
        )
    return result


def _canonical_csr(
    values: np.ndarray | sparse.spmatrix,
    *,
    class_index: int,
) -> sparse.csr_matrix:
    if sparse.issparse(values):
        # Constraint generation already owns canonical float64 CSR matrices.
        # Borrow those immutable inputs for the duration of the solve instead
        # of materializing a second J-by-S probability table.  A copy is still
        # made before any canonicalizing mutation is needed.
        can_borrow = bool(
            sparse.isspmatrix_csr(values)
            and values.dtype == np.dtype(float)
            and values.has_canonical_format
            and not np.any(values.data == 0.0)
        )
        if can_borrow:
            matrix = values
        else:
            matrix = sparse.csr_matrix(values, dtype=float, copy=True)
            matrix.sum_duplicates()
            matrix.sort_indices()
            matrix.eliminate_zeros()
    else:
        array = np.asarray(values, dtype=float)
        if array.ndim != 2:
            raise ValueError(f"class {class_index} laws must be a matrix")
        matrix = sparse.csr_matrix(array)
    if matrix.ndim != 2 or min(matrix.shape) < 1:
        raise ValueError(f"class {class_index} laws must be a nonempty matrix")
    if not np.all(np.isfinite(matrix.data)) or np.any(matrix.data < 0.0):
        raise ValueError(f"class {class_index} contains invalid probabilities")
    row_sums = np.asarray(matrix.sum(axis=1), dtype=float).ravel()
    if not np.all(np.isfinite(row_sums)) or not np.allclose(
        row_sums, 1.0, rtol=0.0, atol=DEFAULT_ROW_SUM_TOLERANCE
    ):
        raise ValueError(f"class {class_index} law rows must each sum to one")
    return matrix


def _row_bounds(matrix: sparse.csr_matrix, row_index: int) -> tuple[int, int]:
    return int(matrix.indptr[row_index]), int(matrix.indptr[row_index + 1])


def _row_digest(matrix: sparse.csr_matrix, row_index: int) -> bytes:
    """Return a compact bucket key; equality is always checked separately."""

    start, stop = _row_bounds(matrix, row_index)
    indices = np.ascontiguousarray(matrix.indices[start:stop], dtype=np.int64)
    data = np.ascontiguousarray(matrix.data[start:stop], dtype=np.float64)
    digest = hashlib.blake2b(digest_size=16, person=b"fluxemu-row-v1")
    digest.update(memoryview(indices).cast("B"))
    digest.update(memoryview(data).cast("B"))
    return digest.digest()


def _rows_equal(
    left: sparse.csr_matrix,
    left_index: int,
    right: sparse.csr_matrix,
    right_index: int,
) -> bool:
    left_start, left_stop = _row_bounds(left, left_index)
    right_start, right_stop = _row_bounds(right, right_index)
    return bool(
        np.array_equal(
            left.indices[left_start:left_stop],
            right.indices[right_start:right_stop],
        )
        and np.array_equal(
            left.data[left_start:left_stop],
            right.data[right_start:right_stop],
        )
    )


def _rule_digest(rule_labels: np.ndarray) -> bytes:
    values = np.ascontiguousarray(rule_labels, dtype=np.int32)
    return hashlib.blake2b(
        memoryview(values).cast("B"), digest_size=16, person=b"fluxemu-rule-v1"
    ).digest()


def _find_rule(
    rules: Sequence[np.ndarray],
    buckets: dict[bytes, list[int]],
    rule_labels: np.ndarray,
) -> tuple[int | None, bytes]:
    digest = _rule_digest(rule_labels)
    for index in buckets.get(digest, ()):
        if np.array_equal(rules[index], rule_labels):
            return index, digest
    return None, digest


def _register_rule(
    rules: list[np.ndarray],
    buckets: dict[bytes, list[int]],
    rule_labels: np.ndarray,
) -> bool:
    existing, digest = _find_rule(rules, buckets, rule_labels)
    if existing is not None:
        return False
    compact = np.array(rule_labels, dtype=np.int32, copy=True)
    rules.append(compact)
    buckets.setdefault(digest, []).append(len(rules) - 1)
    return True


def _grow_risk_storage(
    storage: np.ndarray,
    *,
    required_columns: int,
    maximum_columns: int,
) -> np.ndarray:
    if required_columns <= storage.shape[1]:
        return storage
    added_capacity = min(16, maximum_columns - storage.shape[1])
    new_capacity = max(required_columns, storage.shape[1] + added_capacity)
    result = np.empty((storage.shape[0], new_capacity), dtype=float)
    result[:, : storage.shape[1]] = storage
    return result


@dataclass(frozen=True)
class _DeduplicatedClass:
    original: sparse.csr_matrix
    unique: sparse.csr_matrix
    unique_first_original: np.ndarray
    unique_digests: tuple[bytes, ...]


def _deduplicate_class(matrix: sparse.csr_matrix) -> _DeduplicatedClass:
    member_count = matrix.shape[0]
    buckets: dict[bytes, list[int]] = {}
    representatives: list[int] = []
    representative_digests: list[bytes] = []
    for original_index in range(member_count):
        digest = _row_digest(matrix, original_index)
        matched = None
        for unique_index in buckets.get(digest, ()):
            if _rows_equal(
                matrix,
                original_index,
                matrix,
                representatives[unique_index],
            ):
                matched = unique_index
                break
        if matched is None:
            matched = len(representatives)
            representatives.append(original_index)
            representative_digests.append(digest)
            buckets.setdefault(digest, []).append(matched)

    # Constraint order has no mathematical meaning.  Retaining first-occurrence
    # order lets the overwhelmingly common all-unique case alias the caller's
    # canonical CSR storage instead of copying it merely to sort rows.
    first = np.asarray(representatives, dtype=int)
    ordered_digests = tuple(representative_digests)
    if len(first) == member_count:
        unique = matrix
    else:
        unique = sparse.csr_matrix(matrix[first], dtype=float, copy=True)
        unique.sum_duplicates()
        unique.sort_indices()
    return _DeduplicatedClass(
        original=matrix,
        unique=unique,
        unique_first_original=first,
        unique_digests=ordered_digests,
    )


@dataclass(frozen=True)
class RuleColumnGenerationIteration:
    """One restricted-master solve and full pricing audit."""

    iteration: int
    generated_rule_count: int
    active_rule_count: int
    active_dual_member_count: int
    master_objective: float
    primal_upper_bound: float
    pricing_dual_lower_bound: float
    certified_dual_lower_bound: float
    certificate_gap: float
    certificate_source: str
    raw_master_dual_weight_sum_error: float
    priced_rule_was_duplicate: bool
    master_solver_status: int
    master_solver_message: str
    master_solver_iterations: int
    master_solve_seconds: float


@dataclass(frozen=True)
class RuleColumnGenerationSolution:
    """Primal rule mixture, full-dual certificate, and numerical audits."""

    class_labels: tuple[str, ...]
    decision_probabilities: np.ndarray
    primal_upper_bound: float
    dual_lower_bound: float
    certificate_gap: float
    dual_member_weights: tuple[np.ndarray, ...]
    dual_class_weights: np.ndarray
    member_errors: tuple[np.ndarray, ...]
    classwise_worst_errors: np.ndarray
    generated_rule_labels: np.ndarray
    generated_rule_weights: np.ndarray
    active_rule_indices: np.ndarray
    dual_scores: np.ndarray
    iterations: tuple[RuleColumnGenerationIteration, ...]
    converged: bool
    convergence_tolerance: float
    maximum_simplex_violation: float
    maximum_primal_constraint_violation: float
    dual_weight_sum_error: float
    maximum_member_complementarity_violation: float
    maximum_argmax_complementarity_violation: float
    complementarity_gap_recomputation_error: float
    master_objective_recomputation_error: float
    randomized_support_indices: np.ndarray
    dual_tie_support_indices: np.ndarray
    original_member_counts: tuple[int, ...]
    unique_member_counts: tuple[int, ...]
    certificate_source: str
    solver_status: int
    solver_message: str

    @property
    def class_count(self) -> int:
        return len(self.class_labels)

    @property
    def support_size(self) -> int:
        return self.decision_probabilities.shape[1]

    @property
    def global_worst_error(self) -> float:
        return float(np.max(self.classwise_worst_errors))

    @property
    def objective(self) -> float:
        return self.primal_upper_bound

    @property
    def primal_objective(self) -> float:
        return self.primal_upper_bound

    @property
    def solver_statuses(self) -> tuple[int, ...]:
        return tuple(item.master_solver_status for item in self.iterations)


def _risk_column(
    classes: Sequence[sparse.csr_matrix], rule_labels: np.ndarray
) -> np.ndarray:
    support_size = len(rule_labels)
    support_indices = np.arange(support_size)
    pieces: list[np.ndarray] = []
    for class_index, matrix in enumerate(classes):
        indicator = np.zeros(support_size, dtype=float)
        indicator[support_indices[rule_labels == class_index]] = 1.0
        correct = np.asarray(matrix @ indicator, dtype=float).ravel()
        pieces.append(1.0 - correct)
    return np.concatenate(pieces)


def _dual_scores(
    classes: Sequence[sparse.csr_matrix],
    offsets: np.ndarray,
    flat_weights: np.ndarray,
) -> np.ndarray:
    return np.vstack(
        [
            np.asarray(
                matrix.T @ flat_weights[offsets[index] : offsets[index + 1]],
                dtype=float,
            ).ravel()
            for index, matrix in enumerate(classes)
        ]
    )


def _shared_law_certificate(
    classes: Sequence[_DeduplicatedClass], offsets: np.ndarray
) -> tuple[float, np.ndarray, str] | None:
    # Compact digests only choose comparison buckets.  Every candidate match
    # is checked against the canonical CSR values, so a digest collision can
    # neither merge distinct laws nor create a false exact certificate.
    occurrences: dict[bytes, list[list[tuple[int, int]]]] = {}
    for class_index, item in enumerate(classes):
        for unique_index, digest in enumerate(item.unique_digests):
            groups = occurrences.setdefault(digest, [])
            matched_group = None
            for group in groups:
                other_class, other_index = group[0]
                if _rows_equal(
                    item.unique,
                    unique_index,
                    classes[other_class].unique,
                    other_index,
                ):
                    matched_group = group
                    break
            if matched_group is None:
                groups.append([(class_index, unique_index)])
            else:
                matched_group.append((class_index, unique_index))

    best: tuple[float, np.ndarray, str] | None = None
    unique_matrices = tuple(item.unique for item in classes)
    for groups in occurrences.values():
        for values in groups:
            if len(values) < 2:
                continue
            weights = np.zeros(int(offsets[-1]), dtype=float)
            mass = 1.0 / len(values)
            for class_index, unique_index in values:
                weights[int(offsets[class_index]) + unique_index] = mass
            scores = _dual_scores(unique_matrices, offsets, weights)
            lower = float(1.0 - np.sum(np.max(scores, axis=0)))
            source = f"exact_shared_law_{len(values)}_class"
            if best is None or lower > best[0]:
                best = (lower, weights, source)
    return best


def _disjoint_support_certificate(
    classes: Sequence[sparse.csr_matrix], offsets: np.ndarray
) -> tuple[float, np.ndarray, str] | None:
    """Return a class-balanced exact dual for disjoint represented supports.

    The condition concerns the represented law sets, not their row
    frequencies.  Balancing the dual class totals also keeps every class score
    available to a later continuous-rule reproduction audit.
    """

    represented_by_class = np.vstack(
        [np.asarray(matrix.getnnz(axis=0)).ravel() > 0 for matrix in classes]
    )
    if np.any(np.count_nonzero(represented_by_class, axis=0) > 1):
        return None

    class_count = len(classes)
    weights = np.zeros(int(offsets[-1]), dtype=float)
    for class_index, matrix in enumerate(classes):
        member_count = matrix.shape[0]
        weights[offsets[class_index] : offsets[class_index + 1]] = (
            1.0 / (class_count * member_count)
        )
    scores = _dual_scores(classes, offsets, weights)
    lower = float(1.0 - np.sum(np.max(scores, axis=0)))
    return lower, weights, "exact_disjoint_support_class_balanced"


def solve_rule_column_generation(
    class_probability_rows: Sequence[np.ndarray | sparse.spmatrix],
    *,
    class_labels: Sequence[str] | None = None,
    convergence_tolerance: float = 2.0e-7,
    maximum_iterations: int = 500,
    initial_rule_labels: np.ndarray | None = None,
    solver_method: str = "highs-ds",
    active_tolerance: float = DEFAULT_LP_TOLERANCE,
    dual_support_tolerance: float = 1.0e-9,
) -> RuleColumnGenerationSolution:
    """Solve a finite ``K``-way minimax LP by exact rule column generation.

    Parameters contain observable common-support probability rows only.
    Dense arrays and SciPy sparse matrices may be mixed.  ``maximum_iterations``
    counts restricted-master solves; a nonconverged final bracket is returned
    when that limit is reached.  ``initial_rule_labels`` may warm-start a
    re-solve with deterministic observable-support rules from an earlier
    constraint-generation master.  They are merely feasible columns and do
    not alter the full pricing certificate.  Solver failure or a duplicate
    pricing column with a nonzero certified gap raises
    :class:`MinimaxNumericalError`.
    """

    raw_items = tuple(class_probability_rows)
    if len(raw_items) < 2:
        raise ValueError("at least two finite observable-law classes are required")
    labels = _class_labels(len(raw_items), class_labels)
    tolerance = float(convergence_tolerance)
    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("convergence tolerance must be positive and finite")
    iteration_limit = int(maximum_iterations)
    if iteration_limit < 1:
        raise ValueError("maximum iterations must be positive")
    method = str(solver_method)
    if method not in {"highs", "highs-ds", "highs-ipm"}:
        raise ValueError("unsupported scipy linprog method")
    if float(active_tolerance) < 0.0 or float(dual_support_tolerance) < 0.0:
        raise ValueError("activity tolerances must be nonnegative")

    canonical = tuple(
        _canonical_csr(values, class_index=index)
        for index, values in enumerate(raw_items)
    )
    support_sizes = {matrix.shape[1] for matrix in canonical}
    if len(support_sizes) != 1:
        raise ValueError("all classes must use the same observation support")
    support_size = canonical[0].shape[1]
    deduplicated = tuple(_deduplicate_class(matrix) for matrix in canonical)
    classes = tuple(item.unique for item in deduplicated)
    class_count = len(classes)
    member_counts = tuple(matrix.shape[0] for matrix in classes)
    offsets = np.cumsum([0] + list(member_counts))
    member_count = int(offsets[-1])

    if initial_rule_labels is None:
        initial_rules = np.empty((0, support_size), dtype=np.int32)
    else:
        raw_initial_rules = np.asarray(initial_rule_labels)
        if (
            raw_initial_rules.ndim != 2
            or raw_initial_rules.shape[1] != support_size
            or not np.issubdtype(raw_initial_rules.dtype, np.integer)
            or (
                raw_initial_rules.size > 0
                and (
                    int(np.min(raw_initial_rules)) < 0
                    or int(np.max(raw_initial_rules)) >= class_count
                )
            )
        ):
            raise ValueError(
                "initial rule labels must be an integer L-by-support matrix "
                "with labels in [0, K)"
            )
        initial_rules = np.asarray(raw_initial_rules, dtype=np.int32)

    rules: list[np.ndarray] = []
    rule_buckets: dict[bytes, list[int]] = {}
    for class_index in range(class_count):
        rule = np.full(support_size, class_index, dtype=np.int32)
        _register_rule(rules, rule_buckets, rule)
    for rule in initial_rules:
        _register_rule(rules, rule_buckets, rule)

    shared_certificate = _shared_law_certificate(deduplicated, offsets)
    disjoint_certificate = _disjoint_support_certificate(classes, offsets)
    certificates = tuple(
        item
        for item in (
            shared_certificate,
            disjoint_certificate,
        )
        if item is not None
    )
    if not certificates:
        best_lower = -math.inf
        best_dual = np.zeros(member_count, dtype=float)
        best_source = "none"
    else:
        best_lower, best_dual, best_source = max(
            certificates, key=lambda item: item[0]
        )

    # For pairwise-disjoint represented supports, the balanced certificate
    # prices the globally perfect deterministic rule immediately.  Seed that
    # exact column instead of relying on a degenerate first restricted-master
    # dual to discover the same rule through many partial columns.
    if disjoint_certificate is not None:
        disjoint_scores = _dual_scores(
            classes, offsets, disjoint_certificate[1]
        )
        disjoint_rule = np.argmax(disjoint_scores, axis=0).astype(np.int32)
        _register_rule(rules, rule_buckets, disjoint_rule)

    maximum_rule_count = len(rules) + iteration_limit
    initial_spare_columns = min(16, iteration_limit)
    risk_storage = np.empty(
        (member_count, len(rules) + initial_spare_columns), dtype=float
    )
    for rule_index, rule in enumerate(rules):
        risk_storage[:, rule_index] = _risk_column(classes, rule)

    records: list[RuleColumnGenerationIteration] = []
    converged = False
    final_result = None
    final_rule_weights = None
    final_master_error = math.inf
    support_indices = np.arange(support_size)

    for iteration in range(iteration_limit):
        rule_count = len(rules)
        risks = risk_storage[:, :rule_count]
        inequalities = sparse.hstack(
            (
                sparse.csr_matrix(risks),
                sparse.csr_matrix(-np.ones((member_count, 1), dtype=float)),
            ),
            format="csr",
        )
        simplex = sparse.csr_matrix(
            (
                np.ones(rule_count, dtype=float),
                (np.zeros(rule_count, dtype=int), np.arange(rule_count, dtype=int)),
            ),
            shape=(1, rule_count + 1),
        )
        objective = np.zeros(rule_count + 1, dtype=float)
        objective[-1] = 1.0
        started = time.perf_counter()
        result = linprog(
            objective,
            A_ub=inequalities,
            b_ub=np.zeros(member_count, dtype=float),
            A_eq=simplex,
            b_eq=np.ones(1, dtype=float),
            bounds=[(0.0, None)] * rule_count + [(None, None)],
            method=method,
            options={
                "primal_feasibility_tolerance": 1.0e-9,
                "dual_feasibility_tolerance": 1.0e-9,
            },
        )
        solve_seconds = time.perf_counter() - started
        if not result.success or result.x is None:
            raise MinimaxNumericalError(
                "rule-column restricted master failed "
                f"(status {result.status}): {result.message}"
            )
        raw_rule_weights = np.asarray(result.x[:-1], dtype=float)
        if np.min(raw_rule_weights) < -2.0e-8:
            raise MinimaxNumericalError("restricted master returned negative rule weights")
        rule_weights = np.maximum(raw_rule_weights, 0.0)
        weight_sum = float(np.sum(rule_weights))
        if weight_sum <= 0.0:
            raise MinimaxNumericalError("restricted master rule mixture has zero mass")
        rule_weights /= weight_sum
        member_risks = risks @ rule_weights
        upper = float(np.max(member_risks))
        master_error = abs(float(result.x[-1]) - upper)

        marginals = np.asarray(result.ineqlin.marginals, dtype=float)
        if marginals.shape != (member_count,) or np.max(marginals) > 2.0e-8:
            raise MinimaxNumericalError(
                "restricted-master inequality dual orientation is inconsistent"
            )
        raw_dual = np.maximum(-marginals, 0.0)
        raw_dual_sum = float(np.sum(raw_dual))
        if raw_dual_sum <= 0.0:
            raise MinimaxNumericalError("restricted-master dual has zero mass")
        raw_dual_sum_error = abs(raw_dual_sum - 1.0)
        pricing_dual = raw_dual / raw_dual_sum
        pricing_scores = _dual_scores(classes, offsets, pricing_dual)
        maximum_scores = np.max(pricing_scores, axis=0)
        pricing_lower = float(1.0 - np.sum(maximum_scores))
        if pricing_lower > best_lower + 5.0e-13:
            best_lower = pricing_lower
            best_dual = np.array(pricing_dual, copy=True)
            best_source = f"pricing_iteration_{iteration}"

        gap = upper - best_lower
        if gap < -max(5.0e-8, tolerance):
            raise MinimaxNumericalError(
                "full-dual lower bound exceeds the restricted-master primal bound"
            )
        priced_rule = np.argmax(pricing_scores, axis=0).astype(np.int32)
        duplicate = _find_rule(rules, rule_buckets, priced_rule)[0] is not None
        active_rules = int(np.count_nonzero(rule_weights > float(active_tolerance)))
        active_dual = int(
            np.count_nonzero(pricing_dual > float(dual_support_tolerance))
        )
        records.append(
            RuleColumnGenerationIteration(
                iteration=iteration,
                generated_rule_count=rule_count,
                active_rule_count=active_rules,
                active_dual_member_count=active_dual,
                master_objective=float(result.x[-1]),
                primal_upper_bound=upper,
                pricing_dual_lower_bound=pricing_lower,
                certified_dual_lower_bound=best_lower,
                certificate_gap=max(0.0, gap),
                certificate_source=best_source,
                raw_master_dual_weight_sum_error=raw_dual_sum_error,
                priced_rule_was_duplicate=duplicate,
                master_solver_status=int(result.status),
                master_solver_message=str(result.message),
                master_solver_iterations=int(result.nit),
                master_solve_seconds=solve_seconds,
            )
        )
        final_result = result
        final_rule_weights = rule_weights
        final_master_error = master_error
        if gap <= tolerance:
            converged = True
            break
        if duplicate:
            # If the exact argmax rule is already present, try deterministic
            # alternative tie preferences before declaring numerical stalling.
            node_scale = np.maximum(np.abs(maximum_scores), 1.0 / support_size)
            tie_mask = np.abs(
                pricing_scores - maximum_scores[np.newaxis, :]
            ) <= 2.0e-10 * node_scale[np.newaxis, :]
            alternative = None
            for preferred_class in range(class_count):
                candidate = np.array(priced_rule, copy=True)
                candidate[tie_mask[preferred_class]] = preferred_class
                if _find_rule(rules, rule_buckets, candidate)[0] is None:
                    alternative = candidate
                    break
            if alternative is None:
                raise MinimaxNumericalError(
                    "rule pricing repeated an existing column before the "
                    f"certificate gap closed (gap={gap:.6g})"
                )
            priced_rule = alternative
        if not _register_rule(rules, rule_buckets, priced_rule):  # pragma: no cover
            raise MinimaxNumericalError("rule registration lost duplicate consistency")
        risk_storage = _grow_risk_storage(
            risk_storage,
            required_columns=len(rules),
            maximum_columns=maximum_rule_count,
        )
        risk_storage[:, len(rules) - 1] = _risk_column(classes, priced_rule)

    if final_result is None or final_rule_weights is None:
        raise MinimaxNumericalError("rule-column generation did not execute")

    # The final master precedes a possible last nonconverged pricing addition.
    final_weight_count = len(final_rule_weights)
    used_rules = np.stack(rules[:final_weight_count], axis=0).astype(
        np.int32, copy=False
    )
    used_rules.setflags(write=False)
    rule_weights = np.array(final_rule_weights, dtype=float, copy=True)
    decision = np.zeros((class_count, support_size), dtype=float)
    for rule_index in np.flatnonzero(rule_weights > 0.0):
        decision[
            used_rules[rule_index], support_indices
        ] += rule_weights[rule_index]
    simplex_violation = float(np.max(np.abs(np.sum(decision, axis=0) - 1.0)))
    if np.min(decision) < -2.0e-10 or simplex_violation > 2.0e-7:
        raise MinimaxNumericalError("generated rule mixture violates a nodewise simplex")

    original_errors = tuple(
        np.asarray(
            item.original @ (1.0 - decision[class_index]), dtype=float
        ).ravel()
        for class_index, item in enumerate(deduplicated)
    )
    classwise = np.asarray([np.max(values) for values in original_errors])
    dense_upper = float(np.max(classwise))
    # Recompute from the returned original layout; exact duplicate elimination
    # must not change the primal certificate.
    upper = dense_upper
    primal_violation = max(
        0.0, max(float(np.max(values)) - upper for values in original_errors)
    )

    unique_dual = np.array(best_dual, dtype=float, copy=True)
    unique_dual = np.maximum(unique_dual, 0.0)
    unique_dual_sum = float(np.sum(unique_dual))
    if unique_dual_sum <= 0.0:
        raise MinimaxNumericalError("final full-dual certificate has zero mass")
    unique_dual /= unique_dual_sum
    scores = _dual_scores(classes, offsets, unique_dual)
    maximum_scores = np.max(scores, axis=0)
    lower = float(1.0 - np.sum(maximum_scores))
    gap = upper - lower
    if gap < -max(5.0e-8, tolerance):
        raise MinimaxNumericalError("final full-dual lower bound exceeds primal upper bound")

    original_dual: list[np.ndarray] = []
    cursor = 0
    for item in deduplicated:
        count = item.unique.shape[0]
        weights = np.zeros(item.original.shape[0], dtype=float)
        weights[item.unique_first_original] = unique_dual[cursor : cursor + count]
        original_dual.append(weights)
        cursor += count
    dual_class_weights = np.asarray([np.sum(values) for values in original_dual])
    dual_sum_error = abs(float(np.sum(dual_class_weights)) - 1.0)

    flat_original_errors = np.concatenate(original_errors)
    flat_original_dual = np.concatenate(original_dual)
    member_slacks = upper - flat_original_errors
    member_complementarity = float(
        np.max(
            np.where(
                flat_original_dual > float(dual_support_tolerance),
                np.abs(member_slacks),
                0.0,
            )
        )
    )
    score_gaps = maximum_scores[np.newaxis, :] - scores
    argmax_complementarity = float(
        np.max(
            np.where(
                decision > float(active_tolerance), score_gaps, 0.0
            )
        )
    )
    weighted_member_slack = float(np.dot(flat_original_dual, member_slacks))
    weighted_argmax_slack = float(np.sum(decision * score_gaps))
    complementarity_error = abs(
        gap - weighted_member_slack - weighted_argmax_slack
    )
    if (
        primal_violation > 2.0e-7
        or simplex_violation > 2.0e-7
        or dual_sum_error > 2.0e-7
        or complementarity_error > max(2.0e-7, 2.0 * tolerance)
    ):
        raise MinimaxNumericalError(
            "rule-column primal/dual validation failed: "
            f"constraint={primal_violation:.6g}, simplex={simplex_violation:.6g}, "
            f"dual_sum={dual_sum_error:.6g}, complementarity={complementarity_error:.6g}"
        )

    node_scale = np.maximum(np.abs(maximum_scores), 1.0 / support_size)
    tie_mask = np.abs(scores - maximum_scores[np.newaxis, :]) <= (
        2.0e-7 * node_scale[np.newaxis, :]
    )
    random_support = np.flatnonzero(
        np.count_nonzero(decision > float(active_tolerance), axis=0) > 1
    )
    tie_support = np.flatnonzero(np.count_nonzero(tie_mask, axis=0) > 1)
    active_rule_indices = np.flatnonzero(
        rule_weights > float(active_tolerance)
    )

    return RuleColumnGenerationSolution(
        class_labels=labels,
        decision_probabilities=_readonly_float(decision),
        primal_upper_bound=upper,
        dual_lower_bound=lower,
        certificate_gap=max(0.0, gap),
        dual_member_weights=tuple(_readonly_float(values) for values in original_dual),
        dual_class_weights=_readonly_float(dual_class_weights),
        member_errors=tuple(_readonly_float(values) for values in original_errors),
        classwise_worst_errors=_readonly_float(classwise),
        generated_rule_labels=used_rules,
        generated_rule_weights=_readonly_float(rule_weights),
        active_rule_indices=_readonly_int(active_rule_indices),
        dual_scores=_readonly_float(scores),
        iterations=tuple(records),
        converged=bool(converged and gap <= tolerance),
        convergence_tolerance=tolerance,
        maximum_simplex_violation=simplex_violation,
        maximum_primal_constraint_violation=primal_violation,
        dual_weight_sum_error=dual_sum_error,
        maximum_member_complementarity_violation=member_complementarity,
        maximum_argmax_complementarity_violation=argmax_complementarity,
        complementarity_gap_recomputation_error=complementarity_error,
        master_objective_recomputation_error=final_master_error,
        randomized_support_indices=_readonly_int(random_support),
        dual_tie_support_indices=_readonly_int(tie_support),
        original_member_counts=tuple(item.original.shape[0] for item in deduplicated),
        unique_member_counts=tuple(item.unique.shape[0] for item in deduplicated),
        certificate_source=best_source,
        solver_status=int(final_result.status),
        solver_message=str(final_result.message),
    )


# A long-form alias keeps the numerical method explicit at call sites.
solve_finite_multihypothesis_minimax_by_rule_column_generation = (
    solve_rule_column_generation
)
