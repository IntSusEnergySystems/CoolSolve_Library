# Exercise: cooling tower rated on wet-bulb temperatures

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0198`

Teaching exercise from ULiège MSTh, repetition R6, exercise 1. A direct-contact
cooling tower is rated as a fictitious dry counterflow heat exchanger: the
temperatures of that fluid are the wet-bulb temperatures of the moist air, and
the air leaving the tower is saturated. The exercise gives the dry overall
heat-transfer coefficient, the water and air flow rates and the inlet states.

| | |
|---|---|
| **Category** | HVAC and psychrometrics › Cooling towers and evaporative equipment |
| **Fluids** | Moist air (`AirH2O`); water with constant c = 4187 J/(kg·K) |
| **Size** | 28 equations (largest block: 13) |
| **Source** | ULiège MSTh, repetition R6, exercise 1 (header date 2024-10-05) |
| **Authors** | TBD (ULiège MSTh). The file names no person. The course is attributed to J. Lebrun, V. Lemort and S. Bertagnolio. |
| **License** | MIT |
| **CoolSolve** | 0.3.0@f5b79cd — verified against the EES stored solution (see *Verification*) |

## Problem statement

The equation window is headed "MSTh 241005 - R6 - Exercice 1" and gives the data
directly. Translated from the original comment on the fictitious fluid:

> Working with fictitious values amounts to imagining a fictitious dry ideal
> fluid whose temperatures are the wet-bulb temperatures.

Data, as written: dry overall heat-transfer coefficient 90000 W/K; water and
air flow rates 50 and 60 kg/s; inlet water 35 °C; atmosphere 101325 Pa; inlet
air 25 °C and relative humidity 0.70. The outlet air is taken as saturated
(`RH_ex = 1`). The effectiveness equation is the counterflow ε-NTU relation.

## Model

The tower is closed as a dry counterflow exchanger between the water and the
fictitious fluid on the wet-bulb temperatures. The original equations are kept:

- inlet moist air: specific heat `cp_a`, humidity ratio `w_a_su`, enthalpy
  `h_a_su` and wet-bulb temperature `T_wb_su` from `AirH2O` at 25 °C,
  101325 Pa and relative humidity 0.70;
- outlet air saturated, so `T_wb_ex = wetbulb(AirH2O, T=T_a_ex, P=P_atm, R=1)`,
  with `w_a_ex` and `h_a_ex` at that state;
- fictitious specific heat from
  \(h_{a,ex} - h_{a,su} = c_{p,a,f}(T_{wb,ex} - T_{wb,su})\),
  capacity rate \(\dot C_{a,f} = \dot m_a c_{p,a,f}\), and
  \(AU_f = AU_{dry}\, c_{p,a,f}/c_{p,a}\);
- counterflow effectiveness–NTU on \(\dot C_w = \dot m_w c_w\) and
  \(\dot C_{a,f}\);
- the same heat rate from the water, from the effectiveness and from the
  fictitious air side.

The original leaves a commented provisional value `cp_a_f = 4000`. It is not
an equation; the fictitious specific heat is computed.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `AU_dry` dry overall heat-transfer coefficient | 90000 W/K | `T_w_ex` outlet water temperature | 25.555 °C |
| `M_dot_w` water flow | 50 kg/s | `Q_dot` heat rate | 1.977 MW |
| `M_dot_a` air flow | 60 kg/s | `T_a_ex` outlet dry-bulb (saturated) | 28.765 °C |
| `T_w_su` inlet water | 35 °C | `T_wb_su` inlet wet-bulb | 20.963 °C |
| `T_a_su` / `RH_su` / `P_atm` | 25 °C / 0.70 / 101325 Pa | `epsilon_f` effectiveness | 0.673 |

## How to run

Open `cooling_tower_wetbulb_exchanger.eescode` in the CoolSolve GUI and
press *Solve*, or from the model folder:

```bash
coolsolve ./cooling_tower_wetbulb_exchanger.eescode
```

The shipped `cooling_tower_wetbulb_exchanger.initials` holds the EES stored
solution as guesses and selects that physical root. With those guesses the
solve takes 5 iterations. Without the file, the block of 13 (the wet rating
loop) stops on a singular Jacobian after 1 iteration: the default humidity
ratio is far from the stored value near 0.025 kg/kg. There is no `abs()` call.

## Results

| Quantity | CoolSolve | EES stored solution |
|---|---:|---:|
| Outlet water temperature `T_w_ex` | 25.555 °C | 25.555 °C |
| Heat rate `Q_dot` | 1.9773 MW | 1.9773 MW |
| Air flow `M_dot_a` | 60 kg/s | 60 kg/s |
| Outlet dry-bulb `T_a_ex` (saturated, so `T_wb_ex`) | 28.765 °C | 28.768 °C |

The water leaves between the inlet wet-bulb (20.96 °C) and the inlet water
(35 °C). The air flow is an input. The heat rate is about 1.98 MW.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep plot, e.g. outlet water temperature and heat rate versus the inlet
     air temperature (CoolSolve has no psychrometric chart yet) -->

## Verification

Reference: the solution stored in `MSTh R6 Ex 1.EES` (EES X7.458, candidate
TM-0089). `compare_solution.py` prints:

> `28 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The largest relative difference in that table is 6.52e-04, on `cp_a_f`,
`omega_f`, `C_dot_a_f` and `C_dot_max_f` (exact maximum 6.515e-4 on `cp_a_f`).
Nothing exceeds rtol = 0.001. The solver reports success, so the equations are
satisfied.

The humid-air quantities that move, all under the tolerance, are the inlet
specific heat `cp_a` (6.40e-4), the humidity ratios `w_a_ex` (5.23e-4) and
`w_a_su` (5.16e-4), the wet-bulb temperatures `T_wb_su` (1.18e-4) and
`T_wb_ex` (9.31e-5, and the same figure on `T_a_ex`), and the enthalpies
`h_a_su` (3.54e-5) and `h_a_ex` (1.96e-5): EES 7.458 against CoolProp
`AirH2O`. They pull `cp_a_f` with them. `T_w_ex` differs by 8.8e-5 K
(relative 3.46e-6) and `Q_dot` by 19 W (relative 9.36e-6). `M_dot_a` is
60 kg/s on both sides.

## Source and attribution

The equation window is headed "MSTh 241005 - R6 - Exercice 1" and names no
person. The `{$ID$}` stamp is the J. Lebrun laboratory EES licence
(Univ. Liège), not the authorship, so `authors` is `TBD (ULiège MSTh)`. The
inventory attributes the course to J. Lebrun, V. Lemort and S. Bertagnolio.

Source (not copied into the library):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 06/MSTh R6 Ex 1.EES`
(EES X7.458, candidate TM-0089).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): EES X7.458, unit system
  already `SI MASS DEG PA C J`, so no value was rescaled and the
  `$UnitSystem` directive was deleted. No lookup table and no parametric
  table. The equation window already contains the seven inputs; the system
  is square (28 equations, 28 variables), so no Diagram-window value was
  turned into an equation and no diagram state array was added. The pasted
  solution block and the licence tag were removed. The commented provisional
  `cp_a_f = 4000` stays a comment. No `$Export`, `concat$`, `EESFILEDIR$` or
  `$TABSTOPS` line. The fluid is `AirH2O` (the file writes `AIRH2O`).
- **2026-10-15 — curation**: English comments and the standard header. No
  equation and no numerical input was changed. The wet-bulb closure is the
  original one (`wetbulb` of the outlet state at `R = 1`, humidity ratios,
  and \(h_{a,ex}-h_{a,su} = c_{p,a,f}\Delta T_{wb}\)).
- **Level**: equations 0 (28 < 50), largest block 1 (13, in 6–30), structure
  0 (no procedure, array or `DUPLICATE`), multi-zone 0, physics 0 (one
  operating point, `AU_dry` given), numerics 1 (the block of 13 does not
  converge without the stored-solution guesses) → score 2 → level 2.

## Limitations and CoolSolve gaps

- The outlet air is taken as saturated, and the water specific heat is the
  constant 4187 J/(kg·K). `AU_dry` is an input, not computed from the fill.
- Humid-air properties differ slightly between EES 7.458 and CoolProp; see
  *Verification*.
- No CoolSolve gap blocks the file. `missing_features` is empty.

## Related models

- `CSL-0179` *cooling_tower_counterflow_outlet*: the same wet-bulb exchanger
  rating (course session of 2005-10-24, exercise 1), with the same numerical
  data. That file closes the saturated outlet by `temperature(AirH2O, h, P, R=1)`
  and does not compute humidity ratios. This exercise keeps `wetbulb` at the
  outlet dry-bulb and the humidity ratios. `CSL-0179` was not edited.
