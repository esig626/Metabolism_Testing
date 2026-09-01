"""Product-multinomial observation laws for direct MID testing.

The objects in this module start at the observable boundary.  They contain
integer count depth, a fixed MID block schema, and exact noise-free MID
probabilities; they contain no fluxes, state objectives, or inverse-MFA
quantities.  Exact zero probabilities are preserved and handled with the
usual extended log-PMF conventions.

The proposal and deployable-rule helpers mirror the audited Control 0
product-Dirichlet workflow, but retain the discrete count representation.
Proposal component weights are numerical integration choices, not priors on
the represented state laws.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
from numbers import Integral
import struct
from typing import Any, Sequence

import numpy as np
from scipy.special import gammaln, logsumexp

from .composite_mid_minimax import (
    ContinuousRepresentationUnavailable,
    FiniteMinimaxSolution,
    MinimaxNumericalError,
)


SIMPLEX_CLOSURE_POLICY = "last_coordinate_fsum_closure_v1"
SIMPLEX_CLOSURE_TOLERANCE = 64.0 * np.finfo(np.float64).eps
PROBABILITY_BLOCK_HASH_POLICY = "sha256_float64le_block_v1"
EFFECTIVE_KERNEL_HASH_POLICY = "sha256_ordered_effective_blocks_v1"
PRODUCT_MULTINOMIAL_SAMPLER_POLICY = "sequential_conditional_binomial_v1"
_BLOCK_HASH_DOMAIN = b"fluxemu_probability_block_float64le_v1\0"
_KERNEL_HASH_DOMAIN = b"fluxemu_effective_kernel_v1\0"


@dataclass(frozen=True)
class LastCoordinateClosure:
    """Audited raw/effective views of one deterministically closed simplex block."""

    raw: np.ndarray
    effective: np.ndarray
    raw_sum: float
    raw_normalisation_residual: float
    raw_final_coordinate: float
    effective_final_coordinate: float
    signed_delta: float
    absolute_delta: float
    support_changed: bool
    raw_block_hash: str
    effective_block_hash: str


def probability_block_hash(probabilities: np.ndarray | Sequence[float]) -> str:
    """Hash canonical float64 block bits with an explicit, portable framing.

    The payload is the ASCII domain ``fluxemu_probability_block_float64le_v1``
    followed by NUL, the dimension as an unsigned little-endian 64-bit integer,
    and the contiguous IEEE-754 binary64 little-endian coordinates.  Signed zero
    is canonicalised before hashing; no other coordinate is changed.
    """

    values = np.array(probabilities, dtype=np.float64, copy=True)
    if values.ndim != 1:
        raise ValueError("a probability block hash requires one vector")
    if not np.all(np.isfinite(values)):
        raise ValueError("a probability block hash requires finite coordinates")
    values[values == 0.0] = 0.0
    payload = (
        _BLOCK_HASH_DOMAIN
        + struct.pack("<Q", len(values))
        + np.asarray(values, dtype="<f8").tobytes(order="C")
    )
    return hashlib.sha256(payload).hexdigest()


def effective_kernel_hash(
    records: Sequence[tuple[str, str, str, int, str]],
) -> str:
    """Hash ordered effective block identities and block digests.

    Each record is ``(condition, state_id, lower-case target, dimension,
    effective_block_hash)``.  Text fields are UTF-8 with unsigned little-endian
    64-bit length framing; the dimension has the same integer framing and the
    block digest is appended as its 32 raw bytes.
    """

    digest = hashlib.sha256()
    digest.update(_KERNEL_HASH_DOMAIN)
    for condition, state_id, target, dimension, block_hash in records:
        for value in (condition, state_id, target):
            encoded = str(value).encode("utf-8")
            digest.update(struct.pack("<Q", len(encoded)))
            digest.update(encoded)
        size = int(dimension)
        if size < 1:
            raise ValueError("effective-kernel block dimension must be positive")
        digest.update(struct.pack("<Q", size))
        try:
            block_digest = bytes.fromhex(str(block_hash))
        except ValueError as error:
            raise ValueError("effective block hash is not hexadecimal") from error
        if len(block_digest) != hashlib.sha256().digest_size:
            raise ValueError("effective block hash is not a SHA-256 digest")
        digest.update(block_digest)
    return digest.hexdigest()


def last_coordinate_fsum_closure(
    probabilities: np.ndarray | Sequence[float],
    *,
    tolerance: float = SIMPLEX_CLOSURE_TOLERANCE,
) -> LastCoordinateClosure:
    """Construct the authorized effective simplex block without smoothing.

    All non-final coordinates retain their exact loaded float64 bit patterns.
    The already-positive final coordinate alone is replaced by
    ``1.0 - math.fsum(raw[:-1])``.  The strict machine-scale gates deliberately
    reject global renormalisation, floors, pseudocounts, and support changes.
    """

    limit = float(tolerance)
    if not math.isfinite(limit) or limit < 0.0:
        raise ValueError("simplex closure tolerance must be finite and nonnegative")
    raw = np.array(probabilities, dtype=np.float64, copy=True)
    if raw.ndim != 1 or len(raw) < 2:
        raise ValueError("simplex closure requires one block with at least two coordinates")
    if not np.all(np.isfinite(raw)):
        raise ValueError("raw simplex coordinates must be finite")
    raw[raw == 0.0] = 0.0
    if np.any(raw < 0.0):
        raise ValueError("raw simplex coordinates must be nonnegative")
    raw_sum = math.fsum(float(value) for value in raw)
    raw_residual = raw_sum - 1.0
    if abs(raw_residual) > limit:
        raise ValueError("raw simplex normalisation residual exceeds closure tolerance")
    if not float(raw[-1]) > 0.0:
        raise ValueError("raw final simplex coordinate must be strictly positive")

    effective = raw.copy()
    effective[-1] = 1.0 - math.fsum(float(value) for value in effective[:-1])
    if not math.isfinite(float(effective[-1])) or not float(effective[-1]) > 0.0:
        raise ValueError("effective final simplex coordinate must be finite and positive")
    delta = float(effective[-1] - raw[-1])
    if abs(delta) > limit:
        raise ValueError("effective final-coordinate delta exceeds closure tolerance")
    if not np.array_equal(effective[:-1], raw[:-1]):
        raise RuntimeError("simplex closure changed a non-final coordinate")
    expected_final = 1.0 - math.fsum(float(value) for value in effective[:-1])
    if float(effective[-1]) != expected_final:
        raise RuntimeError("stored effective final coordinate fails the closure formula")
    if not np.all(np.isfinite(effective)) or np.any(effective < 0.0):
        raise ValueError("effective simplex coordinates must be finite and nonnegative")
    support_changed = not np.array_equal(raw > 0.0, effective > 0.0)
    if support_changed:
        raise ValueError("simplex closure changed the probability support")
    # Back the returned audit views with immutable ``bytes``.  Merely setting
    # ``WRITEABLE=False`` on an owning ndarray is reversible by callers and
    # would make a frozen closure record mutable in practice.
    raw = _immutable_array(raw, np.float64)
    effective = _immutable_array(effective, np.float64)
    return LastCoordinateClosure(
        raw=raw,
        effective=effective,
        raw_sum=raw_sum,
        raw_normalisation_residual=raw_residual,
        raw_final_coordinate=float(raw[-1]),
        effective_final_coordinate=float(effective[-1]),
        signed_delta=delta,
        absolute_delta=abs(delta),
        support_changed=False,
        raw_block_hash=probability_block_hash(raw),
        effective_block_hash=probability_block_hash(effective),
    )


def _validate_depth(n_count: int) -> int:
    if (
        not isinstance(n_count, Integral)
        or isinstance(n_count, (bool, np.bool_))
        or int(n_count) < 1
    ):
        raise ValueError("N_count must be a positive integer")
    return int(n_count)


def _immutable_array(
    values: np.ndarray | Sequence[float] | Sequence[int],
    dtype: np.dtype[Any] | type[np.float64] | type[np.int64],
) -> np.ndarray:
    """Return a C-contiguous array whose write flag cannot be re-enabled.

    NumPy arrays that own their allocation can usually be made writeable again
    after ``setflags(write=False)``.  Constructing the public view from an
    immutable ``bytes`` buffer makes immutability an enforced property rather
    than a convention.
    """

    contiguous = np.ascontiguousarray(np.array(values, dtype=dtype, copy=True))
    result = np.frombuffer(contiguous.tobytes(order="C"), dtype=contiguous.dtype)
    return result.reshape(contiguous.shape)


def _readonly_float(values: np.ndarray | Sequence[float]) -> np.ndarray:
    result = np.array(values, dtype=np.float64, copy=True)
    result[result == 0.0] = 0.0  # canonicalise signed zero, without smoothing
    return _immutable_array(result, np.float64)


def _readonly_int(values: np.ndarray | Sequence[int]) -> np.ndarray:
    return _immutable_array(values, np.int64)


def _block_slices(block_sizes: Sequence[int]) -> tuple[slice, ...]:
    cursor = 0
    result: list[slice] = []
    for raw_size in block_sizes:
        size = int(raw_size)
        result.append(slice(cursor, cursor + size))
        cursor += size
    return tuple(result)


def _validate_schema(
    block_names: Sequence[str], block_sizes: Sequence[int]
) -> tuple[tuple[str, ...], tuple[int, ...]]:
    names = tuple(str(value) for value in block_names)
    raw_sizes = tuple(block_sizes)
    if any(
        not isinstance(value, Integral) or isinstance(value, (bool, np.bool_))
        for value in raw_sizes
    ):
        raise ValueError("product-multinomial block sizes must be integers")
    sizes = tuple(int(value) for value in raw_sizes)
    if not names or len(names) != len(sizes):
        raise ValueError("block names and sizes must be nonempty and aligned")
    if len(set(names)) != len(names) or any(value < 2 for value in sizes):
        raise ValueError("product-multinomial block schema is invalid")
    return names, sizes


def _validate_probability_rows(
    probabilities: np.ndarray | Sequence[float],
    block_sizes: Sequence[int],
    *,
    require_rows: bool = True,
) -> np.ndarray:
    sizes = tuple(int(value) for value in block_sizes)
    values = np.array(probabilities, dtype=float, copy=True)
    if values.ndim == 1:
        values = values[np.newaxis, :]
    if values.ndim != 2 or values.shape[1] != sum(sizes):
        raise ValueError("multinomial probabilities have unexpected shape")
    if require_rows and len(values) < 1:
        raise ValueError("at least one probability row is required")
    if not np.all(np.isfinite(values)) or np.any(values < 0.0):
        raise ValueError("multinomial probabilities must be finite and nonnegative")
    # This changes only the sign bit of exact zero.
    values[values == 0.0] = 0.0
    for block in _block_slices(sizes):
        for row in values[:, block]:
            expected_final = 1.0 - math.fsum(float(value) for value in row[:-1])
            if not expected_final > 0.0 or float(row[-1]) != expected_final:
                raise ValueError(
                    "every multinomial probability block must satisfy the "
                    "last-coordinate simplex closure"
                )
    return values


def validate_multinomial_counts(
    counts: np.ndarray | Sequence[int],
    block_sizes: Sequence[int],
    n_count: int,
    *,
    require_nonempty: bool = True,
) -> np.ndarray:
    """Validate count panels without changing any coordinate."""

    depth = _validate_depth(n_count)
    sizes = tuple(int(value) for value in block_sizes)
    raw = np.asarray(counts)
    if raw.ndim == 1:
        raw = raw[np.newaxis, :]
    if raw.ndim != 2 or raw.shape[1] != sum(sizes):
        raise ValueError("count panels have unexpected shape")
    if require_nonempty and len(raw) < 1:
        raise ValueError("at least one count panel is required")
    if not np.issubdtype(raw.dtype, np.number) or not np.all(np.isfinite(raw)):
        raise ValueError("multinomial counts must be finite numbers")
    rounded = np.rint(raw)
    if not np.array_equal(np.asarray(raw, dtype=float), rounded):
        raise ValueError("multinomial counts must be integers")
    values = np.asarray(rounded, dtype=np.int64)
    if np.any(values < 0):
        raise ValueError("multinomial counts must be nonnegative")
    for block in _block_slices(sizes):
        if np.any(np.sum(values[:, block], axis=1) != depth):
            raise ValueError("each multinomial count block must total N_count")
    return values


def multinomial_mids_from_counts(
    counts: np.ndarray | Sequence[int],
    block_sizes: Sequence[int],
    n_count: int,
) -> np.ndarray:
    """Return the exactly equivalent normalized MID panels ``C/N_count``."""

    depth = _validate_depth(n_count)
    return validate_multinomial_counts(counts, block_sizes, depth).astype(float) / depth


def multinomial_counts_from_mids(
    mids: np.ndarray | Sequence[float],
    block_sizes: Sequence[int],
    n_count: int,
    *,
    tolerance: float = 2.0e-12,
) -> np.ndarray:
    """Recover integer panels only when normalized MIDs are exactly compatible."""

    depth = _validate_depth(n_count)
    values = np.asarray(mids, dtype=float)
    if values.ndim == 1:
        values = values[np.newaxis, :]
    if values.ndim != 2 or values.shape[1] != sum(int(x) for x in block_sizes):
        raise ValueError("normalized MID panels have unexpected shape")
    if not np.all(np.isfinite(values)) or np.any(values < 0.0):
        raise ValueError("normalized MID panels must be finite and nonnegative")
    scaled = values * depth
    counts = np.rint(scaled)
    if not np.allclose(scaled, counts, rtol=0.0, atol=float(tolerance)):
        raise ValueError("normalized MID panel is not an N_count count panel")
    validated = validate_multinomial_counts(counts, block_sizes, depth)
    reproduced = validated.astype(float) / depth
    if not np.allclose(values, reproduced, rtol=0.0, atol=float(tolerance)):
        raise ValueError("normalized MID panel cannot be reproduced from counts")
    return validated


def _categorical_kl(q: np.ndarray, p: np.ndarray) -> float:
    positive_q = q > 0.0
    if np.any(positive_q & (p == 0.0)):
        return math.inf
    return float(np.sum(q[positive_q] * (np.log(q[positive_q]) - np.log(p[positive_q]))))


def categorical_kl_divergence(
    q: Sequence[float], p: Sequence[float]
) -> float:
    """Return ``D(q || p)`` with exact extended support conventions."""

    q_values = _validate_probability_rows(q, (len(q),))[0]
    p_values = _validate_probability_rows(p, (len(p),))[0]
    if q_values.shape != p_values.shape:
        raise ValueError("categorical probability vectors have different shapes")
    return _categorical_kl(q_values, p_values)


def categorical_renyi_divergence(
    q: Sequence[float], p: Sequence[float], order: float
) -> float:
    """Return ``D_order(q || p)`` for positive order other than one."""

    lam = float(order)
    if not math.isfinite(lam) or lam <= 0.0 or lam == 1.0:
        raise ValueError("Renyi order must be positive, finite, and different from one")
    q_values = _validate_probability_rows(q, (len(q),))[0]
    p_values = _validate_probability_rows(p, (len(p),))[0]
    if q_values.shape != p_values.shape:
        raise ValueError("categorical probability vectors have different shapes")
    if lam > 1.0 and np.any((q_values > 0.0) & (p_values == 0.0)):
        return math.inf
    valid = (q_values > 0.0) & (p_values > 0.0)
    if not np.any(valid):
        return math.inf
    log_affinity = float(
        logsumexp(lam * np.log(q_values[valid]) + (1.0 - lam) * np.log(p_values[valid]))
    )
    return log_affinity / (lam - 1.0)


def product_multinomial_kl_divergence(
    q: Sequence[float],
    p: Sequence[float],
    block_sizes: Sequence[int],
    n_count: int,
) -> float:
    """Analytic KL for equal-depth independent multinomial MID blocks."""

    q_values = _validate_probability_rows(q, block_sizes)[0]
    p_values = _validate_probability_rows(p, block_sizes)[0]
    total = 0.0
    for block in _block_slices(block_sizes):
        value = _categorical_kl(q_values[block], p_values[block])
        if math.isinf(value):
            return math.inf
        total += value
    return _validate_depth(n_count) * total


def product_multinomial_renyi_divergence(
    q: Sequence[float],
    p: Sequence[float],
    block_sizes: Sequence[int],
    n_count: int,
    order: float,
) -> float:
    """Analytic Renyi divergence, tensorized in depth and across blocks."""

    q_values = _validate_probability_rows(q, block_sizes)[0]
    p_values = _validate_probability_rows(p, block_sizes)[0]
    total = 0.0
    for block in _block_slices(block_sizes):
        value = categorical_renyi_divergence(
            q_values[block], p_values[block], order
        )
        if math.isinf(value):
            return math.inf
        total += value
    return _validate_depth(n_count) * total


def _log_lr_factor(
    base: np.ndarray, numerator: np.ndarray, denominator: np.ndarray, power: float
) -> float:
    terms: list[float] = []
    for r, q, p in zip(base, numerator, denominator, strict=True):
        if r == 0.0:
            continue
        if q == 0.0 and p == 0.0:
            return math.inf
        if q == 0.0:
            if power < 0.0:
                return math.inf
            continue
        if p == 0.0:
            if power > 0.0:
                return math.inf
            continue
        terms.append(math.log(float(r)) + power * (math.log(float(q)) - math.log(float(p))))
    if not terms:
        return -math.inf
    return float(logsumexp(np.asarray(terms, dtype=float)))


def product_multinomial_log_lr_moment(
    base: Sequence[float],
    numerator: Sequence[float],
    denominator: Sequence[float],
    block_sizes: Sequence[int],
    n_count: int,
    power: float,
) -> float:
    """Return ``log E_base exp(power*(log q-log p))`` analytically."""

    exponent = float(power)
    if not math.isfinite(exponent) or exponent == 0.0:
        if exponent == 0.0:
            return 0.0
        raise ValueError("likelihood-ratio moment power must be finite")
    r_values = _validate_probability_rows(base, block_sizes)[0]
    q_values = _validate_probability_rows(numerator, block_sizes)[0]
    p_values = _validate_probability_rows(denominator, block_sizes)[0]
    total = 0.0
    for block in _block_slices(block_sizes):
        factor = _log_lr_factor(
            r_values[block], q_values[block], p_values[block], exponent
        )
        if math.isinf(factor):
            return factor
        total += factor
    return _validate_depth(n_count) * total


@dataclass(frozen=True)
class ProductMultinomialMIDLaw:
    """One immutable product-multinomial law on an ordered MID panel."""

    member_id: str
    block_names: tuple[str, ...]
    block_sizes: tuple[int, ...]
    probabilities: np.ndarray
    n_count: int

    def __post_init__(self) -> None:
        names, sizes = _validate_schema(self.block_names, self.block_sizes)
        depth = _validate_depth(self.n_count)
        values = _immutable_array(
            _validate_probability_rows(self.probabilities, sizes)[0], np.float64
        )
        if not str(self.member_id):
            raise ValueError("law member identifier must be nonempty")
        object.__setattr__(self, "member_id", str(self.member_id))
        object.__setattr__(self, "block_names", names)
        object.__setattr__(self, "block_sizes", sizes)
        object.__setattr__(self, "probabilities", values)
        object.__setattr__(self, "n_count", depth)

    @property
    def observation_dimension(self) -> int:
        return sum(self.block_sizes)

    @property
    def block_slices(self) -> tuple[slice, ...]:
        return _block_slices(self.block_sizes)

    @property
    def support_mask(self) -> np.ndarray:
        result = self.probabilities > 0.0
        result.setflags(write=False)
        return result

    @property
    def exact_mean(self) -> np.ndarray:
        """Mean of the reported normalized MIDs, equal to the frozen centre."""

        return self.probabilities

    @property
    def p_effective(self) -> np.ndarray:
        """The immutable effective kernel used by every law calculation."""

        return self.probabilities

    @property
    def mean_counts(self) -> np.ndarray:
        return _readonly_float(self.n_count * self.probabilities)

    @property
    def covariance_blocks(self) -> tuple[np.ndarray, ...]:
        """Within-block covariance matrices of ``Y=C/N_count``."""

        result: list[np.ndarray] = []
        for block in self.block_slices:
            p = self.probabilities[block]
            covariance = (np.diag(p) - np.outer(p, p)) / self.n_count
            covariance.setflags(write=False)
            result.append(covariance)
        return tuple(result)

    @property
    def fingerprint(self) -> str:
        payload = {
            "law": "product_multinomial_mid_v1",
            "block_names": self.block_names,
            "block_sizes": self.block_sizes,
            "n_count": self.n_count,
            "probabilities_hex": tuple(float(value).hex() for value in self.probabilities),
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(encoded).hexdigest()

    def sample(self, count: int, rng: np.random.Generator) -> np.ndarray:
        if not isinstance(count, Integral):
            raise ValueError("sample count must be a positive integer")
        sample_count = int(count)
        if sample_count < 1:
            raise ValueError("sample count must be a positive integer")
        if not isinstance(rng, np.random.Generator):
            raise TypeError("sampling requires an explicit numpy Generator")
        result = np.empty((sample_count, self.observation_dimension), dtype=np.int64)
        for block in self.block_slices:
            p = self.probabilities[block]
            block_result = result[:, block]
            remaining_count = np.full(sample_count, self.n_count, dtype=np.int64)
            remaining_probability = 1.0
            for local_index in range(len(p) - 1):
                probability = float(p[local_index])
                if probability == 0.0:
                    draw = np.zeros(sample_count, dtype=np.int64)
                else:
                    conditional_probability = probability / remaining_probability
                    if not 0.0 < conditional_probability <= 1.0:
                        raise MinimaxNumericalError(
                            "invalid sequential conditional-binomial probability"
                        )
                    if conditional_probability == 1.0:
                        draw = remaining_count.copy()
                    else:
                        draw = np.asarray(
                            rng.binomial(remaining_count, conditional_probability),
                            dtype=np.int64,
                        )
                block_result[:, local_index] = draw
                remaining_count -= draw
                remaining_probability = 1.0 - math.fsum(
                    float(value) for value in p[: local_index + 1]
                )
                if not remaining_probability > 0.0:
                    raise MinimaxNumericalError(
                        "sequential multinomial sampler exhausted probability early"
                    )
            block_result[:, -1] = remaining_count
        return validate_multinomial_counts(result, self.block_sizes, self.n_count)

    def support_contains(self, counts: np.ndarray | Sequence[int]) -> np.ndarray:
        values = validate_multinomial_counts(counts, self.block_sizes, self.n_count)
        return ~np.any((values > 0) & (self.probabilities == 0.0), axis=1)

    def log_pmf(self, counts: np.ndarray | Sequence[int]) -> np.ndarray:
        return _family_log_pmf(
            self.probabilities[np.newaxis, :],
            self.block_sizes,
            self.n_count,
            counts,
        )[0]

    def likelihood_ratio_score(
        self,
        denominator: "ProductMultinomialMIDLaw",
        counts: np.ndarray | Sequence[int],
    ) -> np.ndarray:
        if (
            self.block_names != denominator.block_names
            or self.block_sizes != denominator.block_sizes
            or self.n_count != denominator.n_count
        ):
            raise ValueError("likelihood-ratio laws use different observation schemas")
        numerator_log_pmf = self.log_pmf(counts)
        denominator_log_pmf = denominator.log_pmf(counts)
        common_zero = np.isneginf(numerator_log_pmf) & np.isneginf(
            denominator_log_pmf
        )
        if np.any(common_zero):
            # A literal 0/0 likelihood ratio has no canonical finite value.
            # A projected theorem must instead declare and audit a measurable
            # extension on any such represented-law support.  Refusing to
            # manufacture a value here prevents silent theorem certification.
            raise ValueError(
                "likelihood ratio is undefined where both selected laws have zero PMF"
            )
        with np.errstate(invalid="ignore"):
            result = numerator_log_pmf - denominator_log_pmf
        if np.any(np.isnan(result)):
            raise MinimaxNumericalError("likelihood-ratio score produced NaN")
        return result

    def kl_divergence(self, denominator: "ProductMultinomialMIDLaw") -> float:
        """Return analytic ``D(self || denominator)`` in count space."""

        self._require_matching_schema(denominator, "KL")
        return product_multinomial_kl_divergence(
            self.probabilities,
            denominator.probabilities,
            self.block_sizes,
            self.n_count,
        )

    def renyi_divergence(
        self, denominator: "ProductMultinomialMIDLaw", order: float
    ) -> float:
        """Return analytic ``D_order(self || denominator)`` in count space."""

        self._require_matching_schema(denominator, "Renyi")
        return product_multinomial_renyi_divergence(
            self.probabilities,
            denominator.probabilities,
            self.block_sizes,
            self.n_count,
            order,
        )

    def _require_matching_schema(
        self, other: "ProductMultinomialMIDLaw", quantity: str
    ) -> None:
        if not isinstance(other, ProductMultinomialMIDLaw) or (
            self.block_names != other.block_names
            or self.block_sizes != other.block_sizes
            or self.n_count != other.n_count
        ):
            raise ValueError(f"{quantity} laws use different observation schemas")


def _family_log_pmf(
    probabilities: np.ndarray,
    block_sizes: Sequence[int],
    n_count: int,
    counts: np.ndarray | Sequence[int],
) -> np.ndarray:
    values = validate_multinomial_counts(counts, block_sizes, n_count)
    members = len(probabilities)
    result = np.zeros((members, len(values)), dtype=float)
    for block in _block_slices(block_sizes):
        block_counts = values[:, block]
        combinatorial = gammaln(int(n_count) + 1.0) - np.sum(
            gammaln(block_counts + 1.0), axis=1
        )
        result += combinatorial[np.newaxis, :]
        for member_index, p in enumerate(probabilities[:, block]):
            positive = p > 0.0
            result[member_index] += block_counts[:, positive] @ np.log(p[positive])
            forbidden = np.any(block_counts[:, ~positive] > 0, axis=1)
            result[member_index, forbidden] = -math.inf
    return result


@dataclass(frozen=True)
class ProductMultinomialFamily:
    """Finite represented family with one separate law per MID centre."""

    member_ids: tuple[str, ...]
    block_names: tuple[str, ...]
    block_sizes: tuple[int, ...]
    exact_mids: np.ndarray
    n_count: int

    def __post_init__(self) -> None:
        names, sizes = _validate_schema(self.block_names, self.block_sizes)
        identifiers = tuple(str(value) for value in self.member_ids)
        if not identifiers or len(set(identifiers)) != len(identifiers):
            raise ValueError("family member identifiers must be nonempty and unique")
        depth = _validate_depth(self.n_count)
        values = _immutable_array(
            _validate_probability_rows(self.exact_mids, sizes), np.float64
        )
        if values.shape != (len(identifiers), sum(sizes)):
            raise ValueError("family MID centres have unexpected shape")
        object.__setattr__(self, "member_ids", identifiers)
        object.__setattr__(self, "block_names", names)
        object.__setattr__(self, "block_sizes", sizes)
        object.__setattr__(self, "exact_mids", values)
        object.__setattr__(self, "n_count", depth)

    @property
    def member_count(self) -> int:
        return len(self.member_ids)

    @property
    def observation_dimension(self) -> int:
        return sum(self.block_sizes)

    @property
    def block_slices(self) -> tuple[slice, ...]:
        return _block_slices(self.block_sizes)

    @property
    def fingerprints(self) -> tuple[str, ...]:
        return tuple(self.law(index).fingerprint for index in range(self.member_count))

    def law(self, member_index: int) -> ProductMultinomialMIDLaw:
        index = int(member_index)
        if index < 0 or index >= self.member_count:
            raise IndexError("family member index is out of range")
        return ProductMultinomialMIDLaw(
            member_id=self.member_ids[index],
            block_names=self.block_names,
            block_sizes=self.block_sizes,
            probabilities=self.exact_mids[index],
            n_count=self.n_count,
        )

    def select(self, indices: Sequence[int]) -> "ProductMultinomialFamily":
        selected = np.asarray(indices, dtype=int)
        if selected.ndim != 1 or len(selected) < 1:
            raise ValueError("at least one family member must be selected")
        if np.any(selected < 0) or np.any(selected >= self.member_count):
            raise IndexError("family member index is out of range")
        if len(set(int(value) for value in selected)) != len(selected):
            raise ValueError("family selection indices must be unique")
        return ProductMultinomialFamily(
            member_ids=tuple(self.member_ids[int(index)] for index in selected),
            block_names=self.block_names,
            block_sizes=self.block_sizes,
            exact_mids=self.exact_mids[selected],
            n_count=self.n_count,
        )

    def sample_member(
        self, member_index: int, count: int, rng: np.random.Generator
    ) -> np.ndarray:
        return self.law(member_index).sample(count, rng)

    def log_pmf(
        self, counts: np.ndarray | Sequence[int], *, chunk_size: int = 2048
    ) -> np.ndarray:
        values = validate_multinomial_counts(counts, self.block_sizes, self.n_count)
        chunk = int(chunk_size)
        if chunk < 1:
            raise ValueError("log-PMF chunk size must be positive")
        result = np.empty((self.member_count, len(values)), dtype=float)
        for start in range(0, len(values), chunk):
            stop = min(start + chunk, len(values))
            result[:, start:stop] = _family_log_pmf(
                self.exact_mids,
                self.block_sizes,
                self.n_count,
                values[start:stop],
            )
        return result

    # Shared numerical machinery historically calls this method a density.
    def log_density(
        self, counts: np.ndarray | Sequence[int], *, chunk_size: int = 2048
    ) -> np.ndarray:
        return self.log_pmf(counts, chunk_size=chunk_size)


def product_multinomial_family_from_mid_class(
    mid_class: object, n_count: int
) -> ProductMultinomialFamily:
    """Build a family from the existing observable MID-class protocol."""

    blocks = tuple(getattr(mid_class, "blocks"))
    return ProductMultinomialFamily(
        member_ids=tuple(getattr(mid_class, "member_ids")),
        block_names=tuple(str(item[0]) for item in blocks),
        block_sizes=tuple(int(item[2]) - int(item[1]) for item in blocks),
        exact_mids=np.asarray(getattr(mid_class, "exact_mids"), dtype=float),
        n_count=n_count,
    )


def _validated_support_masks(
    law: ProductMultinomialMIDLaw, allowed_masks: Sequence[Sequence[bool]]
) -> tuple[np.ndarray, ...]:
    masks = tuple(np.asarray(mask, dtype=bool) for mask in allowed_masks)
    if len(masks) != len(law.block_sizes):
        raise ValueError("support masks do not align with the MID blocks")
    for block, mask in zip(law.block_slices, masks, strict=True):
        if mask.shape != (block.stop - block.start,):
            raise ValueError("a support mask has unexpected block dimension")
    return masks


def support_event_probability_fraction(
    law: ProductMultinomialMIDLaw, allowed_masks: Sequence[Sequence[bool]]
) -> Fraction:
    """Return an exact-rational product-support event probability.

    Each accepted binary64 ``p_effective`` coordinate is interpreted through
    its exact integer ratio.  The probability of an allowed categorical set is
    calculated from the normalization axiom as one minus the exact sum of its
    forbidden coordinates.  Thus there is no second simplex repair and no
    operation-order ambiguity.  Conversion to binary64, when requested by the
    float wrapper, happens exactly once at the end.
    """

    masks = _validated_support_masks(law, allowed_masks)
    result = Fraction(1, 1)
    for block, mask in zip(law.block_slices, masks, strict=True):
        if not np.any(mask):
            return Fraction(0, 1)
        if np.all(mask):
            allowed_probability = Fraction(1, 1)
        else:
            excluded = sum(
                (
                    Fraction.from_float(float(value))
                    for value in law.probabilities[block][~mask]
                ),
                Fraction(0, 1),
            )
            allowed_probability = Fraction(1, 1) - excluded
        if not Fraction(0, 1) <= allowed_probability <= Fraction(1, 1):
            raise ValueError("a support-event block probability lies outside [0,1]")
        result *= allowed_probability**law.n_count
    return result


def support_event_probability(
    law: ProductMultinomialMIDLaw, allowed_masks: Sequence[Sequence[bool]]
) -> float:
    """Return the once-rounded probability of a product-support event."""

    return float(support_event_probability_fraction(law, allowed_masks))


def _support_masks(law: ProductMultinomialMIDLaw) -> tuple[np.ndarray, ...]:
    return tuple(np.asarray(law.probabilities[block] > 0.0) for block in law.block_slices)


def alternative_support_union_probability(
    null_law: ProductMultinomialMIDLaw,
    alternatives: Sequence[ProductMultinomialMIDLaw],
) -> float:
    """Return the once-rounded null probability of a support union."""

    return float(
        alternative_support_union_probability_fraction(null_law, alternatives)
    )


def alternative_support_union_probability_fraction(
    null_law: ProductMultinomialMIDLaw,
    alternatives: Sequence[ProductMultinomialMIDLaw],
) -> Fraction:
    """Exact-rational null probability of a finite support union.

    Inclusion-exclusion is applied after exact duplicate support patterns are
    removed.  This is deliberately bounded because a large number of varying
    support faces should trigger a separate support analysis rather than an
    exponential hidden calculation.  The R1 acetate family has one pattern.
    """

    laws = tuple(alternatives)
    if not laws:
        raise ValueError("at least one alternative law is required")
    patterns: dict[tuple[bytes, ...], tuple[np.ndarray, ...]] = {}
    for law in laws:
        if (
            law.block_names != null_law.block_names
            or law.block_sizes != null_law.block_sizes
            or law.n_count != null_law.n_count
        ):
            raise ValueError("support-union laws use different observation schemas")
        masks = _support_masks(law)
        patterns.setdefault(tuple(mask.tobytes() for mask in masks), masks)
    unique = tuple(patterns.values())
    if len(unique) > 20:
        raise ValueError("too many varying support patterns for exact inclusion-exclusion")
    total = Fraction(0, 1)
    for subset_bits in range(1, 1 << len(unique)):
        chosen = [unique[index] for index in range(len(unique)) if subset_bits & (1 << index)]
        intersections = tuple(
            np.logical_and.reduce([pattern[block_index] for pattern in chosen])
            for block_index in range(len(null_law.block_sizes))
        )
        value = support_event_probability_fraction(null_law, intersections)
        total += value if subset_bits.bit_count() % 2 else -value
    if not Fraction(0, 1) <= total <= Fraction(1, 1):
        raise RuntimeError("support-union probability lies outside [0,1]")
    return total


@dataclass(frozen=True)
class AlternativeSupportUnionTest:
    """Exact MID-only rule that rejects on the union of alternative supports."""

    alternatives: tuple[ProductMultinomialMIDLaw, ...]

    def __post_init__(self) -> None:
        laws = tuple(self.alternatives)
        if not laws:
            raise ValueError("support-union test requires alternative laws")
        reference = laws[0]
        for law in laws[1:]:
            if (
                law.block_names != reference.block_names
                or law.block_sizes != reference.block_sizes
                or law.n_count != reference.n_count
            ):
                raise ValueError("support-union test laws use different schemas")
        object.__setattr__(self, "alternatives", laws)

    def decision_probability(self, counts: np.ndarray | Sequence[int]) -> np.ndarray:
        reference = self.alternatives[0]
        values = validate_multinomial_counts(
            counts, reference.block_sizes, reference.n_count
        )
        result = np.zeros(len(values), dtype=float)
        for law in self.alternatives:
            result[law.support_contains(values)] = 1.0
        return result


@dataclass(frozen=True)
class DiscreteCommonProposalSupport:
    """Shared count panels sampled from an audited finite law mixture."""

    observations: np.ndarray
    proposal_log_pmf: np.ndarray
    component_member_ids: tuple[str, ...]
    component_class_labels: tuple[str, ...]
    component_weights: np.ndarray
    component_laws: tuple[ProductMultinomialMIDLaw, ...]
    sampled_component_indices: np.ndarray
    seed: int
    focus_mass: float = 0.0
    unique_null_component_count: int = 0
    unique_alternative_component_count: int = 0
    focused_null_component_count: int = 0
    focused_alternative_component_count: int = 0

    def __post_init__(self) -> None:
        observations = _readonly_int(self.observations)
        log_pmf = _readonly_float(self.proposal_log_pmf)
        weights = _readonly_float(self.component_weights)
        component_laws = tuple(self.component_laws)
        indices = _readonly_int(self.sampled_component_indices)
        if observations.ndim != 2 or len(observations) < 1:
            raise ValueError("proposal observations must be a nonempty matrix")
        if log_pmf.shape != (len(observations),) or not np.all(np.isfinite(log_pmf)):
            raise ValueError("proposal log PMFs must be finite on sampled nodes")
        if weights.ndim != 1 or np.any(weights <= 0.0) or not math.isclose(
            float(np.sum(weights)), 1.0, rel_tol=0.0, abs_tol=2.0e-12
        ):
            raise ValueError("proposal component weights are invalid")
        if indices.shape != (len(observations),) or np.any(indices < 0) or np.any(indices >= len(weights)):
            raise ValueError("sampled proposal-component indices are invalid")
        if len(self.component_member_ids) != len(weights) or len(self.component_class_labels) != len(weights):
            raise ValueError("proposal component metadata are not aligned")
        if len(component_laws) != len(weights):
            raise ValueError("proposal component laws are not aligned")
        for member_id, law in zip(
            self.component_member_ids, component_laws, strict=True
        ):
            if member_id != law.member_id:
                raise ValueError("proposal component law identity is inconsistent")
        recomputed_log_pmf = np.full(len(observations), -math.inf, dtype=float)
        for weight, law in zip(weights, component_laws, strict=True):
            recomputed_log_pmf = np.logaddexp(
                recomputed_log_pmf,
                math.log(float(weight)) + law.log_pmf(observations),
            )
        if not np.array_equal(log_pmf, recomputed_log_pmf):
            maximum_difference = float(
                np.max(np.abs(log_pmf - recomputed_log_pmf))
            )
            raise MinimaxNumericalError(
                "stored proposal log PMFs disagree with the component-mixture "
                f"recomputation (maximum absolute difference {maximum_difference:.6g})"
            )
        if not 0.0 <= float(self.focus_mass) < 1.0:
            raise ValueError("proposal focus mass must lie in [0,1)")
        object.__setattr__(self, "observations", observations)
        object.__setattr__(self, "proposal_log_pmf", log_pmf)
        object.__setattr__(self, "component_weights", weights)
        object.__setattr__(self, "component_laws", component_laws)
        object.__setattr__(self, "sampled_component_indices", indices)

    @property
    def support_size(self) -> int:
        return len(self.observations)


def _unique_family_indices(family: ProductMultinomialFamily) -> np.ndarray:
    first: dict[str, int] = {}
    for index, fingerprint in enumerate(family.fingerprints):
        first.setdefault(fingerprint, index)
    return np.asarray(tuple(first.values()), dtype=int)


def build_balanced_multinomial_proposal_support(
    null_family: ProductMultinomialFamily,
    alternative_family: ProductMultinomialFamily,
    *,
    support_size: int,
    seed: int,
    focus_mass: float = 0.0,
    null_focus_indices: Sequence[int] | None = None,
    alternative_focus_indices: Sequence[int] | None = None,
) -> DiscreteCommonProposalSupport:
    """Sample a class-balanced mixture after exact duplicate-law removal.

    ``focus_mass`` reserves equal additional numerical mass for explicit
    pilot-selected members on both sides, while every distinct represented
    law retains positive base mass.  Neither allocation is a state prior.
    """

    if (
        null_family.block_names != alternative_family.block_names
        or null_family.block_sizes != alternative_family.block_sizes
        or null_family.n_count != alternative_family.n_count
    ):
        raise ValueError("proposal families use different observation schemas")
    if not isinstance(support_size, Integral):
        raise ValueError("proposal support size must be a positive integer")
    size = int(support_size)
    if size < 1:
        raise ValueError("proposal support size must be a positive integer")
    null_indices = _unique_family_indices(null_family)
    alternative_indices = _unique_family_indices(alternative_family)
    focused_mass = float(focus_mass)
    if not math.isfinite(focused_mass) or not 0.0 <= focused_mass < 1.0:
        raise ValueError("proposal focus mass must lie in [0,1)")

    def distinct_focus(
        family: ProductMultinomialFamily,
        requested: Sequence[int] | None,
        side: str,
    ) -> list[int]:
        result: list[int] = []
        seen: set[str] = set()
        for raw_index in (() if requested is None else requested):
            index = int(raw_index)
            if index < 0 or index >= family.member_count:
                raise IndexError(f"{side} proposal focus index is out of range")
            fingerprint = family.law(index).fingerprint
            if fingerprint not in seen:
                seen.add(fingerprint)
                result.append(index)
        return result

    focused_null = distinct_focus(null_family, null_focus_indices, "null")
    focused_alternative = distinct_focus(
        alternative_family, alternative_focus_indices, "alternative"
    )
    if focused_mass > 0.0 and (not focused_null or not focused_alternative):
        raise ValueError("positive focus mass requires focus laws on both sides")

    component_laws_list: list[ProductMultinomialMIDLaw] = []
    component_labels_list: list[set[str]] = []
    component_weights_list: list[float] = []
    fingerprint_to_component: dict[str, int] = {}

    def add(
        family: ProductMultinomialFamily,
        indices: Sequence[int],
        total_mass: float,
        label: str,
    ) -> None:
        if len(indices) == 0:
            return
        per_law = float(total_mass) / len(indices)
        for raw_index in indices:
            law = family.law(int(raw_index))
            component_index = fingerprint_to_component.get(law.fingerprint)
            if component_index is None:
                component_index = len(component_laws_list)
                fingerprint_to_component[law.fingerprint] = component_index
                component_laws_list.append(law)
                component_labels_list.append(set())
                component_weights_list.append(0.0)
            component_labels_list[component_index].add(label)
            component_weights_list[component_index] += per_law

    base_side_mass = 0.5 * (1.0 - focused_mass)
    add(null_family, null_indices, base_side_mass, "null")
    add(alternative_family, alternative_indices, base_side_mass, "alternative")
    if focused_mass:
        add(null_family, focused_null, 0.5 * focused_mass, "null")
        add(
            alternative_family,
            focused_alternative,
            0.5 * focused_mass,
            "alternative",
        )
    component_laws = tuple(component_laws_list)
    component_ids = tuple(law.member_id for law in component_laws)
    class_labels = tuple("+".join(sorted(labels)) for labels in component_labels_list)
    weights = np.asarray(component_weights_list, dtype=float)
    weights /= np.sum(weights)
    rng = np.random.default_rng(int(seed))
    sampled = rng.choice(len(component_laws), size=size, p=weights)
    observations = np.empty((size, null_family.observation_dimension), dtype=np.int64)
    for component_index, law in enumerate(component_laws):
        rows = np.flatnonzero(sampled == component_index)
        if len(rows):
            observations[rows] = law.sample(len(rows), rng)
    # Stream the component mixture to avoid materialising a
    # ``component_count x support_size`` matrix.  This is algebraically the
    # same log-sum-exp and is important for the audited 40k+ convergence
    # clouds; it changes no proposal draw or component weight.
    mixture_log_pmf = np.full(size, -math.inf, dtype=float)
    for weight, law in zip(weights, component_laws, strict=True):
        mixture_log_pmf = np.logaddexp(
            mixture_log_pmf, math.log(float(weight)) + law.log_pmf(observations)
        )
    if not np.all(np.isfinite(mixture_log_pmf)):
        raise MinimaxNumericalError("proposal mixture has zero PMF on a sampled node")
    return DiscreteCommonProposalSupport(
        observations=observations,
        proposal_log_pmf=mixture_log_pmf,
        component_member_ids=component_ids,
        component_class_labels=class_labels,
        component_weights=weights,
        component_laws=component_laws,
        sampled_component_indices=sampled,
        seed=int(seed),
        focus_mass=focused_mass,
        unique_null_component_count=len(null_indices),
        unique_alternative_component_count=len(alternative_indices),
        focused_null_component_count=len(focused_null),
        focused_alternative_component_count=len(focused_alternative),
    )


_IMPORTANCE_INTEGRITY_DOMAIN = b"fluxemu_multinomial_importance_v1\0"


def multinomial_importance_integrity_sha256(
    *,
    weights: np.ndarray,
    raw_mass_estimates: np.ndarray,
    log_raw_mass_estimates: np.ndarray,
    effective_sample_sizes: np.ndarray,
    maximum_log_weights: np.ndarray,
    underflowed_weight_counts: np.ndarray,
    consolidated_effective_sample_sizes: np.ndarray,
    raw_sample_count: int,
    unique_observation_count: int,
) -> str:
    """Hash a complete importance representation and its diagnostics."""

    digest = hashlib.sha256(_IMPORTANCE_INTEGRITY_DOMAIN)
    arrays = (
        np.asarray(weights, dtype="<f8"),
        np.asarray(raw_mass_estimates, dtype="<f8"),
        np.asarray(log_raw_mass_estimates, dtype="<f8"),
        np.asarray(effective_sample_sizes, dtype="<f8"),
        np.asarray(maximum_log_weights, dtype="<f8"),
        np.asarray(underflowed_weight_counts, dtype="<i8"),
        np.asarray(consolidated_effective_sample_sizes, dtype="<f8"),
    )
    for array in arrays:
        digest.update(struct.pack("<Q", array.ndim))
        for dimension in array.shape:
            digest.update(struct.pack("<Q", int(dimension)))
        digest.update(np.ascontiguousarray(array).tobytes(order="C"))
    digest.update(struct.pack("<Q", int(raw_sample_count)))
    digest.update(struct.pack("<Q", int(unique_observation_count)))
    return digest.hexdigest()


@dataclass(frozen=True)
class MultinomialImportanceDiscretization:
    """Separate row-stochastic importance representation for every law.

    ``effective_sample_sizes`` are the ordinary importance-sampling ESS values
    on the raw proposal draws.  ``consolidated_effective_sample_sizes`` use the
    coefficients after identical observable panels have been combined, and
    therefore diagnose the effective discrete LP representation itself.
    """

    weights: np.ndarray
    raw_mass_estimates: np.ndarray
    log_raw_mass_estimates: np.ndarray
    effective_sample_sizes: np.ndarray
    maximum_log_weights: np.ndarray
    underflowed_weight_counts: np.ndarray
    consolidated_effective_sample_sizes: np.ndarray
    raw_sample_count: int
    unique_observation_count: int
    integrity_sha256: str

    def __post_init__(self) -> None:
        weights = _readonly_float(self.weights)
        raw = _readonly_float(self.raw_mass_estimates)
        log_raw = _readonly_float(self.log_raw_mass_estimates)
        ess = _readonly_float(self.effective_sample_sizes)
        maxima = _readonly_float(self.maximum_log_weights)
        underflow = _readonly_int(self.underflowed_weight_counts)
        consolidated_ess = _readonly_float(
            self.consolidated_effective_sample_sizes
        )
        if weights.ndim != 2 or len(weights) < 1:
            raise ValueError("importance weights must be a nonempty matrix")
        member_count = len(weights)
        for array in (raw, log_raw, ess, maxima, underflow, consolidated_ess):
            if array.shape != (member_count,):
                raise ValueError("importance diagnostics are not member-aligned")
        if not np.all(np.isfinite(weights)) or np.any(weights < 0.0) or not np.allclose(
            np.sum(weights, axis=1), 1.0, rtol=0.0, atol=2.0e-12
        ):
            raise ValueError("importance rows must be finite row-stochastic laws")
        if (
            not np.all(np.isfinite(log_raw))
            or not np.all(np.isfinite(ess))
            or np.any(ess <= 0.0)
            or not np.all(np.isfinite(consolidated_ess))
            or np.any(consolidated_ess <= 0.0)
        ):
            raise ValueError("importance diagnostics are non-finite")
        raw_count = int(self.raw_sample_count)
        unique_count = int(self.unique_observation_count)
        if raw_count != weights.shape[1] or not 1 <= unique_count <= raw_count:
            raise ValueError("importance support-count diagnostics are invalid")
        expected_integrity = multinomial_importance_integrity_sha256(
            weights=weights,
            raw_mass_estimates=raw,
            log_raw_mass_estimates=log_raw,
            effective_sample_sizes=ess,
            maximum_log_weights=maxima,
            underflowed_weight_counts=underflow,
            consolidated_effective_sample_sizes=consolidated_ess,
            raw_sample_count=raw_count,
            unique_observation_count=unique_count,
        )
        if self.integrity_sha256 != expected_integrity:
            raise MinimaxNumericalError(
                "importance representation integrity hash mismatch"
            )
        object.__setattr__(self, "weights", weights)
        object.__setattr__(self, "raw_mass_estimates", raw)
        object.__setattr__(self, "log_raw_mass_estimates", log_raw)
        object.__setattr__(self, "effective_sample_sizes", ess)
        object.__setattr__(self, "maximum_log_weights", maxima)
        object.__setattr__(self, "underflowed_weight_counts", underflow)
        object.__setattr__(self, "consolidated_effective_sample_sizes", consolidated_ess)
        object.__setattr__(self, "raw_sample_count", raw_count)
        object.__setattr__(self, "unique_observation_count", unique_count)
        object.__setattr__(self, "integrity_sha256", expected_integrity)

    @property
    def duplicate_observation_count(self) -> int:
        return self.raw_sample_count - self.unique_observation_count


def multinomial_importance_discretize(
    family: ProductMultinomialFamily,
    support: DiscreteCommonProposalSupport,
) -> MultinomialImportanceDiscretization:
    """Importance-discretize all members on one dominating proposal cloud.

    Members are evaluated one at a time.  This is algebraically identical to
    materialising the complete member-by-support log-PMF matrix, but it avoids
    two transient matrices of that size and permits audited 80k+ convergence
    supports under a bounded-memory production run.
    """

    member_count = family.member_count
    sample_count = support.support_size
    normalized = np.empty((member_count, sample_count), dtype=float)
    raw = np.empty(member_count, dtype=float)
    log_raw = np.empty(member_count, dtype=float)
    ess = np.empty(member_count, dtype=float)
    maxima = np.empty(member_count, dtype=float)
    underflow = np.empty(member_count, dtype=np.int64)
    for index in range(member_count):
        row = (
            family.law(index).log_pmf(support.observations)
            - support.proposal_log_pmf
        )
        if np.any(np.isposinf(row)):
            raise MinimaxNumericalError(
                "proposal does not dominate a represented law"
            )
        maximum = float(np.max(row))
        if not math.isfinite(maximum):
            raise MinimaxNumericalError("a represented law has zero mass on every proposal node")
        scaled = np.exp(row - maximum)
        total = float(np.sum(scaled))
        if total <= 0.0 or not math.isfinite(total):
            raise MinimaxNumericalError("importance row normalization failed")
        normalized[index] = scaled / total
        log_raw[index] = maximum + math.log(total / sample_count)
        raw[index] = math.exp(log_raw[index]) if log_raw[index] > math.log(np.finfo(float).tiny) else 0.0
        ess[index] = total * total / float(np.sum(np.square(scaled)))
        maxima[index] = maximum
        underflow[index] = int(np.count_nonzero((scaled == 0.0) & np.isfinite(row)))

    # Unlike the continuous Control 0 cloud, a discrete multinomial proposal
    # can draw exactly the same observable panel more than once.  Giving those
    # copies separate LP variables would permit different decisions for the
    # same Y and would therefore cease to be a statistical test.  Consolidate
    # their empirical importance mass deterministically onto the first copy.
    # We retain the original column count so nested proposal prefixes and all
    # existing finite-LP APIs remain unchanged; duplicate columns simply have
    # zero mass under every represented law.
    _, first_indices, inverse = np.unique(
        support.observations, axis=0, return_index=True, return_inverse=True
    )
    if len(first_indices) != sample_count:
        consolidated = np.zeros_like(normalized)
        for member_index in range(member_count):
            unique_mass = np.bincount(
                inverse,
                weights=normalized[member_index],
                minlength=len(first_indices),
            )
            consolidated[member_index, first_indices] = unique_mass
        normalized = consolidated
    consolidated_ess = 1.0 / np.sum(np.square(normalized), axis=1)
    integrity = multinomial_importance_integrity_sha256(
        weights=normalized,
        raw_mass_estimates=raw,
        log_raw_mass_estimates=log_raw,
        effective_sample_sizes=ess,
        maximum_log_weights=maxima,
        underflowed_weight_counts=underflow,
        consolidated_effective_sample_sizes=consolidated_ess,
        raw_sample_count=sample_count,
        unique_observation_count=len(first_indices),
    )
    return MultinomialImportanceDiscretization(
        weights=normalized,
        raw_mass_estimates=raw,
        log_raw_mass_estimates=log_raw,
        effective_sample_sizes=ess,
        maximum_log_weights=maxima,
        underflowed_weight_counts=underflow,
        consolidated_effective_sample_sizes=consolidated_ess,
        raw_sample_count=sample_count,
        unique_observation_count=len(first_indices),
        integrity_sha256=integrity,
    )


@dataclass(frozen=True)
class ProductMultinomialMixtureTest:
    """Deployable dual-derived decision rule accepting count panels only."""

    null_family: ProductMultinomialFamily
    alternative_family: ProductMultinomialFamily
    null_mixture_weights: np.ndarray
    alternative_mixture_weights: np.ndarray
    log_likelihood_threshold: float
    tie_probability: float
    tie_log_tolerance: float = 2.0e-10

    def __post_init__(self) -> None:
        if (
            self.null_family.block_names != self.alternative_family.block_names
            or self.null_family.block_sizes != self.alternative_family.block_sizes
            or self.null_family.n_count != self.alternative_family.n_count
        ):
            raise ValueError("deployable mixture families use different schemas")
        null_weights = _readonly_float(self.null_mixture_weights)
        alternative_weights = _readonly_float(self.alternative_mixture_weights)
        if null_weights.shape != (self.null_family.member_count,) or alternative_weights.shape != (
            self.alternative_family.member_count,
        ):
            raise ValueError("deployable mixture weights have unexpected shape")
        for weights in (null_weights, alternative_weights):
            if np.any(weights < 0.0) or not math.isclose(
                float(np.sum(weights)), 1.0, rel_tol=0.0, abs_tol=2.0e-10
            ):
                raise ValueError("deployable mixture weights are invalid")
        if not math.isfinite(float(self.log_likelihood_threshold)):
            raise ValueError("deployable likelihood threshold must be finite")
        if not 0.0 <= float(self.tie_probability) <= 1.0:
            raise ValueError("tie probability must lie in [0,1]")
        object.__setattr__(self, "null_mixture_weights", null_weights)
        object.__setattr__(self, "alternative_mixture_weights", alternative_weights)

    @staticmethod
    def _mixture_log_pmf(
        family: ProductMultinomialFamily,
        weights: np.ndarray,
        counts: np.ndarray,
    ) -> np.ndarray:
        positive = weights > 0.0
        indices = np.flatnonzero(positive)
        return logsumexp(
            np.log(weights[positive])[:, np.newaxis]
            + family.select(indices).log_pmf(counts),
            axis=0,
        )

    def log_score(self, counts: np.ndarray | Sequence[int]) -> np.ndarray:
        values = validate_multinomial_counts(
            counts, self.null_family.block_sizes, self.null_family.n_count
        )
        alternative_log_pmf = self._mixture_log_pmf(
            self.alternative_family, self.alternative_mixture_weights, values
        )
        null_log_pmf = self._mixture_log_pmf(
            self.null_family, self.null_mixture_weights, values
        )
        common_zero = np.isneginf(alternative_log_pmf) & np.isneginf(null_log_pmf)
        if np.any(common_zero):
            raise ValueError(
                "mixture likelihood ratio is undefined where both mixtures have zero PMF"
            )
        with np.errstate(invalid="ignore"):
            result = alternative_log_pmf - null_log_pmf
        if np.any(np.isnan(result)):
            raise MinimaxNumericalError("deployable mixture score produced NaN")
        return result

    def decision_probability(self, counts: np.ndarray | Sequence[int]) -> np.ndarray:
        centred = self.log_score(counts) - float(self.log_likelihood_threshold)
        result = np.empty(len(centred), dtype=float)
        result[centred > float(self.tie_log_tolerance)] = 1.0
        result[centred < -float(self.tie_log_tolerance)] = 0.0
        tie = np.abs(centred) <= float(self.tie_log_tolerance)
        result[tie] = float(self.tie_probability)
        return result


@dataclass(frozen=True)
class DiscreteRepresentationDiagnostics:
    test: ProductMultinomialMixtureTest
    finite_support_worst_type_i: float
    finite_support_worst_type_ii: float
    objective_difference: float
    maximum_member_error_difference_from_primal: float
    strict_support_count: int
    tie_support_count: int
    randomization_probability: float
    stable_on_finite_support: bool


@dataclass(frozen=True)
class KKTScoreBoundary:
    """Guarded score boundary reconstructed from a finite-LP primal."""

    log_likelihood_threshold: float
    tie_probability: float
    fractional_support_indices: np.ndarray
    strict_support_count: int
    tie_support_count: int
    boundary_mode: str
    maximum_fractional_score_deviation: float


@dataclass(frozen=True)
class FinitePairNPBoundary:
    """Complete finite-alphabet Neyman--Pearson boundary for one pair.

    ``exact_decision_probabilities`` follows the complete likelihood-ratio
    ordering and randomises at one ordered node.  The deployable vector uses
    the declared log-score tie convention.  Keeping both vectors makes the
    simple-pair lower bound and any score-rule approximation explicit.
    """

    log_likelihood_threshold: float
    tie_probability: float
    boundary_support_index: int
    complete_lr_order: np.ndarray
    exact_decision_probabilities: np.ndarray
    deployable_decision_probabilities: np.ndarray
    exact_pair_type_i: float
    exact_pair_type_ii_lower_bound: float
    deployable_pair_type_i: float
    deployable_pair_type_ii: float
    strict_support_count: int
    tie_support_count: int
    tie_null_mass: float
    log_ratio_additive_constant: float
    maximum_log_ratio_residual: float


def finite_pair_neyman_pearson_boundary(
    null_probabilities: np.ndarray | Sequence[float],
    alternative_probabilities: np.ndarray | Sequence[float],
    log_scores: np.ndarray | Sequence[float],
    *,
    epsilon: float,
    tie_log_tolerance: float = 2.0e-10,
    log_ratio_tolerance: float = 2.0e-9,
) -> FinitePairNPBoundary:
    """Solve one finite simple-vs-simple test by complete LR sorting.

    The probability rows may be normalized importance discretizations.  Their
    log ratio must equal the supplied raw, p_effective-only score up to one
    additive normalization constant.  This guard prevents a candidate pair
    from being certified with a differently ordered statistic.
    """

    null = np.asarray(null_probabilities, dtype=float)
    alternative = np.asarray(alternative_probabilities, dtype=float)
    scores = np.asarray(log_scores, dtype=float)
    if null.ndim != 1 or alternative.shape != null.shape or scores.shape != null.shape:
        raise ValueError("finite-pair arrays must be aligned vectors")
    if (
        not len(null)
        or not np.all(np.isfinite(null))
        or not np.all(np.isfinite(alternative))
        or np.any(null < 0.0)
        or np.any(alternative < 0.0)
        or np.any(np.isnan(scores))
    ):
        raise ValueError("finite-pair probability or score array is invalid")
    if not math.isclose(float(np.sum(null)), 1.0, rel_tol=0.0, abs_tol=2.0e-12):
        raise ValueError("finite-pair null probabilities must sum to one")
    if not math.isclose(
        float(np.sum(alternative)), 1.0, rel_tol=0.0, abs_tol=2.0e-12
    ):
        raise ValueError("finite-pair alternative probabilities must sum to one")
    size = float(epsilon)
    tie_tolerance = float(tie_log_tolerance)
    ratio_tolerance = float(log_ratio_tolerance)
    if not 0.0 < size < 1.0:
        raise ValueError("finite-pair epsilon must lie strictly between zero and one")
    if (
        not math.isfinite(tie_tolerance)
        or tie_tolerance < 0.0
        or not math.isfinite(ratio_tolerance)
        or ratio_tolerance <= 0.0
    ):
        raise ValueError("finite-pair score tolerances are invalid")

    positive_null = null > 0.0
    positive_alternative = alternative > 0.0
    common_positive = positive_null & positive_alternative
    alternative_only = ~positive_null & positive_alternative
    null_only = positive_null & ~positive_alternative
    if np.any(alternative_only & ~np.isposinf(scores)):
        raise ContinuousRepresentationUnavailable(
            "finite-pair score is not +inf on alternative-only support"
        )
    if np.any(null_only & ~np.isneginf(scores)):
        raise ContinuousRepresentationUnavailable(
            "finite-pair score is not -inf on null-only support"
        )
    if np.any(common_positive & ~np.isfinite(scores)):
        raise ContinuousRepresentationUnavailable(
            "finite-pair common support has a nonfinite score"
        )
    if not np.any(common_positive):
        raise ContinuousRepresentationUnavailable(
            "finite-pair laws have disjoint support; use an exact support certificate"
        )
    normalized_log_ratio = (
        np.log(alternative[common_positive]) - np.log(null[common_positive])
    )
    offsets = normalized_log_ratio - scores[common_positive]
    additive_constant = float(np.median(offsets))
    maximum_ratio_residual = float(
        np.max(np.abs(offsets - additive_constant))
    )
    if maximum_ratio_residual > ratio_tolerance:
        raise ContinuousRepresentationUnavailable(
            "finite-pair raw score and probability-row likelihood ratios disagree: "
            f"maximum residual {maximum_ratio_residual:.12g} exceeds "
            f"{ratio_tolerance:.12g}"
        )

    represented = positive_null | positive_alternative
    represented_indices = np.flatnonzero(represented)
    # Mergesort makes equal-score ordering deterministic by original column.
    order = represented_indices[
        np.argsort(-scores[represented_indices], kind="mergesort")
    ]
    exact = np.zeros(len(null), dtype=float)
    strict_null_mass = 0.0
    boundary_index: int | None = None
    boundary_eta = 0.0
    for raw_index in order:
        index = int(raw_index)
        node_mass = float(null[index])
        if node_mass == 0.0:
            exact[index] = 1.0
            continue
        remaining = size - strict_null_mass
        if remaining <= 2.0e-15:
            boundary_index = index
            boundary_eta = 0.0
            break
        if node_mass >= remaining - 2.0e-15:
            boundary_index = index
            boundary_eta = remaining / node_mass
            boundary_eta = min(1.0, max(0.0, boundary_eta))
            exact[index] = boundary_eta
            break
        exact[index] = 1.0
        strict_null_mass = math.fsum((strict_null_mass, node_mass))
    if boundary_index is None:  # pragma: no cover - null row is stochastic
        raise ContinuousRepresentationUnavailable(
            "finite-pair LR ordering did not reach the Type I budget"
        )
    threshold = float(scores[boundary_index])
    if not math.isfinite(threshold):
        raise ContinuousRepresentationUnavailable(
            "finite-pair randomized boundary has a nonfinite MID-only score"
        )

    strict = scores > threshold + tie_tolerance
    tie = np.abs(scores - threshold) <= tie_tolerance
    tie_mass = float(null @ tie.astype(float))
    deploy_strict_mass = float(null @ strict.astype(float))
    if tie_mass <= 0.0:
        raise ContinuousRepresentationUnavailable(
            "finite-pair deployable boundary has zero null tie mass"
        )
    deploy_eta = (size - deploy_strict_mass) / tie_mass
    if deploy_eta < -2.0e-12 or deploy_eta > 1.0 + 2.0e-12:
        raise ContinuousRepresentationUnavailable(
            "finite-pair deployable boundary randomization lies outside [0,1]"
        )
    deploy_eta = min(1.0, max(0.0, deploy_eta))
    deployable = strict.astype(float) + deploy_eta * tie.astype(float)
    exact_type_i = float(null @ exact)
    exact_type_ii = float(alternative @ (1.0 - exact))
    deploy_type_i = float(null @ deployable)
    deploy_type_ii = float(alternative @ (1.0 - deployable))
    if abs(exact_type_i - size) > 2.0e-12 or abs(deploy_type_i - size) > 2.0e-12:
        raise ContinuousRepresentationUnavailable(
            "finite-pair randomized boundary does not exhaust the Type I budget"
        )
    if deploy_type_ii + 2.0e-13 < exact_type_ii:
        raise ContinuousRepresentationUnavailable(
            "deployable pair rule is spuriously below the complete LR lower bound"
        )
    return FinitePairNPBoundary(
        log_likelihood_threshold=threshold,
        tie_probability=float(deploy_eta),
        boundary_support_index=boundary_index,
        complete_lr_order=_readonly_int(order),
        exact_decision_probabilities=_readonly_float(exact),
        deployable_decision_probabilities=_readonly_float(deployable),
        exact_pair_type_i=exact_type_i,
        exact_pair_type_ii_lower_bound=exact_type_ii,
        deployable_pair_type_i=deploy_type_i,
        deployable_pair_type_ii=deploy_type_ii,
        strict_support_count=int(np.count_nonzero(strict)),
        tie_support_count=int(np.count_nonzero(tie)),
        tie_null_mass=tie_mass,
        log_ratio_additive_constant=additive_constant,
        maximum_log_ratio_residual=maximum_ratio_residual,
    )


def reconstruct_kkt_score_boundary(
    log_scores: np.ndarray | Sequence[float],
    decision_probabilities: np.ndarray | Sequence[float],
    least_favourable_null: np.ndarray | Sequence[float],
    *,
    decision_tolerance: float = 1.0e-8,
    score_tolerance: float = 2.0e-10,
) -> KKTScoreBoundary:
    """Recover a deployable score threshold from primal/KKT boundary nodes.

    A fractional primal node identifies the likelihood-ratio boundary without
    using importance-normalisation estimates.  Multiple fractional nodes are
    admitted only when their observable log scores agree within the declared
    score tolerance.  If the primal is deterministic, a separating boundary
    is placed strictly between accepted and rejected score sets.
    """

    scores = np.asarray(log_scores, dtype=float)
    decision = np.asarray(decision_probabilities, dtype=float)
    least_null = np.asarray(least_favourable_null, dtype=float)
    if scores.ndim != 1 or decision.shape != scores.shape or least_null.shape != scores.shape:
        raise ValueError("KKT boundary arrays must be aligned vectors")
    if (
        np.any(np.isnan(scores))
        or np.any(np.isposinf(scores))
        or not np.all(np.isfinite(decision))
        or not np.all(np.isfinite(least_null))
        or np.any(decision < 0.0)
        or np.any(decision > 1.0)
        or np.any(least_null < 0.0)
    ):
        raise ValueError("KKT boundary arrays contain invalid values")
    if not math.isclose(
        float(np.sum(least_null)), 1.0, rel_tol=0.0, abs_tol=2.0e-12
    ):
        raise ValueError("least-favourable null row must sum to one")
    decision_tol = float(decision_tolerance)
    score_tol = float(score_tolerance)
    if decision_tol <= 0.0 or score_tol < 0.0:
        raise ValueError("KKT boundary tolerances are invalid")
    fractional = np.flatnonzero(
        (decision > decision_tol) & (decision < 1.0 - decision_tol)
    )
    maximum_deviation = 0.0
    if len(fractional):
        fractional_scores = scores[fractional]
        if not np.all(np.isfinite(fractional_scores)):
            raise ContinuousRepresentationUnavailable(
                "fractional KKT boundary has a nonfinite MID-only score"
            )
        threshold = math.fsum(map(float, fractional_scores)) / len(
            fractional_scores
        )
        maximum_deviation = float(
            np.max(np.abs(fractional_scores - threshold))
        )
        if maximum_deviation > score_tol:
            raise ContinuousRepresentationUnavailable(
                "fractional KKT nodes have inconsistent MID-only log scores: "
                f"maximum deviation {maximum_deviation:.12g} exceeds "
                f"{score_tol:.12g}"
            )
        centred = scores - threshold
        strict = centred > score_tol
        tie = np.abs(centred) <= score_tol
        if not np.all(tie[fractional]):
            raise ContinuousRepresentationUnavailable(
                "fractional KKT nodes are not in the deployable score tie set"
            )
        target = float(least_null @ decision)
        strict_mass = float(least_null @ strict.astype(float))
        tie_mass = float(least_null @ tie.astype(float))
        if tie_mass <= 0.0:
            raise ContinuousRepresentationUnavailable(
                "fractional KKT boundary has zero least-favourable null mass"
            )
        eta = (target - strict_mass) / tie_mass
        if eta < -2.0e-10 or eta > 1.0 + 2.0e-10:
            raise ContinuousRepresentationUnavailable(
                "fractional KKT randomization lies outside [0,1]"
            )
        eta = min(1.0, max(0.0, eta))
        mode = "fractional_primal_score_boundary"
    else:
        rejected = decision >= 1.0 - decision_tol
        accepted = decision <= decision_tol
        if not np.all(rejected | accepted):  # pragma: no cover - definition
            raise ContinuousRepresentationUnavailable(
                "primal has unresolved nonbinary decision nodes"
            )
        finite_scores = scores[np.isfinite(scores)]
        if not len(finite_scores):
            raise ContinuousRepresentationUnavailable(
                "deterministic KKT boundary has no finite score"
            )
        if np.any(rejected) and np.any(accepted):
            lower = float(np.max(scores[accepted]))
            upper = float(np.min(scores[rejected]))
            if not math.isfinite(upper) or not lower < upper:
                raise ContinuousRepresentationUnavailable(
                    "deterministic primal decisions are not separated by the MID-only score"
                )
            if math.isinf(lower) and lower < 0.0:
                threshold = math.nextafter(upper, -math.inf)
            else:
                threshold = lower + 0.5 * (upper - lower)
            if not math.isfinite(threshold):
                raise ContinuousRepresentationUnavailable(
                    "deterministic KKT threshold is nonfinite"
                )
        elif np.any(rejected):
            lower = float(np.min(scores[rejected]))
            if not math.isfinite(lower):
                raise ContinuousRepresentationUnavailable(
                    "all-reject deterministic boundary is nonfinite"
                )
            threshold = math.nextafter(lower, -math.inf)
        else:
            upper = float(np.max(finite_scores))
            threshold = math.nextafter(upper, math.inf)
        eta = 0.0
        centred = scores - threshold
        strict = centred > score_tol
        tie = np.abs(centred) <= score_tol
        mode = "deterministic_separating_score_boundary"
    return KKTScoreBoundary(
        log_likelihood_threshold=float(threshold),
        tie_probability=float(eta),
        fractional_support_indices=_readonly_int(fractional),
        strict_support_count=int(np.count_nonzero(strict)),
        tie_support_count=int(np.count_nonzero(tie)),
        boundary_mode=mode,
        maximum_fractional_score_deviation=maximum_deviation,
    )


def reconstruct_product_multinomial_mixture_test_from_kkt(
    solution: FiniteMinimaxSolution,
    raw_test: ProductMultinomialMixtureTest,
    null_discretization: MultinomialImportanceDiscretization,
    alternative_discretization: MultinomialImportanceDiscretization,
    support: DiscreteCommonProposalSupport,
    *,
    validation_null_rows: np.ndarray | None = None,
    validation_alternative_rows: np.ndarray | None = None,
    expected_null_errors: np.ndarray | None = None,
    expected_alternative_errors: np.ndarray | None = None,
    reproduction_tolerance: float = 2.0e-5,
) -> DiscreteRepresentationDiagnostics:
    """Reconstruct and fully validate a deployable primal/KKT score rule."""

    if solution.null_dual_total <= 1.0e-12:
        raise ContinuousRepresentationUnavailable(
            "KKT score reconstruction requires a supported null dual"
        )
    least_null = (
        solution.null_dual_multipliers / solution.null_dual_total
    ) @ null_discretization.weights
    scores = raw_test.log_score(support.observations)
    boundary = reconstruct_kkt_score_boundary(
        scores,
        solution.decision_probabilities,
        least_null,
        score_tolerance=raw_test.tie_log_tolerance,
    )
    test = ProductMultinomialMixtureTest(
        null_family=raw_test.null_family,
        alternative_family=raw_test.alternative_family,
        null_mixture_weights=raw_test.null_mixture_weights,
        alternative_mixture_weights=raw_test.alternative_mixture_weights,
        log_likelihood_threshold=boundary.log_likelihood_threshold,
        tie_probability=boundary.tie_probability,
        tie_log_tolerance=raw_test.tie_log_tolerance,
    )
    probabilities = test.decision_probability(support.observations)
    def finite_rows(values: np.ndarray, name: str) -> np.ndarray:
        rows = np.asarray(values, dtype=float)
        if (
            rows.ndim != 2
            or rows.shape[1] != support.support_size
            or not np.all(np.isfinite(rows))
            or np.any(rows < 0.0)
            or not np.allclose(
                np.sum(rows, axis=1), 1.0, rtol=0.0, atol=2.0e-12
            )
        ):
            raise ValueError(f"{name} are not finite row-stochastic laws")
        return rows

    null_rows = (
        null_discretization.weights
        if validation_null_rows is None
        else finite_rows(validation_null_rows, "KKT null validation rows")
    )
    alternative_rows = (
        alternative_discretization.weights
        if validation_alternative_rows is None
        else finite_rows(
            validation_alternative_rows,
            "KKT alternative validation rows",
        )
    )
    if null_rows.shape[1] != support.support_size or alternative_rows.shape[1] != support.support_size:
        raise ValueError("KKT validation rows use the wrong finite support")
    null_errors = null_rows @ probabilities
    alternative_errors = alternative_rows @ (1.0 - probabilities)
    expected_null = (
        solution.null_errors
        if expected_null_errors is None
        else np.asarray(expected_null_errors, dtype=float)
    )
    expected_alternative = (
        solution.alternative_errors
        if expected_alternative_errors is None
        else np.asarray(expected_alternative_errors, dtype=float)
    )
    if expected_null.shape != null_errors.shape or expected_alternative.shape != alternative_errors.shape:
        raise ValueError("KKT expected errors are not member-aligned")
    maximum_difference = float(
        max(
            np.max(np.abs(null_errors - expected_null)),
            np.max(np.abs(alternative_errors - expected_alternative)),
        )
    )
    worst_i = float(np.max(null_errors))
    worst_ii = float(np.max(alternative_errors))
    objective_difference = abs(worst_ii - solution.beta_objective)
    stable = bool(
        maximum_difference <= float(reproduction_tolerance)
        and worst_i <= solution.epsilon + float(reproduction_tolerance)
        and objective_difference <= float(reproduction_tolerance)
    )
    if not stable:
        raise ContinuousRepresentationUnavailable(
            "KKT score rule failed all-member finite-support reproduction: "
            f"member_difference={maximum_difference:.12g}, "
            f"objective_difference={objective_difference:.12g}, "
            f"worst_type_i={worst_i:.12g}"
        )
    return DiscreteRepresentationDiagnostics(
        test=test,
        finite_support_worst_type_i=worst_i,
        finite_support_worst_type_ii=worst_ii,
        objective_difference=objective_difference,
        maximum_member_error_difference_from_primal=maximum_difference,
        strict_support_count=boundary.strict_support_count,
        tie_support_count=boundary.tie_support_count,
        randomization_probability=boundary.tie_probability,
        stable_on_finite_support=True,
    )


def build_product_multinomial_mixture_test(
    solution: FiniteMinimaxSolution,
    null_family: ProductMultinomialFamily,
    alternative_family: ProductMultinomialFamily,
    null_discretization: MultinomialImportanceDiscretization,
    alternative_discretization: MultinomialImportanceDiscretization,
    support: DiscreteCommonProposalSupport,
    *,
    reproduction_tolerance: float = 2.0e-5,
    dual_coefficient_tolerance: float = 1.0e-12,
) -> DiscreteRepresentationDiagnostics:
    """Convert finite-LP duals to a discrete, out-of-sample MID-only rule."""

    if (
        solution.null_dual_multipliers.shape != (null_family.member_count,)
        or solution.alternative_dual_multipliers.shape != (alternative_family.member_count,)
    ):
        raise ValueError("LP dual rows and product-multinomial families are not aligned")
    if np.any(null_discretization.raw_mass_estimates <= 0.0) or np.any(
        alternative_discretization.raw_mass_estimates <= 0.0
    ):
        raise ContinuousRepresentationUnavailable("importance mass estimate underflow prevents deployable correction")
    null_coefficients = solution.null_dual_multipliers / null_discretization.raw_mass_estimates
    alternative_coefficients = (
        solution.alternative_dual_multipliers / alternative_discretization.raw_mass_estimates
    )
    null_total = float(np.sum(null_coefficients))
    alternative_total = float(np.sum(alternative_coefficients))
    if null_total <= dual_coefficient_tolerance or alternative_total <= dual_coefficient_tolerance:
        raise ContinuousRepresentationUnavailable("finite dual has no two-sided mixture representation")
    null_weights = null_coefficients / null_total
    alternative_weights = alternative_coefficients / alternative_total
    threshold = math.log(null_total / alternative_total)

    discrete_alternative = solution.alternative_dual_multipliers @ alternative_discretization.weights
    discrete_null = solution.null_dual_multipliers @ null_discretization.weights
    advantage = discrete_alternative - discrete_null
    scale = np.maximum.reduce(
        (
            np.abs(discrete_alternative),
            np.abs(discrete_null),
            np.full(support.support_size, 1.0 / support.support_size),
        )
    )
    tie = np.abs(advantage) <= 2.0e-7 * scale
    strict = advantage > 2.0e-7 * scale
    null_dual_total = solution.null_dual_total
    if null_dual_total <= dual_coefficient_tolerance:
        raise ContinuousRepresentationUnavailable("null dual total is zero")
    least_favourable_null = (
        solution.null_dual_multipliers / null_dual_total
    ) @ null_discretization.weights
    target = float(least_favourable_null @ solution.decision_probabilities)
    strict_probability = float(least_favourable_null @ strict.astype(float))
    tie_mass = float(least_favourable_null @ tie.astype(float))
    randomization = (
        (target - strict_probability) / tie_mass if tie_mass > 1.0e-14 else 0.0
    )
    if randomization < -2.0e-7 or randomization > 1.0 + 2.0e-7:
        raise ContinuousRepresentationUnavailable("dual tie set cannot reproduce primal randomization")
    randomization = min(1.0, max(0.0, randomization))
    test = ProductMultinomialMixtureTest(
        null_family=null_family,
        alternative_family=alternative_family,
        null_mixture_weights=null_weights,
        alternative_mixture_weights=alternative_weights,
        log_likelihood_threshold=threshold,
        tie_probability=randomization,
    )
    probabilities = test.decision_probability(support.observations)
    null_errors = null_discretization.weights @ probabilities
    alternative_errors = alternative_discretization.weights @ (1.0 - probabilities)
    differences = np.concatenate(
        (
            np.abs(null_errors - solution.null_errors),
            np.abs(alternative_errors - solution.alternative_errors),
        )
    )
    maximum_difference = float(np.max(differences))
    worst_i = float(np.max(null_errors))
    worst_ii = float(np.max(alternative_errors))
    objective_difference = abs(worst_ii - solution.beta_objective)
    stable = bool(
        maximum_difference <= reproduction_tolerance
        and worst_i <= solution.epsilon + reproduction_tolerance
        and objective_difference <= reproduction_tolerance
    )
    return DiscreteRepresentationDiagnostics(
        test=test,
        finite_support_worst_type_i=worst_i,
        finite_support_worst_type_ii=worst_ii,
        objective_difference=objective_difference,
        maximum_member_error_difference_from_primal=maximum_difference,
        strict_support_count=int(np.count_nonzero(strict)),
        tie_support_count=int(np.count_nonzero(tie)),
        randomization_probability=float(randomization),
        stable_on_finite_support=stable,
    )


__all__ = [
    "AlternativeSupportUnionTest",
    "DiscreteCommonProposalSupport",
    "DiscreteRepresentationDiagnostics",
    "EFFECTIVE_KERNEL_HASH_POLICY",
    "FinitePairNPBoundary",
    "KKTScoreBoundary",
    "LastCoordinateClosure",
    "MultinomialImportanceDiscretization",
    "PROBABILITY_BLOCK_HASH_POLICY",
    "PRODUCT_MULTINOMIAL_SAMPLER_POLICY",
    "ProductMultinomialFamily",
    "ProductMultinomialMIDLaw",
    "ProductMultinomialMixtureTest",
    "SIMPLEX_CLOSURE_POLICY",
    "SIMPLEX_CLOSURE_TOLERANCE",
    "alternative_support_union_probability",
    "alternative_support_union_probability_fraction",
    "build_balanced_multinomial_proposal_support",
    "build_product_multinomial_mixture_test",
    "categorical_kl_divergence",
    "categorical_renyi_divergence",
    "effective_kernel_hash",
    "finite_pair_neyman_pearson_boundary",
    "last_coordinate_fsum_closure",
    "multinomial_counts_from_mids",
    "multinomial_importance_discretize",
    "multinomial_mids_from_counts",
    "product_multinomial_family_from_mid_class",
    "product_multinomial_kl_divergence",
    "product_multinomial_log_lr_moment",
    "product_multinomial_renyi_divergence",
    "probability_block_hash",
    "reconstruct_kkt_score_boundary",
    "reconstruct_product_multinomial_mixture_test_from_kkt",
    "support_event_probability",
    "support_event_probability_fraction",
    "validate_multinomial_counts",
]
