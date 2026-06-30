"""
Two-timescale homeostat + D1 ("go-slow") decision model for Nav1.7 block.

The clinical idea this tests: lifelong genetic Nav1.7 loss (CIP) is analgesic AND
cardiovascular-silent, while acute pharmacological block drops blood pressure at
the same exposures that relieve pain. If the autonomic effect is RATE-dependent,
a slow-onset modality (ASO / gradual titration) might escape it. But the same
slowness lets nociceptors compensate the analgesia away. This module makes that
two-sided tradeoff explicit.

Homeostat (integral feedback), per cell type:
    dg/dt = (u - (1+gamma) g) / tau
    deficit = u - g           # the UNCOMPENSATED Nav1.7 block actually felt
    steady-state (const u):  g_ss = u/(1+gamma)  ->  deficit_ss = u * gamma/(1+gamma)

  * NOCICEPTOR deficit IS the analgesia  -> want LARGE & durable -> gamma_noci HIGH
  * AUTONOMIC  deficit IS the toxicity   -> want SMALL          -> gamma_auto LOW
  * deficit_ss depends ONLY on gamma, NOT tau. tau sets the titration race.

IMPORTANT (see QC_NOTES.md): the *thresholds* ANALGESIA_MIN and AUTO_MAX, and the
maximal block U_MAX, are MODELLING ASSUMPTIONS, not measured constants. The
headline "required gamma_noci" is therefore an illustrative decision boundary
whose value is set mostly by the ratio ANALGESIA_MIN / AUTO_MAX (see
`gn_crit` and the identity below), NOT by measured biology. Treat it as a
framework that names an experiment, not as an empirical threshold.
"""
from __future__ import annotations
import numpy as np

# Default decision thresholds (ASSUMPTIONS — change them and the boundary moves)
U_MAX = 0.70            # Nav1.7 block fraction at full dose
ANALGESIA_MIN = 0.25    # need >= this uncompensated nociceptor deficit to be useful
AUTO_MAX = 0.10         # autonomic residual deficit must stay <= this to be safe


def deficit(u_t: np.ndarray, t: np.ndarray, tau: float, gamma: float) -> np.ndarray:
    """Forward-Euler integral-feedback deficit trajectory for a drive u(t)."""
    u_t = np.asarray(u_t, float); t = np.asarray(t, float)
    g = np.zeros_like(u_t)
    for k in range(1, len(t)):
        g[k] = g[k - 1] + (t[k] - t[k - 1]) * (u_t[k - 1] - (1.0 + gamma) * g[k - 1]) / tau
    return u_t - g


def deficit_ss(gamma: float, u: float = U_MAX) -> float:
    """Closed-form steady-state uncompensated deficit for a constant drive u."""
    return u * gamma / (1.0 + gamma)


def gn_crit(gamma_auto: float, auto_max: float = AUTO_MAX,
            anal_min: float = ANALGESIA_MIN) -> float:
    """Critical gamma_noci: the smallest nociceptor leak for which SOME chronic
    block u keeps autonomic deficit <= auto_max while analgesia >= anal_min.

    Identity worth knowing: when anal_min == auto_max, required gamma_noci ==
    gamma_auto. The multiplier above that is the COST of demanding more analgesic
    deficit than autonomic tolerance (anal_min/auto_max), not a biological fact.
    Returns np.inf when no feasible block exists.
    """
    u = min(auto_max * (1.0 + gamma_auto) / gamma_auto, 1.0)  # hardest safe chronic block
    r = anal_min / u
    return np.inf if r >= 1 else r / (1.0 - r)


def d1_decision(gamma_auto: float, gamma_auto_ci=None,
                auto_max: float = AUTO_MAX, anal_min: float = ANALGESIA_MIN) -> dict:
    """Summarise the D1 feasibility at a (fitted) autonomic leak gamma_auto.

    gamma_auto is itself a fit to a digitised blood-pressure trace (see
    QC_NOTES.md) — confirm its provenance before quoting the number. The CI, if
    given as (lo, hi), is propagated to a range on the required gamma_noci.
    """
    out = {
        "gamma_auto": gamma_auto,
        "max_safe_chronic_block_U": round(min(auto_max * (1.0 + gamma_auto) / gamma_auto, 1.0), 3),
        "required_gamma_noci": round(gn_crit(gamma_auto, auto_max, anal_min), 3),
        "thresholds": {"ANALGESIA_MIN": anal_min, "AUTO_MAX": auto_max},
        "note": "required_gamma_noci is an ASSUMPTION-driven decision boundary, "
                "not a measured threshold (set largely by ANALGESIA_MIN/AUTO_MAX).",
    }
    if gamma_auto_ci is not None:
        lo, hi = gamma_auto_ci
        out["required_gamma_noci_range"] = [
            round(gn_crit(hi, auto_max, anal_min), 3),  # adverse leak -> higher requirement
            round(gn_crit(lo, auto_max, anal_min), 3),
        ]
    return out
