# Exercise: mixing chamber of water and steam, exergy destruction

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0193`

Liquid water and steam mix in a chamber at 138 kPa. The outlet temperature and the heat loss to the surroundings are given. The model finds the steam mass flow from the steady mass and energy balances, then the reversible power an ideal engine would deliver in bringing the inlet streams to the outlet state, and the exergy destruction of mixing them directly. Teaching exercise of the ULiège course *Thermodynamique appliquée* (MECA0002), repetition R10, exercise 4 (2022-2023).

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Water, Steam (same real fluid as Water), Air_ha (dead state) |
| **Size** | 27 equations (largest block: 2) |
| **Source** | thermo_models, file `R10_E04_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@91d2b56 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Water at 138 kPa and 10 °C enters a mixing chamber at 2.27 kg/s, where it is mixed with steam entering at 138 kPa and 115 °C. The mixture leaves the chamber at 138 kPa and 55 °C. Heat losses from the chamber to the surroundings at 21 °C are 3.16 kW. Neglecting changes in potential and kinetic energy, determine the reversible power that an ideal heat engine would have delivered had it brought the incoming streams to the outlet conditions. Also determine the exergy destruction rate of this process.

The statement gives those temperatures in °C. The equation window, whose unit system is kelvin, stores the same values as `T = 10[K]+273.15[K]` (and the same form for 115 °C, 55 °C and 21 °C). The two agree. CoolSolve keeps the Celsius numbers.

## Model

One steady mixing chamber, three streams at the same pressure. Stream 1 is liquid water, stream 2 is steam, stream 3 is the outlet. The dead state used for the flow exergy is not water: the original calls `enthalpy(Air_ha)` and `entropy(Air_ha)` at the ambient temperature and 100 kPa ("1 bar, about atmospheric pressure").

Mass and energy, kinetic and potential energy neglected:

\[
\dot m_1 + \dot m_2 = \dot m_3
\]
\[
\dot m_1 h_1 + \dot m_2 h_2 = \dot m_3 h_3 + \dot Q_\mathrm{loss}
\]

Specific flow exergy and the rate exergy balance, with the heat loss carrying no exergy because it occurs at the ambient temperature:

\[
\psi = (h - h_0) - T_0(s - s_0)
\]
\[
\dot m_1 \psi_1 + \dot m_2 \psi_2 = \dot m_3 \psi_3 + \dot W_\mathrm{rev,out}
\]

The original then sets the reversible power equal to the exergy destruction of the real mixing, and writes that destruction as \(T_0 \dot S_\mathrm{gen}\). The original comment calls `S_dot_gen` the exergy destruction rate; the equation is \(\dot X_\mathrm{destroyed} = T_0 \dot S_\mathrm{gen}\).

`h_0` and `s_0` cancel in the balance when mass is conserved. The original says the same power would follow from \(\phi = h - T_0 s\). Those `phi` lines are comments in the source and are not equations here.

`h_2bis` repeats the steam state with fluid `Steam`. The original says Steam is water vapour, so the enthalpy matches `h_2`. `h_3_bis` repeats the outlet enthalpy with `Water`, with the same remark copied onto that line.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `m_dot_1`, `T_1` | 2.27 kg/s, 10 °C | `m_dot_2` steam flow | 0.174113 kg/s |
| `T_2` steam inlet | 115 °C | `m_dot_3` outlet flow | 2.444113 kg/s |
| `T_3` outlet | 55 °C | `W_dot_rev_out` | 81.328 kW |
| `p` | 138 kPa | `X_destroyed_real` | 81.328 kW |
| `T_0`, dead-state pressure | 21 °C, 100 kPa | `S_dot_gen` | 276.484 W/K |
| `Q_dot_loss` | 3.16 kW | | |

## How to run

Open `mixing_chamber_exergy.eescode` in the CoolSolve GUI and press *Solve*, or from the model folder:

```bash
coolsolve ./mixing_chamber_exergy.eescode
```

The only algebraic loop is the pair `m_dot_2`, `m_dot_3` (block of 2). There is no `abs()` and no second root. `mixing_chamber_exergy.initials` is the EES stored solution converted to Pa, J and °C. The dead-state guesses `h_0`, `s_0` and `psi` still carry the EES Air reference; the explicit property and exergy equations replace them. The run takes 8 iterations with those guesses and 27 without, and both reach the solution below.

## Results

Physical results, compared with the EES stored solution after the unit conversion (kW → W, kPa → Pa, K → °C). Outlet temperature is an input.

| Quantity | EES | CoolSolve |
|---|---:|---:|
| `T_3` | 55 °C | 55 °C |
| `m_dot_1` | 2.27 kg/s | 2.27 kg/s |
| `m_dot_2` | 0.1741132627 kg/s | 0.1741132627 kg/s |
| `m_dot_3` | 2.444113263 kg/s | 2.444113263 kg/s |
| `Q_dot_loss` | 3.16 kW | 3.16 kW |
| `W_dot_rev_out` | 81.32790635 kW | 81.32790634 kW |
| `X_destroyed_real` | 81.32790635 kW | 81.32790634 kW |
| `S_dot_gen` | 276.4844683 W/K | 276.4844683 W/K |

`h_2bis` equals `h_2` in both tools (2.702238331 MJ/kg).

Reference offset of the dead state, kept separate from the table above. `Air_ha` enthalpy at 21 °C and 100 kPa is 126061.5 J/kg above EES (420414.2 J/kg against 294352.7 J/kg), the usual ideal-gas Air offset of about +126 kJ/kg. The entropy is 2978.187 J/kg-K below EES (3870.686 against 6848.873). Each specific flow exergy `psi` is then 1002095.18 J/kg below EES, the same shift on all three streams, equal to \(-\Delta h_0 + T_{0,\mathrm{K}}\Delta s_0\). That shift cancels in the exergy balance, which is why the power and the exergy destruction match. Water enthalpies and entropies have no such offset (largest relative difference 5.3×10⁻⁹ on `h_1` and `s_1` once the EES `kj` values are multiplied by 1000).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `R10_E04_2022.EES` (EES X10.836, 31 variables). Compared with `compare_solution.py --ees-units`. The tool's summary line is:

`26 common variables, 13 differ (rtol=0.001); only in EES: 5; only in CoolSolve: 1`

`--ees-units` scaled `p` (kPa ×1000), `Q_dot_loss`, `W_dot_rev_out`, `X_dot_heat_loss`, `X_destroyed_real` and `S_dot_gen` (kW ×1000), `T_1`, `T_2`, `T_3` and `T_0` (K → °C), and `psi_1`, `psi_2`, `psi_3` (`kJ` ×1000). It did not scale `h_0`, `h_1`, `h_2`, `h_2bis`, `h_3`, `h_3_bis`, `s_0`, `s_1`, `s_2` or `s_3`: EES stored those units as lowercase `kj`, and the tool matches the token `kJ`.

Every difference above rtol 0.001:

- `h_0`, `h_1`, `h_2`, `h_2bis`, `h_3`, `h_3_bis`, `s_1`, `s_2`, `s_3` print 9.99e-01, and `s_0` prints 9.98e-01, because the reference values stayed in kJ while CoolSolve stores J. After ×1000, the Water states agree: largest relative difference 5.34×10⁻⁹ on `h_1` and `s_1`. `h_2` and `h_2bis` are 1.86×10⁻¹⁰.
- `h_0` and `s_0`, after that ×1000, still differ by the Air_ha reference offset above (+126061.5 J/kg, −2978.187 J/kg-K). The printed 9.99e-01 on `h_0` is the largest relative difference over all 26 common variables.
- `psi_1`, `psi_2` and `psi_3` were scaled by the tool and still differ (5.83e-01, 4.40e-01, 5.81e-01). The absolute difference is 1002095.18 J/kg on each, the dead-state shift, and it cancels in the balance.

Inside the tolerance: `m_dot_2` 2.75×10⁻¹⁰, `m_dot_3` 1.03×10⁻¹⁰, `W_dot_rev_out` and `X_destroyed_real` 1.60×10⁻¹⁰, `S_dot_gen` 1.66×10⁻¹⁰, and the inputs `m_dot_1`, `p`, `Q_dot_loss`, `T_1`, `T_2`, `T_3`, `T_0`, `X_dot_heat_loss` at 0.

Only in the EES reference: `phi_1`, `phi_2`, `phi_3`, `X_dot_in`, `X_dot_out`. They appear in comments, not as equations. The stored `phi` values equal the stored `psi` values; `X_dot_in` and `X_dot_out` are the default 1. Only in CoolSolve: `T_0_K`, the absolute ambient temperature added so the exergy terms stay in kelvin after `T_0` is stored in °C.

`verification.max_rel_diff` is 9.99e-01, the maximum the tool prints.

## Source and attribution

The equation window names no person. The EES licence tag is the student and staff licence of the Laboratoire de Thermodynamique, University of Liège, not an author. The inventory attributes the course to S. Quoilin, so the authors field is S. Quoilin. The file itself names nobody.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R10/R10_E04_2022.EES`.

Candidate TM-0391. Teaching exercise, not an exam. Course: *Thermodynamique appliquée* (ULiège, MECA0002), repetition session 10, exercise 4 (2022-2023). EES X10.836.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R10_E04_2022.EES` (EES X10.836, plain text, decimal commas already rewritten as dots, 31 variables, no lookup or parametric tables). The diagram-window RTF is empty. With `$UnitSystem` removed, the extraction is square: 26 equations, 26 variables. No diagram input and no stored unknown was turned into an equation. Commented symbols `phi_1`, `phi_2`, `phi_3`, `X_dot_in` and `X_dot_out` stay out. `$UnitSystem` was deleted. No `$TABSTOPS`, `$Export`, `concat$` or `EESFILEDIR$`.
- **Units**: `$UnitSystem SI MASS DEG KPA K KJ` converted by hand to SI, °C, Pa, J. `p`: 138 kPa → `138E3` Pa. Dead-state pressure: `100[kPa]` → `100E3` Pa. `Q_dot_loss`: 3.16 kW → `3.16E3` W. `X_dot_heat_loss`: 0 kW → 0 W. Temperatures: `10[K]+273.15[K]` → `10` °C, and the same for 115 °C, 55 °C and 21 °C. The exergy products used `T_0` in kelvin; they now use `T_0_K = T_0 + 273.15`. Property calls are left as `enthalpy` and `entropy` with no extra factor. The mass and energy balances are unchanged in form (kJ/kg with kW becomes J/kg with W). `.initials` converted the same way (temperatures −273.15, pressures ×1000, specific energies and `psi` ×1000, powers ×1000).
- **Fluids**: `Water`, `Steam` and `Air_ha`, the names in the equation window. CoolSolve warns that `Steam` might mean `Water` and returns the same enthalpy; the original comment already says they match. `Air_ha` is kept for the dead state.
- **Level**: equations 27 → 0; largest block 2 → 0; no function, procedure, array or `DUPLICATE` → 0; one mixing chamber, not discretised → 0; no calibration, off-design, part-load or dynamics → 0; converges from default guesses (27 iterations) and from the converted stored solution (8), no *Try Harder* and no `coolsolve.conf` → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

The outlet temperature and the heat loss are data, not results. Kinetic and potential energy are neglected, as the exercise states. The dead state is dry air (`Air_ha`) at 21 °C and 100 kPa, so the absolute flow exergies are not water exergies relative to a water dead state. Absolute `Air_ha` enthalpy and entropy are not comparable with EES without the reference offset above; the mass flows, the heat loss and the exergy destruction are.

No CoolSolve gap. `missing_features` is empty. `quality()` is not called. `Density(AirH2O)` is not called.

## Related models

`CSL-0045` (steam turbine exergy balance) is exercise 2 of the same repetition session. Its equations are a turbine, not this mixing chamber, so it is not listed in `related`.
- `CSL-0197` (*rigid_tank_compressor_exergy*): the next exercise in the
  same session, reversible work to fill a rigid air tank.
