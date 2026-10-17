# Development log

## 2026-10-17 — independent release bank v1

Replaces the earlier protocol-only proposal with two explicit label semantics:
published empirical expressions evaluated on observed nuclear coordinates, and
measured/evaluated observables without an asserted exact expression. All work
is performed in the independent benchmark repository worktree. NuSR and
NuSRCore implementations are not imported by data construction or scoring.

Release contents: 10 expression-recovery cards, 15 observable-prediction cards,
32,815 task rows, seven partition families and 173 enabled task/split pairs.
The two sparse B14 edge partitions remain explicitly disabled. The ten formula
cards represent five related families; task rows are not independent nuclei.

Validation completed on Python 3.11.15, NumPy 2.4.6, SymPy 1.14.0:

- 13 focused tests pass, both in the development environment and from outside
  the checkout using a separately created virtual environment with a normal
  noneditable package installation. Tests cover physics anchors, radius
  conventions, source qualifiers, ambiguous level assignments, primitive
  embargoes, source fetching without network, checksum tampering, ID alignment,
  incomplete/nonfinite predictions, expression syntax and equality versus fit.
- Full 56-member artifact inventory validates. Two independent source rebuilds
  reproduced all frozen artifacts byte-for-byte in the recorded environment.
- All ten published reference expressions passed symbolic equality and the
  independent nuclear-domain numerical witnesses. These are scorer integrity
  checks, not recovery results obtained by an SR search.
- Installed CLI exports produce deterministic training-only noise and omit
  held-out targets by default; validation/test remain unchanged. The train-only
  NumPy linear example produced a complete, valid 169-row radius prediction
  file. Its error is a workflow smoke result, not a model comparison.
- Ruff checks/formatting, local documentation links and Git whitespace checks
  pass. Standalone data tools import no NuSR/MySR package or Julia runtime.

Fresh upstream retrieval initially returned HTTP 403 with a default Python
request and later at the mutable IAEA radii page. The downloader now identifies
itself, verifies the five bundled original small source files and retrieves only
the large ENSDF archival zip when needed. The complete six-file acquisition
then passed pinned source hashes. Original source bytes remain attributed and
are not relicensed under the software MIT license.

The work was implemented and reviewed in a fresh isolated benchmark worktree;
NuSR/NuSRCore source and other retained worktrees were preserved. Initial local
Git identity setup was confined to this new repository. Public release is via
the reviewed main branch of TAO-MINGYU/NuSR-Benchmark, version 1.0.0.

No NuSR/PySR/MySR/Operon search campaign, predictor comparison, cluster job or
claim of scientific superiority is part of this release. Campaign model
revisions, effective options and compute budgets remain explicitly unresolved
in the template until the actual software is finalized. Source datasets were
already used during development: validation is retrospective, not blind.

## 2026-10-17 — scientific coverage expansion v2

The v1 publication-adequacy review identified a small, correlated 10-formula
recovery panel. This expansion is implemented in a fresh benchmark-only
worktree from the unchanged v1 main commit. NuSR and NuSRCore source checkouts
are unchanged; no scientific search or predictor campaign was run to select
tasks or coefficients. The immutable v1.0.0 tag is retained.

Version 2 contains 120 task instances and 194,077 task rows: 38 published
empirical formula instances in eight declared related groups, three restricted
spherical macroscopic references, 48 synthetic controls from 16 templates,
22 evaluated-observable tasks and nine evaluation-vintage tasks. It has 770
enabled and 16 explicitly disabled task/split pairs. Twelve synthetic instances
are development-only; 36 public confirmation instances are not blind. Spin,
coefficient, split and noise variants are not independent physical laws.

The source audit adds spectroscopy and radius references, a machine-readable
literature admission/exclusion ledger, conservative higher-spin coverage rules,
and original AME2016 labels for historical prediction. Cross-edition primitive
IDs prevent derived-mass leakage. T01 has 71 newly evaluable test nuclei; old
training values remain old even when revised. B10 now excludes 72 radii whose
element-level absolute reference anchors were identified as model-based in the
source discussion, retaining 812 evaluated entries. This does not imply that
all retained radii are independently measured absolute quantities.

Validation completed on Python 3.11.15, NumPy 2.4.6 and SymPy 1.14.0:

- All 27 focused tests pass in a separate normal noneditable installation,
  invoked outside the checkout. Added checks cover independently calculated
  published physics anchors, missing spectroscopy observations, original old
  labels, cross-vintage embargoes, synthetic roles, inventory documentation,
  equal-group weighting, and incomplete/failed/duplicate/mismatched runs.
  Terminal failures cannot inherit recovery credit from stale candidate flags.
- The 251-member artifact inventory validates. The final pinned-source rebuild
  reproduces every frozen data, split, source and metadata artifact byte-for-byte
  in this environment. The SHA-256 of checksums.json is
  c25852b240a5643c6bac5b4c98197c993f7f1a04ceea7c32836fe122d12571a7.
- All 89 registered reference expressions pass symbolic equality and independent
  nuclear-domain numerical witnesses. These checks supply the known answers to
  the scorer; they are not SR rediscovery results. This check used four workers
  after inspecting CPU affinity, load, cgroup limits and available memory;
  ordinary validation and numerical library threads remain single-threaded.
- Installed CLI checks export all 71 T01 test coordinates without targets,
  recover a synthetic known answer, detect an incomplete fingerprinted result
  collection, and reproduce training-only noise without changing validation or
  test data. The train-only NumPy linear example produces and scores complete
  71-row temporal predictions; this is dataflow smoke evidence only.
- Ruff checks and formatting, local Markdown links, and Git whitespace checks
  pass. Generated task/coverage/split documents match the frozen inventory.
  Fresh GitHub matrix status is verified against the actual publication commit
  during release closure, rather than inferred from the configured workflow.

Source acquisition initially tried guessed AME2016 reaction filenames with
underscores and received HTTP 403; the official hyphenated filenames were then
retrieved and pinned. A development rebuild exposed a Python tuple versus JSON
list registry comparison, corrected before final freezing. Early build and
diagnostic artifacts were retained outside the repository. The full source
papers were reviewed for equations/coefficients; their PDFs are not redistributed.

The source search is selected rather than exhaustive. Synthetic diagnostics,
restricted mass-model pieces and repeated spin variants remain separate panels.
Historical availability is an evaluation-vintage proxy, not certified experiment
dates. Model revisions, actual options, compute/tuning budgets and the full
comparison campaign remain future work. This release establishes a broader,
reproducible question bank, not publication sufficiency or NuSR superiority.

## 2026-10-17 — requested numbering correction to 0.1.0

The maintainer requested a 0.x data-release sequence. The previous 120-task
release is renumbered from 2.0.0 to 0.1.0 with consistent package, bank, citation,
protocol, provenance links and regenerated artifact/campaign fingerprints. All
CSV labels and split bytes must match the prior release; historical commits and
audit entries are retained. This prepares the newly requested research/data
expansion as 0.2.0. No new target or scientific result enters this correction.

Correction validation: all 248 CSV/split/source files are byte-identical to
d320f86; the pinned-source rebuild validates the 120-instance bank. All27 tests
pass both in the task checkout and outside it using a fresh normal noneditable
0.1.0 installation (Python3.11.15/NumPy2.4.6/SymPy1.14.0). Ruff, formatting and
whitespace pass. New checksums.json SHA256:
856832654f8dd306b7b2ae3a21ded31249f9a980c9316424bc3552d4d8ab774a.


## 2026-10-17 — primary-source expansion 0.2.0

The explicitly requested primary-source research and catalogue review expands
120 to 151 task instances: 98 recovery and 53 prediction instances, 206,228 task
rows, 945 enabled and 58 unsupported task/split pairs. The new panels add moments,
collectivity products, GDR response, neutron-resonance and fission parameters,
and an optional decay extension. Experimental observations, evaluated parameters,
experimental-data fits, empirical systematics and analytic references retain
separate semantics. Nine recovery and 22 prediction instances are new; this
is not 31 independent laws or a result selected using NuSR outcomes.

All 76 supplied catalogue families have explicit admission/deferral decisions.
The current lowercase target directory was rechecked after the user's correction;
all 228 consulted metadata hashes match the original uppercase-directory snapshot.
Only independently verified primary data and conventions enter formal labels;
no personal documents or secondary licensed radius transcription are redistributed.
Nine pinned primary files are added, including official IAEA-NDS RIPL-4 bytes at
54afc19a4f7c861d28237c1da812d4cf385b528d. Reviewed paper PDFs remain outside Git.

Validation on Python 3.11.15 / NumPy 2.4.6 / SymPy 1.14.0:

- All 37 focused tests pass from outside the checkout using a separate normal
  noneditable installation. Coverage includes unit factors, state/sign/limit
  filtering, source-column and target/compound identity, direct decay branches,
  censored/estimated/isomer rejection, primitive dependencies and catalogue mapping.
- A changed primary label remains rejected after regenerating its checksum.
  Changing both source bytes and bank source hashes is rejected against the
  frozen code registry. Derived floating values allow 2e-14 comparison tolerance
  for cross-platform libm rounding; provenance and original byte hashes are exact.
- All 324 inventory members match a second pinned-source build byte-for-byte
  in this environment. The final checksums.json SHA-256 is
  8850fa5f95289068afad1b9a79c18a0e1f08805ae88fa23b5cc2e39c0d08a17f.
  All 248 preceding data, split and bundled-source files remain byte-identical
  to 0.1.0. Final log units are explicit dimensionless decades; no label changes.
- All 98 supplied reference answers pass symbolic equality and independent
  numerical nuclear-domain witnesses. A four-worker integrity check followed
  resource inspection, with numerical library threads fixed at one. These are
  answer/scorer checks, not expressions rediscovered by an SR model.
- Installed CLI checks export target-free magnetic-moment and SF test inputs,
  run the training-only linear example, and score complete files (159 moment
  rows and 13 SF rows). A nested GDR known-answer CLI check passes. These are
  workflow smoke results, not predictive comparisons.
- Ruff checks/formatting, local documentation links, and Git whitespace checks
  pass. The actual publication commit's three-Python-version remote matrix is
  checked during release closure; it is not inferred from workflow configuration.

Direct RIPL-3 data requests returned HTTP 403; official immutable RIPL-4 files
were used instead. Early parser/schema/test failures and source probes remain
in task-specific /tmp evidence, rather than being erased or counted as model
results. Proton and two-proton prediction candidates failed the unchanged minimum
coverage gate. Weisskopf direction/coefficient ambiguity, unverified spontaneous
fission coefficients, and extra-input reaction formulas remain deferred. Only
135 experimental-fit GDR rows are retained; 8,845 systematic recommendations are
excluded. Source identity errors are excluded, not silently repaired.

The preceding 120-task release is now v0.1.0 at e1f9233; its main and tag CI passed.
Original d320f86 remains archived under archive/120-task-v2.0.0, and the superseded
v2.0.0 tag was removed as requested without rewriting branch history. Legacy
25-task v1.0.0 remains documented. NuSR/NuSRCore source repositories and unrelated
worktrees are preserved. No formal SR/predictor training campaign, Slurm job,
blind-evaluation claim, or claim of NuSR superiority is part of this release.
