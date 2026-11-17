# Temperature and pressure effects on combustion-product dissociation

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0264`

Equilibrium composition of the products of octane (C8H18) burned with 20 %
excess dry air. `CALL CHEM_EQUIL` returns the mole fractions of the 14
equilibrium species at a given pressure and temperature, so the exercise can
show that dissociation grows with temperature and with falling pressure.

| | |
|---|---|
| **Category** | Fundamentals › Combustion |
| **Fluids** | none (mole-fraction outputs only; the equilibrium data are the NASA-Glenn polynomials) |
| **Size** | 21 equations (largest block: 14, the `CHEM_EQUIL` call) |
| **Source** | ULiège MCI, TP1 exercise 2 (`Ex_2_T&P effects on dissociation.EES`) |
| **Authors** | P. Ngendakumana, R. Dickes |
| **License** | MIT |
| **CoolSolve** | 0.5.0@793f378 — verified |

## Problem statement

C8H18 burns with dry air at 20 % excess
(`C8H18 + 12.5*(O2+3.76*N2)*(1+0.20)`). Compute the equilibrium product
composition at 10 000 kPa and 2500 K. The original file also sweeps pressure
at fixed temperature and temperature at fixed pressure, and concludes that
dissociation increases when the temperature increases and when the pressure
decreases.

## Model

Element ratios per oxygen atom, as in the original: `A\O` = 0, `C\O` = 8/30,
`H\O` = 18/30, `N\O` = 3.76. `CALL CHEM_EQUIL(P, T, A\O, C\O, H\O, N\O : x_H2
… x_Ar)` returns the 14 mole fractions; `sumx` checks that they add to 1.
Pressure and temperature are passed in the units of the model (Pa, °C).

## How to run

```bash
coolsolve temperature_pressure_effects_dissociation.eescode
```

The shipped file is the default point (10 MPa, 2226.85 °C = 2500 K). The two
sweeps are `$IF PARAMETRICTABLE` blocks: CoolSolve drops them, because no
parametric table is attached. Guesses are in the `.initials` file. `x_CH4`
comes out near 1e-16 and raises warning `W002` (below the solver tolerance);
it does not move the other mole fractions.

## Results (default point, 10 MPa, 2500 K)

| Species | Mole fraction |
|---|---:|
| `x_N2` | 0.7372 |
| `x_H2O` | 0.1162 |
| `x_CO2` | 0.1029 |
| `x_O2` | 0.02907 |
| `x_NO` | 0.008275 |
| `x_OH` | 0.003320 |
| `x_CO` | 0.002221 |
| `sumx` | 1 |

<!-- FIGURE (added by the maintainer): mole fractions against T or P -->

## Verification

The EES file stores the last row of its temperature sweep, not the default
point: P = 10 000 kPa, T = 3000 K. That point was solved in a scratch copy
(`T = 2726.85` only) and compared with
`compare_solution.py … --ees-units`:

> 21 common variables, 10 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0

P, T, the four element ratios, `x_Ar`, `x_CH4` (2.4e-14 against a stored 0,
inside the absolute tolerance) and `sumx` agree. `x_CO2` differs by 6.06e-04
and `x_N2` by 3.44e-04. The ten differences are the minor species; the largest
is **9.41e-02** on `x_NO2` (3.80e-5 against 3.44e-5). `x_OH` is 5.73e-02 and
`x_NO` 3.74e-02. EES `Chem_Equil` uses older JANAF data; CoolSolve uses the
NASA-Glenn polynomials (Language Reference, `CALL CHEM_EQUIL`: major species
within about 0.4 %, OH, NO and NO2 within 4–10 %).

## Source and attribution

`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP1_Ex_1-5/Ex_2_T&P effects on dissociation.EES`
(EES 10.589, inventory `TM-0230`). Authors P. Ngendakumana and R. Dickes, as
for the rest of this TP. MIT.

## Conversion log

- **2026-10-22 — import**: `SI MASS DEG KPA C KJ` converted by hand to
  SI-°C-Pa-J (`P = 10000 kPa` → `1E7 Pa`, `T = 2500 K` → `2226.85 °C`);
  `$UnitSystem` removed. Equations otherwise unchanged.
- **Level**: 21 equations (0) + largest block 14 (1) + no user routine (0) +
  no multi-zone, calibration or curated guesses (0) = 1 → level 1.

## Limitations

Equilibrium composition only: no energy balance and no flame temperature
(`CSL-0150` closes that balance on the same call). The pressure and
temperature sweeps are not attached as a CoolSolve parametric table.

## Related models

- `CSL-0150` *adiabatic_flame_dissociation*: same TP series and the same
  `CHEM_EQUIL` call, with the adiabatic flame temperature solved on top.
