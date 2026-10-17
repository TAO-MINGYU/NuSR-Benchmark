# Release 0.2.0: primary-source and physical coverage expansion

This release expands the preceding 120-task bank to **151 task instances**:
98 expression-recovery instances and 53 prediction instances, with 206,228 task
rows, 945 enabled task/split pairs and 58 explicitly unsupported pairs. All
preceding CSV labels and split bytes are preserved. Nine recovery and 22
prediction instances are new. No model outcomes were used to choose them.

The gain is broader physical information and more demanding expression forms,
not a claim that 151 independent nuclear laws have been collected.

| Panel | Previous | Current | Interpretation |
| --- | ---: | ---: | --- |
| Published empirical recovery | 38 | 46 | Thirteen declared related groups; repeated spin/parameter cases remain related |
| Analytic-reference recovery | 3 | 4 | Three spherical macroscopic pieces plus the unenhanced TRK reference |
| Synthetic mechanism controls | 48 | 48 | Sixteen templates, unchanged; 12 development and 36 public confirmation instances |
| Evaluated observations | 22 | 25 | Adds two electromagnetic moments and the collectivity product |
| Evaluated neutron-resonance parameters | 0 | 3 | Fixed s-wave and BNL2018 source columns |
| Experimental-fit/empirical structure parameters | 0 | 11 | Seven GDR and four fission-barrier targets; not direct raw measurements |
| Nuclear-decay extension | 0 | 5 | Partial ground-state lifetimes; separate from the structure core |
| Historical evaluation holdout | 9 | 9 | Original AME2016 labels and newly evaluable AME2020 tests, unchanged |

## Research performed

Public primary sources examined include IAEA nuclear moments, AMDC/NUBASE,
RIPL handbooks and the official IAEA-NDS RIPL-4 repository, plus NNDC NuDat,
ENSDF and B(E2). NuDat's level/gamma/decay views principally expose ENSDF;
they are not a second independent level dataset. Original equations were checked
in the RIPL handbook, the 2018 GDR README, the 2003 pairing paper and the 2021
Grodzins paper. Reviewed PDF hashes and caveats appear in [literature.json](literature.json).

The supplied `Target` collection has 76 formula families spanning structure,
decay, reaction, astrophysics and matter. Its own audit calls it a catalogue,
not a ready-made benchmark or certification of every coefficient. Every family
now has an explicit decision in [TARGET_CATALOG_AUDIT.md](TARGET_CATALOG_AUDIT.md)
and [target_catalog_audit.json](target_catalog_audit.json), including hashes of
the metadata consulted. Personal documents and the licensed secondary radius
transcription were neither copied nor used to replace original source data.

## New empirical information

| Target family | Retained coverage | Why useful |
| --- | --- | --- |
| Ground-state magnetic dipole moment | 754 nuclei | Signed shell/parity-sensitive electromagnetic structure |
| Ground-state electric quadrupole moment | 513 nuclei | Signed spectroscopic deformation/collectivity information, distinct from charge radius |
| Grodzins E(2+) times B(E2) | 394 nuclei | Tests a collective relation without giving measured excitation energy as input |
| GDR response | 135 experimental-fit recommendations, 61 with two modes | Tests collective response energies, widths and peaks; 8,845 systematic rows excluded |
| s-wave neutron resonances | 293 spacing, 255 radiative-width, 268 strength labels | Tests level-structure information at a fixed physical condition, with target/compound identity explicit |
| Empirical fission barriers | 76 inner heights; 45 other parameter labels | Tests a difficult heavy-nucleus parameter surface with its model dependence retained |
| Partial decay lifetimes | 469 alpha, 1,116 beta-minus, 847 beta-plus/EC, 138 EC, 75 spontaneous-fission labels | Optional tests over a wide dynamic range; no measured Q input |

Counts overlap and are not independent measurements. GDR components, barrier
parameters, decay branches and mass differences must not inflate independence
claims. Ground-state moment signs, report versions and units are checked;
tentative signs, malformed values and ambiguous states are excluded. An
inconsistent Z=84/A=207/Bi source row is excluded rather than silently repaired.

Proton-emission and two-proton candidates have only 14 and four eligible domain
rows respectively. They fail the unchanged admission requirement of at least
30 labels and two usable structural splits and are not promoted to formal tasks.

## New recovery structures

The published GDR references add a sum of fractional inverse powers, a nested
noninteger power for width, a substituted reciprocal response expression, and
an isovector rational square-root structure. Two 2018 coefficient sets remain
one related structure. The Raman/Grodzins expression is reformulated as the
N/Z-only product target, with the conversion from keV/e-squared-barn-squared
to MeV/e-squared-fm-to-the-fourth checked explicitly. Classical and Vogel average
pairing references add a controlled comparison of isospin dependence; neither
is asserted to be the exact three-point empirical mass indicator. The TRK case
is an unenhanced analytic reference, not measured integrated strength.

## Why many catalogue formulas remain outside the primary bank

Measured Q values, neighboring measured masses, excitation energy, variable
spin, temperature, projectile/target pairs, radial or momentum coordinates
are additional information. A reaction function cannot become a NuSR N/Z-only
test by hiding these variables or replacing them with lookup tables. Such
families remain recorded for a different interface or explicitly assisted study.
Some apparently eligible simple scalings still lack verified coefficients,
conventions or measured datasets. The Weisskopf catalogue entry has an internal
coefficient/direction inconsistency and was deferred, not copied blindly.

## How this can support a NuSR strength claim

Use recovery outcomes to test search across the declared expression families,
and use the observational/parameter panels to test regional generalization.
Keep NuSR/PySR/MySR/Operon comparisons and NuSR/GPR/LightGBM/MLP comparisons
matched in information access, configuration selection and measured cost.
Include NuSR ablations for fixed nuclear knowledge, effects, AFE and specialized
search settings if attributing gains to specialization. All embedded target
lookups and exact-answer seeds require explicit auditing; several source
families overlap NuSR's embedded data. Group weights do not imply statistical
independence. Report all unsupported cases, failures and unfavorable outcomes.

This bank can discriminate strengths and limitations. It does not establish
NuSR superiority, journal acceptance or an untouched blind evaluation. Model
campaigns remain unexecuted and their software revisions/budgets must be frozen
before test results are observed. Validation evidence is recorded in
[DEVELOPMENT_LOG.md](DEVELOPMENT_LOG.md); a green integrity check is not a scientific result.

The preceding release is consistently renumbered **0.1.0**, and this substantive
expansion is **0.2.0**. See [VERSION_HISTORY.md](VERSION_HISTORY.md) for archived
commits and the replaced historical tag.
