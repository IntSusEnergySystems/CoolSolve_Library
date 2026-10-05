# Air handling unit with moist-air conditioning

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0028`

Supply air for a room comes from outdoors (30 °C, 60 % relative humidity).
The supply conditions are achieved with an air handling unit: a cooling coil
characterised by its contact effectiveness (80 %), followed by post-heating.
The model derives the supply air state from the room sensible and moisture
loads, then computes the cooling coil capacity, the post-heating power and
the condensate flow rate at the cooling coil.

| | |
|---|---|
| **Category** | HVAC › Air handling |
| **Fluids** | Air (dry-air sensible enthalpy), AirH2O (moist air) |
| **Size** | 37 equations, largest block: 5 |
| **Source** | ULiège exercise (VL050429, répétition 10, exercise 3) — CoolSolve example `humidair2` + original EES file |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise, 2005); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file blocked (`CS-GAP-PSYCHRO-SAT`); runnable `_coolsolve` variant verified against the solution stored in the original EES file |

## Problem statement

A room at 25 °C and 50 % relative humidity has a sensible load of 130 W and
a moisture gain of 0.08 kg/h (2.22e-5 kg/s). It is ventilated with 40 m³/h of
outdoor air at 30 °C and 60 % relative humidity (air pressure 1 bar). The
supply conditions are achieved with an air handling unit: a cooling coil
with a contact effectiveness of 80 %, then post-heating. Compute the cooling
coil capacity, the post-heating power and the condensate flow rate at the
cooling coil.

## Model

- **Supply state from the room balances**: sensible balance
  $\dot Q_t = \dot M_a\,(h_{in} - h_{su})$ and moisture balance
  $\dot M_a\,w_{su} + \dot M_{w} = \dot M_a\,w_{in}$, with the dry-air flow
  from the imposed volume flow
  $\dot M_a = \dot V_a/v_{a,su}$ — a small implicit loop (largest block: 5);
- **cooling coil** by the contact-factor (bypass) method, applied identically
  to the humidity ratios and to the dry-bulb temperatures:
  $\varepsilon_c = (w_{out} - w_{su})/(w_{out} - w_c)
  = (T_{out} - T_{ex,bat})/(T_{out} - T_c)$, with the contact state saturated
  at $T_c$;
- **post-heating** $\dot Q_{pc} = \dot M_a\,(h_{su} - h_{ex,bat})$, also
  computed from the dry-air enthalpies only ($\dot Q_{pc,bis}$) — the two agree
  since humidity stays at $w_{su}$ after the coil;
- **condensate** $\dot M_{w,cond} = \dot M_a\,(w_{out} - w_{su})$ and **coil
  capacity** $\dot Q_{batt} = \dot M_a\,(h_{out} - h_{ex,bat})$.

| Inputs | Value | Outputs (variant) | Value |
|---|---|---|---|
| `P_in` air pressure | 1 bar | `T_su` / `w_su` supply air | 19.50 °C / 8.357 g/kg dry air |
| `T_in` / `RH_in` room air | 25 °C / 0.50 | `M_dot_a` dry-air flow | 0.01306 kg/s |
| `Q_dot_t` sensible load | 130 W | `T_c` contact temperature | 7.09 °C |
| `M_dot_w` moisture gain | 0.08 kg/h | `T_ex_bat` coil outlet | 11.68 °C |
| `V_dot_a` outdoor-air flow | 40 m³/h | `Q_dot_batt` coil capacity | 510.6 W |
| `T_out` / `RH_out` outdoor air | 30 °C / 0.60 | `Q_dot_pc` post-heating | 104.3 W |
| `epsilon_c` contact effectiveness | 0.80 | `M_dot_w_cond` condensate | 0.375 kg/h |

## How to run

The native file keeps the EES syntax and does not run in CoolSolve (gap
`CS-GAP-PSYCHRO-SAT`). Run the variant instead — open
`air_handling_unit_moist_air_coolsolve.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./air_handling_unit_moist_air_coolsolve.eescode
```

The curated initial guesses
(`air_handling_unit_moist_air_coolsolve.initials`, taken from the stored EES
solution) are required: from default guesses the solver converges to a
non-physical root (`T_su = 10000`).

## Results

| `T_su` [°C] | `T_ex_bat` [°C] | `T_c` [°C] | Q̇_batt [W] | Q̇_pc [W] | ṁ_cond [kg/h] |
|---:|---:|---:|---:|---:|---:|
| 19.50 | 11.68 | 7.09 | 510.6 | 104.3 | 0.375 |

Cooling the 30 °C outdoor air to 11.68 °C at the coil outlet takes 510.6 W
(sensible + latent, 0.375 kg/h of condensate); reheating it to the 19.50 °C
supply state takes 104.3 W. The alternative dry-air computation gives
102.7 W (`Q_dot_pc_bis`), i.e. the same power within 1.5 %.

The arrays `T[i]`/`w[i]` (i = 1 outdoor, 2 coil outlet, 3 supply, 4 room)
give the process on the psychrometric chart.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
      sweep plot, e.g. Q_dot_batt, Q_dot_pc and M_dot_w_cond vs T_out or
      epsilon_c (Parametric tab). Psychrometric-chart overlays are not
      available in CoolSolve (CS-FEAT-PSYCHRO); the T[i]/w[i] arrays give the
      outdoor, coil-outlet, supply and room states. -->

## Verification

Reference: the solution stored in the original EES file `humidair2.EES`
(EES 9.920, `misc/EES_ok.zip` of the CoolSolve repository), compared with
`tools/compare_solution.py` (variant `.sol` vs `reference/ees_variables.csv`):
`37 common variables, 26 differ (rtol=0.001)`; the 11 variables within 0.1 %
are the inputs. The two spurious reference rows `air`/`T` (the extractor
mis-read the arguments of `enthalpy(air, T=…)` as variables) have no
CoolSolve counterpart.

| Variable | EES | CoolSolve (variant) | rel. diff |
|---|---:|---:|---:|
| `T_su` | 19.5427 °C | 19.4972 °C | 0.23 % |
| `T_ex_bat` | 11.6938 °C | 11.6756 °C | 0.16 % |
| `T_c` | 7.11729 °C | 7.09450 °C | 0.32 % |
| `w_su` / `w_out` / `w_c` | 8.329 / 16.260 / 6.346 g/kg | 8.357 / 16.335 / 6.363 g/kg | 0.25–0.46 % |
| `h_su` / `h_in` / `h_out` / `h_ex_bat` | 40753 / 50614 / 71698 / 32750 J/kg | 40810 / 50766 / 71927 / 32818 J/kg | 0.14–0.32 % |
| `RH_su` | 0.581266 | 0.582371 | 0.19 % |
| `v_a_su` | 0.842756 m³/kg | 0.850960 m³/kg | 0.96 % |
| `M_dot_a` | 0.0131843 kg/s | 0.0130572 kg/s | 0.96 % |
| `Q_dot_batt` | 513.510 W | 510.648 W | 0.56 % |
| `Q_dot_pc` | 105.522 W | 104.347 W | 1.11 % |
| `Q_dot_pc_bis` | 103.916 W | 102.743 W | 1.13 % |
| `M_dot_w_cond` | 0.104562 g/s | 0.104168 g/s | 0.38 % |

All per-mass-of-dry-air quantities (humidity ratios, enthalpies,
temperatures, relative humidity) agree within 0.5 %: the same CoolProp-vs-EES
psychrometrics formulation difference as in `CSL-0016` (humidity ratios
0.25–0.46 % high in CoolSolve). The specific volume `v_a_su` is 0.96 % high
in CoolSolve (checked against the ideal-gas value 0.8514 m³/kg at the same
state, which CoolSolve reproduces: the EES psychrometric formulation gives a
lower volume — unexplained: at the C-38 review the EES `volume(AirH2O, …, R=…)`
of `CSL-0030` agrees with CoolProp within 0.04 %, so the difference may come
from the (T, P, w) input pair; to be checked in EES); it propagates directly to the dry-air flow (−0.96 %) and to
the flow-proportional duties (`Q_dot_pc` −1.11 %, `Q_dot_batt` −0.56 %,
`M_dot_w_cond` −0.38 %). The dry-air absolute enthalpies `h_su_air` /
`h_ex_bat_air` differ by a reference-state offset (EES refers ideal-gas
enthalpy to 0 K, as in `CSL-0016`); their difference `Q_dot_pc_bis` agrees
within 1.13 %.

## Source and attribution

Original exercise (in French, header `VL050429`, répétition 10, exercise 3)
by **Vincent Lemort** (ULiège Thermodynamics Laboratory) — the companion
exercise of `humidair1` (same header, exercise 1 of the same session,
imported as `CSL-0016`); the author was identified from the `VL` initials.
The model was rewritten in English as the CoolSolve example
`examples/humidair2.eescode` by S. Quoilin; this library model supersedes
that example, which remains in the CoolSolve repository as a test case. The
example's equations match the EES original except for the contact
temperature (see *Conversion log*), so the library model follows the EES
original.

Sources (not copied into the library):

- CoolSolve example: `~/git/CoolSolve/examples/humidair2.eescode`
  (inventory candidate `CSX-022`);
- original EES file with its stored solution:
  `~/git/CoolSolve/misc/EES_ok.zip` → `EES_ok/humidair2.EES` (EES 9.920).

No candidate of the `thermo_models` inventory is this exercise (searched for
the room-load/ventilation values, the `T_ex_bat`/`Q_dot_batt` variables and
the AHU process: the psychrometrics exercises `TM-0452`/`TM-0453`/`TM-0534`
mix recirculated room air with outdoor air, a different system; the
`TM-0470`–`TM-0476` reference coils model components, not this room-level
unit). All `thermo_models` rows therefore stay `todo` for their own cards.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on the original
  `humidair2.EES`): unit system already SI-°C-Pa-J (no conversion needed);
  EES licence tag (`Jean Lebrun`, the lab licence, not the author) and `{$PX$}`
  display tag removed; no tables, no external functions (only humid-air and
  dry-air property calls, all CoolSolve built-ins); full stored solution
  available (39 variables, of which `air`/`T` are spurious extractor rows from
  the arguments of `enthalpy(air, T=…)` — dropped from the curated
  `.initials`).
- **2026-10-05 — EES original vs CoolSolve example.** The equations are
  identical except for the contact temperature: the EES original evaluates
  the saturated state at given humidity ratio with
  `T_c = temperature(airH2O, P=P_in, w=w_c, R=1)`, the example with
  `T_c = dewpoint(airH2O, P=P_in, w=w_c, T=T_out)` (same dew-point
  temperature). Per the import rule the library model follows the EES
  original; the native file keeps the `R=1` form and is blocked by
  `CS-GAP-PSYCHRO-SAT`, while the runnable `_coolsolve` variant uses the
  example's `dewpoint` form (the only change, logged in the variant header).
- **2026-10-05 — curation**: standard header added, French comments translated
  to English (paraphrasing the original), section titles added, SI units added
  to every comment (`[Pa]`, `[C]`, `[W]`, `[J/kg dry air]`,
  `[kg/kg dry air]`, `[-]`); the `$UnitSystem` line deleted per the library
  convention. No change to any equation or value. The `T[i]`/`w[i]` arrays
  are kept as-is (psychrometric-chart states; no `P[i]`/`h[i]`/`T[i]`/`s[i]`
  diagram block since CoolSolve has no psychrometric chart yet,
  `CS-FEAT-PSYCHRO`).
- **2026-10-05 — level.** Score 2 (arrays +1, curated guesses needed +1;
  37 equations, largest block 5): level 2 by the rubric, kept at level 1
  (−1) since this is an introductory exercise with a small implicit loop,
  as announced on the task card (L1).
- **Decision — curated `.initials` required**: from default guesses the
  variant converges to a non-physical root (`T_su = 10000`, coil duties ≈ 0);
  with the stored-solution guesses it converges in 9 iterations. Both the
  need and the file are documented here and in *How to run*.

## Limitations and CoolSolve gaps

- Contact-factor (bypass) model: the whole coil is reduced to one contact
  temperature and one effectiveness, applied identically to temperatures and
  humidity ratios; no air- or water-side heat transfer, no geometry.
- `CS-GAP-PSYCHRO-SAT` (new, registered 2026-10-05): the native EES call
  `temperature(AirH2O, P=…, w=…, R=1)` fails in CoolSolve (*"CoolProp
  HumidAir cannot accept both R and W as inputs"*); listed in
  `missing_features`. The `_coolsolve` variant uses `dewpoint()` for the
  same saturated state.
- No other CoolSolve gaps encountered. Three benign solver warnings:
  `ENTHALPY(Air, T=…)` intentionally evaluates dry air only (the sensible
  part — its difference `Q_dot_pc_bis` agrees with EES within 1.13 %);
  the `t=30 looks like Fahrenheit` hint on `HUMRAT` is a false positive
  (30 °C is the legitimate outdoor temperature; `CS-BUG-HINT-FAHRENHEIT`);
  the `volume(): w=… is high` hints come from the solver probing
  intermediate iterates, not from the converged solution.

## Related models

- `CSL-0016` *moist_air_cooling_coil_contact_factor*: companion exercise of
  the same session (contact factor on a single coil, per kg of dry air).
- `CSL-0017` *chilled_water_cooling_coil*: the coil at the next level of
  detail (NTU-based, dry and wet regimes).
- `CSL-0055` *moist_air_room_psychrometrics*: humid-air properties of a room
  (humidity ratio, enthalpy, dew point) — the psychrometric relations this
  model starts from.
- See also the CoolSolve example `humidair2.eescode` (same exercise, kept in
  CoolSolve as a test case).
- `CSL-0062` *cooling_coil_condensate_ratio*: cooling coil with condensate
  flow on `AirH2O`, at the level of global first-law balances (two methods).
- `CSL-0063` *moist_air_adiabatic_mixing*: adiabatic mixing of room and
  outdoor air, the first step of an air-handling chain.
- `CSL-0066` *adiabatic_saturation_wet_bulb*: moist-air properties of
  `AirH2O` obtained from dry-bulb and wet-bulb readings (same functions).
- `CSL-0070` *adiabatic_humidifier_simplified*: humidifier component on
  `AirH2O` (effectiveness-NTU), one stage of an air-handling chain.
