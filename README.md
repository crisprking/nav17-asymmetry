# nav17-asymmetry

**Why the best-validated pain target keeps failing: a genetic–pharmacological asymmetry at Nav1.7 — analysed entirely from open data.**

Nav1.7 (`SCN9A`) is the most genetically validated non-opioid pain target known: people born without it feel no pain, with no reported cardiovascular dysautonomia. Yet fifteen years of selective inhibitors keep dying in development. This repo asks *why* — using only public databases (gnomAD, ClinVar, Open Targets, HPO, single-cell atlases) and the published trial record — and lands on one reframe: **lifelong genetic loss and acute pharmacological block are not the same intervention.** Genetic loss is analgesic *and* cardiovascular-silent; acute block drops blood pressure at the exposures that relieve pain. The barrier is rate-dependent, and "go slow to escape it" runs into a second, opposing constraint on the analgesic side.

As of 2024 this is no longer a contrarian read — it is convergent. In humans, a peripherally-restricted Nav1.7 inhibitor (MK-2075, **no brain penetrance** by primate whole-body autoradiography) produced dose-dependent autonomic effects, establishing the toxicity as **on-target and peripheral** (Regan et al., *Circulation* 2024). A second 2024 paper states the conclusion outright — selective Nav1.7 blockers "will fail as analgesic drugs" (Iseppon et al., *Neurobiology of Pain* 2024) — and a third independently frames the preclinical-to-clinical "discordance" (Yang et al., *Pain* 2025). This repo's contribution is not the diagnosis; it is (a) reproducing the genetic-safety side from open data and (b) naming the one bench experiment that resolves the remaining open question.

> **One mechanism caveat, stated up front:** the *mechanism* of CIP analgesia is contested. Deng et al. (*Neuron* 2023, Genentech) report Nav1.7 is required for C-fiber action potentials and the analgesia is opioid-independent; MacDonald et al. (*Neuron* 2021, Wood/UCL) report Nav1.7-null mice have essentially normal nociceptor activity and the human analgesia is opioid-dependent and naloxone-reversible. This repo's autonomic-asymmetry thesis holds either way — but nothing here should be read as settling that dispute.

> **Read [`QC_NOTES.md`](QC_NOTES.md) before citing any number.** It states plainly which results are empirical and reproducible, which are illustrative model outputs whose value depends on assumptions, and which arms are broken. That tiering is the point of this project. Full citation ledger with PMIDs/DOIs: [`SOURCES.md`](SOURCES.md).

---

## What problem does it solve?

It tests, against open data, three questions a Nav1.7 program has to answer:

1. **Is losing Nav1.7 safe at the genetic level?** (constraint + phenotype-ontology evidence)
2. **Do nociceptors and autonomic neurons differ in their ability to run *without* Nav1.7?** — the molecular asymmetry the "slow-titration / ASO" escape depends on. (single-cell substitution index)
3. **Could a slow-onset drug thread the needle?** — a two-timescale homeostat that makes the autonomic-vs-analgesic tradeoff explicit and names the one bench measurement that would settle it.

## What's the input format?

The reusable engine (`nav17/`) consumes a **pseudobulk expression table**: a CSV (or pandas DataFrame) of `cell_type × gene`, any consistent unit (CPM recommended), with at least these columns where available:

```
SCN1A SCN2A SCN3A SCN8A SCN9A SCN10A SCN11A KCNQ2 KCNQ3 KCNQ5
```

See [`examples/example_pseudobulk.csv`](examples/example_pseudobulk.csv) for the exact shape (5 cell types × 10 genes). Loaders that build this table from real atlases (CZ CELLxGENE Census, 10x `.mtx`, Linnarsson `.loom`) live in [`notebooks/`](notebooks/).

## What's the output format?

* A **substitution-capacity table** — one `substitution_index` per cell type (higher = more able to run without Nav1.7).
* A **content-addressed asymmetry verdict** — `SUPPORTS_H1` / `AGAINST_H1` / `INCONCLUSIVE`, with `nociceptor_index`, `autonomic_index`, `observed_gap`, and a `sha256` so a run is reproducible and tamper-evident.
* A **D1 decision summary** — the `required_gamma_noci` (the nociceptor adaptation that the "go-slow" lever would need) at a given fitted autonomic leak, with the CI propagated.

**Plain-English glossary** (defined once, here, so the I/O isn't jargon):
* **H1** = the asymmetry hypothesis — that autonomic neurons can run without Nav1.7 better than nociceptors can. `SUPPORTS_H1` means *this dataset's* index gap points that way; it is not a claim that the biology is settled (see the robustness note in `QC_NOTES.md`).
* **`observed_gap`** = autonomic substitution index minus nociceptor substitution index. Bigger = more asymmetry.
* **γ_noci (`required_gamma_noci`)** = how much of the Nav1.7 block a nociceptor would have to "give back" through compensation for a slow drug to still relieve pain. It is a *model output set by chosen efficacy/safety cutoffs*, **not a measured constant** — see the TIER 2 section of `QC_NOTES.md`.
* **CPM** = counts per million (a unit for expression). **HPO** = Human Phenotype Ontology. **LOEUF/pLI** = gnomAD loss-of-function intolerance metrics (low LOEUF / high pLI = intolerant to losing the gene).

## What's a working example?

```bash
pip install -r requirements.txt
PYTHONPATH=. python examples/run_example.py
```

This runs the whole chain on the synthetic table and prints results you can diff against [`examples/expected_output.txt`](examples/expected_output.txt). Expected highlights: synthetic `observed_gap ≈ 2.18` (`SUPPORTS_H1`), and `required_gamma_noci ≈ 1.84`. **The example data is synthetic, literature-shaped, for verification only — it is not a result.**

To run on real data, build the same `cell_type × gene` table from an atlas and call:

```python
from nav17 import substitution_capacity, asymmetry_verdict
cap = substitution_capacity(pb)                      # pb: your cell_type x gene CPM frame
v   = asymmetry_verdict(cap, noci_types, auto_types, {"source": "your atlas"})
```

## How long does it take?

The engine is pure numpy/pandas and runs in milliseconds. The real-data loaders are bounded by download/query time of the atlas you point them at (seconds to a few minutes); several are written to stream only the ~13 panel genes out of multi-GB matrices.

---

## Layout

```
nav17/                 reusable, tested engine (substitution index + homeostat/D1)
examples/              synthetic input + run_example.py + expected_output.txt
tests/                 pytest suite (run: python -m pytest -q)
notebooks/             the full research notebook (all arms, real-data loaders)
QC_NOTES.md            evidence tiering — empirical vs illustrative vs broken
SOURCES.md             full external-citation ledger (PMID/DOI + what each supports)
PREREGISTRATION.md     the falsifiable two-sided-squeeze prediction, date-stamped
```

## Install / test

```bash
pip install -r requirements.txt
python -m pytest -q          # 5 tests, all should pass
```

CI runs the same suite on every push (`.github/workflows/ci.yml`).

## Data sources (all public)

gnomAD v4.1 (constraint) · ClinVar (variant classifications) · Open Targets Platform (target–disease) · HPO / `phenotype.hpoa` (phenotype ontology) · CZ CELLxGENE Census, Linnarsson L5 mouse atlas, WashU/SPARC human PNS atlases (single-cell). External clinical/literature anchors are listed in [`SOURCES.md`](SOURCES.md) and tiered in [`QC_NOTES.md`](QC_NOTES.md).

## Status & caveats

Open-data computational synthesis, not wet-lab work. The genetic-loss/asymmetry framing rests on reproducible public data and the published trial record; the quantitative homeostat is a framework that names an experiment, not a fitted model. The single decisive test — chronic vs acute Nav1.7 block, does the blood-pressure effect wane while analgesia grows — needs a collaborator with the animal model. See `QC_NOTES.md` and `PREREGISTRATION.md`.

## License

MIT — see [LICENSE](LICENSE).
