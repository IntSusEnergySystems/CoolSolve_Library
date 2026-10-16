# Evaporative condenser as a semi-isothermal exchanger (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0227`

Nominal point of an evaporative condenser treated as a semi-isothermal
exchanger. The air-side heat rate sets the capacity rate `C_dot_a_f` from
the inlet and outlet wet-bulb temperatures. The effectiveness, the NTU and
the overall exchange coefficient `AU_f` then follow. The exchange
coefficient is assumed constant. Teaching exercise of the ULiège course
MSTh (Machines et systèmes thermiques), repetition 5, exercise 3
(continued).

| | |
|---|---|
| **Category** | HVAC and psychrometrics › Air handling |
| **Fluids** | AirH2O |
| **Size** | 13 equations (largest block: 1) |
| **Source** | thermo_models, file `R5 - SB - Ex 3.EES` (candidate TM-0086) |
| **Authors** | Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see *Verification*) |

## Problem statement

Nominal conditions of an evaporative condenser, as written in the equation
window "MSTh - SB - R5 - Exercice 3 (suite)":

- condenser heat rate 35 000 W
- air from 25 °C and relative humidity 0.6 to 30 °C and relative humidity 1
- air pressure 101 325 Pa
- condenser temperature 45 °C

A semi-isothermal exchanger is assumed. On the air side the heat rate is
written between the outlet and inlet wet-bulb temperatures. Determine the
air-side capacity rate, the effectiveness, the NTU and `AU_f`. The original
records the result `AU_f = 1767` and states that the exchange coefficient is
assumed constant.

## Model

Both wet-bulb temperatures are `WETBULB(AirH2O, T=..., P=P_a, R=...)`.

- `Q_dot_cd = C_dot_a_f*(T_wb_ex - T_wb_su)` sets the air-side capacity rate.
- `Q_dot_cd = epsilon_cd*C_dot_a_f*(T_cd - T_wb_su)` sets the effectiveness.
- `epsilon_cd = 1 - exp(-NTU_f)` and `NTU_f = AU_f/C_dot_a_f` set the NTU
  and the exchange coefficient.

| Inputs | Value |
|---|---|
| `Q_dot_cd` condenser heat rate | 35 000 W |
| `T_a_su` inlet air dry-bulb temperature | 25 °C |
| `T_a_ex` outlet air dry-bulb temperature | 30 °C |
| `P_a` air pressure | 101 325 Pa |
| `RH_su` inlet relative humidity | 0.6 |
| `RH_ex` outlet relative humidity | 1 |
| `T_cd` condenser temperature | 45 °C |

`C_dot_a_f`, `epsilon_cd`, `NTU_f` and `AU_f` are computed. The line
`AU_f = 1767` in the original is a comment (the stored result, rounded).

## How to run

```bash
coolsolve ./evaporative_condenser_effectiveness.eescode
```

`evaporative_condenser_effectiveness.initials` holds the EES stored
solution. With those guesses the solver takes 9 iterations. Without the
guesses it takes 20 iterations. Both runs satisfy all 13 equations. There
is no `coolsolve.conf`.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `epsilon_cd` [-] | 0.4125150692 | 0.4125815508 | 1.61e-04 |
| `AU_f` [W/K] | 1767.532925 | 1767.424196 | 6.15e-05 |
| `C_dot_a_f` [W/K] | 3323.025689 | 3322.114247 | 2.74e-04 |
| `NTU_f` [-] | 0.5319046830 | 0.5320178852 | 2.13e-04 |
| `T_wb_su` [°C] | 19.46743020 | 19.46454053 | 1.48e-04 |
| `T_wb_ex` [°C] | 30 | 30 | 0 |

The comment in the equation window rounds the exchange coefficient to
`AU_f = 1767`. The stored solution is 1767.424196 W/K. CoolSolve gives
1767.532925 W/K.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `R5 - SB - Ex 3.EES` (EES X7.458, 13
variables), compared with `compare_solution.py` without `--ees-units`. The
tool's summary line is:

`13 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The maximum relative difference over all 13 common variables is 2.74e-04
(unrounded 2.742806e-04) on `C_dot_a_f`. It follows from the inlet wet-bulb
temperature: CoolSolve 19.46743020 °C, EES 19.46454053 °C (1.48e-04). The
same humid-air residual appears in `epsilon_cd` (1.61e-04), `NTU_f`
(2.13e-04) and `AU_f` (6.15e-05). `T_wb_ex` is 30 °C on both sides, which
is the wet-bulb temperature of saturated air at the outlet dry-bulb
temperature.

`Q_dot_cd`, `T_a_su`, `T_a_ex`, `P_a`, `RH_su`, `RH_ex` and `T_cd` match.

With the stored guesses the maximum absolute residual is 7.2760e-12 and
every equation is satisfied. Without the guesses the maximum absolute
residual is 2.9272e-10 and every equation is satisfied.

`--ees-units` prints the same summary line and prints no converted names.
The units column of the extracted reference is empty, except `epsilon_cd`,
whose units cell is `-`. No equation was scaled.

## Source and attribution

The equation window is titled "MSTh - SB - R5 - Exercice 3 (suite)". The
file name carries the initials SB, which the library workflow maps to
Stéphane Bertagnolio. The EES licence tag is the ULiège thermodynamics
laboratory licence (`{$ID$ #202}`), the licence holder, and is omitted from
the model.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 05/SB/R5 - SB - Ex 3.EES`.

Candidate TM-0086, the representative of duplicate group DG-0019. Teaching
exercise. Course: ULiège MSTh, repetition 5, exercise 3 (continued). EES
X7.458. Language of the source: French.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R5 - SB - Ex 3.EES` (EES X7.458, plain text, 13 variables, no tables, no warnings). The unit system recorded for the window is `SI MASS DEG PA C J`. `$UnitSystem` was deleted. The equation window contains no `$TABSTOPS` and no `$Export`. Comments translated to English. Both `WETBULB(AirH2O, T=..., P=..., R=...)` calls are unchanged. The comment `"AU_f=1767"` was left as a comment. No diagram-state arrays (humid air).
- **Units**: already SI. No input, equation, constant or guess was scaled. `.initials` are the stored solution as extracted.
- **Square system**: with `$UnitSystem` removed, CoolSolve reports `System square: Yes` (13 equations, 13 variables, largest block 1). No stored unknown was added.
- **Level**: equations 13 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one exchanger, not discretised → 0; no calibration, off-design or dynamics → 0; converges with and without the stored guesses, no `coolsolve.conf` → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

The exchange coefficient is the result of this nominal point and is assumed
constant, as in the original comment. The file does not sweep another
operating point.

CoolSolve prints `WETBULB(): t=30 looks like Fahrenheit (water freezing (0 °C)). CoolSolve uses Celsius: T=-1.11.` The outlet wet-bulb temperature in the solution is 30 °C, the stored value, so both `WETBULB` calls stay on `AirH2O` with the original arguments.

The inlet wet-bulb temperature differs from the stored value by 1.48e-04, a humid-air property residual. The heat-rate equations remain satisfied.

`missing_features` is empty.

## Related models

`related` is empty.
