# Scientific coverage expansion: v1.0.0 to v0.1.0

The original version was a reproducible **25-card core**, not an exhaustive nuclear-structure benchmark or a scientifically justified final manuscript examination. Only 10 cards had exact formula-generated recovery labels; seven were radius formulas. Nine of the 15 observation cards came from the same mass evaluation and its differences. More seeds, splits or data rows could not repair that limited structural coverage.

This release adds source-backed spectroscopy, different radius structures, restricted analytic mass-model references, explicitly designed mechanism controls, broader real spectroscopy, and genuine old-to-new evaluation labels. No scientific model campaign was run while selecting the expansion.

## What the 120 instances mean

| Panel | 0.1.0 instances | Independent interpretation |
| --- | ---: | --- |
| Published empirical recovery | 38 | Eight declared related groups; 22 are parameter/spin variants of valence-spectroscopy expressions |
| Restricted analytic recovery | 3 | Related spherical macroscopic pieces; not the complete LDM/NLD/LSD models |
| Designed mechanism recovery | 48 | 16 templates with three deterministic coefficient instances each |
| Evaluated-observable prediction | 22 | Original core plus seven conservatively usable spectroscopy/shape targets |
| Evaluation-vintage prediction | 9 | Correlated mass observables using old training labels and newly evaluable test entries |

There are **89 recovery instances and 31 prediction instances**, 194,077 task rows and 770 enabled task/split pairs. These are not 120 independent nuclear laws. The grouping is exposed in `bank.json`, `nuclearbench summary` and [COVERAGE.md](COVERAGE.md), and implemented in the result aggregator. No task-count multiplication by seeds, noise settings or folds is used as evidence of novelty.

## Substantive additions

**Published expressions.** Ha/Cha's first 2+/3- formula and the 20 printed yrast parameter sets add inverse powers and valence-dependent exponentials to a mass/radius-heavy core. Spin is fixed per task; no extra J input is invented. Duflo-Zuker radius forms add exponential finite-size/isovector behavior and EI-shell occupancy factors. Angeli's rms interpolation adds inverse-power structure. The spherical macroscopic pieces test surface/curvature/asymmetry combinations while explicitly excluding unavailable corrections. Sources, equations, coefficient sets and rejected candidates are recorded in [FORMULAS.md](FORMULAS.md), [literature.json](literature.json) and [COVERAGE.md](COVERAGE.md).

**Controlled search questions.** The 16 synthetic templates isolate isospin, parity, shell localization, valence coupling/saturation and global/local combinations. Twelve instances are for development; 36 are public confirmation, including four composition templates excluded from development tuning. Generated coefficients use declared hashes/ranges, not fits to real observations or algorithm outcomes. These tasks are labeled artificial throughout and never presented as extra experimental discoveries.

**Real observations.** New usable targets are first 6+, 8+, 10+, 1-, 5-, 3+ and excited 0+ energies. The last probes low-lying shape/coexistence-related structure without asserting a unique shape interpretation. The parser retains conservative definite-state rules. Other requested spin states with inadequate safe coverage are listed as rejected, rather than promoted into empty or unusable benchmark tasks.

**Historical labels.** The T panel trains and validates on original AME2016 values and tests nonestimated targets newly available in AME2020 under the same complete-parent rule. The binding task has 71 test nuclei. A later revised value is not used to clean old training labels. Primitive masses remain the same dependency across edition prefixes; embargoes prevent shared mass parents across partitions. This is retrospective evaluation-vintage extrapolation, not certified future measurement chronology or a private blind test.

**Radius truth audit.** The 0.1.0 primary absolute-radius task excludes 72 rows from elements identified in the source discussion as using model-based absolute anchors, retaining 812. This narrows an earlier overbroad experimental interpretation. It does not erase correlations/calibrations in the remaining evaluated data. The original v1 tag remains unchanged for historical reproducibility.

## What was deliberately not added

- An 11+ yrast recovery task: the reviewed parameter table has no corresponding row despite its caption.
- Sparse definite-state prediction targets below the predeclared new-target coverage gate, or tentative levels relabeled as definite merely to increase counts.
- Full Duflo-Zuker mass discovery through an opaque external callable, full macroscopic-microscopic mass models with missing deformation/shell data, or formulas requiring measured binding/pairing inputs inserted into N/Z-only comparisons.
- Variable-spin rotor formulas, reaction tasks, or decay formulas with Q-values as if their extra variables were N/Z-only input.
- Hundreds of coefficient/noise/fold variants advertised as independent physics problems.

The admission ledger is a selected audit, not proof that the literature is exhausted. New source families should be added when their definitions, information requirements and numerical reference can be verified.

## Release meaning and remaining science

The bank is materially broader and can support a more informative NuSR manuscript campaign. It does **not** guarantee journal acceptance, establish NuSR superiority or replace measured comparisons. All exact answers, controls and public data are inspectable. Freeze model releases, adapters, prior knowledge, template assistance, tuning and measured compute accounting before the actual campaign. Compare NuSR/PySR/MySR/Operon on recovery and NuSR/GPR/LightGBM/MLP on observations, with appropriate separately labeled physical references.

Report errors, recovery and complexity by panel, declared group and structural split; retain every failure and unsupported case. An actual external blind evaluation and additional observable families remain future work, not completed release claims. `v1.0.0` is immutable; use `v0.1.0` with its own code, metadata and artifact inventory.
