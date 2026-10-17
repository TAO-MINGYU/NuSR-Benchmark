# Release integrity and scientific acceptance

## Bank v0.2.0 integrity gates

- Every task has actual CSV labels, stable unique IDs, physical units, source record locators, source hashes, filtering/domain definitions and frozen partitions.
- Formula-generated labels match the declared reference expressions; observations and uncertainties stay distinct. Every published radius formula uses the declared radius convention.
- Estimated/qualified/censored/preliminary values do not silently enter primary point regression. Unavailable derived covariance produces unknown uncertainty, not an invented sigma.
- Every enabled split has at least three retained train, validation and test rows. Every row is assigned once to a retained partition or purge list; retained primitive label dependencies are disjoint. Sparse unsupported splits remain explicit.
- The checked-in artifact checksum inventory matches; a same-environment source rebuild is byte-identical. Missing or changed upstream raw files fail hash checks.
- The scorer verifies exact ID coverage, uniqueness and finite values. Reordered predictions score identically. Missing/extra/duplicate/nonfinite predictions fail.
- Recovery checks distinguish symbolic equality from finite numerical agreement and good approximate fit. The expression interpreter rejects arbitrary executable syntax.
- All 98 recovery entries and their panel/group/role metadata match the source-audited or synthetic-generator registry. The literature ledger matches the reviewed decisions; generated documentation matches the actual task inventory.
- Temporal labels and membership reconstruct from both bundled editions, old values remain old, and shared primitive parents cannot escape embargo by changing edition prefixes.
- Artificial controls, restricted macroscopic pieces and missing spectroscopy context are not represented as experimental observations. Model-anchored absolute-radius rows are excluded from the primary prediction target.
- New observational labels reconstruct from bundled IAEA/AMDC/RIPL4 bytes, including state identity, sign, units, In flags and branch definitions; recomputing a hash cannot legitimize a fabricated label. All76 supplied catalogue families have explicit decisions and metadata-source hashes.
- Equal-group aggregation prevents parameter/state multiplicity from dominating a report. Missing/failed/duplicate runs and mismatched bank fingerprints are detected; raw mixed-unit RMSE is not averaged.
- Clean installation, standalone CLI export/scoring, source rebuild, focused tests, lint and Git whitespace checks pass. No source package modifications or trained NuSR artifact is required.

Validation evidence and environment versions are recorded in `DEVELOPMENT_LOG.md`. GitHub Actions independently runs the bank tests and validation on Python 3.10, 3.11 and 3.12 when triggered; a configured workflow is not itself evidence those remote checks have passed.

## What a future NuSR release report must show

Run the complete preregistered campaign at frozen revisions. Report all category A recovery outcomes, category B errors, effective data coverage, unsupported cases, failures, stochastic variability, complexity and measured compute cost. Include NuSR internal ablations if claiming benefit from nuclear specialization. Evidence of improvement must identify the supported task/split families rather than assert universal nuclear-physics superiority.

There is no universal RMSE cutoff across MeV, fm and e^2 fm^4, and no requirement that an interpretable symbolic model beat every neural/theoretical model on every task. A release may document an accuracy/simplicity tradeoff, strong extrapolation performance or superior recoverability. Those claims require measured results and predefined comparisons, not integrity tests. Keep both positive and negative findings.

The bank is retrospective because these source datasets were already available during NuSR development. Reusing a frozen public split prevents moving the evaluation target, but does not restore blindness. An independent future-data or externally held evaluation is an additional study. This repository does not claim that such a study or the model campaign has been completed.
