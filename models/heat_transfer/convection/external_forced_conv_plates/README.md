# External forced convection over a flat plate

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0101`

Four EES `FUNCTION`s returning the average Nusselt number of an **isothermal
flat plate** in crossflow at constant surface temperature: two laminar forms
(Baehr-Stephan, piecewise in the Prandtl number, and Churchill-Ozoe, one
equation for the whole range) and two fully turbulent forms (Schlichting and
Kreith). The arguments are dimensionless (`Re` on the plate length and `Pr` at
the bulk temperature); the average heat-transfer coefficient follows from
`h = Nu·k/L` and is left to the caller, as in the source library. This is the
plate counterpart of `CSL-0094` *external_crossflow_cylinder* (same source
module `ht/conv_external.py`, same layout), of `CSL-0087`
*internal_turbulent_nusselt* (internal forced convection) and of the
free-convection plate correlations of `CSL-0093`.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; Re and Pr are arguments) |
| **Size** | 19 equations after analysis (largest block: 1); 4 functions of 1 code line each, except `Nu_horizontal_plate_laminar_Baehr` (nested `IF` blocks, the selection of its four Prandtl branches) |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_external.py` (MIT); inventory row `HT-015` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (13 values, max deviation 2.5·10⁻¹³) |

## Problem statement

For a fluid in crossflow over a flat plate of length `L` — a wing, a ship hull,
a flat heating surface, the leading edge of a finned tube bundle — compute the
average Nusselt number Nu on `L` from the plate-length Reynolds number Re and
the bulk Prandtl number Pr; multiply it by `k/L` to obtain the average
heat-transfer coefficient. Four correlations of the family are available, two
for a laminar boundary layer and two for a turbulent one, each with its own data
basis; the choice between them, and the choice of the laminar or the turbulent
branch, is left to the user, who knows the fluid, the geometry and the regime.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `Nu_horizontal_plate_laminar_Baehr` | Re, Pr | Nu_L = 1.128·(Re·Pr)^0.5 for Pr < 0.005; (Re·Pr)^0.5 for Pr < 0.05; 0.664·Re^0.5·Pr^(1/3) for Pr < 10; 0.678·Re^0.5·Pr^(1/3) otherwise | laminar; the four Prandtl branches above; free convection over the plate is not accounted for |
| `Nu_horizontal_plate_laminar_Churchill_Ozoe` | Re, Pr | Nu_L = 0.6774·Re^0.5·Pr^(1/3) / [1 + (0.0468/Pr)^(2/3)]^0.25 | laminar; a single equation covers all Prandtl numbers, no limit quoted; free convection not accounted for |
| `Nu_horizontal_plate_turbulent_Schlichting` | Re, Pr | Nu_L = 0.037·Re^0.8·Pr / {1 + 2.443·Re^(−0.1)·(Pr^(2/3) − 1)} | turbulent only; no limit quoted; free convection not accounted for |
| `Nu_horizontal_plate_turbulent_Kreith` | Re, Pr | Nu_L = 0.036·Re^0.8·Pr^(1/3) | turbulent only (as in the original); no limit quoted; free convection not accounted for |

Arguments: `Re` (Reynolds number on the plate length `L`, with the bulk fluid
properties, `[-]` — the plate length does not appear explicitly, it enters
through Re) and `Pr` (Prandtl number at the **bulk temperature**, `[-]`), both
mandatory. No other wall correction is necessary for these formulations, and no
length or property appears in the argument list: the calling model passes Re and
Pr (`sources/ht/README.md` §7 rule 5).

Every function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by `ht`**, (iii) the original paper or book and (iv) the `ht`
module, function, version and commit it was taken from. The plate is isothermal
in all four correlations (constant surface temperature), as stated by `ht`.

**Not translated — the selectors of the module.** `Nu_external_horizontal_plate`
and `Nu_external_horizontal_plate_methods` only map a method name ("Baehr",
"Churchill Ozoe", "Schlichting", "Kreith") to one of the four functions above and
return a list of applicable names; the dictionaries
`conv_horizontal_plate_laminar_methods`, `conv_horizontal_plate_turbulent_methods`
and `conv_horizontal_plate_methods` hold those same four functions. An EES caller
calls the chosen `FUNCTION` directly. The constant
`LAMINAR_TRANSITION_HORIZONTAL_PLATE = 5E5` of `ht` (the Reynolds number at
which the selector switches from the laminar to the turbulent method) is a
property of the *calling* model, not a correlation; it is not translated either.

## How to run

Open `external_forced_conv_plates.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./external_forced_conv_plates.eescode
```

The demonstration program after the definitions calls each of the 4 functions:
case *A* reproduces the input sets published by `ht` — the doctest of
`conv_external.py` for each correlation and the four Prandtl branches of the
`tests/test_conv_external.py` regression test of `Nu_horizontal_plate_laminar_Baehr`
(Pr = 10⁻⁴, 0.1, 1 and 100 at Re = 10⁵, plus the doctest Pr = 0.7), to which one
computed call at Pr = 0.01 is added so that **all four Prandtl branches** of that
correlation are exercised (0.005 ≤ Pr < 0.05 is not covered by a published
value) — and case *B* is a single uniform input set (Re = 5·10⁶, Pr = 0.7: air in
crossflow over a plate). It solves without any iteration (`Solver: SUCCESS (0 iterations)`, every
equation is explicit) and is the regression baseline
(`external_forced_conv_plates.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0101 ---}` and
lists `CSL-0101` in its `related` field.

## Results

Values of the demonstration program (full precision in
`external_forced_conv_plates.sol`):

| Quantity | Nu [−] |
|---|---:|
| `Nu_horizontal_plate_laminar_Baehr_A_Pr_1e_4` (Pr = 10⁻⁴) | 3.5670 |
| `Nu_horizontal_plate_laminar_Baehr_A_Pr_0p01` (Pr = 0.01) | 31.6228 |
| `Nu_horizontal_plate_laminar_Baehr_A_Pr_0p1` (Pr = 0.1) | 97.4619 |
| `Nu_horizontal_plate_laminar_Baehr_A_Pr1` (Pr = 1) | 209.9752 |
| `Nu_horizontal_plate_laminar_Baehr_A_Pr100` (Pr = 100) | 995.1679 |
| `Nu_horizontal_plate_laminar_Baehr_A` (Re = 10⁵, Pr = 0.7) | 186.4379 |
| `Nu_horizontal_plate_laminar_Churchill_Ozoe_A` (Re = 10⁵, Pr = 0.7) | 183.0860 |
| `Nu_horizontal_plate_turbulent_Schlichting_A` (Re = 10⁵, Pr = 0.7) | 309.6200 |
| `Nu_horizontal_plate_turbulent_Kreith_A` (Re = 1.03·10⁶, Pr = 0.71) | 2074.8740 |
| `Nu_horizontal_plate_laminar_Baehr_B` (Re = 5·10⁶, Pr = 0.7) | 1318.3147 |
| `Nu_horizontal_plate_laminar_Churchill_Ozoe_B` (Re = 5·10⁶, Pr = 0.7) | 1294.6136 |
| `Nu_horizontal_plate_turbulent_Schlichting_B` (Re = 5·10⁶, Pr = 0.7) | 6658.2319 |
| `Nu_horizontal_plate_turbulent_Kreith_B` (Re = 5·10⁶, Pr = 0.7) | 7308.7737 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the four correlations
     over a Reynolds-number sweep, e.g. Nu vs Re_L at Pr = 0.7 from Re = 1E4 to 1E7 with
     the ht laminar-turbulent transition Re_L = 5E5 marked,
     figures/external_forced_conv_plates_nu_re.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_external.py`, commit `85e0ee6`), the four **regression values of
`ht/tests/test_conv_external.py`** for `Nu_horizontal_plate_laminar_Baehr`, plus
values computed with the same Python functions for case *B* and for the fifth
call of `Nu_horizontal_plate_laminar_Baehr` (the local clone `pip install`ed in a
throw-away virtual environment under `work/`). The 13 output values of the
demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
13 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 6
```

(the 6 “only in CoolSolve” variables are the 6 inputs of the demonstration
program — `Re_A`, `Pr_A`, `Re_Kreith_A`, `Pr_Kreith_A`, `Re_B`, `Pr_B` —; the
reference table holds only the 13 outputs). The largest relative deviation over
the 13 values is **2.5·10⁻¹³** (`Nu_horizontal_plate_laminar_Baehr_B`), i.e.
round-off in the double-precision evaluation.

Per-function values, `ht` / CoolSolve:

| Function | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Nu_horizontal_plate_laminar_Baehr_A_Pr_1e_4` | 3.567049200670 | 3.5670492007 | 1.9e-14 |
| `Nu_horizontal_plate_laminar_Baehr_A_Pr_0p01` | 31.622776601684 | 31.6227766017 | 1.2e-13 |
| `Nu_horizontal_plate_laminar_Baehr_A_Pr_0p1` | 97.461871370105 | 97.4618713701 | 4.7e-14 |
| `Nu_horizontal_plate_laminar_Baehr_A_Pr1` | 209.975236635180 | 209.9752366352 | 9.3e-14 |
| `Nu_horizontal_plate_laminar_Baehr_A_Pr100` | 995.167903447763 | 995.1679034478 | 3.7e-14 |
| `Nu_horizontal_plate_laminar_Baehr_A` | 186.437852875226 | 186.4378528752 | 1.4e-13 |
| `Nu_horizontal_plate_laminar_Churchill_Ozoe_A` | 183.086007825914 | 183.0860078259 | 7.7e-14 |
| `Nu_horizontal_plate_turbulent_Schlichting_A` | 309.620048541267 | 309.6200485413 | 1.1e-13 |
| `Nu_horizontal_plate_turbulent_Kreith_A` | 2074.874007041112 | 2074.8740070410 | 5.4e-14 |
| `Nu_horizontal_plate_laminar_Baehr_B` | 1318.314700379323 | 1318.3147003790 | 2.5e-13 |
| `Nu_horizontal_plate_laminar_Churchill_Ozoe_B` | 1294.613576740772 | 1294.6135767410 | 1.8e-13 |
| `Nu_horizontal_plate_turbulent_Schlichting_B` | 6658.231920432900 | 6658.2319204330 | 1.5e-14 |
| `Nu_horizontal_plate_turbulent_Kreith_B` | 7308.773741220860 | 7308.7737412210 | 1.9e-14 |

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the forced-convection-over-a-flat-plate correlations of
`ht`, the heat-transfer component of ChEDL, file `ht/conv_external.py`, functions
`Nu_horizontal_plate_laminar_Baehr`, `Nu_horizontal_plate_laminar_Churchill_Ozoe`,
`Nu_horizontal_plate_turbulent_Schlichting` and
`Nu_horizontal_plate_turbulent_Kreith`, version 1.2.0, commit 85e0ee6
(2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; each correlation became one EES
`FUNCTION` named after the `ht` function, and the Python `if/elif/else` chain of
`Nu_horizontal_plate_laminar_Baehr` became nested EES `IF` blocks (the four
Prandtl branches are a non-smooth regime switch, so no single closed form
reproduces them). No equation was changed. Scientific basis per function: the
original paper or book quoted in its comment block.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`).

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-110, family `HT-015`).** One EES
  `FUNCTION` per `ht` correlation (4 functions), named as in `ht`, with the
  formula, the validity range as quoted by `ht`, the original reference and the
  `ht` module/function/version/commit in the comment block. Arguments are the
  Python arguments `Re` and `Pr`, both dimensionless; no property function is
  used inside a function, so the calling model passes Re and Pr itself (rule 5
  of `sources/ht/README.md` §7). The module is otherwise identical to that of
  `CSL-0094` (same `ht` file), so the two models share the layout and the
  comment-block convention.
- `Nu_horizontal_plate_laminar_Baehr`: the Prandtl branch limits are those of
  the **`ht` code** (`Pr < 0.005`, `< 0.05`, `< 10`), which is what reproduces
  its published values; its docstring quotes `0.6 < Pr < 10` for the 0.664
  equation (as in the original). The discrepancy is noted in the function
  comment. The four branches are written with nested `IF` blocks (the library
  convention for a non-smooth switch, `CSL-0094`), the function value being
  assigned in each branch; the alternative (a local variable plus a final
  assignment) gives the same numbers.
- **Selectors not translated**: `Nu_external_horizontal_plate`,
  `Nu_external_horizontal_plate_methods` and the three `conv_horizontal_plate_*_methods`
  dictionaries only map a method name to a correlation of this file; the
  transition constant `LAMINAR_TRANSITION_HORIZONTAL_PLATE = 5E5` belongs to the
  calling model.
- The variable names of the demonstration program cannot contain `.` or `-`
  (EES names are letters, digits and `_`; CoolSolve rejects them too — see the
  register entry `CS-GAP-NAME-SYMBOL`), so the four Baehr branches are named
  `..._A_Pr_1e_4`, `..._A_Pr_0p1`, `..._A_Pr1` and `..._A_Pr100`; the Prandtl
  numbers themselves are the constant arguments of the calls.
- **Level**: equations 19 → 0 points (< 50), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 1 → **level 1**; raised to **level 2** (± 1,
  docs/taxonomy.md §3), the reading of the other `ht` function libraries of the
  library (`CSL-0087`, `CSL-0088`, `CSL-0092`, `CSL-0093`, `CSL-0094`), since
  the user has to know four data bases, validity ranges and two flow regimes to
  pick a correlation.
- `stats.n_equations = 19`: the `coolsolve` analysis of the whole file reports
  `Equations: 19`, `Variables: 19`, `System square: Yes`, `Largest block: 1`.
  The file is written directly in the model folder and solves with the guessed
  values of its own inputs, so no `.initials` file is needed.

## Limitations and CoolSolve gaps

- The demonstration input sets are chosen to be realistic, not to stay inside
  every quoted validity range: in case *B* (Re = 5·10⁶ > the `ht` transition
  value 5·10⁵) the two **laminar** correlations are evaluated well above their
  range, as `ht` does not check the ranges; the two turbulent correlations are
  the ones to use there. The numbers of the *Results* and *Verification* tables
  are a check of the **equations**, not recommended design values; the validity
  column of the table above is the one to use when choosing an input.
- These are **fully developed, isothermal-plate** correlations: they give the
  average coefficient over the length `L` (or over a distance `x ≤ L`, with
  `Re_x`), not a local distribution, and they ignore the contribution of free
  convection, which `ht` notes can increase the convection substantially.
- No laminar/turbulent combined correlation is provided: `ht` has none either
  (the two turbulent forms are already fully turbulent from the leading edge);
  a calling model that needs the mixed boundary layer combines the two branches
  itself at `Re_L = 5E5`.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No gap registered for this card: everything is plain EES
  (`FUNCTION`, nested `IF/THEN/ELSE`) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0094` *external_crossflow_cylinder*: the **external** forced-convection
  family of the same `ht` module (`ht/conv_external.py`, single cylinder in
  crossflow, Zukauskas, Churchill-Bernstein, Sanitjai-Goldstein, Fand, McAdams,
  Whitaker, Perkins-Leppert 1962 and 1964), same layout and same comment blocks;
  a flat plate and a cylinder are the two elementary external geometries.
- `CSL-0087` *internal_turbulent_nusselt*: the **internal** forced-convection
  counterpart of this file (23 turbulent and turbulent-entry in-tube Nusselt
  correlations), same layout.
- `CSL-0095` *tube_bank_nusselt*: the tube-bank Nu of the same `ht` triage (the
  row and inclination correction factors applied to the single-cylinder Nu of
  `CSL-0094`); the flat-plate correlations of this file apply to the
  leading-edge region of a crossflow bundle.
- `CSL-0093` *free_conv_plates_and_sphere* and `CSL-0092`
  *free_conv_cylinders*: the free-convection plate and cylinder correlations
  (same geometry, Gr instead of Re); `ht` notes that free convection can
  increase the convection over a plate substantially.
- `CSL-0100` *free_conv_enclosed_and_jackets* and `CSL-0089`
  *condensation_film*: the other `ht` convection families of the library, same
  layout (definitions + demonstration program).
