# Aircraft-engine diffuser exercise

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0180`

Steady flow of dry air through an aircraft-engine diffuser. The equation
window sets the inlet at 10 °C and 80 kPa, 200 m/s, with an area of 0.4 m².
The exit velocity is neglected and the exit pressure is atmospheric. The
model computes the mass flow and the exit temperature from the steady-flow
energy balance. ULiège MECA0002 exercise, 2022-2023.

| | |
|---|---|
| **Category** | Components › Valves, nozzles and piping |
| **Fluids** | Air_ha |
| **Size** | 28 equations (largest block: 1) |
| **Source** | thermo_models, ULiège MECA0002, file `R3_E10_2022_diffuseur.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Exercise (the file titles it "Exercice 8"; the collection path is repetition
R3, exercise 10). Air at 108 °C and 80 kPa enters an aircraft-engine diffuser
at 200 m/s in steady state. The inlet area is 0.4 m². The air leaves with a
negligible velocity. Determine the air mass flow rate and the air temperature
at the diffuser exit.

The equation window and the stored solution use `T_in = 10` °C. The model
follows that equation, so the solved case is 10 °C, 80 kPa. The exit pressure
is set to 101.325 kPa (atmospheric, as the file assumes). Shaft work is zero.
Heat transfer is zero because the file gives no heat-loss data. Elevations
are zero, so the potential-energy change is zero. The gravitational
acceleration is 9.1 m/s², as written in the file.

## Model

Dry air, EES fluid `air_ha` (real dry air: temperature and pressure only, no
humidity ratio). Mass conservation sets the exit mass flow equal to the inlet
mass flow. The inlet mass flow is the inlet velocity times the inlet area,
divided by the specific volume. The steady-flow energy balance is

\[
\dot Q + \dot W = \dot m\,(\Delta h + \Delta e_c + \Delta e_p)
\]

with \(\dot Q = 0\), \(\dot W = 0\), \(\Delta e_p = 0\) and
\(\Delta e_c = (c_\mathrm{out}^2 - c_\mathrm{in}^2)/2\). Then
\(\Delta h = -\Delta e_c\) and the exit temperature follows from the exit
enthalpy and the exit pressure.

| Input | Value |
|---|---|
| `A_in` | 0.4 m² |
| `p_in` | 80 kPa (80×10³ Pa in the file) |
| `p_out` | 101.325 kPa (101.325×10³ Pa) |
| `T_in` | 10 °C (equation window and stored solution) |
| `c_in` | 200 m/s |
| `c_out` | 0 m/s |
| `z_in`, `z_out` | 0 m |
| `g` | 9.1 m/s² |

The twenty equation-window equations are square (20 variables) without any
Diagram-window value. The stored values of the unknowns are guesses in
`.initials`, in SI. Eight further equations, `P[i]`, `h[i]`, `T[i]`, `s[i]`
for i = 1 (inlet) and i = 2 (exit), are post-processing for the CoolSolve
diagram. A solve of the twenty equations alone and a solve of this file give
the same twenty variables (relative difference 0).

## How to run

```bash
coolsolve ./aircraft_engine_diffuser.eescode
```

CoolSolve reports 3 iterations with the shipped `.initials` and 11 iterations
without them. Both runs succeed. The largest block has one equation. The
`.initials` file is the EES stored solution converted to pascal and joule.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `c_out` | 0 m/s | 0 m/s |
| `T_out` | 29.9317 °C | 29.9318 °C |
| `q_m_in` | 78.7721 kg/s | 78.7725 kg/s |
| `v_in` | 1.015588 m³/kg | 1.015583 m³/kg |
| `Deltah` | 20000 J/kg | 20 kJ/kg |
| `DeltaEC` | −20000 J/kg | −20 kJ/kg |
| `h_in` | 409399 J/kg | 283.338 kJ/kg |
| `h_out` | 429399 J/kg | 303.338 kJ/kg |

`c_out` is an input (negligible exit velocity). `Deltah = 20000` J/kg is the
kinetic-energy rise written as an enthalpy rise:
\(0.5 \times 200^2 = 20000\) J/kg.

The diagram states, present only in the CoolSolve solution, are
`P[1] = 80000` Pa, `P[2] = 101325` Pa, `T[1] = 10` °C, `T[2] = 29.9317` °C,
`h[1] = 409399` J/kg, `h[2] = 429399` J/kg, `s[1] = 3896.55` J/kg·K,
`s[2] = 3897.00` J/kg·K.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
`R3_E10_2022_diffuseur.EES` (EES X10.836, 20 stored variables). The tool
scaled `kPa`, `kJ` and `kW` (the stored unit strings are `kPa`, `kJ/kg` and
`kW`). Summary line:

> 20 common variables, 2 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8

The maximum relative difference over all common variables is **3.08e-01**
(`h_in`). The tool prints:

| Variable | EES (scaled) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `h_in` | 283338 J/kg | 409399 J/kg | 3.08e-01 |
| `h_out` | 303338 J/kg | 429399 J/kg | 2.94e-01 |
| `q_m_in` | 78.7725 kg/s | 78.7721 kg/s | 4.92e-06 |
| `v_in` | 1.01558 m³/kg | 1.01559 m³/kg | 4.92e-06 |
| `T_out` | 29.9318 °C | 29.9317 °C | 3.27e-06 |
| other 15 common variables | assigned or zero | same | 0.00e+00 |

`h_in` and `h_out` differ by the same 126061 J/kg. That is the enthalpy
reference of EES `air_ha` against CoolProp real dry air (`Air_ha`): the
stored 283.338 kJ/kg at 10 °C is the ideal-gas air-table value (about
283.4 kJ/kg at 283.15 K), and CoolSolve returns 409399 J/kg. `Deltah` is
20000 J/kg on both sides, so the energy balance agrees. `T_out` recovered
from `h_out` agrees to 3.27e-06, and `v_in` (hence `q_m_in`) agrees to
4.92e-06. Those residuals are the dry-air property formulation.

The eight names only in the CoolSolve solution are `P[1]`, `h[1]`, `T[1]`,
`s[1]`, `P[2]`, `h[2]`, `T[2]` and `s[2]`. The stored solution has no
entropy, so no entropy reference offset was measured.

## Source and attribution

The EES file names no person. Author taken from the course inventory:
S. Quoilin, ULiège MECA0002, 2022-2023. The licence tag is the University of
Liège thermodynamics laboratory student/staff licence, not an author.
Source file:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R3/R3_E10_2022_diffuseur.EES`
(EES X10.836, inventory row TM-0409). The comments in the source are French.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X10.836,
  `$UnitSystem SI MASS DEG KPA C KJ`, decimal commas converted by the
  extractor: `0,4` → 0.4, `101,325` → 101.325, `9,1` → 9.1, `0,5` → 0.5,
  `0,001` → 0.001). The `$UnitSystem` directive was removed. Pressures:
  `p_in` 80 kPa → `80e3` Pa, `p_out` 101.325 kPa → `101.325e3` Pa. Specific
  kinetic and potential energy dropped the factor `0.001` kJ/J, so
  `DeltaEC = 0.5*(c_out^2-c_in^2)` and `DeltaEP = g*(z_out-z_in)` are in
  J/kg (−20000 J/kg and 0). The energy balance is unchanged in form (kW and
  kJ/kg become W and J/kg together). Property calls stay
  `volume` / `enthalpy` / `temperature` of `Air_ha`; their results are in
  J/kg and m³/kg with pressures in Pa. Temperatures stay in °C. Velocities
  stay in m/s. `.initials` is the stored solution in SI: pressures ×1000
  (`p_in` 80000 Pa, `p_out` 101325 Pa), energies ×1000 (`Deltah` 20000,
  `DeltaEC` −20000, `DeltaEP` 0, `h_in` 283337.8535, `h_out` 303337.8535,
  `Q_dot` 0, `W_dot` 0). No Diagram-window input was restored: 20 equations,
  20 variables, system square. Comments translated to English. Variable
  names unchanged. The file calls `air_ha` with temperature and pressure
  only, so the fluid is real dry air `Air_ha`. Ideal-gas `Air` returns the
  same enthalpy, volume and exit temperature at this state.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  i = 1, 2. A solve without that block and a solve of this file give the
  same twenty original variables (relative difference 0).
- **Level**: equations 28 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone or discretised component → 0; no
  semi-empirical, off-design or dynamic physics → 0; converges from the
  default guess (11 iterations, 3 with the stored solution) → 0. Score 1 →
  level 1.

## Limitations and CoolSolve gaps

The exit velocity is imposed (`c_out = 0`), not calculated. The inlet
temperature that is solved is 10 °C, which is the equation-window value.
Absolute enthalpies use the CoolProp reference of real dry air. No
CoolSolve gap: `volume`, `enthalpy`, `temperature` and `entropy` of `Air_ha`
run, and the native file is the file that was solved.

## Related models

None.
