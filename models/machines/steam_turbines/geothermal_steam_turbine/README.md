# Geothermal hot water driving a steam turbine (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0182`

Geothermal water at 1.5 MPa and 180 °C is throttled into a flash evaporator
at 400 kPa. Saturated vapour from that vessel expands in an adiabatic
turbine to 10 kPa and a quality of 0.9. The turbine power is 1000 kW. The
model computes the steam flow and the hourly flow required from the source.
Teaching exercise, ULiège MECA0002, 2022-2023, repetition R3, exercise 8.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | Water |
| **Size** | 33 equations (largest block: 1) |
| **Source** | thermo_models, ULiège MECA0002, 2022-2023, file `R3_E8_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A geothermal source of hot water drives a steam turbine. The water arrives
at 1.5 MPa and 180 °C and is throttled into a flash evaporator, where it
forms liquid and vapour at 400 kPa. The liquid leaves at the bottom of the
vessel. The vapour is extracted and sent to the turbine. At the turbine
exit the vapour is at 10 kPa with a quality of 90 %. The turbine produces
1000 kW. The exercise asks for the hourly flow of hot water from the source.

The statement and the equation window agree on those values. The equation
window writes the power as `W_dot_turb = -1000` kW. The comment in the
source says the control volume is the geothermal water, which supplies the
power.

## Model

The inlet state is fixed by pressure and temperature. The throttle is
adiabatic, exchanges no work, and changes of kinetic and potential energy
are neglected, so the flash-mixture enthalpy equals the inlet enthalpy.
The quality at the flash pressure is the vapour mass-flow fraction. The
turbine is adiabatic, with the same kinetic and potential energy
assumption, so its power is the vapour flow times the enthalpy drop from
saturated vapour at 400 kPa to the two-phase exit. Enthalpies are
real-fluid properties of Water.

- \(h_\mathrm{ev} = h_1\)
- \(x_\mathrm{ev} = x(p_\mathrm{ev}, h_\mathrm{ev}) = \dot m_\mathrm{vap}/\dot m_\mathrm{tot}\)
- \(\dot W_\mathrm{turb} = \dot m_\mathrm{vap}(h_3 - h_2)\)
- \(\dot m_\mathrm{source} = 3600\,\dot m_\mathrm{tot}\) (hourly flow, as written)

| Input | Value |
|---|---|
| `p_1` | 1.5 MPa (1.5×10⁶ Pa) |
| `T_1` | 180 °C |
| `p_ev`, `p_2` | 400 kPa (4×10⁵ Pa) |
| `p_3` | 10 kPa (10⁴ Pa) |
| `x_3` | 0.9 |
| `W_dot_turb` | −1000 kW (−10⁶ W) |

These inputs are already equations in the EES equation window. `p_ev`
and `p_2` are both set to 400 kPa. The window has 17 equations and 17
variables, so the system is square. The stored values of the unknowns
are guesses in `.initials`.

`quality(Water, p=p_ev, h=h_ev)` is inside the vapour dome. The result is
`x_ev` = 0.074365, and that quality is the equation that splits the source
flow into vapour and liquid.

The hourly mass and volume flows keep the factor 3600 s/h of the original,
because the exercise asks for an hourly flow. `q_m_source` is in kg/h and
`q_v_source` is in m³/h. The mass flows `q_m_vap` and `q_m_tot` stay in
kg/s.

The sixteen equations `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 geothermal
inlet, i = 2 mixture after the throttle, i = 3 saturated vapour at the
turbine inlet, i = 4 turbine exit) are post-processing for the CoolSolve
diagram. A solve of the 17 equation-window equations and a solve of this
file, both with the same `.initials`, give the same seventeen original
variables (relative difference 0).

## How to run

```bash
coolsolve ./geothermal_steam_turbine.eescode
```

Every block is explicit. CoolSolve reports 4 iterations with the shipped
`.initials` and 13 iterations without them. The `.initials` file is the
EES stored solution after the unit conversion below.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `T_1` | 180 °C | 180 °C |
| `W_dot_turb` | −1000000 W | −1000000 W |
| `q_m_vap` | 2.541944 kg/s | 2.541824 kg/s |
| `q_m_tot` | 34.18210 kg/s | 34.18087 kg/s |
| `q_m_source` | 123055.5 kg/h | 123051.1 kg/h |
| `q_v_source` | 138.6805 m³/h | 138.6755 m³/h |
| `x_ev` | 0.07436479 | 0.07436394 |
| `h_2` | 2738053 J/kg | 2738069 J/kg |
| `h_3` | 2344653 J/kg | 2344651 J/kg |
| `T[2]`, `T[3]` | 143.608 °C | not stored |
| `T[4]` | 45.806 °C | not stored |

`T[2]` and `T[3]` are both the saturation temperature at 400 kPa: the
flash mixture (`x_ev` = 0.074) and the saturated vapour drawn into the
turbine are at the same pressure. `T[4]` is the saturation temperature at
10 kPa, because the exit quality 0.9 is inside the dome. EES stored only
`T_1`. `q_m_vap`, `W_dot_turb` and the enthalpies are printed at the digits
used in *Verification*.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv`
from `R3_E8_2022.EES` (EES X10.836, 18 stored variables):

> 17 common variables, 0 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 16

No common variable exceeds rtol = 0.001. The maximum relative difference
over all common variables is **4.74e-05** (`q_m_vap`), the value
`compare_solution.py --all` prints. The exact ratio is 4.736955e-05.

`--ees-units` scaled the stored pressures (kPa), enthalpies (kJ/kg) and
power (kW). The stored unit strings are lowercase `kPa`, `kJ/kg` and `kW`,
and the tool listed each of them as converted.

`h_1`, `h_ev`, `h_2` and `h_3` are the absolute enthalpies. EES stored no
entropy. `h_1` and `h_ev` are the same state and agree with EES to
2.51×10⁻⁵ J/kg. `h_2` and `h_3` differ by −16.2405 J/kg and +2.395 J/kg.
Those residuals are unequal, so they are a property difference between the
two libraries. The steam flow follows from the enthalpy drop across the
turbine, and the power is the given input.

| Variable | EES | CoolSolve | CoolSolve − EES | rel. diff |
|---|---:|---:|---:|---:|
| `q_m_vap` | 2.54182395 | 2.541944361 | +0.000120411 | 4.74e-05 |
| `q_v_source` | 138.6754724 | 138.6804554 | +0.004983 | 3.59e-05 |
| `q_m_tot` | 34.1808685 | 34.1820967 | +0.001228 | 3.59e-05 |
| `q_m_source` | 123051.1266 | 123055.5481 | +4.4215 | 3.59e-05 |
| `x_ev` | 0.07436393696 | 0.0743647875 | +8.51e-07 | 1.14e-05 |
| `h_2` | 2738069.281 | 2738053.040 | −16.2405 | 5.93e-06 |
| `h_3` | 2344651.004 | 2344653.399 | +2.395 | 1.02e-06 |
| `h_1`, `h_ev` | 763304.2797 | 763304.2797 | +2.51e-05 | 3.29e-11 |

The enthalpy drop is 393418.3 J/kg in the stored solution and 393399.6 J/kg
in CoolSolve. Dividing the given 10⁶ W by that drop reproduces `q_m_vap`.
The hourly source flow is 3600 times `q_m_tot` and carries the same
relative difference, 3.59e-05.

The other common variables are exact (`--all`): `p_1`, `p_2`, `p_3`,
`p_ev`, `T_1`, `x_3` and `W_dot_turb`. `v_1` differs by 3.95e-10.

The name only in the EES solution is `P` (value 1, no unit, no equation).
The sixteen names only in the CoolSolve solution are the diagram arrays
`P[1]`, `h[1]`, `T[1]`, `s[1]`, `P[2]`, `h[2]`, `T[2]`, `s[2]`, `P[3]`,
`h[3]`, `T[3]`, `s[3]`, `P[4]`, `h[4]`, `T[4]`, `s[4]`.

## Source and attribution

The equation window names no person. The authors field is therefore
S. Quoilin, the name the inventory gives for the course. The EES licence
tag is the student and staff licence of the Laboratoire de Thermodynamique,
University of Liège, not an author. Course: ULiège MECA0002, 2022-2023,
repetition R3, exercise 8. Source file:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R3/R3_E8_2022.EES`
(EES X10.836, inventory row TM-0418). The comments in the source are French.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X10.836,
  unit system `SI MASS DEG KPA C KJ`, decimal comma already rewritten to a
  dot, 18 stored variables, no tables). The equation window with the
  `$UnitSystem` line removed is square (17 equations, 17 variables), so no
  Diagram-window input was restored. The extra stored name is `P` = 1.
  Pressures and the power were converted by hand, and the original value is
  in the comment:
  - `p_1`: 1500 kPa → 1.5×10⁶ Pa
  - `p_ev`: 400 kPa → 4×10⁵ Pa
  - `p_2`: 400 kPa → 4×10⁵ Pa
  - `p_3`: 10 kPa → 10⁴ Pa
  - `W_dot_turb`: −1000 kW → −10⁶ W
  - `T_1` = 180 °C and `x_3` = 0.9 unchanged (`x_3` was `0,9` in the file)
  - `q_m_source = 3600*q_m_tot` unchanged; 3600 s/h is the hourly result the
    exercise asks for, and `--ees-units` does not scale kg/h or m³/h
  - the energy balance is unchanged: W and Δh both scale by 1000
  - property calls had no extra factor of 1000
  The `$UnitSystem` directive was deleted. The fluid name `water` was
  written `Water`. Comments were translated into English. The `.initials`
  file is the stored solution with pressures, enthalpies and the power
  multiplied by 1000. `P` is omitted.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  i = 1 to 4 as listed above. Relative difference 0 on the 17 original
  variables.
- **2026-10-15 — separate from CSL-0174**: the equations were compared with
  `steam_turbine_isentropic_efficiency` (CSL-0174, Cengel 7-104: 3 kg/s,
  8 MPa to 30 kPa, isentropic efficiency 0.9). This file is the geothermal
  flash exercise, so the two models are separate. `related` is empty.
  CSL-0174 needs no back-link.
- **Level**: equations 33 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone, discretised or coupled-component
  sub-model (a throttle balance and a turbine balance) → 0; no
  semi-empirical, off-design or dynamic physics → 0; converges with and
  without guesses, no `coolsolve.conf` → 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

The turbine and the throttle are adiabatic, and changes of kinetic and
potential energy are omitted, as in the source. The liquid that leaves the
flash vessel is not given its own state. No CoolSolve gap blocks the file.

## Related models

None. CSL-0174 is a different steam-turbine exercise and is not linked.
