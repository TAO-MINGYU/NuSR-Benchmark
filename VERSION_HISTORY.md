# Version numbering migration

At the maintainer's request on 2026-10-17, the 120-instance release previously
published as v2.0.0 is consistently renumbered **v0.1.0**. This is a version
metadata/provenance update, not a new scientific bank: all CSV label and split
bytes are unchanged. Version metadata, generated inventories, control-design
links and artifact/campaign fingerprints are regenerated together.

Original commit d320f868eefe01b05b5be8c6ef3b58b895b9ade5 remains in Git history
and is archived under `archive/120-task-v2.0.0`. The old `v2.0.0` tag is replaced
by `v0.1.0`; no branch history is rewritten. The still older 25-card v1.0.0 tag
is a legacy historical artifact, not the new release sequence.

The next substantive data expansion is **v0.2.0**. Use the code and checksums
from the same version; artifacts whose source/version metadata changed must
not be mixed by relying only on their equal task counts. Historical development
log entries retain the names used when those operations occurred.
