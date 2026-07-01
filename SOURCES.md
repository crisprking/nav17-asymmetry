# SOURCES.md — external citation ledger

Every external (non-database) claim this project leans on, with a stable
identifier, exactly what it supports, the evidence tier it maps to in
`QC_NOTES.md`, and a one-line note on what it does **not** support. Database
sources (gnomAD, ClinVar, Open Targets, HPO, single-cell atlases) are queried
live in the notebook and are not repeated here.

> **Verification posture.** These citations have been checked against primary
> sources across multiple review passes. Regan 2024 — the load-bearing clinical
> anchor — was re-confirmed directly against the *Circulation* article and its PMC
> record at the most recent revision. **No author should publish a citation they
> have not personally read.** The two most pivotal here (Regan 2024, MacDonald
> 2021) are flagged ⚑ for that reason.

---

## Clinical / pharmacology anchors

**⚑ Regan et al. — "Autonomic Dysfunction Linked to Inhibition of the Nav1.7 Sodium Channel."**
*Circulation* 2024. doi:10.1161/CIRCULATIONAHA.123.067331 · PMC11027978. (Merck.)
- **Supports:** the strongest claim in the project — that Nav1.7-block autonomic
  toxicity is **on-target and peripheral, in humans.** MK-2075 (human IC50
  85 nmol/L) produced dose-dependent decline in heart-rate variability and
  spontaneous baroreflex sensitivity in NHP and clinical effects in phase I;
  on-target confirmed by a more-selective JzTx-V peptide analogue reproducing the
  HRV effect; **no brain penetrance** by NHP whole-body autoradiography → effect is
  peripheral, not central. Authors explicitly name "phenotypic differences between
  acute pharmacological block versus genetic deficiency and the important role
  developmental compensation may play."
- **Does NOT support:** chronic dosing (phase I is short-duration); the human arm is
  small, healthy adult males.

**Mulcahy et al. — "ST-2560, a selective inhibitor of the NaV1.7 sodium channel, affects nocifensive and cardiovascular reflexes in non-human primates."**
*Br J Pharmacol* 2024; 181(17):3160–3171. doi:10.1111/bph.16398 · PMID 38715413.
- **Supports:** the efficacy/autonomic-overlap claim. IC50 39 nM; ≥1000× selective;
  analgesia at 3–5× IC50; 10–20 mmHg systolic/diastolic BP drop **at similar
  exposures.**
- **Does NOT support:** a *calculated* therapeutic index. The paper says "similar
  exposures." **Do not write "TI ≈ 1."** Primate, acute.

**Rothenberg et al. — "Safety, Tolerability, and Pharmacokinetics of GDC-0276, a Novel NaV1.7 Inhibitor … First-in-Human."**
*Clin Drug Investig* 2019; 39(9):873–887. PMID 31172446. (Genentech.)
- **Supports:** the published anchor for the exposure observation — hypotension was
  dose-limiting in the **fast cyclodextrin** formulation (higher Cmax/AUC), while
  the slower powder-in-capsule arm was dose-limited instead by transaminase
  elevations.
- **Does NOT support:** the *rate-vs-total-exposure* attribution as the paper's own
  conclusion. The trial does not disentangle peak (Cmax) from total (AUC); the
  "rate-dependence" reading is **our interpretation** and is labeled as such.

**Safina, Sutherlin et al.** *J Med Chem* 2021; 64(6):2953–2966.
- **Supports:** identity of the two acyl-sulfonamide candidates (GDC-0276 / GDC-0310). Chemistry context only.

---

## Mechanism / genetics anchors

**Deng et al. — "Nav1.7 is essential for nociceptor action potentials in the mouse in a manner independent of endogenous opioids."**
*Neuron* 2023; 111(17):2642–2659.e13. PMID 37352856 (open access). (Hackos senior, Genentech.)
- **Supports:** Nav1.7 block silences C-fibers; the BP effect is on-target
  (binding-site-mutant mouse); analgesia is **opioid-independent** in their model.
  The Discussion itself names autonomic effects as potentially efficacy-limiting.
- **Does NOT support:** a settled mechanism — see MacDonald, directly below.

**⚑ MacDonald et al. — "A central mechanism of analgesia in mice and humans lacking the sodium channel NaV1.7."**
*Neuron* 2021; 109(9):1497–1512. PMID 33823138. (Wood/UCL.)
- **Supports (and complicates):** the **counter-finding** — Nav1.7-null mice have
  "essentially normal nociceptor activity," and human Nav1.7-null analgesia is
  **opioid-dependent and naloxone-reversible.** Two top labs, same journal, opposite
  conclusions on mechanism.
- **Use:** cite alongside Deng to present the mechanism as **contested**, not to
  pick a side. The autonomic-asymmetry thesis is independent of this dispute.

**Cox et al. — "An SCN9A channelopathy causes congenital inability to experience pain."**
*Nature* 2006; 444:894–898. PMID 17167479.
- **Supports:** the foundational genetics — CIP is recessive, biallelic *SCN9A*
  loss-of-function, confirmed by patch-clamp.
- **Does NOT support:** any blood-pressure / autonomic measurement. **It does not
  report BP.** The "cardiovascular-silent" claim must be sourced to the HPO analysis
  (absence of annotated CV terms) and to Iseppon et al. 2024 ("autonomic function appears
  normal"), **not** to Cox.

---

## Independent corroboration (the thesis is convergent, not contrarian)

**Iseppon et al. — "Sodium channels Nav1.7, Nav1.8 and pain; two distinct mechanisms for Nav1.7 null analgesia."** *(first author Iseppon; Jing Zhao is a co-author)*
*Neurobiology of Pain* 2024. PMID 39559752. (Wood/UCL.)
- **Supports:** the verbatim conclusion — pharmacological Nav1.7 inhibition causes
  "dramatic side-effects on the autonomic nervous system with no therapeutic window
  … specific Nav1.7 channel blockers will fail as analgesic drugs"; autonomic
  function normal in genetic nulls.
- **Strategic note:** this is third-party validation **and** evidence that the
  diagnosis is now consensus. Frame the project as *synthesis + one open question*,
  not as a lone correction of the field.

**Yang et al. — "Discordance between preclinical and clinical testing of NaV1.7-selective inhibitors for pain."** *(first author Yang; Ratté & Prescott are co-senior)*
*Pain* 2025; 166(3):481–501 (epub 2024 Oct 23). PMID 39928833. doi:10.1097/j.pain.0000000000003425 (open access). (SickKids.)
- **Supports:** an independent 2024 framing of the same preclinical-to-clinical
  failure gap. Reinforces the convergence point.

**Pharmacological Reviews 2025 review.**
- **Supports:** an independent statement of the genetic-vs-pharmacological asymmetry
  (BP falls with ST-2560 in primates; normal in LoF patients). General-review tier.

---

## What this body of evidence is — and is not

It is: **human genetics** (natural experiment), **preclinical pharmacology** (NHP),
**phase I clinical-trial data**, and **basic/mechanistic science**.

It is **not Real-World Evidence (RWE).** In the FDA/EMA/ICH framework, RWE means
data generated in routine clinical care — EHRs, claims, registries, wearables,
observational studies. None of the above qualifies. Do not describe this package as
RWE; doing so is a category error a regulatory-literate reviewer will catch. Making
it RWE-grade would require a different study (e.g., an OMOP/OHDSI query of EHRs for
biallelic *SCN9A* carriers' longitudinal vitals).
