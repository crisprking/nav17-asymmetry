# PREREGISTRATION.md — the two-sided-squeeze prediction

**Status:** pre-registered · **Date locked:** 2026-06-30 · **Direction commitment:**
this prediction will be reported here whether it is confirmed, refuted, or returns
inconclusive. A null is a result.

---

## Background (one paragraph)

Genetic Nav1.7 loss is analgesic and cardiovascular-silent; acute pharmacological
block drops blood pressure at the exposures that relieve pain (Mulcahy 2024), and
that autonomic toxicity is on-target and peripheral in humans (Regan 2024,
*Circulation*). The standard escape proposed for this is **kinetic**: dose slowly
(or use an ASO/biologic onset) so autonomic neurons adapt and the BP effect wanes.
This project's contribution is to name the **opposing** constraint on the analgesic
side: the same slow onset that lets autonomic neurons compensate may also let
**nociceptors** compensate, eroding analgesia. Hence a *two-sided squeeze*. The
homeostat in this repo formalises the tradeoff but its quantitative output
(`γ_noci ≥ 1.84`) is assumption-driven (see `QC_NOTES.md`, TIER 2) — it sharpens
the question, it does not answer it. Only a bench experiment answers it.

## The hypothesis (H_squeeze)

> Under chronic / slow-onset Nav1.7 block titrated into the exposure window where
> the **autonomic** (blood-pressure / baroreflex) effect has measurably attenuated
> relative to acute dosing, the **analgesic** effect will *also* attenuate over the
> same timescale — i.e., the kinetic window that buys autonomic safety does not
> come for free on the efficacy side.

## The decisive experiment (the one measurement that settles it)

In an animal model with a validated Nav1.7-dependent nociceptive readout **and**
continuous cardiovascular monitoring (e.g., telemetered rodent or NHP):

1. Establish the **acute** dose–response for (a) antinociception and (b) the
   blood-pressure / baroreflex effect.
2. Administer the **same compound chronically / slow-onset** to reach a matched
   steady-state unbound exposure.
3. At steady state, measure the **paired** change in (a) antinociception and
   (b) the cardiovascular effect, each relative to its acute value.

## Pre-committed outcomes

| Outcome at matched steady-state exposure | Verdict |
|---|---|
| BP effect attenuates **and** analgesia attenuates (both vs. acute) | **H_squeeze SUPPORTED** — the kinetic escape is self-limiting |
| BP effect attenuates **and** analgesia is preserved | **H_squeeze REFUTED** — slow dosing is a clean escape; the two-sided framing is wrong |
| Neither attenuates | the kinetic-escape premise itself fails (autonomic adaptation absent); H_squeeze not tested |
| Analgesia attenuates but BP does not | off-thesis; revisit model assumptions |

## What would falsify H_squeeze

A single well-powered chronic-vs-acute experiment in which the autonomic effect
attenuates while analgesia is preserved at matched exposure **refutes** the
prediction. The author commits to recording that refutation here.

## Scope and honesty boundaries

- This is a **prediction about a future bench experiment**, not a claim that current
  data demonstrate the squeeze. No published dataset currently runs the
  chronic-vs-acute paired design above.
- `γ_noci ≥ 1.84` is **not** the prediction; it is an illustrative threshold whose
  value is set by chosen efficacy/safety cutoffs (`QC_NOTES.md`). The prediction is
  the **direction** in the table above.
- The mouse expression "asymmetry" is definitional/fragile (`QC_NOTES.md`) and is
  **not** evidence for H_squeeze. The expression arm is hypothesis-generating only.

## Provenance

Lock this file's hash at publication and reference it from the manuscript/Substack:

```bash
sha256sum PREREGISTRATION.md
```

Cite the resulting digest (and the commit SHA) wherever the two-sided squeeze is
described, so the prediction is timestamped and tamper-evident.
