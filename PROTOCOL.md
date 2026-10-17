# Evaluation protocol — 0.1.0

The frozen bank is a release evaluation instrument, not a claim that NuSR has passed it. Scientific model runs are a separate campaign. Freeze the campaign manifest, adapter revisions and all model settings before seeing test scores. Do not choose task subsets, seeds, software revisions or retries after observing outcomes.

## Questions and model panels

**Horizontal / expression recovery:** compare NuSR, PySR, MySR and Operon on category A. PySR is the established external reference; MySR is the general precursor and tests specialization; Operon adds an independently implemented external SR route. Shared ancestry means MySR alone is insufficient evidence of broad superiority. AI Feynman is optional after an operator/domain preflight, not a mandatory additional package.

**Vertical / observable prediction:** compare NuSR with GPR, LightGBM and one declared MLP ensemble recipe on category B, adding empirical or theoretical references per observable. Other SR tools can also predict these targets; the two panels answer different questions and do not prohibit this overlap.

The primary vertical panel trains every learned model on the same bank training observations. A second, clearly labeled published-model panel may evaluate existing formula coefficients or prediction tables. Historical fitting or unknown training coverage prevents those entries from being described as matched held-out training comparisons. Multi-target, residual-learning and externally assisted models require separate panels.

## Inputs, prior knowledge and NuSR settings

1. Raw mode uses integer `N,Z` plus target and optional training weights. A declared nuclear-knowledge mode may add only deterministic functions of N/Z. `export --features nuclear` provides the same values of `A,I,d,P_s,P_m,Np,Nn,P,Q_EI` for adapter authors; their definitions are public. NuSR's public fit interface remains N/Z. Its adapter must record which internal features implement the declared knowledge; it cannot pretend to accept arbitrary external feature columns. A required macro unavailable in an adapter's language must be identified in the preflight, not silently omitted or injected only for another tool.
2. Primary NuSR runs disable every embedded experimental-data terminal, plus all direct or indirect target-table access. Record **effective configuration**, not just a claim that defaults are safe. Inspect exact release API, feature graph, profile/effects, seeds, loss, exported expression and provenance. `profile='null'` alone is not proof embedded data or AFE is off.
3. For category A, supplying the exact reference initializer/template or coefficient vector is template assistance, not rediscovery. Audit built-in seeds and profile knowledge before running. Report assisted and unassisted results separately. For category B, no same-source measured masses, radii, levels, strengths or their derived labels may appear as inputs at held-out coordinates.
4. Every normalizer, imputer, feature selector, AFE candidate screen, loss-weight calibration and hyperparameter selection is fitted strictly inside training data. The outer validation partition chooses the model/candidate. AFE's own construction/confirmation split is nested inside outer training. No use of `observed_y`, source identifiers, uncertainty, test labels, or other-task observations as predictors in the primary panel.
5. Exported weights are all 1 by default. An uncertainty-weighted extension must preregister a training-only weighting rule and bounds; unknown covariance is not zero uncertainty. Primary test RMSE remains unweighted in physical units.

## Frozen partitions

`splits/*.json` stores **all** assigned IDs and retained/purged counts. The seven families are:

| Split | Initial assignment |
| --- | --- |
| `iid101` | SHA-256 of the fixed prefix and sample ID, modulo 100: 0-59 train, 60-79 validation, 80-99 test |
| `isotope101` | Same bucket rule using Z, holding out entire isotope chains |
| `isotone101` | Same bucket rule using N, holding out entire isotone chains |
| `neutron_edge` | Within each Z chain with at least 8 eligible rows, highest 20% rounded up are test, next same count validation; other rows/chains train |
| `proton_edge` | Corresponding highest-Z holdout within N chains |
| `shell_N` | Distance to N reference closures 8,20,28,50,82,126: distance <=2 test, 3-4 validation, >=5 train |
| `shell_Z` | Same distance rule along Z |

The exact hash prefix and integer conversion are defined in `nuclearbench/splits.py`; no Python process-dependent `hash()` is used. Edge cases are defined by available evaluated rows, not an asserted physical dripline. Chain and shell holdouts are structural generalization tests, not substitutes for an authentic future-measurement experiment.

After initial assignment, all test primitive dependencies are protected. Remove any validation row sharing one; protect the retained validation dependencies as well, then remove conflicting training rows. Every removed ID is recorded as `purged`; do not move it into another partition. This preserves test membership and forbids shared label-building observations between partitions. It is intentionally stricter than merely avoiding duplicate `(N,Z)` pairs.

A split with fewer than three retained rows in any train/validation/test partition is `insufficient_coverage`. It is not scored or silently replaced. Report effective sample sizes after purging; a small training set is part of the declared difficulty and may provide weak statistical power.

Version 2 has 16 explicitly disabled task/split pairs, including the sparse light-radius and higher-spin cases; the complete list and counts are in [SPLIT_COUNTS.md](SPLIT_COUNTS.md). Newly admitted observed targets need >=30 domain rows and >=2 usable structural splits, in addition to the conservative label rules. The original B14 core case remains retained and marked sparse. The nine T tasks instead use the single genuine `ame2016_to_2020` availability split, with old labels retained and primitive IDs shared across editions; see [TEMPORAL_PROTOCOL.md](TEMPORAL_PROTOCOL.md).

## Noise and repeated runs

Model seeds are **7,17,37,73,101**. Each completed run and failed run is retained. Seeds index stochastic training; they do not change the registered data partitions. Report recovery proportions and error distributions across all seeds, not the best seed.

Separate the 38 empirical formula instances, 3 restricted analytic references and 48 synthetic controls in reports. The controls consist of 16 templates; their 12 development instances are excluded from default final aggregation and their 36 public confirmation instances are evaluated after adapter/configuration freeze. Public confirmation roles do not establish blindness. See [CONTROL_DESIGN.md](CONTROL_DESIGN.md).

Category A has clean, 1% and 5% training-label noise settings, measured relative to the clean training-label standard deviation. Noise is a deterministic Box-Muller sample keyed by task/sample ID and a fixed noise101 prefix; validation/test labels stay clean and weight=1. Export with `--noise 0.01` or `--noise 0.05` for training. All methods receive identical perturbed targets. The primary core is the clean condition; noise is the robustness extension. Category B adds no artificial noise.

## Candidate selection and budgets

For each run, retain the full final candidate frontier and select the candidate with the lowest validation RMSE; ties within relative `1e-8` validation RMSE use the registered syntax cost and then the serialized expression lexicographic order. Predictive models use the same validation criterion. No candidate selection on test scores, exact-reference match or a paper's expected expression. Do not refit using the validation labels after selection in the primary campaign, since that would change the dependency embargo.

Before execution, complete `campaign.template.json`: immutable source revisions, package/runtime versions, CPU affinity/thread counts, effective features/operators, selection policy, comparable measured compute budget, hyperparameter-search budget, uncertainty policy, and failure/retry handling. The bank does **not** invent final runtime knobs for unfinished model versions. Null configuration/budget entries are unresolved and prohibit treating a campaign as preregistered. They do not prevent using the frozen bank to implement adapters.

For SR, report CPU seconds, elapsed time, total fitness/case-loss work and evaluation counts. Equal nominal evaluation counts need not mean equal work when case-loss evaluations or preprocessing are excluded by one implementation. Record preparation and AFE time separately and include their cost in the total. For predictors, count all training/hyperparameter fits and ensemble members. State separately whether a comparison is compute-matched or a declared practical configuration comparison. No expensive benchmark runs or Slurm jobs are launched by this repository's validation workflow.

## Scoring and artifacts

- Prediction CSV columns must be exactly `sample_id,prediction`. Every expected test ID must appear once, with a finite numeric prediction; missing, duplicate or additional IDs fail the run. The scorer never drops difficult nuclei to improve an error metric.
- Category B primary metrics are RMSE/MAE in the task unit. Report bias, maximum error, per-isotope-chain counts and RMSE, equal-chain mean RMSE and worst-chain RMSE. Normalized RMSE uses the training target standard deviation. Do not merge MeV, fm and transition-strength errors into one raw average.
- Category A reports symbolic status, finite numerical agreement, RMSE and complexity separately. A proven equality counts as symbolic recovery. Unproved/timeout cases are retained for manual equivalence audit with the numerical witness result; no automatic relabeling by low RMSE. Print failure counts and the number of unproved cases alongside recovery fractions. A manually adjudicated equality needs a published derivation.
- Group related formula cards and related mass-derived observables in interpretation. Do not compute significance by treating every row, expression variant or neighboring nucleus as an independent replicate. Paired differences and resampling at a declared chain/group level are preferable to pointwise uncertainty claims. Seed variability is algorithmic variability, not experimental predictive uncertainty.
- Persist task/split/data/config checksums, model revision, effective settings, seed, exported expression, predictions, complete frontier or model artifact, runtime/resource record, stderr/stdout and terminal status. Preserve failed/timeout/unsupported runs. A timeout cannot enter a prediction table unless the declared protocol permits a previously completed valid candidate, and must still retain its terminal status.

## NuSR longitudinal checks

To assess NuSR's own progression, use fixed revisions and the same data, seeds, splits and compute accounting. Suggested ablations: raw N/Z configuration, permitted fixed nuclear features, explicitly enabled physics effects, AFE, and profile/seed specialization. Audit configuration compatibility for the actual NuSR version; unsupported combinations are not fabricated baselines. Keep the original baseline and all negative results. This is additional evidence alongside the user's vertical prediction-model panel.

The release must distinguish implementation/integrity checks from measured scientific outcomes. As public datasets have already informed development, the present bank is retrospective. An untouched future-data panel requires its own source versions, historical availability rules and sealed evaluation; it is not implied by a fresh random split of AME2020.

## Equal-group result summaries

Use `nuclearbench summary --root .` to inspect instance counts and declared structure groups. For model results, retain each scored JSON, append the actual `model`, `seed` and `noise` fields, and store a JSON list. Failure records need the same frozen `bank_checksums_sha256`, task, split and model/seed/noise condition plus a terminal `failed`, `timeout` or `unsupported` status. A scored SR recovery record must include both the proof status and numerical-agreement result from `recover`.

```bash
nuclearbench aggregate --root . --results runs.json \
  --panel published_empirical --split iid101 --models NuSR PySR MySR Operon
```

For the requested panel/split and noise condition, the aggregator expects every eligible nondevelopment task at all five registered seeds for each named model. It rejects duplicate task/seed entries and mismatched bank fingerprints, and lists missing runs. It averages seeds within tasks, tasks within a declared group and groups within the panel. Thus 22 spectroscopy instances do not have 22 times the weight of a one-instance radius group. Group definitions are a declared reporting convention, not a proof of physical or statistical independence.

An incomplete group has no final aggregate. A terminal failure remains in the recovery denominator; normalized predictive error is left unavailable if any expected run has no valid prediction. Unproved equality remains an explicit unresolved proof status; the automatic symbolic rate counts only proved equal cases and is not a manually adjudicated recovery rate. Physical-unit RMSE/MAE remain task-specific; no aggregate averages raw MeV, fm and transition-strength errors. A normalized-error mean is a distribution-specific summary, not a universal quality measure. Conditions, panels and structural splits are not silently pooled.
