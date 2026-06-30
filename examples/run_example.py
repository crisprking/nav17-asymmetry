#!/usr/bin/env python3
"""
Worked example — runs the full chain on a small, literature-shaped SYNTHETIC
pseudobulk (NOT real data). It exists so you can verify the tool works before
pointing it at a real single-cell atlas.

    INPUT : examples/example_pseudobulk.csv   (cell_type x gene, relative units)
    OUTPUT: per-cell-type substitution index + a falsifiable asymmetry verdict
            (printed; compare against examples/expected_output.txt)

To run on REAL data, build the same [cell_type x gene] CPM table from a
single-cell atlas (see notebooks/ for Census / 10x / loom loaders) and call
substitution_capacity() + asymmetry_verdict() exactly as below.
"""
import os
import pandas as pd
from nav17 import substitution_capacity, asymmetry_verdict, gn_crit, d1_decision

HERE = os.path.dirname(__file__)

# 1) load the [cell_type x gene] pseudobulk
pb = pd.read_csv(os.path.join(HERE, "example_pseudobulk.csv"), index_col=0)

# 2) per-cell-type substitution capacity
cap = substitution_capacity(pb)
print("=== substitution capacity (synthetic, validation only) ===")
print(cap.round(2).to_string(), "\n")

# 3) falsifiable asymmetry verdict (the H1 the 'go-slow' lever needs)
NOCI = [t for t in pb.index if t.startswith("DRG")]
AUTO = [t for t in pb.index if t.startswith("Sympathetic")]
v = asymmetry_verdict(cap, NOCI, AUTO,
                      dict(source="example_pseudobulk.csv", unit="relative"))
print("=== asymmetry verdict ===")
for k in ("nociceptor_index", "autonomic_index", "observed_gap", "call", "sha256"):
    print(f"  {k:18}: {v[k]}")

# 4) the two-sided homeostat side: what gamma_noci would the 'go-slow' lever need,
#    given a (literature-shaped) fitted autonomic leak? (illustrative thresholds)
print("\n=== D1 decision at an example fitted autonomic leak gamma_auto=0.35 ===")
dec = d1_decision(gamma_auto=0.35, gamma_auto_ci=(0.26, 0.40))
for k, val in dec.items():
    print(f"  {k}: {val}")
