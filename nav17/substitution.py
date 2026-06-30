"""
Nav1.7 substitution-capacity engine.

Turns a [cell_type x gene] pseudobulk expression table into a per-cell-type
"substitution index": how well a cell could run *without* Nav1.7, given the
threshold-capable sodium channels and the M-current brake it expresses.

    substitution_index = ( sum[SCN1A,SCN2A,SCN3A,SCN8A]  +  sum[KCNQ2,KCNQ3,KCNQ5] )
                         / ( SCN9A + eps )

Rationale (see QC_NOTES.md for the load-bearing caveat):
  * Only TTX-S threshold Na channels that activate near rest (Nav1.1/1.2/1.3/1.6)
    can stand in for Nav1.7's subthreshold-amplifier role. Nav1.8/1.9 (TTX-R,
    upstroke / ultraslow) are deliberately NOT counted as substitutes in the
    primary index — this is a *modelling choice*, and the headline result is
    sensitive to it (the robustness grid flips when Nav1.8/1.9 are credited).
  * KCNQ (M-current) is an independent threshold-retuning axis.
  * The index is a WITHIN-cell-type ratio, so it is invariant to per-sample
    (CPM) normalisation.

Pure numpy / pandas. No network, no file IO. Importable and unit-testable.
"""
from __future__ import annotations
import hashlib
import json
import pandas as pd

# gene -> (protein, role, counts as a Nav1.7 threshold substitute?)
NAV = {
    "SCN1A":  ("Nav1.1", "threshold_TTXs", True),
    "SCN2A":  ("Nav1.2", "threshold_TTXs", True),
    "SCN3A":  ("Nav1.3", "threshold_TTXs", True),   # injury-inducible
    "SCN8A":  ("Nav1.6", "threshold_TTXs", True),
    "SCN9A":  ("Nav1.7", "TARGET",         False),
    "SCN10A": ("Nav1.8", "upstroke_TTXr",  False),
    "SCN11A": ("Nav1.9", "ultraslow_TTXr", False),
}
SUBSTITUTORS = [g for g, v in NAV.items() if v[2]]   # SCN1A/2A/3A/8A
KCNQ = ["KCNQ2", "KCNQ3", "KCNQ5"]                    # M-current brake
TARGET = "SCN9A"


def substitution_capacity(pb: pd.DataFrame, eps: float = 1.0) -> pd.DataFrame:
    """pb: [cell_type x gene] mean expression (any consistent unit, e.g. CPM).

    Returns a frame with the numerator components and the substitution_index,
    sorted high -> low. HIGH index => the cell type carries backup for Nav1.7's
    threshold role (predict it ADAPTS to loss). LOW => Nav1.7-monodependent.
    """
    have = lambda gs: [g for g in gs if g in pb.columns]
    sub = pb[have(SUBSTITUTORS)].sum(axis=1)
    mcur = pb[have(KCNQ)].sum(axis=1)
    nav17 = pb[TARGET] if TARGET in pb.columns else pd.Series(eps, index=pb.index)
    out = pd.DataFrame({"sub_nav": sub, "m_current": mcur, "nav1_7": nav17})
    out["substitution_index"] = (sub + mcur) / (nav17 + eps)
    return out.sort_values("substitution_index", ascending=False)


def asymmetry_verdict(cap: pd.DataFrame, nociceptor_types, autonomic_types,
                      inputs_meta: dict, margin: float = 0.30) -> dict:
    """The hypothesis (H1) is supported only if autonomic substitution capacity
    EXCEEDS nociceptor capacity by `margin`. Verdict is content-addressed
    (sha256) and explicitly falsifiable in either direction.
    """
    noc = float(cap.reindex(nociceptor_types)["substitution_index"].dropna().mean())
    aut = float(cap.reindex(autonomic_types)["substitution_index"].dropna().mean())
    d = aut - noc
    if d > margin:
        call = "SUPPORTS_H1 (autonomic can substitute, nociceptor cannot)"
    elif d < -margin:
        call = "AGAINST_H1 (nociceptor has MORE backup -> analgesia erodes, tox persists)"
    else:
        call = "INCONCLUSIVE (no decisive asymmetry -> repertoire alone does not decide the lever)"
    payload = dict(
        nociceptor_index=round(noc, 3), autonomic_index=round(aut, 3),
        margin_required=margin, observed_gap=round(d, 3), call=call,
        gene_sets=dict(substitutors=SUBSTITUTORS, m_current=KCNQ, target=TARGET),
        inputs=inputs_meta,
    )
    payload["sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16]
    return payload
