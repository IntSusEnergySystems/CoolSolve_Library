# CO2 in a 200 L tank: real-gas mass and ideal-gas error (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0225`

A 200 L tank holds carbon dioxide at 35 °C and 2 MPa. The model computes the
mass from the real-gas specific volume and the percentage error of the mass
obtained from `volume(CO2)`. A second specific volume uses the ideal-gas
constant. The vapour quality is the original check that the state is not
two-phase. Teaching exercise of the ULiège course *Thermodynamique appliquée*
(MECA0002), repetition 1 (2022-2023).

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | CarbonDioxide, CO2 |
| **Size** | 13 equations (largest block: 1) |
| **Source** | thermo_models, file `R1_E2_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (see *Verification*) |

## Problem statement

A 200 L tank contains carbon dioxide at 35 °C and 2 MPa.

a. Calculate the mass of gas in the tank.

b. Evaluate the percentage error made in a. if the ideal-gas model is used.

The equation window also computes a second ideal-gas specific volume from the
gas constant, and the vapour quality, as a check that the state is gaseous.
The inventory titles this file exercise 3.9.

## Model

One tank state, as written in the equation window. The real-gas mass uses
`volume(CarbonDioxide)`. The ideal-gas mass uses `volume(CO2)`. The percentage
error is \((m_{gp}-m)/m \times 100\).

The second method is the ideal-gas law written in the original,
\(v = r T / p\), with \(r = R/M\). `R` is 8.3144621 J/(mol·K). `MolarMass`
returns kg/kmol, so `r_CO2` is in J/(g·K), the same number as in the stored
solution. With `p` in Pa the specific volume is

\[
v_{gp2} = r_{CO2}\, T / (p/1000)
\]

The quality call is the original check. The original comment says that
`x_CO2 = 100` means the state is superheated vapour, not under the saturation
dome, and that under the dome `T` and `p` are not independent for the
azeotropic fluids of the course.

| Input | Value |
|---|---|
| `Vol` | 0.2 m³ (200 L, `200e-3`) |
| `T` | 35 °C, stored as `35 [K]+273.15 [K]` (308.15 K) |
| `p` | 2×10³ kPa (2×10⁶ Pa) |
| `R` | 8.3144621 J/(mol·K) |

Those four assignments are already equations. The system is square without
any further assignment (13 equations, 13 variables). No diagram-state array
is added: the window computes one tank state.

Property calls pass `T - 273.15` because CoolSolve reads the temperature
argument as °C. No `temperature()` result is stored, so nothing adds 273.15
back. `T` stays in kelvin.

## How to run

```bash
coolsolve ./co2_tank_ideal_gas.eescode
```

Every block is explicit. CoolSolve reports 0 iterations with the shipped
`.initials` and 0 iterations without them. There is no `abs()`, so the
guesses do not select a root. The `.initials` file is the EES stored
solution with `p` in Pa. The other stored values, including `T` in kelvin,
are unchanged.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `m` [kg] | 7.591476 | 7.591625 | 1.96e-05 |
| `m_gp` [kg] | 7.591476 | 6.871023 | 9.49e-02 |
| `erreur` [%] | 0 | −9.492064 | 1.00e+00 |
| `v` [m³/kg] | 0.02634534 | 0.02634482 | 1.96e-05 |
| `v_gp` [m³/kg] | 0.02634534 | 0.02910775 | 9.49e-02 |
| `v_gp2` [m³/kg] | 0.02910831 | 0.02910817 | 4.54e-06 |
| `T` | 308.15 K | 308.15 K | 8.86e-01 against 35 °C |
| `x_CO2` | 0 | 100 | 1.00e+00 |

The real-gas mass is 7.591476 kg in CoolSolve and 7.591625 kg in the stored
solution. The mass from `volume(CO2)` is 7.591476 kg in CoolSolve and
6.871023 kg in the stored solution. The gas-constant specific volume
`v_gp2` is 0.02910831 m³/kg in CoolSolve and 0.02910817 m³/kg in the stored
solution.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `R1_E2_2022.EES` (EES X10.836, 13 variables),
compared with `compare_solution.py --ees-units`. The tool's summary line is:

`13 common variables, 5 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

`--ees-units` scaled `p` (kPa ×1000) and rewrote `T` from K to °C. `R` is
already in J, so it is not scaled. `r_CO2` is stored as J/(g·K); that
spelling is not kJ, so the tool leaves 0.1889221109 unscaled, and the model
keeps that number.

Every difference above rtol 0.001:

- `erreur` prints 1.00e+00 (unrounded 1). CoolSolve gives 0. EES stores
  −9.492063815 %. The two masses that enter the percentage are equal in
  CoolSolve and differ in EES.
- `x_CO2` prints 1.00e+00 (unrounded 1). CoolSolve gives 0. EES stores 100.
  The original comment uses 100 to mean the state is not two-phase.
  `quality()` in CoolSolve is clamped to [0, 1]. At 35 °C and 2 MPa the
  fluid is a gas: the critical temperature of CO2 is 30.98 °C.
- `T` prints 8.86e-01. The equation window stores 308.15 K and the model
  keeps 308.15 K. The tool subtracts 273.15 and compares 308.15 with 35.
  In kelvin the two values are the same 308.15 K.
- `v_gp` and `m_gp` print 9.49e-02. EES `CO2` is an ideal gas
  (`v_gp` = 0.02910774677 m³/kg, `m_gp` = 6.871023084 kg). CoolSolve
  `volume(CO2, T=T-273.15, P=p)` returns 0.02634533708 m³/kg, the same
  value as `volume(CarbonDioxide)` at this state, so `m_gp` equals `m`
  (7.591476222164 kg). The call is the original ideal-gas check; the fluid
  name stays `CO2`.

`m` and `v` print 1.96e-05, inside rtol 0.001. `v_gp2` prints 4.54e-06:
the gas-constant volume matches the stored ideal-gas specific volume.
`MCO2` is 44.0098 kg/kmol against the stored 44.01, and `r_CO2` follows;
both print 4.54e-06. `Vol`, `p` and `R` match.

The largest relative difference over all 13 common variables, as printed by
the tool, is 1.00e+00, on `erreur` and on `x_CO2`.

CoolSolve warns that fluid `CO2` "Did you mean 'CO2'?". The source fluid of
that call is `CO2`, so the call stays `CO2`. A further warning says that
`t=35` looks like Fahrenheit and shows T=1.67. 35 °C is the argument
`T - 273.15` (308.15 K). The real-gas mass agrees with the stored mass at
35 °C.

All 13 equations are satisfied (max residual 0).

## Source and attribution

The equation window names no person. The EES licence tag is the student and
staff licence of the Laboratoire de Thermodynamique, University of Liège. The
file itself names nobody. The inventory attributes the course to S. Quoilin,
so the authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R1/R1_E2_2022.EES`.

Candidate TM-0379, the representative of duplicate group DG-0089. Teaching
exercise. Course: *Thermodynamique appliquée* (ULiège, MECA0002), repetition 1,
2022-2023. EES X10.836. The inventory title calls the problem exercise 3.9.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R1_E2_2022.EES` (EES X10.836, plain text, decimal commas already rewritten as dots, European argument separators, 13 variables, no tables). With `$UnitSystem` removed, the extraction is square: 13 equations, 13 variables, largest block 1. No diagram input and no stored unknown was turned into an equation. `$UnitSystem` was deleted. No `$TABSTOPS` and no `$Export`. Comments translated to English.
- **Units**: `$UnitSystem SI MASS DEG KPA K J`. Pressure: `p` 2e3 kPa → `2e6` Pa. Temperature stays in kelvin: `T = 35 [K]+273.15 [K]`, as the equation window stores it. Property calls pass `T - 273.15` because CoolSolve reads the temperature argument as °C. `R = 8.3144621` J/(mol·K) is already in J, so it is not multiplied by 1000. `MolarMass` returns kg/kmol, and `r_CO2 = R/MCO2` stays in J/(g·K) (stored 0.1889221109). `v_gp2 = r_CO2*T/(p/1000)` uses that constant with `p` in Pa, so the specific volume stays in m³/kg. `.initials`: `p` ×1000; temperatures and the other stored values left as stored.
- **Fluids**: `volume(CARBONDIOXIDE, ...)`, `Quality(CarbonDioxide, ...)` and `MolarMass(CarbonDioxide)` are written `CarbonDioxide`. `volume(CO2, ...)` stays `CO2`. `MolarMass(C)` is not used.
- **Level**: equations 13 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one closed tank, not discretised → 0; no calibration, off-design or dynamics → 0; explicit, 0 iterations with or without guesses → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

The equation window compares the real-gas mass with the mass from `volume(CO2)`
and with the gas-constant specific volume. CoolSolve's `volume(CO2)` at
35 °C and 2 MPa returns the real-gas specific volume, so the percentage error
is 0. The gas-constant volume `v_gp2` still matches the stored ideal-gas
specific volume. EES stores `x_CO2 = 100` for this gas state; CoolSolve
returns 0.

`compare_solution.py --ees-units` rewrites a stored kelvin temperature whose
name starts with `T` into °C, so `T` prints a large relative difference while
308.15 K agrees with the stored 308.15 K.

No CoolSolve gap. `missing_features` is empty.

## Related models

`related` is empty. No other tank model is linked.
