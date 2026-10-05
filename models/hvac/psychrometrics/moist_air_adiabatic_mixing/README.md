# Adiabatic mixing of room air and outdoor air (moist air)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0063`

Air extracted from a room is mixed adiabatically with a small flow of outdoor
air and supplied back to the room. From the states of the two inlet streams
(room air known by its dry-bulb and wet-bulb temperatures, outdoor air by its
temperature and relative humidity) the model computes the humidity ratio and
the specific enthalpy of the mixed air, and as a bonus its temperature, dew
point and relative humidity, and the recirculated flow fraction.

| | |
|---|---|
| **Category** | HVAC › Psychrometrics |
| **Fluids** | AirH2O (humid air) |
| **Size** | 28 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), session R9, exercise 2, 2022-2023 (EES file `R09_E02_2022.EES`) |
| **Authors** | TBD (see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution and the course's Python/CoolProp solution (see *Verification*) |

## Problem statement

Air extracted from a room is mixed with outdoor air and the mixture is
supplied to the room at a dry-air mass flow of 0.639 kg/s. The room air is
characterised by a dry-bulb temperature of 20 °C and a wet-bulb temperature of
16.2 °C. The outdoor air is characterised by a dry-air mass flow of 50 g/s, a
temperature of 27 °C and a relative humidity of 90 %. Determine the specific
humidity (humidity ratio) and the enthalpy of the mixed air if the ambient
pressure is 101 325 Pa.

(The EES file solves the mixing question only; the exercise statement of the
session also lists conditioning steps — heating, humidification, cooling coil
— which are not part of this file.)

## Model

Mixing of two humid-air streams, assumed adiabatic (as in the original):

- humidity ratios of the inlets from the property functions: `w_1` at
  (`T_1`, wet bulb `T_h_1`), `w_2` at (`T_2`, `phi_2`);
- dry-air balance $\dot m_{a,1} + \dot m_{a,2} = \dot m_{a,3}$ and
  water-vapour balance $\dot m_{v,1} + \dot m_{v,2} = \dot m_{v,3}$ with
  $\dot m_v = w\,\dot m_a$ per stream → $w_3$;
- first law on the (adiabatic) mixing chamber, written per unit of dry air,
  $\dot m_{a,3} h_{a,3} = \dot m_{a,2} h_{a,2} + \dot m_{a,1} h_{a,1}$ →
  $h_{a,3}$;
- bonus: `T_3` (from `h_a_3`, `w_3`), dew point `T_r3`, relative humidity
  `phi_3` of the mixture — `T_3 > T_r3`, so no condensation occurs during the
  mixing (as in the original) — and the recirculated fraction
  `r_q = 100*m_dot_a_1/m_dot_a_3`.

The arrays `T[1..3]`, `w[1..3]` hold the three states for the psychrometric
chart representation of the original.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `p` ambient pressure | 101 325 Pa | `w_3` mixed-air humidity ratio | 0.0108 kg/kg |
| `m_dot_a_3` supply dry-air flow | 0.639 kg/s | `h_a_3` mixed-air specific enthalpy | 48.09 kJ/kg |
| `T_1` / `T_h_1` room air | 20 / 16.2 °C | `T_3` mixed-air temperature | 20.56 °C |
| `T_2` / `phi_2` outdoor air | 27 °C / 0.90 | `T_r3` dew point of the mixture | 15.15 °C |
| `m_dot_a_2` outdoor dry-air flow | 0.05 kg/s | `phi_3` mixed-air relative humidity | 0.711 |
| | | `r_q` recirculated fraction | 92.2 % |

## How to run

Open `moist_air_adiabatic_mixing.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./moist_air_adiabatic_mixing.eescode
```

## Results

| Quantity | EES | CoolSolve | Python/CoolProp |
|---|---:|---:|---:|
| `w_1` room air [kg/kg] | 0.009937 | 0.009982 | 0.009982 |
| `w_2` outdoor air [kg/kg] | 0.020353 | 0.020446 | 0.020446 |
| `w_3` mixture [kg/kg] (asked) | 0.010752 | 0.010801 | 0.010801 |
| `h_a_1` [kJ/kg] | 45.30 | 45.44 | 45.44 |
| `h_a_2` [kJ/kg] | 79.03 | 79.29 | 79.29 |
| `h_a_3` [kJ/kg] (asked) | 47.94 | 48.09 | 48.09 |
| `T_3` [°C] | 20.557 | 20.557 | 20.557 |
| `T_r3` [°C] | 15.149 | 15.152 | – |
| `phi_3` [-] | 0.7113 | 0.7114 | 0.7114 |
| `r_q` [%] | 92.175 | 92.175 | 92.175 |

Only ~8 % outdoor air is needed: the mixture stays close to the room state
(`T_3` between `T_1` and `T_2`, much nearer to `T_1`), and its temperature
remains above its dew point, so the mixing produces no condensation.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep, e.g.
     the mixed-air humidity ratio w_3 and temperature T_3 versus the outdoor-air
     dry-air flow m_dot_a_2 (0 to 0.639 kg/s) — humid-air model, no psychrometric
     chart in CoolSolve (CS-FEAT-PSYCHRO); the arrays T[i]/w[i] hold the three states. -->

## Verification

1. **vs the EES stored solution** (source file, unit-converted with
   `compare_solution.py --ees-units`): 26 common variables, 11 differ, maximum
   relative difference 4.57e-03 (table above). The differences sit on the
   humidity ratios and enthalpies and come from the humid-air property
   formulations of EES vs CoolProp — within the 0.5 % tolerance for different
   equations of state (`docs/ees_import.md` §11); the temperatures agree to
   1.5e-05. The stored solution also contains 23 variables that are not in the
   equations window (`h[1..6]`, `p[1..6]`, `s[1..5]`, `T[4]`, `t[5]`, `a`,
   `AirH2O`, `T`, `h` — leftovers of another exercise solved previously in the
   same file); they are ignored.
2. **vs the course's Python/CoolProp solution of the same exercise**
   (`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R9/Python/ThAp21_R08E02.py`,
   `HAPropsSI`): identical to 1e-05 on every shared quantity (`w_1`, `w_2`,
   `w_3`, `h_a_1`, `h_a_2`, `h_a_3`, `T_3`, `phi_3`, `r_q`) — CoolSolve uses
   the same humid-air backend (CoolProp).

## Source and attribution

Exercise solution of the ULiège course *Thermodynamique appliquée*
(MECA0002), session R9, 2022-2023 edition. The EES file names no author (the
`{$ID$}` tag is the laboratory licence of the *Laboratoire de Thermodynamique*,
University of Liège); the inventory metadata attributes the session to
S. Quoilin with the repetition assistants N. Paulus and B. Dechesne (companion
Python and Word files) — the maintainer will confirm the author attribution
(`TBD`). The Python/CoolProp companion solution of the same exercise is used
as an additional verification reference only; it is not copied into the
library.

Source file (EES 10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R9/R09_E02_2022.EES`
(inventory candidate `TM-0452`; an identical copy inside
`R9.zip`, inventory candidate `TM-0552`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  - **Unit conversion by hand** (original `$UnitSystem SI MASS DEG KPA C KJ`):
    the only unit-bearing input is `p = 101.325 [kPa]` → `p = 101325 [Pa]`
    (original value kept in the comment). The enthalpy balance
    `m_dot_a_3*h_a_3 = …` is homogeneous (mass flow × specific enthalpy), so
    kJ/kg → J/kg needs no equation change; the property calls then simply
    return J/kg. No absolute-temperature relation, no hidden unit constant.
  - `r_q = 100[%]*m_dot_a_1/m_dot_a_3`: the unit annotation on the
    sub-expression `100[%]` does not parse in CoolSolve (registered gap
    `CS-GAP-UNIT-SUBEXPR`, non-blocking: the line is rewritten by the manual
    conversion, see the register); the annotation moved to the comment, the
    value is unchanged (`[%]` is an annotation, not a factor).
  - Comments translated to English; standard header added; stale variables of
    the stored solution (another exercise, see *Verification*) not part of the
    equations. No equation changed otherwise; the model is faithful.
  - **Level justification** (taxonomy.md §3 score): equations 28 (0) +
    largest block 1 (0) + arrays present (1) = 1 → level 1.

## Limitations and CoolSolve gaps

- Wet-bulb-based states (`B=` keyword) and the mixing balance itself are
  supported; no blocking gap. The psychrometric chart of the original
  ("Representation in the psychrometric chart" arrays) has no CoolSolve
  counterpart yet (`CS-FEAT-PSYCHRO`, feature request, not blocking).
- Humid-air property values differ between EES and CoolProp by up to ~0.5 %
  here (see *Verification*).

## Related models

- `CSL-0055` *moist_air_room_psychrometrics*: same course, same session R9
  (exercise 1): moist-air properties of a single room state.
- `CSL-0016` *moist_air_cooling_coil_contact_factor*: psychrometric process on
  humid air (cooling coil with contact factor).
- `CSL-0028` *air_handling_unit_moist_air*: room air handling with mixing-like
  coil and post-heating steps (blocked by a humid-air saturation gap).
- `CSL-0066` *adiabatic_saturation_wet_bulb*: same session, exercise 5:
  moist-air state from the dry-bulb and wet-bulb temperatures.
