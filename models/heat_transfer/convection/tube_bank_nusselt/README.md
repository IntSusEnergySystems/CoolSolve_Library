# Crossflow tube banks: Nusselt-number correlations and row / angle correction factors

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0095`

Six EES `FUNCTION`s for the forced convection across a bank of plain tubes:
three correlations returning the Nusselt number of the bundle (Zukauskas with
the Bejan fit, ESDU 73031 as given by Hewitt, and the Heat Exchanger Design
Handbook) and three correction factors (the tube-row factor of Zukauskas, the
tube-row factor of ESDU 73031 and its bundle-inclination factor). The Nusselt
number is taken with respect to the tube **outside** diameter, so the
heat-transfer coefficient follows from `h = Nu*k/Do` and is left to the caller.
Arguments are dimensionless (Re, Pr, Pr_wall, the number of tube rows and the
flags) except the tube outside diameter and the two pitches, in metres; no
property function is called inside the functions. This is family `HT-009` of the
24 `ht` families of the library triage; it follows the layout of `CSL-0087`
(`internal_turbulent_nusselt`), the first of them.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; Re, Pr and Pr_wall are arguments) |
| **Size** | 28 equations after analysis; 6 functions of 1–110 lines (the two tables of the Zukauskas row correction are IF ladders) |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_tube_bank.py` (MIT); inventory row `HT-009` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (Zukauskas, Bejan, ESDU, Schlünder; see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (20 values, max deviation 2.8·10⁻¹²) |

## Problem statement

For a fluid crossing a bundle of `n` tubes of outside diameter `Do` with a
transverse pitch `pitch_normal` and a longitudinal pitch `pitch_parallel`
(Reynolds number Re, Prandtl number Pr, bundle inclination `angle`), compute the
Nusselt number of the bundle and multiply it by `k/Do` to obtain the average
heat-transfer coefficient. Three historical correlations and their row /
inclination correction factors are available; each has its own validity range
and the choice between them is left to the user, who knows the fluid and the
geometry.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `Nu_Zukauskas_Bejan` | Re, Pr, tube_rows, pitch_parallel, pitch_normal, Pr_wall | Nu = C·Re^m·Pr^0.36·(Pr/Pr_wall)^0.25·(Xt/Xl)^0.2·Cn, with C = 0.9/0.52/0.27/0.033 and m = 0.4/0.05/0.63/0.8 for Re < 100, < 1000, < 2·10⁵, ≥ 2·10⁵ (in-line) and C = 1.04/0.71/0.35/0.031, m = 0.4/0.5/0.6/0.8 for Re < 500, < 1000, < 2·10⁵, ≥ 2·10⁵ (staggered) | 1 < Re < 2·10⁵ (the four regimes above) |
| `Zukauskas_tube_row_correction` | tube_rows, staggered, Re | Cn = F(n), table of 19 values per configuration, F = 1 for n ≥ 20 | as in `ht`, none quoted |
| `Nu_ESDU_73031` | Re, Pr, tube_rows, pitch_parallel, pitch_normal, Pr_wall, angle | Nu = a·Re^m·Pr^0.34·F1·F2·F3, a = 0.742/0.211/0.116 and m = 0.431/0.651/0.700 (in-line) or a = 1.309/0.273/0.124 and m = 0.360/0.635/0.700 (staggered) for Re ≤ 300, ≤ 2·10⁵, > 2·10⁵; F1 = (Pr/Pr_wall)^0.26, F2 = `ESDU_tube_row_correction`, F3 = `ESDU_tube_angle_correction` | 10 < Re < 2·10⁶; transverse pitch/Do from 1.2 to 4 (in-line) and 1 to 4 (staggered); accuracy 15% |
| `ESDU_tube_row_correction` | tube_rows, staggered | F2 = table of 7 values per configuration, F2(3) for n ≤ 2, 1 for n ≥ 10 | as in `ht`, none quoted |
| `ESDU_tube_angle_correction` | angle [deg] | F3 = Nu_θ/Nu_θ=90° = (sin θ)^0.6 | 10² < Re < 10⁶; below 10° the problem is internal flow |
| `Nu_HEDH_tube_bank` | Re, Pr, Do, tube_rows, pitch_parallel, pitch_normal | Nu = Nu_m·f_N with Nu_m = 0.3 + √(Nu_m,lam² + Nu_m,turb²), Nu_m,turb = 0.037·Re^0.8·Pr/{1 + 2.443·Re^(−0.1)(Pr^(2/3) − 1)}, Nu_m,lam = 0.664·Re^0.5·Pr^(1/3) on Re/ψ, ψ = 1 − π/4a (b ≥ 1) or 1 − π/4ab, f_A = 1 + 0.7/ψ^1.5·(b/a − 0.3)/(b/a + 0.7)² (in-line) or 1 + 2/3b (staggered), f_N = {1 + (n−1)f_A}/n | 10 < Re < 10⁵, 0.6 < Pr < 1000 |

Arguments: Re (Reynolds number on `Do` and the average fluid properties, `[-]`),
Pr (bulk Prandtl number, `[-]`), Pr_wall (Prandtl number at the wall
temperature, `[-]`), `tube_rows` (number of tube rows per bundle, `[-]`),
`staggered` (flag: 1 staggered, 0 in-line, `[-]`), `Do` (tube outside diameter,
`[m]`), `pitch_parallel` (longitudinal pitch, `[m]`), `pitch_normal`
(transverse pitch, `[m]`) and `angle` (inclination of the bank with respect to
the longitudinal axis, `[deg]`, 90° for a straight bank). In `Nu_Zukauskas_Bejan`,
`Nu_ESDU_73031` and `Nu_HEDH_tube_bank` the configuration is **derived** from
the pitches, exactly as in `ht`: the bank is staggered when
`|pitch_normal/pitch_parallel − 1| > 0.05`.

Every function carries in its comment block (i) the equation and the tabulated
coefficients, (ii) the validity range **as quoted by `ht`**, (iii) the original
paper or book and (iv) the `ht` module, function, version and commit it was
taken from. The scientific basis is A. Zukauskas, "Heat transfer from tubes in
crossflow", *Advances in Heat Transfer* **8**, 93–160, 1972; A. Bejan,
*Convection Heat Transfer*, 4E, Wiley, 2013; the ESDU data sheets 73031 (1973)
and 86022 (1986) as given in Hewitt, Shires & Bott, *Process Heat Transfer*,
1994; and E. U. Schlünder (ed.), *Heat Exchanger Design Handbook*, Hemisphere,
1987, whose example 3.11 of Baehr & Stephan, *Heat and Mass Transfer*,
Springer, 2013, is used as a demonstration case.

### The seventh `ht` function is not translated

`Nu_Grimison_tube_bank` is **not** translated, because in `ht` it is not a
closed-form correlation: the two tabulated Grimison coefficients `C1` and `m`
are read from a bivariate least-squares spline surface fitted to the digitised
tables (`bisplev` on the pre-generated splines `Grimison_C1_aligned_tck` … of
degrees (3,3) in-line and (1,1) staggered, `ht/conv_tube_bank.py`). Reading
such a table inside an EES `FUNCTION` is the registered gap
`CS-GAP-LOOKUP-PROC` (CoolSolve cannot read a lookup table in a subroutine
body), and reproducing the fitted surface would mean transcribing 16 + 24
spline coefficients and a tensor-product B-spline evaluator. The deviation of
the fitted surface from the published Grimison tables is itself large (checked
with the Python functions: up to 0.72 relative on `C1` and 0.27 on `m` at the
tabulated pitch ratios), and a linear interpolation of the published tables —
the obvious EES transcription — is a **different** function (it returns 86.47
instead of 79.93 at the second `ht` doctest, +8.2%). Shipping a function whose
name says Grimison but whose values differ by that much from the source
library would be misleading, so the family is shipped with six functions; the
Grimison correlation remains a documented exclusion.

## How to run

Open `tube_bank_nusselt.eescode` in the CoolSolve GUI and press *Solve*, or
from a terminal:

```bash
coolsolve ./tube_bank_nusselt.eescode
```

The demonstration program after the definitions calls each of the six functions
twice: once (case *A*) with the input set of the `ht` doctest of the
corresponding correlation, once (case *B*) with a single uniform input set
(Re = 1.2·10⁴, Pr = 0.71, Pr_wall = 0.8, `Do` = 0.025 m, 8 tube rows, transverse
pitch 0.07 m, longitudinal pitch 0.05 m, bank inclined at 60°). It solves
without any iteration (`Solver: SUCCESS (0 iterations)`, every equation is
explicit) and is the regression baseline (`tube_bank_nusselt.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0095 ---}` and
lists `CSL-0095` in its `related` field.

## Results

Values of the demonstration program (full precision in
`tube_bank_nusselt.sol`):

| Quantity (case A) | value [−] | Quantity (case B) | value [−] |
|---|---:|---|---:|
| `Zukauskas_row` (4 staggered rows) | 0.8942 | `Zukauskas_row_B` (8 rows) | 0.9652 |
| `Zukauskas_row_inline` (6 in-line rows) | 0.9465 | `Zukauskas_row_inline_B` | 0.9647 |
| `Nu_Zukauskas_Bejan` (Pr_wall = Pr) | 175.92 | `Nu_Zukauskas_Bejan_B` | 89.510 |
| `Nu_Zukauskas_Bejan_Prwall` (Pr_wall = 5) | 191.36 | `Nu_Zukauskas_Bejan_Prwall_B` | 86.879 |
| `ESDU_row` (4 staggered rows) | 0.8984 | `ESDU_row_B` | 0.9777 |
| `ESDU_row_inline` (6 in-line rows) | 0.9551 | `ESDU_row_inline_B` | 0.9839 |
| `ESDU_angle` (75°) | 0.97941 | `ESDU_angle_B` (60°) | 0.91731 |
| `Nu_ESDU` | 98.256 | `Nu_ESDU_B` (Pr_wall = Pr, 90°) | 92.486 |
| `Nu_HEDH` | 382.46 | `Nu_ESDU_Prwall_angle_B` (Pr_wall = 0.8, 60°) | 82.247 |
| `Nu_HEDH_ex311` (example 3.11 of Baehr & Stephan) | 149.19 | `Nu_HEDH_B` | 140.83 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the three Nu
     correlations and the two row-correction factors over a Reynolds-number sweep
     and a tube-row sweep, e.g. Nu vs Re at Pr = 0.71 for a 8-row staggered air
     bundle, figures/tube_bank_nusselt_nu_re.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_tube_bank.py`, commit `85e0ee6`, installed from the local clone
`~/git/ht` in a throw-away virtual environment under `work/`) for case *A*, plus
values computed with the same Python functions for case *B*. The 20 output
values of the demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
20 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8
```

(the 8 “only in CoolSolve” variables are the 8 inputs of the demonstration
program — `Re_B`, `Pr_B`, `Pr_wall_B`, `Do_B`, `tube_rows_B`,
`pitch_normal_B`, `pitch_parallel_B`, `angle_B` —; the reference table holds
only the 20 outputs). The largest relative deviation over the 20 values is
**2.8·10⁻¹²** (`Nu_Zukauskas_Bejan_A`), i.e. round-off in the double-precision
evaluation; the four table look-ups (`Zukauskas_row*`, `ESDU_row*`) are exact.

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Zukauskas_row_A` | 0.8942 | 0.8942 | 0 |
| `Zukauskas_row_inline_A` | 0.9465 | 0.9465 | 0 |
| `Nu_Zukauskas_Bejan_A` | 175.920227715 | 175.9202277145 | 2.8e-12 |
| `Nu_Zukauskas_Bejan_Prwall_A` | 191.358512959 | 191.3585129586 | 2.1e-12 |
| `ESDU_row_A` | 0.8984 | 0.8984 | 0 |
| `ESDU_row_inline_A` | 0.9551 | 0.9551 | 0 |
| `ESDU_angle_A` | 0.979413908025 | 0.9794139080248 | 2.0e-13 |
| `Nu_ESDU_A` | 98.2563319141 | 98.25633191406 | 4.1e-13 |
| `Nu_HEDH_A` | 382.463655440 | 382.4636554405 | 1.3e-12 |
| `Nu_HEDH_ex311_A` | 149.187352510 | 149.1873525102 | 1.3e-12 |

Case *B* (second input set, computed with the same Python functions):

| Function | `ht` | CoolSolve | Function | `ht` | CoolSolve |
|---|---:|---:|---|---:|---:|
| `Zukauskas_row_B` | 0.9652 | 0.9652 | `Nu_ESDU_B` | 92.4860415953 | 92.48604159533 |
| `Zukauskas_row_inline_B` | 0.9647 | 0.9647 | `Nu_ESDU_Prwall_angle_B` | 82.2466741317 | 82.24667413172 |
| `Nu_Zukauskas_Bejan_B` | 89.5102392384 | 89.51023923841 | `ESDU_row_B` | 0.9777 | 0.9777 |
| `Nu_Zukauskas_Bejan_Prwall_B` | 86.8789989780 | 86.87899897804 | `ESDU_row_inline_B` | 0.9839 | 0.9839 |
| `ESDU_angle_B` | 0.917314754642 | 0.9173147546424 | `Nu_HEDH_B` | 140.827222018 | 140.8272220184 |

All 20 relative deviations are below 2.9·10⁻¹².

Two values of the case *A* set were **not** compared, because they are not
shipped: the two doctests of `Nu_Grimison_tube_bank` (79.0788386601 at
`pitch_normal` = `pitch_parallel` = 0.05 m, 79.9272107857 at 0.07 m) and the
`ht` value of that function (see the section above).

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the crossflow tube-bank correlations of `ht`, the
heat-transfer component of ChEDL, file `ht/conv_tube_bank.py`, functions
`Zukauskas_tube_row_correction`, `Nu_Zukauskas_Bejan`,
`ESDU_tube_row_correction`, `ESDU_tube_angle_correction`, `Nu_ESDU_73031` and
`Nu_HEDH_tube_bank`, version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one EES
`FUNCTION` named after the `ht` function; the tabulated coefficient sets
(Zukauskas row factors, ESDU row factors) became explicit nested `IF` ladders
(CoolSolve cannot read a table inside a `FUNCTION` body, `CS-GAP-LOOKUP-PROC`);
the three regime switches of `Nu_Zukauskas_Bejan` and the three of
`Nu_ESDU_73031` became nested `IF/THEN/ELSE` blocks (the non-smooth switches);
the two Python booleans became 1/0 flags; the optional `Pr_wall` arguments of
`Nu_Zukauskas_Bejan` and `Nu_ESDU_73031` became mandatory (pass `Pr_wall = Pr`
for the form without the correction); `sin(radians(angle))` became
`SIN(angle)` because CoolSolve and EES take trigonometric arguments in
degrees; the constant `pi` became `pi()` because `pi` is not resolved inside a
subprogram body in CoolSolve v0.3.0 (`CS-BUG-PI-FUNCTION`, registered). **No
equation was changed.** Scientific basis per function: the original paper,
data sheet or book quoted in its comment block.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`).

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-104, family `HT-009`).** Six EES
  `FUNCTION`s of the seven of the `ht` family, named after the `ht` function,
  with the formula and the tabulated coefficients, the validity range as quoted
  by `ht`, the original reference and the `ht` module/function/version/commit
  in each comment block. Arguments are the Python arguments, dimensionless or in
  SI (`m`, degrees); no property function is used inside the functions, so the
  calling model passes Re, Pr, Pr_wall, `Do` and the pitches itself (rule 5 of
  `sources/ht/README.md` §7).
- **Decision (documented here, this card has no other place for it):**
  `Nu_Grimison_tube_bank` is **not** translated — it is a fitted spline surface
  in `ht`, not a published closed-form correlation (see the section above);
  the family is therefore shipped with six functions instead of seven, and the
  exclusion is repeated in the file header and in the `HT-009` inventory note.
- `Nu_Zukauskas_Bejan`, `Nu_ESDU_73031`, `Nu_HEDH_tube_bank`: the staggered /
  in-line choice is **derived** inside the function from the two pitches with
  the `IF(a, b, c)` inline conditional of `ht`'s
  `abs(1 - pitch_normal/pitch_parallel) > 0.05`; the regime switches are
  nested `IF/THEN/ELSE` blocks, not a selector function.
- `Zukauskas_tube_row_correction`, `ESDU_tube_row_correction`: the Python
  `staggered` booleans are **1/0 integer flags** (they are arguments of these
  two functions in `ht`); `Re` is an argument of the Zukauskas factor (it
  selects between the two staggered tables, the in-line table does not use it).
  The values are written as constant assignments in the ladder and are exact.
  `ESDU_tube_row_correction` maps 2 rows or fewer onto the 3-row value and 10
  rows or more onto 1, as the Python `if/elif` does.
- `Nu_Zukauskas_Bejan`: `Pr_wall` is mandatory; the demonstration program calls
  the function with `Pr_wall = Pr` (uncorrected, the `ht` doctest) and with
  `Pr_wall = 5` (corrected), so both forms are exercised.
- `Nu_ESDU_73031`: `Pr_wall` is mandatory and the property factor is written
  explicitly as `F1 = (Pr/Pr_wall)^0.26`. In `ht` this factor comes from
  `ht.core.wall_factor` with the heating and cooling coefficients both equal to
  0.26, i.e. the same expression; `wall_factor` itself is a selector of the
  property and the phenomenon and is not translated.
- `Nu_HEDH_tube_bank`: the constant `pi` is written `pi()` (CoolSolve does not
  resolve `pi` inside a subroutine body, `CS-BUG-PI-FUNCTION`, P1 silent);
  the local quantities (`psi`, `Re_psi`, `Nu_laminar`, `Nu_turbulent`,
  `Nu_m`, `f_A`, `f_N`) are the intermediates `ht` computes internally.
- `ESDU_tube_angle_correction`: `SIN` takes degrees in CoolSolve and EES, so
  the Python `sin(radians(angle))**0.6` is written `SIN(angle)^0.6`.
- **Selectors not translated**: none of the six is a selector. The seven
  shell-side pressure-drop and Bell-Delaware functions of the same `ht` module
  (`dP_Kern`, `dP_Zukauskas`, `baffle_correction_Bell`, `baffle_leakage_Bell`,
  `bundle_bypassing_Bell`, `unequal_baffle_spacing_Bell`,
  `laminar_correction_Bell`) belong to inventory family `HT-017`.
- **Level**: equations 28 → 0 points (< 50), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 1 → level 1, moved **+1 to level 2**: the content is a
  curated set of published correlations with regime switches (the same rating
  as the other `ht` families, `HT-001` … `HT-024`, `level_guess = 2` in
  `sources/ht/inventory.csv`).

## Limitations and CoolSolve gaps

- The two demonstration input sets are realistic but do not stay inside every
  quoted validity range; `ht` does not check the ranges in these functions, so
  its values are reproduced as they are. Case *A* uses the published doctest
  inputs, case *B* a uniform air-side set (Re = 1.2·10⁴, Pr = 0.71, 8 rows,
  ST/Do = 2.8, SL/Do = 2): the staggered `Nu_ESDU_73031` range on the
  transverse pitch ratio (1 to 4) and the HEDH range (10 < Re < 10⁵,
  0.6 < Pr < 1000) are respected, the inclination factor F3 is used at 60°,
  inside the 10° limit above which the ESDU angle correction is claimed.
- The `Nu_Grimison_tube_bank` exclusion above is the one correlation of the
  family that is missing.
- The shell-side pressure drop of the same bundle (Kern, Zukauskas) and the
  Bell-Delaware method are **not** in this file: they are inventory family
  `HT-017` (`tube_bank_dp_bell_delaware`).
- **Gaps referenced, none blocking, none newly registered for this card**:
  `CS-FEAT-IMPORT` (`$INCLUDE library:…`, planned), `CS-GAP-LOOKUP-PROC`
  (lookup table inside a `FUNCTION`, already registered — reason of the
  `IF`-ladder transcription), `CS-BUG-PI-FUNCTION` (`pi` inside a subprogram
  body, already registered — worked around with `pi()`, the equations are
  unchanged). Everything else is plain EES (`FUNCTION`, nested `IF/THEN/ELSE`,
  `SIN`, `SQRT`, `EXP`) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0096` *plate_hx_heat_transfer*: the plate-heat-exchanger counterpart
  of this file in the same `ht` triage (corrugated plate channel instead of a
  crossflow tube bundle), same layout and same comment blocks.
- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` family of the library
  and the pattern of this file (one `FUNCTION` per correlation, comment block
  with formula, validity and dual citation, demonstration program, verification
  table); its arguments are pipe dimensionless numbers instead of the bundle
  geometry of this file.
- `CSL-0094` *external_crossflow_cylinder*: the **external** forced-convection
  counterpart (single cylinder in crossflow, 8 functions); a crossflow tube
  bundle combines both, with the row and angle correction factors of this file.
- `CSL-0090` *hx_effectiveness_ntu*: the effectiveness-NTU relations of the
  heat exchanger whose single-stream (crossflow) side uses the Nu of this file.
- `sources/labothappy` LTP-037 (shell-side HTC) and LTP-038 (external tube
  bundles): the LaboThapPy integration of bundle-scale correlations; the `ht`
  family here is the reference for the equations.
- `CSL-0101` *external_forced_conv_plates*: the other **external** forced-convection geometry of the same `ht` module `ht/conv_external.py` (isothermal flat plate in crossflow: Baehr-Stephan and Churchill-Ozoe laminar, Schlichting and Kreith turbulent), same layout.
