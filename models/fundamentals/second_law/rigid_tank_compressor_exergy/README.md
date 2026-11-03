# Exercise: reversible work to fill a rigid air tank

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0197`

A rigid 200 m³ tank of air starts at 100 kPa and 300 K and is filled by a compressor to 1 MPa at the same temperature. The model takes the tank and the compressor as one system and finds the reversible work from an exergy balance. Teaching exercise of the ULiège course *Thermodynamique appliquée* (MECA0002), repetition R10, exercise 5 (2022-2023).

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Air_ha |
| **Size** | 23 equations (largest block: 1) |
| **Source** | thermo_models, file `R10_E05_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@f5b79cd — verified against the EES stored solution (see *Verification*) |

## Problem statement

A rigid tank of 200 m³ initially contains atmospheric air at 100 kPa and 300 K. It is used as a storage tank by compressing air up to 1 MPa and 300 K. The air charged into the tank is compressed by a compressor from the ambient conditions (100 kPa and 300 K). Determine the minimum work of this process. The system considered is the tank and the compressor together.

The equation window stores the same numbers: `Vol = 200` m³, `T_0 = 300` K, `p_0 = 100` kPa, `p_1 = 1000` kPa, and `T_1 = T_0`. The statement and the equations agree. The unit column is kelvin, and 300 K is kept as kelvin.

A comment in the equation window says the reversible case is a maximum work and sets the destroyed exergy to zero. The statement asks for the minimum work. The equations are the reversible balance, and that is what is solved.

## Model

One control volume: the tank and the compressor. The final pressure and the final temperature are data. The compressor is not a separate machine. There is no second tank and no turbine.

Initial and final masses from the specific volume of `Air_ha`:

\[
m_0 = V / v_0, \qquad m_1 = V / v_1
\]

Specific exergy of the air in the tank, with the dead state equal to the ambient state (`p_0`, `T_0`):

\[
\phi = (h - h_\mathrm{amb}) - T_\mathrm{amb}(s - s_\mathrm{amb})
\]

`T_amb` stays at 300 K, so the product \(T_\mathrm{amb}(s - s_\mathrm{amb})\) is in J/kg when entropy is in J/kg-K. Property calls receive Celsius: `T_0 - 273.15` and `T_1 - 273.15`.

Exergy balance of the combined system. The original comment sets the destroyed exergy to zero. It also writes `X_in = W_rev_in + m_in*psi_in` and notes that `psi_in` is zero because the air enters at the dead state. `psi_in` and `m_in` are comments, not equations.

\[
X_\mathrm{in} - X_\mathrm{out} = X_1 - X_0, \qquad X_\mathrm{in} = W_\mathrm{rev,in}, \qquad X_\mathrm{out} = 0
\]
\[
X_1 = m_1 \phi_1, \qquad X_0 = m_0 \phi_0
\]

`phi_0` is zero because the initial state is the dead state, which the original states.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `Vol` | 200 m³ | `W_rev_in` | 461.293 MJ |
| `T_0`, `T_1`, `T_amb` | 300 K | `m_0` | 232.320 kg |
| `p_0` | 100 kPa | `m_1` | 2329.093 kg |
| `p_1` | 1 MPa | `phi_1` | 198.057 kJ/kg |

## How to run

Open `rigid_tank_compressor_exergy.eescode` in the CoolSolve GUI and press *Solve*, or from the model folder:

```bash
coolsolve ./rigid_tank_compressor_exergy.eescode
```

Every block has size 1. There is no `abs()` and no second root. `rigid_tank_compressor_exergy.initials` is the EES stored solution with pressures in Pa, energies in J and temperatures left at 300 K. The guesses of `h` and `s` still carry the EES Air reference; the property equations replace them. The run takes 4 iterations with those guesses and 48 without, and both reach the solution below.

## Results

Physical results, compared with the EES stored solution. Temperatures below are kelvin, as stored. Pressures are shown in kPa; the model stores Pa. Work is shown in kJ; the model stores J.

| Quantity | EES | CoolSolve |
|---|---:|---:|
| `T_0`, `T_1`, `T_amb` | 300 K | 300 K |
| `p_1` | 1000 kPa | 1000 kPa |
| `m_0` | 232.3210677 kg | 232.3199254 kg |
| `m_1` | 2329.104497 kg | 2329.093020 kg |
| `W_rev_in` | 461293.4257 kJ | 461293.4226 kJ |
| `phi_1` | 198.0561312 kJ/kg | 198.0571057 kJ/kg |

`W_rev_in` differs from the stored value by −3.07 J (relative difference 6.66×10⁻⁹). `p_1` agrees exactly after the kPa to Pa conversion. `m_1` differs by 4.93×10⁻⁶, with `m_0` at 4.92×10⁻⁶, following the specific volume of `Air_ha`.

Reference offset of `Air_ha`, kept separate from the work, the final pressure and the mass. Enthalpy is 126061.5 J/kg above EES at 300 K and 100 kPa (426300.8 J/kg against 300239.3 J/kg), and the same offset to 0.001 J/kg at 1 MPa. Entropy is 2978.187 J/kg-K below EES at 100 kPa (3890.501 against 6868.688) and 2978.190 J/kg-K below EES at 1 MPa. The offset cancels in `phi_0`. On `phi_1` it leaves +0.975 J/kg (relative difference 4.92×10⁻⁶), because the entropy offset changes by 0.00325 J/kg-K between the two pressures. That residual and the mass difference nearly cancel in `W_rev_in`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `R10_E05_2022.EES` (EES X10.836, 25 variables, 25 of them solved). Compared with `compare_solution.py --ees-units`. The tool's summary line is:

`23 common variables, 13 differ (rtol=0.001); only in EES: 2; only in CoolSolve: 0`

`--ees-units` scaled `p_0` and `p_1` (kPa ×1000) and `X_0` (`kJ` ×1000), and rewrote `T_0`, `T_1` and `T_amb` from K to °C. It also scaled `p`, which is only in the EES list. It did not scale `h_0`, `h_1`, `h_amb`, `s_0`, `s_1`, `s_amb`, `phi_0` or `phi_1`: EES stored those units as lowercase `kj`, and the tool matches the token `kJ`. It did not scale `W_rev_in`, `X_1`, `X_in` or `X_out`: EES stored those units as uppercase `KJ`.

Every difference above rtol 0.001:

- `h_0`, `h_1` and `h_amb` print 9.99e-01 because the reference stayed in kJ while CoolSolve stores J. After ×1000 the values are the Air_ha offset above, +126061.5 J/kg. The printed 9.99e-01 is the largest relative difference over all 23 common variables.
- `s_0`, `s_1` and `s_amb` print 9.98e-01 for the same unscaled `kj` string. After ×1000 the entropy offset is −2978.187 J/kg-K at 100 kPa and −2978.190 J/kg-K at 1 MPa.
- `phi_1` prints 9.99e-01 for the same reason. After ×1000 the difference is +0.975 J/kg (relative difference 4.92×10⁻⁶), the pressure dependence of that offset.
- `W_rev_in`, `X_1` and `X_in` print 9.99e-01 because uppercase `KJ` is not scaled. The model values are already in J. After ×1000 the difference is −3.07 J (relative difference 6.66×10⁻⁹). This is not a model error.
- `T_0`, `T_1` and `T_amb` print 9.10e-01. The equation window stores 300 K and the model keeps 300 K. The tool subtracts 273.15 before comparing.

Inside the tolerance: `m_0` 4.92×10⁻⁶, `m_1` 4.93×10⁻⁶, `v_0` 4.92×10⁻⁶, `v_1` 4.93×10⁻⁶, and `p_0`, `p_1`, `Vol`, `phi_0`, `X_0` and `X_out` at 0. `phi_0`, `X_0` and `X_out` are zero on both sides, so the unscaled unit strings do not show up.

Only in the EES reference: `m` and `p`. `p` is 138 kPa and `m` equals the stored `m_0`. Neither name is in the equation window. The diagram-window RTF is empty, and the unmodified extract is square, so neither was added.

`verification.max_rel_diff` is 9.99e-01, the maximum the tool prints.

## Source and attribution

The equation window names no person. The EES licence tag is the student and staff licence of the Laboratoire de Thermodynamique, University of Liège, not an author. The inventory attributes the course to S. Quoilin, so the authors field is S. Quoilin. The file itself names nobody.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R10/R10_E05_2022.EES`.

Candidate TM-0392. Teaching exercise, not an exam. Course: *Thermodynamique appliquée* (ULiège, MECA0002), repetition session 10, exercise 5 (2022-2023). EES X10.836.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R10_E05_2022.EES` (EES X10.836, plain text, European argument separators, 25 stored variables, no lookup or parametric tables). The diagram-window RTF is empty. With `$UnitSystem` removed, the extraction is square: 23 equations, 23 variables, largest block 1. No diagram input and no stored unknown was turned into an equation. `m` and `p` stay out. `$UnitSystem` was deleted. No `$TABSTOPS`, `$Export`, `concat$` or `EESFILEDIR$`. The equation-window numbers are integers; the extractor rewrote the semicolon argument lists as commas.
- **Units**: `$UnitSystem SI MASS DEG KPA K KJ` converted by hand to SI, Pa and J. Temperatures stay in kelvin: `T_0 = 300` K, `T_1 = T_0`, `T_amb = T_0`, as the equation window stores them. Property calls pass `T - 273.15` because CoolSolve reads the temperature argument as °C. `p_0`: 100 kPa → `100E3` Pa. `p_1`: 1000 kPa → `1000E3` Pa. `Vol` is unchanged. Property results are left in J/kg and J/kg-K with no extra factor. The exergy products keep `T_amb` in kelvin, so the balance is unchanged in form (kJ with K becomes J with K). `.initials` converted the same way (pressures ×1000, specific energies and `phi` ×1000, `W_rev_in`, `X_1` and `X_in` ×1000, temperatures left at 300 K, zeros left at 0).
- **Statement**: the pasted statement and the equations agree on 200 m³, 100 kPa, 300 K and 1 MPa. The comment says "maximum work" for the reversible case; the statement says minimum work. The solved equation is the reversible balance.
- **Level**: equations 23 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one control volume, not discretised → 0; no calibration, off-design, part-load or dynamics → 0; converges from default guesses (48 iterations) and from the converted stored solution (4), no *Try Harder* and no `coolsolve.conf` → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

The final pressure and the final temperature are data, not results. The compressor has no separate efficiency or displacement: the work is the reversible work of the combined system. Absolute `Air_ha` enthalpy and entropy are not comparable with EES without the reference offset above; the work, the final pressure and the masses are.

No CoolSolve gap. `missing_features` is empty. `quality()` is not called.

## Related models

`CSL-0193` (mixing chamber of water and steam, exergy destruction) is exercise 4 of the same repetition session. It is a mixing chamber, not this tank. It is listed in `related`. Its own `model.json` is left unchanged.

`CSL-0172` (rigid tank, two compartments, water) and `CSL-0176` (piston-cylinder, water, constant pressure) are other tank exercises. The fluid and the balances are different, so they are not listed in `related`.
