# Conduction: thermal resistances, shape factors and R-value conversions

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0106`

Fourteen conduction relations of the Python library `ht`: the plane-wall
resistance conversions (`R_to_k`, `k_to_R`), the thermal-resistivity
conversions, the **R-value ↔ k** conversions (SI `m²·K/(W·inch)` and imperial
`ft²·°F·h/(Btu·inch)`), the cylindrical-wall resistance, the six **isothermal
shape factors** (sphere to plane, pipe to plane, pipe normal to a plane, pipe
to pipe, pipe between two planes, eccentric pipe in pipe) and the layered
**cylindrical-wall heat transfer** with inner and outer convection
coefficients (a `PROCEDURE`, two layers). This is the twelfth of the 24 `ht`
families (roadmap cards C-96…C-119); it follows the layout set by `CSL-0087`:
one `FUNCTION` per relation, a comment block with the formula, the validity
range and the dual citation, and a demonstration program calling every
function.

| | |
|---|---|
| **Category** | Heat transfer › Conduction |
| **Fluids** | none (pure conduction; no property call) |
| **Size** | 129 equations after analysis (largest block: 10, the `PROCEDURE` call); 13 functions + 1 procedure |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conduction.py` (MIT); inventory row `HT-020` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the books cited per function (Bergman/Lavine/Incropera/DeWitt, Kreith/Manglik/Bohn, VDI Heat Atlas, Sunderland & Johnson); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (50 values, max deviation 8.0·10⁻¹¹) |

## Problem statement

Given a geometry (wall, cylinder, buried pipe, sphere), a conductivity `k`
and the boundary temperatures, compute either the thermal resistance `R`
(`Q = ΔT/R`) or the conduction shape factor `S` (`Q = S·k·ΔT`,
`R_shape = 1/(S·k)`), plus the practical unit conversions of building
physics: resistance ↔ conductivity and R-value ↔ conductivity, in SI and
imperial R-value conventions. The last function assembles the full
cylindrical-wall problem (inner and outer convection + two solid layers) and
returns the heat rate, the overall coefficients and the temperature profile.

## Model

| EES `FUNCTION`/`PROCEDURE` | Arguments | Equation | Validity (as quoted in `ht`) | Original |
|---|---|---|---|---|
| `R_to_k` | R [K/W], t [m], A [m²] | k = t/(A·R) | none quoted | Bergman et al., *Introduction to Heat Transfer*, 6E, Wiley, 2011 |
| `k_to_R` | k [W/m-K], t [m], A [m²] | R = t/(k·A) | none quoted | idem |
| `k_to_thermal_resistivity` | k [W/m-K] | r = 1/k | none quoted | VDI Heat Atlas, 2E, Springer, 2010 |
| `thermal_resistivity_to_k` | r [m-K/W] | k = 1/r | none quoted | idem |
| `R_value_to_k` | R_value [m²-K/(W-inch)] or [ft²-°F-h/(Btu-inch)], SI flag | k = 1/r, r = R_value/0.0254 (SI) or R_value·6.933471798515978 (imperial) | none quoted | idem |
| `k_to_R_value` | k [W/m-K], SI flag | R_value = (1/k)·0.0254 (SI) or (1/k)/6.933471798515978 | none quoted | idem |
| `R_cylinder` | Di, Do, L [m], k [W/m-K] | R = ln(Do/Di)/(2π·L·k) [K/W] | none quoted | Bergman et al. 2011 |
| `S_isothermal_sphere_to_plane` | D, Z [m] | S = 2π·D/(1 − D/(4Z)) [m] | none | Kreith, Manglik & Bohn, *Principles of Heat Transfer*, Cengage, 2010; Bergman et al. 2011 |
| `S_isothermal_pipe_to_plane` | D, Z, L [m] | S = 2π·L/acosh(2Z/D) | L >> D | idem |
| `S_isothermal_pipe_normal_to_plane` | D, L [m] | S = 2π·L/ln(4L/D) | L >> D | idem |
| `S_isothermal_pipe_to_isothermal_pipe` | D1, D2, W, L [m] | S = 2π·L/acosh[(4W² − D1² − D2²)/(2·D1·D2)] | L >> W, L >> both D | idem |
| `S_isothermal_pipe_to_two_planes` | D, Z, L [m] | S = 2π·L/ln[8Z/(π·D)] | L >> D, L >> Z | Sunderland & Johnson, ASHRAE Trans. 70, 1964; Bergman et al. 2011 |
| `S_isothermal_pipe_eccentric_to_isothermal_pipe` | D1, D2, Z, L [m] | S = 2π·L/acosh[(D2² + D1² − 4Z²)/(2·D1·D2)] | L >> both D, D2 > D1 | Kreith, Manglik & Bohn 2010; Bergman et al. 2011 |
| `cylindrical_heat_transfer` (`PROCEDURE`) | Ti, To [°C], hi, ho [W/m²-K], Di [m], t1, t2 [m], k1, k2 [W/m-K] | see below | none quoted (helper) | standard layered cylindrical-wall result; `ht` gives no reference |

Shape factors are used with `Q = S·k·(T1 − T2)` (`R_shape = 1/(S·k)`); `Z` is
the axis/centre distance to the plane(s) or between the pipe axes; `L = 1 m`
gives the per-metre factor used with some sources (the `ht` default), as in
the original.

`cylindrical_heat_transfer`, on a 1 m length basis (as in `ht`), with
`D_ext = Di + 2·(t1 + t2)`:

- `R1 = 0.5·D_ext·ln(Do1/Di)/k1`, `R2 = 0.5·D_ext·ln(Do2/Do1)/k2` [m²-K/W],
  used as `q·Ri` = layer temperature drop;
- `U_outer = 1/[(D_ext/Di)/hi + R1 + R2 + 1/ho]` [W/m²-K];
- `UA = π·D_ext·U_outer` [W/K], `Q = UA·(Ti − To)` [W],
  `q_ext = Q/(π·D_ext)` [W/m²], `U_inner = UA/(π·Di)` [W/m²-K];
- `To1 = Ti`, `To2`, `To3` = temperatures at the outside of each layer [°C].

A single layer is `t2 = 0`. The `ht` helper takes a Python list of layers and
its docstring gives `Rs` in m·K/W and `q` in W/m³; its **code and doctest**
produce the quantities written above (see the conversion log).

## How to run

```bash
coolsolve ./conduction_resistances_and_shapes.eescode
```

The demonstration program after the definitions calls each of the 13
functions twice and the procedure twice: once (case *A*) with the input set
of the `ht` doctest of the corresponding function, once (case *B*) with a
second, uniform input set (an insulated pipe: 3 mm steel + 40 mm insulation
on a 50 mm inner diameter; plus the same conversions with other values, and
the shape factors at field-scale distances). It solves in 4 iterations
(the `PROCEDURE` block; everything else is explicit) and is the regression
baseline (`conduction_resistances_and_shapes.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these relations copies their
definitions in a block `{--- Library functions copied from CSL-0106 ---}` and
lists `CSL-0106` in its `related` field.

## Results

Values of the demonstration program (full precision in
`conduction_resistances_and_shapes.sol`):

| Quantity (case A) | Value | Quantity (case B) | Value |
|---|---:|---|---:|
| `R_to_k` [W/m-K] | 0.5 | `R_to_k` (A = 2.5 m²) | 0.0222222 |
| `k_to_R` [K/W] | 0.05 | `k_to_R` (A = 2.5 m²) | 0.0114286 |
| `k_to_thermal_resistivity` [m-K/W] | 4 | `k_to_thermal_resistivity` | 27.027 |
| `thermal_resistivity_to_k` [W/m-K] | 0.25 | `thermal_resistivity_to_k` | 0.037037 |
| `R_value_to_k` (SI) [W/m-K] | 0.211667 | `R_value_to_k` (SI) | 0.0338667 |
| `R_value_to_k_imp` (imperial) [W/m-K] | 0.203138 | `R_value_to_k_imp` (imperial) | 0.0288456 |
| `k_to_R_value` (SI) [m²-K/(W-inch)] | 0.12 | `k_to_R_value` (SI, k = 0.034) | 0.747059 |
| `k_to_R_value_imp` (imperial) | 0.71 | `k_to_R_value_imp` (imperial, k = 0.034) | 4.24200 |
| `R_cylinder` [K/W] | 8.38432·10⁻⁵ | `R_cylinder` | 0.0193449 |
| `S_isothermal_sphere_to_plane` [m] | 6.29893 | `S_isothermal_sphere_to_plane` | 3.35103 |
| `S_isothermal_pipe_to_plane` [m] | 3.14607 | `S_isothermal_pipe_to_plane` | 18.4795 |
| `S_isothermal_pipe_normal_to_plane` [m] | 104.869 | `S_isothermal_pipe_normal_to_plane` | 7.77927 |
| `S_isothermal_pipe_to_isothermal_pipe` [m] | 1.18871 | `S_isothermal_pipe_to_isothermal_pipe` | 2.99955 |
| `S_isothermal_pipe_to_two_planes` [m] | 1.29637 | `S_isothermal_pipe_to_two_planes` | 10.8284 |
| `S_isothermal_pipe_eccentric_to_isothermal_pipe` [m] | 47.7098 | `S_isothermal_pipe_eccentric_to_isothermal_pipe` | 31.2327 |
| `Q` [W] | 73.1200 | `Q` | 40.5185 |
| `q_ext` [W/m²] | 123.212 | `q_ext` | 94.8340 |
| `UA` [W/K] | 0.481053 | `UA` | 0.266569 |
| `U_inner` [W/m²-K] | 1.96496 | `U_inner` | 1.69703 |
| `U_outer` [W/m²-K] | 0.810608 | `U_outer` | 0.623908 |
| `To1` [°C] | 180 | `To1` | 180 |
| `To2` [°C] | 179.973 | `To2` | 179.984 |
| `To3` [°C] | 33.4285 | `To3` | 36.9346 |
| `Rl1` [m²-K/W] | 2.22011·10⁻⁴ | `Rl1` | 1.71252·10⁻⁴ |
| `Rl2` [m²-K/W] | 1.18936 | `Rl2` | 1.50842 |

Case *A* is the `ht` doctest case of `cylindrical_heat_transfer`
(steel pipe 77.93 mm + 50 mm insulation, `hi = 10¹² W/m²-K` holding the inner
face at `Ti`, `ho = 22.697193 W/m²-K`); case *B* is the insulated pipe above
(`hi = 250`, `ho = 12`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. the
     temperature profile To1..To3 across the insulated wall of case B
     (Parametric tab), figures/conduction_resistances_and_shapes_profile.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conduction.py`, commit `85e0ee6`, installed from the local clone in a
throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for case *B*. The 50 output values of the demonstration
program were compared with `CoolSolve/tools/compare_solution.py`
(tolerance `rtol = 0.001`):

```
50 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 79
```

(the 79 "only in CoolSolve" variables are the 79 inputs of the demonstration
program — the reference table holds only the 50 outputs). The largest
relative deviation over the 50 values is **8.0·10⁻¹¹** (`Rl1_B`), and the
runner-up 5.7·10⁻¹¹ (`Rl1_A`): the two layer resistances are the smallest
outputs of the `PROCEDURE` block (≈10⁻⁴), which CoolSolve solves iteratively
(4 iterations); they agree with `ht` to its last printed digits up to the
solver convergence level. Every other deviation is below 5·10⁻¹³.

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `R_to_k` | 0.5 | 0.5 | 0 |
| `k_to_R` | 0.05 | 0.05 | 0 |
| `k_to_thermal_resistivity` | 4.0 | 4.0 | 0 |
| `thermal_resistivity_to_k` | 0.25 | 0.25 | 0 |
| `R_value_to_k` (SI) | 0.2116666666666667 | 0.2116666666667 | 1.6e-13 |
| `R_value_to_k_imp` (imperial) | 0.20313787163983463 | 0.2031378716398 | 1.7e-13 |
| `k_to_R_value` (SI) | 0.11999999999999998 | 0.12 | 1.2e-16 |
| `k_to_R_value_imp` (imperial) | 0.71 | 0.71 | 0 |
| `R_cylinder` | 8.38432343682705e-05 | 8.384323436827e-05 | 6.0e-15 |
| `S_isothermal_sphere_to_plane` | 6.298932638776527 | 6.298932638777 | 7.5e-14 |
| `S_isothermal_pipe_to_plane` | 3.146071454894645 | 3.146071454895 | 1.1e-13 |
| `S_isothermal_pipe_normal_to_plane` | 104.86893910124888 | 104.8689391012 | 4.7e-13 |
| `S_isothermal_pipe_to_isothermal_pipe` | 1.188711034982268 | 1.188711034982 | 2.3e-13 |
| `S_isothermal_pipe_to_two_planes` | 1.2963749299921428 | 1.296374929992 | 1.1e-13 |
| `S_isothermal_pipe_eccentric_to_isothermal_pipe` | 47.709841915608976 | 47.70984191561 | 2.1e-14 |
| `Q` | 73.12000884069367 | 73.12000884069 | 5.0e-14 |
| `q_ext` | 123.21239646288495 | 123.2123964629 | 1.2e-13 |
| `UA` | 0.48105268974140575 | 0.4810526897414 | 1.2e-14 |
| `U_inner` | 1.9649599487726137 | 1.964959948773 | 2.0e-13 |
| `U_outer` | 0.8106078714663484 | 0.8106078714663 | 6.0e-14 |
| `To1` [°C] | 180.0 (453.15 K) | 180.0 | 0 (shift 273.15) |
| `To2` [°C] | 179.9726455779877 | 179.972645578 | 6.8e-14 |
| `To3` [°C] | 33.428530147744 | 33.42853014774 | 1.2e-13 |
| `Rl1` | 0.00022201030738405449 | 0.0002220103073967 | 5.7e-11 |
| `Rl2` | 1.189361782070256 | 1.18936178207 | 2.2e-13 |

Case *B* (second input set, computed with the same Python functions): all 25
values agree likewise, the largest deviation being the 8.0·10⁻¹¹ quoted above
on `Rl1_B` (`Q_B` 40.51846933075866, `q_ext_B` 94.83403941922943,
`UA_B` 0.266568877176, `U_inner_B` 1.697030179081, `U_outer_B` 0.623908154074,
`To2_B` 179.9837594587, `To3_B` 36.93463096715, `Rl2_B` 1.508415431502, and
the remaining 17 values identical to the last printed digit; full precision
in `conduction_resistances_and_shapes.sol`).

The temperatures of case *A* are given in °C: `ht` takes K (453.15 K /
301.15 K in its doctest), but only temperature differences enter the
equations, so the results in W and K are identical and its temperature
outputs simply shift by 273.15.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the conduction relations of `ht`, the heat-transfer
component of ChEDL, file `ht/conduction.py`, functions `R_to_k`, `k_to_R`,
`k_to_thermal_resistivity`, `thermal_resistivity_to_k`, `R_value_to_k`,
`k_to_R_value`, `R_cylinder`, `S_isothermal_sphere_to_plane`,
`S_isothermal_pipe_to_plane`, `S_isothermal_pipe_normal_to_plane`,
`S_isothermal_pipe_to_isothermal_pipe`, `S_isothermal_pipe_to_two_planes`,
`S_isothermal_pipe_eccentric_to_isothermal_pipe` and
`cylindrical_heat_transfer`, version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every relation kept the name of
its `ht` function; the Python default arguments became mandatory (area `A`,
length `L` — pass `A = 1` / `L = 1` for the per-unit values, as in the
original), the `SI` boolean became a 1/0 flag, the layer lists of
`cylindrical_heat_transfer` became two fixed layers, and the Python `log`,
`pi` and `acosh` became the EES `LN`, a local `pi_val` constant and
`ArcCosH`. No equation was changed. Scientific basis per function: the book
or paper quoted in its comment block (Bergman, Lavine, Incropera & DeWitt,
*Introduction to Heat Transfer*, 6E, Wiley, 2011; Kreith, Manglik & Bohn,
*Principles of Heat Transfer*, Cengage, 2010; VDI Heat Atlas, 2E, Springer,
2010; Sunderland & Johnson, ASHRAE Transactions 70, 1964).

## Conversion log

- **2026-10-08 — translation (T-FUNC card C-115, family `HT-020`).** One EES
  `FUNCTION` per `ht` relation (13) plus one `PROCEDURE` for
  `cylindrical_heat_transfer` (7 outputs of the ht dict returned as 10
  scalars: `Q`, `q_ext`, `UA`, `U_inner`, `U_outer`, `To1`, `To2`, `To3`,
  `Rl1`, `Rl2`), with the formula, the validity range as quoted by `ht`, the
  original reference and the `ht` module/function/version/commit in the
  comment block. All arguments in SI; no property functions inside, so the
  calling model passes `k`, `h`, `R` itself.
- **`pi_val` local constant** in every subprogram body that needs π:
  CoolSolve does not resolve the `pi`/`PI` constant inside a
  `FUNCTION`/`PROCEDURE` body (it silently evaluates as 1 — **bug
  `CS-BUG-PI-FUNCTION`**, already registered in the CoolSolve gap register
  with library model `CSL-0089`; not re-reported). `pi_val = 3.141592653589793`
  is a local literal, valid EES, numerically identical to `pi`; the equations
  are unchanged. In the main program `pi`/`PI` resolves correctly (no pi is
  used there).
- **`ArcCosH`** (EES name of the inverse hyperbolic cosine, three `S_*`
  functions) is supported by CoolSolve v0.3.0 (checked against
  `acosh(2) = 1.316957896925`).
- **`cylindrical_heat_transfer`**: the ht helper takes Python lists
  `ts`, `ks` of any length; the `PROCEDURE` fixes **two layers** (single
  layer: `t2 = 0`; the ht doctest and the case-B demonstration both have two).
  Its result names `q`, `T1`, `T2`, `T3` are renamed `q_ext`, `To1`, `To2`,
  `To3` (EES names are case-insensitive: they would collide with the inputs
  `t1`, `t2` and with each other); the layer resistances are `Rl1`, `Rl2` in
  the caller. The ht docstring calls `Rs` [m·K/W] and `q` [W/m³]; its code
  and doctest give `Ri = 0.5·D_ext·ln(Do/Di)/k` used as `q·Ri` = layer
  temperature drop (i.e. [m²-K/W] on the external-area basis) and
  `q = Q/(π·D_ext)` [W/m²] — the function comment follows the code.
- **Temperatures in °C** (CoolSolve unit system): `ht` takes K; only
  differences enter the equations, results in W and K identical, temperature
  outputs shift by 273.15 (case A: 453.15 K → 180 °C, as in the doctest).
- **R-value conversions**: the imperial factor is
  `ft²·°F·h/(Btu·inch) = 6.933471798515978` in [m·K/W] (fluids.constants:
  Btu = 1055.05585262 J, foot = 0.3048 m, hour = 3600 s, inch = 0.0254 m,
  °F difference = K/1.8); the ht docstring rounds it to "6.93347". The `SI`
  boolean became a 1/0 flag argument.
- **Selectors not translated**: none — `ht/conduction.py` has no dispatcher
  (its 14 public functions are all translated). The deprecated aliases of
  `ht/units.py` (`R_to_k`, `R_value_to_k`, `k_to_R_value`) are the same
  functions, translated once here.
- **Level**: equations 129 → 1 point (50–300), largest block 10 → 1 point
  (6–30), functions present → 1, multi-zone no → 0, semi-empirical no → 0,
  curated guesses no → 0. Score 3 → **level 2**.

## Limitations and CoolSolve gaps

- **`CS-BUG-PI-FUNCTION`** (already registered, reference only): the `pi`
  constant is not resolved inside a `FUNCTION`/`PROCEDURE` body (it silently
  evaluates as 1). This model writes `pi_val = 3.141592653589793` as a local
  literal in the bodies that need it — valid EES, numerically identical, so
  the model is not blocked; when the bug is closed the local constant can be
  replaced by `pi`.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  relations copies the definitions for now.
- The `PROCEDURE` block (10 outputs) is solved iteratively by CoolSolve
  (4 iterations); the two smallest outputs (`Rl1`, `Rl2` ≈ 10⁻⁴) therefore
  agree with `ht` only to ≈10⁻¹⁰ relative (see *Verification*). Everything
  else is exact to the last printed digit.
- No gap was registered by this card.

## Related models

- `CSL-0089` *condensation_film*: the `ht` family where `CS-BUG-PI-FUNCTION`
  was discovered; it uses the same local `pi_val` convention in its function
  bodies and shares the *one function per correlation + demonstration
  program* layout of the `ht` triage.
- `CSL-0107` *radiation_heat_flux*: the `ht` family of the neighbouring
  physics (radiation exchange, 3 functions), same layout and same
  attribution; the two files complete the "no-flow" heat-transfer relations.
- `CSL-0042` *building_rc_network_3r2c* and `CSL-0012` *thermal_comfort_pmv_ppd*:
  building models that write their wall conduction (plane-wall `R = t/(k·A)`)
  inline — this file provides the same relations as reusable functions.
- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` family (convection),
  which set the layout of this file.
- `sources/labothappy` LTP-047 (pipe heat loss): an application model that
  could use `R_cylinder` and `S_isothermal_pipe_to_plane` from this file.
