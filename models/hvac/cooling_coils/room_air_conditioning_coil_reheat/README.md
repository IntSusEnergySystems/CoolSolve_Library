# Air conditioning of a room: cooling-dehumidifying coil and reheat

🟢 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0292`

An air handling unit conditions 40 m³/h of outdoor air (30 °C, 60 % relative
humidity) for a room held at 25 °C and 50 % saturation (1 bar), in which one
occupant releases 130 W and 80 g/h of water. The room energy and moisture
balances give the required supply state; the cooling coil dehumidifies the
outdoor air down to a saturated state at the supply humidity ratio and the
reheat coil brings the air back to the supply temperature. The model computes
the supply state, the coil duty (with the condensate enthalpy in the first
law), the reheat power, the condensate flow and the inter-coil temperature.

| | |
|---|---|
| **Category** | HVAC › Air handling |
| **Fluids** | AirH2O (moist air), Water (condensate) |
| **Size** | 37 equations, largest block: 5 |
| **Source** | ULiège, course *Thermodynamique appliquée* (MECA0002), repetition 10 (29 Apr 2010), exercise 3 — EES file `THD10_R10_E3.EES` |
| **Authors** | Sébastien Borguet, Samuel Gendebien (ULiège Thermodynamics Laboratory, session répétiteurs) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — native file blocked (`CS-GAP-PSYCHRO-SAT`); runnable `_coolsolve` variant verified against the solution stored in the original EES file |

## Problem statement (paraphrased from the original, in French)

Air-condition a room so that the room air stays at 25 °C with a degree of
saturation of 50 %. The room contains one person who releases 80 g of water
per hour and 130 W of total heat. The ventilation requires 40 m³/h of fresh
air, taken from outdoors (30 °C, 60 % relative humidity). The room pressure is
1 bar. The supply conditions are produced by an air handling unit. Compute
these supply conditions, the heat exchanged at the cooling coil, the power
needed for the post-heating, the flow of water condensed on the cooling coil
and the temperature between the two coils.

## Model

- **Supply state from the room balances** (states: EXT outdoor, INT inter-coil,
  SU supply, IN room): sensible balance
  $\dot Q = \dot m_a\,(h_{in} - h_{su})$ and moisture balance
  $\dot m_a\,w_{su} + \dot m_w = \dot m_a\,w_{in}$, with the air flow from the
  imposed volume flow $\dot m_a = \dot V_a/v_{a,su}$ — a small implicit loop
  (largest block: 5), which the original already helps with initial guesses
  ($T_{su} \approx T_{in}$, $w_{su} \approx w_{in}$);
- **cooling coil**: the air leaves the coil *saturated* at the supply humidity
  ratio ($r = 1$ at $w_{int} = w_{su}$), so
  $\dot Q_{bf} = \dot m_a\,(h_{int} - h_{ext}) + \dot m_{cond}\,h_{cond}$
  includes the (small, < 1 % of the air flow) condensate enthalpy, with the
  condensate a saturated liquid at $T_{int}$;
- **condensate flow** from the water balance
  $\dot m_a\,w_{ext} = \dot m_a\,w_{int} + \dot m_{cond}$, reported in L/h;
- **reheat coil**: isobaric heating at constant humidity ratio,
  $\dot Q_{pc} = \dot m_a\,(h_{su} - h_{int})$;
- the outdoor-air dew point $T_{r,ext}$ is computed to show
  $T_{int} < T_{r,ext}$, i.e. condensation does occur (as in the original);
- the states EXT → INT → SU → IN are stored in the arrays `T[i]`, `w[i]` for
  the psychrometric chart, as in the original.

| Inputs | Value | Outputs (CoolSolve variant) | Value |
|---|---|---|---|
| `p` air pressure | 1 bar | `q_m_a` air mass flow | 0.01305 kg/s |
| `q_v_a` fresh-air volume flow | 40 m³/h | `T_su` / `w_su` supply state | 19.50 °C / 8.357 g/kg |
| `T_in` / `phi_in` room air | 25 °C / 0.50 | `phi_su` supply relative humidity | 0.582 |
| `q_m_w` moisture release | 80 g/h | `T_int` inter-coil temperature | 11.09 °C |
| `Q_dot` heat release | 130 W | `Q_dot_bf` cooling-coil duty | −513.6 W |
| `T_ext` / `phi_ext` outdoor air | 30 °C / 0.60 | `Q_dot_pc` reheat power | 112.2 W |
| | | `q_v_cond` condensate flow | 0.375 L/h |
| | | `T_r_ext` outdoor dew point | 21.39 °C |

## How to run

The native file keeps the EES syntax and does not run in CoolSolve: the
saturated coil-outlet state `h_int = enthalpy(AirH2O, p=…, r=1, w=…)`
evaluated with the gap `CS-GAP-PSYCHRO-SAT`. Run the variant instead — open
`room_air_conditioning_coil_reheat_coolsolve.eescode` in the CoolSolve GUI
and press *Solve*, or from a terminal:

```bash
coolsolve ./room_air_conditioning_coil_reheat_coolsolve.eescode
```

The curated initial guesses
(`room_air_conditioning_coil_reheat_coolsolve.initials`, taken from the
stored EES solution) are required: from default guesses the solver converges
to a non-physical root (`T_su = 10000`, as in `CSL-0028`).

## Niche

Nearest library models, compared by equations:

- `CSL-0028` *air_handling_unit_moist_air* is **the same exercise** (R10 E3,
  2005 version, `VL050429`; this file is the 2010 version) with the same room
  data, but it closes the cooling coil with a **contact-factor (bypass)
  method** (contact effectiveness 80 %, contact state at $T_c$, coil outlet
  $T_{ex,bat} = 11.68$ °C superheated), while this 2010 version closes the
  coil with a **saturated outlet state** ($r = 1$ at $w_{su}$,
  $T_{int} = 11.09$ °C) and an energy balance that **includes the condensate
  enthalpy**. The two coil closures are the two classic textbook
  descriptions; the equation overlap measured by `audit.py --cand` is 11 %.
- `CSL-0016` *moist_air_cooling_coil_contact_factor*: the contact-factor coil
  alone, per kg of dry air, without room balances, reheat or condensate flow.
- `CSL-0062` *cooling_coil_condensate_ratio*: a cooling coil with condensate
  flow by global first-law balances, but no room or supply state.

This model adds the saturated-off-coil closure with the condensate term in
the coil first law, the condensate volumetric flow and the dew-point
plausibility check, on the full outdoor-air → room chain, with its own EES
stored solution as verification reference.

## Results

| `T_su` [°C] | `w_su` [g/kg] | `T_int` [°C] | Q̇_bf [W] | Q̇_pc [W] | `q_v_cond` [L/h] |
|---:|---:|---:|---:|---:|---:|
| 19.50 | 8.357 | 11.09 | −513.6 | 112.2 | 0.375 |

Cooling the outdoor air down to the saturated state at 11.09 °C (below the
outdoor dew point of 21.39 °C, hence the condensate) takes 513.6 W; the
condensate term `q_m_cond*h_cond` contributes +4.9 W inside the first law
(i.e. < 1 % of the duty, as the original notes); reheating to the 19.50 °C
supply state takes 112.2 W.

The arrays `T[i]`/`w[i]` (i = 1 outdoor, 2 coil outlet, 3 supply, 4 room)
give the process on the psychrometric chart.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
      sweep plot, e.g. Q_dot_bf, Q_dot_pc and q_v_cond vs T_ext or phi_ext
      (Parametric tab). Psychrometric-chart overlays are not available in
      CoolSolve (CS-FEAT-PSYCHRO); the T[i]/w[i] arrays give the outdoor,
      coil-outlet, supply and room states. -->

## Verification

Reference: the solution stored in the original EES file `THD10_R10_E3.EES`
(EES 8.423, 35 variables — full stored solution), compared with
`tools/compare_solution.py … --ees-units` (variant `.sol` vs
`reference/ees_variables.csv`):

`35 common variables, 19 differ (rtol=0.001)` — maximum relative deviation
**5.37e-03**, on the humidity ratios (`w_su`, `w_int`, `w[2]`, `w[3]`: 8.3122
g/kg in EES against 8.3571 g/kg in CoolSolve). The 16 variables within 0.1 %
are the inputs, `T_su`, `T[1]`, `T[3]`, `T[4]`, `v_a_su` and `q_m_a`. The
differences are the known EES-vs-CoolProp humid-air formulation difference
already documented on `CSL-0028` and `CSL-0016` (humidity ratios ≈ 0.5 % high
in CoolProp); they propagate to the derived enthalpies (up to 3.66e-03), the
duties (`Q_dot_pc` 2.41e-03, `Q_dot_bf` 1.26e-03) and the condensate flow
(`q_v_cond` 4.13e-03). The condensate mass flow `q_m_cond` itself is not
stored in the EES reference; it is verified through `q_v_cond`.

The same comparison for `CSL-0028` (contact-factor closure) gave 0.23–1.13 %
on the same quantities: the two closures agree to within the property
difference on the shared outputs (`T_su`, `q_m_a` identical).

## Source and attribution

Exercise of the ULiège course *Thermodynamique appliquée* (MECA0002),
repetition 10 of 2009–2010 (29 April 2010), exercise 3. The EES file names no
author; the session sheet `THD10_R10.pdf` in the same archive names the
session répétiteurs **Sébastien Borguet** and **Samuel Gendebien**
(Laboratoire de Thermodynamique), who are credited here. The archive also
contains the exercise statements of the four exercises of the session; the
companion files are inventoried as `TM-0533` (E1, merged into `CSL-0055`),
`TM-0534` (E2, merged into `CSL-0063`) and `TM-0536` (E4, merged into
`CSL-0065`).

Source file (EES 8.423, comments in French, decimal comma), collection of
S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R10.zip!`
→ `THD10_R10_E3.EES` (inventory candidate `TM-0535`).

## Conversion log

- **2026-10-24 — import** (`tools/ees_extract.py`): unit system
  `SI MASS DEG KPA C KJ` + decimal comma; both converted by hand
  (CoolSolve `docs/ees_import.md` §6): `p = 100E3 [Pa]` (100 kPa),
  `Q_dot = 130 [W]` (0.130 kW); the enthalpy and power results of the
  property calls and balances follow the J/Pa system (the equation
  `q_v_cond = q_m_cond*3600*v_cond*1000` keeps its factors, they are the
  s/h and L/m³ conversions of the output unit). No absolute-temperature
  relation, no other hidden constant. Decimal comma → dot (tool). EES licence
  tag removed. Comments translated to English (paraphrasing the original).
  `.initials` from the stored solution (pressures ×1000, enthalpies and
  powers ×1000).
- **2026-10-24 — native file blocked by `CS-GAP-PSYCHRO-SAT`** (registered;
  same gap as `CSL-0028`): `h_int = enthalpy(AirH2O, p=p, r=1, w=w_int)`
  fails (*"CoolProp HumidAir cannot accept both R and W as inputs"*). The
  native file keeps the valid-EES call; the runnable variant
  `room_air_conditioning_coil_reheat_coolsolve.eescode` evaluates the same
  saturated state through its dew-point temperature
  (`T_int = dewpoint(fluid$, P=p, W=w_int, T=T_ext)`, then
  `h_int = enthalpy(fluid$, p=p, T=T_int, w=w_int)`) and deletes the later
  `T_int = temperature(…h=h_int…)` line, now superseded — these are the only
  changes, everything else is the native file.
- **2026-10-24 — curated `.initials` required** (variant): from default
  guesses the solver converges to a non-physical root (`T_su = 10000`), as on
  `CSL-0028`; with the stored-solution guesses it converges in 5 iterations.
  The original itself recommends initial guesses (`T_su = T_in`,
  `w_su = w_in`).
- **2026-10-24 — level.** Score 3 (arrays +1, three coupled components
  room/coil/reheat +1, curated guesses +1; 37 equations, largest block 5):
  level 2, in line with the inventory guess.
- Solver noise: probing iterates of `volume(AirH2O, …)` trigger CoolProp
  range warnings during the solve; the converged solution is physical
  (see *Results*). No other gaps encountered.

## Limitations and CoolSolve gaps

- `CS-GAP-PSYCHRO-SAT` (registered 2026-10-05 on `CSL-0028`): the native EES
  saturated-state call at given humidity ratio fails in CoolSolve; listed in
  `missing_features`. The `_coolsolve` variant uses `dewpoint()` for the same
  state.
- Design-point model: the coil is closed by its outlet state (saturated at
  the supply humidity ratio), not by a heat-transfer model; no part load, no
  bypass factor.

## Related models

- `CSL-0028` *air_handling_unit_moist_air*: the same exercise (2005 version)
  with the other classic coil closure (contact factor / bypass method) —
  compare the two coil models on the same room.
- `CSL-0016` *moist_air_cooling_coil_contact_factor*: the contact-factor coil
  alone, per kg of dry air.
- `CSL-0062` *cooling_coil_condensate_ratio*: cooling coil with condensate
  flow by global first-law balances.
- `CSL-0055` / `CSL-0063` / `CSL-0065`: the other three exercises of the same
  session (room psychrometrics, air mixing, cooling tower), imported from the
  same archive `THD10_R10.zip`.
