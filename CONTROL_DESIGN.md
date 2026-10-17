# Designed nuclear-mechanism controls

These are **synthetic diagnostics**, not extra experimental discoveries. Their purpose is to separate expression-search difficulties that a few related empirical formulas cannot isolate. The complete templates, parameter ranges and instantiated coefficients are in `nuclearbench/controls.py` and each S task's `formula` metadata.

Their target is explicitly named `E_control`, a designed numeric energy, rather than total binding `B`. Restricted published macroscopic pieces use the distinct `B_macro` target. Neither quantity is mislabeled as a directly measured total binding energy.

## Templates and interpretation

| Templates | What is varied |
| --- | --- |
| S01-S02 | Smooth quadratic isospin and surface/curvature symmetry scaling |
| S03-S04 | Absolute isospin cusp and exponentially decaying congruence-like terms |
| S05-S06 | Discrete even-even/odd-odd pairing, power-law decay and isospin modulation |
| S07-S09 | Separate and joint localized shell terms; smooth Gaussian versus absolute-distance cusp |
| S10-S12 | Valence proton/neutron product, saturation and symmetry modulation |
| S13-S14 | Shell-isospin and shell-parity interactions |
| S15-S16 | Global bulk/surface/symmetry structure combined with pairing or shell/collective terms |

These mechanisms are motivated by the liquid-drop, pairing, shell and valence-systematics literature referenced in [FORMULAS.md](FORMULAS.md) and [COVERAGE.md](COVERAGE.md). The **specific combinations and numeric coefficients are benchmark designs**. A Gaussian shell bump is a controlled localization assumption, not a universal measured shell-correction law. Positive or negative contributions use the declared numeric energy convention; a template is not necessarily a complete physically positive binding energy.

There are **16 templates and three coefficient instances per template**, hence 48 task instances. They are not 48 independent structures. For each `(template, instance, parameter)`, SHA-256 of `nuclearbench-v2-control:<template>:<instance>:<parameter>` supplies a 12-hex-digit uniform fraction. This historical generator namespace is retained across release renumbering so the controls stay byte-identical. Map it into the published parameter range and round to four decimals. Shell centers use the predetermined pairs `(28,20),(50,28),(82,50)` for instances 1,2,3. No observation targets, algorithm errors or NuSR results enter this construction. The coordinates come from nonestimated AME nuclides within `8<=N<=154,8<=Z<=100`; their binding labels are **not used**.

## Development and confirmation roles

- Instance 1 of S01-S12 is the development pool: 12 tasks.
- Instances 2 and 3 of S01-S12 are coefficient-instance confirmation: 24 tasks.
- All three instances of S13-S16 are composition-family confirmation: 12 tasks.

The resulting public confirmation pool has 36 tasks. The manifest records `evidence_role` and `confirmation_axis`. Freeze adapters, model versions and tuning rules using only the development pool before reporting confirmation performance. The formulas and labels are public, so this division is **not a claim of a private blind test or developer nonexposure**. It is an auditable separation of tuning roles. The default aggregation excludes development tasks; choosing an easier confirmation subset after seeing scores is forbidden.

Clean, 1% and 5% training-label noise variants follow the existing protocol, with clean validation/test labels. All compared tools receive identical perturbed targets and the same declared deterministic feature knowledge. If a NuSR initializer already supplies a target structure or its exact coefficients, label the run as assisted. Recovering a provided template is not evidence of independent expression discovery. Include generic or structurally mismatched cases in the family report rather than retaining only NuSR-friendly outcomes.

Report by template/group, coefficient instance and confirmation role. Use equal-group aggregation, failure accounting, complexity and compute measurements. A high control recovery rate is evidence about the registered artificial task distribution; actual nuclear usefulness still requires the real-observation panel.
