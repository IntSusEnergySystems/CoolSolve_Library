# Refrigeration evaporator with moist air, wet regime

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0031`

An air-cooled R134a evaporator of a refrigeration circuit, working in the
**wet regime**: moist air is cooled and dehydrated over the coil, water
condenses on it and leaves as condensate. The refrigerant side is described by
imposed evaporating and condensing temperatures, a superheating of 5 K at the
evaporator outlet, a subcooling of 4 K at the condenser outlet and an
isenthalpic expansion between them; the air side by an imposed supply state
(35 °C, 50 % RH) and outlet state (10 °C, 95 % RH) at atmospheric pressure.
The 25 kW evaporator duty then determines the refrigerant and air flow rates,
the fictitious (wet-regime) air-side capacity rate and the coil conductance
`AU_f`. It is the R134a counterpart of `CSL-0017` (same exercise session,
water-cooled coil) and the moist-air counterpart of `CSL-0016`.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | R134a (CoolProp properties), AirH2O (moist air) |
| **Size** | 45 equations (largest block: 2) |
| **Source** | ULiège MSTh exercise (répétition 5, exercise 2, SB solution) — CoolSolve example `evaporator` + original EES file |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory, original exercise, 2017); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — runs (no `.initials` needed); import verified against the solution stored in the original EES file |

## Problem statement

An air-cooling evaporator of a refrigeration circuit has a capacity of 25 kW
with R134a evaporating at 3 °C and condensing at 50 °C, 5 K of superheating
at the evaporator outlet and 4 K of subcooling at the condenser outlet. The
air enters at 35 °C and 50 % relative humidity and leaves at 10 °C and 95 %
relative humidity. Determine the parameters of the evaporator (as in the
original): `AU_f`, `M_dot_a` and `M_dot_r`.

## Model

Refrigerant side (as in the original):

- saturation pressures `P_ev = PRESSURE(R134a,T=T_ev,x=0.5)` and
  `P_cd = PRESSURE(R134a,T=T_cd,x=0.5)`;
- enthalpies `h_1` (superheated vapour at the evaporator outlet),
  `h_3` (subcooled liquid at the condenser outlet) and `h_4 = h_3`
  (isenthalpic expansion);
- evaporator duty `Q_dot_ev = M_dot_r*(h_1 - h_4)`, which gives the refrigerant
  flow rate.

Air side, wet regime (as in the original):

- moist-air states from `ENTHALPY`/`HUMRAT` on `AirH2O`: supply from
  `T_a_su`, `RH_su`; outlet from `T_a_ex` and the imposed `RH_ex`;
- condensate flow rate `M_dot_cd = M_dot_a*(w_su - w_ex)`;
- air-side balance with the condensate enthalpy
  `Q_dot_ev = M_dot_a*(h_a_su - h_a_ex) - M_dot_cd*cp_w*T_cd_w`, with the
  condensate leaving at the outlet air temperature (`T_cd_w = T_a_ex`) and
  `cp_w = 4187 J/(kg·K)`; this equation fixes the air flow rate `M_dot_a`.

Wet-regime performance (as in the original):

- `Q_dot_ev = C_dot_a_f*(T_wb_su - T_wb_ex)` with the wet-bulb temperatures
  from `WETBULB` on `AirH2O` and the capacity rate `C_dot_a_f = M_dot_a*cp_a_f`
  — `cp_a_f` (3179 J/(kg·K)) is the *derived* fictitious air specific heat that
  makes the two duty equations compatible;
- effectiveness definition `Q_dot_ev = epsilon_ev_f*C_dot_min*(T_wb_su - T_ev)`
  with `C_dot_min = C_dot_a_f`, `epsilon_ev_f = 1-exp(-NTU_f)` and
  `NTU_f = AU_f/C_dot_a_f`, which gives the coil conductance `AU_f`.

The 33 equations of the original form a single coupled set (the wet-bulb
temperature of the outlet air depends on the outlet humidity ratio, itself
fixed by the imposed `RH_ex`); CoolSolve splits it into blocks of at most 2
equations and converges in 30 iterations from default guesses.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `Q_dot_ev` duty | 25 kW | `M_dot_a` air flow | 0.4757 kg/s (475.7 g/s) |
| `T_ev` / `T_cd` | 3 / 50 °C | `M_dot_r` refrigerant flow | 0.18152 kg/s |
| `DELTAT_oh` / `DELTAT_sc` | 5 / 4 K | `AU_f` coil conductance | 1900 W/K |
| `T_a_su` / `RH_su` | 35 °C / 50 % | `P_ev` / `P_cd` | 3.260 / 13.179 bar |
| `T_a_ex` / `RH_ex` | 10 °C / 95 % | `C_dot_a_f` / `cp_a_f` | 1512 W/K / 3179 J/(kg·K) |
| `P_atm` | 1 bar | `epsilon_ev_f` / `NTU_f` | 0.7153 / 1.256 |
| | | `M_dot_cd` condensate | 5.10 g/s |
| | | `w_su` / `w_ex` | 0.018095 / 0.007372 kg/kg dry air |
| | | `T_wb_su` / `T_wb_ex` | 26.11 / 9.578 °C |

## How to run

Open `refrigeration_evaporator_wet_coil.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./refrigeration_evaporator_wet_coil.eescode
```

No guess file is needed: the model converges from the default guesses
(30 iterations). CoolSolve prints one harmless warning on the way
(`ENTHALPY(): t=35 looks like Fahrenheit`): the 35 °C of the supply air
trips the unit sanity check of the property call — the known false positive
`CS-BUG-HINT-FAHRENHEIT` of the CoolSolve register (the hint fires for any
temperature within ±3 °C of 32 °C) — but the value is read as °C and matches
the EES reference.

## Results

| `M_dot_a` [g/s] | `M_dot_r` [kg/s] | `AU_f` [W/K] | `epsilon_ev_f` [-] | `NTU_f` [-] | `M_dot_cd` [g/s] |
|---:|---:|---:|---:|---:|---:|
| 475.7 | 0.18152 | 1900 | 0.7153 | 1.256 | 5.10 |

The 25 kW duty is carried by 0.182 kg/s of R134a evaporating at 3 °C and by
476 g/s of moist air whose wet-bulb temperature falls from 26.11 °C to
9.58 °C; 5.1 g/s of water condense on the coil. The determined conductances
reproduce the values quoted by the original's author in the model itself
(`AU_f = 1900 W/K`, `M_dot_a = 0.4761 kg/s`, `M_dot_r = 0.1815 kg/s`) to
0.09 % or better.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram
     of the R134a states 1/3/4 of the evaporator (array overlay of P[i]/h[i]),
     or a parametric sweep plot of M_dot_a and AU_f vs T_a_ex or RH_ex
     (Parametric tab). Psychrometric-chart overlays are not available in
     CoolSolve (CS-FEAT-PSYCHRO). -->

## Verification

Reference: the solution stored in the original EES file
`MSTh-SB-R5-Ex2.EES` (EES 7.458), compared with `tools/compare_solution.py`
(no unit conversion — the original is already SI-°C-Pa-J). The tool prints
`tolerances as printed: rtol=0.001`, 22 common variables, 2 differ:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `h_1` | 255 094.3 J/kg | 403 195.8 J/kg | 36.7 % (see below) |
| `h_3` | 117 342.2 J/kg | 265 466.7 J/kg | 55.8 % (see below) |
| `h_1 - h_3` (duty enthalpy drop) | 137 752.0 J/kg | 137 729.1 J/kg | 0.017 % |
| `w_su` | 0.01807733 | 0.01809522 | 0.099 % |
| `P_cd` | 1 318 607.9 Pa | 1 317 905.5 Pa | 0.053 % |
| `P_ev` | 326 211.7 Pa | 325 984.9 Pa | 0.070 % |
| `h_a_su` | 81 586.98 J/kg | 81 627.34 J/kg | 0.049 % |
| `T_wb_su` | 26.10284 °C | 26.11031 °C | 0.029 % |
| `w_ex` | 0.00737149 | 0.00737225 | 0.010 % |
| `T_wb_ex` | 9.578340 °C | 9.578434 °C | < 0.01 % |
| `Q_dot_ev`, `P_atm`, `P_a_su`, `T_*`, `RH_*`, `T_cd_w`, `cp_w`, `DELTAT_*` | imposed | imposed | exact |

- **The two absolute enthalpies** `h_1` and `h_3` differ by a constant
  reference-state offset of **+148.10 kJ/kg** and **+148.12 kJ/kg** (constant
  to 23 J/kg out of 148 kJ/kg) — the R134a default reference state of EES
  7.458 versus the CoolProp IIR reference used by CoolSolve. As prescribed by
  CoolSolve `docs/ees_import.md` §11 for absolute enthalpies, the *difference*
  is compared instead: the evaporator duty enthalpy drop agrees within
  0.017 %, and every derived result below follows from it.
- **The 11 variables cleared in the EES stored solution** (`M_dot_r`, `h_4`,
  `M_dot_a`, `M_dot_cd`, `h_a_ex`, `C_dot_a_f`, `cp_a_f`, `C_dot_min`,
  `epsilon_ev_f`, `NTU_f`, `AU_f` carry the EES marker −9999, so
  `compare_solution.py` cannot use them). Their EES *guess* values are the
  design values quoted in the original's own comment block
  (`AU_f = 1900 W/K`, `M_dot_a = 0.4761 kg/s`, `M_dot_r = 0.1815 kg/s`) and
  serve as a secondary reference:

  | Variable | design value (original) | CoolSolve | rel. diff |
  |---|---:|---:|---:|
  | `M_dot_r` | 0.1815 kg/s | 0.181516 kg/s | 0.009 % |
  | `M_dot_a` | 0.4761 kg/s | 0.475724 kg/s | 0.079 % |
  | `AU_f` | 1900 W/K | 1900.09 W/K | 0.005 % |
  | `C_dot_a_f` = `C_dot_min` | 1512.788 W/K | 1512.230 W/K | 0.037 % |
  | `cp_a_f` | 3177.46 J/(kg·K) | 3178.79 J/(kg·K) | 0.042 % |
  | `epsilon_ev_f` | 0.71471 | 0.71535 | 0.089 % |
  | `NTU_f` | 1.25425 | 1.25648 | 0.178 % |
  | `M_dot_cd` | 5.0974 g/s | 5.1012 g/s | 0.075 % |
  | `h_a_ex` | 28 628.78 J/kg | 28 626.94 J/kg | 0.006 % |

All 20 comparable variables agree within 9.9e-4 and the nine design
quantities within 0.18 %; the residual deviations are the moist-air
formulation difference (CoolProp psychrometrics with enhancement factor vs
EES 7.458) and the R134a saturation pressures, both within the
different-equation-of-state tolerance of CoolSolve `docs/ees_import.md` §11
(same pattern as `CSL-0016`, `CSL-0017` and `CSL-0008`).

The faithful run of the raw extraction (EES stored values as guesses) and the
curated model give identical results, and so does the run without any guess
file.

## Source and attribution

Original exercise (in French, header `MSTh - SB - R5 - Exercice 2`) solved by
**Stéphane Bertagnolio** (ULiège Thermodynamics Laboratory, `SB` initials —
see `docs/model_workflow.md` §3) — MSTh répétition 5, exercise 2, file dated
2017. The model was rewritten in English as the CoolSolve example
`examples/evaporator.eescode` by S. Quoilin; this library model follows the
EES original (faithful import), which remains the reference; the example
stays in the CoolSolve repository as a test case.

Sources (not copied into the library):

- original EES file with its stored solution:
  `~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 05/MSTh-SB-R5-Ex2.EES`
  (inventory candidate `TM-0078`);
- CoolSolve example: `~/git/CoolSolve/examples/evaporator.eescode`
  (inventory candidate `CSX-015`).

The CoolSolve example is not in `misc/EES_ok.zip`, so the EES original of the
same exercise in the ULiège collection is used as the verification reference.
The exercise has no stored solution in the example's companion files either
(the example ships no `.sol`), so nothing else could serve as a reference.

Related candidates in the `thermo_models` inventory, triaged by this card:

- `TM-0074` (`Copie de MSTh-SB-R5-Ex2.EES`) is **byte-identical** to `TM-0078`
  (same MD5): recorded as a duplicate of this model;
- `TM-0081` (`R5 - Ex 2.EES`) is the *exercise-statement* version of the same
  exercise with a different closure (evaporator at imposed pressures, outlet
  air state from the imposed `RH_ex` directly, semi-isothermal refrigerant
  side, no ε-NTU performance block, renamed variables) — a different model,
  left `todo` for its own card;
- `TM-0083`/`TM-0084` (duplicate group `DG-0018`) are SB *alternative*
  solutions of the same exercise statement with a counterflow ε-NTU law on
  both streams, an isenthalpic expansion used to obtain the evaporator inlet
  temperature and a 12 kW duty — a different level of detail from this
  component model, left `todo` for their own card.

`CSL-0017` (chilled-water cooling coil, same session, exercise 1) already
mentions these five rows and states that they stay `todo` for their own cards;
`TM-0074`/`TM-0078` are now imported here as `CSL-0031`.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on `MSTh-SB-R5-Ex2.EES`):
  unit system already SI-°C-Pa-J (no conversion needed); EES licence tag
  (`Laboratoire de Thermodynamique, U. de Liege`, the lab licence, not the
  author) removed; no table, no external function (`enthalpy`, `exp`,
  `humrat`, `pressure`, `wetbulb` are all CoolSolve built-ins); the report
  lists 35 variables, two of them (`AU`, `T`) carry no equation in the model
  and no stored value — they are ignored by CoolSolve and do not appear in
  the solution. The stored solution is complete except for the 11 variables
  of −9999 listed in *Verification*. Faithful run of the raw extraction with
  the stored values as guesses: success in 15 iterations, 20/22 variables
  within `rtol=0.001`.
- **2026-10-05 — curation**: standard header added; French comments
  translated to English (paraphrasing the original); SI units added to every
  dimensional comment (`[W]`, `[W/K]`, `[J/kg-K]`, `[kg/s]`, `[Pa]`, `[C]`,
  `[K]`, `[kg/kg dry air]`, `[-]`); section titles added in the
  `"!Section"` form; the `$UnitSystem` line deleted per the library
  convention; the commented-out `RELHUM` line and the two section comments
  kept, marked as the alternative closure they document. No change to any
  equation or value — re-solved after curation, results identical to the
  faithful run.
- **2026-10-05 — state points**: the workflow asks real-fluid components to
  be diagram-ready; a post-processing block adds `P[i]`, `h[i]`, `T[i]`,
  `s[i]` for the three evaporator states (1: superheated outlet, 3: subcooled
  liquid at the condenser pressure, 4: after the isenthalpic expansion, in
  the two-phase region). The results of the model are unchanged (12 extra
  single-equation blocks, 45 equations in total).
- **2026-10-05 — differences with the CoolSolve example** (`CSX-015`): the
  example is a faithful translation — after stripping comments and blanks the
  35 equations are *identical*, line for line. The only differences are the
  rewritten English header (which lists the determined design parameters) and
  the missing `$UnitSystem` line (CoolSolve has a single unit system).
  Nothing had to be reconciled; both files give the same solution.
- **2026-10-05 — level**: 45 equations (< 50 → 0), largest algebraic block 2
  (≤ 5 → 0), arrays present for the diagram states (1), no procedures, no
  multi-zone structure, no calibrated or off-design physics, converges from
  default guesses (0 + 0) → score 1 → **level 1**, one below the L2 estimate
  of the card, allowed by `docs/taxonomy.md` §3 (±1): the model is a single
  fully algebraic design point with no implicit loop and no procedures.

## Limitations and CoolSolve gaps

- Both air states are imposed (`T_a_su`/`RH_su` and `T_a_ex`/`RH_ex`): the
  model sizes the coil for a given duty and air state, it does not predict
  the outlet state of a given coil (that would be the off-design problem).
- `cp_w = 4187 J/(kg·K)` is a constant and the condensate leaves at the
  outlet air temperature (`T_cd_w = T_a_ex`), as in the original.
- The wet-regime effectiveness uses the fictitious capacity rate `C_dot_a_f`
  with `C_dot_min = C_dot_a_f` and `epsilon = 1-exp(-NTU_f)`; `cp_a_f` is
  therefore a *result* of the design, not an input (the original does not give
  it either — see *Model*).
- No pressure drops on the air or refrigerant side, no frost model (the coil
  runs at 10 °C, above freezing).
- The original notes a one-directional convergence and a numerical
  instability in the `RH_ex` calculation; the model converges here from
  default guesses and with the EES guesses, but the instability of the
  original is not characterised (it would appear when `RH_ex` is left
  unknown, i.e. the commented-out `RELHUM` closure).
- **No CoolSolve gap blocks the model** (status `verified`, `missing_features`
  empty, no runnable variant needed). The only CoolSolve defect met is the
  cosmetic, already registered false positive `CS-BUG-HINT-FAHRENHEIT`
  (see *How to run*). The psychrometric-chart feature `CS-FEAT-PSYCHRO` and the
  saturated-state temperature call `CS-GAP-PSYCHRO-SAT` are not used by this
  model.

## Related models

- `CSL-0017` *chilled_water_cooling_coil*: same exercise session
  (répétition 5, exercise 1), water-cooled coil with dry and wet regimes.
- `CSL-0016` *moist_air_cooling_coil_contact_factor*: moist-air coil treated
  with the contact (bypass) factor instead of the wet-bulb effectiveness.
- `CSL-0015` *refrigeration_cycle_basic_r134a*: the R134a circuit these
  evaporating/condensing temperatures and this duty belong to.
- `CSL-0008` *condenser_three_zones*: air-cooled R134a condenser, the
  counterpart of this evaporator on the condensing side.
