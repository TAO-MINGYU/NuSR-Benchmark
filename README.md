# NuSR Nuclear Structure Benchmark

An independent question bank for symbolic expression recovery and prediction of nuclear structure observables. **Version 0.2.0 contains 151 task instances**, with 206,228 task rows and 945 enabled task/split pairs. These are **not 151 independent physical laws**. The preceding 120-task release is [v0.1.0](https://github.com/TAO-MINGYU/NuSR-Benchmark/tree/v0.1.0); all its CSV and split bytes are retained.

| Evaluation question | Panel | Instances | Interpretation |
| --- | --- | ---: | --- |
| Expression recovery | Published empirical formulas | 46 | Thirteen declared related groups; 22 spectroscopy instances share one group |
| Expression recovery | Published analytic references | 4 | Three spherical macroscopic pieces and one unenhanced TRK reference |
| Expression recovery | Designed mechanism controls | 48 | 16 templates, three coefficient instances each; 12 development and 36 public confirmation instances |
| Observable prediction | Evaluated observations | 25 | Mass, radii, transition strength, spectroscopy, moments and a collectivity product |
| Observable prediction | Evaluated resonance parameters | 3 | s-wave spacing, radiative width and neutron strength; fixed BNL2018 columns |
| Observable prediction | Structure parameters | 11 | Seven experimental-data-fitted GDR response targets and four model-dependent barrier targets |
| Observable prediction | Nuclear decay extension | 5 | N/Z-only prediction of ground-state partial lifetimes; separately labeled extension |
| Observable prediction | Historical evaluation holdout | 9 | Train/validate using AME2016 labels, test newly nonestimated AME2020 entries |

See [VERSION_HISTORY.md](VERSION_HISTORY.md) for the requested numbering correction.

Read [EXPANSION_020_REPORT.md](EXPANSION_020_REPORT.md) for this expansion, [TARGET_CATALOG_AUDIT.md](TARGET_CATALOG_AUDIT.md) for all 76 supplied formula-family decisions, and [EXPANSION_REPORT.md](EXPANSION_REPORT.md) for the earlier 120-task expansion and [COVERAGE.md](COVERAGE.md) for related families, sparse cases and excluded candidates. Engineering integrity and a version tag do not establish publication sufficiency or NuSR superiority.

The bank is designed for NuSR release evaluation, but its data and scoring tools do not import NuSR, MySR, PySR, Julia, or a trained model. A fresh clone works offline after installing the small Python dependencies. No model-comparison campaign has been run for this release.

## Two categories

| Category | Labels | Question | Principal measures |
| --- | --- | --- | --- |
| A: expression recovery | Values generated from a fixed, declared reference expression | Can an SR method recover that specified expression? | Symbolic equality status, separate numerical agreement, recovery frequency, expression complexity, error and runtime |
| B: observable prediction | Evaluated observables, explicitly labeled parameters and optional decay labels | How well does a model generalize to withheld nuclides or nuclear regions? | RMSE and MAE in physical units, chain-level errors, generalization across split families |

Category A retains experimental `observed_y` and `observed_sigma` **where available**; its training label is **`y`, the formula-generated value**. Spectroscopy recovery uses common measured-mass nuclide coordinates, with missing level observations left empty. Restricted analytic components and synthetic controls assert no experimental target. A published empirical expression is a designated model, not the unique exact law behind observations. Category B makes no exact-expression claim. The two categories distinguish evaluation questions, not whether someone has ever proposed a formula for an observable.

The primary scope is **nuclear structure**, including mass indicators, charge radii, excitations, transition strength, electromagnetic moments and collective/resonance structure. Decay lifetimes form an explicitly separate extension. Reaction cross sections, spectra, optical potentials and matter-density functions requiring additional independent variables remain outside NuSR's N/Z interface. This is not coverage of all nuclear physics.

## Quick start

```bash
git clone https://github.com/TAO-MINGYU/NuSR-Benchmark.git
cd NuSR-Benchmark
python -m pip install '.[symbolic]'
nuclearbench validate --root .
nuclearbench summary --root .
nuclearbench list --root .
nuclearbench export --root . --task A01_BW --split isotope101 --partition train > train.csv
nuclearbench export --root . --task A01_BW --split isotope101 --partition validation > validation.csv
nuclearbench export --root . --task A01_BW --split isotope101 --partition test > test_inputs.csv
```

Train the selected software using the training data, select its final candidate using validation data, and create a CSV with exactly `sample_id,prediction`. Test exports omit targets by default. All reference labels are public in this repository; this is an auditable retrospective benchmark, not a private examination.

```bash
nuclearbench score --root . --task A01_BW --split isotope101 --predictions predictions.csv
nuclearbench recover --root . --task A04_R_A --split iid101 \
  --expression 'sqrt(3/5)*1.2269*(N+Z)**(1/3)'
python -m unittest discover -s tests -v
```

`recover` distinguishes a symbolic proof from finite numerical agreement. A timeout or inability to prove equality is reported as **unproved**, not automatically incorrect. Small prediction error does not imply expression recovery. The example above is an integrity check using the known answer, never a benchmark performance result.

For an executable prediction-file example, see [examples/train_linear.py](examples/train_linear.py). It uses only NumPy and training-partition observations. Historical evaluation is available with `--task T01_B --split ame2016_to_2020`. The 71 test nuclei for that binding task have no usable nonestimated label in the older evaluation.

## Evaluation design

- Seven structural split families, plus the dedicated `ame2016_to_2020` evaluation-vintage split. Temporal tasks do not receive a replacement random split.
- Shared primitive label dependencies are purged across train/validation/test, including mass parents across evaluation versions. Old labels are never silently replaced by revised AME2020 values. All purge lists and 58 disabled task/split pairs remain explicit.
- Sources, units, formula conventions, row IDs, partitions and SHA-256 checksums are frozen. Estimated masses, preliminary radii, ambiguous first-level assignments and censored transition strengths are excluded from primary point regression.
- Primary fits receive only `N,Z`, or the same declared deterministic nuclear feature set for every competing model. Embedded experimental lookup, target-derived features and held-out targets are forbidden. NuSR ablations and template-assisted recovery are reported explicitly.
- Fixed model seeds: `7,17,37,73,101`. Clean, 1% and 5% training-label noise variants are available for category A. Actual model versions, settings, knowledge access and compute allocations must be frozen before campaign launch; see [PROTOCOL.md](PROTOCOL.md).
- `aggregate` averages seeds within tasks, task instances within declared groups and groups within a panel. It reports missing/failed runs and never averages raw mixed-unit RMSE. Designed controls and restricted references have their own panels.

Recommended horizontal methods: **NuSR, PySR, MySR and Operon**. Recommended vertical methods: **GPR, LightGBM and an MLP ensemble**, with empirical/physical references appropriate to each observable. Published formulas or per-nuclide prediction tables can save computation; unrelated paper-level RMSE values cannot form a matched ranking. See [MODEL_CANDIDATES.md](MODEL_CANDIDATES.md).

## Contents and reproducibility

- [TARGET_CATALOG_AUDIT.md](TARGET_CATALOG_AUDIT.md): 76 supplied families, eligibility decisions and reasons.
- [EXTERNAL_DATA.md](EXTERNAL_DATA.md): moments, RIPL4 parameters and partial-lifetime conventions.
- [TASKS.md](TASKS.md): every task, row count, source, formula and supported partitions.
- [FORMULAS.md](FORMULAS.md): exact numerical conventions, effective magic numbers and radius conversion.
- [CONTROL_DESIGN.md](CONTROL_DESIGN.md): designed templates, coefficient generation and public confirmation roles.
- [TEMPORAL_PROTOCOL.md](TEMPORAL_PROTOCOL.md): actual vintage labels, new-entry definition and cross-version embargo.
- [DATA_SOURCES.md](DATA_SOURCES.md): upstream versions, citations, filtering and data-use notices.
- [PROTOCOL.md](PROTOCOL.md): comparisons, leakage controls, budgets, candidate selection and reporting.
- [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md): integrity gates and limits of the release claims.
- `bank.json`, `checksums.json`, `data/`, `splits/`: machine-readable frozen bank.
- `nuclearbench/`: independent source readers, generators, partitioner, exporter and scorers.

To reconstruct the frozen data rather than use the checked-in CSVs:

```bash
nuclearbench fetch --raw .cache/raw
nuclearbench build --raw .cache/raw --output /tmp/nuclearbench-rebuilt
diff checksums.json /tmp/nuclearbench-rebuilt/checksums.json
```

`fetch` first verifies and copies seventeen original files in `source_snapshots/`; only the 42 MB ENSDF archival zip needs downloading. These original bytes and their attribution are preserved, avoiding dependence on mutable pages and browser-download restrictions. An alternative snapshot location can be supplied with `--snapshots`. All input bytes are checked: `fetch` **fails on a hash mismatch** rather than silently changing the release. If upstream changes, obtain the locked ENSDF snapshot or use the checked-in normalized bank; creating a newer source snapshot requires a new bank version. Last-bit math differences across platforms are tolerated by formula validation; byte-identical rebuild claims apply to the recorded Python/NumPy environment in the development log. Use each version's own code and artifacts together; this verifier deliberately rejects a v1 bank.

The source datasets have been used in NuSR development. This release supports reproducible retrospective validation; an independent future-data or genuinely untouched release set is needed for a blind performance claim. Passing the integrity checks does not establish NuSR superiority.

Software and original documentation use the MIT license. Third-party data and published formulas retain their original rights and attribution requirements; see [LICENSE](LICENSE) and [DATA_SOURCES.md](DATA_SOURCES.md).
