# External baseline campaign

This runner evaluates the frozen 151-task v0.2.0 bank. It does not change data,
reference coefficients, splits or source snapshots. Its code commit and source
inventory are recorded separately from the bank version. Model results are not
part of the data release or the engineering acceptance checks below.

## Models and scope

| Method | Expression recovery | Observable prediction | Registered implementation |
| --- | --- | --- | --- |
| PySR | Yes | Yes | PySR 2.7.0, SymbolicRegression.jl 2.7.1, Julia 1.10.3 |
| Operon | Yes | Yes | pyoperon 0.6.2, upstream double-precision build |
| AI Feynman | Yes | Yes | aifeynman 2.0.7, PyTorch 2.2.2 CPU, NumPy 1.23.5 |
| Gaussian process regression | No | Yes | scikit-learn 1.9.1 |
| LightGBM | No | Yes | LightGBM 4.7.0 |
| MLP ensemble | No | Yes | scikit-learn 1.9.1 |
| Linear/ridge regression | No | Yes | scikit-learn 1.9.1 |

MySR and NuSR are intentionally absent while their implementations remain under
development. Their later runs must identify the final revisions and configuration.
Published physical-model prediction tables require a separate matched-coverage
study; paper-level RMSE values are not substitutes for these test predictions.

All 945 enabled task/split pairs run with seeds 7, 17, 37, 73 and 101 in raw and
nuclear feature modes. Expression recovery includes clean, 1% and 5% training
noise. Observable prediction uses clean evaluated labels. This produces 79,630
requests: 22,930 per SR method and 2,710 per predictive method. All twelve
development controls run, but their 7,560 requests are excluded from confirmation
aggregates. Unsupported splits remain disabled. Public confirmation is retrospective.

## Native configurations

The authoritative machine-readable recipes are
[external_profiles.py](nuclearbench/external_profiles.py). Each fit uses one CPU
thread, including BLAS, Julia and PyTorch. The supervisor runs up to 256 independent
fits in one node2 Slurm allocation, subject to observed memory availability.
It imposes no external per-fit timeout or RSS kill cap.

- PySR: five million native evaluations, eight populations of 100, size 128,
  depth 32, constant optimization 25 iterations with two restarts, float64,
  deterministic serial execution. The iteration guard is one million.
- Operon: five million native evaluations, population and pool size 1,000,
  MSE/length Pareto objectives, Levenberg–Marquardt constant optimization with
  25 iterations, size 128 and depth 32, epsilon 0, float64. Its generation guard
  is one million. Expressions are exported with 17 significant digits.
- AI Feynman: native BF_try_time 60 seconds, 14ops grammar, polynomial degree 4,
  NN_epochs 4,000 and native internal test percentage 0. BF_try_time applies to
  each native call. Upstream also uses 600-second compositionality calls, four
  learning-rate stages and a threefold small-data epoch multiplier. Thus 60 seconds
  is not a global fit deadline. Every actual NN invocation is recorded.
- GPR: six RBF/Matérn kernel recipes, with and without a linear component,
  white-noise terms, explicit bounds and three optimizer restarts.
- LightGBM: twelve leaf/minimum-child recipes, 4,000-tree guard, learning rate
  0.03, L2 regularization 1 and validation early stopping after 100 rounds.
- MLP ensemble: six architecture/regularization recipes, five members per recipe,
  tanh/Adam, learning rate 0.001, maximum 2,000 epochs. The actual external
  validation partition controls early stopping; no random internal split is used.
- Ridge: linear regression and six positive penalties from 1e-6 through 100.

The SR grammars cover arithmetic, powers and the declared elementary functions;
they differ in native complexity and search mechanisms. Native evaluation counters
do not imply equal computational work across methods. Report actual process CPU,
wall time, native counts where available, precision and full effective options.
These are practical native configurations, not a claim of compute-matched search.

## Data access and selection

Every fitting payload has exactly features, x_train, y_train, x_validation,
y_validation, x_test and test_ids. No test labels, source lookup, observed_y or
reference expressions enter a solver call. The worker seals selected.json before
test prediction. Selection uses validation RMSE, then declared complexity and a
deterministic tie break. There is no validation refit, test reselection or best-retry
selection. Test-domain failures remain terminal failures.

Training-only transforms are replayed on validation/test. SR target scaling preserves
zero and sign; predictive models additionally center the target. PySR/Operon retain
raw feature scales. Other methods standardize using training statistics. All inverse
transforms are retained. Recovery expressions are exported back to physical variables.

Nuclear payloads contain N, Z, A, I, d, P_s, P_m, Np, Nn, P and Q_EI. AI Feynman
uses the predeclared invertible continuous coordinates A,I, followed by training-only
rank filtering; raw mode uses N,Z and the same rank filtering. Derived columns lie on
the two-dimensional N/Z manifold, so treating all eleven as independently sampled
variables does not identify off-manifold derivatives. This method-specific coordinate
choice is disclosed: the payload interface is shared, but active variables and
grammars are not identical. Its output is transformed back before common scoring.

## Compatibility and provenance

The original Operon wheel used float32. Its artifact and failed strict-export probe
are preserved. The accepted native upstream v0.6.2 source revision is
adf7e0e34041238e22e7ff7cd4330451de97bb36 with Operon core
fad10f087c592812b1a9ecfabce669f37bf459f7, Eigen 3.4, Taskflow 3.9 and GCC 14.4.
Only the official USE_SINGLE_PRECISION=OFF build option changes precision; algorithm
sources are unchanged. [build_operon_fp64.py](scripts/build_operon_fp64.py) records
the official dependency revisions and actual build commands. The accepted wheel SHA
is 8d7d6fb03563a2b5669b3841ced1138d1677369657c939e32bfb189c05a75e48.

AI Feynman's polynomial code constructs a ragged NumPy array; NumPy 1.23.5 retains
the behavior required by this upstream release. The adapter also converts exactly
integral NN epoch floats to integers where upstream pretrained recursion passes
NN_epochs/2 into range(). It rejects fractional values and preserves epoch counts.
The root native Pareto set is observed for export; reduced recursive targets are not
mistaken for the original target. Compatibility probes and earlier failures are
retained independently of formal scientific runs.

Source/runtime inventories, interpreters, Julia project/manifest/preferences,
package bundle, complete matrix and answer-free payloads are fingerprinted. Python
package layers are staged once to node-local storage, then imported in isolated
workers. Node-local probes reject incorrect precision, runtime versions or allocation.
Provisioning/staging costs are recorded separately from per-fit full process costs.

## Execution and evidence

Use [external_prepare.py](nuclearbench/external_prepare.py) to prepare the complete
matrix, then [freeze_external.py](scripts/freeze_external.py) to bundle runtimes
and freeze a clean committed checkout. The freezer can reuse verified payloads
while rebuilding request identities from the final recipes. Machine-specific runtime
paths live outside this repository. Submit the frozen
[external_node2.sbatch](scripts/external_node2.sbatch) once with absolute interpreter,
source and campaign-config arguments. It requests node2, 256 logical CPUs, mem=0,
unlimited partition wall time and no automatic requeue.

Each terminal result retains the request, selection, candidate history, predictions,
warnings, native artifacts, errors, resource records and hashes. Successful prediction
does not itself imply expression recovery. Symbolic proof status and numerical
agreement are separate. A candidate undefined on extra equivalence witnesses can
retain its valid held-out predictive score without receiving numerical-agreement
credit. Equal-group aggregates retain failures and distinguish development panels;
missing results prevent a final summary. A terminal campaign is not automatically a
successful scientific comparison.

Official method references: [PySR](https://ai.damtp.cam.ac.uk/pysr/),
[Operon](https://github.com/heal-research/pyoperon),
[AI Feynman](https://github.com/SJ001/AI-Feynman),
[scikit-learn](https://scikit-learn.org/stable/),
[LightGBM](https://lightgbm.readthedocs.io/).
