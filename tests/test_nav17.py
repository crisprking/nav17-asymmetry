"""Unit tests for the nav17 engine. Run: pytest -q  (or python -m pytest)."""
import numpy as np
import pandas as pd
from nav17 import (substitution_capacity, asymmetry_verdict,
                   deficit, deficit_ss, gn_crit, d1_decision)


def _example_pb():
    return pd.DataFrame({
        "SCN1A": [8, 6, 10, 14, 16], "SCN2A": [3, 2, 4, 10, 11],
        "SCN3A": [5, 4, 6, 12, 10], "SCN8A": [15, 12, 20, 18, 16],
        "SCN9A": [50, 46, 38, 35, 33], "SCN10A": [42, 48, 18, 1, 1],
        "SCN11A": [26, 30, 10, 1, 1], "KCNQ2": [10, 8, 14, 30, 28],
        "KCNQ3": [6, 5, 9, 22, 24], "KCNQ5": [4, 3, 6, 14, 12],
    }, index=["DRG_peptidergic", "DRG_nonpeptidergic", "DRG_Adelta_LTMR",
              "Sympathetic_NA", "Sympathetic_chol"])


def test_substitution_index_matches_definition():
    pb = _example_pb()
    cap = substitution_capacity(pb)
    # hand-check sympathetic_chol: (16+11+10+16)+(28+24+12) = 53+64 = 117; /(33+1)=3.441
    assert abs(cap.loc["Sympathetic_chol", "substitution_index"] - 3.441) < 1e-2
    # The ratio is scale-invariant in the eps->0 limit (the design intent: a
    # within-cell-type ratio robust to per-sample CPM scaling). With the default
    # eps=1.0 regulariser the +eps term in the denominator breaks exact
    # invariance slightly; it vanishes as eps->0. Verify both facts.
    pb2 = pb.copy(); pb2.loc["Sympathetic_chol"] *= 7.0
    cap2_eps0 = substitution_capacity(pb2, eps=1e-9)
    cap_eps0 = substitution_capacity(pb, eps=1e-9)
    assert abs(cap2_eps0.loc["Sympathetic_chol", "substitution_index"]
               - cap_eps0.loc["Sympathetic_chol", "substitution_index"]) < 1e-4
    # with default eps the deviation is small but non-zero (regularised, by design)
    cap2 = substitution_capacity(pb2)
    assert abs(cap2.loc["Sympathetic_chol", "substitution_index"]
               - cap.loc["Sympathetic_chol", "substitution_index"]) < 0.15


def test_asymmetry_verdict_is_deterministic_and_directional():
    pb = _example_pb(); cap = substitution_capacity(pb)
    noci = [t for t in pb.index if t.startswith("DRG")]
    auto = [t for t in pb.index if t.startswith("Sympathetic")]
    v1 = asymmetry_verdict(cap, noci, auto, {"src": "test"})
    v2 = asymmetry_verdict(cap, noci, auto, {"src": "test"})
    assert v1["sha256"] == v2["sha256"]           # content-addressed, reproducible
    assert v1["observed_gap"] > 0.30
    assert v1["call"].startswith("SUPPORTS_H1")
    # swapping the labels must flip the verdict sign
    vflip = asymmetry_verdict(cap, auto, noci, {"src": "test"})
    assert vflip["observed_gap"] < -0.30


def test_homeostat_steady_state_closed_form():
    t = np.linspace(0, 20000, 20000); u = np.full_like(t, 0.7)
    d = deficit(u, t, tau=120.0, gamma=0.4)
    assert abs(d[-1] - deficit_ss(0.4, 0.7)) < 1e-3   # numeric == analytic
    # deficit_ss depends only on gamma, not tau
    d_fast = deficit(u, t, tau=10.0, gamma=0.4)
    assert abs(d_fast[-1] - d[-1]) < 1e-3


def test_gn_crit_identity_and_value():
    # documented identity: anal_min == auto_max  =>  required gamma_noci == gamma_auto
    for ga in (0.2, 0.35, 0.6):
        assert abs(gn_crit(ga, auto_max=0.10, anal_min=0.10) - ga) < 1e-6
    # the headline value reproduced
    assert abs(gn_crit(0.35, auto_max=0.10, anal_min=0.25) - 1.842) < 1e-2


def test_d1_decision_ci_range_orientation():
    dec = d1_decision(gamma_auto=0.35, gamma_auto_ci=(0.26, 0.40))
    lo, hi = dec["required_gamma_noci_range"]
    assert lo > hi   # adverse (lower) leak demands a HIGHER gamma_noci -> wider range top
    assert abs(dec["required_gamma_noci"] - 1.842) < 1e-2
