# Cooling tower water and air sides (exercise)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0232`

Teaching exercise of the ULiège course MSTh (Machines et systèmes
thermiques), repetition 6, exercise 1. A direct-contact cooling tower is
closed on the water side and on the moist-air side. The air side uses the
wet-bulb temperatures and a fictitious capacity rate. The same heat rate
also follows from the moist-air enthalpy change and from the counterflow
effectiveness–NTU relation.

| | |
|---|---|
| **Category** | HVAC and psychrometrics › Cooling towers and evaporative equipment |
| **Fluids** | AirH2O, Water |
| **Size** | 28 equations (largest block: 18) |
| **Source** | thermo_models, file `MSTh-SB-R6-Ex1.EES` (candidate TM-0100) |
| **Authors** | Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see *Verification*) |

## Problem statement

The equation window is headed "MSTh - SB - R6 - Exercice 1" and gives the
data directly:

- overall heat-transfer coefficient `AU` = 90000 W/K
- water mass flow rate 50 kg/s, air mass flow rate 60 kg/s
- inlet water 35 °C
- pressure 101325 Pa
- inlet air 25 °C and relative humidity 0.7
- outlet air relative humidity 1

The water-side heat rate uses the specific heat of liquid water at the mean
water temperature. The original leaves `cp_w = 4187` as a provisional
comment. On the air side the heat rate is written on the wet-bulb rise with
a fictitious capacity rate. The original leaves `cp_a_f = 4000` as a
provisional comment. That specific heat is an unknown: it is fixed by
`AU_f/AU = cp_a_f/cp_a` together with the air-side energy balance. The
effectiveness equation is the counterflow ε-NTU relation, with the smaller
and larger capacity rates from `min()` and `max()`.

## Model

The original equations are kept. Humid air stays `AirH2O`.

- Water side: `Q_dot_ct = C_dot_w*(T_w_su - T_w_ex)`, with
  `cp_w = CP(Water, T=T_w_m, P=P_su)` and
  `T_w_m = (T_w_su + T_w_ex)/2`.
- Wet-bulb temperatures: both calls are
  `WETBULB(AirH2O, T=..., P=P_su, R=...)`.
- Fictitious air side: `Q_dot_ct = C_dot_a_f*(T_wb_ex - T_wb_su)` and
  `C_dot_a_f = M_dot_a*cp_a_f`.
- Moist-air energy balance: `Q_dot_ct = M_dot_a*(h_a_ex - h_a_su)`, with
  both enthalpies from `ENTHALPY(AirH2O, T=..., P=P_su, R=...)`.
- Performance: `Q_dot_ct = epsilon_ct*C_dot_min_f*(T_w_su - T_wb_su)`,
  counterflow effectiveness, `NTU_f = AU_f/C_dot_min_f`, and
  `AU_f/AU = cp_a_f/cp_a` with
  `cp_a = CP(AirH2O, T=T_a_m, P=P_su, R=RH_su)`.

| Inputs | Value |
|---|---|
| `AU` overall heat-transfer coefficient | 90000 W/K |
| `M_dot_w` water mass flow rate | 50 kg/s |
| `M_dot_a` air mass flow rate | 60 kg/s |
| `T_w_su` inlet water temperature | 35 °C |
| `P_su` pressure | 101325 Pa |
| `T_a_su` inlet air dry-bulb temperature | 25 °C |
| `RH_su` inlet air relative humidity | 0.7 |
| `RH_ex` outlet air relative humidity | 1 |

`Q_dot_ct`, `T_w_ex` and `T_a_ex` are computed. The lines `cp_w = 4187` and
`cp_a_f = 4000` in the original are comments.

## How to run

```bash
coolsolve ./cooling_tower_water_air_sides.eescode
```

`cooling_tower_water_air_sides.initials` holds the EES stored solution.
With those guesses the block of 18 takes 3 Newton iterations. Without the
guesses that block stops on a singular Jacobian after 1 Newton iteration.
There is no `coolsolve.conf`.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. |
|---|---:|---:|---:|
| `Q_dot_ct` [W] | 1973285.893541 | 1974133.611 | 4.29e-04 |
| `T_w_ex` [°C] | 25.55791236062 | 25.56132665 | 1.34e-04 |
| `T_a_ex` [°C] | 28.75156562145 | 28.75702397 | 1.90e-04 |
| `omega_f` [-] | 0.8248775838458 | 0.8260166232 | 1.38e-03 |

Absolute moist-air enthalpies, reported separately from the three results
above:

| Quantity | CoolSolve | EES stored | rel. diff. |
|---|---:|---:|---:|
| `h_a_ex` [J/kg] | 93645.08495689 | 93657.06502 | 1.28e-04 |
| `h_a_su` [J/kg] | 60756.9867312 | 60754.83816 | 3.54e-05 |
| `h_a_ex - h_a_su` [J/kg] | 32888.09822569 | 32902.22686 | 4.29e-04 |

The enthalpy difference and `Q_dot_ct` carry the same relative difference,
because `Q_dot_ct = M_dot_a*(h_a_ex - h_a_su)` with `M_dot_a = 60` kg/s on
both sides.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `MSTh-SB-R6-Ex1.EES` (EES X7.458, 28
variables), compared with `compare_solution.py` without `--ees-units`. The
tool's summary line is:

`28 common variables, 1 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The maximum relative difference over all 28 common variables is 1.38e-03
(unrounded 1.3789545e-03) on `omega_f`. `omega_f = C_dot_min_f/C_dot_max_f`,
and at this root that ratio is `C_dot_w/C_dot_a_f`. The relative residual of
`cp_w` is 7.90e-04 (`CP(Water)` at `T_w_m`) and the relative residual of
`C_dot_a_f` is 5.89e-04; they add in the ratio. `AU`, the two mass flows and
the effectiveness formula were left as written.

`Q_dot_ct` differs by 4.29e-04 (1973285.893541 W against 1974133.611 W).
`T_w_ex` differs by 1.34e-04 (25.55791236062 °C against 25.56132665 °C).
`T_a_ex` differs by 1.90e-04 (28.75156562145 °C against 28.75702397 °C).

`h_a_ex` differs by 1.28e-04 and `h_a_su` by 3.54e-05. Their difference
differs by 4.29e-04, the same relative amount as `Q_dot_ct`. The heat-rate
equation on the enthalpy change is satisfied.

With the stored guesses the maximum absolute residual is 1.0664e-07 and all
28 equations are satisfied. Without the guesses the block of 18 does not
converge.

`--ees-units` prints the same summary line and prints no converted names.
The units column of the extracted reference is empty. No equation was scaled.

## Source and attribution

The equation window is titled "MSTh - SB - R6 - Exercice 1". The file name
and that header carry the initials SB, which the library workflow maps to
Stéphane Bertagnolio. The EES licence tag is the ULiège thermodynamics
laboratory licence (`{$ID$ #202}`), the licence holder, and is omitted from
the model.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 06/SB/MSTh-SB-R6-Ex1.EES`.

Candidate TM-0100. No duplicate group. Teaching exercise. Course: ULiège
MSTh, repetition 6, exercise 1. EES X7.458. Language of the source: French.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `MSTh-SB-R6-Ex1.EES` (EES X7.458, plain text, 28 variables, no tables, no warnings). The unit system recorded for the window is `SI MASS DEG PA C J`. `$UnitSystem` was deleted. The equation window contains no `$TABSTOPS` and no `$Export`. Comments translated to English. Both `WETBULB(AirH2O, ...)` calls, both `ENTHALPY(AirH2O, ...)` calls, `CP(Water, ...)` and `CP(AirH2O, ...)` are unchanged. `min()` and `max()` are unchanged. The comments `"cp_w=4187"` and `"cp_a_f=4000"` stay comments; they were not restored as equations. No diagram-state arrays (humid air). The figure placeholder is left for the maintainer.
- **Units**: already SI. No input, equation, constant or guess was scaled. `.initials` are the stored solution as extracted. `--ees-units` rewrote no name.
- **Square system**: with `$UnitSystem` removed, CoolSolve reports `System square: Yes` (28 equations, 28 variables, largest block 18). No stored unknown was added.
- **Level**: equations 28 → 0; largest block 18 → 1; no function, procedure, array or `DUPLICATE` → 0; one tower, not three coupled components → 0; no calibration, off-design or dynamics → 0; the block of 18 needs the stored guesses (singular Jacobian after 1 Newton iteration without them) → 1. Score 2 → level 2.

## Limitations and CoolSolve gaps

The outlet air is taken as saturated (`RH_ex = 1`), as written. `AU` is an
input at this one operating point.

CoolSolve prints `CP(): t=30.2807 looks like Fahrenheit (water freezing (0 °C)). CoolSolve uses Celsius: T=-0.96.` The mean water temperature in the solution is 30.279 °C, next to the stored 30.281 °C, so `T_w_su = 35` and `T_a_su = 25` stay as written.

`omega_f` is the one common variable above the compare tolerance. It is the
capacity-rate ratio, and the water and moist-air specific heats differ
slightly between EES and CoolProp. The effectiveness formula was not changed
to force a closer root.

`missing_features` is empty.

## Related models

- `CSL-0287` *cooling_tower_chiller_variable_airflow*: the same tower core
  (counter-flow effectiveness, fictitious air side, saturated outlet) coupled to a
  chiller and to a variable-flow fan.
