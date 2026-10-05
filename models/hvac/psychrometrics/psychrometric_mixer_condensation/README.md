# Psychrometric mixer with condensation: room air mixed with outdoor air

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0064`

Air extracted from a room is mixed with outdoor air and the mixture is injected
back into the room. The data of this exercise are such that the mixture falls
below saturation, so water condenses inside the mixer. The model determines the
condensate flow rate from the conservation of the dry-air and water flows and
from an adiabatic energy balance of the mixer; it also gives the state of the
mixed air (saturated), its dew-point temperature and the share of recirculated
air. It is the companion of the same exercise *without* condensation
(`R09_E02_2022.EES`, inventory row TM-0452): only the inlet data differ.

| | |
|---|---|
| **Category** | HVAC › Psychrometrics |
| **Fluids** | AirH2O (humid air), Air_ha (dry air), Water/Steam |
| **Size** | 34 equations (largest block: 6) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), exercise session R9 (2022-2023), exercise 3 (EES file `R09_E03_2022.EES`) |
| **Authors** | TBD (ULiège course MECA0002 — see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution and an independent recomputation (see *Verification*) |

## Problem statement (paraphrase of the French original)

Same exercise as the previous one, except that the mixed air falls below
saturation, so water condenses in the mixer. The air extracted from a room is
mixed with outdoor air; the mixture is injected into the room at a dry-air flow
rate of 0.639 kg/s. The room air is characterised by a dry-bulb temperature of
20 °C and a wet-bulb temperature of 19.2 °C. The outdoor air is characterised by
a dry-air flow rate of 300 g/s, a temperature of 0 °C and a relative humidity of
90 %. Determine the mass of water that condenses in the mixer, at an ambient
pressure of 101 325 Pa.

## Model

Two inlet streams (1 = room air, 2 = outdoor air) and the mixture (3), all at the
same ambient pressure, with an adiabatic mixer (as assumed in the original):

- humidity ratios `w_1 = humrat(T_1, B=T_h_1)`, `w_2 = humrat(T_2, R=phi_2)`
  and, for information, `phi_1 = relhum(T_1, B=T_h_1)`;
- dry-air conservation: $\dot m_{a,1} + \dot m_{a,2} = \dot m_{a,3}$,
  so $\dot m_{a,1} = 0.639 - 0.300$ kg/s;
- water conservation, **with condensation**: $\dot m_{v,1} + \dot m_{v,2} =
  \dot m_{v,3} + \dot m_{cond}$, with $\dot m_{v,i} = w_i \dot m_{a,i}$;
- because water condenses, the mixed air leaves saturated:
  `w_3 = humrat(T_3, R=1)`, which closes the system with the energy balance
  $\dot m_{a,3} h_{a,3} + \dot m_{cond} h_w = \dot m_{a,2} h_{a,2} +
  \dot m_{a,1} h_{a,1}$ with `h_w = enthalpy(Water, T_3, p)` the enthalpy of the
  condensate and `h_a,i` the moist-air enthalpies per kg of dry air;
- bonus check: the outlet temperature is the dew point
  (`T_r3 = dewpoint(T_3, R=1)`);
- two diagnostic ratios: `r_q` = share of recirculated dry air and `r_cond` =
  share of condensed water per unit dry-air flow, both in %.

The original also writes the moist-air enthalpies a second way, through the dry
air and the vapour (`h_a_1bis`, `h_a_2bis`, `h_a_3bis`): the dry-air enthalpy is
first brought onto the reference scale EES uses for water by subtracting its
value at 0 °C. These three equations are kept as post-processing checks; they
change nothing in the balances.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `p` ambient pressure | 101 325 Pa | `m_dot_cond` condensate flow | 2.25e-4 kg/s (0.225 g/s) |
| `m_dot_a_3` dry-air flow of the mixture | 0.639 kg/s | `T_3` mixture temperature (saturated) | 11.56 °C |
| `T_1` / `T_h_1` room air, dry/wet bulb | 20 / 19.2 °C | `w_3` mixture humidity ratio | 8.51e-3 kg/kg |
| `T_2` / `phi_2` outdoor air | 0 °C / 90 % | `m_dot_a_1` recirculated dry-air flow | 0.339 kg/s |
| `m_dot_a_2` outdoor dry-air flow | 0.300 kg/s | `T_r3` dew point of the mixture | 11.56 °C |
| | | `r_q` recirculated share | 53.05 % |
| | | `r_cond` condensed share | 0.0353 % of the dry-air flow |

## How to run

Open `psychrometric_mixer_condensation.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./psychrometric_mixer_condensation.eescode
```

No `.initials` is needed: the single loop (the saturation balance on `T_3`)
converges in 7–8 iterations from the default guesses over the whole range of
outdoor temperatures checked for the figure below (see *Limitations*). To
reproduce another data set, edit the values of the *Data* section only.

## Results

| Stream | T [°C] | w [kg/kg] | h [J/kg dry air] | dry-air flow [kg/s] |
|---|---:|---:|---:|---:|
| 1 — room air | 20.00 | 1.369e-2 | 54 850 | 0.339 |
| 2 — outdoor air | 0.00 | 3.409e-3 | 8 522 | 0.300 |
| 3 — mixture (saturated) | 11.56 | 8.511e-3 | 33 082 | 0.639 |

- condensate flow: **2.25e-4 kg/s = 0.225 g/s**, i.e. 4.0 % of the water
  brought in by the two streams (5.66 g/s), or 0.035 % of the dry-air flow;
- energy balance closed to 1e-12: 0.639·33 082 + 2.25e-4·48 649 =
  0.300·8 522 + 0.339·54 850 = 21.15 kW;
- the mixture is saturated and its temperature is its dew point
  (`T_r3` = `T_3` = 11.557 °C to 1e-9 K);
- 53 % of the dry air entering the mixer is recirculated room air.

Sweeping the outdoor-air temperature (the model solves for every value tried
from −20 °C to +30 °C) shows the limit of the assumption of the exercise: the
condensate flow falls from 1.14 g/s at −20 °C to 0 at about +6.4 °C and then
becomes *negative* (the mixture stays below saturation, so the correct answer
there is evaporation, which this model — forced to `R = 1`, as in the original —
expresses as a negative `m_dot_cond`):

| `T_2` [°C] | −20 | −10 | 0 | 5 | 10 | 20 | 30 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `m_dot_cond` [g/s] | 1.142 | 0.645 | 0.225 | 0.043 | −0.103 | −0.257 | −0.183 |
| `T_3` [°C] | 5.82 | 8.53 | 11.56 | 13.18 | 14.95 | 19.04 | 24.07 |

The arrays `T[i]`, `w[i]` (i = 1 room air, 2 outdoor air, 3 mixture) carry the
three states for a psychrometric chart; CoolSolve has no such chart yet
(`CS-FEAT-PSYCHRO`), so the figure is a parametric sweep.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep,
     figures/psychrometric_mixer_condensation_sweep.png — m_dot_cond [g/s] vs
     T_2 [-20…30 °C], 1-D Parametric tab of the CoolSolve GUI (humid-air model,
     roadmap decision D7) -->

## Verification

Two references were used.

**1. Solution stored in the EES file.** The extracted file holds the solution of
a *partly solved* state: for the eleven variables of the outlet state
(`T_3`, `T[3]`, `w_3`, `w[3]`, `h_a_3`, `h_a_3bis`, `h_w`, `m_dot_v_3`,
`m_dot_cond`, `r_cond`, `T_r3`) the stored value is identical to the stored
*guess* and does not satisfy the equations of the file — e.g. the stored
`m_dot_v_3` = 0.001 kg/s would give `w_3` = 1.56e-3 kg/kg, a factor 6.8 *below*
the saturation humidity ratio at the stored `T_3` = 15 °C (1.069e-2 kg/kg at
101 325 Pa), and the stored energy balance is 42.8 kW on the left against
21.1 kW on the right. These
eleven values are therefore excluded from the comparison (they are user-typed
guesses, not a solution). `compare_solution.py … --ees-units` on the 21 remaining
common variables:

| Variable | EES | CoolSolve | rel. diff | |
|---|---:|---:|---:|---|
| `w_1` / `w[1]` | 0.0136318 | 0.0136918 | 4.38e-03 | **DIFF** |
| `w_2` / `w[2]` | 0.00339515 | 0.00340895 | 4.05e-03 | **DIFF** |
| `h_a_1` | 54678.5 | 54849.5 | 3.12e-03 | **DIFF** |
| `h_a_2` | 8490.81 | 8522.25 | 3.69e-03 | **DIFF** |
| `h_a_1bis` | 54707.6 | 54859.9 | 2.78e-03 | **DIFF** |
| `h_a_2bis` | 8490.95 | 8525.44 | 4.05e-03 | **DIFF** |
| `m_dot_v_1` | 0.00462118 | 0.00464154 | 4.38e-03 | **DIFF** |
| `m_dot_v_2` | 0.00101855 | 0.00102269 | 4.05e-03 | **DIFF** |

`m_dot_a_1` = 0.339, `m_dot_a_2` = 0.3, `m_dot_a_3` = 0.639, `p`, `T_1`, `T_2`,
`T_h_1`, `phi_2`, `T[1]`, `T[2]`, `r_q` = 53.0516432 agree to 5e-11 or better and
`phi_1` (0.9291472 / 0.9291605) to 1.4e-05. **Maximum relative deviation:
4.38e-03**, on `w_1` and `m_dot_v_1`.

The 4e-3 deviations are the humid-air property difference between EES 10.836 and
CoolProp documented for the same course (`CSL-0055`): the CoolProp humid-air
fluid carries the enhancement factor of the vapour pressure of water, so its
humidity ratios sit ~0.4 % above EES's `HumRat`. The two enthalpies follow the
same humidity ratio. All eight variables are inlet-stream properties; no
EES-stored value of the *result* of the exercise (the condensate flow) exists,
the file having been left unsolved.

**2. Independent recomputation (Python 3.10 / CoolProp 8.0.0 / SciPy 1.7.3,
script not shipped).** The same two balances were solved again with the
psychrometric relations of the course ($w = 0.622\, p_v/(p-p_v)$,
$h = 1.005 T + w(2501 + 1.86 T)$, $h_w = 4.18 T$), taking only the saturation
pressure of water from CoolProp's *water* fluid — the humid-air code is not used
at all:

| Inlet properties used | `T_3` [°C] | `m_dot_cond` [g/s] | rel. diff. vs CoolSolve (`T_3` / `m_dot_cond`) |
|---|---:|---:|---|
| course relations (CoolProp `p_ws` only) | 11.5468 | 0.2226 | 9.0e-04 / 1.3e-02 |
| course relations, CoolProp liquid-water `h` | 11.5467 | 0.2226 | 9.0e-04 / 1.3e-02 |
| the EES stored `w_1`, `w_2`, `h_a_1`, `h_a_2` | 11.5483 | 0.2260 | 7.7e-04 / 2.3e-03 |
| CoolProp `AirH2O` (the code path CoolSolve uses) | 11.5571 | 0.2254 | 0 / 0 |

The last row reproduces the CoolSolve solution to all printed digits, which
confirms the transcription of the equations. With the inlet properties EES had
stored, the answer is 0.2260 g/s of condensate against 0.2254 g/s here
(2.3e-03), i.e. within the humid-air property tolerance of CoolSolve
`docs/ees_import.md` §11 (≤ 0.5 % for properties of a different formulation);
the outlet temperature agrees to 8e-4.
The larger 1.3e-03 deviation of the condensate flow against the *course*
relations comes from the 0.5 % difference between the psychrometric formula used
there and the humid-air property functions.

**Sanity checks.** Energy balance closed to 1e-12; `T_r3` = `T_3` = 11.557 °C
(saturated outlet, as the original assumes); the condensate is 4 % of the
incoming water vapour; `m_dot_cond > 0`, as the statement requires. The
22 variables that exist only in the EES record (`p[1..6]`, `v[1..6]`,
`s[1..5]`, `T[4]`, `t[5]`, `T`, `a`, `r`, `v`, `AirH2O`) are leftovers of an
earlier exercise of the same file and are in no equation.

## Source and attribution

Exercise solution of the course *Thermodynamique appliquée* (MECA0002),
exercise session R9 of 2022-2023, exercise 3, distributed by the ULiège
Thermodynamics Laboratory. The file names no author and the folder gives no
initial: `TBD`. The `{$ID$…}` tag of the file identifies the EES licence
("For use only by students and staff at the Laboratoire de Thermodynamique,
University of Liege PoloUHB"), not an author. The companion exercise 1 of the
same session (`TM-0451`, model `CSL-0055`) is attributed the same way.

Source file (EES 10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R9/R09_E03_2022.EES`
(inventory candidate `TM-0453`, duplicate group empty: the inventory lists it as
"similar but not grouped" to `TM-0452` and `TM-0552`, the exercise *without*
condensation). No table, no lookup file, no function library, no module.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES 10.836, 56 variable records, no lookup or parametric table; the licence
  tag `{$ID$…}` and the display tags `{$NC$…}`, `{$PX$96}`, `{$ST$ON}` were
  removed by the tool; the decimal comma of the European format was converted
  (`volume(Air_ha;T=T_1;P=p)` → `,`), which changes no number. The stored
  solution of the file is a partly solved state (see *Verification*), so no
  `.initials` is shipped: the model converges from the default guesses.
- **2026-10-05 — hand unit conversion** (kPa/kJ → Pa/J, CoolSolve
  `docs/ees_import.md` §6): the only input whose unit changes is
  `p = 101.325 [kPa]` → `p = 101325 [Pa]`. The property calls need no factor
  (they return J/kg in the SI-°C-Pa-J system); the equations mix only flows in
  kg/s and enthalpies in J/kg, so the balances are unchanged. Temperatures were
  already in °C in the original (`$UnitSystem … KPA C KJ`), and no relation uses
  an absolute temperature. `T=0[C]` in the three `enthalpy(Air_ha,…)` calls
  becomes `T=0`: the unit annotation on a named argument is what CoolSolve
  rejects (`CS-GAP-UNIT-NAMEDARG`), and 0 °C is the value the annotation
  carried. `.initials` was therefore not converted (none is shipped).
- **2026-10-05 — `100[%]` → `100` with the unit in the comment.** The original
  writes `r_q = 100[%]*m_dot_a_1/m_dot_a_3` and `r_cond = 100[%]*…`. A unit
  annotation in the middle of a right-hand side is a parse error in CoolSolve
  (`CS-GAP-UNIT-SUBEXPR`); the numerical result of the original is
  100·m_dot_a_1/m_dot_a_3 (`r_q` = 53.05164319 stored by EES), so the factor
  100 is kept and `[%]` moved to the comment. Nothing else changed.
- **2026-10-05 — comments** translated to English (paraphrase of the French
  comments; the two long pedagogical notes of the original — the heat-exchanger
  alternative and the common enthalpy reference of EES for moist air and water —
  are kept, as in the original); standard header added; dimensional comments
  given their SI unit. **No equation of the original was changed** (the unit
  conversion excepted) and no equation was added or removed.
- **Level**: score 2 per `docs/taxonomy.md` §3 (34 equations → 0; largest
  block 6 → 1; arrays `T[i]`, `w[i]` present → 1; no procedure, no multi-zone, no
  empirical calibration, no curated guesses → 0) → level 2, moved −1 to
  **level 1** per the card: a 34-equation teaching exercise whose only loop is the
  single saturation balance of the mixer, the arrays being only the three
  psychrometric-diagram points.

## Limitations and CoolSolve gaps

- The mixer is assumed adiabatic and at the ambient pressure, as in the original:
  no heat loss to the surroundings, no pressure drop.
- The outlet is *forced* saturated (`R = 1`), as in the original: for outdoor-air
  temperatures above about +6.4 °C the mixture is not saturated and
  `m_dot_cond` turns negative (see *Results*).
- The condensate leaves the mixer at the mixture temperature (no subcooling).
- No CoolSolve gap blocks the native file. Two registered gaps were met and are
  removed by the unit conversion of the equations themselves
  (`CS-GAP-UNIT-NAMEDARG` for `T=0[C]`, `CS-GAP-UNIT-SUBEXPR` for `100[%]`), so
  no runnable variant is needed. `CS-FEAT-PSYCHRO` (no psychrometric chart) is
  the reason for the parametric-sweep figure.

## Related models

- `CSL-0055` *moist_air_room_psychrometrics*: same course and same session,
  exercise 1 (room air, humidity ratio, enthalpy, dew point); the humid-air
  property functions and the reference-state remarks are the same.
- `CSL-0062` *cooling_coil_condensate_ratio*: condensation of the water of a
  moist-air stream in a cooling coil, written with separate dry-air, vapour and
  condensate enthalpy terms.
- `CSL-0016` *moist_air_cooling_coil_contact_factor*: moist-air states on a
  psychrometric chart given by a contact factor.
- `CSL-0030` *two_speed_cooling_tower*: evaporative cooling of water by
  unsaturated air (mass and energy balances of the same kind).
- Inventory row `TM-0452` (`~/Nextcloud/thermo_models/thermodynamique
  appliquee/2022-2023/R9/R09_E02_2022.EES`): the same exercise *without*
  condensation (same equations, other inlet data), the solution shipped with the
  course in Python/CoolProp (`…/R9/Python/ThAp21_R08E02.py`, 2021 edition).
- `CSL-0066` *adiabatic_saturation_wet_bulb*: same session, exercise 5:
  moist-air state from the dry-bulb and wet-bulb temperatures.
