# Engine cylinder count and operating parameters at rated power

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0331`

An H2 four-stroke engine is sized from bore, stroke, mean piston speed and
rated shaft power. The cylinder count comes out non-integer, is rounded up,
and the mean effective pressure is corrected so the rated power is kept. At
300 kW the oxidiser is 30 % O2 and 70 % recirculated H2O by mass; combustion
is stoichiometric and the volumetric efficiency follows from the inlet
mixture molar mass.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | H2, O2, H2O |
| **Size** | 43 equations (largest block: 1) |
| **Source** | ULiège MCI, TP2 exercise 3 (`Exercice_3_Param opératoires et combustion.EES`) |
| **Authors** | Ph. Ngendakumana, Rémi Dickes |
| **License** | MIT |
| **CoolSolve** | 0.5.0@793f378 — verified |

## Problem statement

A four-stroke engine delivers 400 kW at rated speed. Bore 110 mm, stroke
150 mm, mean piston speed 17.5 m/s, intermittency factor 0.5. Find the
displacement per cylinder and the number of cylinders; round the count up and
correct the mean effective pressure. In submerged operation the engine
delivers 300 kW with speed following W ∝ N³. The fuel is H2, the oxidiser is
30 % O2 by mass, φ = 1, efficiency 0.32, LHV 120 000 kJ/kg. At the inlet
(180 kPa, 388 K) compute the mixture molar mass, the density and the
volumetric efficiency. `LowerHeatingValue(H2)` checks the LHV of the statement.

## Model

`V_s = pi*D^2/4*L`, speed from the mean piston speed, `n_c` from the rated
power and `DELTAp_bar_e_n`, then `N_cyl = CEIL(n_c)` with `DELTAp_bar_e_new`
keeping the rated power. Part load closes the same power law and a cube law
on speed. Stoichiometry of `H2 + (0.5 O2 + alpha H2O)` fixes `alpha` from the
O2 mass fraction; the fuel flow follows from the efficiency and the stated
LHV. `epsilon_v = M_dot_oxydant/(rho_inlet*V_dot_th_2)` with the ideal-gas
density of the mole-fraction mixture.

## How to run

```bash
coolsolve engine_cylinder_count.eescode
```

Guesses (speeds, `alpha`, volume flows) are in `engine_cylinder_count.initials`.

## Results

| Variable | CoolSolve | EES |
|---|---:|---:|
| V_s [m³] | 0.0014255 | 0.0014255 |
| n_c [-] | 7.4005 | 7.4005 |
| N_cyl [-] | 8 | 8 |
| N_1 / N_2 [rev/min] | 3500 / 3180 | 3500 / 3180 |
| DELTAp_bar_e_new [kPa] | 1202.6 | 1202.6 |
| alpha [-] | 2.0722 | 2.0722 |
| M_dot_f [kg/s] | 0.0078125 | 0.0078125 |
| epsilon_v [-] | 0.7911 | 0.7910 |
| LHV_f_EES [kJ/kg] | 119 961 | 119 946 |

## Verification

`compare_solution.py engine_cylinder_count.sol reference/ees_variables.csv --ees-units`:

> 43 common variables, 1 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1

The flagged row is `r`: EES stores 0.53659 kJ/(kg·K) with a blank units cell,
so the comparator does not scale it; CoolSolve's 536.605 J/(kg·K) is the same
value (printed relative difference 9.99e-01). Excluding that row the maximum
is **1.21e-04**, on `LHV_f_EES`: `LowerHeatingValue(H2)` from the NASA-Glenn
formation enthalpies against the EES value. Speeds, cylinder count and the
fuel flow agree to the stored digits.

## Source and attribution

`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP2_Ex_1-3/Exercice_3_Param opératoires et combustion.EES`
(EES 10.589, Ph. Ngendakumana, Rémi Dickes). MIT.

## Conversion log

- **2026-11-02 — import**: `SI MASS DEG KPA K KJ` converted by hand to
  SI-°C-Pa-J (powers in W, pressures in Pa, `LHV_f` in J/kg, `T_inlet` =
  114.85 °C, `R_u` = 8314 J/(kmol·K), ideal-gas law on `T_inlet+273.15`).
  French comments translated. The unused variable `N` is not carried over.
- **Level**: score 0 on the taxonomy count, raised to level 2 because the
  exercise joins a sizing closure and a combustion stoichiometry (inventory
  level 2).

## Limitations

Fixed geometry and one part-load point. The LHV used for the fuel flow is the
statement value (120 MJ/kg); `LHV_f_EES` is only the check.

## Related models

- `CSL-0279` *engine_bsfc_bore_stroke_afr*: bore and stroke sizing; the
  cylinder count is an input.
- `CSL-0185` *diesel_injection_sizing*: displacement and volumetric
  efficiency with a given cylinder count.
