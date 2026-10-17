# NuSR Nuclear Structure Benchmark

An independent, frozen question bank for symbolic expression recovery and prediction of nuclear structure observables. It contains **10 published expression-recovery tasks and 15 evaluated-observable prediction tasks**, with 32,815 task rows. Repeated nuclides and related observables are not independent experiments.

The bank is designed for NuSR release evaluation, but its data and scoring tools do not import NuSR, MySR, PySR, Julia, or a trained model. A fresh clone works offline after installing the small Python dependencies. No model-comparison campaign has been run for this release.

## Two categories

| Category | Labels | Question | Principal measures |
| --- | --- | --- | --- |
| A: expression recovery | Values generated from a fixed, published empirical formula at evaluated nuclear coordinates | Can an SR method recover that specified expression? | Symbolic equality status, separate numerical agreement, recovery frequency, expression complexity, error and runtime |
| B: observable prediction | Evaluated experimental nuclear observables | How well does a model generalize to withheld nuclides or nuclear regions? | RMSE and MAE in physical units, chain-level errors, generalization across split families |

Category A retains experimental `observed_y` and `observed_sigma` for context; its training label is **`y`, the formula-generated value**. A published empirical expression is a designated model, not the unique exact law behind the observations. Category B makes no exact-expression claim. An observable can belong to both categories with different labels and scientific questions.

The scope is **nuclear structure**: mass and separation energies, pairing and shell indicators, charge radii, excitation energies, energy ratios and transition strengths. This release does not establish coverage of nuclear reactions, decay lifetimes, magnetic moments or all nuclear physics.

## Quick start

```bash
git clone https://github.com/TAO-MINGYU/NuSR-Benchmark.git
cd NuSR-Benchmark
python -m pip install '.[symbolic]'
nuclearbench validate --root .
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

For an executable prediction-file example, see [examples/train_linear.py](examples/train_linear.py). It uses only NumPy and training-partition observations.

## Evaluation design

- Seven registered split families: deterministic point holdout, entire isotope chains, entire isotone chains, neutron edge, proton edge, neutron-shell bands, and proton-shell bands.
- Shared primitive label dependencies are purged across train/validation/test, including adjacent AME masses used in separation energies, pairing indicators and shell gaps. Purged IDs remain recorded. Two edge splits for the sparse first `3-` level task have insufficient coverage and are explicitly disabled.
- Sources, units, formula conventions, row IDs, partitions and SHA-256 checksums are frozen. Estimated masses, preliminary radii, ambiguous first-level assignments and censored transition strengths are excluded from primary point regression.
- Primary fits receive only `N,Z`, or the same declared deterministic nuclear feature set for every competing model. Embedded experimental lookup, target-derived features and held-out targets are forbidden. NuSR ablations and template-assisted recovery are reported explicitly.
- Fixed model seeds: `7,17,37,73,101`. Clean, 1% and 5% training-label noise variants are available for category A. Actual model versions, settings, knowledge access and compute allocations must be frozen before campaign launch; see [PROTOCOL.md](PROTOCOL.md).

Recommended horizontal methods: **NuSR, PySR, MySR and Operon**. Recommended vertical methods: **GPR, LightGBM and an MLP ensemble**, with empirical/physical references appropriate to each observable. Published formulas or per-nuclide prediction tables can save computation; unrelated paper-level RMSE values cannot form a matched ranking. See [MODEL_CANDIDATES.md](MODEL_CANDIDATES.md).

## Contents and reproducibility

- [TASKS.md](TASKS.md): every task, row count, source, formula and supported partitions.
- [FORMULAS.md](FORMULAS.md): exact numerical conventions, effective magic numbers and radius conversion.
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

`fetch` first verifies and copies the five small original files in `source_snapshots/`; only the 42 MB ENSDF archival zip needs downloading. These original bytes and their attribution are preserved, avoiding dependence on mutable pages and browser-download restrictions. An alternative snapshot location can be supplied with `--snapshots`. All input bytes are checked: `fetch` **fails on a hash mismatch** rather than silently changing the release. If upstream changes, obtain the locked ENSDF snapshot or use the checked-in normalized bank; creating a newer source snapshot requires a new bank version. Last-bit math differences across platforms are tolerated by formula validation; byte-identical rebuild claims apply to the recorded Python/NumPy environment in the development log.

The source datasets have been used in NuSR development. This release supports reproducible retrospective validation; an independent future-data or genuinely untouched release set is needed for a blind performance claim. Passing the integrity checks does not establish NuSR superiority.

Software and original documentation use the MIT license. Third-party data and published formulas retain their original rights and attribution requirements; see [LICENSE](LICENSE) and [DATA_SOURCES.md](DATA_SOURCES.md).
