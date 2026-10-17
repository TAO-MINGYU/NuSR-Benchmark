# New source conventions and leakage boundaries

All ordinary prediction coordinates satisfy N>=8 and Z>=8. New candidates need
at least 30 retained rows and two enabled structural splits. The original
input bytes are locked in [bank.json](bank.json); source-reader exclusions are
in [external_audit.json](external_audit.json). Task definitions and information
restrictions are stored in each new task's `target_spec`.

## Recommended ground-state moments

The IAEA magnetic and quadrupole CSV tables identify report 0915 and 0833
respectively. Column two, misleadingly headed `n.n+n.z`, contains A, not N;
N is A-Z. Only exact zero excitation energy, the selected report and definite
spin/sign/value are retained. Conflicting duplicate recommendations would all
be excluded. Parenthesized tentative signs, alternative values, limits, malformed
uncertainties and inferred signs are not repaired into point labels.

Magnetic `[nm]` denotes nuclear magnetons, mu_N, not nanometres. Quadrupole
values in barns are multiplied by 100 to obtain e fm^2. Parenthesized uncertainty
digits are converted using the value's last decimal place. Published reference
corrections and evaluation correlations remain part of the data; these are
recommended quantities, not independent raw measurements.

## RIPL-4 GDR response

The official IAEA-NDS repository is frozen at commit
`54afc19a4f7c861d28237c1da812d4cf385b528d`. The 2018 SLO file contains 8,980
rows: 135 `In=1` experimental-data fitted recommendations and 8,845 `In=0`
systematic values. Only the former supply prediction labels. There are 74
one-mode and 61 two-mode recommendations. A one-mode fit is not proof that
the actual nucleus has a spherical ground state.

`E1/W1/peak1` describe the single mode or lower mode; `E2/W2/peak2` describe the
upper mode only where present. The peak is the individual Lorentzian component,
not the sum of both responses at an energy. The centroid is calculated as
`(E1*S1+E2*S2)/(S1+S2)` from rounded published components, or E1 for one mode.
The component strengths and their sum are context for this convention, not
extra independent prediction tasks. No covariance/parameter uncertainties are
supplied in this file, so sigma is unknown. Parameters retain their fitted-model
status and are reported separately from primary observations.

The 2005 handbook gives the unenhanced TRK integral in MeV mb. The 2018
README's shortened `[mb]` TRK label is not used to assign units to that analytic
integral. Its Lorentzian peak cross sections are in mb.

## Evaluated s-wave neutron resonances

The 2025 RIPL-4 file preserves both RIPL-3 and BNL2018 columns. The benchmark
uses BNL2018 only; it never fills missing BNL values from another evaluation.
N/Z identify the incident target, with fixed partial wave L=0. The corresponding
compound nucleus is (N+1,Z) and is not substituted for the target coordinate.
Target spin, parity and neutron binding energy are provenance, not predictors.

Spacing labels are `log10(D0/1eV)` in dimensionless decades. Their published
uncertainties use first-order propagation `sigma_D/(D0*ln(10))`; this is not a
lognormal uncertainty model. Average radiative width is in eV. Neutron strength
values retain the reported units of 1e-4, rather than silently rescaling them.
No learned transform uses held-out labels.

## Empirical fission-barrier parameters

The 2025 table provides inner/outer heights and curvatures. These are empirical,
model-dependent structure parameters, partly assessed from calculations, rather
than direct observations of an experimental potential. The source's estimated
errors are ad-hoc spreads; they remain in provenance and are not passed off as
statistical sigma. The inconsistent Z=84/A=207/Bi row is excluded. Four related
targets share a declared family; some edge/shell splits are unsupported.

## Optional ground-state decay extension

NUBASE2020 state index must be zero, with no ambiguous/inverted ground-state
ordering flag. Stable, particle-unstable, estimated, approximate, censored or
unknown half-lives do not become point labels. Select only numeric direct
branches with positive fractions and no limits/estimation markers.

`T_partial = T_total/(branch_percent/100)`. Year conversion is 365.25 days;
all labels are `log10(T_partial/1second)` in dimensionless decades. A total
half-life is not relabeled as a partial lifetime when the branch is below
100%. Source uncertainty text remains in provenance; unknown branch/lifetime
covariance means sigma is unavailable. The B+ source convention includes
electron capture; an explicit EC-only branch has its own target. Ground-state
alpha, beta-minus, beta-plus/EC, EC and spontaneous fission pass coverage;
proton/two-proton candidates do not. These tasks are an optional nuclear-decay
panel, not evidence of reaction capability.

## Collectivity product and allowed information

The product uses the existing conservative first-2+ ENSDF and adopted
B(E2;0+->2+) labels, with both primitive parent sets retained. MeV times
e^2 fm^4 is the target. It does not provide measured E2 as input to predict
BE2. This is one composite relation, not an independent new experiment.

Several source families also appear in NuSR embedded bundles. Every primary
fit must disable direct/derived target lookup, measured moments, mass/Q values,
levels, branches, lifetimes and resonance parameters as inputs. Re-fetching a
public table does not make it independent or blind. Separate assisted models
and historically calibrated published formulas from matched training comparisons.
