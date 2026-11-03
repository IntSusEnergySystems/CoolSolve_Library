# Centrifugal air compressor power (example 5.14)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0181`

Power required to drive the centrifugal air compressor of a gas turbine, from
the steady-flow energy balance. The compressor is adiabatic. The change in
potential energy and the inlet kinetic energy are neglected; the outlet
kinetic energy is kept. Teaching example 5.14 of the ULiège course
*Thermodynamique appliquée*, THD10 repetition 2 (2017-2018).

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air |
| **Size** | 9 equations (largest block: 1) |
| **Source** | thermo_models, file `R2_E6_borguet.EES` |
| **Authors** | TBD (ULiège THD) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution (see *Verification*) |

## Problem statement

The centrifugal air compressor of a gas turbine receives air from the ambient
atmosphere, where the pressure is 1 bar and the temperature is 300 K. At the
compressor outlet the pressure is 4 bar, the temperature is 480 K and the
velocity is 100 m/s. The mass flow rate at the compressor inlet is 15 kg/s.
Calculate the power required to drive the compressor.

The equation window states the pressures as 100 kPa and 400 kPa (1 bar and
4 bar as written in the example, not 101.325 kPa).

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
enough that the air speed across the inlet surface is very small (compressor
on a test bench), as in the original.

| Input | Value |
|---|---|
| `p_in` | 100 kPa (1×10⁵ Pa), 1 bar in the statement |
| `T_in` | 26.85 °C (300 K in the statement) |
| `p_out` | 400 kPa (4×10⁵ Pa), 4 bar in the statement |
| `T_out` | 206.85 °C (480 K in the statement) |
| `c_out` | 100 m/s |
| `q_m` | 15 kg/s |

Nine equations, nine variables, system square. The stored values of `h_in`,
`h_out` and `W_dot` are guesses in `.initials`, not equations. The diagram
window contains no inputs.

## How to run

```bash
coolsolve ./centrifugal_air_compressor_power.eescode
```

Every block is explicit. CoolSolve reports 0 iterations with the shipped
`.initials` and 0 iterations without them. The guesses are not used.

## Results

| Quantity | CoolSolve | EES stored (SI) | rel. diff. |
|---|---:|---:|---:|
| `p_in` [Pa] | 100000 | 100000 | 0 |
| `p_out` [Pa] | 400000 | 400000 | 0 |
| `T_in` [°C] | 26.85 | 26.85 | 0 |
| `T_out` [°C] | 206.85 | 206.85 | 0 |
| `c_out` [m/s] | 100 | 100 | 0 |
| `q_m` [kg/s] | 15 | 15 | 0 |
| `h_in` [J/kg] | 426297.77 | 300430 | 2.95e-01 |
| `h_out` [J/kg] | 608835.00 | 482787.51 | 2.07e-01 |
| `W_dot` [W] | 2813058.42 | 2810362.64 | 9.58e-04 |

The outlet kinetic energy is \(c_\mathrm{out}^2/2 = 5000\) J/kg. The power is
15 kg/s times (enthalpy rise + 5000 J/kg).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `R2_E6_borguet.EES` (EES X8.423, 9 variables),
compared with `compare_solution.py --ees-units`. The tool's summary line is:

`9 common variables, 2 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

`--ees-units` was used. It scaled `p_in` and `p_out` (kPa ×1000), `W_dot`
(kW ×1000), `h_in` and `h_out` (kJ ×1000). Temperatures were already in °C
and `c_out` in m/s.

The two variables above rtol 0.001 are the absolute enthalpies. Ideal-gas Air
keeps CoolProp's reference state; EES references Air enthalpy to 0 at 0 K
(\(h = \int_0^T c_p\,\mathrm{d}T\)). CoolSolve − EES is +125867.8 J/kg on
`h_in` (26.85 °C) and +126047.5 J/kg on `h_out` (206.85 °C), about +126 kJ/kg,
the offset quoted for Air in CoolSolve `docs/ees_import.md` §11 (there given
as EES − CoolSolve = −126 kJ/kg). The offset is not the same at the two
temperatures: it changes by 179.7 J/kg. That residual is a difference of
\(c_p(T)\) between EES and CoolProp. It raises the enthalpy rise, and therefore
the power, from 2810362.64 W to 2813058.42 W (relative difference 9.58e-04),
which is inside rtol 0.001. The largest relative difference over all nine
common variables, as printed by the tool, is 2.95e-01 on `h_in`.

## Source and attribution

The equation window names no person. The EES licence tag is the student and
staff licence of the Laboratoire de Thermodynamique, University of Liège, not
an author. The inventory attributes the 2017-2018 THD course to S. Bertagnolio
and S. Borguet. The file name contains "borguet"; the file text does not, so
that name is not used as authorship. Authors: TBD (ULiège THD).

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R02/R2_E6_borguet.EES`.

Candidate TM-0364. Teaching example, not an exam.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R2_E6_borguet.EES` (EES X8.423, plain text, 9 variables, no tables). Unit system `$UnitSystem SI MASS DEG KPA C KJ`, deleted after the conversion below. The extractor replaced the decimal comma in `273,15` by a dot. The diagram-window RTF is empty. The system is square (9 equations, 9 variables), so no stored value was turned into an equation. Comments translated to English.
- **Units, value by value**:
  - `p_in`: 100 kPa → `100e3` Pa
  - `p_out`: 400 kPa → `400e3` Pa
  - `T_in`: `300 - 273.15` left in °C (300 K in the statement) → 26.85 °C
  - `T_out`: `480 - 273.15` left in °C (480 K in the statement) → 206.85 °C
  - `c_out`: 100 m/s, unchanged
  - `q_m`: 15 kg/s, unchanged
  - `W_dot = q_m*(h_out - h_in + c_out^2/2/1000)` with enthalpies in kJ/kg and power in kW → `W_dot = q_m*(h_out - h_in + c_out^2/2)` with enthalpies in J/kg and power in W. The factor `/1000` converted J/kg of kinetic energy into kJ/kg; it is removed.
  - `h_in`, `h_out`: `enthalpy` now returns J/kg. No extra factor.
  - `.initials`: `p_in` 100 → 100000, `p_out` 400 → 400000, `h_in` 300.43 → 300430, `h_out` 482.7875092 → 482787.5092, `W_dot` 2810.362637 → 2810362.637. `T_in`, `T_out`, `c_out` and `q_m` unchanged. The enthalpy guesses are the EES numbers in J; they differ from the CoolSolve solution by the Air reference offset and are unused.
- **Case**: the original calls `enthalpy(air, T=t_in)` and `enthalpy(air, T=t_out)`. EES stores only `T_in` and `T_out` (case-insensitive). The calls are written `enthalpy(Air, T=T_in)` and `enthalpy(Air, T=T_out)`.
- **Fluid**: `air` written `Air` (the same ideal gas). CoolSolve warns that moist air would be `AirH2O`. The source is dry air, so the fluid stays `Air`.
- **Level**: equations 9 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one component, not discretised → 0; no calibration, off-design or dynamics → 0; explicit, 0 iterations with or without guesses → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

The balance neglects heat transfer, potential energy and inlet kinetic energy,
as the example states. Pressures are data only: ideal-gas enthalpy does not
use them. Absolute Air enthalpies are not comparable with EES without the
reference offset above; the power is the result of the example.

No CoolSolve gap. `missing_features` is empty.

## Related models

`CSL-0023` (centrifugal turbocompressor performance) and `CSL-0069` (centrifugal
compressor design and similarity) were compared. Their equations are velocity
triangles and similarity factors, not this energy balance, so they are not
listed in `related`. No back-link is required. Later copies of example 5.14
(inventory TM-0415 and TM-0408) are not library models.
