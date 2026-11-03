# Air cooled in a vertical piston-cylinder with stops (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0214`

A frictionless piston fitted with stops closes a vertical cylinder of air.
Cooling at constant pressure brings the piston down to the stops. Further
cooling is at constant volume. The model computes the air temperature when
the piston reaches the stops and the pressure after cooling to the final
temperature, and the same two results from the ideal-gas law. Teaching
exercise of the ULiège course *Thermodynamique appliquée* (MECA0002),
repetition 2 (2022-2023).

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Air |
| **Size** | 17 equations (largest block: 1) |
| **Source** | thermo_models, file `R2_E4_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@62d92f0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A vertical cylinder closed by a frictionless piston fitted with stops contains
air. The piston area is 0.2 m². The air is initially at 200 kPa and 500 °C.
It is then cooled by heat transfer to the surroundings.

a. What is the temperature of the air in the cylinder when the piston reaches
the stops?

b. If cooling continues until the temperature reaches 20 °C, what is the
pressure inside the cylinder in that final state?

The equation window also checks both answers with the ideal-gas law, and it
says to use kelvin in that law. The heat and the work of the process are not
variables of this equation window.

## Model

Two processes, as written in the equation window:

1. Constant pressure and fixed mass, from the initial height down to the
   stops. The stop height is half the initial height (`h_1 = h_0/2`).
2. Constant volume from the temperature at the stops down to the final
   temperature. Volume and mass are unchanged, so the specific volume is
   unchanged.

The ideal-gas check keeps the ratio \(T/V\) on the isobar and the ratio
\(T/P\) on the isochore, with the temperatures in kelvin.

\[
T_{1,\mathrm{gp}} = T_0\,\frac{V_1}{V_0}, \qquad
p_{2,\mathrm{gp}} = p_0\,\frac{T_2}{T_{1,\mathrm{gp}}}
\]

| Input | Value |
|---|---|
| `A_p` | 0.2 m² |
| `T_0` | 500 °C, stored as `500 [K]+273.15 [K]` (773.15 K) |
| `p_0` | 200 kPa (200×10³ Pa) |
| `h_0` | 2 m |
| `T_2` | 20 °C, stored as `20 [K]+273.15 [K]` (293.15 K) |

Those five assignments are already equations. The system is square without
any further assignment (17 equations, 17 variables). The diagram-window RTF
is empty. No diagram-state array is added.

Property calls pass `T - 273.15` because CoolSolve reads the temperature
argument as °C. `temperature()` returns °C, so `T_1` adds 273.15 and stays
in kelvin, with `T_0`, `T_2` and `T_1_gp`.

## How to run

```bash
coolsolve ./piston_cylinder_stops_air.eescode
```

Every block is explicit. CoolSolve reports 0 iterations with the shipped
`.initials` and 0 iterations without them. There is no `abs()`, so the
guesses do not select a root. The `.initials` file is the EES stored
solution with `p_0`, `p_2` and `p_2_gp` in Pa and `iso_v` in K/Pa.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `T_1` | 386.734 K | 386.575 K | 7.07e-01 against 113.425 °C |
| `T_1_gp` | 386.575 K | 386.575 K | 7.07e-01 against 113.425 °C |
| `p_2` [Pa] | 151472.94 | 151665.27 (151.6652655 kPa) | 1.27e-03 |
| `p_2_gp` [Pa] | 151665.27 | 151665.27 (151.6652655 kPa) | 1.82e-10 |
| `v_air` [m³/kg] | 1.110447 | 1.109655 | 7.13e-04 |
| `m_air` [kg] | 0.360215 | 0.360472 | 7.13e-04 |
| `iso_v` | 0.001932875 K/Pa | 1.932875 K/kPA | 9.99e-01 |

The temperature at the stops is 386.734 K in CoolSolve and 386.575 K in the
stored solution. The ideal-gas value `T_1_gp` is 386.575 K on both sides.
The pressure after cooling is 151472.94 Pa in CoolSolve and 151665.27 Pa in
the stored solution. The ideal-gas value `p_2_gp` is 151665.27 Pa on both
sides. The equation window does not compute the heat or the work.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `R2_E4_2022.EES` (EES X10.836, 17 variables),
compared with `compare_solution.py --ees-units`. The tool's summary line is:

`17 common variables, 6 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

`--ees-units` scaled `p_0`, `p_2` and `p_2_gp` (kPa ×1000) and rewrote `T_0`,
`T_1`, `T_2` and `T_1_gp` from K to °C. It left `iso_v` unscaled. The stored
unit of `iso_v` is `K/kPA`: the tool scales a `kPa` numerator only, and the
stored spelling is `kPA`.

Every difference above rtol 0.001:

- `iso_v` prints 9.99e-01 (unrounded 0.999). The equation is `T_1_gp/p_0`.
  With `p_0` in Pa the result is 0.001932875 K/Pa. EES stores 1.932875
  because `p_0` was 200 kPa. The two values are the same ratio.
- `T_2` prints 9.32e-01, `T_1` prints 7.07e-01, `T_1_gp` prints 7.07e-01 and
  `T_0` prints 3.53e-01. The equation window stores 773.15 K, 386.575 K and
  293.15 K, and the model keeps kelvin. The tool subtracts 273.15 and then
  compares 773.15 with 500, 386.575 with 113.425 and 293.15 with 20. In
  kelvin, `T_0`, `T_2` and `T_1_gp` match the stored values. `T_1` is
  386.734 K against 386.575 K, a relative difference of 4.11e-04.
- `p_2` prints 1.27e-03. EES `Air` is an ideal gas, so the stored `p_2`
  equals `p_2_gp` (151665.265 Pa). CoolSolve `pressure(Air, T=T_2-273.15, V=v_1)`
  returns 151472.941 Pa. The ratio of those two pressures is Z = 0.99873,
  the CoolProp air departure at this state. `p_2_gp` itself matches
  (relative difference 1.82e-10).

`v_air`, `v_1` and `m_air` print 7.13e-04, inside rtol 0.001. At 500 °C and
200 kPa the specific volume is 1.110447 m³/kg in CoolSolve and 1.109655 m³/kg
in EES. The specific gas constants implied by \(v = RT/p\) are 287.253 J/kg-K
and 287.048 J/kg-K.

The equation window has no enthalpy, so the ideal-gas Air reference offset
(about +126 kJ/kg) does not appear. It also has no heat and no work.

The largest relative difference over all 17 common variables, as printed by
the tool, is 9.99e-01 on `iso_v`.

CoolSolve warns that fluid `Air` is dry air and that `t=500` is read as °C.
The source fluid is `AIR` / `air`, so the calls stay `Air`. 500 °C is the
argument `T_0 - 273.15` (773.15 K). A further warning says that
`v = 0.555 m³/kg` is large for a density. It is the specific volume at the
stops; the stored EES value is 0.554827 m³/kg.

## Source and attribution

The equation window names no person. The EES licence tag is the student and
staff licence of the Laboratoire de Thermodynamique, University of Liège. The
file itself names nobody. The inventory attributes the course to S. Quoilin,
so the authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R2/R2_E4_2022.EES`.

Candidate TM-0400. Teaching exercise, not an exam. Course: *Thermodynamique
appliquée* (ULiège, MECA0002), repetition 2, 2022-2023. EES X10.836.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R2_E4_2022.EES` (EES X10.836, plain text, decimal commas already rewritten as dots, European argument separators, 17 variables, no tables). The diagram-window RTF is empty. With `$UnitSystem` removed, the extraction is square: 17 equations, 17 variables, largest block 1. No diagram input and no stored unknown was turned into an equation. `$UnitSystem` was deleted. No `$TABSTOPS`, `$Export`, `concat$` or `EESFILEDIR$`. Comments translated to English.
- **Units**: `$UnitSystem SI MASS DEG KPA K KJ`. Pressure: `p_0` 200 kPa → `200e3` Pa. Temperatures stay in kelvin: `T_0 = 500 [K]+273.15 [K]`, `T_2 = 20 [K]+273.15 [K]`, as the equation window stores them. Property calls pass `T - 273.15` because CoolSolve reads the temperature argument as °C, and `T_1 = temperature(...)+273.15` so the stored temperature stays in kelvin. `iso_v = T_1_gp/p_0` and `p_2_gp = T_2/iso_v` are unchanged as equations; with `p_0` in Pa, `iso_v` is in K/Pa and `p_2_gp` is in Pa. No energy term is present, so nothing is scaled from kJ to J. `.initials`: `p_0`, `p_2` and `p_2_gp` ×1000; `iso_v` ÷1000; temperatures and the other stored values left as stored.
- **Case**: the original calls `volume(AIR, ...)`, `temperature(air, ...)` and `pressure(air, ...)`. The calls are written `volume(Air, T=T_0-273.15, P=p_0)`, `temperature(Air, P=p_0, V=v_1)+273.15` and `pressure(Air, T=T_2-273.15, V=v_1)`. The parentheses around `T_1_gp` in the original assignment are omitted.
- **Fluid**: `AIR` and `air` written `Air` (the same ideal gas in the source). CoolSolve warns that moist air would be `AirH2O`. The source is dry air, so the fluid stays `Air`.
- **Level**: equations 17 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one closed system, not discretised → 0; no calibration, off-design or dynamics → 0; explicit, 0 iterations with or without guesses → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

The equation window stops at the temperature at the stops and the pressure
after the constant-volume cooling. It does not compute the heat or the work.
Absolute Air enthalpies are not part of the model. `compare_solution.py
--ees-units` rewrites a stored kelvin temperature whose name starts with `T`
into °C, so `T_0`, `T_1`, `T_2` and `T_1_gp` print a large relative difference
while the stored kelvin values agree. It also leaves `iso_v` (`K/kPA`)
unscaled.

No CoolSolve gap. `missing_features` is empty.

## Related models

`related` is empty. `CSL-0210` is a piston-cylinder exercise on water with a
spring. TM-0402 and TM-0406 are the other files of duplicate group DG-0098.
They are not imported here.
