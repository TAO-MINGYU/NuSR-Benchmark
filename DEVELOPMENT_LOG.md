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
