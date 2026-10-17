# Published expression conventions

The authoritative machine-readable expressions are `task.formula.expression` in `bank.json`; independent registries are `nuclearbench/formulas.py` and `nuclearbench/expanded_formulas.py`. Published coefficients are the printed values, not estimates refitted to this bank. Designed controls are separately identified in `nuclearbench/controls.py`. Energy outputs are MeV and charge radius outputs are fm. `**` is exponentiation; only the arithmetic language documented below is accepted by the recovery scorer.

## Reference systems

1. A01: Bethe-Weizsaecker form in [Roy Chowdhury, Samanta and Basu, arXiv:nucl-th/0405080v4](https://arxiv.org/pdf/nucl-th/0405080), Eq. (1), coefficients in the text. A02: modified BWM, Eqs. (4)-(5). The volume coefficients are respectively **15.78 and 15.777**. The Coulomb term uses `Z*(Z-1)`. The experimental isotonic shift discussed later in that paper is excluded, because it would require neighboring observed targets. Coordinates are measured AME nuclides with `N>=8, 8<=Z<=83`.
2. A04-A09: [Sheng, Fan and Qian (2015), DOI 10.7498/aps.64.112101](https://wulixb.iphy.ac.cn/pdf-content/10.7498/aps.64.112101.pdf), Eqs. (2), (6), (4), (5), (10), (11), Table 1. The paper defines the equivalent sharp radius `R_C=sqrt(5/3)*r_rms` in Eq. (1). Every expression here is multiplied by `sqrt(3/5)` to produce the **rms charge radius** of the Angeli data. Coordinates have `N>8, Z>8`. Some formula families describe subregions better than others; category A tests recovery of the stated formula across the declared mathematical domain, not universal empirical accuracy.
3. A03 and A10: [Munoz, Udrescu and Garcia Ruiz, arXiv:2404.11477v3](https://arxiv.org/html/2404.11477v3), Eqs. (4) and (5). These are **leading-order MISR1** expressions, not the full iterative MISR10 system. Their numeric convention and coefficients are pinned to this preprint version, even though a later journal publication exists. Coordinates have `N>=8, 12<=Z<=50`. A10 includes the printed final `-I` term, with the expression interpreted as a numerical formula for fm; this is not an assertion that all printed coefficients are dimensionless physical constants.
4. A11-A13: the same Sheng source, Eqs. (7)-(9), Table 1. The negative printed isospin coefficients become plus signs in the implemented expressions; sharp-to-rms conversion is retained. These are related proton-scaling variants, not three new mechanisms.
5. A14-A15: [Ha and Cha, arXiv:nucl-th/0612003v2](https://arxiv.org/pdf/nucl-th/0612003), Eq. (1), Table I: `alpha*A**(-gamma)+beta*(exp(-lambda*Np)+exp(-lambda*Nn))`. Parameter sets `(alpha,beta,gamma,lambda)` are `(34.9,1,1.19,.36)` for 2+ and `(62.8,.9,.79,.24)` for 3-.
6. A16-A35: [Jin et al., arXiv:1007.3192v1](https://arxiv.org/pdf/1007.3192), Eq. (3), Table A p.9: `alpha*A**(-gamma)+beta_p*exp(-lambda_p*Np)+beta_n*exp(-lambda_n*Nn)`. The 20 printed coefficient rows are stored verbatim numerically in the registry. Although the caption mentions 11+, no coefficient row is supplied: 11+ is excluded. Spin/parity is fixed **per task** and is not an extra fitted input. All 22 spectroscopy instances, including Ha, share the declared `valence_spectroscopy` group.
7. A36-A37: [Heylen et al., arXiv:1609.05021v1](https://arxiv.org/pdf/1609.05021), Eq. (3a)-(3b), Duflo-Zuker radius reference. Naive parameters `(rho0,zeta,upsilon,g)=(.947,.8,.295,1.37)` with `A<=60`; correlated parameters `(.94,.8,.334,1.14), lambda=5.208`, with `8<N<=50,8<Z<30,A<=80`. The term linear in `t=N-Z` is `-zeta*t/(2*A**(4/3))` **inside** the `A**(1/3)` factor. No extra finite-size correction is silently applied to the source's empirical `r_pi` expression.
8. A38: [Angeli and Marinova (2013)](https://doi.org/10.1016/j.adt.2011.12.006), Eq. (8): `0.9071*A**(1/3)+1.105/A**(1/3)-.548/A`, in rms fm. The source also uses this interpolation for some reference anchors; these anchors are excluded from primary absolute-radius prediction.
9. A39-A41: [Pomorski and Dudek, arXiv:nucl-th/0205011v1](https://arxiv.org/pdf/nucl-th/0205011), macroscopic expression and Table I. These are **restricted analytic references**, the negative spherical macroscopic energy of the LDM/NLD/LSD parameterizations. Spherical shape factors are 1; `e^2=1.4399764 MeV fm` is the explicit benchmark numerical convention. Microscopic, deformation, electron and congruence contributions are excluded. These cards are not complete published nuclear mass predictions and have no asserted experimental target.

For spectroscopy recovery, every task uses the common AME2020 nonestimated-coordinate support filtered to even-even `8<=N<=154,8<=Z<=100`. Available conservative ENSDF measurements are context only; missing context is empty. The empirical expression is well defined even where a definite first-state observation is absent from this filtered snapshot. A common support avoids confounding the function comparison with different measurement-availability masks.

## Input macros

| Symbol | Definition |
| --- | --- |
| `N,Z` | Positive integer neutron and proton numbers |
| `A` | `N+Z` |
| `I` | `(N-Z)/(N+Z)` |
| `d` | `((-1)**N+(-1)**Z)/2`: +1 even-even, -1 odd-odd, 0 odd A |
| `P_s` | `vp*vn/(vp+vn)` with nearest-distance valence counts; zero at simultaneous closures |
| `P_m` | Same numerical definition, with the MISR reference closures |
| `Np,Nn` | Valence particle/hole distances to the declared standard shell boundaries |
| `P` | `Np*Nn/(Np+Nn)`, zero when both counts are zero |
| `Q_EI` | Product of proton/neutron `u*(D-u)/D**2` occupancy factors in EI shells |

Sheng `P_s` proton reference numbers: **2,6,14,28,50,82,114**; neutron reference numbers: **2,8,14,28,50,82,126,184**. MISR `P_m` uses **8,20,28,50,82** for both. `vp`/`vn` are minimum absolute distances to the respective lists; distances are nonnegative. These are source-specific conventions, including proposed/effective closures, not a declaration of universal nuclear magic numbers.

Standard `Nn` boundaries: 2,8,20,28,50,82,126,184; `Np`: 2,8,20,28,50,82,126. The spectroscopy upper-domain cut avoids dependence on unobserved upper-shell midpoints. `Q_EI` uses boundaries 2,6,14,28,50; `u=count-lower, D=upper-lower`, and vanishes at boundaries. Its mathematical implementation returns zero outside this helper range; admitted DZ tasks remain inside the declared supported domain.

`nuclearbench export --features nuclear` makes the same macro values available to every method. A supplied macro is prior knowledge. A comparison must not credit NuSR with discovery of that macro while withholding it from other methods.

## Formula recovery rules

The expression parser accepts arithmetic `+,-,*,/,**`, numeric literals, the symbols above and unary `sqrt,exp,log,abs`. It rejects attributes, indexing, arbitrary calls, lambdas and code execution. Parentheses and unary signs are permitted. The tree is limited to 512 AST nodes and 4,000 characters; a symbolic proof runs in a separate process with a five-second timeout.

For symbolic checks, decimal literals are interpreted as exact printed rational numbers and `N,Z` as positive integers. `A,I,d` are expanded. Valence/occupancy macros remain nonnegative symbolic variables: equality using the same macro can be proved, but a separately written piecewise implementation may remain unproved. Numerical witnesses evaluate the actual helper definitions. This limitation must be reported, not relabeled as failed recovery. Record both raw and normalized exported expressions and any adapter translation.

Finite numerical agreement uses the clean held-out labels and a deterministic grid spanning parity classes and shell neighborhoods, within the task's registered domain. The tolerance is `rtol=1e-8, atol=1e-8*std(clean training y)`, with a scale floor of `1e-12`. It is a numerical-agreement measure, not a proof. Approximate learned constants can therefore fail the strict agreement criterion while achieving excellent RMSE; report both measures. No scorer-side coefficient refit is performed.

Complexity is a **registered syntax cost**, separate from tool-native tree size. Constants and raw variables cost 1; each operation costs 1; macro costs are `A:3, I:9, d:9, P_s:67, P_m:43, Np:55, Nn:63, P:131, Q_EI:95`. Macro costs are declared protocol weights, not claims of literal expanded subtree size. Report the expression and native complexity alongside this cost, and compare error-complexity frontiers; avoid claiming a universal simplicity ranking from one cost system. Physically harmless floating-point underflow to zero is allowed for localized exponentials; nonfinite/invalid outputs still fail.

The 46 empirical instances belong to thirteen declared related groups. Four analytic references form two separate groups: three macroscopic pieces and one TRK sum rule. Designed controls use 16 declared templates in their own panel. None of these group labels is a proof of independence. A04 and A05 remain deliberately easy calibration cases. No supplied reference expression, coefficient vector or exact matching initializer may be counted as de novo recovery. Template-assisted runs belong in a separately labeled panel.

## Additional N/Z references in 0.2.0

The exact generated expressions and domains for A42-A50 are in `bank.json`.
A42-A44 use the [RIPL handbook](https://www-nds.iaea.org/RIPL-3/handbook/ripl2-feb2005.pdf),
printed p.129, Eq.(7.25): `E0=31.2*A**(-1/3)+20.6*A**(-1/6)`,
`width=0.026*E0**1.91`, `peak=144*N*Z/(A*pi*width)`. Substitute E0 and width
fully to obtain N/Z-only expressions; no measured energy/width is supplied.
These cases use the one-mode experimental-fit coordinates with A>=40; this
is a reference domain, not proof that every selected nucleus is spherical.

A45-A46 use the official 2018 SLO/SMLO centroid parameterization
`e1*sqrt(4*N*Z/A**2)*A**(-1/3)/sqrt(1+e2*A**(-1/3))` with `(e1,e2)`
`(130.0,9.0)` and `(128.0,8.5)`. They are two instances of one structure.
Their coordinate/context source is the SLO experimental-fit table; those
context values are not represented as SMLO measurements. See the frozen
[official README](source_snapshots/ripl4-gdr.readme), COMMENT 2.

A47 is the [Raman/Grodzins product](https://arxiv.org/html/2105.07164v1),
Eq.(1): `25.7*Z**2*A**(-2/3)` in MeV e^2 fm^4. The source coefficient
2.57 uses keV and e^2 barn^2; converting their product multiplies it by 10.
The real prediction task is also the product, so measured E2 is never a
hidden input for B(E2). Primitive level and strength dependencies are retained.

A48-A49 are average pairing references from the [primary BCS paper](https://arxiv.org/pdf/nucl-th/0308046v1),
Eq.(16): `12/sqrt(A)` and `(7.2-44*I**2)*A**(-1/3)`, MeV, with original
Vogel/Jonson/Hansen credit retained. A49's benchmark coordinates are restricted
to 50<Z<82 and 82<N<126. An average pairing gap is not asserted to be exactly
the measured three-point mass difference. No experimental gap is fabricated
for these references; AME supplies coordinates only.

A50 is the unenhanced TRK analytic reference `60*N*Z/A` in MeV mb, using
kappa=0 and the handbook text below Eq.(7.25). It is not an asserted measured
integral. The fixed pi convention for A44 is 3.141592653589793.
