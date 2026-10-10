# Combustion of octane with 400 % theoretical air

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** (verified runnable variant) &nbsp;|&nbsp; `CSL-0046`

Introductory combustion exercise: octane C8H18 at 25 °C is burned with 400 %
theoretical air, also at 25 °C, in a steady-flow adiabatic process. The
adiabatic flame temperature follows from the first law written on the
combustion reaction; the fuel-air ratio (dosage) and the stoichiometric
dosage follow from the molar masses.

| | |
|---|---|
| **Category** | Fundamentals › Combustion |
| **Fluids** | Ideal gases CO2, H2O, O2, N2 (real Water for a diagnostic line) |
| **Size** | 35 equations (largest block: 5) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition 11, exercise 1 (EES file `R11_E01_2022.EES`) |
| **Authors** | TBD (ULiège course MECA0002 repetition team) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file blocked by `CS-GAP-FLUIDS-C8H18`; the runnable `_coolsolve` variant is verified against the EES stored solution (see *Verification*) |

## Problem statement

Octane at 25 °C is burned with 400 % theoretical air at 25 °C in a
steady-flow process. Determine the adiabatic flame temperature, the dosage
(fuel-air ratio) and the stoichiometric dosage; study also the effect of the
excess air on the adiabatic flame temperature. (English paraphrase of the
original French statement.)

## Model

Combustion reaction in excess air (as in the original course notes):

$$C_xH_y + \lambda\,(x+\tfrac{y}{4})\,O_2 + 3.76\,\lambda\,(x+\tfrac{y}{4})\,N_2
\rightarrow x\,CO_2 + \tfrac{y}{2}H_2O + (\lambda-1)(x+\tfrac{y}{4})\,O_2 + 3.76\,\lambda\,(x+\tfrac{y}{4})\,N_2$$

with x = 8, y = 18, λ = 4. The reaction is adiabatic and without work, so the
reactant enthalpy equals the product enthalpy (computed for 1 kmol of fuel):

$$H_R = n_f\,h^0_{f,f} = H_P = \sum_i n_i\left(h^0_{f,i} + (h_i(T_{AF}) - h_i(T_{ref}))\,M_i\right)$$

The species enthalpies are the **ideal-gas** EES substances (`CO2`, `H2O`,
`O2`, `N2`): their enthalpies include the formation enthalpies, and the
formation enthalpy of pure O2 and N2 is zero (CoolSolve implements the same
EES/JANAF convention). The dosage is `far = n_f·MM_f / m_air` of the
reaction above, and `far_st` the same at λ = 1. Two extra lines of the
original (`h_H2O_taf_bis`, `h_H2O_ref_bis`) evaluate **real-fluid** Water at
TAF and 1 atm as a diagnostic; both are kept (as in the original, both at
T = TAF).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_su` / `T_ref` | 25 / 25 °C | `TAF` adiabatic flame temperature | 688.6 °C (961.7 K) |
| `lambda` theoretical air | 4 (400 %) | `far` dosage | 0.01664 |
| `n_f` basis | 1 kmol C8H18 | `far_st` stoichiometric dosage | 0.06654 |
| `h_0f_f` | −249 952 kJ/kmol | products per kmol fuel: `n_CO2`/`n_H2O`/`n_O2`/`n_N2` | 8 / 9 / 37.5 / 188 kmol |
| `h_0f_CO2` / `h_0f_H2O` | −393 522 / −241 827 kJ/kmol | `H_R` = `H_P` | −249.95 MJ |

(`T_su` is stated by the exercise but not used in the equations, as in the
original.)

## How to run

The native file `octane_combustion_400pct_air.eescode` is valid EES but is
**blocked** in CoolSolve: `molarmass(C8H18)` fails because octane is not in
the CoolSolve fluid registry (gap `CS-GAP-FLUIDS-C8H18`). Run the variant:

```bash
coolsolve ./octane_combustion_400pct_air_coolsolve.eescode
```

The variant differs by one line only (`MM_f = 114.23` instead of
`molarmass(C8H18)`); it uses no CoolSolve-only syntax.

## Results

CoolSolve gives TAF = 688.6 °C with 400 % theoretical air (EES: 688.7 °C);
the dosage far = 0.0166 is five times smaller than the stoichiometric dosage
far_st = 0.0665 because λ = 4.

Excess-air effect on TAF (reproduced from the model; the original's
parametric study is configured in the EES GUI and not stored in the file):

| λ (theoretical air) | 1.2 | 1.5 | 2 | 3 | 4 | 6 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| TAF [°C] | 1848 | 1553 | 1233 | 880 | 689 | 484 | 375 |

The flame temperature decreases monotonically with the excess air: the extra
O2 and N2 are heated without releasing energy. Near stoichiometric
conditions (λ → 1) the temperature becomes very sensitive to the excess air.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep of TAF vs lambda
     (ideal-gas model: no thermodynamic diagram), figures/octane_combustion_400pct_air_*.png -->

## Verification

The runnable `_coolsolve` variant was solved with CoolSolve and compared with
the solution stored in the original EES file
(`compare_solution.py octane_combustion_400pct_air_coolsolve.sol
reference/ees_variables.csv --ees-units`, converting the kPa/kJ reference by
the tool):

> 35 common variables, 3 differ (rtol=0.001); only in EES: 3; only in CoolSolve: 0

The 3 flagged variables are unit-annotation artifacts of the comparison, both
hand-checked:

- `h_H2O_taf_bis`, `h_H2O_ref_bis`: stored by EES **without units** (kJ/kg),
  not converted by the tool: 3903.74 kJ/kg vs 3.9034e6 J/kg, rel. diff 8.7e-5;
- `TAF_K`: stored in K, but the tool converts K→°C for variable names
  starting with T: 961.86 K vs 961.71 K, rel. diff 1.5e-4.

Over all common variables the maximum relative deviation is **2.2e-4**, on
`TAF` (688.56 °C vs 688.71 °C): it comes from the ideal-gas enthalpy data
(CoolSolve Çengel-based species data vs EES JANAF). The dosages agree to
1.2e-5. The stored records `x`, `y`, `mm` of the EES file are stale variables
of an earlier version, not part of the equations; ignored.

| Variable | EES | CoolSolve (variant) |
|---|---:|---:|
| `TAF` [°C] | 688.71 | 688.56 |
| `far` [-] | 0.0166361 | 0.0166359 |
| `far_st` [-] | 0.0665444 | 0.0665436 |
| `H_R` = `H_P` [J] | −2.49952e8 | −2.49952e8 |
| `h_H2O_taf_bis` [J/kg] | 3.90374e6 | 3.90341e6 |

## Source and attribution

Exercise solution of the course *Thermodynamique appliquée* (MECA0002),
Université de Liège, repetition session 11 (2022-2023). The EES file itself
names no author (only the laboratory licence tag); the inventory attributes
the course material to S. Quoilin with repetition assistants N. Paulus and
B. Dechesne (from companion Python/Word metadata), to be confirmed by the
maintainer.

Source file (EES 10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R11/R11_E01_2022.EES`
(inventory candidate `TM-0393`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `SI MASS DEG KPA C KJ` with decimal commas (converted by the
  tool); converted by hand to SI-°C-Pa-J (ees_import.md §6): the three
  formation enthalpies ×1000 (`h_0f_f = -249952E3 [J/kmol]`, "-249952
  kJ/kmol in the original", likewise CO2 and H2O) and `p_ref = 101325 [Pa]`
  (101.325 kPa in the original); the enthalpy balances stay unchanged (all
  terms switch consistently from kJ to J). No absolute-temperature relation
  (`TAF_K = TAF + 273.15` is unchanged in °C), no other unit-dependent
  constant. Comments translated to English, standard header added, equations
  otherwise unchanged. `.initials` shipped for the variant (converted stored
  values; the stale records `x`, `y`, `mm` dropped).
- **Duplicate group DG-0095** (2 files, triaged per workflow §2):
  - `TM-0537` (`THD10_R11.zip!/THD10_R11_E1.EES`, 2017-2018 version,
    `duplicate`): stripped-equation diff identical to TM-0393 except three
    diagnostic lines added in 2022 (`p_ref`, `h_H2O_taf_bis`,
    `h_H2O_ref_bis`; no effect on the results). Stored solution consistent:
    far and far_st identical, TAF 688.115 °C (older EES species data).
- **Runnable variant** (workflow §6): one line changed, `MM_f =
  molarmass(C8H18)` → `MM_f = 114.23` (the value EES returns), because
  `C8H18` is not in the CoolSolve fluid registry. Logged in the variant
  header; no CoolSolve-only syntax.
- **Level**: 35 equations (0) + largest block 5 (0) + no functions/arrays (0)
  + no multi-zone (0) + no calibration/dynamics (0) + no curated guesses (0)
  = 0 → level 1.

## Limitations and CoolSolve gaps

- `CS-GAP-FLUIDS-C8H18` (blocks the native file): `molarmass(C8H18)` —
  octane is an ideal-gas substance of EES but is not registered in CoolSolve
  (no ideal-gas octane, `n-Octane`/`IsoOctane` not in CoolProp standard
  fluids). Workaround in the variant: the constant 114.23 kg/kmol.
- The warning `enthalpy(): fluid 'CO2'. Did you mean 'CO2'?`
  (`CS-BUG-FLUID-HINT-CO2`) is informational; the results are correct.
- No EES reference is available for the excess-air sweep (GUI parametric
  study, not stored in the file): the sweep table above is a CoolSolve
  result, sanity-checked for monotonicity.
- Water is assumed to remain gaseous in the products (formation enthalpy of
  H2O(g), as in the original).

## Related models

- `CSL-0005` *cpbar_combustion_products*: function library for the mean
  specific heat of combustion products (same course, combustion session).
- `CSL-0058` *diesel_engine_excess_air_exhaust_analysis*: exercise 3 of the
  same repetition series, same five-box combustion balance with a diesel fuel
  whose `CH_n` is fitted from its mass fractions.
- `CSL-0150` *adiabatic_flame_dissociation*: the same adiabatic flame
  temperature with **chemical-equilibrium dissociation** of the products
  (EES built-in `Chem_Equil`, native file blocked), for CH4 or fuel
  oil instead of octane.
