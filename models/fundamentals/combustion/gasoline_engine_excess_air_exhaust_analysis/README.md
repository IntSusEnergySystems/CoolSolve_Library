# Gasoline engine: excess air and useful power from exhaust-gas analysis

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0266`

A gasoline engine is fed with 3 g/s of gasoline (assimilated to `CH1.95`) and
46 g/s of dry air, both at 20 °C; the exhaust gas leaves at 700 °C and its dry
composition shows a CO mole fraction of 2 % (incomplete combustion). The
excess air follows from the fuel-air ratio and the CO balance; the unburned
losses and the "useful power" (the heat to withdraw from the chamber) from the
five-box energy balance of the course, with the fuel brought to the reference
state in the vapour phase (its LHV is defined for gaseous fuel) and the
products from the reference state to the exhaust temperature. The native file
is **blocked** in CoolSolve (`CS-GAP-FLUIDS-ALIAS`: the EES real-fluid
substance `CarbonMonoxide` is unknown); a faithful runnable variant
`gasoline_engine_excess_air_exhaust_analysis_coolsolve.eescode` ships beside it
and is verified against EES (this README quotes its results).

| | |
|---|---|
| **Category** | Fundamentals › Combustion |
| **Fluids** | Air, CO, CO2, H2O, N2, O2 (ideal-gas property calls at 20/25/700 °C; molar mass of CO from the real-fluid name) |
| **Size** | 54 equations, all explicit (largest block: 1); same size in the `_coolsolve` variant |
| **Source** | ULiège — THD course (2010), repetition 11 (combustion), exercise 2 (EES file `THD10_R11_E2.EES` inside `THD10_R11.zip`) |
| **Authors** | Stéphane Bertagnolio, S. Borguet (per the collection inventory; file itself carries only the ULiège lab licence stamp) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — native file blocked by `CS-GAP-FLUIDS-ALIAS`; runnable `_coolsolve` variant verified against EES (see *Verification*) |

## Problem statement

A gasoline engine is fed with gasoline, assimilated to `CH1.95`, and dry air
at 20 °C. Measurements on the exhaust gas give the indications of the
exercise data (CO mole fraction in the dry gas 2 %, exhaust at 700 °C). The
gasoline has the characteristics given in the data (lower heating value
44 MJ/kg, liquid specific heat 2.4 kJ/kg·K, latent heat of vaporisation
305 kJ/kg). Determine the loss in unburned products and the power supplied to
the engine by the combustion. (English paraphrase of the French statement of
the 2010 exercise; never copied.)

## Model

The fuel is `CH_n` with `n` = 1.95 given; the combustion is incomplete
(`x_CO` = 0.02 in the dry exhaust → `y` = 0.8601 of the carbon burned to CO2).

Excess air: the fuel-air ratio `far` = ṁ_e/ṁ_a = 0.06522 and the
stoichiometric value `far_st` (from the molar masses and the stoichiometric
reaction) give `far·(1+e) = far_st` → e = 4.71 %, air coefficient
λ = 104.71 %.

Useful power — five-box balance of the original exercise:

| Box | Content | Value |
|---|---|---:|
| `Q_dot_1` | bring the air from its supply state to the reference state (20 → 25 °C) | 231 W |
| `Q_dot_2` | bring the fuel to the reference state **and vaporise it** (LHV defined for gaseous fuel) | 951 W |
| `Q_dot_3` | heat released by the reaction at reference conditions (−ṁ_e·LHV) | −132.0 kW |
| `Q_dot_4` | heat lost in the unburned CO | 8.52 kW |
| `Q_dot_5` | bring the products from the reference state to the exhaust temperature | +38.36 kW |

`Q_dot_1+…+Q_dot_5 = Q_dot_utile` = **−83.94 kW**: holding the exhaust at
700 °C, the chamber must reject 83.9 kW (the model's sign convention; the
quantity the exercise calls the power supplied by the combustion).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `m_dot_e` fuel flow | 3 g/s | `y` carbon to CO2 | 0.8601 |
| `m_dot_a` air flow | 46 g/s | `e` excess air | 0.04710 |
| `n` H/C mole ratio | 1.95 | `lambda` air coefficient | 104.71 % |
| `x_CO` CO in dry exhaust | 0.02 | `Q_dot_utile` useful power | −83.94 kW |
| `T_su` / `T_ex` | 20 / 700 °C | `Q_dot_4` unburned-loss power | 8.52 kW |
| `LHV_e` | 44 MJ/kg | `far_st` stoichiometric FAR | 0.06829 |

## How to run

Open `gasoline_engine_excess_air_exhaust_analysis.eescode` in the CoolSolve
GUI and press *Solve*, or from a terminal:

```bash
coolsolve ./gasoline_engine_excess_air_exhaust_analysis.eescode
```

The native file does not solve yet (see *Limitations and CoolSolve gaps*):
run the variant instead,

```bash
coolsolve ./gasoline_engine_excess_air_exhaust_analysis_coolsolve.eescode
```

No `.initials` file is shipped: every equation is explicit and the variant
converges from the default guesses (17 iterations).

## Results

(Values of the `_coolsolve` variant, verified against EES; the two files
share the same equations — the variant only renames one substance in one
`molarmass` call.)

The excess air is 4.71 % (λ = 104.71 %) and the useful power is −83.94 kW.
Per kg of fuel the exhaust carries `q_N2` = 8.65 MJ, `q_CO2` = 1.97 MJ,
`q_H2O` = 1.74 MJ, `q_CO` = 0.209 MJ and `q_O2` = 0.219 MJ above the
reference state (38.36 kW in total), against the 132 kW released by the
combustion; 8.52 kW leave in the unburned CO.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): ideal-gas
     model, so a parametric sweep plot, e.g. Q_dot_utile and e vs the air mass
     flow m_dot_a (D7), figures/gasoline_engine_excess_air_exhaust_analysis_sweep.png -->

## Verification

The comparison concerns the **`_coolsolve` variant** (the native file is
blocked, workflow §6).

0. **Native file**: 54 equations / 54 variables, but it fails on the EES
   real-fluid substance name: *"Unknown fluid: 'CarbonMonoxide'"*
   (`CS-GAP-FLUIDS-ALIAS`).
1. **EES stored solution** (`THD10_R11_E2.EES`, 54 variables,
   `compare_solution.py --ees-units`, run on the variant):

   > 54 common variables, 6 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0

   Flagged rows (values in the converted units, rel. diff. as printed):
   `h_a_ref` 2.97e-01, `h_a_su` 3.00e-01 (absolute Air enthalpies: EES anchors
   its ideal-gas `air` at 0 for 0 K, CoolProp keeps its own reference — only
   their difference enters), `h_N2_ex` 1.24e-03, `q_N2` 1.24e-03, `q_CO2`
   2.73e-03, `Q_dot_1` 1.71e-03 (ideal-gas property differences EES vs
   CoolProp, all within the ≤ 0.5 % property tolerance; `Q_dot_1` weighs
   0.23 kW). No CO enthalpy is flagged: the ideal-gas `co` of the source
   matches the NASA-based CoolProp enthalpies within rtol. The derived
   results all match —

   | Variable | EES (converted) | CoolSolve |
   |---|---:|---:|
   | `y` [-] | 0.8600684861 | 0.8600702364 |
   | `e` [-] | 0.04711672042 | 0.04710448406 |
   | `lambda` [%] | 104.711672 | 104.710448 |
   | `far` / `far_st` [-] | 0.0652173913 / 0.0682902209 | 0.0652173913 / 0.0682894229 |
   | `Q_dot_2` [W] | 951 | 951 |
   | `Q_dot_3` [W] | −132 000 | −132 000 |
   | `Q_dot_4` [W] | 8518.97 | 8521.64 |
   | `Q_dot_5` [W] | 38 377.5 | 38 357.9 |
   | `Q_dot_utile` [W] | −83 921.5 | −83 938.0 |

   (`e` and `Q_dot_utile` agree to 2.6e-04 and 2.0e-04 relative; the small
   residual comes from the ideal-gas N2/CO2 property differences above, which
   weigh in `Q_dot_5`.)

## Source and attribution

Exercise solution file of the ULiège THD course (2010), repetition 11
(combustion), exercise 2; the file itself names no author (EES licence stamp
of the ULiège Thermodynamics Laboratory student licence). The collection
inventory attributes the THD repetition files of that period to
S. Bertagnolio and S. Borguet.

Source file (EES 8.423, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R11.zip!/THD10_R11_E2.EES`
(inventory candidate `TM-0538`).

## Conversion log

- **2026-10-22 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES 8.423, unit system `SI MASS DEG KPA C KJ`, decimal-comma conversion by
  the tool, ULiège lab licence tag removed, 54 stored variables, no lookup and
  no parametric table. The extraction was solved **unmodified** first: 54
  equations / 54 variables, *System square: Yes* — the original is neither
  over- nor under-determined; it failed only on `molarmass(CarbonMonoxide)`
  (treated below). No `.initials` file is shipped: the variant converges from
  the default guesses.
- **Unit conversion by hand** (`docs/ees_import.md` §6): `LHV_e = 44e6 [J/kg]`
  (44e3 kJ/kg), `c_e = 2400 [J/kg-K]` (2.4 kJ/kg-K), `h_fg_e = 305e3 [J/kg]`
  (305 kJ/kg), `HV_CO = 10.11e6 [J/kg]` (10.11e3 kJ/kg) — the original values
  are kept in the comments. The `enthalpy(...)` results become J/kg; every
  balance (`Q_dot_*`, `q_*`) is homogeneous, so no equation changed. No
  absolute-temperature relation, no unit factor and no empirical correlation
  in the model. `lambda` is a percentage in the original (`(1+e)*100`) and
  stays one (`[%]`).
- **Fluid names**: the original's ideal-gas formula names (`air`, `co2`,
  `co`, `H2o`, `N2`, `O2`) are kept in the enthalpy and molar-mass calls; the
  EES **real-fluid** long name `CarbonMonoxide` (only in
  `MM_CO = molarmass(CarbonMonoxide)`) stays in the native file and is
  substituted by ideal-gas `CO` in the runnable variant (see *Limitations*).
- **Comments** translated to English (paraphrasing the original ones);
  standard header added. The original comments on `c_e` and `h_fg_e` are
  swapped (*"chaleur latente de vaporisation"* on the specific heat and
  *"chaleur specifique"* on the latent heat); the values and equations make
  the intent clear and the comments are corrected here (the 2022 version of
  the exercise fixed them too). `MM_a = molarmass(air)` is declared but used
  by no equation (as in the original; kept with a note). No dead code, no
  correction of the original equations.
- **Level**: taxonomy score 1 (54 equations → 1; largest block 1 → 0; no
  functions or arrays → 0; single zone → 0; no off-design/part-load → 0; no
  curated guesses → 0), which gives level 1; raised by one to **level 2** as
  assigned in the source inventory: a complete combustion balance (molar
  balances, mass fractions, five-box enthalpy model, incomplete combustion)
  of an applied thermodynamics course, like the other combustion exercises of
  the library.
- **Relation to `CSL-0058`** (same exercise family; equation diff after
  stripping comments): `CSL-0058` is the 2022 *diesel* version (TM-0395,
  merged TM-0394). This 2010 gasoline version differs by (1) the gasoline
  data (`n` = 1.95 given, `x_CO` = 0.02, `T_ex` = 700 °C, 3/46 g/s,
  `LHV` 44 MJ/kg — the same data as the merged TM-0394), (2) the vaporisation
  term `+ h_fg_e` in `Q_dot_2` (the 2022 files dropped it), (3) `lambda` in
  percent, and (4) the `far_st` written directly instead of `far` via
  `lambda` (mathematically equivalent closures). The inventory row of
  TM-0394 (C-137) was left `merged` into `CSL-0058`; TM-0538 was imported as
  its own model per its card (planning C-137/C-306: "similar but not
  grouped").

## Limitations and CoolSolve gaps

- **Blocked**: the EES **real-fluid** substance `CarbonMonoxide` (used by the
  source file for the molar mass of CO, `MM_CO` = 28.001 kg/kmol) is unknown
  to CoolSolve — *"Unknown fluid: 'CarbonMonoxide'"* — although CoolProp
  provides the fluid under the same name. The ideal-gas `CO` **is a different
  substance** (in EES as in CoolSolve), so the native file cannot simply be
  renamed. Registered as `CS-GAP-FLUIDS-ALIAS` (same gap as `CSL-0058`). The
  runnable `_coolsolve` variant substitutes the ideal-gas `CO` in this one
  call: `MM_CO` becomes 28.0101 instead of 28.001 kg/kmol (3.2e-4 relative),
  which shifts `fm_CO`, `q_CO` and `Q_dot_4` by the same relative amount
  (+2.7 W on `Q_dot_4`) — within the property tolerance quoted above.
- The absolute enthalpies of the products carry the reference state of each
  property backend; only their differences are physical, and the model uses
  differences only (see *Verification*).
- `Q_dot_utile` is negative by the model's sign convention: it is the power
  to withdraw from the chamber so that the exhaust leaves at 700 °C.
- Water in the exhaust is evaluated as pure superheated steam (`H2o`), the
  air as dry air; no condensation in the exhaust is considered (as in the
  original).

## Related models

- `CSL-0058` *diesel_engine_excess_air_exhaust_analysis*: the same five-box
  combustion-balance model in its 2022 diesel version (TM-0395, with TM-0394
  merged); differences listed in the conversion log.
- `CSL-0046` *octane_combustion_400pct_air*: combustion of octane with 400 %
  excess air, exercise 1 of the same repetition series.
- `CSL-0005` *cpbar_combustion_products*: mean specific heats of combustion
  gases (`cpbar`, `gamma`), the property functions of the ULiège combustion
  toolkit.
