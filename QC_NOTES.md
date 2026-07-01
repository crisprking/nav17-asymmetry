# QC_NOTES.md — evidence tiering and senior-review audit

> **Changelog (this revision).** Three surgical corrections vs. the prior version,
> each closing a flagged overclaim or adding a verified anchor:
> (1) the acute-block row no longer reads "(TI ≈ 1)" — Mulcahy reports *overlapping
> exposures*, not a calculated therapeutic index;
> (2) three TIER-1 anchors added — **Regan 2024 (Circulation)**, **Iseppon 2024
> (Neurobiology of Pain)**, **MacDonald 2021 (Neuron)** — with the Deng/MacDonald
> *mechanism* dispute flagged explicitly;
> (3) audit footer updated to the current notebook revision. No TIER-2/3 numbers changed.

This file is the result of a line-by-line quality-control pass over the analysis
notebook. It exists so that nothing in this repo gets cited at the wrong
confidence level. **The honesty about tiers is the deliverable, not a disclaimer.**

Three tiers are used:

- **TIER 1 — Empirical & reproducible.** Pulled live from a public database or
  taken from a peer-reviewed paper; re-runs to the same number. Safe to cite.
- **TIER 2 — Illustrative model.** A framework / decision boundary whose output
  is set largely by chosen assumptions, not measured constants. Cite the *shape*
  of the argument, never the specific number as if it were measured.
- **TIER 3 — Broken / void in this run.** Did not produce a usable result; the
  notebook correctly flags and discards it. Not used downstream. Do not cite.

---

## TIER 1 — Empirical & reproducible (safe to cite)

| Claim | Value | Source | Status |
|---|---|---|---|
| `SCN9A` is LoF-tolerant at population scale | LOEUF 0.81, pLI 0.00, o/e 131/187 | gnomAD v4.1 GraphQL (live) | Reproduces exactly (notebook G1) |
| Family contrast: `SCN1A` constrained, `SCN5A` intermediate | LOEUF 0.11 / 0.38 | gnomAD v4.1 | Reproduces (G1, G6) |
| LoF-tolerance is tissue-stratified (peripheral Nav1.7/1.8/1.9 tolerant; CNS/cardiac constrained) | — | gnomAD v4.1 (G6/G6b) | Reproduces |
| `SCN9A` disease associations are pain/sensory-dominated, not cardiovascular | 16 pain vs 7 CV-binned | Open Targets Platform GraphQL (live, HTTP 200) | Reproduces (G-OpenTargets). *Caveat below.* |
| CIP (genetic Nav1.7 loss) is **cardiovascular-silent** in HPO; footprint is sudomotor + anosmia, unlike reference dysautonomias | CV subsystem count = 0 (CIP) vs ≥1 (HSAN4, familial dysautonomia) | HPO `phenotype.hpoa` (G8/G9) | Reproduces. *This is **absence of annotated CV terms**, not a measured longitudinal BP study — caption accordingly.* |
| `SCN9A` missense is a "VUS swamp"; standard predictors calibrate on controls but not here | 69% VUS; controls AUROC 0.83–0.99 | ClinVar via myvariant.info (G2/G4) | Reproduces |
| Acute Nav1.7 block drops BP at the **same exposures that relieve pain** (efficacy and autonomic windows overlap; **not** a calculated therapeutic index) | 10–20 mmHg at 3–5× IC50; IC50 39 nM | **Mulcahy et al., Br J Pharmacol 2024**, 181(17):3160–3171, doi:10.1111/bph.16398 | Verified. Paper states "similar exposures"; *do not write "TI ≈ 1."* |
| **In humans**, a peripherally-restricted Nav1.7 inhibitor (no brain penetrance) produced dose-dependent autonomic effects → toxicity is **on-target and peripheral** | human IC50 85 nmol/L; HRV + baroreflex decline; on-target confirmed by JzTx-V peptide analogue; no brain penetrance (NHP autoradiography) | **Regan et al., Circulation 2024**, doi:10.1161/CIRCULATIONAHA.123.067331, PMC11027978 | Verified (re-confirmed against primary source this revision). **Strongest clinical anchor in the project.** |
| Independent 2024 statement of the failure thesis | "specific Nav1.7 channel blockers will fail as analgesic drugs"; autonomic function normal in genetic nulls | **Iseppon et al., Neurobiology of Pain 2024**, PMID 39559752 (Wood/UCL) | Verified — verbatim quote. Note: this means the thesis is **convergent**, not contrarian. |
| Nav1.7 BP effect is **on-target** (binding-site-mutant mouse); block silences C-fibers; **opioid-independent** | — | **Deng et al., Neuron 2023**, 111(17):2642–2659.e13, PMID 37352856 (open access) | Verified. *See contested-mechanism note below.* |
| GDC-0276 first-in-human: liver-transaminase elevations + hypotension; hypotension dose-limiting in the fast cyclodextrin formulation | — | **Rothenberg et al., Clin Drug Investig 2019**, 39(9):873–887, PMID 31172446 | Verified — the *published* anchor for the exposure/rate observation |
| Two acyl-sulfonamide candidates are GDC-0276 / GDC-0310 | — | Safina & Sutherlin et al., J Med Chem 2021, 64(6):2953–2966 | Verified |
| Independent statement of the asymmetry (BP falls with ST-2560 in primates; normal in LOF patients) | — | Pharmacological Reviews 2025 review | Verified |

**Contested mechanism (cite both, settle neither).** Deng 2023 and MacDonald 2021
were published in the **same journal** and disagree on the mechanism of CIP
analgesia: **MacDonald et al., Neuron 2021**, 109(9):1497–1512, PMID 33823138
(Wood/UCL) reports Nav1.7-null mice have "essentially normal nociceptor activity"
and that human Nav1.7-null analgesia is **opioid-dependent and naloxone-reversible**
— the opposite of Deng on both counts. The autonomic-asymmetry thesis in this repo
does **not** depend on which is right, but any write-up must present the mechanism as
**unsettled**, not as Deng-settled.

**Caveat on the Open Targets 16-vs-7 split:** the keyword binner mis-files
*primary erythermalgia* (= erythromelalgia, a Nav1.7 **gain-of-function pain**
disorder) and *hemorrhoid* into the "cardiovascular/autonomic" bin. Correcting
the misbin makes the pain-dominance **stronger**, but do not quote "16 vs 7" as a
precise figure — quote the qualitative direction. *(Fix: tighten the AUTO/PAIN
keyword lists; `erythermalgia` should map to PAIN.)*

---

## TIER 2 — Illustrative model (cite the argument, not the number)

These are the homeostat / D1 outputs. The qualitative claim is defensible and is
the project's original contribution; the specific numbers are assumption-driven.

| Output | Value | Why it is TIER 2 |
|---|---|---|
| Two-sided constraint exists: the slow onset that spares autonomics also lets nociceptors compensate analgesia away | qualitative | **This is the sound, original point.** Safe to state as a logical/mechanistic argument. |
| `required_gamma_noci ≥ 1.84` ("nociceptor must retain ≥65% of block at steady state") | 1.84 (CI 1.07–2.50) | The notebook's own sensitivity cell shows this number is set **mostly by the ratio ANALGESIA_MIN/AUTO_MAX = 0.25/0.10 = 2.5**, an assumed efficacy/safety pair — *not* by biology. Identity: when those two thresholds are equal, required γ_noci = γ_auto. **Do not present 1.84 as a measured threshold.** |
| `gamma_auto = 0.35` (autonomic adaptation leak) | 0.35 (CI 0.26–0.40) | Fit to a **single digitised Rothenberg-2019 BP trace**. The CI is fit-noise only, from one trace. **Action item: confirm the digitised trace is real extracted data, not a placeholder, before this feeds any published figure.** |
| Biophysics state-dependent block ratios (noci/auto) | 1.08–1.97 | Labeled in-code as "illustrative, grounded params"; HH params are textbook, resting-Vm assumptions are reasoned but not fitted. |
| `U_MAX = 0.70`, `ANALGESIA_MIN = 0.25`, `AUTO_MAX = 0.10` | — | Chosen thresholds, not measured. They drive everything downstream. |

**Bottom line for the manuscript/Substack:** the *rate-dependence reframe* and the
*two-sided squeeze* are legitimate and original. The number **γ_noci ≥ 1.84** must
be framed as "under these illustrative efficacy/safety cutoffs, the lever needs a
nociceptor that barely compensates" — i.e., a hypothesis-sharpening device that
names a bench experiment, not a result. The decisive experiment is unchanged:
**chronic vs acute Nav1.7 block — does the BP effect wane while analgesia grows?**
(see `PREREGISTRATION.md`).

---

## TIER 3 — Broken / void in this run (correctly flagged, not cited)

| Arm | What happened | Notebook's handling |
|---|---|---|
| **Human expression (SPARC ds465, sympathetic snMultiome)** | Deposited matrix is **row-decoupled from its annotations** — all 12 textbook macrophage markers read ~1× in their own 0.988-pure cluster; every per-gene number reads the *wrong gene*. Markers TH/DBH at floor → ambient-dominated. | Correctly diagnosed; verdict `UNINTERPRETABLE_AMBIENT_DOMINATED` / `MAPPING BROKEN`. Voided, not patched. ✅ Right call. |
| **AlphaMissense calibration (G2 first version)** | Remote tabix unsupported in-kernel; control gene PAH AUROC = None. | QC gate fired "do NOT interpret SCN9A." Superseded by the myvariant.info VUS-swamp version. ✅ |
| **Census / decoupler loaders** | `ModuleNotFoundError` (offline kernel can't reach S3 or pip-install). | Environment failure, not logic failure; code restructured to run internet-on elsewhere. |

---

## The most important QC finding — read this

The **mouse expression "asymmetry"** (the registered PRIMARY for question 2) is
**DEFINITIONAL, not robust.** On the correct populations (SYNOR/SYCHO sympathetic
vs PSPEP/PSNP nociceptor), the autonomic-over-nociceptor substitution gap is:

| channel definition | auto/noci ratio | holds? |
|---|---|---|
| original (CNS-Nav + KCNQ, Nav1.8/1.9 excluded) | **6.32×** | yes |
| credit Nav1.8/1.9 as nociceptor backups | **1.38×** | barely |
| drop the M-current term | **0.43×** | **inverts** |

and **74% of the original gap comes from the M-current (KCNQ) term, only 26% from
Nav substitution.** So "autonomic neurons can substitute for Nav1.7 but
nociceptors can't" depends entirely on (a) excluding Nav1.8/1.9 from the
nociceptor's repertoire and (b) including KCNQ. The notebook says this itself
(robustness grid → "DEFINITIONAL") and reconciles it honestly:

> *expression arm predicted favorable γ_auto, BUT the static proxy is weak, and the
> direct dynamic fit gives γ_auto = 0.35 → adverse. **Static optimism, dynamic
> pessimism.***

**Implication for any public write-up:** do **not** claim the expression data
*shows* the asymmetry. The honest statement is that the asymmetry is **not robustly
supported** — the static repertoire proxy is fragile and the human confirmatory
arm is broken. This is exactly why the falsifiable bench test, not the expression
index, is the load-bearing next step.

---

## Code-level cleanup (notebook hygiene, before publishing the repo)

1. **Drop stray/duplicate cells:** cell 5 (pasted output, not code), cell 36
   (f-string bug `:.1f }` → `ValueError`, fully superseded by cell 37), cell 58
   (verbatim duplicate of cell 57 / G9), cell 60 (empty), and the voided run in
   cell 17 (keyword auto-detector swept CNS neurons into "nociceptor").
2. **Consolidate the ~6 near-duplicate Census loaders** (cells 7, 9, 11, 12, 13,
   15) into one canonical module — already done here as `nav17/substitution.py`
   plus one loader notebook.
3. **Add provenance hashes** to the result cells currently missing them
   (G5 / G6b / mouse robustness grid emit no `prov sha256`).
4. **Confirm the SCN9A isoform length.** G5 projects onto UniProt Q15858 and the
   header says 1977 aa, but the cell text elsewhere references 1988 aa. The
   placement reports WT-concordance 1.000 at offset 0, so the mapping is internally
   consistent — but pin the exact isoform/version in the figure caption so a
   structural reviewer can reproduce the domain assignment.
5. **Fix the Open Targets keyword binner** (see Tier 1 caveat) so erythromelalgia
   is counted as pain, not cardiovascular.
6. Replace deprecated `datetime.utcnow()` calls (cosmetic warnings).

---

*Audit performed against the current research notebook (`nav1-7-project`, 65-cell
revision). External citations re-verified against primary sources, including a
fresh re-confirmation of Regan 2024 (Circulation) at this revision. The `nav17/`
engine is an extracted, unit-tested reimplementation of the notebook's core;
`python -m pytest -q` reproduces the synthetic verdict (gap 2.18) and the
γ_noci = 1.84 boundary.*
