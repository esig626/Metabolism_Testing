"""Renyi separation and projected tests for product-Dirichlet MID laws.

This module begins at the observable-law boundary.  Its inputs are positive
Dirichlet parameter vectors, MID observations, and metabolite-block sizes; it
has no metabolic-model, flux-coordinate, or inverse-MFA interface.

The order convention is fixed throughout:

``D_lam(Q || P) = log integral(q**lam * p**(1-lam)) / (lam - 1)``.

Thus the parameter vector belonging to ``Q`` receives weight ``lam``.  The
implementation uses analytic multivariate-beta identities.  A Hessian-line
integral avoids cancellation close to either endpoint of ``(0, 1)``.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable, Iterable, Sequence

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize, minimize_scalar
from scipy.special import betaln, digamma, gammaln, log_ndtr, loggamma, polygamma
from scipy.stats import norm


DEFAULT_ENDPOINT_SWITCH = 1.0e-3
DEFAULT_GAUSS_LEGENDRE_ORDER = 300
DEFAULT_IDENTITY_TOLERANCE = 0.0


class RenyiNumericalError(RuntimeError):
    """Raised when a Renyi or projected-test calculation is numerically invalid."""


def _validate_order(order: float) -> float:
    value = float(order)
    if not math.isfinite(value) or not 0.0 < value < 1.0:
        raise ValueError("Renyi order must lie strictly inside (0, 1)")
    return value


def _validate_block_sizes(block_sizes: Sequence[int], dimension: int) -> tuple[int, ...]:
    sizes = tuple(int(value) for value in block_sizes)
    if not sizes or any(value < 2 for value in sizes) or sum(sizes) != int(dimension):
        raise ValueError("invalid product-Dirichlet block layout")
    return sizes


def _validate_alpha(alpha: Sequence[float], name: str) -> np.ndarray:
    values = np.asarray(alpha, dtype=float)
    if (
        values.ndim != 1
        or len(values) < 2
        or not np.all(np.isfinite(values))
        or np.any(values <= 0.0)
    ):
        raise ValueError(f"{name} must be a finite positive parameter vector")
    return values


def log_multivariate_beta(alpha: Sequence[float]) -> float:
    """Return ``log B(alpha)`` using log-gamma operations."""

    values = _validate_alpha(alpha, "Dirichlet alpha")
    return float(np.sum(gammaln(values)) - gammaln(np.sum(values)))


def _block_slices(block_sizes: Sequence[int]) -> tuple[slice, ...]:
    cursor = 0
    result: list[slice] = []
    for size in block_sizes:
        stop = cursor + int(size)
        result.append(slice(cursor, stop))
        cursor = stop
    return tuple(result)


def dirichlet_kl_divergence(
    alpha_q: Sequence[float], alpha_p: Sequence[float]
) -> float:
    """Return the analytic ``KL(Dir(alpha_q) || Dir(alpha_p))``."""

    q = _validate_alpha(alpha_q, "alpha_q")
    p = _validate_alpha(alpha_p, "alpha_p")
    if q.shape != p.shape:
        raise ValueError("Dirichlet parameter vectors have different shapes")
    if np.array_equal(q, p):
        return 0.0
    gradient_q = digamma(q) - digamma(np.sum(q))
    value = (
        log_multivariate_beta(p)
        - log_multivariate_beta(q)
        + float(np.dot(q - p, gradient_q))
    )
    if value < -1.0e-10:
        raise RenyiNumericalError(f"negative Dirichlet KL divergence {value}")
    return max(0.0, float(value))


def product_dirichlet_kl_divergence(
    alpha_q: Sequence[float],
    alpha_p: Sequence[float],
    block_sizes: Sequence[int],
) -> float:
    """Return ``KL(Q || P)`` for independent Dirichlet MID blocks."""

    q = _validate_alpha(alpha_q, "alpha_q")
    p = _validate_alpha(alpha_p, "alpha_p")
    if q.shape != p.shape:
        raise ValueError("product-Dirichlet parameter vectors have different shapes")
    sizes = _validate_block_sizes(block_sizes, len(q))
    if np.array_equal(q, p):
        return 0.0
    return float(
        sum(dirichlet_kl_divergence(q[block], p[block]) for block in _block_slices(sizes))
    )


def _dirichlet_renyi_direct(q: np.ndarray, p: np.ndarray, order: float) -> float:
    mixture = order * q + (1.0 - order) * p
    numerator = (
        order * log_multivariate_beta(q)
        + (1.0 - order) * log_multivariate_beta(p)
        - log_multivariate_beta(mixture)
    )
    return float(numerator / (1.0 - order))


def _dirichlet_line_hessian_scalar(q: np.ndarray, p: np.ndarray, position: float) -> float:
    """Second derivative of ``log B(p+t(q-p))`` along its line."""

    direction = q - p
    alpha = p + float(position) * direction
    component = float(np.dot(np.square(direction), polygamma(1, alpha)))
    total = float(np.square(np.sum(direction)) * polygamma(1, np.sum(alpha)))
    result = component - total
    if result < -1.0e-10 or not math.isfinite(result):
        raise RenyiNumericalError("invalid log-beta line Hessian")
    return max(result, 0.0)


def _dirichlet_renyi_line_integral(
    q: np.ndarray,
    p: np.ndarray,
    order: float,
    *,
    quadrature_order: int,
) -> float:
    """Cancellation-resistant Jensen-gap evaluation of ``D_order(Q||P)``.

    With ``g(t)=log B(p+t(q-p))`` and ``h=g''``, the exact identity is

    ``D = order**2 int_0^1 u h(order*u) du``
    ``  + order*(1-order) int_0^1 (1-u) h(order+(1-order)*u) du``.
    """

    # Adaptive quadrature is intentional.  Some admissible alpha paths have
    # sharp curvature near a simplex boundary; fixed 32/64-point rules can
    # look converged while losing scientifically relevant endpoint digits.
    limit = max(100, int(quadrature_order))
    first_integral, first_error = quad(
        lambda unit: unit
        * _dirichlet_line_hessian_scalar(q, p, order * unit),
        0.0,
        1.0,
        epsabs=2.0e-12,
        epsrel=2.0e-12,
        limit=limit,
    )
    second_integral, second_error = quad(
        lambda unit: (1.0 - unit)
        * _dirichlet_line_hessian_scalar(
            q, p, order + (1.0 - order) * unit
        ),
        0.0,
        1.0,
        epsabs=2.0e-12,
        epsrel=2.0e-12,
        limit=limit,
    )
    first = order * order * first_integral
    second = order * (1.0 - order) * second_integral
    weighted_error_bound = (
        order * order * first_error
        + order * (1.0 - order) * second_error
    )
    value = first + second
    if weighted_error_bound > 2.0e-9 + 2.0e-11 * abs(value):
        raise RenyiNumericalError("endpoint Renyi quadrature did not converge")
    return value


def dirichlet_renyi_divergence(
    alpha_q: Sequence[float],
    alpha_p: Sequence[float],
    order: float,
    *,
    endpoint_switch: float = DEFAULT_ENDPOINT_SWITCH,
    quadrature_order: int = DEFAULT_GAUSS_LEGENDRE_ORDER,
    force_stable: bool = False,
) -> float:
    """Return analytic ``D_order(Dir(alpha_q) || Dir(alpha_p))``.

    The exact identity shortcut is important: subtracting equal log-beta
    values can otherwise manufacture a tiny signed divergence.  Away from the
    endpoints the direct log-beta formula is used; close to either endpoint a
    positive Hessian-line integral removes the cancellation.
    """

    q = _validate_alpha(alpha_q, "alpha_q")
    p = _validate_alpha(alpha_p, "alpha_p")
    lam = _validate_order(order)
    if q.shape != p.shape:
        raise ValueError("Dirichlet parameter vectors have different shapes")
    if np.array_equal(q, p):
        return 0.0
    switch = float(endpoint_switch)
    if not 0.0 <= switch < 0.5:
        raise ValueError("endpoint switch must lie in [0, 0.5)")
    use_stable = bool(force_stable or min(lam, 1.0 - lam) <= switch)
    value = (
        _dirichlet_renyi_line_integral(
            q, p, lam, quadrature_order=int(quadrature_order)
        )
        if use_stable
        else _dirichlet_renyi_direct(q, p, lam)
    )
    if not math.isfinite(value) or value < -2.0e-9:
        raise RenyiNumericalError(f"invalid Dirichlet Renyi divergence {value}")
    return max(0.0, float(value))


def product_dirichlet_renyi_divergence(
    alpha_q: Sequence[float],
    alpha_p: Sequence[float],
    block_sizes: Sequence[int],
    order: float,
    *,
    endpoint_switch: float = DEFAULT_ENDPOINT_SWITCH,
    quadrature_order: int = DEFAULT_GAUSS_LEGENDRE_ORDER,
    force_stable: bool = False,
) -> float:
    """Return the sum of blockwise ``D_order(Q || P)`` values."""

    q = _validate_alpha(alpha_q, "alpha_q")
    p = _validate_alpha(alpha_p, "alpha_p")
    if q.shape != p.shape:
        raise ValueError("product-Dirichlet parameter vectors have different shapes")
    sizes = _validate_block_sizes(block_sizes, len(q))
    _validate_order(order)
    if np.array_equal(q, p):
        return 0.0
    result = sum(
        dirichlet_renyi_divergence(
            q[block],
            p[block],
            order,
            endpoint_switch=endpoint_switch,
            quadrature_order=quadrature_order,
            force_stable=force_stable,
        )
        for block in _block_slices(sizes)
    )
    return float(result)


def pairwise_product_dirichlet_renyi(
    alpha_q_rows: np.ndarray,
    alpha_p_rows: np.ndarray,
    block_sizes: Sequence[int],
    order: float,
    *,
    chunk_size: int = 64,
) -> np.ndarray:
    """Evaluate all oriented row pairs with the analytic log-beta formula.

    This vectorised routine is intended for dense-grid validation strictly
    away from numerical endpoint limits.  Scalar endpoint diagnostics should
    use :func:`product_dirichlet_renyi_divergence`.
    """

    q_rows = np.asarray(alpha_q_rows, dtype=float)
    p_rows = np.asarray(alpha_p_rows, dtype=float)
    lam = _validate_order(order)
    if (
        q_rows.ndim != 2
        or p_rows.ndim != 2
        or q_rows.shape[1] != p_rows.shape[1]
        or min(q_rows.shape[0], p_rows.shape[0]) < 1
        or not np.all(np.isfinite(q_rows))
        or not np.all(np.isfinite(p_rows))
        or np.any(q_rows <= 0.0)
        or np.any(p_rows <= 0.0)
    ):
        raise ValueError("invalid product-Dirichlet parameter matrices")
    sizes = _validate_block_sizes(block_sizes, q_rows.shape[1])
    if min(lam, 1.0 - lam) <= 1.0e-7:
        raise ValueError("dense pairwise evaluation is too close to an order endpoint")
    result = np.empty((len(q_rows), len(p_rows)), dtype=float)
    step = int(chunk_size)
    if step < 1:
        raise ValueError("pairwise chunk size must be positive")
    for start in range(0, len(q_rows), step):
        stop = min(start + step, len(q_rows))
        values = np.zeros((stop - start, len(p_rows)), dtype=float)
        for block in _block_slices(sizes):
            q = q_rows[start:stop, block]
            p = p_rows[:, block]
            log_b_q = np.sum(gammaln(q), axis=1) - gammaln(np.sum(q, axis=1))
            log_b_p = np.sum(gammaln(p), axis=1) - gammaln(np.sum(p, axis=1))
            mixture = (
                lam * q[:, np.newaxis, :]
                + (1.0 - lam) * p[np.newaxis, :, :]
            )
            log_b_mix = np.sum(gammaln(mixture), axis=2) - gammaln(
                np.sum(mixture, axis=2)
            )
            values += (
                lam * log_b_q[:, np.newaxis]
                + (1.0 - lam) * log_b_p[np.newaxis, :]
                - log_b_mix
            ) / (1.0 - lam)
        result[start:stop] = values
    identical = np.all(
        q_rows[:, np.newaxis, :] == p_rows[np.newaxis, :, :], axis=2
    )
    result[identical] = 0.0
    if np.min(result) < -2.0e-8 or not np.all(np.isfinite(result)):
        raise RenyiNumericalError("dense Renyi matrix contains invalid values")
    return np.maximum(result, 0.0)


@dataclass(frozen=True)
class ProjectedScore:
    """A MID-only log likelihood ratio ``log(q_star / p_star)``."""

    alpha_p: np.ndarray
    alpha_q: np.ndarray
    block_sizes: tuple[int, ...]
    log_constant: float
    coefficients: np.ndarray

    def __post_init__(self) -> None:
        p = np.array(self.alpha_p, dtype=float, copy=True)
        q = np.array(self.alpha_q, dtype=float, copy=True)
        if p.shape != q.shape:
            raise ValueError("projected law parameter vectors have different shapes")
        _validate_alpha(p, "alpha_p")
        _validate_alpha(q, "alpha_q")
        sizes = _validate_block_sizes(self.block_sizes, len(p))
        coefficients = np.array(self.coefficients, dtype=float, copy=True)
        if coefficients.shape != p.shape or not np.all(np.isfinite(coefficients)):
            raise ValueError("invalid projected-score coefficients")
        expected_constant = sum(
            log_multivariate_beta(p[block]) - log_multivariate_beta(q[block])
            for block in _block_slices(sizes)
        )
        if not math.isclose(
            float(self.log_constant), expected_constant, rel_tol=0.0, abs_tol=2.0e-10
        ):
            raise ValueError("projected-score normalising constant is inconsistent")
        if not np.allclose(coefficients, q - p, rtol=0.0, atol=0.0):
            raise ValueError("projected-score coefficients have the wrong orientation")
        p.setflags(write=False)
        q.setflags(write=False)
        coefficients.setflags(write=False)
        object.__setattr__(self, "alpha_p", p)
        object.__setattr__(self, "alpha_q", q)
        object.__setattr__(self, "block_sizes", sizes)
        object.__setattr__(self, "log_constant", float(self.log_constant))
        object.__setattr__(self, "coefficients", coefficients)

    def evaluate(self, observations: np.ndarray) -> np.ndarray:
        """Evaluate ``log(q_star(y)/p_star(y))`` on MID observations."""

        values = np.asarray(observations, dtype=float)
        if values.ndim == 1:
            values = values[np.newaxis, :]
        if (
            values.ndim != 2
            or values.shape[1] != len(self.coefficients)
            or not np.all(np.isfinite(values))
            or np.any(values <= 0.0)
        ):
            raise ValueError("invalid MID observations for projected score")
        cursor = 0
        for size in self.block_sizes:
            stop = cursor + size
            if not np.allclose(
                np.sum(values[:, cursor:stop], axis=1),
                1.0,
                rtol=0.0,
                atol=2.0e-12,
            ):
                raise ValueError("each observed MID block must sum to one")
            cursor = stop
        result = self.log_constant + np.log(values) @ self.coefficients
        if not np.all(np.isfinite(result)):
            raise RenyiNumericalError("projected score is non-finite")
        return result

    def log_moment(self, alpha_law: Sequence[float], exponent: float) -> float:
        """Return ``log E_law[exp(exponent * S)]`` analytically."""

        alpha = _validate_alpha(alpha_law, "alpha_law")
        if alpha.shape != self.coefficients.shape:
            raise ValueError("moment law has the wrong dimension")
        t = float(exponent)
        if not math.isfinite(t):
            raise ValueError("score-moment exponent must be finite")
        shifted = alpha + t * self.coefficients
        if np.any(shifted <= 0.0):
            return math.inf
        result = t * self.log_constant
        for block in _block_slices(self.block_sizes):
            result += log_multivariate_beta(shifted[block]) - log_multivariate_beta(
                alpha[block]
            )
        return float(result)

    def cumulant_derivative(
        self, alpha_law: Sequence[float], exponent: float, derivative: int
    ) -> float:
        """Return a derivative of the score cumulant-generating function.

        Derivative one is the tilted mean, derivative two the tilted
        variance, and derivative three the tilted third cumulant.
        """

        alpha = _validate_alpha(alpha_law, "alpha_law")
        if alpha.shape != self.coefficients.shape:
            raise ValueError("cumulant law has the wrong dimension")
        t = float(exponent)
        degree = int(derivative)
        if degree < 1 or degree > 4 or not math.isfinite(t):
            raise ValueError("supported cumulant derivatives are one through four")
        shifted = alpha + t * self.coefficients
        if np.any(shifted <= 0.0):
            raise ValueError("cumulant exponent leaves the finite-moment domain")
        result = self.log_constant if degree == 1 else 0.0
        for block in _block_slices(self.block_sizes):
            block_delta = self.coefficients[block]
            block_alpha = shifted[block]
            if degree == 1:
                result += float(
                    np.dot(block_delta, digamma(block_alpha))
                    - np.sum(block_delta) * digamma(np.sum(block_alpha))
                )
            else:
                result += float(
                    np.dot(
                        np.power(block_delta, degree),
                        polygamma(degree - 1, block_alpha),
                    )
                    - np.power(np.sum(block_delta), degree)
                    * polygamma(degree - 1, np.sum(block_alpha))
                )
        return float(result)

    def finite_moment_domain(self, alpha_law: Sequence[float]) -> tuple[float, float]:
        """Return the open exponent interval on which the score MGF is finite."""

        alpha = _validate_alpha(alpha_law, "alpha_law")
        if alpha.shape != self.coefficients.shape:
            raise ValueError("moment law has the wrong dimension")
        lower = -math.inf
        upper = math.inf
        positive = self.coefficients > 0.0
        negative = self.coefficients < 0.0
        if np.any(positive):
            lower = float(np.max(-alpha[positive] / self.coefficients[positive]))
        if np.any(negative):
            upper = float(np.min(-alpha[negative] / self.coefficients[negative]))
        return lower, upper


def projected_log_likelihood_score(
    alpha_p: Sequence[float],
    alpha_q: Sequence[float],
    block_sizes: Sequence[int],
) -> ProjectedScore:
    """Construct the oriented score ``log(q/p)`` from observable parameters."""

    p = _validate_alpha(alpha_p, "alpha_p")
    q = _validate_alpha(alpha_q, "alpha_q")
    if p.shape != q.shape:
        raise ValueError("projected law parameter vectors have different shapes")
    sizes = _validate_block_sizes(block_sizes, len(p))
    constant = sum(
        log_multivariate_beta(p[block]) - log_multivariate_beta(q[block])
        for block in _block_slices(sizes)
    )
    return ProjectedScore(
        alpha_p=p,
        alpha_q=q,
        block_sizes=sizes,
        log_constant=float(constant),
        coefficients=q - p,
    )


@dataclass(frozen=True)
class SaddlepointCDF:
    probability: float
    log_probability: float
    saddlepoint: float
    tilted_mean: float
    tilted_variance: float
    method: str


@dataclass(frozen=True)
class CharacteristicCDF:
    probability: float
    absolute_quadrature_error: float
    integration_cutoff: float
    log_characteristic_magnitude_at_cutoff: float
    method: str


def characteristic_score_cdf(
    score: ProjectedScore,
    alpha_law: Sequence[float],
    threshold: float,
    *,
    cutoff_log_magnitude: float = -80.0,
    maximum_cutoff: float = 1_000.0,
    absolute_tolerance: float = 2.0e-11,
) -> CharacteristicCDF:
    """Deterministically invert the exact score characteristic function.

    Gil--Pelaez inversion is applied to the analytic product-Dirichlet
    characteristic function.  The returned quadrature error does not include
    a formal tail enclosure beyond the recorded cutoff; callers must inspect
    the characteristic magnitude there before using certified language.
    """

    alpha = _validate_alpha(alpha_law, "alpha_law")
    if alpha.shape != score.coefficients.shape:
        raise ValueError("characteristic-function law has the wrong dimension")
    target = float(threshold)
    if not math.isfinite(target):
        raise ValueError("characteristic-function threshold must be finite")
    cutoff_target = float(cutoff_log_magnitude)
    if not cutoff_target < 0.0:
        raise ValueError("characteristic cutoff magnitude must be negative")
    block_data = tuple(
        (
            np.asarray(alpha[block], dtype=float),
            np.asarray(score.coefficients[block], dtype=float),
            log_multivariate_beta(alpha[block]),
        )
        for block in _block_slices(score.block_sizes)
    )

    def log_characteristic(frequency: float) -> complex:
        value = 1j * frequency * score.log_constant
        for block_alpha, block_delta, base_log_beta in block_data:
            shifted = block_alpha + 1j * frequency * block_delta
            complex_log_beta = np.sum(loggamma(shifted)) - loggamma(
                np.sum(shifted)
            )
            value += complex_log_beta - base_log_beta
        return complex(value)

    cutoff = 0.1
    log_magnitude = float(log_characteristic(cutoff).real)
    while log_magnitude > cutoff_target and cutoff < float(maximum_cutoff):
        cutoff *= 1.5
        log_magnitude = float(log_characteristic(cutoff).real)
    if log_magnitude > cutoff_target:
        raise RenyiNumericalError(
            "characteristic function did not decay before the integration cutoff"
        )
    mean = score.cumulant_derivative(alpha, 0.0, 1)

    def integrand(frequency: float) -> float:
        if frequency == 0.0:
            return mean - target
        value = np.exp(
            log_characteristic(frequency) - 1j * frequency * target
        )
        return float(np.imag(value) / frequency)

    integral, error = quad(
        integrand,
        0.0,
        cutoff,
        epsabs=float(absolute_tolerance),
        epsrel=float(absolute_tolerance),
        limit=3_000,
    )
    probability = 0.5 - integral / math.pi
    scaled_error = float(error / math.pi)
    if probability < -5.0 * scaled_error or probability > 1.0 + 5.0 * scaled_error:
        raise RenyiNumericalError("characteristic inversion left the probability range")
    return CharacteristicCDF(
        probability=min(1.0, max(0.0, float(probability))),
        absolute_quadrature_error=scaled_error,
        integration_cutoff=cutoff,
        log_characteristic_magnitude_at_cutoff=log_magnitude,
        method="Gil-Pelaez characteristic-function inversion",
    )


def saddlepoint_score_cdf(
    score: ProjectedScore,
    alpha_law: Sequence[float],
    threshold: float,
    *,
    root_tolerance: float = 1.0e-12,
) -> SaddlepointCDF:
    """Approximate ``P(S <= threshold)`` by Lugannani--Rice inversion.

    This deterministic approximation is useful for smooth optimisation and
    must be validated independently when used for scientific error or bound
    estimates.  It is not advertised as exact quadrature.
    """

    alpha = _validate_alpha(alpha_law, "alpha_law")
    if alpha.shape != score.coefficients.shape:
        raise ValueError("saddlepoint law has the wrong dimension")
    target = float(threshold)
    if not math.isfinite(target):
        raise ValueError("saddlepoint threshold must be finite")
    mean = score.cumulant_derivative(alpha, 0.0, 1)
    variance = score.cumulant_derivative(alpha, 0.0, 2)
    if not math.isfinite(variance) or variance <= 0.0:
        if np.array_equal(score.alpha_p, score.alpha_q):
            probability = 1.0 if target >= mean else 0.0
            return SaddlepointCDF(
                probability,
                0.0 if probability == 1.0 else -math.inf,
                0.0,
                mean,
                0.0,
                "degenerate",
            )
        raise RenyiNumericalError("score variance is not positive")
    standard_deviation = math.sqrt(variance)
    standardized = (target - mean) / standard_deviation
    if abs(standardized) <= 1.0e-5:
        skewness = score.cumulant_derivative(alpha, 0.0, 3) / variance**1.5
        probability = 0.5 + float(norm.pdf(0.0)) * skewness / 6.0
        probability = min(1.0, max(0.0, probability))
        return SaddlepointCDF(
            probability,
            -math.inf if probability == 0.0 else math.log(probability),
            0.0,
            mean,
            variance,
            "mean Edgeworth limit",
        )

    lower_domain, upper_domain = score.finite_moment_domain(alpha)
    margin = 1.0e-10
    if target < mean:
        right = 0.0
        left = -1.0
        if math.isfinite(lower_domain):
            left = max(left, lower_domain + margin * max(1.0, abs(lower_domain)))
        while score.cumulant_derivative(alpha, left, 1) > target:
            proposed = 2.0 * left
            if math.isfinite(lower_domain):
                proposed = max(
                    proposed,
                    lower_domain + margin * max(1.0, abs(lower_domain)),
                )
            if proposed == left:
                return SaddlepointCDF(
                    0.0, -math.inf, left, mean, variance, "domain-tail limit"
                )
            left = proposed
    else:
        left = 0.0
        right = 1.0
        if math.isfinite(upper_domain):
            right = min(right, upper_domain - margin * max(1.0, abs(upper_domain)))
        while score.cumulant_derivative(alpha, right, 1) < target:
            proposed = 2.0 * right
            if math.isfinite(upper_domain):
                proposed = min(
                    proposed,
                    upper_domain - margin * max(1.0, abs(upper_domain)),
                )
            if proposed == right:
                return SaddlepointCDF(
                    1.0, 0.0, right, mean, variance, "domain-tail limit"
                )
            right = proposed
    saddle = float(
        brentq(
            lambda value: score.cumulant_derivative(alpha, value, 1) - target,
            left,
            right,
            xtol=float(root_tolerance),
            rtol=4.0 * np.finfo(float).eps,
            maxiter=200,
        )
    )
    cumulant = score.log_moment(alpha, saddle)
    signed_root_argument = 2.0 * (saddle * target - cumulant)
    if signed_root_argument < -2.0e-9:
        raise RenyiNumericalError("negative saddlepoint root argument")
    signed_root = math.copysign(math.sqrt(max(0.0, signed_root_argument)), saddle)
    tilted_variance = score.cumulant_derivative(alpha, saddle, 2)
    scaled_saddle = saddle * math.sqrt(tilted_variance)
    if abs(signed_root) < 1.0e-7 or abs(scaled_saddle) < 1.0e-12:
        probability = float(norm.cdf(standardized))
        log_probability = float(log_ndtr(standardized))
        method = "normal near-singular fallback"
    else:
        log_normal_cdf = float(log_ndtr(signed_root))
        log_normal_density = (
            -0.5 * signed_root * signed_root - 0.5 * math.log(2.0 * math.pi)
        )
        correction_ratio = (
            (1.0 / signed_root - 1.0 / scaled_saddle)
            * math.exp(log_normal_density - log_normal_cdf)
        )
        correction_factor = 1.0 + correction_ratio
        if correction_factor > 0.0 and math.isfinite(correction_factor):
            log_probability = log_normal_cdf + math.log(correction_factor)
        else:
            # A negative LR correction is outside the approximation's useful
            # regime.  Preserve a finite, explicitly labeled log-tail
            # diagnostic rather than returning a false exact zero.
            log_probability = log_normal_cdf
            method = "signed-root log-CDF fallback"
        probability = (
            0.0
            if log_probability < math.log(np.nextafter(0.0, 1.0))
            else float(math.exp(log_probability))
        )
        if correction_factor > 0.0 and math.isfinite(correction_factor):
            method = "Lugannani-Rice"
    return SaddlepointCDF(
        probability=min(1.0, max(0.0, probability)),
        log_probability=min(0.0, float(log_probability)),
        saddlepoint=saddle,
        tilted_mean=score.cumulant_derivative(alpha, saddle, 1),
        tilted_variance=tilted_variance,
        method=method,
    )


def closed_form_minimum_threshold(
    order: float,
    separation: float,
    *,
    epsilon: float = 0.05,
    sample_size: int = 1,
) -> float:
    """Smallest Markov/Renyi threshold guaranteeing the null budget.

    ``r=-log(epsilon)/sample_size`` and
    ``tau_min=(sample_size*r-sample_size*(1-order)*D)/order``.
    """

    lam = _validate_order(order)
    divergence = float(separation)
    n = int(sample_size)
    level = float(epsilon)
    if n < 1:
        raise ValueError("sample size must be positive")
    if not 0.0 < level < 1.0 or not math.isfinite(level):
        raise ValueError("epsilon must lie strictly inside (0, 1)")
    if not math.isfinite(divergence) or divergence < 0.0:
        raise ValueError("Renyi separation must be finite and nonnegative")
    return float((-math.log(level) - n * (1.0 - lam) * divergence) / lam)


def complete_moment_exponential_bound(
    order: float,
    separation: float,
    threshold: float,
    *,
    sample_size: int = 1,
) -> float:
    """Return the raw (uncapped) projected complete-moment expression."""

    lam = _validate_order(order)
    divergence = float(separation)
    tau = float(threshold)
    n = int(sample_size)
    if n < 1 or divergence < 0.0 or not math.isfinite(divergence):
        raise ValueError("invalid separation or sample size")
    log_value = (1.0 - lam) * (tau - n * divergence)
    if log_value > math.log(np.finfo(float).max):
        return math.inf
    return float(math.exp(log_value))


@dataclass(frozen=True)
class EmpiricalThresholdTest:
    threshold: float
    tie_probability: float
    worst_type_i: float
    worst_type_ii: float
    worst_null_index: int
    worst_alternative_index: int


def threshold_error(
    scores: Sequence[float],
    threshold: float,
    tie_probability: float,
    *,
    hypothesis: str,
) -> float:
    """Evaluate a randomised strict-threshold Type-I or Type-II error."""

    values = np.asarray(scores, dtype=float)
    tau = float(threshold)
    eta = float(tie_probability)
    if values.ndim != 1 or len(values) < 1 or not np.all(np.isfinite(values)):
        raise ValueError("score sample must be a nonempty finite vector")
    if not 0.0 <= eta <= 1.0 or not math.isfinite(tau):
        raise ValueError("invalid threshold randomisation")
    above = float(np.mean(values > tau))
    ties = float(np.mean(values == tau))
    rejection = above + eta * ties
    if hypothesis == "H0":
        return rejection
    if hypothesis == "H1":
        return 1.0 - rejection
    raise ValueError("hypothesis must be 'H0' or 'H1'")


def calibrate_empirical_threshold(
    null_score_samples: Sequence[Sequence[float]],
    alternative_score_samples: Sequence[Sequence[float]],
    *,
    epsilon: float = 0.05,
) -> EmpiricalThresholdTest:
    """Solve the empirical composite budget within one fixed-score family.

    The returned interface retains boundary randomisation.  With continuous
    Dirichlet observations independently simulated scores almost surely have
    no cross-stream ties, but no such assumption is made here.
    """

    level = float(epsilon)
    if not 0.0 < level < 1.0:
        raise ValueError("epsilon must lie strictly inside (0, 1)")
    null_rows = tuple(np.sort(np.asarray(row, dtype=float)) for row in null_score_samples)
    alternative_rows = tuple(
        np.asarray(row, dtype=float) for row in alternative_score_samples
    )
    if not null_rows or not alternative_rows:
        raise ValueError("both score classes must be nonempty")
    if any(row.ndim != 1 or len(row) < 1 or not np.all(np.isfinite(row)) for row in (*null_rows, *alternative_rows)):
        raise ValueError("score samples must be nonempty finite vectors")

    # For each null row, choose its smallest observed boundary with strict-tail
    # mass no larger than epsilon.  The maximum of those boundaries is the
    # smallest threshold feasible for every represented null member.
    member_boundaries: list[float] = []
    for row in null_rows:
        permitted_above = math.floor(level * len(row) + 1.0e-12)
        index = max(0, len(row) - permitted_above - 1)
        member_boundaries.append(float(row[index]))
    threshold = max(member_boundaries)

    eta_upper = 1.0
    for row in null_rows:
        above = int(np.count_nonzero(row > threshold))
        ties = int(np.count_nonzero(row == threshold))
        if ties:
            eta_upper = min(eta_upper, (level * len(row) - above) / ties)
        elif above / len(row) > level + 2.0e-15:
            raise RenyiNumericalError("empirical threshold calibration is infeasible")
    eta = min(1.0, max(0.0, float(eta_upper)))
    null_errors = np.asarray(
        [threshold_error(row, threshold, eta, hypothesis="H0") for row in null_rows]
    )
    alternative_errors = np.asarray(
        [
            threshold_error(row, threshold, eta, hypothesis="H1")
            for row in alternative_rows
        ]
    )
    if float(np.max(null_errors)) > level + 2.0e-12:
        raise RenyiNumericalError("calibrated empirical test exceeds Type-I budget")
    return EmpiricalThresholdTest(
        threshold=threshold,
        tie_probability=eta,
        worst_type_i=float(np.max(null_errors)),
        worst_type_ii=float(np.max(alternative_errors)),
        worst_null_index=int(np.argmax(null_errors)),
        worst_alternative_index=int(np.argmax(alternative_errors)),
    )


@dataclass(frozen=True)
class CorrectedBoundEvaluation:
    order: float
    threshold: float
    separation: float
    complete_constant: float
    gamma: float
    tilde_gamma: float
    corrected_bound: float
    exponential_bound: float
    corrected_probability_cap: float
    exponential_probability_cap: float
    worst_corrected_alternative_index: int
    same_q_identity_residual: float


def evaluate_empirical_corrected_bound(
    alternative_score_samples: Sequence[Sequence[float]],
    order: float,
    separation: float,
    threshold: float,
    *,
    tie_probability: float = 0.0,
    sample_size: int = 1,
) -> CorrectedBoundEvaluation:
    """Evaluate Gamma and the same-Q slack/rejection correction empirically."""

    lam = _validate_order(order)
    divergence = float(separation)
    tau = float(threshold)
    eta = float(tie_probability)
    n = int(sample_size)
    if divergence < 0.0 or not math.isfinite(divergence) or n < 1:
        raise ValueError("invalid separation or sample size")
    if not 0.0 <= eta <= 1.0:
        raise ValueError("tie probability must lie in [0,1]")
    rows = tuple(np.asarray(row, dtype=float) for row in alternative_score_samples)
    if not rows or any(
        row.ndim != 1 or len(row) < 1 or not np.all(np.isfinite(row)) for row in rows
    ):
        raise ValueError("alternative score samples must be nonempty and finite")
    log_c = n * (lam - 1.0) * divergence
    complete_constant = float(math.exp(log_c))
    full_moments: list[float] = []
    rejected_moments: list[float] = []
    accepted_moments: list[float] = []
    for scores in rows:
        weights = np.exp((lam - 1.0) * scores)
        rejection = (scores > tau).astype(float) + eta * (scores == tau)
        rejected = float(np.mean(weights * rejection))
        full = float(np.mean(weights))
        accepted = float(np.mean(weights * (1.0 - rejection)))
        full_moments.append(full)
        rejected_moments.append(rejected)
        accepted_moments.append(accepted)
    full_values = np.asarray(full_moments)
    rejected_values = np.asarray(rejected_moments)
    accepted_values = np.asarray(accepted_moments)
    same_q_terms = complete_constant - full_values + rejected_values
    tilde_gamma = float(np.min(same_q_terms))
    gamma = float(np.min(rejected_values))
    multiplier = math.exp((1.0 - lam) * tau)
    corrected_from_definition = multiplier * (complete_constant - tilde_gamma)
    corrected_direct = multiplier * float(np.max(accepted_values))
    residual = abs(corrected_from_definition - corrected_direct)
    scale = max(1.0, abs(corrected_from_definition), abs(corrected_direct))
    if residual > 5.0e-12 * scale:
        raise RenyiNumericalError("same-Q corrected-bound identity failed")
    exponential = complete_moment_exponential_bound(
        lam, divergence, tau, sample_size=n
    )
    return CorrectedBoundEvaluation(
        order=lam,
        threshold=tau,
        separation=divergence,
        complete_constant=complete_constant,
        gamma=gamma,
        tilde_gamma=tilde_gamma,
        corrected_bound=float(corrected_direct),
        exponential_bound=float(exponential),
        corrected_probability_cap=min(1.0, float(corrected_direct)),
        exponential_probability_cap=min(1.0, float(exponential)),
        worst_corrected_alternative_index=int(np.argmax(accepted_values)),
        same_q_identity_residual=float(residual),
    )


@dataclass(frozen=True)
class PairOptimisationResult:
    order: float
    divergence: float
    null_coordinate: float
    alternative_coordinate: float
    success: bool
    solver_message: str
    starts_refined: int
    exploratory_grid_size: int
    dense_grid_divergence: float
    dense_grid_null_coordinate: float
    dense_grid_alternative_coordinate: float
    dense_grid_discrepancy: float


def minimise_parameterised_pair(
    order: float,
    null_alpha: Callable[[float], np.ndarray],
    alternative_alpha: Callable[[float], np.ndarray],
    null_bounds: tuple[float, float],
    alternative_bounds: tuple[float, float],
    block_sizes: Sequence[int],
    *,
    exploratory_grid_size: int = 41,
    validation_grid_size: int = 101,
    candidate_start_count: int = 12,
    coordinate_tolerance: float = 1.0e-10,
) -> PairOptimisationResult:
    """Continuously minimise pairwise observable-law Renyi divergence.

    A full two-dimensional exploratory grid supplies multiple starts.  Every
    selected start is refined with bounded Powell optimisation, and the final
    answer is checked against a separate denser grid.
    """

    lam = _validate_order(order)
    n0 = tuple(float(value) for value in null_bounds)
    n1 = tuple(float(value) for value in alternative_bounds)
    if len(n0) != 2 or len(n1) != 2 or not n0[0] < n0[1] or not n1[0] < n1[1]:
        raise ValueError("invalid class-coordinate bounds")
    coarse_count = int(exploratory_grid_size)
    dense_count = int(validation_grid_size)
    if coarse_count < 3 or dense_count <= coarse_count:
        raise ValueError("pair grids must be ordered and contain at least three points")
    coarse_p_x = np.linspace(n0[0], n0[1], coarse_count)
    coarse_q_x = np.linspace(n1[0], n1[1], coarse_count)
    coarse_p = np.asarray([null_alpha(float(value)) for value in coarse_p_x])
    coarse_q = np.asarray([alternative_alpha(float(value)) for value in coarse_q_x])
    coarse_values = pairwise_product_dirichlet_renyi(
        coarse_q, coarse_p, block_sizes, lam
    )
    flat_order = np.argsort(coarse_values, axis=None)
    starts: list[tuple[float, float]] = []
    for flat_index in flat_order:
        q_index, p_index = np.unravel_index(int(flat_index), coarse_values.shape)
        candidate = (float(coarse_p_x[p_index]), float(coarse_q_x[q_index]))
        if all(
            abs(candidate[0] - previous[0]) > (n0[1] - n0[0]) / coarse_count
            or abs(candidate[1] - previous[1]) > (n1[1] - n1[0]) / coarse_count
            for previous in starts
        ):
            starts.append(candidate)
        if len(starts) >= int(candidate_start_count):
            break
    starts.extend(
        [
            (n0[0], n1[0]),
            (n0[0], n1[1]),
            (n0[1], n1[0]),
            (n0[1], n1[1]),
        ]
    )
    starts = list(dict.fromkeys(starts))

    def objective(point: np.ndarray) -> float:
        p_alpha = null_alpha(float(point[0]))
        q_alpha = alternative_alpha(float(point[1]))
        return product_dirichlet_renyi_divergence(q_alpha, p_alpha, block_sizes, lam)

    candidates: list[tuple[float, float, float, bool, str]] = []
    for start in starts:
        solution = minimize(
            objective,
            np.asarray(start, dtype=float),
            method="Powell",
            bounds=(n0, n1),
            options={"xtol": coordinate_tolerance, "ftol": 1.0e-12, "maxiter": 500},
        )
        point = np.clip(np.asarray(solution.x, dtype=float), [n0[0], n1[0]], [n0[1], n1[1]])
        candidates.append(
            (
                float(objective(point)),
                float(point[0]),
                float(point[1]),
                bool(solution.success),
                str(solution.message),
            )
        )
    for point in ((n0[0], n1[0]), (n0[0], n1[1]), (n0[1], n1[0]), (n0[1], n1[1])):
        candidates.append((float(objective(np.asarray(point))), point[0], point[1], True, "explicit boundary"))
    best = min(candidates, key=lambda item: (item[0], item[1], item[2]))

    dense_p_x = np.linspace(n0[0], n0[1], dense_count)
    dense_q_x = np.linspace(n1[0], n1[1], dense_count)
    dense_p = np.asarray([null_alpha(float(value)) for value in dense_p_x])
    dense_q = np.asarray([alternative_alpha(float(value)) for value in dense_q_x])
    dense_values = pairwise_product_dirichlet_renyi(dense_q, dense_p, block_sizes, lam)
    dense_flat = int(np.argmin(dense_values))
    dense_q_index, dense_p_index = np.unravel_index(dense_flat, dense_values.shape)
    dense_minimum = float(dense_values[dense_q_index, dense_p_index])
    discrepancy = dense_minimum - best[0]
    if discrepancy < -5.0e-8:
        raise RenyiNumericalError(
            "independent dense class grid beat continuous pair optimisation"
        )
    return PairOptimisationResult(
        order=lam,
        divergence=best[0],
        null_coordinate=best[1],
        alternative_coordinate=best[2],
        success=best[3],
        solver_message=best[4],
        starts_refined=len(starts),
        exploratory_grid_size=coarse_count,
        dense_grid_divergence=dense_minimum,
        dense_grid_null_coordinate=float(dense_p_x[dense_p_index]),
        dense_grid_alternative_coordinate=float(dense_q_x[dense_q_index]),
        dense_grid_discrepancy=max(0.0, float(discrepancy)),
    )


@dataclass(frozen=True)
class LambdaOptimisationResult:
    objective_name: str
    optimiser_kind: str
    order: float | None
    objective: float
    equivalent_order_lower: float | None
    equivalent_order_upper: float | None
    exploratory_grid_size: int
    validation_grid_size: int
    candidate_basin_count: int
    refinement_discrepancy: float
    endpoint_value_near_zero: float
    endpoint_value_near_one: float
    local_curvature: float | None


def optimise_order_globally(
    objective: Callable[[float], float],
    *,
    objective_name: str,
    lower: float = 1.0e-4,
    upper: float = 1.0 - 1.0e-4,
    exploratory_grid_size: int = 201,
    validation_grid_size: int = 401,
    flat_absolute_tolerance: float = 1.0e-10,
    order_tolerance: float = 2.0e-4,
) -> LambdaOptimisationResult:
    """Search all sampled basins and continuously refine a scalar order objective."""

    lo = _validate_order(lower)
    hi = _validate_order(upper)
    if not lo < hi:
        raise ValueError("lambda optimisation bounds are reversed")
    first_count = int(exploratory_grid_size)
    second_count = int(validation_grid_size)
    if first_count < 9 or second_count <= first_count:
        raise ValueError("lambda validation grid must be finer than exploratory grid")

    def scan(count: int) -> tuple[np.ndarray, np.ndarray]:
        grid = np.linspace(lo, hi, count)
        values = np.asarray([float(objective(float(value))) for value in grid])
        if not np.all(np.isfinite(values)):
            raise RenyiNumericalError(f"non-finite {objective_name} order objective")
        return grid, values

    coarse_grid, coarse_values = scan(first_count)
    fine_grid, fine_values = scan(second_count)
    total_span = float(np.max(fine_values) - np.min(fine_values))
    if total_span <= float(flat_absolute_tolerance):
        return LambdaOptimisationResult(
            objective_name=str(objective_name),
            optimiser_kind="set-valued flat objective",
            order=None,
            objective=float(np.min(fine_values)),
            equivalent_order_lower=0.0,
            equivalent_order_upper=1.0,
            exploratory_grid_size=first_count,
            validation_grid_size=second_count,
            candidate_basin_count=0,
            refinement_discrepancy=abs(float(np.min(fine_values) - np.min(coarse_values))),
            endpoint_value_near_zero=float(objective(1.0e-8)),
            endpoint_value_near_one=float(objective(1.0 - 1.0e-8)),
            local_curvature=0.0,
        )

    local_indices = [
        index
        for index in range(1, len(coarse_grid) - 1)
        if coarse_values[index] <= coarse_values[index - 1]
        and coarse_values[index] <= coarse_values[index + 1]
    ]
    if coarse_values[0] <= coarse_values[1]:
        local_indices.insert(0, 0)
    if coarse_values[-1] <= coarse_values[-2]:
        local_indices.append(len(coarse_grid) - 1)
    if not local_indices:
        local_indices = [int(np.argmin(coarse_values))]
    refined: list[tuple[float, float]] = []
    for index in local_indices:
        left = coarse_grid[max(0, index - 1)]
        right = coarse_grid[min(len(coarse_grid) - 1, index + 1)]
        if left == right:
            refined.append((float(coarse_grid[index]), float(coarse_values[index])))
            continue
        solution = minimize_scalar(
            objective,
            bounds=(float(left), float(right)),
            method="bounded",
            options={"xatol": 2.0e-11, "maxiter": 500},
        )
        refined.append((float(solution.x), float(solution.fun)))
    best_order, best_value = min(refined, key=lambda item: (item[1], item[0]))
    fine_index = int(np.argmin(fine_values))
    fine_order = float(fine_grid[fine_index])
    fine_value = float(fine_values[fine_index])
    grid_step = float(fine_grid[1] - fine_grid[0])
    if abs(best_order - fine_order) > max(2.0 * grid_step, float(order_tolerance)):
        raise RenyiNumericalError(
            f"{objective_name} optimum depends materially on lambda-grid resolution"
        )
    step = max(1.0e-4, min(2.0e-3, 0.1 * min(best_order, 1.0 - best_order)))
    curvature: float | None
    if best_order - step > 0.0 and best_order + step < 1.0:
        curvature = float(
            (objective(best_order + step) - 2.0 * best_value + objective(best_order - step))
            / (step * step)
        )
    else:
        curvature = None
    return LambdaOptimisationResult(
        objective_name=str(objective_name),
        optimiser_kind="interior continuous minimum",
        order=best_order,
        objective=best_value,
        equivalent_order_lower=None,
        equivalent_order_upper=None,
        exploratory_grid_size=first_count,
        validation_grid_size=second_count,
        candidate_basin_count=len(local_indices),
        refinement_discrepancy=abs(best_value - fine_value),
        endpoint_value_near_zero=float(objective(1.0e-8)),
        endpoint_value_near_one=float(objective(1.0 - 1.0e-8)),
        local_curvature=curvature,
    )


def finite_difference_flatness(
    objective: Callable[[float], float], order: float, *, radius: float = 0.01
) -> tuple[float, float, float]:
    """Return left, centre, and right values for a reported local-flatness audit."""

    centre = _validate_order(order)
    width = float(radius)
    if width <= 0.0 or centre - width <= 0.0 or centre + width >= 1.0:
        raise ValueError("flatness radius leaves the Renyi-order domain")
    return (
        float(objective(centre - width)),
        float(objective(centre)),
        float(objective(centre + width)),
    )
