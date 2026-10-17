# Evaluation-vintage holdout: AME2016 to AME2020

The nine T tasks evaluate binding, Sn/S2n/Sp/S2p, neutron/proton three-point OES and neutron/proton two-nucleon gaps using **actual different label vintages**. They are correlated views of the mass surface, not nine independent new datasets.

## Membership and label values

1. Parse the official AME2016 mass/reaction files using their own fixed widths and precision; reject estimated `#` values and labels with estimated/missing mass parents. AME2016 was published in 2017; AME2020 was published in 2021. Names refer to evaluation editions.
2. For a target available nonestimated in AME2016, retain its **AME2016 value and uncertainty**. Do not replace a training or validation label with a later revised number. Preserve old rows even if a later evaluation downgraded or omitted them: using that later decision to curate old training data would itself use future information.
3. A nonestimated AME2020 target unavailable under the same older-edition rules enters test. For a derived target, this means newly evaluable under the complete-parent rule, not necessarily a previously unknown target nucleus. Primary coordinates have `N>=8,Z>=8`.
4. Old rows use the registered `bucket(sample_id)` rule: the validation bucket remains validation; both other buckets become training, giving approximately 80/20 before embargo. Newly available rows remain test. T tasks expose **only** `ame2016_to_2020`; a random split of the merged editions is not a substitute.

T01 binding has **71 test nuclei**. The union contains 2,479 labels: 1,926 training, 482 validation and 71 test. It includes old labels that are no longer nonestimated in the newer edition, which explains why its total is not the current AME2020-only count. Other T tasks have their own counts in [SPLIT_COUNTS.md](SPLIT_COUNTS.md).

This is an **evaluation-availability proxy** for temporal generalization. It does not certify the first experimental measurement date of every record. The bank has not audited individual experiment dates or all historical calibration dependencies. Both editions were public during NuSR development; call this retrospective evaluation-vintage extrapolation, not blind future prediction.

## Cross-edition primitive embargo

Mass-parent IDs are `nuclide_mass:N:Z`, independent of edition. `AME2016:ME:N:Z` and `AME2020:ME:N:Z` do not become independent observations by changing a prefix. Protect every test parent, remove conflicting validation rows, then protect retained validation parents and remove conflicting training rows. Save purged IDs and counts. Common neutron/hydrogen mass constants are fixed per source edition and are not per-nuclide experimental input terminals.

The verifier reconstructs both editions from the bundled source files and checks the exact T rows, label values, source vintages and membership, in addition to verifying all embargo masks. Three-point/gap covariances remain unknown; published reaction-file uncertainties are retained. Source rounding tolerances are explicit in the parser (3 eV for AME2020 and 30 eV for the older reaction-file precision).

## Running the panel

```bash
nuclearbench export --root . --task T01_B --split ame2016_to_2020 --partition train > train.csv
nuclearbench export --root . --task T01_B --split ame2016_to_2020 --partition validation > validation.csv
nuclearbench export --root . --task T01_B --split ame2016_to_2020 --partition test > test_inputs.csv
nuclearbench score --root . --task T01_B --split ame2016_to_2020 --predictions predictions.csv
```

All learned models train on the old retained observations and select on the old validation set. Primary N/Z-only fits disable embedded measured lookup from **both** editions. Published model/table references need a verified original fit/calibration date and coverage; a later refit on AME2020 is not an independent earlier forecast. Recompute errors on exactly these test IDs rather than importing a paper's aggregate RMSE.
