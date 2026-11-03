# Centrifugal air compressor of a gas turbine, power including kinetic energy (exercise 5.14)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0213`

Power required to drive the centrifugal air compressor of a gas turbine, from
the steady-flow energy balance, and the share of that power that goes into
the enthalpy rise. The compressor is adiabatic. The change in potential
energy and the inlet kinetic energy are neglected; the outlet kinetic energy
is kept. Teaching exercise 5.14 of the ULiège course *Thermodynamique
appliquée* (MECA0002), repetition 3 (2022-2023).

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air |
| **Size** | 10 equations (largest block: 1) |
| **Source** | thermo_models, file `R3_E5_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@62d92f0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

The centrifugal air compressor of a gas turbine receives air from the ambient
atmosphere, where the pressure is 1 bar and the temperature is 300 K. At the
compressor outlet the pressure is 4 bar, the temperature is 480 K and the
velocity is 100 m/s. The mass flow rate at the compressor inlet is 15 kg/s.
Calculate the power required to drive the compressor.

The equation window states the pressures as 100 kPa and 400 kPa (1 bar and
4 bar as written in the exercise) and the temperatures as 300 K and 480 K.
Variable comments in the file name the exercise “Exemple 5.14”.

## Model

Ideal-gas enthalpy of Air depends only on temperature, so the given pressures
do not enter the balance. They stay as data, as in the original. The original
applies the steady-flow energy balance to an adiabatic open system:

\[
\dot W = \dot m \left(h_\mathrm{out} - h_\mathrm{in} + \frac{c_\mathrm{out}^2}{2}\right)
\]

with \(\dot Q = 0\), \(\dot m_\mathrm{out} = \dot m_\mathrm{in}\),
\(g(z_\mathrm{out} - z_\mathrm{in}) = 0\) and \(c_\mathrm{in}^2/2 = 0\). The
inlet kinetic energy is neglected because the control volume is taken large
enough that the air speed across the inlet surface is very small, as in the
original. Work received by the system is positive, as in the original.

The share of the power that goes into the enthalpy rise is

\[
\mathrm{rapW} = 100\,\frac{\dot m\,(h_\mathrm{out}-h_\mathrm{in})}{\dot W}
\]

The original writes the factor as `100[%]`. The comment in the file says that
about 97.4% of the power goes into the enthalpy transfer and about 2.6% into
kinetic energy.

| Input | Value |
|---|---|
| `p_in` | 100 kPa (1×10⁵ Pa), 1 bar in the statement |
| `T_in` | 300 K, as stored |
| `p_out` | 400 kPa (4×10⁵ Pa), 4 bar in the statement |
| `T_out` | 480 K, as stored |
| `c_out` | 100 m/s |
| `q_m` | 15 kg/s |

Ten equations, ten variables, system square. The stored values of `h_in`,
`h_out`, `W_dot` and `rapW` are guesses in `.initials`, not equations. The
diagram-window RTF is empty. The pressure ratio is `p_out/p_in` = 4; it is
not a variable of the equation window.

Property calls pass `T - 273.15` because CoolSolve reads the temperature
argument as °C. `T_in` and `T_out` stay in kelvin.

## How to run

```bash
coolsolve ./centrifugal_air_compressor_ke.eescode
```

Every block is explicit. CoolSolve reports 0 iterations with the shipped
`.initials` and 0 iterations without them. There is no `abs()`, so the guesses
do not select a root. The enthalpy guesses are the EES values in J; they
differ from the CoolSolve solution by the Air reference offset and are unused.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `p_in` [Pa] | 100000 | 100000 (100 kPa) | 0 |
| `p_out` [Pa] | 400000 | 400000 (400 kPa) | 0 |
| `T_in` | 300 K | 300 K | 9.10e-01 against 26.85 °C |
| `T_out` | 480 K | 480 K | 5.69e-01 against 206.85 °C |
| `c_out` [m/s] | 100 | 100 | 0 |
| `q_m` [kg/s] | 15 | 15 | 0 |
| `h_in` [J/kg] | 426297.77 | 300444.832 | 2.95e-01 |
| `h_out` [J/kg] | 608835.00 | 482814.2392 | 2.07e-01 |
| `W_dot` [W] | 2813058.42 | 2810541.109 | 8.95e-04 |
| `rapW` [%] | 97.33386 | 97.33147 | 2.45e-05 |

The pressure ratio is 4 on both sides (400 kPa / 100 kPa). The outlet velocity
is 100 m/s on both sides. The inlet velocity is neglected and is not a
variable. The outlet kinetic energy is \(c_\mathrm{out}^2/2 = 5000\) J/kg.
The power is 15 kg/s times (enthalpy rise + 5000 J/kg).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `R3_E5_2022.EES` (EES X10.836, 10 variables),
compared with `compare_solution.py --ees-units`. The tool's summary line is:

`10 common variables, 4 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

`--ees-units` scaled `p_in` and `p_out` (kPa ×1000) and rewrote `T_in` and
`T_out` from K to °C. It left `W_dot` (W), `h_in` and `h_out` (J/kg), `rapW`
(%), `c_out` (m/s) and `q_m` (kg/s) unscaled. No stored unit string is blank.

Every difference above rtol 0.001:

- `T_in` prints 9.10e-01 and `T_out` prints 5.69e-01. The equation window
  stores 300 K and 480 K, and the model keeps 300 K and 480 K. The tool
  subtracts 273.15 and then compares 300 with 26.85 and 480 with 206.85.
  That relative difference is the comparator, on temperatures that agree in
  kelvin.
- `h_in` prints 2.95e-01 and `h_out` prints 2.07e-01. Ideal-gas Air keeps
  CoolProp's reference state; EES references Air enthalpy to 0 at 0 K
  (\(h = \int_0^T c_p\,\mathrm{d}T\)). CoolSolve − EES is +125852.9 J/kg on
  `h_in` (300 K) and +126020.8 J/kg on `h_out` (480 K), about +126 kJ/kg.
  This offset is separate from the power.

The offset is not the same at the two temperatures: it changes by 167.8 J/kg.
That residual is a difference of \(c_p(T)\) between EES and CoolProp. It
raises the power from 2810541.109 W to 2813058.42 W (relative difference
8.95e-04), inside rtol 0.001. `rapW` differs by 2.45e-05. The largest
relative difference over all ten common variables, as printed by the tool, is
9.10e-01 on `T_in`.

CoolSolve warns that fluid `Air` is dry air and that `t=206.85` is read as
°C. The source fluid is `air`, so the call stays `Air`. 206.85 °C is the
argument `T_out - 273.15` (480 K). `T_out` itself stays 480 K.

## Source and attribution

The equation window names no person. The EES licence tag is the student and
staff licence of the Laboratoire de Thermodynamique, University of Liège. The
file itself names nobody. The inventory attributes the course to S. Quoilin,
so the authors field is S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R3/R3_E5_2022.EES`.

Candidate TM-0415. Teaching exercise, not an exam. Course: *Thermodynamique
appliquée* (ULiège, MECA0002), repetition 3, exercise 5 (2022-2023), textbook
example 5.14. EES X10.836.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R3_E5_2022.EES` (EES X10.836, plain text, European argument separators, 10 variables, no tables). The diagram-window RTF is empty. With `$UnitSystem` removed, the extraction is square: 10 equations, 10 variables, largest block 1. No diagram input and no stored unknown was turned into an equation. `$UnitSystem` was deleted. No `$TABSTOPS`, `$Export`, `concat$` or `EESFILEDIR$`. The equation-window numbers are integers; the extractor rewrote the semicolon argument lists as commas. Comments translated to English. The comment “2,6%” is written 2.6% in that English text.
- **Units**: `$UnitSystem SI MASS DEG KPA K J`. Pressures: `p_in` 100 kPa → `100e3` Pa, `p_out` 400 kPa → `400e3` Pa. Temperatures stay in kelvin: `T_in = 300` K, `T_out = 480` K, as the equation window stores them. Property calls pass `T - 273.15` because CoolSolve reads the temperature argument as °C. Energies are already in J: `W_dot` is in W and `h_in`, `h_out` are in J/kg, so the balance `W_dot = q_m*(h_out - h_in + c_out^2/2)` is unchanged (the kinetic term is already in J/kg). `c_out` and `q_m` are unchanged. `rapW = 100[%]*...` is unchanged. `.initials`: `p_in` 100 → 100000, `p_out` 400 → 400000; temperatures, enthalpies, `W_dot`, `rapW`, `c_out` and `q_m` left at the stored values. The enthalpy guesses are the EES numbers in J.
- **Case**: the original calls `enthalpy(air;T=t_out)` and `enthalpy(air;T=t_in)`. EES stores `T_in` and `T_out`. The calls are written `enthalpy(Air, T=T_out-273.15)` and `enthalpy(Air, T=T_in-273.15)`.
- **Fluid**: `air` written `Air` (the same ideal gas). CoolSolve warns that moist air would be `AirH2O`. The source is dry air, so the fluid stays `Air`. A variable-info string in the file suggests `T_in = 300-273.15`. The equation window stores `T_in = 300[K]`, so the value stays 300 K.
- **Level**: equations 10 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one component, not discretised → 0; no calibration, off-design or dynamics → 0; explicit, 0 iterations with or without guesses → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

The balance neglects heat transfer, potential energy and inlet kinetic energy,
as the exercise states. Pressures are data only: ideal-gas enthalpy does not
use them. Absolute Air enthalpies are not comparable with EES without the
reference offset above; the power and `rapW` are the results of the exercise.
`compare_solution.py --ees-units` rewrites a stored kelvin temperature whose
name starts with `T` into °C, so `T_in` and `T_out` print a large relative
difference while the stored kelvin values agree.

No CoolSolve gap. `missing_features` is empty.

## Related models

`CSL-0181` (centrifugal air compressor power, example 5.14, candidate TM-0364)
uses the same statement and the same inlet and outlet data. Its equation
window differs: temperatures are `300 - 273.15` and `480 - 273.15` in a °C
unit system, the power equation divides the kinetic energy by 1000 because
that file stores enthalpies in kJ/kg, and it has no `rapW`. Because the
equation windows differ, `CSL-0181` is not listed in `related`.

TM-0408 is the other file of duplicate group DG-0099. It is not imported here.
