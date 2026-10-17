# Coverage audit — v0.1.0

## Instance counts and declared grouping

Declared groups organize reports; they do not certify statistical independence. Different coefficients, spin states, splits, noise levels or random seeds must not be counted as new structure families.

### evaluated_observables: 22 instances

| Declared group | Instances |
| --- | ---: |
| collectivity | 2 |
| mass | 1 |
| mass_difference | 4 |
| pairing | 2 |
| radius | 1 |
| shape_coexistence | 1 |
| shell_gap | 2 |
| spectroscopy | 9 |

### historical_new_measurements: 9 instances

| Declared group | Instances |
| --- | ---: |
| mass | 1 |
| mass_difference | 4 |
| pairing | 2 |
| shell_gap | 2 |

### published_analytic_reference: 3 instances

| Declared group | Instances |
| --- | ---: |
| macroscopic_curvature | 3 |

### published_empirical: 38 instances

| Declared group | Instances |
| --- | ---: |
| liquid_drop | 2 |
| misr | 2 |
| radius_inverse_powers | 1 |
| radius_isospin | 5 |
| radius_isovector_exponential | 2 |
| radius_scaling | 2 |
| radius_valence | 2 |
| valence_spectroscopy | 22 |

### synthetic_mechanism_control: 48 instances

| Declared group | Instances |
| --- | ---: |
| bulk_pairing | 3 |
| bulk_shell_collective | 3 |
| congruence_exp | 3 |
| isospin_quadratic | 3 |
| pairing_isospin | 3 |
| pairing_power | 3 |
| shell_absolute_exp | 3 |
| shell_gaussian_joint | 3 |
| shell_gaussian_sum | 3 |
| shell_isospin | 3 |
| shell_pairing | 3 |
| surface_symmetry | 3 |
| valence_isospin | 3 |
| valence_product | 3 |
| valence_saturation | 3 |
| wigner_cusp | 3 |

## Evaluated-observable admission

Original 15 core targets are retained with the radius-anchor correction. New observed targets require at least 30 conservative N/Z-domain rows and two enabled split families. The rule was fixed before any model campaign; sparse/ambiguous states are not rescued by relaxing their label definition.

| Target | Parsed source rows | Domain rows after exclusions | Admitted | Enabled splits | Reason |
| --- | ---: | ---: | --- | ---: | --- |
| B | 2550 | 2457 | True | 7 | legacy core retained |
| S2n | 2301 | 2232 | True | 7 | legacy core retained |
| S2p | 2212 | 2151 | True | 7 | legacy core retained |
| Sn | 2393 | 2314 | True | 7 | legacy core retained |
| Sp | 2343 | 2268 | True | 7 | legacy core retained |
| OES3n | 2264 | 2192 | True | 7 | legacy core retained |
| OES3p | 2173 | 2105 | True | 7 | legacy core retained |
| delta2n | 2086 | 2031 | True | 7 | legacy core retained |
| delta2p | 1893 | 1846 | True | 7 | legacy core retained |
| Rch | 908 | 812 | True | 7 | legacy core retained |
| BE2 | 424 | 417 | True | 7 | legacy core retained |
| E2plus | 524 | 509 | True | 7 | legacy core retained |
| E4plus | 369 | 368 | True | 7 | legacy core retained |
| E3minus | 103 | 99 | True | 5 | legacy core retained |
| R42 | 369 | 368 | True | 7 | legacy core retained |
| E6plus | 185 | 185 | True | 7 | meets >=30 observations and >=2 usable splits |
| E8plus | 88 | 88 | True | 5 | meets >=30 observations and >=2 usable splits |
| E10plus | 31 | 31 | True | 4 | meets >=30 observations and >=2 usable splits |
| E1minus | 51 | 45 | True | 5 | meets >=30 observations and >=2 usable splits |
| E5minus | 56 | 56 | True | 5 | meets >=30 observations and >=2 usable splits |
| E7minus | 20 | 20 | False | 2 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E9minus | 4 | 4 | False | 0 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E2minus | 27 | 23 | False | 2 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E4minus | 26 | 25 | False | 1 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E6minus | 7 | 7 | False | 0 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E8minus | 6 | 6 | False | 0 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E10minus | 2 | 2 | False | 0 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E1plus | 15 | 13 | False | 1 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E3plus | 109 | 108 | True | 5 | meets >=30 observations and >=2 usable splits |
| E5plus | 24 | 24 | False | 1 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E7plus | 4 | 4 | False | 0 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E9plus | 0 | 0 | False | 0 | insufficient conservative definite-state coverage: need >=30 rows and >=2 usable splits |
| E0plus | 228 | 221 | True | 6 | meets >=30 observations and >=2 usable splits |

The absolute-radius panel excludes 72 domain rows with Z=75,84,86,87,88,96 because of model-based reference anchors identified in the source discussion. Remaining radii are evaluated quantities with shared calibration/correlation, not independent raw measurements.

## Literature decisions

| Source ID | Decision | Locator / role | Caveat |
| --- | --- | --- | --- |
| [bw_bwm](https://arxiv.org/pdf/nucl-th/0405080) | admitted | Eqs. (1), (4)-(5) Original BW/BWM reference cards retained | Experimental isotonic shift is excluded; exact built-in template/initializer access must be audited |
| [sheng2015](https://doi.org/10.7498/aps.64.112101) | admitted | Eqs. (2),(4)-(11), Table 1 Radius scaling, isospin, finite-size and valence/pairing instances | Equivalent sharp radii converted to rms; proton-scaling variants remain related instances |
| [misr2024v3](https://arxiv.org/html/2404.11477v3) | admitted | Eqs. (4)-(5) Original leading-order MISR binding/radius cards retained | Version-pinned leading expressions, not the complete MISR10 model or a blind discovery challenge |
| [ha2007](https://arxiv.org/pdf/nucl-th/0612003v2) | admitted | Eq. (1), Table I Two fixed-state instances of one shared-rate valence formula | Fixed even-even spin tasks; reference valence boundaries stated explicitly |
| [yrast2010](https://arxiv.org/pdf/1007.3192) | admitted | Eq. (3), Table A p.9 20 fixed-state parameter instances; one structural family | No 11+ row in Table A despite caption; excluded. Sparse observed states use common AME coordinate anchors with no invented observations. |
| [heylen2016](https://arxiv.org/pdf/1609.05021) | admitted | Eq. (3a)-(3b), fitted parameter sets in text Naive and correlated Duflo-Zuker radius forms | Restricted light-nucleus domains and explicit EI-shell occupancy convention; original r_pi notation retained as an empirical radius reference |
| [angeli2013](https://doi.org/10.1016/j.adt.2011.12.006) | admitted | Eq. (8), reference-radius discussion Inverse-power rms-radius interpolation | Some evaluated radii share model-based absolute anchors; exclude Z=75,84,86,87,88,96 from primary absolute-radius prediction |
| [pomorski2002](https://arxiv.org/pdf/nucl-th/0205011) | restricted_reference | Macroscopic expression, Table I Three spherical analytic macroscopic components | These are not complete LDM/NLD/LSD mass predictions: no microscopic, deformation, electron or congruence corrections are invented |
| [dz_mass](https://arxiv.org/abs/1407.8218) | deferred |  Possible future complex shell-occupation recovery panel | Full model requires a separately audited algorithmic grammar; an opaque callable is not a short formula recovery answer |
| [radius_ml2025](https://arxiv.org/html/2512.06683v1) | assisted_panel_only |  Published radius SR/predictive reference candidate | Measured binding energy/pairing features exceed N/Z-only primary information; no silent primary admission |
| [madland_nix1988](https://doi.org/10.1016/0375-9474(88)90370-3) | deferred |  Potential pairing-gap references | Shape-dependent terms and target-estimator correspondence require further audit; no unverified coefficients included |
| [garvey_kelson](https://www.iasa.gr/stathis/Nucl/Mass_Prediction_Garvey_Kelson.pdf) | not_NZ_only_recovery |  Possible future mass-relation diagnostic | Neighboring measured masses are additional inputs; cannot silently count a relation as an N/Z-only expression |
| [variable_J](https://arxiv.org/pdf/1007.3192) | not_variable_J_primary |  Possible separate spectroscopy model study | Variable angular momentum and moment of inertia are outside N/Z input. Fixed-spin empirical yrast tasks do not add J as a fitted input. |

This is an audited selection, not an exhaustive literature review or a guarantee of manuscript acceptance. Source PDF hashes, where recorded, identify reviewed originals; complete articles are not redistributed.
