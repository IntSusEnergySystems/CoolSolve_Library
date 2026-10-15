# 1 GW steam plant cooled by a river (exercise 1)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0195`

Teaching exercise. A 1 GW steam plant rejects condenser heat to a river. The
plant is not built state by state: its efficiency is taken as half the Carnot
value between the maximum steam temperature and the condenser saturation
temperature. The river temperature rise follows from that heat and from the
river cross-section and velocity.

| | |
|---|---|
| **Category** | Cycles and machines › Steam power cycles |
| **Fluids** | Water |
| **Size** | 18 equations, all explicit (largest block: 1) |
| **Source** | ULiège MECA0002, repetition R4, exercise 1 (2022-2023), file `R04_E1_2022.EES` |
| **Authors** | S. Quoilin — the file itself names nobody |
| **License** | MIT |
| **CoolSolve** | 0.3.0@f5b79cd — verified against the EES stored solution |

## Problem statement

Exercise 1 of repetition R4 (2022-2023), as written in the equation window.
A 1 GW electric power plant would use steam as its working fluid. The
condensers would be cooled by a river. The maximum steam temperature would be
550 °C and the condenser pressure 10 kPa. Estimate the river temperature rise
caused by the plant. The statement says that further data are on the figure.

The opening statement does not give an efficiency. The resolution in the
equation window assumes that the real efficiency is half the Carnot efficiency,
with the hot source at the maximum steam temperature and the cold source at
the saturation temperature for 10 kPa. That is the calculation that is solved.
The equation window has no turbine stages, no pump, no feedwater heater and no
cooling tower.

## Model

Steady balances. The original unit system is kelvin, kPa and kJ; CoolSolve
stores temperatures in °C, pressures in Pa and energies in J. The Carnot
ratio uses absolute temperatures.

- **Plant power:** \(\dot W = -1\,\mathrm{GW}\) (negative because the plant produces it).
- **Hot source:** \(T_C = T_\mathrm{vap} = 550\,^\circ\mathrm{C}\). In the original kelvin system this is `550 [K] + 273.15 [K]`.
- **Cold source:** \(T_{F2} = T_\mathrm{sat}(\mathrm{Water}, p_\mathrm{cond})\) and \(T_F = T_{F2}\). The equation window computes \(T_{F2}\) and uses \(T_F\) without assigning it; the comment on \(T_{F2}\) is “identique”.
- **Efficiencies:** \(\eta_\mathrm{Carnot} = 1 - T_{F,\mathrm{K}}/T_{C,\mathrm{K}}\), \(\eta = 0.5\,\eta_\mathrm{Carnot}\), \(\eta = -\dot W / \dot Q_\mathrm{gen}\).
- **Cycle balance:** \(\dot W + \dot Q_\mathrm{gen} + \dot Q_\mathrm{cond} = 0\).
- **River:** \(\dot Q_r = -\dot Q_\mathrm{cond} = \dot q_{v,r}\,\rho\,c\,\Delta T\), with \(A_r = 480\,\mathrm{m}^2\), \(c_r = 10/60\,\mathrm{m/s}\), \(\rho = 1000\,\mathrm{kg/m}^3\) and \(c = 4184\,\mathrm{J/kg\cdot K}\).

`c_eau_2` is `SpecHeat` of water at 15 °C and 100 kPa. The original computes
it as a check. It does not enter the river balance, which keeps the constant
4.184 kJ/kg-K.

| Inputs | Value | Outputs | CoolSolve |
|---|---|---|---|
| `W_dot` | −1 GW | `DELTAT` | 6.7675 K |
| `T_vap` | 550 °C | `Q_dot_cond` | −2.2652 GW |
| `p_cond` | 10 kPa | `eta` | 0.30626 |
| `A_r` | 480 m² | `q_v_r` | 80 m³/s |
| `c_r` | 1/6 m/s | `eta_carnot` | 0.61252 |
| `C_eau` | 4184 J/kg-K | `T_F` | 45.806 °C |

## How to run

Open `power_plant_cooling_river.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./power_plant_cooling_river.eescode
```

The system is square and fully explicit (18 blocks of size 1). There is no
`abs()` and only one root. Without `.initials` CoolSolve reaches that root in
65 iterations. The shipped `.initials` are the stored EES solution converted
to SI (°C, Pa, J) and bring the iteration count to 6.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| Net power `W_dot` | −1 GW | −1 GW |
| Condenser heat `Q_dot_cond` | −2.265214 GW | −2.265209 GW |
| Steam-generator heat `Q_dot_gen` | 3.265214 GW | 3.265209 GW |
| River heat `Q_dot_r` | 2.265214 GW | 2.265209 GW |
| River volume flow `q_v_r` | 80 m³/s | 80 m³/s |
| River mass flow \(\rho q_v\) | 80 000 kg/s | 80 000 kg/s |
| River temperature rise `DELTAT` | 6.767488 K | 6.767473 K |
| Cold temperature `T_F` | 45.80633 °C | 45.80558 °C |
| Efficiency `eta` | 0.306259 | 0.306259 |

The river mass flow is the product \(\rho\,q_v\). It is not a separate
variable. The cycle energy balance \(\dot W + \dot Q_\mathrm{gen} + \dot Q_\mathrm{cond}\)
is an equation of the model; the solved values sum to zero.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![River temperature rise](figures/power_plant_cooling_river.png)  + one-line caption.
     The equation window has no state-point arrays, so there is no cycle to overlay. -->

## Verification

Compared with the solution stored in `R04_E1_2022.EES` by
`compare_solution.py --ees-units` (kPa→Pa, kJ→J, kW→W, and K→°C for names
that start with `T`). The tool's summary line is:

`18 common variables, 0 differ (rtol=0.001); only in EES: 8; only in CoolSolve: 0`

`verification.max_rel_diff` is **1.64e-05**, the maximum the tool prints over
all 18 common variables, on `T_F` and `T_F2`. Nothing is above rtol 0.001.

**Saturation temperature (the largest difference).** Stored `T_F` is
318.9555786 K, which `--ees-units` converts to 45.8055786 °C. CoolSolve
`T_sat` at 10 kPa returns 45.8063289 °C. Absolute difference 0.00075 °C,
relative 1.64e-05 on the Celsius value. `T_F2` is the same number. The
equation window computes no enthalpy and no entropy, so there is no `h` or
`s` residual to separate from the powers.

**Powers, river flow and temperature rise.** These follow from that
saturation temperature through the Carnot factor. Their relative differences
stay smaller: `eta` and `eta_carnot` 1.49e-06, `Q_dot_gen` 1.49e-06,
`Q_dot_cond` and `Q_dot_r` 2.14e-06, `DELTAT` 2.15e-06. `W_dot` and `q_v_r`
match exactly. `DELTAT` is a temperature difference; its EES unit is K and
its name does not start with `T`, so `--ees-units` leaves 6.767473344
unchanged, which is the correct °C rise.

**Specific heat check.** `c_eau_2` differs by 5.90e-11 (4188.465 J/kg-K).
The river balance does not use it. It uses the constant `C_eau` = 4184 J/kg-K
(4.184 kJ/kg-K in the original), which matches exactly.

**Only in EES.** `P` and `p[1]`…`p[7]` (eight names) are in the stored
variable table and are not in the equation window. They were not added.
`P` has no unit and the value 1. The pressures run from 6200 kPa down to
9 kPa. The equation window contains no array.

## Source and attribution

The equation window names no person. The licence tag
`{$ID$ #0202: For use only by students and staff at the Laboratoire de Thermodynamique, University of Liege PoloUHB}`
is the licence holder, not an author, and is not listed. The inventory
attributes the course to S. Quoilin, so the author is S. Quoilin.

Source file (EES X10.836, French comments, decimal comma, unit system
SI mass, degrees, kPa, K, kJ):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R4/R04_E1_2022.EES`
(inventory candidate `TM-0421`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): 48 equation-window lines,
  26 stored variables, no lookup or parametric table. Unit system
  `$UnitSystem SI MASS DEG KPA K KJ`. Decimal commas were rewritten as dots
  (`273,15`, `4,184`, `1,0`, `0,5`). The licence tag was removed.
  `$UnitSystem` was deleted. The file has no `$Export`, `concat$`,
  `EESFILEDIR$` or `$TABSTOPS`.
- **2026-10-15 — units.** kW→W (`W_dot` −1e6 kW → −1e9 W, and the three heat
  rates), kPa→Pa (`p_cond` 10 kPa → 10 kPa expressed as 10e3 Pa;
  `SpecHeat` pressure 100 kPa → 1e5 Pa), kJ→J (`C_eau` 4.184 kJ/kg-K →
  4184 J/kg-K). The equation window stores temperatures in kelvin, as the
  unit column says: `T_vap = 550 [K] + 273.15 [K]` is 823.15 K, and `T_sat`
  returns kelvin. CoolSolve stores 550 °C and a Celsius saturation
  temperature. The Carnot line, which divided those kelvin values, is
  `1 - (T_F + 273.15)/(T_C + 273.15)`. `DELTAT` is a difference and is
  unchanged. The opening statement writes 550 °C; the kelvin arithmetic
  is the same temperature, not a conflicting value.
- **2026-10-15 — square system.** The extracted equation window has 17
  equations and 18 unknowns (`System square: No`). `T_F` is used in the
  Carnot factor and never assigned. The next line is
  `T_F2 = T_sat(water, P=p_cond)` with the comment “identique”, and the
  paragraph above it says the cold source is that saturation temperature.
  The shipped file adds `T_F = T_F2`. That is not a stored number in place
  of a computed unknown: both temperatures are still the saturation
  temperature at `p_cond`. Guesses of the unknowns stay in `.initials`.
- **2026-10-15 — not added.** The stored solution also holds `P` and
  `p[1]`…`p[7]`. The equation window has no arrays and no diagram-state
  equations, so none were added. No second turbine and no cooling tower
  were added. A UTF-16 fragment in the file still contains an older line
  `T_F = T_sat(Steam, …)`, from the 2010 wording of the exercise. The
  plain-text equation window is the 2022 text (half the Carnot efficiency,
  `T_F2`, fluid `Water`), and that is what was imported. `TM-0514` was not
  imported and its inventory row was not edited.
- **2026-10-15 — initials.** One root (18 blocks of size 1, no `abs()`).
  `.initials` are the stored solution in SI and are that root. Without
  initials: 65 iterations. With these initials: 6 iterations.
- **Level** (taxonomy.md §3): equations 18 → 0; largest block 1 → 0; no
  function, procedure, array or `DUPLICATE` → 0; one Carnot factor and one
  river balance, not a multi-zone or three-component coupling → 0; fixed
  efficiency assumption, design point → 0; converges from default guesses,
  no `coolsolve.conf` → 0. Score 0 → level 1. No pedagogical shift.

## Limitations and CoolSolve gaps

- The plant is a Carnot bound at half the Carnot efficiency. Steam states,
  a turbine, a pump and a cooling tower are not in the equation window.
- The river uses a constant specific heat of 4184 J/kg-K. `c_eau_2` is only
  a check at 15 °C and 100 kPa.
- Saturation temperature differs from EES by 0.00075 °C; see Verification.
  No CoolSolve gap blocks this model.

## Related models

`related` is empty. `CSL-0191` (*steam_reheat_power_plant*) is an 80 MW
reheat Rankine cycle solved state by state. `CSL-0053`
(*steam_power_plant_elementary*) is a component-by-component plant with seven
given states. Neither uses this Carnot bound or this river balance, so they
are not linked.
