# Exercise: cooling tower at nominal and half fan speed

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0215`

Teaching exercise from ULiège MSTh, repetition R6, exercise 2. A direct-contact
cooling tower is rated as a fictitious dry counterflow heat exchanger, once at
the nominal fan speed and once at half speed. The temperatures of that
fictitious fluid are the wet-bulb temperatures of the moist air, and the air
leaving the tower is saturated. A fraction `theta` then mixes the two regimes
at an outlet-water setpoint.

| | |
|---|---|
| **Category** | HVAC and psychrometrics › Cooling towers and evaporative equipment |
| **Fluids** | Moist air (`AirH2O`); water with constant c = 4187 J/(kg·K) |
| **Size** | 59 equations (largest block: 13) |
| **Source** | ULiège MSTh, repetition R6, exercise 2 (header date 2024-10-05) |
| **Authors** | TBD (ULiège MSTh). The file names no person. The course is attributed to J. Lebrun, V. Lemort and S. Bertagnolio. |
| **License** | MIT |
| **CoolSolve** | 0.3.0@62d92f0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

The equation window is headed "MSTh 241005 - R6 - Exercice 2". The original
comments say to duplicate the equations with an index `r` for the reduced
regime, and that the reduced regime is at half speed. Translated from the
original comment on the fictitious fluid:

> Working with fictitious values amounts to imagining a fictitious dry ideal
> fluid whose temperatures are the wet-bulb temperatures.

Data, as written: dry overall heat-transfer coefficient 90000 W/K; water and
air flow rates 50 and 60 kg/s; inlet water 35 °C; atmosphere 101325 Pa; inlet
air 25 °C and relative humidity 0.70. The outlet air is taken as saturated
(`RH_ex = 1`). At half speed the dry coefficient and the air flow are halved.
The fan power at nominal speed is 15000 W and the fan efficiency is 0.60,
taken as constant. The effectiveness equation is the counterflow ε-NTU
relation, written once for each regime.

The operating-regime block mixes the two outlet water temperatures and the
two fan powers with a weight `theta`. The equation window comments a trial
`T_w_ex_set = 25` and does not assign `theta`. The stored solution holds
`theta` = 0. That stored value is the input used here.

## Model

The tower is closed as a dry counterflow exchanger between the water and the
fictitious fluid on the wet-bulb temperatures. The original equations are
kept, including the suffix `_r` on the half-speed regime:

- inlet moist air: specific heat `cp_a`, humidity ratio `w_a_su`, enthalpy
  `h_a_su` and wet-bulb temperature `T_wb_su` from `AirH2O` at 25 °C,
  101325 Pa and relative humidity 0.70;
- outlet air saturated, so the wet-bulb temperature is `wetbulb` at
  `R = 1`, with the humidity ratio at that state;
- fictitious specific heat from
  \(h_{a,ex} - h_{a,su} = c_{p,a,f}(T_{wb,ex} - T_{wb,su})\),
  and the same relation with the suffix `_r`;
- \(AU_f = AU_{dry}\, c_{p,a,f}/c_{p,a}\) and
  \(AU_{f,r} = AU_{dry,r}\, c_{p,a,f,r}/c_{p,a}\), with
  \(AU_{dry,r} = AU_{dry}/2\) and \(\dot m_{a,r} = \dot m_a/2\);
- counterflow effectiveness–NTU on each regime;
- the same heat rate from the water, from the effectiveness and from the
  fictitious air side;
- fan: \(\dot W = \dot V_a \Delta p / \eta\) and
  \(v_a \Delta p = C_a^2/2\), and the same relations at half speed with the
  same inlet specific volume and the same efficiency;
- \(T_{w,ex,set} = \theta T_{w,ex} + (1-\theta) T_{w,ex,r}\) and
  \(\dot W_{mean} = \theta \dot W + (1-\theta) \dot W_r\).

The original evaluates the half-speed outlet enthalpy at the nominal outlet
dry-bulb:

`h_a_ex_r = enthalpy(AirH2O, T=T_a_ex, P=P_atm, w=w_a_ex_r)`.

That call is kept. The original leaves commented provisional values
`cp_a_f = 4000` and `cp_a_f_r = 4000`. They are not equations.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `AU_dry` dry overall heat-transfer coefficient | 90000 W/K | `T_w_ex` nominal outlet water | 25.555 °C |
| `M_dot_w` water flow | 50 kg/s | `Q_dot` nominal heat rate | 1.977 MW |
| `M_dot_a` nominal air flow | 60 kg/s | `T_a_ex` nominal outlet dry-bulb | 28.765 °C |
| `T_w_su` inlet water | 35 °C | `T_w_ex_r` half-speed outlet water | 29.400 °C |
| `T_a_su` / `RH_su` / `P_atm` | 25 °C / 0.70 / 101325 Pa | `Q_dot_r` half-speed heat rate | 1.172 MW |
| `W_dot` / `eta` | 15000 W / 0.60 | `M_dot_a_r` half-speed air flow | 30 kg/s |
| `theta` time fraction at nominal speed | 0 | `W_dot_r` half-speed fan power | 1875 W |

## How to run

Open `cooling_tower_half_speed.eescode` in the CoolSolve GUI and press
*Solve*, or from the model folder:

```bash
coolsolve ./cooling_tower_half_speed.eescode
```

The shipped `cooling_tower_half_speed.initials` holds the EES stored solution
as guesses. Those guesses select the stored positive air velocities
(`C_a` = 17.32 m/s, `C_a_r` = 8.66 m/s). The velocity-head equations are
quadratic in the velocities; CoolSolve solves each of them as a block of
size 1 and returns the positive root. A trial with the three velocity guesses
negated still converges to that positive root. With the shipped guesses the
solve takes 20 iterations. Without the file, the nominal wet-rating block of
13 stops on a singular Jacobian after 1 iteration: the default humidity ratio
is far from the stored value near 0.025 kg/kg. There is no `abs()` call.
There is no `coolsolve.conf`.

## Results

| Quantity | CoolSolve | EES stored solution |
|---|---:|---:|
| Nominal outlet water `T_w_ex` | 25.555 °C | 25.555 °C |
| Nominal heat rate `Q_dot` | 1.9773 MW | 1.9773 MW |
| Nominal air flow `M_dot_a` | 60 kg/s | 60 kg/s |
| Nominal outlet dry-bulb `T_a_ex` | 28.765 °C | 28.768 °C |
| Half-speed outlet water `T_w_ex_r` | 29.400 °C | 29.401 °C |
| Half-speed heat rate `Q_dot_r` | 1.1723 MW | 1.1722 MW |
| Half-speed air flow `M_dot_a_r` | 30 kg/s | 30 kg/s |
| Half-speed fan power `W_dot_r` | 1875 W | 1875 W |
| Inlet specific volume `v_a` | 0.86328 m³/kg | 0.86357 m³/kg |
| Mix weight `theta` | 0 | ≈ 0 |
| Mean fan power `W_dot_mean` | 1875 W | 1875 W |
| Mixed outlet `T_w_ex_set` | 29.400 °C | 35 °C |

The nominal water outlet lies between the inlet wet-bulb (20.96 °C) and the
inlet water (35 °C). At half speed the air flow is 30 kg/s, the outlet water
is warmer (29.40 °C) and the heat rate falls to 1.172 MW. The fan power falls
from 15000 W to 1875 W, which is \((1/2)^3\) of the nominal power, with the
velocity and the pressure rise in the ratio 1/2 and 1/4.

Inlet humid-air density from `density(AirH2O)` at 25 °C, 101325 Pa and
relative humidity 0.70 is 1.15837 kg/m³. It equals `1/v_a`. The model itself
calls `volume`, and `v_a` is 0.86328 m³/kg.

The shipped closure is the stored fraction `theta` = 0, so the tower runs at
half speed only. The mean fan power is then 1875 W, equal to `W_dot_r`, and
the mix equation gives `T_w_ex_set` = 29.400 °C. The stored 35 °C equals the
water inlet `T_w_su` and does not satisfy the mix at `theta` = 0.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep plot, e.g. outlet water temperature and fan power versus fan speed
     (CoolSolve has no psychrometric chart yet) -->

## Verification

Reference: the solution stored in `MSTH R6 EX 2 2.EES` (EES X7.458, candidate
TM-0090). `compare_solution.py` prints:

> `59 common variables, 1 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The comparison is without `--ees-units`: the extract reports
`SI MASS DEG PA C J`, and no value was converted by hand.

One variable is above rtol = 0.001:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `T_w_ex_set` | 35 | 29.4002 | 1.60e-01 |

The exact maximum over all 59 common variables is 0.159992924904, on
`T_w_ex_set`. The tool prints that relative difference as 1.60e-01.

The equation window leaves `theta` free (the line `T_w_ex_set = 25` is a
comment). The stored solution holds `theta` ≈ 0 and
`W_dot_mean` = `W_dot_r` = 1875 W, which is the half-speed regime. The
shipped model assigns `theta = 0`. The mix equation then returns
`T_w_ex_set` = `T_w_ex_r` = 29.400 °C. The stored 35 °C is the water inlet
temperature and does not satisfy
`T_w_ex_set = theta*T_w_ex + (1-theta)*T_w_ex_r` at that fraction.
`theta` and `W_dot_mean` agree with the stored solution.

Every other common variable is within rtol = 0.001. The next largest relative
difference is 6.515e-04, on `cp_a_f` (the same figure on `omega_f`,
`C_dot_a_f` and `C_dot_max_f`). It comes from the humid-air specific heat,
EES 7.458 against CoolProp `AirH2O`: `cp_a` 6.40e-4, `NTU_f_r` 6.40e-4,
`cp_a_f_r` and the half-speed capacity rates 6.28e-4, `w_a_ex_r` 5.93e-4,
`w_a_ex` 5.23e-4, `w_a_su` 5.16e-4. They stay under the tolerance and pull
the fictitious specific heats with them. `T_w_ex` differs by 8.8e-5 K and
`Q_dot` by 18.5 W. `T_w_ex_r` differs by 3.7e-4 K and `Q_dot_r` by 78 W.
`M_dot_a` is 60 kg/s and `M_dot_a_r` is 30 kg/s on both sides. `W_dot_r` is
1875 W on both sides.

The solver reports success with the shipped guesses (20 iterations): 59
equations, largest block 13. Without the guesses, block 14
(the nominal wet rating, 13 unknowns) stops on a singular Jacobian after 1
iteration. During the successful solve CoolSolve prints a hint that a
`humrat` temperature near 30 °C looks like Fahrenheit. The converged humidity
ratios still agree with the stored solution within 6e-4, so the temperatures
stay in °C.

## Source and attribution

The equation window is headed "MSTh 241005 - R6 - Exercice 2" and names no
person. The `{$ID$}` stamp is the J. Lebrun laboratory EES licence
(Univ. Liège), not the authorship, so `authors` is `TBD (ULiège MSTh)`. The
inventory attributes the course to J. Lebrun, V. Lemort and S. Bertagnolio.

Source (not copied into the library):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 06/MSTH R6 EX 2 2.EES`
(EES X7.458, candidate TM-0090).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): EES X7.458, unit system
  already `SI MASS DEG PA C J`, so no value was rescaled and the
  `$UnitSystem` directive was deleted. No lookup table and no parametric
  table. The file contains the label "Table 1" followed by an empty record;
  the extract report lists no table, and no table was added. Licence tag
  removed. The pasted nominal solution block was a multi-line comment and
  was removed. The commented provisional values `cp_a_f = 4000` and
  `cp_a_f_r = 4000` stay comments. No `$Export`, `concat$`, `EESFILEDIR$` or
  `$TABSTOPS` line. The fluid is `AirH2O` (the file writes `AIRH2O`).
- **Unmodified extract.** With `$UnitSystem` removed and the solution block
  left as a comment: 58 equations, 59 variables, `System square: No`.
- **Stored fraction restored.** The operating-regime block defines
  `T_w_ex_set` and `W_dot_mean` from `theta` and does not assign any of the
  three. The only commented assignment is `T_w_ex_set = 25`. The stored
  solution holds `theta` ≈ 0 and `W_dot_mean` = `W_dot_r`. The added equation
  is `theta = 0`. `T_w_ex_set` stays an unknown: the stored 35 °C equals
  `T_w_su` and does not satisfy the mix. No diagram-state array was added.
  With the assignment the system is square: 59 equations, 59 variables,
  largest block 13.
- **Half-speed outlet enthalpy.** The original calls
  `enthalpy(AirH2O, T=T_a_ex, P=P_atm, w=w_a_ex_r)`, the nominal dry-bulb
  with the half-speed humidity ratio. The call is unchanged.
- **2026-10-15 — curation**: English comments and the standard header. No
  other equation and no other numerical input was changed.
- **Level**: equations 1 (59, in 50–300), largest block 1 (13, in 6–30),
  structure 0 (no procedure, array or `DUPLICATE`), multi-zone 0 (one
  tower), physics 1 (half fan speed is part-load), numerics 1 (the nominal
  block of 13 does not converge without the stored-solution guesses) →
  score 4 → level 3. No pedagogical ±1.

## Limitations and CoolSolve gaps

- The outlet air is taken as saturated, and the water specific heat is the
  constant 4187 J/(kg·K). `AU_dry` is an input. Half speed is imposed by
  halving `AU_dry` and the air flow, with the fan efficiency held at 0.60.
- The stored outlet setpoint 35 °C equals the water inlet and does not
  satisfy the mix at `theta` = 0. The commented trial value 25 °C is not an
  equation. The shipped model uses the stored fraction `theta` = 0.
- The half-speed outlet enthalpy is evaluated at `T_a_ex`, as written in the
  source file.
- Humid-air properties differ slightly between EES 7.458 and CoolProp; see
  *Verification*. `density(AirH2O)` at the inlet state returns 1.15837 kg/m³,
  equal to `1/v_a`. The model does not call `density`.
- No CoolSolve gap blocks the file. `missing_features` is empty.

## Related models

- `CSL-0287` *cooling_tower_chiller_variable_airflow*: continuous air-flow
  variation with the fan laws (instead of two discrete regimes) and the plant
  `COP_global` of a chiller coupled to the tower.
