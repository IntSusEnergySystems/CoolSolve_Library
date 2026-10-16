# R113 ORC turbine outlet temperature (example)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0248`

Teaching example for an R113 ORC turbine. The inlet is 150 kPa and 65 °C,
the isentropic efficiency is 0.89 and the enthalpy drop is 17.5 kJ/kg. The
result is the turbine outlet temperature. ULiège course *Thermodynamique
appliquée* (MECA0002), August 2022.

| | |
|---|---|
| **Category** | Cycles and machines › Organic Rankine cycles |
| **Fluids** | R113 |
| **Size** | 11 equations (largest block: 1) |
| **Source** | thermo_models, file `Q2_temp_sortie_turb.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@6c1755b — verified against the EES stored solution (see *Verification*) |

## Problem statement

The ORC turbine has an isentropic efficiency of 89 %. The pressure and
temperature at the turbine inlet are 150 kPa and 65 °C. The fluid undergoes
an enthalpy change of 17.5 kJ/kg inside the turbine.

Calculate the turbine outlet temperature, in °C. These conditions are not
optimised, and the turbine outlet can still be superheated vapour.

The equation window already writes `eta_is_turb = 0.89`. The quoted statement
stays a comment.

## Model

The window computes one turbine. State 8 is the inlet. State 5 is the outlet.
Temperatures are stored in kelvin. Property calls receive °C.

Inlet data, as written:

\[
\Delta h_{turb} = 17.5 \times 1000
\]
\[
\eta_{is,turb} = 0.89
\]
\[
p_8 = 150 \times 10^3
\]
\[
T_8 = 65 + 273.15
\]

`T_sat` returns °C, so 273.15 is added once. `enthalpy` and `entropy` receive
`T8 - 273.15`:

\[
T_{sat,8} = T_{sat}(\mathrm{R113}, p_8) + 273.15
\]
\[
h_8 = h(\mathrm{R113},\, T = T_8 - 273.15,\, p_8)
\]
\[
s_8 = s(\mathrm{R113},\, T = T_8 - 273.15,\, p_8)
\]

Outlet enthalpy, as written:

\[
h_{5s} = -\Delta h_{turb}/\eta_{is,turb} + h_8
\]
\[
h_5 = h_8 - \Delta h_{turb}
\]

Outlet pressure and temperature. The pressure pair is `(H, S)`. `Temperature`
returns °C, so 273.15 is added once:

\[
p_5 = P(\mathrm{R113},\, H = h_{5s},\, S = s_8)
\]
\[
T_5 = T(\mathrm{R113},\, H = h_5,\, P = p_5) + 273.15
\]

| Input | Value |
|---|---|
| `delta_h_turb` | `17.5*1000` J/kg (17.5 kJ/kg) |
| `eta_is_turb` | 0.89 |
| `p8` | 150e3 Pa (150 kPa written as 150e3) |
| `T8` | `65+273.15` K (65 °C) |

The bracket tags `[J/kg]`, `[Pa]` and `[K]` parse, and the numbers stay
17500 J/kg, 150000 Pa and 338.15 K. The system is square (11 equations,
11 variables). Diagram-state arrays are omitted: the window is a turbine
inlet and a given enthalpy drop.

## How to run

```bash
coolsolve ./orc_r113_turbine_outlet_temperature.eescode
```

Every block is explicit (largest block 1). CoolSolve reports 0 iterations
with the shipped `.initials` and 0 iterations without them. The `.initials`
file is the EES stored solution, with temperatures in kelvin and pressures
in pascal. The solution is the same in both runs.

## Results

Outlet temperature, enthalpies and outlet pressure. `h8 - h5` is the given
drop, on both sides:

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `T5` [K] | 309.5075967834 | 309.6273251 | 3.87e-04 |
| `T5` as °C (`T5` − 273.15) | 36.3575967834 | 36.4773251 | same 0.119728 K |
| `h5` [J/kg] | 381742.3610876 | 215906.395 | 4.34e-01 |
| `h8` [J/kg] | 399242.3610876 | 233406.395 | 4.15e-01 |
| `h8 - h5` [J/kg] | 17500 | 17500 | matches |
| `p5` [Pa] | 36236.26685868 | 36090.73529 | 4.02e-03 |

`T8` is 338.15 K on both sides. The enthalpy reference is +165835.9660876 J/kg
on `h8` and on `h5`, so it cancels in `h8 - h5`. The same offset is on `h5s`
(379579.4397392 J/kg against the stored 213743.4736 J/kg).

`s8` is 1614.623046721 J/kg-K against 749.6180463 J/kg-K. That entropy
reference, +865.005000421 J/kg-K, is the largest relative difference.

The inlet is 150 kPa and 65 °C. The outlet is about 36.2 kPa and 36.4 °C,
and the fluid enthalpy falls by 17.5 kJ/kg.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `Q2_temp_sortie_turb.EES` (EES X6.883,
11 variables), compared with `compare_solution.py` without `--ees-units`.
The tool's summary line is:

`11 common variables, 5 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The maximum relative difference over all 11 common variables, as printed by
the tool, is 5.36e-01, on `s8` (unrounded 0.5357318552944385).

Every difference above rtol 0.001:

- `s8` prints 5.36e-01. CoolSolve keeps 1614.623046721 J/kg-K against
  749.6180463 J/kg-K. The gap is the entropy reference, +865.005000421 J/kg-K.
- `h5s` prints 4.37e-01, `h5` prints 4.34e-01 and `h8` prints 4.15e-01.
  The absolute enthalpies carry +165835.9660876 J/kg. `h8 - h5` is 17500 J/kg
  on both sides.
- `p5` prints 4.02e-03 (unrounded 0.004016185476). The model keeps
  36236.26685868 Pa against 36090.73529 Pa, from
  `Pressure(R113, H=h5s, S=s8)`. The gap is +145.53156868 Pa.

`T5` prints 3.87e-04 and stays inside rtol. The model keeps 309.5075967834 K
against 309.6273251 K (−0.1197283166 K). That gap is the
`Temperature(R113, H=h5, P=p5)` property difference. Read as °C, the outlet
is 36.3575967834 °C against 36.4773251 °C. `T8` matches 338.15 K. `T_sat8`
is 333.1069961435 K against 333.0692556 K (1.13e-04).

All 11 equations are satisfied. The largest residual is 0.

CoolSolve reports 0 iterations with the shipped `.initials` and 0 iterations
without them. The fluid call stays `R113`. This solve printed no fluid-name
warning.

## Source and attribution

The equation window names no person. The EES licence tag is
`{$ID$ #434: For use only by Kwangil Kim of Samsung Electronics Co.}`, the
licence holder, not the author. The file belongs to the ULiège course
MECA0002. The authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/Aout 2022/Q2_temp_sortie_turb.EES`.

Candidate TM-0458. No duplicate group. Teaching example. Course:
*Thermodynamique appliquée* (ULiège, MECA0002), August 2022. EES X6.883.

## Conversion log

- **2026-10-16 — import**: `ees_extract.py` on `Q2_temp_sortie_turb.EES` (EES X6.883, plain text, decimal commas rewritten as dots, 11 variables, no tables). The converted window is square: 11 equations, 11 variables, largest block 1. No stored unknown was added. `$UnitSystem` was deleted. The extracted window has no `$TABSTOPS` and no `$Export`. Comments translated to English. The quoted problem statement stays a comment. `eta_is_turb = 0.89` stays an equation. Diagram-state arrays are omitted. This question is imported alone. The August 2022 Q1–Q10 notes say to merge those questions; this import does not merge them. `related` is empty.
- **Units**: `$UnitSystem SI MASS DEG PA K J`. `p8` stays `150e3` Pa. `delta_h_turb` stays `17.5*1000` J/kg. `T8` stays `65+273.15` K, and the `[K]` tags parse (stored `T8` is 338.15 K). Property boundary only: `T_sat8 = T_sat(R113, P=p8)+273.15`, `h8 = enthalpy(R113, T=T8-273.15, P=p8)`, `s8 = entropy(R113, T=T8-273.15, P=p8)`, and `T5 = Temperature(R113, H=h5, P=p5)+273.15`. `h5s = -delta_h_turb/eta_is_turb+h8` and `h5 = h8-delta_h_turb` stay as written. `p5 = Pressure(R113, H=h5s, S=s8)` stays the pair `(H, S)`. `.initials` are the stored solution, with temperatures in kelvin.
- **Fluid**: `R113` stays `R113`.
- **Level**: equations 11 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one turbine → 0; no calibration, off-design or dynamics → 0; explicit, 0 iterations with or without guesses → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

Absolute R113 enthalpies differ from the stored solution by +165835.9660876 J/kg.
The drop `h8 - h5` is 17500 J/kg on both sides. Absolute entropy differs by
+865.005000421 J/kg-K, which prints 5.36e-01 on `s8`. `p5` prints 4.02e-03
and `T5` prints 3.87e-04. The equations are satisfied.

`missing_features` is empty.

## Related models

`related` is empty. This example stands on its own.
