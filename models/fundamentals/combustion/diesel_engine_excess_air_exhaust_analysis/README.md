# Diesel engine: excess air and useful power from exhaust-gas analysis

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0058`

A diesel engine is fed with 4 g/s of diesel fuel (assimilated to `CH_n`) and
111 g/s of air, both at 25 °C; the exhaust gas leaves at 432 °C. The fuel
composition is obtained from its C and H mass fractions (`n` = 1.953), the
excess air from the fuel-air ratio, and the useful power from the five-box
energy balance of the course, which brings the combustion products from the
reference state to the exhaust temperature. The native file is **blocked** in
CoolSolve (`CS-GAP-FLUIDS-ALIAS`: the EES real-fluid substance
`CarbonMonoxide` is unknown); a faithful runnable variant
`diesel_engine_excess_air_exhaust_analysis_coolsolve.eescode` ships beside it
and is verified against EES (this README quotes its results).

| | |
|---|---|
| **Category** | Fundamentals › Combustion |
| **Fluids** | Air, CO, CarbonDioxide, water, nitrogen, oxygen (property calls at 25 °C and 432 °C, 1 atm) |
| **Size** | 58 equations, all explicit (largest block: 1); same size in the `_coolsolve` variant |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition 11 (combustion), exercise 3 (EES file `R11_E03_2022.EES`) |
| **Authors** | TBD (ULiège, course of S. Quoilin; repetition assistants per the collection metadata) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file blocked by `CS-GAP-FLUIDS-ALIAS`; runnable `_coolsolve` variant verified against EES (see *Verification*) |

## Problem statement

Determine the excess air and the useful power of a diesel engine fed with a
fuel mass flow of 4 g/s and an air mass flow of 111 g/s. The exhaust gas is at
432 °C; the air and the fuel are supplied at 25 °C. The diesel fuel has the
following characteristics: 0.86 kg of C and 0.14 kg of H per kg of fuel, a
lower heating value of 42.5 MJ/kg, a liquid specific heat of 2.2 kJ/kg·K.
(English paraphrase of the French statement; the original is an exercise of
the ULiège course *Thermodynamique appliquée*.)

## Model

The fuel is assimilated to `CH_n` with `n = y_H/y_C` from the mass fractions
(`y_C = z_C/12`, `y_H = z_H` kmol per kg of fuel → `n` = 1.953). The engine
runs with excess air, so the combustion is complete (`x_CO` = 0, `y` = 1).

Excess air: the fuel-air ratio `far = ṁ_e/ṁ_a` = 0.03604 and the
stoichiometric value `far_st` (from the molar masses and the stoichiometric
reaction) give `far·(1+e) = far_st` → e = 89.44 %, air coefficient
λ = 1.894.

Useful power — five-box balance of the original exercise:

| Box | Content | Value |
|---|---|---:|
| `Q_dot_1` | bring the air from its supply state to the reference state (25 °C, 1 atm) | 0 W |
| `Q_dot_2` | bring the fuel to the reference state | 0 W |
| `Q_dot_3` | heat released by the reaction at reference conditions (−ṁ_e·LHV) | −170.0 kW |
| `Q_dot_4` | heat lost in the unburned CO (zero: complete combustion) | 0 W |
| `Q_dot_5` | bring the products from the reference state to the exhaust temperature | +63.1 kW |

`Q_dot_1+…+Q_dot_5 = Q_dot_utile` = **−106.9 kW**: holding the exhaust at
432 °C, the chamber must reject 106.9 kW (the model's sign convention; the
quantity the exercise calls the useful power).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `m_dot_e` fuel flow | 4 g/s | `n` fuel H/C mole ratio | 1.9535 |
| `m_dot_a` air flow | 111 g/s | `e` excess air | 0.8944 |
| `z_C` / `z_H` | 0.86 / 0.14 | `lambda` air coefficient | 1.8944 |
| `T_su` / `T_ex` | 25 / 432 °C | `Q_dot_utile` useful power | −106.9 kW |
| `LHV_e` | 42.5 MJ/kg | `far_st` stoichiometric FAR | 0.06827 |

## How to run

Open `diesel_engine_excess_air_exhaust_analysis.eescode` in the CoolSolve GUI
and press *Solve*, or from a terminal:

```bash
coolsolve ./diesel_engine_excess_air_exhaust_analysis.eescode
```

The native file does not solve yet (see *Limitations and CoolSolve gaps*):
run the variant instead,

```bash
coolsolve ./diesel_engine_excess_air_exhaust_analysis_coolsolve.eescode
```

## Results

(Values of the `_coolsolve` variant, verified against EES; the two files
share the same equations — the variant only renames one substance.)

The excess air is 89.4 % (λ = 1.894) and the useful power is −106.9 kW. The
exhaust carries `q_N2` = 9.19 MJ and `q_H2O` = 4.09 MJ per kg of fuel above
the reference state; with 21.3 kg of N2, 3.15 kg of CO2 and 3.05 kg of O2 per
kg of fuel, `Q_dot_5` = 63.1 kW, which the balance subtracts from the 170 kW
released by the combustion.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): ideal-gas
     model, so a parametric sweep plot, e.g. Q_dot_utile and e vs the air mass
     flow m_dot_a (D7), figures/diesel_engine_excess_air_exhaust_analysis_sweep.png -->

## Verification

The comparison concerns the **`_coolsolve` variant** (the native file is
blocked, workflow §6).

0. **Native file**: square in CoolSolve's analysis (*"Equations: 58,
   Variables: 58, System square: Yes"*) but it fails on the EES real-fluid
   substance name: *"Unknown fluid: 'CarbonMonoxide'"* (`CS-GAP-FLUIDS-ALIAS`).
1. **EES stored solution** (`R11_E03_2022.EES`, 58 variables,
   `compare_solution.py --ees-units`, run on the variant):

   > 58 common variables, 9 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0

   Flagged rows (values in the converted units, rel. diff. as printed):
   `h_a_ref`/`h_a_su` 2.97e-01, `h_CO2_ex` 5.53e-01, `h_CO2_ref` 1.00e+00,
   `h_CO_ex` 1.20e+00, `h_CO_ref` 1.07e+00, `h_O2_ex` 4.07e-01,
   `h_O2_ref` 1.00e+00 — absolute enthalpies on different reference states
   (EES anchors its real-fluid `carbondioxide`/`oxygen` near 0 at 25 °C,
   CoolProp at the normal boiling point; the EES `CarbonMonoxide` value has no
   formation enthalpy, the CoolSolve ideal-gas `CO` has one; EES `air_ha` vs
   CoolSolve `Air`). Only **differences** of enthalpy enter the model, and
   they agree: the derived results all match —

   | Variable | EES (converted) | CoolSolve |
   |---|---:|---:|
   | `n` [-] | 1.95348837 | 1.95348837 |
   | `e` [-] | 0.89439886 | 0.89439471 |
   | `lambda` [-] | 1.89439886 | 1.89439471 |
   | `far` / `far_st` [-] | 0.036036036 / 0.068266626 | 0.036036036 / 0.068266476 |
   | `Q_dot_3` [W] | −170 000 | −170 000 |
   | `Q_dot_5` [W] | 63 127.4 | 63 136.0 |
   | `Q_dot_utile` [W] | −106 872.6 | −106 864.0 |

   The only flagged variable that feeds the results is `q_O2`:
   1.20727 MJ/kg (EES) vs 1.20942 MJ/kg (CoolSolve), rel. diff. 1.78e-03 —
   the real-fluid O2 enthalpy difference between 25 °C and 432 °C, within the
   ≤ 0.5 % EES-vs-CoolProp property tolerance; its weight in the balance is
   3.05 kg/kg of fuel, i.e. the 8.6 W difference on `Q_dot_utile`.
2. **Python/CoolProp solution of the same exercise** (companion `.py` of the
   2018-2019 version of the repetition, same statement, same data): prints
   excess air 89.4 %, air coefficient 189.4 %, useful power −106.9 kW — the
   three results of the variant, unchanged.

## Source and attribution

Exercise solution file of the ULiège course *Thermodynamique appliquée*
(MECA0002), repetition 11 (combustion), exercise 3; the file itself names no
author (EES licence stamp of the ULiège Thermodynamics Laboratory student
licence). A Python/CoolProp solution of the same exercise exists in the
collection (2018-2019 repetition folder) and was used as an additional
verification reference.

Source file (EES 10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R11/R11_E03_2022.EES`
(inventory candidate `TM-0395`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES 10.836, unit system `SI MASS DEG KPA C KJ`, decimal comma converted to
  the dot convention by the tool, EES licence/display tags removed, 58 stored
  variables, no lookup and no parametric table. The extraction was solved
  **unmodified** first: *"Equations: 58, Variables: 58, System square: Yes"* —
  the original is neither over- nor under-determined; it failed only on the
  fluid name `CarbonMonoxide` and on the kPa values fed to the property calls
  (both treated below). No `.initials` file is shipped: every equation is
  explicit and the variant converges from the default guesses.
- **Unit conversion by hand** (`docs/ees_import.md` §6): `p_ref = 101325 [Pa]`
  (101.325 kPa), `LHV_e = 42.5e6 [J/kg]` (42.5e3 kJ/kg), `c_e = 2200 [J/kg-K]`
  (2.2 kJ/kg-K), `h_fg_e = 270e3 [J/kg]` (270 kJ/kg), `HV_CO = 10.11e6 [J/kg]`
  (10.11e3 kJ/kg) — the original values are kept in the comments. The
  `enthalpy(...)` results become J/kg; every balance (`Q_dot_2`, `Q_dot_3`,
  `Q_dot_4`, `Q_dot_5`, `q_*`) is homogeneous, so no equation changed. No
  absolute-temperature relation, no unit factor and no empirical correlation
  in the model; the `Q_dot_*`/`q_*` values simply read in W and J/kg.
- **Fluid names**: the EES humid-air substance `air_ha`, used here without
  humidity (dry air), is written `Air` (ideal-gas dry air) in both files, as
  in `CSL-0052`; it is only evaluated at 25 °C and the difference
  `h_a_ref − h_a_su` is 0 in both tools. The real-fluid names of the products
  (`carbondioxide`, `water`, `nitrogen`, `oxygen`) are kept as in the
  original.
- **2026-10-05 — correction (orchestrator review)**: an earlier version of
  the library file wrote the ideal-gas substance `CO` where the original uses
  the **real-fluid** substance `CarbonMonoxide` — two different substances in
  EES — which rewrote valid EES around the CoolSolve gap. The **native file
  is restored** with the original `CarbonMonoxide` calls (`molarmass` and the
  two `enthalpy` calls) and is **blocked** by `CS-GAP-FLUIDS-ALIAS`. The CO
  version ships as the runnable variant
  `diesel_engine_excess_air_exhaust_analysis_coolsolve.eescode` (+ `.sol`),
  whose only difference is this one substitution; it uses no CoolSolve-only
  syntax (valid EES throughout). The substitution changes no result: the
  combustion is complete (`x_CO` = 0 → `fm_CO` = 0), so the CO terms
  (`q_CO`, `Q_dot_4`) are exactly 0 in both tools and no CO enthalpy enters
  the balance; the molar mass differs in the 4th digit only
  (28.001 vs 28.0101 kg/kmol, both quoted in the verification).
- **Comments** translated to English (paraphrasing the original ones);
  standard header added. The original comment on `LHV_e` says *"pouvoir
  calorifique de l'essence"* (gasoline) — a leftover of exercise 2, whose code
  this file reuses with new data and with `n` fitted from the mass fractions;
  it is written "fuel" here. `h_fg_e` is declared but used by no equation (as
  in the original; kept with a note). No dead code, no correction of the
  original equations.
- **Level**: taxonomy score 1 (58 equations → 1; largest block 1 → 0; no
  functions or arrays → 0; single zone → 0; no off-design/part-load → 0; no
  curated guesses → 0), which gives level 1; raised by one to **level 2** as
  assigned in the source inventory: a complete combustion balance (molar
  balances, mass fractions, five-box enthalpy model) of an applied
  thermodynamics course, like the other combustion exercises of the library.
- **Duplicate group DG-0096** (decision D4): `R11_E02_2022.EES` (TM-0394,
  exercise 2) is the same model with other data (gasoline `CH_1.95`,
  incomplete combustion with `x_CO` = 0.02, `T_ex` = 700 °C, 46 g/s of air
  and 3 g/s of fuel, `LHV` 44 MJ/kg, `c_e` 2.4 kJ/kg·K) and the other closure
  for the fuel: `n = 1.95` given, instead of fitted from `z_C`/`z_H` here. It
  is `merged` (same system, other data and the one closure difference); it is
  described only — no variant file shipped; the equations otherwise are
  identical (equation diff after stripping comments: data values + the `n`
  block).

## Limitations and CoolSolve gaps

- **Blocked**: the EES **real-fluid** substance `CarbonMonoxide` (used by the
  source file, which stores `MM_CO` = 28.001 kg/kmol and the CO enthalpies at
  25 °C and 432 °C) is unknown to CoolSolve — *"Unknown fluid:
  'CarbonMonoxide'"* — although CoolProp provides the fluid under the same
  name. The ideal-gas `CO` **is a different substance** (in EES as in
  CoolSolve), so the native file cannot simply be renamed. Registered as
  `CS-GAP-FLUIDS-ALIAS` (the only missing real-fluid long name of those
  verified: `Methane`, `Ethane`, `Propane`, `Hydrogen`, `Helium`, `Argon`,
  `Neon`, `CarbonDioxide`, `Nitrogen`, `Oxygen`, `Water` are all known). The
  runnable `_coolsolve` variant substitutes the ideal-gas `CO` (see
  *Conversion log*).
- The absolute enthalpies of the products carry the reference state of each
  property backend; only their differences are physical, and the model uses
  differences only (see *Verification*).
- `Q_dot_utile` is negative by the model's sign convention: it is the power
  to withdraw from the chamber so that the exhaust leaves at 432 °C.
- Water in the exhaust is evaluated as pure superheated steam
  (`water`), the air as dry air; no condensation in the exhaust is considered
  (as in the original).

## Related models

- `CSL-0046` *octane_combustion_400pct_air*: combustion of octane with 400 %
  excess air, exercise 1 of the same repetition series of the same course.
- `CSL-0005` *cpbar_combustion_products*: mean specific heats of combustion
  gases (`cpbar`, `gamma`), the property functions of the ULiège combustion
  toolkit.
