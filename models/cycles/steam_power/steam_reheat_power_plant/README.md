# Steam power plant with reheat (Cengel exercise 10-34)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0191`

Steady reheat Rankine cycle on water, solved state by state. Saturated liquid
is pumped from the condenser, boiled, expanded, reheated once and expanded
again. The net power is imposed at 80 MW; the model returns the thermal
efficiency and the steam mass flow.

| | |
|---|---|
| **Category** | Cycles and machines › Steam power cycles |
| **Fluids** | Water |
| **Size** | 37 equations, all explicit (largest block: 1) |
| **Source** | KU Leuven thermodynamics exercise, file `10-34.EES` (Cengel exercise 10-34) |
| **Authors** | TBD (KU Leuven thermo) — the file names no person |
| **License** | MIT |
| **CoolSolve** | 0.3.0@3e9c1b6 — verified against the EES stored solution |

## Problem statement

Textbook exercise Cengel 10-34, as solved in the source file. A steam power
plant with one reheat delivers a net power of 80 MW. At the pump inlet the
water is saturated liquid at 10 kPa. The pump (isentropic efficiency 0.95)
discharges at 10 MPa. Steam enters the high-pressure turbine at 10 MPa and
500 °C, expands to 1 MPa (isentropic efficiency 0.80), is reheated to 500 °C
at that pressure, and expands in the low-pressure turbine to 10 kPa at the
same isentropic efficiency. Determine the thermal efficiency and the steam
mass flow.

The equation window has one reheat and one turbine efficiency, used for both
stages. It does not add a second reheat, an open or closed feedwater heater,
a cooling-water stream, or the moisture at the turbine exit.

## Model

Steady flow. Kinetic and potential energy are absent from the original
equations. Pressures are equal across the boiler (`p_2 = p_3`), the reheater
(`p_4 = p_5`) and the condenser connection (`p_6 = p_1`).

- **Pump inlet (1):** \(x_1 = 0\), \(p_1 = 10\,\mathrm{kPa}\).
- **Pump:** \(p_2 = p_3\) and \(\eta_\mathrm{pump} = (h_{2s} - h_1)/(h_2 - h_1)\) with \(s_{2s} = s_1\).
- **Boiler (2 → 3):** heat addition to \(T_3 = 500\,^\circ\mathrm{C}\) at \(p_3 = 10\,\mathrm{MPa}\).
- **HP turbine (3 → 4):** \(\eta_\mathrm{tur} = (h_3 - h_4)/(h_3 - h_{4s})\), \(p_4 = 1\,\mathrm{MPa}\), \(s_{4s} = s_3\).
- **Reheat (4 → 5):** heat addition to \(T_5 = 500\,^\circ\mathrm{C}\) at \(p_5 = 1\,\mathrm{MPa}\).
- **LP turbine (5 → 6):** the same \(\eta_\mathrm{tur}\), exit at \(p_6 = 10\,\mathrm{kPa}\). The original does not compute \(s_6\) or the exit quality.
- **Cycle:** \(w_\mathrm{net} = w_\mathrm{hp} + w_\mathrm{lp} - w_\mathrm{pump}\), \(q_\mathrm{in} = (h_3 - h_2) + (h_5 - h_4)\), \(\eta = w_\mathrm{net}/q_\mathrm{in}\), \(\dot W_\mathrm{net} = \dot m\, w_\mathrm{net}\).

| Inputs | Value | Outputs | CoolSolve |
|---|---|---|---|
| `W_dot_net` | 80 MW | `eta_cycle` | 0.3405 |
| `p_3`, `T_3` | 10 MPa, 500 °C | `M_dot` | 62.65 kg/s |
| `p_5`, `T_5` | 1 MPa, 500 °C | `w_net` | 1.277 MJ/kg |
| `eta_tur` | 0.80 | `q_in` | 3.750 MJ/kg |
| `eta_pump` | 0.95 | `T_4` | 231.6 °C |
| `p_1`, `x_1` | 10 kPa, 0 | `T_6` | 88.08 °C |

## How to run

Open `steam_reheat_power_plant.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./steam_reheat_power_plant.eescode
```

The system is square and fully explicit (37 blocks of size 1). The turbine
and pump efficiencies are linear in the unknown outlet enthalpy, so there is
one root. Without `.initials` CoolSolve still reaches that root (112
iterations). The shipped `.initials` are the stored EES solution, including
`x_1 = 0`, and bring the iteration count to 12.

CoolSolve prints a warning that `t=500` is read as 500 °C. That is the
temperature in the exercise; the value is not a kelvin figure.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| Net power `W_dot_net` | 80 MW | 80 MW |
| Thermal efficiency `eta_cycle` | 0.34052 | 0.34057 |
| Steam mass flow `M_dot` | 62.651 kg/s | 62.653 kg/s |
| Net specific work `w_net` | 1.27691 MJ/kg | 1.27688 MJ/kg |
| Heat input `q_in` | 3.74986 MJ/kg | 3.74922 MJ/kg |
| HP turbine work `w_hp` | 0.47316 MJ/kg | 0.47299 MJ/kg |
| LP turbine work `w_lp` | 0.81435 MJ/kg | 0.81449 MJ/kg |
| Pump work `w_pump` | 10.601 kJ/kg | 10.601 kJ/kg |
| HP exit temperature `T_4` | 231.58 °C | 231.71 °C |
| LP exit temperature `T_6` | 88.08 °C | 87.97 °C |
| Live-steam temperatures `T_3`, `T_5` | 500 °C | 500 °C |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![T-s diagram of the reheat cycle](figures/steam_reheat_power_plant_ts.png)  + one-line caption.
     States are already named p_i, T_i, h_i, s_i for i = 1…5, and p_6, T_6, h_6 (the original does not compute s_6). -->

## Verification

Compared with the solution stored in `10-34.EES` by `compare_solution.py`
(no `--ees-units`). The tool's summary line is:

`37 common variables, 1 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

`verification.max_rel_diff` is **1.26e-03**, the maximum over all 37 common
variables, on `T_6`. Every other variable is within rtol 0.001. Pressures,
both efficiencies, `x_1` and `W_dot_net` match exactly.

**`T_6` (the only difference above the tolerance).** Stored value
87.9729 °C, CoolSolve 88.0841 °C, absolute difference 0.111 °C. Two property
effects nearly cancel:

- at the stored enthalpy `h_6` = 2.664065 MJ/kg and 10 kPa, CoolSolve
  `temperature(Water, P, H)` returns 87.724 °C, 0.249 °C below the stored
  temperature;
- the solved `h_6` is 687 J/kg higher than the stored enthalpy, which raises
  the temperature by about 0.36 °C (local specific heat near 1.9 kJ/kg-K).

The relative figure is 1.26e-03 because the denominator is the Celsius value
(about 88), not kelvin.

**Enthalpies and entropies** stay under the tolerance. They are not a
reference-state offset: a constant shift would move every enthalpy by the
same amount. Liquid states differ by about 87 J/kg (`h_1`: stored
191719 J/kg, CoolSolve 191806 J/kg, relative 4.55e-04; `s_1` relative
4.62e-04, about 0.30 J/kg-K). Vapour enthalpies differ by 550 to 1130 J/kg
(relative 1.58e-04 to 3.35e-04) and vapour entropies by about 1.9 to
2.5 J/kg-K (relative 2.47e-04 to 3.65e-04). The largest enthalpy relative
difference is `h_1` at 4.55e-04; the largest entropy relative difference is
`s_1` at 4.62e-04.

The energy equations themselves are satisfied: CoolSolve reports all 37
equations satisfied, maximum absolute residual 6.41e-10. The h and s
differences against EES are the steam-property formulation (CoolProp versus
the EES water properties), propagated through explicit balances.

The extracted `ees_variables.csv` units column is empty. Stored enthalpies
are already in joules (`h_1` ≈ 1.92×10⁵ J/kg, not 192 kJ/kg), consistent with
`$UnitSystem SI MASS DEG PA C J`. A `kJ/kg` fragment in the binary sits among
other unit labels and is not a per-variable unit in the extracted table.
`--ees-units` was not used. An uppercase `KJ` string, had one been stored on
a value that is already in joules, would not have been scaled by that flag
either; nothing here was treated as a unit-conversion error.

## Source and attribution

The equation window and the file header name no person. The EES licence tag
`{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege Owner}`
is the licence holder, not an author, and is not listed. Authors:
TBD (KU Leuven thermo). The exercise is Cengel 10-34 (a steam power plant
with reheat, net power 80 MW). Cengel is not listed as an author.

Source file (EES X8.940, comments already in English, decimal comma,
unit system SI mass, degrees, Pa, °C, J):
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/10-34.EES`
(inventory candidate `TM-0348`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): 37 equations, 37 stored
  variables, no lookup or parametric table, no warnings. `$UnitSystem SI MASS DEG PA C J`
  was deleted; the values were already in that system, so nothing was
  rescaled. The licence tag was removed. The diagram-window RTF is empty and
  the system is square, so no diagram input was turned into an equation.
  No state-point arrays were added: the equation window does not contain
  them. The fluid name is written `Water` (the original calls `water`, the
  same real fluid). Property calls keep `t=` for temperature in °C.
  Comments stay in English and carry SI units. `s_6` and an exit quality are
  not in the original and were not added.
- **2026-10-15 — initials.** The efficiency definitions are linear in the
  unknown enthalpy (one root). `.initials` are the stored solution.
  `ees_extract.py` had written `x_1 = 1`, which is the EES guess; the stored
  value and the equation are `x_1 = 0`, and that is what is shipped. Without
  initials: 112 iterations. With these initials: 12 iterations. Same root.
- **2026-10-15 — not imported.** `10-34b.EES` (TM-0349) is a longer array
  form of the same exercise and stays `todo`. It was not copied and its
  inventory row was not edited.
- **Level** (taxonomy.md §3): equations 37 → 0; largest block 1 → 0; no
  function, procedure, array or `DUPLICATE` → 0; components are a chain of
  explicit balances, not a multi-zone or coupled implicit system → 0; fixed
  isentropic efficiencies, design point → 0; converges from default guesses,
  no `coolsolve.conf` → 0. Score 0 → level 1. A textbook exercise with
  explicit equations; no pedagogical shift.

## Limitations and CoolSolve gaps

- One reheat only, and the same isentropic efficiency on both turbine stages,
  as in the equation window. No feedwater heater, no boiler or reheater
  pressure drop, no cooling-water balance.
- The low-pressure turbine exit entropy and quality are not computed.
- Steam properties differ slightly from the EES implementation; see
  Verification. `T_6` is 0.11 °C higher. No CoolSolve gap blocks this model.

## Related models

- `CSL-0208` *steam_reheat_power_plant_arrays*: the same 80 MW reheat cycle
  written with state arrays (Cengel 10-34b, inventory TM-0349).
- `CSL-0053` (*steam_power_plant_elementary*) is a different plant: component
  balances from seven given states, with pressure drops and kinetic energy.
  `CSL-0174` is a single steam turbine. Neither is linked.
