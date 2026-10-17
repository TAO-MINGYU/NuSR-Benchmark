# Model selection and published artifacts

This is a task-matched candidate list, not a literature leaderboard. Software versions and effective settings are deliberately finalized at campaign launch, after NuSR/MySR development is complete. No paper-level metric below has been copied into a supposedly matched result table.

## Horizontal: expression recovery

| Method | Role | Primary-source entry |
| --- | --- | --- |
| NuSR | Nuclear-structure product under evaluation | [NuSR](https://github.com/TAO-MINGYU/NuSR) |
| PySR | Established external evolutionary SR reference | [Official repository](https://github.com/astroautomata/PySR) |
| MySR | General precursor; assess the gain from nuclear specialization | [MySR](https://github.com/TAO-MINGYU/MySR) |
| Operon | Additional independently implemented SR reference | [Operon](https://github.com/heal-research/operon), [Python binding](https://github.com/heal-research/pyoperon) |
| AI Feynman, optional | Different discovery approach, if its supported language and discrete nuclear inputs fit a card | [Original paper](https://www.science.org/doi/10.1126/sciadv.aay2631) |

Four core methods are sufficient for a first release campaign. Adding many close variants increases maintenance and compute without necessarily adding scientific coverage. MySR's shared ancestry makes it valuable for specialization analysis, but it should not be the only external comparison. A clean grammar/feature/domain preflight comes before expensive runs. Unsupported syntax is recorded as coverage information, and not interpreted as proof of worse search within a shared language.

## Vertical: learned predictors trained on these partitions

| Core baseline | Why retain it | Candidate recipe to freeze before running |
| --- | --- | --- |
| Gaussian process regression | Strong small-data smooth predictor and useful uncertainty baseline | N/Z-only and the same declared nuclear features; train-only standardization; kernel family and validation search budget fixed |
| LightGBM | Nonlinear tabular model with interactions and modest training cost | Shared declared features; validation-only early stopping; fixed parameter search space and budget |
| MLP ensemble | Neural reference with a different inductive bias | Shared inputs; train-only standardization; fixed architecture/optimizer/early stopping; report all member costs |
| Empirical train-only reference | Checks whether a sophisticated method beats a basic physical fit | Liquid-drop coefficients for mass and radius scaling parameters fitted only on training data; separately label historically published coefficients |

Do not choose a large neural model merely because it is newer. These evaluated datasets contain hundreds to a few thousand usable rows; baseline strength and matching information access matter more than model count. GPR and tree models can provide strong competition. A residual model needs the same physical reference available to NuSR and separate cost/provenance accounting.

## Nuclear publications and reuse options

| Observable / publication | Verified useful artifact | Planned use and remaining conditions |
| --- | --- | --- |
| Nuclear mass: Yuksel et al., [PRC 109, 064322 (2024)](https://doi.org/10.1103/PhysRevC.109.064322), [preprint](https://arxiv.org/abs/2401.02824) | Published SVR/GPR method with physics features and an extrapolation study | Motivates GPR/SVR candidates. Code, exact per-nuclide predictions and identical splits are not established here; reproduce on this bank if absent. The paper predicts mass excess: derive binding with identical fixed constants before comparing a binding target. |
| Binding and radii: Munoz et al., [MISR preprint](https://arxiv.org/html/2404.11477v3), [published article](https://doi.org/10.1038/s42005-025-02023-2) | Printed expressions and [author model implementation/notebooks](https://github.com/munozariasjm/nuclear-misr) | Cheaply evaluate published expressions; full MISR10 reuse requires pinning an author-code commit and matching conventions. A01-A10's recovery references do not imply permission to seed exact answers. Published models are calibrated external references, not cleanly retrained holdouts. |
| E2+ and transition properties: [NST 36, 21 (2025)](https://doi.org/10.1007/s41365-024-01613-z) | Article explicitly links supporting data: [Science Data Bank DOI](https://doi.org/10.57760/sciencedb.j00186.00423) | Strong reason to include LightGBM. Existence of a data deposit is verified; its downloadable contents, per-nuclide prediction coverage and split alignment still need auditing. Do not assume a deposit contains model predictions or the same 509-nucleus filtered ENSDF set. |
| Nuclear mass theory: HFB-24, [official ULB tables](https://astro.ulb.ac.be/pmwiki/Brusslib/Hfb17), [model paper](https://doi.org/10.1103/PhysRevC.88.024308) | Official downloadable table of 8,392 theoretical masses | Import and convert to the exact bank definition; recompute errors on matched IDs without rerunning HFB. Historical calibration overlap must be labeled. Missing predictions require an explicitly common intersection panel in addition to coverage reporting. |
| Nuclear mass theory: FRDM(2012), [publication/table reference](https://arxiv.org/abs/1508.06294) | Published global theoretical mass table | Useful second physics reference. Acquire and checksum the official machine-readable artifact before adoption; no table has been imported in this bank release. As with HFB, calibration and mass-convention checks are necessary. |
| Charge radii: [Sheng et al. (2015)](https://doi.org/10.7498/aps.64.112101) | Printed radius formulas and coefficients | Evaluate directly; convert sharp radius to rms before scoring. Published coefficients fitted to overlapping evaluated data are a descriptive reference, not leakage-free training. |
| Fixed-spin spectroscopy: [Ha/Cha](https://arxiv.org/abs/nucl-th/0612003), [Jin et al. tables](https://arxiv.org/abs/1007.3192) | Printed empirical formulas and 20 explicit yrast parameter rows | The new recovery references are directly evaluable. Their prediction use is a historical-calibration reference panel, not a train-only refit or independent recovery success. Related spin instances share group weight. |
| Light radii: [Heylen et al.](https://arxiv.org/abs/1609.05021) | Printed naive/correlated DZ radius expressions and parameter sets | Keep their source-specific radius notation, domains and EI-shell occupancy definition. They are not a full Duflo-Zuker mass-model implementation. |

No additional published-model table is silently bundled or treated as a finished baseline. Candidate-source availability is not a completed reproduction. Data deposits can contain experimental data alone; prediction tables can omit IDs, units or training membership. Audit their actual contents before marking them reusable.

## When can a paper replace a local model fit?

1. A complete published formula or released model can be evaluated locally: cheap inference can replace costly training, but preserve its original calibration status.
2. A per-nuclide prediction table can be aligned by `(N,Z)` and scored with this bank's labels. Freeze artifact hashes, units, prediction date and exact coverage. Match the primary test set completely; if only an intersection is available, define a separate common-intersection panel for **all** methods and disclose missing coverage.
3. A trained model/checkpoint may be reused if its preprocessing and information access can be reproduced. It belongs in the published-model panel unless its training membership matches the registered partition.
4. A paper reporting only aggregate RMSE/MAE supplies background context. It cannot replace the test predictions needed for this benchmark's formal ranking.

The bottleneck is usually **matching the evaluation protocol**, not whether another local numerical calculation is possible. A published model may predict almost every needed nuclide cheaply, yet have trained on this bank's test nuclei. That comparison can still be informative if labeled correctly; it is not a fair claim about held-out learning superiority.

For T tasks, an existing physical model with genuinely frozen pre-test calibration can provide useful retrospective forecasting evidence after the original fit date and data coverage are verified. A later AME2020 refit cannot be presented as an earlier forecast merely because its model family is older. The primary learned-model comparison still uses the identical retained AME2016 training and validation labels.
