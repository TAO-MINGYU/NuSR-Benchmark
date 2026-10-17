# Data sources, transformations and notices

This bank freezes evaluated public nuclear data, not a collection of independent raw experimental measurements. Source publications and official providers must be acknowledged when using the data. The software MIT license does **not** grant a new license to source datasets, articles or reference formulas. No full article, original software package or complete ENSDF archive is redistributed here.

## Official snapshots

| Dataset | Official source | Reference and retained fields |
| --- | --- | --- |
| AME2020 | [IAEA AMDC](https://www-nds.iaea.org/amdc/ame2020/) files `mass_1.mas20.txt`, `rct1.mas20.txt`, `rct2_1.mas20.txt` | [AME2020 II, DOI 10.1088/1674-1137/abddaf](https://doi.org/10.1088/1674-1137/abddaf); binding, mass parents, Sn/S2n/Sp/S2p |
| Published charge radii | [IAEA nuclear charge radii](https://www-nds.iaea.org/radii/) | Angeli and Marinova (2013), [DOI 10.1016/j.adt.2011.12.006](https://doi.org/10.1016/j.adt.2011.12.006); rms charge radii and uncertainties |
| Adopted B(E2) | [NNDC adopted JSON](https://www.nndc.bnl.gov/be2/data/adopted-entries.json) | Pritychenko et al. (2016), [DOI 10.1016/j.adt.2015.10.001](https://doi.org/10.1016/j.adt.2015.10.001); model-independent 0+ to 2+ strength |
| ENSDF | [NNDC September 2026 archive](https://www.nndc.bnl.gov/ensdfarchivals/distributions/dist26/ensdf_260901.zip) | Adopted levels, snapshot 2026-09-01; definite first 2+, 4+, 3- states of even-even nuclei with 0+ ground states |

Exact upstream SHA-256 hashes, URLs and cached retrieval date **2026-10-01** are in `bank.json` and `nuclearbench/sources.py`. This repository was assembled on **2026-10-17**. The five small original data files are preserved byte-for-byte in `source_snapshots/`, with original metadata and notices; the complete ENSDF zip remains an external archival download. Git attributes prevent line-ending conversion of these source bytes. Parsed CSV rows preserve original source records, including table-row positions or ENSDF file/line locations. Parsing is performed by the independent `nuclearbench/data.py`; it imports no NuSR bundle.

NNDC's [NuDat guide](https://www.nndc.bnl.gov/nudat3/guide/) describes use and attribution of retrieved material. The [NSDD/ENSDF dissemination policy](https://www.nndc.bnl.gov/nsdd/reports/indc-nds-421-r1.pdf) describes acknowledged use and reformatting of evaluated data. Original data-provider conditions and acknowledgments continue to apply. Do not imply endorsement by IAEA, AMDC, NNDC, Brookhaven or the evaluators.

## Filtering and units

- All primary category B coordinates have `N>=8,Z>=8`. Category A uses the per-formula domain in `bank.json`; see `FORMULAS.md`.
- AME `#` estimated entries are excluded. A mass-derived label requires every nonconstant mass parent to be present and nonestimated. Published separation energies and their uncertainties come from the reaction files; values are cross-checked against mass-excess differences to 3 eV. Convert keV to MeV by `1e-3`; total binding is `A` times the published rounded binding per nucleon. Do not silently use atomic mass as nuclear binding.
- Nucleon mass excesses are fixed constants from the same AME release, not experimental features available per test nucleus. Their common use does not require deleting every row during the primitive-dependency embargo.
- Three-point OES: `(-1)^q/2 * [ME(q-1)-2*ME(q)+ME(q+1)]`, where `q=N` or `Z`. Shell gap: `ME(q-2)-2*ME(q)+ME(q+2)`. Sigma is unknown because the covariance matrix is not included. Atomic mass convention is retained consistently.
- Only the published radius columns are used. Preliminary values and the neutron's negative mean-square charge radius are excluded from positive rms-radius regression. Do not mix matter, point-proton, charge rms and sharp radii.
- B(E2) is the model-independent adopted 2016 reference only. Exclude upper/lower limits and `LT,GT,LE,GE,AP,CA,SY` qualified point labels. Convert `e^2 b^2` to `e^2 fm^4` by multiplying by `10000`. Preserve negative/asymmetric source-error notation in `note`; do not invent a positive symmetric sigma. A deformation parameter derived from B(E2) is not a second independent experimental target here.
- ENSDF uses definite spin/parity labels; ambiguous lower levels or qualified/offset energies cause conservative exclusion rather than substitution of a higher definite level. Energy keV is converted to MeV. Numeric last-digit uncertainty is decoded using the printed energy precision. R42 is `E4/E2` with both level dependencies; its sigma is unknown without covariance.

Per-source usable counts before the primary N/Z cut are in `bank.source_counts`; each task records this source population and its retained count. Every primary row has a source locator. These counts describe the declared filtering, not all measurements in a publication. For example, a paper may quote 909 radius entries including a neutron entry, while this parse retains 908 positive published nuclear radii before its domain cut.

## Dependencies and data reuse

CSV `dependencies` contains primitive observations used to construct `y`. A mass parent is identified by `AME2020:ME:N:Z`; level parents have exact archive record IDs. For formula labels these dependencies are formula-coordinate IDs, while original observational dependencies remain in `observed_dependencies`. Formula coefficients were fitted historically and can encode experimental knowledge; that calibration overlap is disclosed rather than removed by row partitioning.

Partition purging prevents direct shared-parent labels across train/validation/test within a task. It cannot erase evaluator correlations, historical model calibration, developer exposure or cross-task supervision. No joint training on other task targets is allowed in the primary single-target comparison. A multi-target model needs an explicit joint primitive-dependency audit and a separate result panel.
