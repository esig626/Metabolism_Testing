"""Finite minimax estimation of noise-free MID centres.

This module starts after a finite family of observation laws and its target
MIDs have been constructed.  It accepts no fluxes, support labels, or other
semantic state metadata.

For row-stochastic laws ``p[i, j]`` and target MIDs ``z[i]``, a prior
``lambda`` makes the Bayes action at support point ``j`` the posterior target
mean.  Restricting actions to the compact convex hull of the targets is
without loss under squared Euclidean error.  The finite decision space is
therefore compact and convex, risk is convex in the action and linear in the
state mixture, and finite minimax gives

``min_delta max_i R_i(delta) = max_lambda min_delta sum_i lambda_i R_i``.

Completion of squares gives the posterior mean and the concave Bayes-risk
objective used below.  At a least-favourable prior its gradient is the vector
of recomputed statewise risks: positive-prior states equalise and zero-prior
states have no larger risk.  A generic optimiser is not treated as a proof.
Every returned result carries the explicit numerical bracket
``Bayes risk <= finite minimax risk <= maximum recomputed state risk``.

Importance-discretised probability rows can contain exact zeros or subnormal
values even though the underlying Dirichlet densities are positive.  The
posterior calculation consequently scales every support column before
multiplication by prior weights.  Columns that are zero for every
positive-prior state have no Bayes mass; their action is explicitly completed
by the prior target mean and the resulting worst-state risk is still audited.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
from scipy.optimize import least_squares, minimize


PROBABILITY_ROW_TOLERANCE = 2.0e-12
DEFAULT_ACTIVE_PRIOR_CUTOFF = 1.0e-8
DEFAULT_PRIOR_PRUNING_CUTOFF = 1.0e-12
DEFAULT_SADDLE_GAP_TOLERANCE = 1.0e-9
DEFAULT_OPTIMIZER_TOLERANCE = 1.0e-13
DEFAULT_OPTIMIZER_MAXIMUM_ITERATIONS = 2_000
DEFAULT_OPTIMIZER_OBJECTIVE_SCALE = 1.0
DEFAULT_KKT_POLISH_RESIDUAL_SCALE = 1.0e7
DEFAULT_DETERMINISTIC_START_COUNT = 8
DEFAULT_START_SEED = 0


def _readonly(values: np.ndarray | Sequence[float]) -> np.ndarray:
    result = np.array(values, dtype=float, copy=True)
    result.setflags(write=False)
    return result


def _probability_rows(values: np.ndarray | Sequence[Sequence[float]]) -> np.ndarray:
    rows = np.asarray(values, dtype=float)
    if rows.ndim != 2 or min(rows.shape) < 1:
        raise ValueError("probability rows must be a nonempty matrix")
    if not np.all(np.isfinite(rows)) or np.any(rows < 0.0):
        raise ValueError("probability rows must be finite and nonnegative")
    sums = np.sum(rows, axis=1)
    if not np.allclose(
        sums, 1.0, rtol=0.0, atol=PROBABILITY_ROW_TOLERANCE
    ):
        raise ValueError("every observation-law row must sum to one")
    # Preserve the finite problem while removing harmless accumulated row-sum
    # roundoff from later statewise expectations.
    return np.array(rows / sums[:, np.newaxis], dtype=float, copy=True)


def _target_mids(
    values: np.ndarray | Sequence[Sequence[float]], *, state_count: int | None = None
) -> np.ndarray:
    targets = np.asarray(values, dtype=float)
    if targets.ndim != 2 or min(targets.shape) < 1:
        raise ValueError("target MIDs must be a nonempty matrix")
    if state_count is not None and targets.shape[0] != int(state_count):
        raise ValueError("target MIDs and observation laws do not align")
    if not np.all(np.isfinite(targets)) or np.any(targets < 0.0):
        raise ValueError("target MID components must be finite and nonnegative")
    if not np.allclose(
        np.sum(targets, axis=1), 1.0, rtol=0.0, atol=2.0e-12
    ):
        raise ValueError("each target MID must sum to one")
    return np.array(targets, dtype=float, copy=True)


def _prior_weights(values: np.ndarray | Sequence[float], state_count: int) -> np.ndarray:
    prior = np.asarray(values, dtype=float)
    if prior.shape != (int(state_count),):
        raise ValueError("prior weights do not align with model states")
    if not np.all(np.isfinite(prior)) or np.any(prior < -1.0e-12):
        raise ValueError("prior weights must be finite and nonnegative")
    prior = np.maximum(prior, 0.0)
    total = float(np.sum(prior))
    if not math.isfinite(total) or total <= 0.0:
        raise ValueError("prior weights must have positive total mass")
    return np.array(prior / total, dtype=float, copy=True)


def dimension_normalized_squared_mid_error(
    target: np.ndarray | Sequence[float],
    estimate: np.ndarray | Sequence[float],
) -> float | np.ndarray:
    """Return ``||target-estimate||_2^2 / d`` along the last axis."""

    truth = np.asarray(target, dtype=float)
    prediction = np.asarray(estimate, dtype=float)
    if truth.ndim < 1 or prediction.ndim < 1 or truth.shape[-1] < 1:
        raise ValueError("MID values need a nonempty component axis")
    if truth.shape[-1] != prediction.shape[-1]:
        raise ValueError("target and estimate MID dimensions differ")
    if not np.all(np.isfinite(truth)) or not np.all(np.isfinite(prediction)):
        raise ValueError("MID error inputs must be finite")
    try:
        difference = np.broadcast_arrays(truth, prediction)[0] - np.broadcast_arrays(
            truth, prediction
        )[1]
    except ValueError as error:
        raise ValueError("target and estimate arrays cannot be broadcast") from error
    result = np.mean(np.square(difference), axis=-1)
    return float(result) if np.ndim(result) == 0 else result


def robust_rmse(worst_expected_squared_mid_error: float) -> float:
    """Convert minimax component-normalised MSE to robust RMSE."""

    value = float(worst_expected_squared_mid_error)
    if not math.isfinite(value) or value < -1.0e-14:
        raise ValueError("minimax MSE must be finite and nonnegative")
    return math.sqrt(max(0.0, value))


@dataclass(frozen=True)
class SharedLawEstimationBound:
    """Exact two-state lower bound induced by one shared observation law."""

    target_rms_separation: float
    minimax_mse_lower_bound: float
    robust_rmse_lower_bound: float
    law_maximum_absolute_difference: float
    law_identity_tolerance: float
    law_identity_verified: bool


def identical_observation_law_lower_bound(
    left_probability: np.ndarray | Sequence[float],
    right_probability: np.ndarray | Sequence[float],
    left_target_mid: np.ndarray | Sequence[float],
    right_target_mid: np.ndarray | Sequence[float],
    *,
    law_tolerance: float = 0.0,
) -> SharedLawEstimationBound:
    """Return the exact ``Delta**2/4`` shared-law estimation lower bound.

    The law identity is checked separately from target geometry.  For any
    action ``a``, the parallelogram identity implies that the larger of the
    two squared target errors is at least one quarter of their squared
    separation.  Averaging under the common law preserves that bound.
    """

    left_law = np.asarray(left_probability, dtype=float)
    right_law = np.asarray(right_probability, dtype=float)
    if left_law.ndim != 1 or right_law.shape != left_law.shape or len(left_law) < 1:
        raise ValueError("shared-law rows must be aligned nonempty vectors")
    if (
        not np.all(np.isfinite(left_law))
        or not np.all(np.isfinite(right_law))
        or np.any(left_law < 0.0)
        or np.any(right_law < 0.0)
        or not math.isclose(float(np.sum(left_law)), 1.0, abs_tol=2.0e-12)
        or not math.isclose(float(np.sum(right_law)), 1.0, abs_tol=2.0e-12)
    ):
        raise ValueError("shared-law inputs must be probability vectors")
    tolerance = float(law_tolerance)
    if not math.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("law identity tolerance must be nonnegative")
    maximum = float(np.max(np.abs(left_law - right_law)))
    verified = maximum <= tolerance
    if not verified:
        raise ValueError("the two observation laws are not identical")

    targets = _target_mids(np.vstack((left_target_mid, right_target_mid)))
    separation_squared = float(
        dimension_normalized_squared_mid_error(targets[0], targets[1])
    )
    return SharedLawEstimationBound(
        target_rms_separation=math.sqrt(separation_squared),
        minimax_mse_lower_bound=separation_squared / 4.0,
        robust_rmse_lower_bound=math.sqrt(separation_squared) / 2.0,
        law_maximum_absolute_difference=maximum,
        law_identity_tolerance=tolerance,
        law_identity_verified=True,
    )


@dataclass(frozen=True)
class PosteriorMeanMIDEstimate:
    """Posterior-mean actions on one finite common observation support."""

    estimates: np.ndarray
    mixture_probabilities: np.ndarray
    zero_mixture_columns: np.ndarray
    fallback_mid: np.ndarray

    def __post_init__(self) -> None:
        object.__setattr__(self, "estimates", _readonly(self.estimates))
        object.__setattr__(
            self, "mixture_probabilities", _readonly(self.mixture_probabilities)
        )
        zero = np.array(self.zero_mixture_columns, dtype=bool, copy=True)
        zero.setflags(write=False)
        object.__setattr__(self, "zero_mixture_columns", zero)
        object.__setattr__(self, "fallback_mid", _readonly(self.fallback_mid))


def posterior_mean_mid_estimator(
    prior_weights: np.ndarray | Sequence[float],
    probability_rows: np.ndarray | Sequence[Sequence[float]],
    target_mids: np.ndarray | Sequence[Sequence[float]],
) -> PosteriorMeanMIDEstimate:
    """Evaluate the squared-error Bayes estimator on a finite support.

    Scaling each support column before multiplying by the prior prevents loss
    of symmetry for identical subnormal probability rows.
    """

    rows = _probability_rows(probability_rows)
    targets = _target_mids(target_mids, state_count=rows.shape[0])
    prior = _prior_weights(prior_weights, rows.shape[0])
    positive = prior > 0.0
    active_rows = rows[positive]
    active_prior = prior[positive]
    active_targets = targets[positive]
    column_scale = np.max(active_rows, axis=0)
    nonzero = column_scale > 0.0
    zero = ~nonzero
    fallback = prior @ targets
    estimates = np.repeat(fallback[np.newaxis, :], rows.shape[1], axis=0)
    if np.any(nonzero):
        scaled = active_rows[:, nonzero] / column_scale[nonzero]
        scores = active_prior[:, np.newaxis] * scaled
        score_sums = np.sum(scores, axis=0)
        if np.any(score_sums <= 0.0) or not np.all(np.isfinite(score_sums)):
            raise FloatingPointError("posterior score normalization failed")
        estimates[nonzero] = (scores.T @ active_targets) / score_sums[:, np.newaxis]

    # Convex combinations of valid target MIDs are valid MIDs.  Normalize a
    # final time only to remove matrix-multiplication roundoff.
    estimates = np.maximum(estimates, 0.0)
    estimates /= np.sum(estimates, axis=1, keepdims=True)
    mixture = prior @ rows
    if (
        not np.all(np.isfinite(estimates))
        or np.any(estimates < 0.0)
        or not np.allclose(np.sum(estimates, axis=1), 1.0, atol=2.0e-12)
    ):
        raise FloatingPointError("posterior estimator did not return valid MIDs")
    return PosteriorMeanMIDEstimate(estimates, mixture, zero, fallback)


def recompute_statewise_mid_risks(
    probability_rows: np.ndarray | Sequence[Sequence[float]],
    target_mids: np.ndarray | Sequence[Sequence[float]],
    estimates: np.ndarray | Sequence[Sequence[float]],
) -> np.ndarray:
    """Recompute each state's expected dimension-normalised squared error."""

    rows = _probability_rows(probability_rows)
    targets = _target_mids(target_mids, state_count=rows.shape[0])
    actions = np.asarray(estimates, dtype=float)
    if actions.shape != (rows.shape[1], targets.shape[1]):
        raise ValueError("finite estimator and model dimensions do not align")
    if not np.all(np.isfinite(actions)):
        raise ValueError("finite estimator contains non-finite values")
    losses = np.mean(
        np.square(targets[:, np.newaxis, :] - actions[np.newaxis, :, :]), axis=2
    )
    risks = np.sum(rows * losses, axis=1)
    return _readonly(risks)


def finite_bayes_mid_risk(
    prior_weights: np.ndarray | Sequence[float],
    probability_rows: np.ndarray | Sequence[Sequence[float]],
    target_mids: np.ndarray | Sequence[Sequence[float]],
) -> float:
    """Return Bayes risk after independently constructing its posterior mean."""

    rows = _probability_rows(probability_rows)
    prior = _prior_weights(prior_weights, rows.shape[0])
    posterior = posterior_mean_mid_estimator(prior, rows, target_mids)
    risks = recompute_statewise_mid_risks(rows, target_mids, posterior.estimates)
    return float(prior @ risks)


@dataclass(frozen=True)
class OptimizerStartAudit:
    start_index: int
    source: str
    success: bool
    status: int
    message: str
    iteration_count: int
    function_evaluation_count: int
    jacobian_evaluation_count: int
    optimized_bayes_risk: float
    simplex_residual: float
    minimum_weight: float


@dataclass(frozen=True)
class FiniteMinimaxMIDEstimationSolution:
    """Audited numerical saddle bracket for one finite estimation problem."""

    least_favourable_prior: np.ndarray
    estimator: np.ndarray
    statewise_risks: np.ndarray
    mixture_probabilities: np.ndarray
    zero_mixture_columns: np.ndarray
    bayes_risk_lower_bound: float
    maximum_risk_upper_bound: float
    finite_saddle_gap: float
    robust_rmse: float
    simplex_residual: float
    active_state_indices: np.ndarray
    active_prior_cutoff: float
    active_risk_equalization_residual: float
    inactive_risk_violation: float
    maximum_complementarity_residual: float
    bayes_risk_identity_residual: float
    optimisation_converged: bool
    chosen_candidate_source: str
    prior_pruning_cutoff: float
    kkt_polish_attempted: bool
    kkt_polish_success: bool
    kkt_polish_message: str
    kkt_polish_function_evaluations: int
    optimizer_runs: tuple[OptimizerStartAudit, ...]

    def __post_init__(self) -> None:
        for name in (
            "least_favourable_prior",
            "estimator",
            "statewise_risks",
            "mixture_probabilities",
        ):
            object.__setattr__(self, name, _readonly(getattr(self, name)))
        zero = np.array(self.zero_mixture_columns, dtype=bool, copy=True)
        zero.setflags(write=False)
        active = np.array(self.active_state_indices, dtype=int, copy=True)
        active.setflags(write=False)
        object.__setattr__(self, "zero_mixture_columns", zero)
        object.__setattr__(self, "active_state_indices", active)


@dataclass(frozen=True)
class _Candidate:
    prior: np.ndarray
    source: str
    posterior: PosteriorMeanMIDEstimate
    risks: np.ndarray
    bayes_risk: float
    maximum_risk: float

    @property
    def gap(self) -> float:
        return self.maximum_risk - self.bayes_risk


def _candidate(
    prior: np.ndarray,
    source: str,
    rows: np.ndarray,
    targets: np.ndarray,
) -> _Candidate:
    normalized = _prior_weights(prior, rows.shape[0])
    posterior = posterior_mean_mid_estimator(normalized, rows, targets)
    risks = recompute_statewise_mid_risks(rows, targets, posterior.estimates)
    bayes = float(normalized @ risks)
    return _Candidate(
        prior=normalized,
        source=str(source),
        posterior=posterior,
        risks=risks,
        bayes_risk=bayes,
        maximum_risk=float(np.max(risks)),
    )


def _deterministic_starts(
    targets: np.ndarray,
    *,
    start_count: int,
    seed: int,
    initial_priors: Sequence[np.ndarray | Sequence[float]] | None,
) -> tuple[tuple[str, np.ndarray], ...]:
    state_count = len(targets)
    requested = max(2, int(start_count))
    result: list[tuple[str, np.ndarray]] = [
        ("uniform", np.full(state_count, 1.0 / state_count, dtype=float))
    ]
    if state_count >= 2:
        differences = targets[:, np.newaxis, :] - targets[np.newaxis, :, :]
        distances = np.mean(np.square(differences), axis=2)
        left, right = np.unravel_index(int(np.argmax(distances)), distances.shape)
        diameter = np.zeros(state_count, dtype=float)
        diameter[int(left)] = 0.5
        diameter[int(right)] = 0.5
        result.append(("target_diameter_pair", diameter))
    if initial_priors is not None:
        result.extend(
            (f"caller_{index}", _prior_weights(values, state_count))
            for index, values in enumerate(initial_priors)
        )
    rng = np.random.default_rng(int(seed))
    while len(result) < requested:
        result.append(
            (f"deterministic_dirichlet_{len(result)}", rng.dirichlet(np.ones(state_count)))
        )
    deduplicated: list[tuple[str, np.ndarray]] = []
    seen: set[bytes] = set()
    for source, values in result:
        normalized = _prior_weights(values, state_count)
        key = np.round(normalized, decimals=15).tobytes()
        if key not in seen:
            seen.add(key)
            deduplicated.append((source, normalized))
    return tuple(deduplicated)


def solve_finite_minimax_mid_estimation(
    probability_rows: np.ndarray | Sequence[Sequence[float]],
    target_mids: np.ndarray | Sequence[Sequence[float]],
    *,
    initial_priors: Sequence[np.ndarray | Sequence[float]] | None = None,
    deterministic_start_count: int = DEFAULT_DETERMINISTIC_START_COUNT,
    start_seed: int = DEFAULT_START_SEED,
    optimizer_tolerance: float = DEFAULT_OPTIMIZER_TOLERANCE,
    optimizer_maximum_iterations: int = DEFAULT_OPTIMIZER_MAXIMUM_ITERATIONS,
    optimizer_objective_scale: float = DEFAULT_OPTIMIZER_OBJECTIVE_SCALE,
    kkt_polish_residual_scale: float = DEFAULT_KKT_POLISH_RESIDUAL_SCALE,
    active_prior_cutoff: float = DEFAULT_ACTIVE_PRIOR_CUTOFF,
    prior_pruning_cutoff: float = DEFAULT_PRIOR_PRUNING_CUTOFF,
    saddle_gap_tolerance: float = DEFAULT_SADDLE_GAP_TOLERANCE,
) -> FiniteMinimaxMIDEstimationSolution:
    """Numerically maximize finite Bayes risk over the probability simplex.

    Multiple deterministic SLSQP starts use explicit equality and bound
    constraints.  Caller-supplied analytical-control starts are admitted but
    never accepted without the same independently recomputed state-risk and
    saddle-gap audit as every optimizer result.
    """

    rows = _probability_rows(probability_rows)
    targets = _target_mids(target_mids, state_count=rows.shape[0])
    state_count = len(rows)
    active_cutoff = float(active_prior_cutoff)
    pruning_cutoff = float(prior_pruning_cutoff)
    gap_tolerance = float(saddle_gap_tolerance)
    objective_scale = float(optimizer_objective_scale)
    polish_scale = float(kkt_polish_residual_scale)
    if (
        active_cutoff < 0.0
        or pruning_cutoff < 0.0
        or gap_tolerance < 0.0
        or not all(math.isfinite(x) for x in (active_cutoff, pruning_cutoff, gap_tolerance))
        or not math.isfinite(objective_scale)
        or objective_scale <= 0.0
        or not math.isfinite(polish_scale)
        or polish_scale <= 0.0
    ):
        raise ValueError("solver tolerances must be finite and nonnegative")

    if state_count == 1:
        chosen = _candidate(np.ones(1), "single_state_exact", rows, targets)
        audits: tuple[OptimizerStartAudit, ...] = ()
        optimizer_success = True
        polish_attempted = False
        polish_success = True
        polish_message = "single-state problem needs no KKT polishing"
        polish_evaluations = 0
    else:
        starts = _deterministic_starts(
            targets,
            start_count=int(deterministic_start_count),
            seed=int(start_seed),
            initial_priors=initial_priors,
        )
        audits_list: list[OptimizerStartAudit] = []
        candidates: list[_Candidate] = []

        def evaluate(prior: np.ndarray) -> tuple[float, np.ndarray]:
            item = _candidate(prior, "optimizer_evaluation", rows, targets)
            return item.bayes_risk, np.asarray(item.risks, dtype=float)

        constraint = {
            "type": "eq",
            "fun": lambda values: float(np.sum(values) - 1.0),
            "jac": lambda values: np.ones_like(values),
        }
        for start_index, (source, start) in enumerate(starts):
            candidates.append(_candidate(start, f"{source}:initial", rows, targets))

            def objective(values: np.ndarray) -> float:
                return -objective_scale * evaluate(values)[0]

            def jacobian(values: np.ndarray) -> np.ndarray:
                # Envelope theorem: gradient B(lambda) is statewise Bayes risk
                # wherever the mixture law is positive.  Boundary candidates
                # are independently re-audited below.
                return -objective_scale * evaluate(values)[1]

            result = minimize(
                objective,
                start,
                jac=jacobian,
                method="SLSQP",
                bounds=tuple((0.0, 1.0) for _ in range(state_count)),
                constraints=(constraint,),
                options={
                    "ftol": float(optimizer_tolerance),
                    "maxiter": int(optimizer_maximum_iterations),
                    "disp": False,
                },
            )
            optimized_prior = _prior_weights(result.x, state_count)
            optimized = _candidate(
                optimized_prior, f"{source}:optimized", rows, targets
            )
            candidates.append(optimized)
            if pruning_cutoff > 0.0:
                pruned = np.where(optimized_prior < pruning_cutoff, 0.0, optimized_prior)
                if float(np.sum(pruned)) > 0.0:
                    candidates.append(
                        _candidate(pruned, f"{source}:optimized_pruned", rows, targets)
                    )
            audits_list.append(
                OptimizerStartAudit(
                    start_index=start_index,
                    source=source,
                    success=bool(result.success),
                    status=int(result.status),
                    message=str(result.message),
                    iteration_count=int(getattr(result, "nit", 0)),
                    function_evaluation_count=int(getattr(result, "nfev", 0)),
                    jacobian_evaluation_count=int(getattr(result, "njev", 0)),
                    optimized_bayes_risk=optimized.bayes_risk,
                    simplex_residual=abs(float(np.sum(optimized_prior)) - 1.0),
                    minimum_weight=float(np.min(optimized_prior)),
                )
            )

        maximum_bayes = max(item.bayes_risk for item in candidates)
        selection_tolerance = max(1.0e-12, 10.0 * float(optimizer_tolerance))
        eligible = [
            item
            for item in candidates
            if item.bayes_risk >= maximum_bayes - selection_tolerance
        ]
        chosen = min(
            eligible,
            key=lambda item: (
                max(0.0, item.gap),
                -item.bayes_risk,
                int(np.count_nonzero(item.prior > active_cutoff)),
                item.source,
            ),
        )
        audits = tuple(audits_list)
        optimizer_success = any(item.success for item in audits)

        # SLSQP can maximize the Bayes objective accurately while leaving a
        # visibly non-equal risk vector when the optimum risk itself is tiny.
        # The KKT identity supplies a small, source-agnostic polishing system:
        # on the candidate active set solve R_i(lambda)-R_ref(lambda)=0 using
        # a softmax simplex parameterization, then retain the result only after
        # the same Bayes/maximum-risk bracket audit used for every candidate.
        polish_attempted = chosen.gap > gap_tolerance
        polish_success = not polish_attempted
        polish_message = "finite saddle gap already passed"
        polish_evaluations = 0
        if polish_attempted:
            active_for_polish = np.flatnonzero(chosen.prior > pruning_cutoff)
            if len(active_for_polish) < 2:
                polish_message = "fewer than two positive candidate weights"
            else:
                reference = int(active_for_polish[-1])
                initial_logits = np.log(
                    chosen.prior[active_for_polish[:-1]]
                    / chosen.prior[reference]
                )

                def prior_from_logits(logits: np.ndarray) -> np.ndarray:
                    augmented = np.concatenate((np.asarray(logits, dtype=float), [0.0]))
                    augmented -= float(np.max(augmented))
                    weights = np.exp(augmented)
                    weights /= np.sum(weights)
                    result = np.zeros(state_count, dtype=float)
                    result[active_for_polish] = weights
                    return result

                def equalization_residual(logits: np.ndarray) -> np.ndarray:
                    current = _candidate(
                        prior_from_logits(logits),
                        "kkt_polish_evaluation",
                        rows,
                        targets,
                    )
                    return polish_scale * (
                        current.risks[active_for_polish[:-1]]
                        - current.risks[reference]
                    )

                polished = least_squares(
                    equalization_residual,
                    initial_logits,
                    xtol=1.0e-13,
                    ftol=1.0e-13,
                    gtol=1.0e-13,
                    max_nfev=5_000,
                )
                polish_success = bool(polished.success)
                polish_message = str(polished.message)
                polish_evaluations = int(polished.nfev)
                polished_candidate = _candidate(
                    prior_from_logits(polished.x),
                    f"{chosen.source}:kkt_polished",
                    rows,
                    targets,
                )
                if (
                    polished_candidate.bayes_risk
                    >= chosen.bayes_risk - selection_tolerance
                    and polished_candidate.gap < chosen.gap
                ):
                    chosen = polished_candidate

    prior = chosen.prior
    risks = np.asarray(chosen.risks, dtype=float)
    bayes = float(prior @ risks)
    maximum = float(np.max(risks))
    active = np.flatnonzero(prior > active_cutoff)
    inactive = np.flatnonzero(prior <= active_cutoff)
    active_equalization = (
        0.0 if len(active) == 0 else float(np.max(np.abs(risks[active] - bayes)))
    )
    inactive_violation = (
        0.0
        if len(inactive) == 0
        else max(0.0, float(np.max(risks[inactive] - bayes)))
    )
    complementarity = float(np.max(prior * np.abs(risks - bayes)))
    simplex_residual = abs(float(np.sum(prior)) - 1.0)
    identity_residual = abs(chosen.bayes_risk - bayes)
    finite_gap = maximum - bayes
    converged = bool(
        optimizer_success
        and simplex_residual <= 1.0e-10
        and finite_gap <= gap_tolerance
        and active_equalization <= max(1.0e-8, 10.0 * gap_tolerance)
        and inactive_violation <= max(1.0e-8, 10.0 * gap_tolerance)
    )
    return FiniteMinimaxMIDEstimationSolution(
        least_favourable_prior=prior,
        estimator=chosen.posterior.estimates,
        statewise_risks=risks,
        mixture_probabilities=chosen.posterior.mixture_probabilities,
        zero_mixture_columns=chosen.posterior.zero_mixture_columns,
        bayes_risk_lower_bound=bayes,
        maximum_risk_upper_bound=maximum,
        finite_saddle_gap=finite_gap,
        robust_rmse=robust_rmse(maximum),
        simplex_residual=simplex_residual,
        active_state_indices=active,
        active_prior_cutoff=active_cutoff,
        active_risk_equalization_residual=active_equalization,
        inactive_risk_violation=inactive_violation,
        maximum_complementarity_residual=complementarity,
        bayes_risk_identity_residual=identity_residual,
        optimisation_converged=converged,
        chosen_candidate_source=chosen.source,
        prior_pruning_cutoff=pruning_cutoff,
        kkt_polish_attempted=polish_attempted,
        kkt_polish_success=polish_success,
        kkt_polish_message=polish_message,
        kkt_polish_function_evaluations=polish_evaluations,
        optimizer_runs=audits,
    )


@dataclass(frozen=True)
class EstimabilityCount:
    threshold: float
    target_count: int
    estimable_count: int


def estimability_threshold_counts(
    robust_rmses: Sequence[float] | np.ndarray,
    thresholds: Sequence[float] | np.ndarray,
    *,
    comparison_tolerance: float = 1.0e-12,
) -> tuple[EstimabilityCount, ...]:
    """Count targets whose robust RMSE is no larger than each threshold."""

    errors = np.asarray(robust_rmses, dtype=float)
    levels = np.asarray(thresholds, dtype=float)
    tolerance = float(comparison_tolerance)
    if errors.ndim != 1 or levels.ndim != 1 or len(levels) < 1:
        raise ValueError("robust RMSEs and thresholds must be one-dimensional")
    if (
        not np.all(np.isfinite(errors))
        or np.any(errors < 0.0)
        or not np.all(np.isfinite(levels))
        or np.any(levels < 0.0)
        or not math.isfinite(tolerance)
        or tolerance < 0.0
    ):
        raise ValueError("estimability inputs must be finite and nonnegative")
    return tuple(
        EstimabilityCount(
            threshold=float(level),
            target_count=len(errors),
            estimable_count=int(np.count_nonzero(errors <= level + tolerance)),
        )
        for level in levels
    )


__all__ = [
    "DEFAULT_ACTIVE_PRIOR_CUTOFF",
    "DEFAULT_DETERMINISTIC_START_COUNT",
    "DEFAULT_OPTIMIZER_MAXIMUM_ITERATIONS",
    "DEFAULT_OPTIMIZER_OBJECTIVE_SCALE",
    "DEFAULT_KKT_POLISH_RESIDUAL_SCALE",
    "DEFAULT_OPTIMIZER_TOLERANCE",
    "DEFAULT_PRIOR_PRUNING_CUTOFF",
    "DEFAULT_SADDLE_GAP_TOLERANCE",
    "EstimabilityCount",
    "FiniteMinimaxMIDEstimationSolution",
    "OptimizerStartAudit",
    "PosteriorMeanMIDEstimate",
    "SharedLawEstimationBound",
    "dimension_normalized_squared_mid_error",
    "estimability_threshold_counts",
    "finite_bayes_mid_risk",
    "identical_observation_law_lower_bound",
    "posterior_mean_mid_estimator",
    "recompute_statewise_mid_risks",
    "robust_rmse",
    "solve_finite_minimax_mid_estimation",
]
