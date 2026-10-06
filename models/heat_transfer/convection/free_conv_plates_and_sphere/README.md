# Free convection from plates and a sphere: Nusselt-number correlations

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0093`

Five EES `FUNCTION`s returning the Nusselt number of natural convection from an
isothermal surface — one for a vertical plate (Churchill & Chu 1975), three for a
horizontal plate (McAdams; VDI Heat Atlas 2010, whose buoyancy-enhanced forms are
from Stewartson 1958 and whose lower-surface form is attributed to Schlünder 1987;
Rohsenow, Hartnett & Cho 1998) and one for a sphere (Churchill, as presented in
Schlünder 1987). All of them take dimensionless arguments only (`Pr`, `Gr` and,
for the horizontal plate, the buoyancy flag); the surface heat-transfer
coefficient follows from `h = Nu*k/L_c` and is left to the caller, as in the
source library. This is the free-convection counterpart of `CSL-0087`
(`internal_turbulent_nusselt`) and the plate/sphere complement of `CSL-0092`
(`free_conv_cylinders`), which lives in the same `ht` module and even repeats the
vertical-plate correlation of this model inside its
`Nu_vertical_cylinder_Popiel_Churchill`.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; Pr and Gr are arguments) |
| **Size** | 38 equations after analysis (largest block: 1); 5 functions of 2 to 13 statements |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_free_immersed.py` (MIT); inventory row `HT-007` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (26 values, max deviation 3.4·10⁻¹³) |

## Problem statement

For a given fluid state and geometry (Prandtl number `Pr` and Grashof number `Gr`
on the plate height for a vertical plate, on the characteristic length of the
plate for a horizontal plate, on the diameter for a sphere), compute the Nusselt
number Nu of the surface; multiply it by `k/L_c` to obtain the surface
heat-transfer coefficient. For a horizontal plate, the buoyancy of the plate has
to be stated as well, since a hot plate (heat transfer from its upper surface) and
a cold plate (heat transfer from its lower surface) give different correlations.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity (as quoted in `ht`) |
|---|---|---|---|
| `Nu_vertical_plate_Churchill` | Pr, Gr | Nu = [0.825 + 0.387·Ra^(1/6)/{1+(0.492/Pr)^(9/16)}^(8/27)]² | all Rayleigh numbers; applicable to a vertical cylinder as well if D/L ≥ 35/Gr_L^(1/4) |
| `Nu_horizontal_plate_McAdams` | Pr, Gr, buoyancy | Nu = 0.54·Ra^(1/4) (hot plate, Ra ≤ 1E7), 0.15·Ra^(1/3) (hot plate, Ra > 1E7), 0.27·Ra^(1/4) (cold plate, Ra ≤ 1E10), 0.15·Ra^(1/3) (cold plate, Ra > 1E10) | the four Ra branches; no range given |
| `Nu_horizontal_plate_VDI` | Pr, Gr, buoyancy | Nu = 0.766·(Ra·f2)^0.2 (hot plate, Ra·f2 < 7E4), 0.15·(Ra·f2)^(1/3) (hot plate, above), 0.6·(Ra·f1)^0.2 (cold plate), f2 = {1+(0.322/Pr)^0.55}^(20/11), f1 = {1+(0.492/Pr)^(9/16)}^(−16/9) | the three branches; the lower-surface form is recommended in the laminar regime |
| `Nu_horizontal_plate_Rohsenow` | Pr, Gr, buoyancy | Nu = {Nu_l^10 + Nu_t^10}^(1/10) (hot plate), Nu_l = 1.4/ln{1 + 1.4/Nu_T}, Nu_T = 0.835·Cl·Ra^(1/4), Cl = 0.0972 − (0.0157 + 0.462·C_tV)·t1 + (0.615·C_tV − 0.0548 − 6·10⁻⁶·Pr)·t2, Nu_t = C_tU·Ra^(1/3), C_tU = 0.14·(1 + 0.01707·Pr)/(1 + 0.01·Pr), C_tV = 0.13·Pr^0.22/{1 + 0.61·Pr^0.81}^0.42; Nu = 2.5/ln{1 + 2.5/Nu_T}, Nu_T = 0.527·Ra^0.2/{1+(1.9/Pr)^0.9}^(2/9) (cold plate) | no range given; the lower-surface form is recommended in the laminar regime |
| `Nu_sphere_Churchill` | Pr, Gr | Nu = 2 + 0.589·Ra^0.25/{1+(0.469/Pr)^(9/16)}^(4/9)·{1 + 7.44·10⁻⁸·Ra/{1+(0.469/Pr)^(9/16)}^(16/9)}^(1/12) | Ra < 1E13; Nu → 2 at low Ra |

Arguments: Pr (Prandtl number, `[-]`), Gr (Grashof number, `[-]`, on the length
stated in each comment block) and `buoyancy` (`1` = buoyancy assisted, i.e. a hot
plate with heat transfer from its upper surface — the `ht` default `True`;
`0` = not buoyancy assisted, i.e. a cold plate with heat transfer from its lower
surface). `Ra = Pr·Gr` throughout. In the Rohsenow correlation `t1 = Ah/A`
(heated to non-heated area ratio) and `t2 = Lf·P/A` (vertical distance between the
lowest and the highest point of the body) are the values `ht` uses for a plain
plate, 1 and 0, so the `t2` term of `Cl` vanishes.

Every function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by `ht`**, (iii) the original paper or book and (iv) the `ht`
module, function, version and commit it was taken from. The scientific basis is
Churchill & Chu (1975) for the vertical plate, McAdams's *Heat Transmission*,
the VDI Heat Atlas (2nd ed., 2010) with Stewartson (1958) and Schlünder (1987),
Rohsenow, Hartnett & Cho (1998) for the horizontal plate, and Churchill's
correlation as presented in Schlünder (1987) for the sphere.

Two members of the `ht` family are **not** translated: `Nu_free_vertical_plate`
and `Nu_free_vertical_plate_methods` (and their horizontal counterparts
`Nu_free_horizontal_plate` and `Nu_free_horizontal_plate_methods`) are
dispatchers that map a method name to a correlation; an EES caller calls the
chosen `FUNCTION` directly.

## How to run

Open `free_conv_plates_and_sphere.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./free_conv_plates_and_sphere.eescode
```

The demonstration program after the definitions calls each of the 5 functions at
least once: case *A* reproduces the input set of the `ht` doctest of the
corresponding correlation (the two `_cold` calls and the two `_lowPr` calls
exercise the lower-surface forms and the low-Prandtl set), case *B*
(Pr = 0.7, Gr = 1E4, Ra = 7E3) exercises the **laminar** branches of the
horizontal-plate correlations and case *C* (Pr = 0.71, Gr = 2E10,
Ra = 1.42E10) their **turbulent** branches. It solves without any iteration
(`Solver: SUCCESS (0 iterations)`; the analysis reports `System square: Yes`,
38 equations and 38 variables) and is the regression baseline
(`free_conv_plates_and_sphere.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies the definitions
in a block `{--- Library functions copied from CSL-0093 ---}` and lists
`CSL-0093` in its `related` field.

## Results

Values of the demonstration program (full precision in
`free_conv_plates_and_sphere.sol`), Nu in `[-]`:

| Function | case A (hot) | case A (`_cold`) | case B | case C |
|---|---:|---:|---:|---:|
| `Nu_vertical_plate_Churchill` | 147.16 | – | 5.03 | 281.89 |
| `Nu_horizontal_plate_McAdams` | 181.73 | 55.45 | 4.94 | 363.23 |
| `Nu_horizontal_plate_VDI` | 203.90 | 39.17 | 5.40 | 491.55 |
| `Nu_horizontal_plate_Rohsenow` | 175.91 | 35.96 | 2.69 | 44.24 |
| `Nu_sphere_Churchill` | 25.67 | – | 6.15 | 259.13 |

The case *A* values are the published `ht` doctest values. The two
`Nu_horizontal_plate_McAdams` calls of case *A_lowPr` (Pr = 0.01, Gr = 3.21E8,
Ra = 3.21E6) give 22.86 (hot) and 11.43 (cold); with case *B* (Ra = 7E3) they are
the only two sets of the demonstration program inside the laminar branch of the
buoyancy-assisted McAdams form. In case *C* the hot and the cold McAdams calls
give the same value (363.23) because both fall in the turbulent branch, whose two
forms are identical (0.15·Ra^(1/3)).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the five
     correlations over a Rayleigh-number sweep at Pr = 0.71 (Nu vs Ra), with the
     hot/cold plates shown separately and the regime transitions of the
     McAdams and VDI forms,
     figures/free_conv_plates_and_sphere_nu_ra.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_free_immersed.py`, commit `85e0ee6`, installed from the local clone in
a throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for cases *B* and *C*. The 26 output values of the
demonstration program were compared with
`CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
26 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 12
```

(the 12 “only in CoolSolve” variables are the 12 inputs of the demonstration
program — `Pr_A_plate`, `Gr_A_plate`, `Pr_A_horiz`, `Gr_A_horiz`, `Pr_A_lowPr`,
`Gr_A_lowPr`, `Pr_A_sphere`, `Gr_A_sphere` and `Pr_B`, `Gr_B`, `Pr_C`, `Gr_C` —
the reference table holds only the 26 outputs). The largest relative deviation
over the 26 values is **3.4·10⁻¹³**
(`Nu_horizontal_plate_McAdams_A_lowPr_cold`), i.e. round-off in the
double-precision evaluation.

Per-value results, `ht` / CoolSolve (case *A*, the published doctest values):

| Function | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Nu_vertical_plate_Churchill_A` | 147.161852238 | 147.161852238 | 4.1e-14 |
| `Nu_horizontal_plate_McAdams_A` | 181.731212744 | 181.731212744 | 2.5e-13 |
| `Nu_horizontal_plate_McAdams_A_cold` | 55.445647994 | 55.445647994 | 3.1e-14 |
| `Nu_horizontal_plate_McAdams_A_lowPr` | 22.857041558 | 22.857041558 | 1.0e-13 |
| `Nu_horizontal_plate_McAdams_A_lowPr_cold` | 11.428520779 | 11.428520779 | 3.4e-13 |
| `Nu_horizontal_plate_VDI_A` | 203.896812249 | 203.896812249 | 1.2e-13 |
| `Nu_horizontal_plate_VDI_A_cold` | 39.168649715 | 39.168649715 | 9.8e-14 |
| `Nu_horizontal_plate_Rohsenow_A` | 175.910547163 | 175.910547163 | 1.6e-13 |
| `Nu_horizontal_plate_Rohsenow_A_cold` | 35.957992449 | 35.957992449 | 4.0e-15 |
| `Nu_sphere_Churchill_A` | 25.670869440 | 25.670869440 | 9.4e-14 |

Cases *B* and *C* (computed with the same Python functions, so they check the
branches that the doctests do not reach):

| Function | case B `ht` | case B CoolSolve | case C `ht` | case C CoolSolve |
|---|---:|---:|---:|---:|
| `Nu_vertical_plate_Churchill` | 5.028408941 | 5.028408941 | 281.888038664 | 281.888038664 |
| `Nu_horizontal_plate_McAdams` | 4.939332584 | 4.939332584 | 363.234736501 | 363.234736501 |
| `Nu_horizontal_plate_McAdams_…_cold` | 2.469666292 | 2.469666292 | 363.234736501 | 363.234736501 |
| `Nu_horizontal_plate_VDI` | 5.402109720 | 5.402109720 | 491.552887558 | 491.552887558 |
| `Nu_horizontal_plate_VDI_…_cold` | 2.849004941 | 2.849004941 | 52.081704118 | 52.081704118 |
| `Nu_horizontal_plate_Rohsenow` | 2.691266278 | 2.691266278 | 340.708864099 | 340.708864099 |
| `Nu_horizontal_plate_Rohsenow_…_cold` | 3.450747061 | 3.450747061 | 44.236347569 | 44.236347569 |
| `Nu_sphere_Churchill` | 6.150727223 | 6.150727223 | 259.129669300 | 259.129669300 |

All 26 relative deviations are below 3.4·10⁻¹³. The branches really exercised are
the ones claimed above: Ra = 5.54·3.21E8 = 1.778E9 for the case *A* horizontal
inputs (above the 1E7 switch of the hot McAdams form, below the 1E10 switch of the
cold one) with Ra·f2 = 1.778E9·1.4124 = 2.512E9 > 7E4, i.e. the turbulent VDI
form; Ra = 7E3 with Ra·f2 = 1.744E4 < 7E4 in case *B*, the laminar VDI form; and
Ra = 0.71·2E10 = 1.42E10 in case *C*, on the turbulent side of both McAdams
switches.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language CoolSolve
reads) of the free-convection plate and sphere correlations of `ht`, the
heat-transfer component of ChEDL, file `ht/conv_free_immersed.py`, functions
`Nu_vertical_plate_Churchill`, `Nu_horizontal_plate_McAdams`,
`Nu_horizontal_plate_VDI`, `Nu_horizontal_plate_Rohsenow` and
`Nu_sphere_Churchill`, version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one EES
`FUNCTION` named after the `ht` function, the Python boolean `buoyancy` became
the mandatory integer argument `buoyancy` (1 = `True`, the `ht` default;
0 = `False`) since EES has no boolean type and no optional argument, the
non-smooth regime switches use EES `IF`, and the Python `log` became the EES `LN`
in the two Rohsenow forms. No equation was changed. Scientific basis per
function: the original paper or book quoted in its comment block.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`); the same module also gives
the cylinder correlations of `CSL-0092`.

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-102, family `HT-007`).** One EES
  `FUNCTION` per `ht` correlation (5 functions), named `Nu_<method>`, with the
  formula, the validity range as quoted by `ht`, the original reference and the
  `ht` module/function/version/commit in the comment block. Arguments are the
  Python arguments, all dimensionless; no property function is used inside the
  functions, so the calling model passes Pr and Gr itself (rule 5 of
  `sources/ht/README.md` §7).
- The boolean `buoyancy` of the three horizontal-plate correlations is a
  **two-state integer argument**: `1` for `ht`'s `True` (hot plate, upper-surface
  forms, the default) and `0` for `False` (cold plate, lower-surface form). EES
  has neither booleans nor optional arguments, so every call must state the
  buoyancy; the demonstration program calls each of the three correlations with
  both values in all three cases (cases *A*, *A_cold*, *B*, *C*), which is what
  exercises every branch and makes the 26-value verification possible.
- `Nu_horizontal_plate_McAdams`: its four forms are selected by two nested
  switches (hot/cold, then Ra); a local integer `sel` (0…3) holds the branch, as
  in `CSL-0092` for its `turbulent` flag. The two turbulent forms of McAdams are
  written once in the EES code because they are the same expression (0.15·Ra^(1/3)).
- `Nu_horizontal_plate_Rohsenow`: the local variables `t1`, `t2`, `C_tU`, `C_tV`,
  `Cl`, `Nu_T`, `Nu_l`, `Nu_t` and `m` of `ht` are kept as such, including `t1 = 1`
  and `t2 = 0`, which `ht` sets for a plain plate; the `t2` term of `Cl` is
  therefore identically zero, as in the source.
- **Selectors not translated**: `Nu_free_vertical_plate`,
  `Nu_free_vertical_plate_methods`, `Nu_free_horizontal_plate` and
  `Nu_free_horizontal_plate_methods` only map a method name to a correlation; the
  caller chooses the `FUNCTION` directly.
- `Nu_vertical_plate_Churchill` is not duplicated inside `CSL-0092`: that model's
  `Nu_vertical_cylinder_Popiel_Churchill` repeats its three equations inline (as
  documented in its conversion log), so the function names stay unique across the
  library.
- **Level**: equations 38 → 0 points (< 50), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 1 → **level 1** by the table, moved up by one to **level
  2** for consistency with the five other `ht` function libraries of the same
  family and intent (`CSL-0087`, `CSL-0088`, `CSL-0089`, `CSL-0090`,
  `CSL-0092`), whose demonstration programs are of the same size: a correlation
  library is rated by its correlations and regime logic, not by the length of
  its demonstration program.

## Limitations and CoolSolve gaps

- The three demonstration input sets are chosen to be realistic and to exercise
  every branch of the horizontal-plate correlations, not to give a design value:
  `ht` quotes no Rayleigh-number range at all for McAdams and Rohsenow,
  recommends the lower-surface (cold-plate) forms of VDI and Rohsenow in the
  laminar regime, and **none** of the five functions checks its range, so its
  values are reproduced as they are. The numbers of the *Results* and
  *Verification* tables are therefore a check of the **equations**, not
  recommended design values; the validity column of the table above is the one to
  use when choosing an input.
- Three of the correlations are **discontinuous** at a Rayleigh number: the
  branch changes at a fixed value and the two forms do not join. Evaluated on the
  two forms themselves (with `ht`), the jump from the laminar to the turbulent
  branch is +6.4 % for the buoyancy-assisted McAdams form at Ra = 1E7
  (30.37 → 32.32), +278 % for the cold-plate McAdams form at Ra = 1E10
  (85.38 → 323.2), and −13.3 % for the buoyancy-assisted VDI form at
  Ra·f2 = 7E4 (7.13 → 6.18). This is a property of the original correlations,
  reproduced as in `ht`, not of the translation; away from the switch the two
  McAdams branches diverge (at Ra = 1E10 the turbulent form is 3.8 times the
  laminar one). A sweep of Ra through a transition therefore shows a jump — these
  correlations are not meant to be used that close to it. The Rohsenow forms of
  the hot plate are continuous: its two branches are combined by a tenth-power
  mean.
- The buoyancy flag is not a regime switch but a **change of geometry**: the two
  values of the three horizontal-plate functions are heat transfer from the upper
  and from the lower face of the plate, not two branches of one regime, so there
  is no reason for them to agree anywhere. At low Ra the two Rohsenow faces even
  cross (case *B*, Ra = 7E3: 2.69 on the hot plate, 3.45 on the cold one) because
  they are different expressions with different constants.
- No property calls are made: Pr and Gr are arguments, so a model using these
  functions must evaluate them itself (`Gr = g·|ρ_∞ − ρ_s|·L³/(μ²)` in its own SI
  variables). The characteristic length of the horizontal plate is the caller's
  choice; the VDI and Rohsenow docstrings suggest `L = a·b/{2·(a+b)}` for a
  rectangle of length `a` and width `b`.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No gap registered for this card: everything is plain EES (`FUNCTION`, nested
  `IF/THEN/ELSE`, `LN`, `^`) and runs in CoolSolve v0.3.0 (`System square: Yes`,
  0 solver iterations).

## Related models

- `CSL-0092` *free_conv_cylinders*: the cylinder family of the same `ht` module
  and the closest neighbour; its `Nu_vertical_cylinder_Popiel_Churchill` repeats
  the vertical-plate correlation of this model (`Nu_vertical_plate_Churchill`)
  inline, and its `Nu_horizontal_cylinder_Churchill_Chu` is the cylinder
  counterpart of the same 1975 paper.
- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` function library
  (internal turbulent convection, 23 `FUNCTION`s) and the layout followed here.
- `CSL-0065` *cooling_tower_condenser_water* and `CSL-0076`
  *cooling_tower_direct_contact_refsim*: natural convection on the surfaces of a
  cooling tower; they use their own formulas, so they are a cross-check only.
- `sources/labothappy` LTP-035 and ThermoCycle THC-011: plate
  heat-transfer coefficients, other geometries and other assumptions.

- `CSL-0094` *external_crossflow_cylinder*: the forced-convection (crossflow)
  cylinder correlations of the same `ht` layout, 8 functions; the counterpart
  of the natural-convection cylinder family `CSL-0092`.
- `CSL-0100` *free_conv_enclosed_and_jackets*: the enclosed-plate,
  helical-coil and vessel-jacket correlations of the same `ht` layout
  (10 functions), the counterpart of the free convection of *immersed* plates.
- `CSL-0101` *external_forced_conv_plates*: the other **external** forced-convection geometry of the same `ht` module `ht/conv_external.py` (isothermal flat plate in crossflow: Baehr-Stephan and Churchill-Ozoe laminar, Schlichting and Kreith turbulent), same layout.
