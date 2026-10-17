# Published expression conventions

The authoritative machine-readable expressions are `task.formula.expression` in `bank.json`; the independent source registry is `nuclearbench/formulas.py`. Decimal coefficients are the printed values, not estimates refitted to this bank. Energy outputs are MeV and charge radius outputs are fm. `**` is exponentiation; only the arithmetic language documented below is accepted by the recovery scorer.

## Reference systems

1. A01: Bethe-Weizsaecker form in [Roy Chowdhury, Samanta and Basu, arXiv:nucl-th/0405080v4](https://arxiv.org/pdf/nucl-th/0405080), Eq. (1), coefficients in the text. A02: modified BWM, Eqs. (4)-(5). The volume coefficients are respectively **15.78 and 15.777**. The Coulomb term uses `Z*(Z-1)`. The experimental isotonic shift discussed later in that paper is excluded, because it would require neighboring observed targets. Coordinates are measured AME nuclides with `N>=8, 8<=Z<=83`.
2. A04-A09: [Sheng, Fan and Qian (2015), DOI 10.7498/aps.64.112101](https://wulixb.iphy.ac.cn/pdf-content/10.7498/aps.64.112101.pdf), Eqs. (2), (6), (4), (5), (10), (11), Table 1. The paper defines the equivalent sharp radius `R_C=sqrt(5/3)*r_rms` in Eq. (1). Every expression here is multiplied by `sqrt(3/5)` to produce the **rms charge radius** of the Angeli data. Coordinates have `N>8, Z>8`. Some formula families describe subregions better than others; category A tests recovery of the stated formula across the declared mathematical domain, not universal empirical accuracy.
3. A03 and A10: [Munoz, Udrescu and Garcia Ruiz, arXiv:2404.11477v3](https://arxiv.org/html/2404.11477v3), Eqs. (4) and (5). These are **leading-order MISR1** expressions, not the full iterative MISR10 system. Their numeric convention and coefficients are pinned to this preprint version, even though a later journal publication exists. Coordinates have `N>=8, 12<=Z<=50`. A10 includes the printed final `-I` term, with the expression interpreted as a numerical formula for fm; this is not an assertion that all printed coefficients are dimensionless physical constants.

## Input macros

| Symbol | Definition |
| --- | --- |
| `N,Z` | Positive integer neutron and proton numbers |
| `A` | `N+Z` |
| `I` | `(N-Z)/(N+Z)` |
| `d` | `((-1)**N+(-1)**Z)/2`: +1 even-even, -1 odd-odd, 0 odd A |
| `P_s` | `vp*vn/(vp+vn)` with nearest-distance valence counts; zero at simultaneous closures |
| `P_m` | Same numerical definition, with the MISR reference closures |

Sheng `P_s` proton reference numbers: **2,6,14,28,50,82,114**; neutron reference numbers: **2,8,14,28,50,82,126,184**. MISR `P_m` uses **8,20,28,50,82** for both. `vp`/`vn` are minimum absolute distances to the respective lists; distances are nonnegative. These are source-specific conventions, including proposed/effective closures, not a declaration of universal nuclear magic numbers.

`nuclearbench export --features nuclear` makes the same macro values available to every method. A supplied macro is prior knowledge. A comparison must not credit NuSR with discovery of that macro while withholding it from other methods.

## Formula recovery rules

The expression parser accepts arithmetic `+,-,*,/,**`, numeric literals, the symbols above and unary `sqrt,exp,log,abs`. It rejects attributes, indexing, arbitrary calls, lambdas and code execution. Parentheses and unary signs are permitted. The tree is limited to 512 AST nodes and 4,000 characters; a symbolic proof runs in a separate process with a five-second timeout.

For symbolic checks, decimal literals are interpreted as exact printed rational numbers and `N,Z` as positive integers. `A,I,d` are expanded. `P_s,P_m` remain nonnegative symbolic variables: equality using the same macro can be proved, but a separately written piecewise valence implementation may remain unproved. This limitation must be reported, not relabeled as failed recovery. Record both raw and normalized exported expressions and any adapter translation.

Finite numerical agreement uses the clean held-out labels and a deterministic grid spanning parity classes and shell neighborhoods, within the task's registered domain. The tolerance is `rtol=1e-8, atol=1e-8*std(clean training y)`, with a scale floor of `1e-12`. It is a numerical-agreement measure, not a proof. Approximate learned constants can therefore fail the strict agreement criterion while achieving excellent RMSE; report both measures. No scorer-side coefficient refit is performed.

Complexity is a **registered syntax cost**, separate from tool-native tree size. Constants and raw variables cost 1; each operation costs 1; macro costs are `A:3, I:9, d:9, P_s:67, P_m:43`. The valence macro costs are declared protocol weights, not claims of literal expanded subtree size. Report the expression and native complexity alongside this cost, and compare error-complexity frontiers; avoid claiming a universal simplicity ranking from one cost system.

These ten cards belong to five related formula families; they are not ten independent discoveries. Report by formula and family. A04 and A05 are deliberately easy calibration cases. A08 and A09 test valence and pairing information, while A02 and A10 add exponential structure. No supplied reference expression, coefficient vector or exact matching initializer may be counted as de novo recovery. Template-assisted runs belong in a separately labeled panel.
