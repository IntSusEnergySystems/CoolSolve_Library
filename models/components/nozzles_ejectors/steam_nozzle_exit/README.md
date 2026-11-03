# Steam nozzle exercise

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0190`

Steady flow of steam through a nozzle. The equation window sets the inlet
at 17 bar and 370 °C, with an area of 0.018 m² and a mass flow of 4.53 kg/s.
The steam leaves at 13.8 bar and 274 m/s. The specific heat loss is
1.27 kJ/kg. The model computes the inlet velocity and the exit temperature
from the steady-flow energy balance. ULiège MECA0002 exercise, 2022-2023.

| | |
|---|---|
| **Category** | Components › Valves, nozzles and piping |
| **Fluids** | Water |
| **Size** | 29 equations (largest block: 1) |
| **Source** | thermo_models, ULiège MECA0002, file `R3_E1_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@3e9c1b6 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Exercise 1 of repetition R3 (2022-2023). Steam at 17 bar and 370 °C enters a
nozzle of cross-section 0.018 m² in steady state. The steam flow rate is
4.53 kg/s. The steam leaves the nozzle at 13.8 bar with a velocity of
274 m/s. The specific heat loss is 1.27 kJ/kg. Determine the velocity at
which the steam enters the nozzle, and the steam temperature at the nozzle
exit.

The equation window and this statement agree. The EES unit system is kelvin,
so the equation window stores the inlet temperature as
`T_in = 370 [K] + 273.15 [K]` (643.15 K). That is 370 °C. CoolSolve stores
temperatures in °C, so the model uses `T_in = 370`. The exit velocity is an
input. Shaft work is zero. Elevations are zero, so the potential-energy
change is zero. The gravitational acceleration is 9.1 m/s², as written in
the file. The specific heat loss is negative because the heat leaves the
steam.

## Model

Steam, EES fluid `water` (real fluid `Water`). The inlet specific volume
follows from the inlet temperature and pressure. The inlet velocity is the
inlet volume flow divided by the inlet area. Mass conservation is a comment
in the original (`q_m_out = q_m_in`); the energy balance uses `q_m_in`. The
steady-flow energy balance is

\[
\dot Q + \dot W = \dot m\,(\Delta h + \Delta e_c + \Delta e_p)
\]

with \(\dot W = 0\), \(\dot Q = \dot m\, q\) and \(q = -1270\) J/kg. Then
\(\Delta h = q - \Delta e_c\) and the exit temperature follows from the exit
enthalpy and the exit pressure.

| Input | Value |
|---|---|
| `A_in` | 0.018 m² |
| `q_m_in` | 4.53 kg/s |
| `q_dot_loss` | −1.27 kJ/kg (−1270 J/kg) |
| `p_in` | 17 bar (17×10² kPa in the file, 1.7×10⁶ Pa) |
| `p_out` | 13.8 bar (13.8×10² kPa in the file, 1.38×10⁶ Pa) |
| `T_in` | 370 °C (643.15 K in the equation window) |
| `c_out` | 274 m/s |
| `z_in`, `z_out` | 0 m |
| `g` | 9.1 m/s² |

The twenty-one equation-window equations are square (21 variables) without
any Diagram-window value. The stored values of the unknowns are guesses in
`.initials`, in SI. Eight further equations, `P[i]`, `h[i]`, `T[i]`, `s[i]`
for i = 1 (inlet) and i = 2 (exit), are post-processing for the CoolSolve
diagram. A solve of the twenty-one equations alone and a solve of this file
give the same twenty-one variables (relative difference 0).

## How to run

```bash
coolsolve ./steam_nozzle_exit.eescode
```

CoolSolve reports 4 iterations with the shipped `.initials` and 16 iterations
without them. Both runs succeed. The largest block has one equation. The
`.initials` file is the EES stored solution converted to pascal, joule and
°C (pressures ×1000, energies ×1000, temperatures −273.15).

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `c_out` | 274 m/s | 274 m/s |
| `c_in` | 42.7594 m/s | 42.7594 m/s |
| `T_out` | 349.710 °C | 349.710 °C (622.860 K) |
| `p_in` | 1.700×10⁶ Pa | 1700 kPa |
| `p_out` | 1.380×10⁶ Pa | 1380 kPa |
| `v_in` | 0.169905 m³/kg | 0.169905 m³/kg |
| `Deltah` | −37893.8 J/kg | −37.8938 kJ/kg |
| `DeltaEC` | 36623.8 J/kg | 36.6238 kJ/kg |
| `h_in` | 3187767 J/kg | 3187.767 kJ/kg |
| `h_out` | 3149873 J/kg | 3149.873 kJ/kg |

`c_out` is an input. The exit state is superheated steam at 349.710 °C and
1.38 MPa. The file does not compute a quality. The enthalpy change is the
heat loss minus the kinetic-energy rise:
\(-1270 - 0.5\times(274^2 - 42.759^2) = -37893.8\) J/kg.

The diagram states, present only in the CoolSolve solution, are
`P[1] = 1700000` Pa, `P[2] = 1380000` Pa, `T[1] = 370` °C,
`T[2] = 349.710` °C, `h[1] = 3187767` J/kg, `h[2] = 3149873` J/kg,
`s[1] = 7110.11` J/kg·K, `s[2] = 7144.01` J/kg·K.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
`R3_E1_2022.EES` (EES X10.836, 21 stored variables). The tool scaled `kPa`,
`kJ`, `kW` and `K` (the stored unit strings are `kPa`, `kJ/kg`, `kW` and
`K`). Summary line:

> 21 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8

The maximum relative difference over all common variables is **4.01e-10**
(`c_in`), as printed by the tool. Every common variable is inside rtol
0.001. The largest printed residuals are:

| Variable | EES (scaled) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `c_in` | 42.75937634 m/s | 42.75937632 m/s | 4.01e-10 |
| `V_dot_in` | 0.769668774 m³/s | 0.769668774 m³/s | 2.45e-10 |
| `h_in` | 3187767.214 J/kg | 3187767.213 J/kg | 1.78e-10 |
| `h_out` | 3149873.396 J/kg | 3149873.396 J/kg | 1.38e-10 |
| `v_in` | 0.1699048066 m³/kg | 0.1699048066 m³/kg | 1.12e-10 |
| `T_out` | 349.7096335 °C | 349.7096335 °C | 8.38e-11 |
| other 15 common variables | assigned or the balance | same | ≤ 4.81e-11 |

`h_in` and `h_out` differ by −0.00057 J/kg and −0.00043 J/kg. That is the
rounding of the stored digits, not a CoolProp-versus-EES reference offset:
the two differences are not a common constant, and `Deltah` agrees to
4.64e-11. Water enthalpies in this model therefore carry no offset to
separate from the physical results.

The energy balance closes on both sides:
`Deltah + DeltaEC + DeltaEP = -37893.818 + 36623.818 + 0 = -1270` J/kg,
which is `q_dot_loss`, and `Q_dot = 4.53 × (−1270) = −5753.1` W.

The eight names only in the CoolSolve solution are `P[1]`, `h[1]`, `T[1]`,
`s[1]`, `P[2]`, `h[2]`, `T[2]` and `s[2]`. The stored solution has no
entropy, so no entropy reference offset was measured. The file never calls
`quality()`.

## Source and attribution

The EES file itself names nobody. Author taken from the course inventory:
S. Quoilin, ULiège MECA0002, 2022-2023. The licence tag is the University of
Liège thermodynamics laboratory student/staff licence, not an author.
Source file:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R3/R3_E1_2022.EES`
(EES X10.836, inventory row TM-0411). The comments in the source are French.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X10.836,
  `$UnitSystem SI MASS DEG KPA K KJ`, decimal commas converted by the
  extractor: `0,018` → 0.018, `4,53` → 4.53, `1,27` → 1.27, `13,8` → 13.8,
  `273,15` → 273.15, `9,1` → 9.1, `0,5` → 0.5, `0,001` → 0.001; argument
  separator `;` → `,`). The `$UnitSystem` directive was removed. No
  `$Export`, `concat$`, `EESFILEDIR$` or `$TABSTOPS` lines were present.
  Pressures: `p_in` 17×10² kPa → `17e5` Pa, `p_out` 13.8×10² kPa →
  `13.8e5` Pa. Specific heat loss: −1.27 kJ/kg → −1270 J/kg. Specific
  kinetic and potential energy dropped the factor `0.001` kJ/J, so
  `DeltaEC = 0.5*(c_out^2-c_in^2)` and `DeltaEP = g*(z_out-z_in)` are in
  J/kg. The energy balance is unchanged in form (kW and kJ/kg become W and
  J/kg together). Temperatures: the equation window stores kelvin, so
  `T_in = 370+273.15` becomes `T_in = 370` °C; `temperature()` then returns
  °C. Property calls are `volume` / `enthalpy` / `temperature` of `Water`
  (the file writes `water`) with `P=` (the file writes `p=`). Velocities
  stay in m/s. `.initials` is the stored solution in SI. No Diagram-window
  input was restored: the diagram body is an empty RTF shell, and the
  21 equations and 21 variables are already square. Comments translated to
  English. Variable names unchanged. CoolSolve warns that `T=370` is read
  as 370 °C; that reading is the conversion of the stored 643.15 K, and
  `T_in`, `T_out` and both enthalpies match the stored solution.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  i = 1, 2. A solve without that block and a solve of this file give the
  same twenty-one original variables (relative difference 0).
- **Level**: equations 29 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone or discretised component → 0; no
  semi-empirical, off-design or dynamic physics → 0; converges from the
  default guess (16 iterations, 4 with the stored solution) → 0. Score 1 →
  level 1.

## Limitations and CoolSolve gaps

The exit velocity is imposed (`c_out = 274` m/s), not calculated. The inlet
temperature that is solved is 370 °C, which is the equation-window value
after converting kelvin to °C. Absolute enthalpies use the CoolProp
reference of `Water`, which here agrees with the EES steam table to
0.001 J/kg. No CoolSolve gap: `volume`, `enthalpy`, `temperature` and
`entropy` of `Water` run, and the native file is the file that was solved.

## Related models

None.
- `CSL-0310` *isentropic_nozzle_critical*: air nozzle with the critical-pressure (choked/unchoked) test that this steam exercise does not make.
