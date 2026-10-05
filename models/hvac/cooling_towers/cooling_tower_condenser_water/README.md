# Cooling tower for the condenser water of a steam power plant

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0065`

Exercise on a direct-contact (evaporative) cooling tower: the water leaving the
condenser of a steam power plant is cooled by ambient air while part of it
evaporates. Total mass, water, dry-air and energy balances on the tower give
the required air volume flow rate and the make-up water flow rate.

| | |
|---|---|
| **Category** | HVAC › Cooling towers |
| **Fluids** | AirH2O (moist air), Water |
| **Size** | 24 equations (largest block: 3) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), 2022-2023, repetition session R9, exercise 4 (EES file `R09_E04_2022.EES`) |
| **Authors** | TBD (ULiège course *Thermodynamique appliquée*, S. Quoilin; repetition assistants N. Paulus and B. Dechesne per companion metadata) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A cooling tower cools the water of the condenser of a steam power plant. The
water enters the tower at 65 °C and returns to the condenser at 30 °C with the
same mass flow rate, 2.78 kg/s. Ambient air enters the tower at 15 °C with a
relative humidity of 55 % and leaves it saturated at 35 °C. The make-up water
is added at 14 °C. The ambient pressure is 1 bar. Determine the volume flow
rate of air drawn through the tower (at the inlet conditions) and the mass
flow rate of make-up water (bonus: the heat rate given up by the condenser).

## Model

Steady-state balances on a control volume enclosing the tower (states: air
inlet *a_su*, air outlet *a_ex*, spray water *w_su*, basin water *w_ex*,
make-up *add*):

- dry-air balance: $\dot m_{a,ex} = \dot m_{a,su}$ (all dry air entering
  leaves the tower);
- water balance: $\dot m_{a,ex}\,\omega_{ex} + \dot m_{w,ex}
  = \dot m_{a,su}\,\omega_{su} + \dot m_{add} + \dot m_{w,su}$, with
  $\dot m_{w,ex} = \dot m_{w,su}$ (constant condenser flow); the evaporation
  is covered by the make-up water;
- energy balance: $\dot m_{w,su}h_{w,su} + \dot m_{a,su}h_{a,su}
  + \dot m_{add}h_{add} = \dot m_{w,ex}h_{w,ex} + \dot m_{a,ex}h_{a,ex}$. As
  noted in the original, this mixed balance works because the enthalpy
  reference scales of the humid air (AirH2O) and of the water are consistent;
  it would not hold as such with dry air.

The humid-air states ($\omega$, $h$, $v$) are evaluated with the real
humid-air properties of `AirH2O` at (T, P, R); the water enthalpies at
(T, P = 120 kPa). The air volume flow is $\dot V_{a,su} =
\dot m_{a,su}\,v_{a,su}\times 3600$ (m³/h).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `p` ambient pressure | 100 000 Pa | `V_dot_a_su` air volume flow | 12 361 m³/h |
| `m_dot_w_su` condenser water flow | 2.78 kg/s | `m_dot_add` make-up water | 0.129 kg/s |
| `T_w_su` / `T_w_ex` water in / out | 65 / 30 °C | `m_dot_a_su` dry air flow | 4.114 kg/s |
| `T_a_su` / `phi_a_su` air in | 15 °C / 0.55 | `Q_dot_cd` condenser heat rate | −406.9 kW |
| `T_a_ex` / `phi_a_ex` air out | 35 °C / 1 | `w_ex` outlet humidity ratio | 0.0373 kg_w/kg_da |
| `T_w_add` make-up water | 14 °C | | |

`Q_dot_cd = m_dot_w_su*(h_w_ex - h_w_su)` is the heat rate *received* by the
tower water, hence negative here; the condenser gives up 406.9 kW.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. parametric sweep of the
     outlet air temperature T_a_ex: air flow and make-up water vs T_a_ex (humid-air model) -->

## How to run

Open `cooling_tower_condenser_water.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./cooling_tower_condenser_water.eescode
```

No guess file is needed (solves from default guesses in 2 iterations, largest
block of 3 equations).

## Results

See the table above (default inputs). The air flow of 12 361 m³/h for 2.78
kg/s of condenser water and an evaporation (make-up) rate of 0.129 kg/s
(≈ 4.6 % of the water flow) are the answers of the exercise.

## Verification

Reference: the solution stored in the source EES file
(`compare_solution.py cooling_tower_condenser_water.sol reference/ees_variables.csv --ees-units`):
23 common variables, 8 differ (rtol=0.001); largest deviation 5.98e-03 on
`w_ex`. Both deviations classes are explained:

- `w_su`, `w_ex`, `h_a_su`, `h_a_ex`: 0.3–0.6 % — humid-air property backend
  (EES 10 vs CoolProp `AirH2O`); near saturation at 35 °C the humidity ratio
  differs by 0.6 % between the two formulations (slightly above the 0.5 %
  typical property tolerance of `docs/ees_import.md` §11);
- `m_dot_a_su`, `m_dot_a_ex`, `m_dot_add`, `V_dot_a_su`: the EES file stores
  the value 1 for these four variables, i.e. the **default guess, not a
  solution value** (the file was saved unsolved; the stored values are
  inconsistent with its own balances). They were therefore recomputed by hand
  from the EES stored properties: water balance gives
  $\dot m_{add} = \dot m_{a,su}(\omega_{ex}-\omega_{su})$ and the energy
  balance gives $\dot m_{a,su} = \dot m_w (h_{w,su}-h_{w,ex}) /
  (h_{a,ex}-h_{a,su}-(\omega_{ex}-\omega_{su})h_{add})$ = 4.1288 kg/s
  (CoolSolve: 4.1141 kg/s, −0.36 %), `m_dot_add` = 0.1287 kg/s (CoolSolve:
  0.1290 kg/s, +0.28 %), `V_dot_a_su` = 12 410 m³/h (CoolSolve: 12 361
  m³/h, −0.40 %) — within the property-backend deviation above.

All other variables (inputs, water enthalpies, `Q_dot_cd` = −406 867 W)
agree exactly; `Q_dot_cd` depends only on the water properties.

## Source and attribution

Exercise file of the ULiège course *Thermodynamique appliquée*
(MECA0002), repetition session R9, exercise 4, year 2022-2023 (EES 10.836,
comments in French). The file itself names no author; the companion course
metadata credits the course to S. Quoilin with repetition assistants
N. Paulus and B. Dechesne — left `TBD` for the maintainer to confirm.

Source file, collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R9/R09_E04_2022.EES`
(inventory candidate `TM-0454`). No Python/CoolProp solution of this exercise
was found in the source folder.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `SI MASS DEG KPA C KJ` with decimal commas (converted to dots
  by the tool) → converted by hand to SI-°C-Pa-J: `p = 100E3` (100 kPa), the
  three `enthalpy(Water, …)` calls at `P=120E3` (120 kPa); all other equations
  are homogeneous (property calls now return J/kg, balances unchanged; the
  `3600 s/h` factor of `V_dot_a_su` is kept). `$UnitSystem` line removed;
  EES licence/display tags removed; comments translated to English (the
  variable-role comment of the water balance and the remark on the enthalpy
  references are paraphrases of the original); standard header added.
  State points: the model has a single air path and a single water path, no
  cycle arrays were added.
- **2026-10-05 — level**: 24 equations (< 50) = 0, largest block 3 (≤ 5) = 0,
  no functions/arrays = 0, no multi-zone = 0, no calibration/off-design = 0,
  no curated guesses = 0 → score 0 → **level 1** (matches the card).
- **2026-10-05 — merged candidate TM-0536** (`THD10_R10_E4.EES`, 2017-2018
  session, same exercise, extracted from `THD10_R10.zip` for comparison): same
  statement, data and balances with the older names `q_m_*`/`q_v_*`, water
  enthalpies evaluated at saturation (`x=0`, a difference below 0.1 % on
  `h_w`) and the bonus heat rate written positive (`h_w_su - h_w_ex`). Not
  imported as a separate file; described here only.

## Limitations and CoolSolve gaps

- The outlet air is assumed saturated (`phi_a_ex = 1`), as in the original;
  no fan power, no pressure drops, no loss coefficient (level-1 tower
  balance, unlike the ε-NTU model of `CSL-0030`).
- The mixed water/humid-air enthalpy balance relies on the consistency of the
  two enthalpy reference scales (remark of the original); with CoolProp the
  residual reference difference (triple point at 0.01 °C) is negligible
  compared with the 0.3–0.6 % property-backend deviations documented above.
- No blocking CoolSolve gap (`missing_features` empty).

## Related models

- `CSL-0030` *two_speed_cooling_tower*: the same equipment at level 2
  (ε-NTU rating on a fictitious fluid, two-speed fan, part load); here a
  level-1 mass/energy balance exercise on one operating point.
