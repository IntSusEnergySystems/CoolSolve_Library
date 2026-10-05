# Moist-air cooling coil with contact factor

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0016`

Moist air is cooled and dehumidified by passage over a coil held at a mean
surface (contact) temperature. The coil is characterised by its contact
factor, applied identically to the dry-bulb temperatures and to the humidity
ratios. The model returns the total heat extracted per kilogram of dry air,
its sensible and latent parts, and the mass of condensate.

| | |
|---|---|
| **Category** | HVAC › Psychrometrics |
| **Fluids** | Air (dry-air sensible enthalpy), AirH2O (moist air) |
| **Size** | 25 equations, all explicit (largest block: 1) |
| **Source** | ULiège exercise (VL050429, répétition 10, exercise 1) — CoolSolve example `humidair1` + original EES file |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise, 2005); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — runs; import verified against the solution stored in the original EES file |

## Problem statement

Air at 32 °C and 40 % relative humidity is cooled to 20 °C by passage over a
cooling coil whose mean surface temperature is 5 °C (air pressure 1 bar).
Compute the heat to extract from the air, the sensible and latent parts, and
the mass of water vapour condensed per kilogram of dry air.

## Model

Contact factor (bypass-factor method), written once on the temperatures and
once on the humidity ratios:

- $\varepsilon_c = (T_{su} - T_{ex})/(T_{su} - T_c) = (w_{su} - w_{ex})/(w_{su} - w_c)$,
  with the contact state saturated ($RH_c = 1$) at $T_c$;
- total heat $q = h_{su} - h_{ex}$ from `ENTHALPY(AirH2O, …)`;
- sensible heat $q_s$ from the dry-air enthalpies `ENTHALPY(Air, T=…)` only;
- latent heat $q_l = (w_{su} - w_{ex})\,L_{fg}$ with $L_{fg} = 2.5$ MJ/kg
  (value as in the original);
- condensate $\Delta w = w_{su} - w_{ex}$ per kg of dry air.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_su` / `RH_su` supply air | 32 °C / 0.40 | `epsilon_c` contact factor | 0.4444 |
| `T_ex` outlet air | 20 °C | `q` total heat | 19.82 kJ/kg dry air |
| `T_c` contact temperature | 5 °C | `q_s` / `q_l` | 12.08 / 7.36 kJ/kg dry air |
| `P` air pressure | 1 bar | `DELTAw` condensate | 0.002946 kg/kg dry air |
| | | `w_ex` outlet humidity ratio | 0.009179 kg/kg dry air |

## How to run

Open `moist_air_cooling_coil_contact_factor.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./moist_air_cooling_coil_contact_factor.eescode
```

The system is fully explicit (25 blocks of 1 equation); no guess values are
needed.

## Results

| ε_c [-] | q [kJ/kg] | q_s [kJ/kg] | q_l [kJ/kg] | Δw [g/kg] | w_ex [g/kg] |
|---:|---:|---:|---:|---:|---:|
| 0.4444 | 19.82 | 12.08 | 7.36 | 2.946 | 9.179 |

About 61 % of the extracted heat is sensible, 37 % latent; 2.95 g of water
condense per kilogram of dry air.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep plot, e.g. q, q_s, q_l and DELTAw vs T_ex or T_c (Parametric tab).
     Psychrometric-chart overlays are not available in CoolSolve
     (CS-FEAT-PSYCHRO); the T[i]/w[i] arrays give the supply, outlet and
     contact states. -->

## Verification

Reference: the solution stored in the original EES file `humidair1.EES`
(EES 9.920, `misc/EES_ok.zip` of the CoolSolve repository), compared with
`tools/compare_solution.py` (25/25 variables):

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `epsilon_c` | 0.444444 | 0.444444 | exact |
| `w_su` | 0.0120686 | 0.0121247 | 0.46 % |
| `w_ex` | 0.0091354 | 0.0091790 | 0.48 % |
| `w_c` | 0.0054689 | 0.0054969 | 0.51 % |
| `h_su` / `h_ex` | 63037 / 43266 J/kg | 63229 / 43408 J/kg | 0.30 / 0.33 % |
| `q` | 19770.9 J/kg | 19821.1 J/kg | 0.25 % |
| `q_s` | 12056.0 J/kg | 12076.2 J/kg | 0.17 % |
| `q_l` | 7332.9 J/kg | 7364.2 J/kg | 0.42 % |
| `DELTAw` | 0.00293317 | 0.00294567 | 0.42 % |

All derived energy results agree within 0.43 %. The humidity ratios are
0.46–0.51 % high in CoolSolve: its humid-air formulation (CoolProp, with the
enhancement factor) differs slightly from EES psychrometrics — the
saturation pressure alone was checked to agree within 0.11 %
(`PRESSURE(Water, T, x)` probe), so the remainder is the formulation
difference, well within the different-equation-of-state tolerance of
CoolSolve `docs/ees_import.md` §11. The dry-air absolute enthalpies
`h_su_air`/`h_ex_air` differ by a reference-state offset (EES refers
ideal-gas enthalpy to 0 K); their difference `q_s` agrees within 0.17 %.

## Source and attribution

Original exercise (in French, header `VL050429`) by **Vincent Lemort**
(ULiège Thermodynamics Laboratory) — répétition 10, exercise 1, 2005; the
author was identified from the `VL` initials. The model was rewritten in
English as the CoolSolve example `examples/humidair1.eescode` by S. Quoilin;
this library model supersedes that example, which remains in the CoolSolve
repository as a test case. The example's equations are identical to the EES
original (only the comments were translated), so the library model follows
the EES original.

Sources (not copied into the library):

- CoolSolve example: `~/git/CoolSolve/examples/humidair1.eescode`
  (inventory candidate `CSX-021`);
- original EES file with its stored solution:
  `~/git/CoolSolve/misc/EES_ok.zip` → `EES_ok/humidair1.EES` (EES 9.920).

No candidate of the `thermo_models` inventory is this exercise: the
Répétition-10 psychrometrics session (2005 numbering) has no counterpart in
the collection (its TP 10 holds refrigeration machines); the nearest coils
(MSTh R5 air-water coils `TM-0075`–`TM-0082`, the room-AC coil `TM-0535`,
the RefSim/PARAMID reference coils `TM-0470`–`TM-0472`) are different systems
or levels of detail and stay `todo` for their own cards. The companion
CoolSolve example `humidair2` (`CSX-022`, air handling unit) is a different
model and also stays `todo`.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on the original
  `humidair1.EES`): unit system already SI-°C-Pa-J (no conversion needed);
  EES licence tag (`Jean Lebrun`, the lab licence, not the author) and `{$PX$}`
  display tag removed; no tables, no external functions (only `enthalpy` and
  `humrat`, both CoolSolve built-ins); full stored solution available
  (25/25 variables). Faithful run of the raw extraction: all algebraic
  relations exact, humid-air quantities within 0.51 % (see *Verification*).
- **2026-10-05 — curation**: standard header added, French comments translated
  to English (paraphrasing the original), section titles added, SI units added
  to every comment (`[J/kg dry air]`, `[kg/kg dry air]`, `[-]`); the
  `$UnitSystem` line deleted per the library convention. No change to any
  equation or value (re-verified: results identical to the faithful run).
- **Decision — no diagram state arrays**: the workflow asks for `P[i]`,
  `h[i]`, `T[i]`, `s[i]` arrays on real-fluid models; here the meaningful
  states are moist-air points, and CoolSolve has no psychrometric chart yet
  (`CS-FEAT-PSYCHRO`), so the original `T[i]`/`w[i]` arrays (supply, outlet,
  contact) are kept as-is and the figure will be a parametric sweep (see
  placeholder above, roadmap decision D7).

## Limitations and CoolSolve gaps

- Contact-factor (bypass) model: the whole coil is reduced to one contact
  temperature and one effectiveness, applied identically to temperatures and
  humidity ratios; no air- or water-side heat transfer, no geometry.
- Latent heat $L_{fg}$ kept constant at 2.5 MJ/kg as in the original.
- No CoolSolve gaps encountered during the import. Two benign solver
  warnings: `ENTHALPY(Air, T=…)` intentionally evaluates dry air only (the
  sensible part — its difference `q_s` agrees with EES within 0.17 %), and
  the `t=32 looks like Fahrenheit` hint on `HUMRAT` is a false positive
  (32 °C is the legitimate supply temperature).

## Related models

- `CSL-0017` *chilled_water_cooling_coil*: the NTU-based chilled-water coil
  at the next level of detail; it uses the same contact-factor (bypass)
  outlet method.
- `CSL-0055` *moist_air_room_psychrometrics*: humid-air properties of a room
  (humidity ratio, enthalpy, dew point), the psychrometric basis of this
  cooling-coil model; same EES-vs-CoolProp humid-air offsets.
- CoolSolve example `humidair2` (air handling unit, companion exercise of
  the same group), not yet in the library.
- `CSL-0062` *cooling_coil_condensate_ratio*: 7 kW cooling-and-dehumidifying
  coil solved with two first-law methods (with/without the condensate
  enthalpy term), same humid-air property offsets.
- `CSL-0063` *moist_air_adiabatic_mixing*: adiabatic mixing of room and
  outdoor air (psychrometrics, same course and collection).
- `CSL-0070` *adiabatic_humidifier_simplified*: the same
  effectiveness-type closure (about the wet-bulb state) for the opposite
  air-handling process (humidification).

- `CSL-0064` *psychrometric_mixer_condensation*: adiabatic mixing of room
  and outdoor air with condensation in the mixer (same humid-air property
  offsets).
- `CSL-0073` *cooling_coil_with_control_simplified*: the same
  contact-factor closure in a simplified coil model with a control law on the
  exhaust air temperature (ULiège model bank).
