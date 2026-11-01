# Zeotropic propane/isobutane heat pump with glide-matching sectioned exchangers (TESPy)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0324`

Single-stage water-to-water heat pump whose working fluid is a **zeotropic
mixture** (propane/isobutane, CoolProp mixture backend). The condenser and the
evaporator are *sectioned* exchangers: each is cut into 50 sections of equal
heat and the minimum temperature difference over the section boundaries (an
internal pinch, not only the end differences) is imposed. The temperature
glide of the mixture therefore decides the two pressures, and the model
returns the COP, the volumetric heating capacity and the condenser glide as
functions of the composition. It is a translation of the TESPy how-to
*Zeotropic mixtures in a heat pump* (class `ZeotropicHeatPumpModel`).

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration cycles and heat pumps |
| **Fluids** | propane/isobutane mixture `Propane[0.5]&IsoButane[0.5]` (mole fractions; the sweep also uses the pure fluids), Water |
| **Size** | 567 equations (largest block: 335) |
| **Source** | [TESPy](https://github.com/oemof/tespy), `docs/how_to_guides/zeotropic_heat_pump.ipynb`, commit `19425523ff7ecd67b36e7b90efe04a9480a9ebe3` ([notebook](https://github.com/oemof/tespy/blob/19425523ff7ecd67b36e7b90efe04a9480a9ebe3/docs/how_to_guides/zeotropic_heat_pump.ipynb)) |
| **Authors** | Francesco Witte (TESPy lead developer; author of the notebook per the git history) and the TESPy contributors |
| **License** | MIT (TESPy: "Copyright (c) Francesco Witte") |
| **CoolSolve** | 0.4.0 (`0.4.0@9768373`) — verified against a re-run of the TESPy model (see Verification); needs its `.initials` and `coolsolve.conf` |

## Problem statement

As in the notebook: a heat pump delivers `Q_dot_cd` = 100 kW to water heated
from 30 °C to 50 °C and takes heat from water cooled from 15 °C to 10 °C (both
at 3 bar, no pressure drop). The compressor has an isentropic efficiency of
0.8, the working fluid leaves the evaporator 5 K above its dew point
(`td_dew`) and leaves the condenser 2 K below its bubble point (`td_bubble`),
and the minimum temperature difference over the sections of each exchanger is
3 K. Compute both pressures, the mass flow rates, the COP, the heating
capacity per unit of compressor-inlet volume flow (VHC) and the condenser
glide, for a propane mole fraction of 0.5; then repeat for 0 % to 100 %
propane (the composition sweep).

## Model

State names follow the TESPy connections: `01` = compressor inlet = `05`
evaporator outlet (the cycle closer), `02` compressor outlet, `03` condenser
outlet, `04` evaporator inlet (after the valve); `11`/`12` heating water
in/out, `21`/`22` source water in/out. States are suffixed `_1` … `_5`,
`_11`, `_12`, `_21`, `_22`.

- **Compressor**: `h_2 = h_1 + (h_2s - h_1)/eta_s`, `h_2s` at `(P_cd, s_1)`.
- **Superheat / subcooling**: `T_1 = T_dew(P_ev) + DELTAT_dew`,
  `T_3 = T_bub(P_cd) - DELTAT_bub` (bubble and dew points of the mixture from
  `TEMPERATURE(fluid$, P=…, x=0/1)`).
- **Valve**: `h_4 = h_3`. **Evaporator outlet**: `h_5 = h_1`.
- **Energy balances**: `Q_dot_cd = M_dot*(h_2 - h_3) = M_dot_11*(h_12 - h_11)`,
  `Q_dot_ev = M_dot*(h_5 - h_4) = M_dot_21*(h_21 - h_22)`; the heat is
  distributed over the sections by enthalpy, equal steps in `Q`.
- **Sections** (`SectionedHeatExchanger`, `num_sections = 50`): at the 51
  boundaries `i = 1…51` both streams are at `h = h_in + (i-1)/50*(h_out - h_in)`
  and `dT[i]` is the temperature difference (counterflow: the cold-side
  coordinate runs from the working-fluid outlet of the condenser, from the
  working-fluid inlet of the evaporator). The pinch conditions
  `td_pinch = MIN(dT_cd[…])` and `td_pinch = MIN(dT_ev[…])` close `P_cd` and
  `P_ev`.
- **Bubble and dew points as extra boundaries**: TESPy adds the phase
  boundaries to the section grid (`_get_moving_steps`: the mixture string is
  one fluid name, so TESPy treats it like a pure fluid). They enter the `MIN`
  through two candidates per exchanger (arrays `dT_cd_sat[j]`, `dT_ev_sat[j]`,
  `j = 1` saturated liquid, `j = 2` saturated vapour), used only when the
  boundary lies inside the exchanger (function `Cand`).
- **Indicators**: `COP = Q_dot_cd/W_dot`; `VHC = Q_dot_cd/(M_dot*v_1)/1000`
  [kJ/m³]; `Glide_cd = T_dew - T_bub` at `P_cd`.
- **Function `Tmix_ph(fluid$, P, h)`**: temperature of the mixture at `(P, h)`
  (see conversion log, performance).

## How to run

```bash
coolsolve ./zeotropic_hp_propane_isobutane.eescode   # about 7 s, uses the .initials and coolsolve.conf
```

Another composition: change the mole fractions in `fluid$` (numbers, summing
to 1: `'Propane[0.3]&IsoButane[0.7]'`; the pure ends are `'Propane'` and
`'IsoButane'`) and start from the `.initials` of a neighbouring composition
(run with `-g`; remove the `fluid$ = …` lines it writes into the `.initials`:
a string initial overrides the model's `fluid$`). **Without `.initials` the
file fails** (SingularJacobian): the large block of 335 unknowns needs guesses.
`coolsolve.conf` sets `tolerance = 1e-6` (see conversion log).

## Results

Design point of the notebook (50 % propane, mole fraction), CoolSolve:

| Quantity | Value |
|---|---|
| `P_ev` / `P_cd` | 3.0019 bar / 10.3343 bar |
| `T_dew_ev`, `T_1` | 7.00 °C, 12.00 °C |
| `T_2` (compressor outlet) | 62.10 °C |
| `T_bub_cd`, `T_dew_cd`, `T_3` | 45.11 °C, 51.72 °C, 43.11 °C |
| `M_dot` (working fluid) | 0.29254 kg/s |
| `M_dot_11` / `M_dot_21` (water) | 1.1964 kg/s / 3.8275 kg/s |
| `W_dot` / `Q_dot_ev` | 19.798 kW / 80.202 kW |
| `COP` | 5.0511 |
| `VHC` | 2391.6 kJ/m³ |
| `Glide_cd` | 6.60 K |

The condenser pinch (3.000 K) sits at the **dew point** (a section boundary
added at 93.6 % of the heat from the cold end; the nearest grid point has
3.21 K); the evaporator pinch (3.000 K) is the hot end of the exchanger
(`T_21 - T_5` = 15 °C − 12 °C), so `P_ev` follows from `T_dew_ev = 7 °C`.

Composition sweep (propane mole fraction; CoolSolve with CoolProp HEOS, and
the thermopack Peng-Robinson sweep of the notebook, reproduced):

| propane | COP | COP thermopack | VHC [kJ/m³] | VHC thermopack | glide [K] | glide thermopack | `P_ev` [bar] | `P_cd` [bar] |
|---|---|---|---|---|---|---|---|---|
| 0.0 | 4.9808 | 4.9533 | 1629.6 | 1633.1 | 0.00 | 0.00 | 1.998 | 7.244 |
| 0.1 | 5.0297 | 5.0042 | 1757.2 | 1754.8 | 2.43 | 2.15 | 2.143 | 7.714 |
| 0.2 | 5.0568 | 5.0378 | 1893.4 | 1886.3 | 4.25 | 3.90 | 2.310 | 8.244 |
| 0.3 | 5.0671 | 5.0554 | 2041.7 | 2030.3 | 5.52 | 5.23 | 2.504 | 8.846 |
| 0.4 | 5.0643 | 5.0579 | 2206.1 | 2190.2 | 6.29 | 6.13 | 2.732 | 9.536 |
| 0.5 | 5.0511 | 5.0467 | 2391.6 | 2370.6 | 6.60 | 6.58 | 3.002 | 10.334 |
| 0.6 | 5.0297 | 5.0232 | 2604.5 | 2577.6 | 6.44 | 6.52 | 3.328 | 11.268 |
| 0.7 | 5.0023 | 4.9894 | 2853.4 | 2820.4 | 5.78 | 5.93 | 3.730 | 12.376 |
| 0.8 | 4.9717 | 4.9488 | 3151.1 | 3112.5 | 4.56 | 4.71 | 4.238 | 13.713 |
| 0.9 | 4.9441 | 4.9092 | 3518.4 | 3476.1 | 2.68 | 2.77 | 4.907 | 15.361 |
| 1.0 | 4.9364 | 4.8901 | 3994.7 | 3952.4 | 0.00 | 0.00 | 5.842 | 17.450 |

With CoolProp the COP is highest at 30 % propane (5.0671, +1.7 % over pure
isobutane and +2.6 % over pure propane); with thermopack at 40 %, as the
notebook says (30-40 %). The VHC grows with the propane fraction and is
maximal for pure propane; the glide peaks (6.6 K) at 50 % propane. The 0 % and
100 % rows are the pure fluids (zero glide).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![T-Q diagram of the condenser](figures/zeotropic_hp_propane_isobutane_tq.png)
     + one-line caption -->

## Verification

Reference: the notebook model, re-run in a throw-away virtual environment
(Python 3.12, local TESPy clone commit `19425523`, CoolProp 8.0.0,
thermopack 2.2.3; REFPROP is not available). The class
`ZeotropicHeatPumpModel` was taken from the notebook cells unchanged except
for a third engine entry `heos`: back end `HEOS`, names `Propane`/`IsoButane`,
i.e. the same CoolProp equation of state as CoolSolve (8.0.0 in the venv,
8.1.0dev in the CoolSolve build).

1. **Notebook value reproduced** (thermopack, 50/50): COP 5.046708577260929,
   VHC 2370.5643209153664, glide 6.575896771585121, `p_ev` 2.9853744130205486
   bar, `p_cd` 10.310099188864099 bar — the stored outputs of the notebook,
   digit for digit.
2. **CoolProp HEOS re-run versus the CoolSolve `.sol`** (same equation of
   state; one design point takes 13.7 min in TESPy with CoolProp mixtures, so
   four compositions were run):

| propane | quantity | TESPy (HEOS) | CoolSolve | rel. diff. |
|---|---|---|---|---|
| 0.5 | COP | 5.0510513007 | 5.0510513007 | 1.2e-11 |
| 0.5 | VHC [kJ/m³] | 2391.610148 | 2391.610148 | 1.8e-12 |
| 0.5 | glide [K] | 6.6042148 | 6.6042148 | 1.3e-11 (abs.) |
| 0.5 | `p_ev` [bar] | 3.0018954 | 3.0018954 | 8.4e-13 |
| 0.5 | `p_cd` [bar] | 10.3342992 | 10.3342992 | 1.4e-11 |
| 0.3 | COP / VHC / `p_cd` | 5.0671369758 / 2041.664356 / 8.8464532 | 5.0671369760 / 2041.664356 / 8.8464532 | 2.7e-11 / 4.5e-12 / 3.0e-11 |
| 0.0 (isobutane) | COP / `p_cd` | 4.9807829009 / 7.2440965 | 4.9807829006 / 7.2440965 | 5.1e-11 / 2.8e-11 |
| 1.0 (propane) | COP / `p_cd` | 4.9363535643 / 17.4501425 | 4.9363535641 / 17.4501424 | 5.3e-11 / 1.8e-09 |

   Maximum relative difference over COP, VHC, `p_ev`, `p_cd` at the four
   compositions: 1.8e-09 (`p_cd` of pure propane); the glide of the pure fluids
   is zero in the reference and below 1e-7 K in CoolSolve. (TESPy with HEOS
   fails at 80 % propane — "critical point finding routine found 2 critical
   points" — and the other compositions were not run, 13 min each.)
3. **CoolSolve sweep versus the thermopack sweep of the notebook** (11
   compositions, table above): maximum deviation COP 0.95 %, VHC 1.24 %,
   condenser glide 0.35 K, optimum shifted from 40 % (thermopack) to 30 %
   propane. These are equation-of-state differences (Peng-Robinson against the
   CoolProp Helmholtz mixture model); the notebook reports 0.94 %, 1.23 % and
   0.35 K between thermopack and REFPROP, so CoolProp HEOS behaves like
   REFPROP here (REFPROP itself was not available to check).
4. **`Tmix_ph` against the built-in flash**: at eight profile points of the
   solution the function and `TEMPERATURE(fluid$, P=…, h=…)` differ by at most
   1.1e-8 K.

Not verified: the propane/pentane blend of the notebook (higher glide,
second half of the notebook), not translated.

## Niche

Nearest models: `CSL-0253` (high-temperature heat pump, zeotropic/transcritical,
blocked by `CS-GAP-FLUIDS-R1336MZZ`; its runnable variant is on pure R365mfc and
its pinch is the `MIN` of the end differences of the exchangers); `CSL-0133`
(propane heat pump with pinch-sized exchangers, pure fluid, three zones);
`CSL-0013` (TESPy basic heat pump) and `CSL-0250` (TESPy cascade, sectioned
exchangers, pure fluids). Checked against `CSL-0253` first, as the card
required: it is the same type of cycle but not the same study (its default is a
pure fluid, its exchangers are closed by end-point differences, there is no
composition parameter), so this is a new model, not a variant. What it adds:
**a heat pump with a real mixture working fluid** (`A[x]&B[y]`; the earlier
mixture files of the library are an ORC, `CSL-0153`, and a plate-exchanger
identification, `CSL-0124`, and `CSL-0253` runs on a pure fluid), an **internal
pinch on 51-point profiles** with the bubble and dew points as section
boundaries (the glide-matching mechanism: the condenser pinch sits at the dew
point inside the exchanger; adding that boundary changes the COP at 50 %
propane from 5.0764 to 5.0511, 0.5 %), the **composition sweep** with COP, VHC
and glide, and an EES-language `(P, h)` temperature function that makes
mixtures tractable (CoolProp's mixture `(P, h)` flash costs 0.1-0.2 s per
call).

## Source and attribution

Original model: the TESPy how-to *Zeotropic mixtures in a heat pump*
(`docs/how_to_guides/zeotropic_heat_pump.ipynb`, git history: Francesco Witte,
2026-09-21), [github.com/oemof/tespy](https://github.com/oemof/tespy), commit
`19425523ff7ecd67b36e7b90efe04a9480a9ebe3`, MIT licence (`LICENSE`: "Copyright
(c) Francesco Witte"). Components: `ZeotropicHeatPumpModel` (`ModelTemplate`),
`SectionedHeatExchanger` (`src/tespy/components/heat_exchangers/sectioned.py`,
`td_pinch_func`, `_get_moving_steps`, `_assign_steps`), connection parameters
`td_dew`/`td_bubble`. The sectioned-exchanger formulation is documented in
TESPy as following the NextGenerationHeatPumps repository (S. Quoilin; see
`CSL-0253`). Reference for TESPy: F. Witte and I. Tuschy, *TESPy: Thermal
Engineering Systems in Python*, Journal of Open Source Software 5(49), 2178
(2020). Properties: CoolProp (the notebook's thermopack and REFPROP engines are
replaced by CoolProp's HEOS mixture model, decision D12). Candidate `TSP-049`
of `sources/tespy/inventory.csv` (card C-445).

## Conversion log

- **2026-10-31 — translation (T-TRANSLATE)**: the `ModelTemplate` plumbing,
  the plots and the engine/back-end selection are removed; the network becomes
  simultaneous equations (state names above). Inputs as in `_create_network`:
  `td_dew = 5`, `td_bubble = 2`, `eta_s = 0.8`, `Q = -100 kW` (written
  positive), `td_pinch = 3` for both exchangers, waters at 3 bar with the
  inlet/outlet temperatures of the notebook, `dp = 0`. The TESPy unknowns
  `p_ev`, `p_cd`, the three mass flow rates are solved from the two pinch
  conditions, the condenser duty and the water outlet temperatures.
- **Mixture composition**: the notebook builds `Propane[x]&Isobutane[1-x]|molar`
  (mole fractions); CoolSolve's `'Propane[0.5]&IsoButane[0.5]'` is the same
  CoolProp HEOS mixture. Mole fractions must be numbers in the string, so the
  sweep is run by editing `fluid$`.
- **Extra section boundaries**: a first version with only the 51 equal-heat
  boundaries gave `P_cd` = 10.282 bar (COP 5.0764) against 10.334 bar (COP
  5.0511) of TESPy with HEOS. Reading `_get_moving_steps` showed why: with a
  single fluid entry (the mixture string) TESPy adds the bubble and dew points
  of the working fluid to the section boundaries. With the two candidates per
  exchanger (`dT_*_sat`) the agreement is 1e-11.
- **Performance — function `Tmix_ph`**: CoolProp's `(P, h)` flash of the
  propane/isobutane mixture takes about 0.1-0.2 s per call (single phase and
  two-phase alike; the `(P, x)` and `(P, T)` calls take 0.5 ms and 8 ms; same
  cost in Python, TESPy took 13.7 min for one design point). 102 profile
  points per iteration are then out of reach. `Tmix_ph` computes the same
  temperature in EES language by a secant iteration on `x` (two-phase) or `T`
  (single phase) with the fast calls; the model solves in about 7 s. This is
  a CoolProp property, not a CoolSolve gap; nothing is registered. The
  built-in `TEMPERATURE(…, h=…)` is kept for diagnostics (`T_2`, `T_4`).
- **Solver settings**: `coolsolve.conf` sets `tolerance = 1e-6`. The block mixes
  enthalpies of 1e5-6e5 J/kg whose CoolProp mixture evaluations carry a noise
  of about 1e-8 J/kg, so the default absolute tolerance of 1e-9 cannot be met
  and Newton did not stop even when started at the stored solution (6-section
  test file: 107 and 151 iterations, then a MaxIterations failure; with the
  setting: 4 iterations).
  Not registered (only an observation on this model; an unverified
  suggestion: a residual test relative to the scale of the equation terms).
- **Guesses**: the file needs `.initials` (SingularJacobian without). They are
  the converged solution; a fresh composition is started from a neighbouring one.
  The `.initials` contain no `fluid$` line (a string initial overrides the
  model).
- **Not translated**: the REFPROP and thermopack engines (only the CoolProp
  HEOS equation of state), the propane/pentane blend, the plots, solve-time
  bookkeeping.
- **Level**: equations 567 → 2; largest block 335 → 2; function and arrays → 1;
  discretised exchangers → 1; off-design/semi-empirical → 0; curated guesses
  and tuned `coolsolve.conf` → 1. Score 7 → level 4, lowered by one to **level
  3**: the physics is a basic single-stage cycle, the size comes from the
  profile discretisation, not from calibration or many coupled machines.

## Limitations and CoolSolve gaps

- No CoolSolve gap. CoolSolve supports the CoolProp mixture (`A[x]&B[y]`,
  warning `C003`: predictive mixture properties); mixture composition must be
  a literal in the string.
- Needs `.initials` and a relaxed tolerance (above); about 7 s per run.
- Mixture properties are predictive (CoolProp binary interaction parameters):
  the sweep differs from the thermopack sweep by up to 0.95 % in COP.

## Related models

- `CSL-0253` (high_temp_heat_pump_zeotropic_transcritical): high-temperature
  heat pump with an optional zeotropic/transcritical fluid; end-point pinch.
- `CSL-0013` (heat_pump_basic_tespy): the TESPy basic heat pump (pure R134a).
- `CSL-0250` (cascade_heat_pump_geothermal_dh): TESPy cascade with sectioned
  exchangers, pinch-sized, pure fluids.
- `CSL-0133` (heat_pump_propane_pinch): pure-propane heat pump with pinch-sized
  exchangers.
- `CSL-0127` (hx_constant_effectiveness_discretised) and `CSL-0138`
  (hx_moving_boundary_bell): other discretised exchanger formulations.
