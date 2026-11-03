# R134a refrigerator with a water-cooled condenser (Cengel 11-11)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0209`

R134a vapour-compression cycle with a water-cooled condenser. The equation
window fixes three refrigerant states and a cooling-water stream, then
computes the condenser heat, the refrigerant mass flow, the compressor power
and the refrigerator COP. Textbook exercise Cengel 11-11.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R134a, Water |
| **Size** | 29 equations (largest block: 1) |
| **Source** | thermo_models, KU Leuven exercises, file `11-11d.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@d1e1203 — verified against the EES stored solution (see *Verification*) |

## Problem statement

The source is textbook exercise Cengel 11-11, written as an exercise. The
equation window gives the cycle data directly:

- point 1: −34 °C and 60 kPa (`60e3` Pa)
- point 2: 65 °C and 1.2 MPa (`1.2E6` Pa)
- point 3: 42 °C, at the pressure of point 2
- water circuit: 18 °C to 26 °C, mass flow 0.25 kg/s, water taken at 1 bar
- compressor data: `Q_dot_in` = 450 W

Point 4 is defined by `p_4 = p_1` and `h_4 = h_3`. The window then forms the
condenser heat balance on the water and on the refrigerant, the open-system
balance `Q_dot_in + W_dot_in = M_dot*(h_2 - h_1)`, the refrigeration rate
`Q_dot_L = M_dot*(h_1 - h_4)`, and the COP in refrigerator mode. It does not
add a theoretical-maximum load.

## Model

Real-fluid properties of R134a give the enthalpies and entropies at points 1,
2 and 3 from temperature and pressure. Superheat at point 1 and subcooling at
point 3 are differences from `T_sat`. Point 4 uses the pressure–enthalpy pair
already written in the source. Water enthalpies use `Water` at 1 bar, as in
the original comment.

- \(h_1 = h(T_1, p_1)\), and the same form for points 2 and 3
- \(p_3 = p_2\), \(p_4 = p_1\), \(h_4 = h_3\)
- \(\dot Q_h = \dot m_w (h_{w,\mathrm{out}} - h_{w,\mathrm{in}}) = \dot m (h_2 - h_3)\)
- \(\dot Q_\mathrm{in} + \dot W_\mathrm{in} = \dot m (h_2 - h_1)\)
- \(\dot Q_L = \dot m (h_1 - h_4)\), \(\mathrm{COP} = \dot Q_L / \dot W_\mathrm{in}\)

| Input | Value |
|---|---|
| `T_1`, `p_1` | −34 °C, 60×10³ Pa |
| `T_2`, `p_2` | 65 °C, 1.2×10⁶ Pa |
| `T_3` | 42 °C |
| `T_w_in`, `T_w_out`, `M_dot_w` | 18 °C, 26 °C, 0.25 kg/s |
| `Q_dot_in` | 450 W |

Those nine assignments are already equations in the EES equation window. The
system is square without any further assignment (29 equations, 29 variables).
The stored values of the unknowns are guesses in `.initials`, not equations.
No diagram-state arrays were added: the equation window does not contain them.

## How to run

```bash
coolsolve ./r134a_water_cooled_condenser.eescode
```

Every block is an explicit assignment (largest block 1). CoolSolve reports
4 iterations with the shipped `.initials` and 8 iterations without them. Both
runs reach the same root. The equation window has no `abs()`, so there is no
second root to reject. The `.initials` file is the EES stored solution,
including R134a enthalpies and entropies on the EES reference state.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `COP` | 2.150503 | 2.150496 |
| `Q_dot_h` | 8365.889 W | 8366.082 W |
| `M_dot_w` | 0.25 kg/s | 0.25 kg/s |
| `M_dot` | 0.0454840 kg/s | 0.0454855 kg/s |
| `W_dot_in` | 2512.580 W | 2512.646 W |
| `Q_dot_L` | 5403.309 W | 5403.436 W |
| `x_4` | 0.479477 | 0.479536 |
| `DELTAT_sh_1` | 2.93460 °C | 2.94756 °C |
| `DELTAT_sc_3` | 4.31453 °C | 4.29396 °C |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against `reference/ees_variables.csv` from `11-11d.EES`
(EES X9.920, 29 stored variables). The extract unit system is
`SI MASS DEG PA C J`. Pressures in the equation window are already in Pa
(`60e3`, `1.2E6`) and the stored enthalpies are already in J
(`h_1` = 230026.7772 J/kg). The unit strings in the reference CSV are blank.
Nothing was converted by hand, so `--ees-units` was not used.

> 29 common variables, 10 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0

The maximum relative difference over all common variables is **6.63e-01**
(`s_3`), the value `compare_solution.py` prints. The exact ratio is
0.6633360234. That maximum is the reference offset on the absolute entropy.
It is the value stored in `verification.max_rel_diff`.

EES sets the enthalpy and entropy of saturated liquid R134a at −40 °C to
zero. In this CoolSolve binary that state is

- \(h = 148144.046\,\mathrm{J/kg}\)
- \(s = 795.610\,\mathrm{J/kg{\cdot}K}\)

| Variable | EES | CoolSolve | CoolSolve − EES | after the −40 °C reference |
|---|---:|---:|---:|---:|
| `h_1` | 230026.777 | 378172.912 | +148146.135 | +2.089 J/kg |
| `h_2` | 295160.657 | 443307.486 | +148146.829 | +2.783 J/kg |
| `h_3` | 111232.045 | 259377.038 | +148144.992 | +0.947 J/kg |
| `h_4` | 111232.045 | 259377.038 | +148144.992 | +0.947 J/kg |
| `s_1` | 973.823 | 1769.442 | +795.620 | +0.0092 J/kg·K |
| `s_2` | 977.833 | 1773.453 | +795.620 | +0.0095 J/kg·K |
| `s_3` | 403.799 | 1199.413 | +795.614 | +0.0034 J/kg·K |
| `s_4` | 470.973 | 1266.587 | +795.615 | +0.0041 J/kg·K |

The eight absolute enthalpies and entropies are the differences above
rtol = 0.001. They are the reference offset, not a unit error: the stored
values are already in J and J/kg·K.

The other two differences above rtol = 0.001 are saturation temperatures
written as superheat and subcooling:

| Variable | EES | CoolSolve | rel. diff | cause |
|---|---:|---:|---:|---|
| `DELTAT_sh_1` | 2.94756 °C | 2.93460 °C | 4.40e-03 | `T_sat` at 60 kPa is −36.9346 °C against −36.9476 °C |
| `DELTAT_sc_3` | 4.29396 °C | 4.31453 °C | 4.77e-03 | `T_sat` at 1.2 MPa is 46.3145 °C against 46.2940 °C |

Water has no large reference offset. The residuals are property differences
under rtol = 0.001:

| Variable | EES | CoolSolve | CoolSolve − EES | rel. diff |
|---|---:|---:|---:|---:|
| `h_w_in` | 75561.150 | 75636.457 | +75.307 J/kg | 9.96e-04 |
| `h_w_out` | 109025.479 | 109100.014 | +74.535 J/kg | 6.83e-04 |

The water enthalpy rise is 33463.557 J/kg against 33464.329 J/kg. That is why
the condenser heat and the flows stay close while the absolute water
enthalpies differ by about 75 J/kg.

Quantities that do not carry the R134a reference:

| Quantity | CoolSolve | EES | rel. diff |
|---|---:|---:|---:|
| `COP` | 2.150503 | 2.150496 | 2.98e-06 |
| `Q_dot_h` | 8365.889 W | 8366.082 W | 2.31e-05 |
| `M_dot_w` | 0.25 kg/s | 0.25 kg/s | 0 |
| `M_dot` | 0.04548398 kg/s | 0.04548549 kg/s | 3.31e-05 |
| `W_dot_in` | 2512.580 W | 2512.646 W | 2.64e-05 |
| `Q_dot_L` | 5403.309 W | 5403.436 W | 2.34e-05 |
| `x_4` | 0.479477 | 0.479536 | 1.24e-04 |

## Source and attribution

The equation window and the file header name no person. The EES licence tag
`{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege}` is
the licence holder, not an author. The inventory attributes the KU Leuven
course to S. Quoilin, so the author is S. Quoilin.

Source file: `~/Nextcloud/thermo_models/thermo_kuleuven/exercices/11-11d.EES`
(candidate TM-0351, EES X9.920). An earlier file of the same exercise,
`11-11.EES` (TM-0350), is not this model.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `11-11d.EES` (EES X9.920, 29 variables, no tables, no warnings). The unit system is already `SI MASS DEG PA C J`. `$UnitSystem` was deleted. No kPa or kJ value was converted by hand. Comments were already in English; each dimensional quantity now carries its SI unit. Fluid names are written `R134a` and `Water` (the source uses `r134a` and `water`). Property-call keys are written `T`, `P` and `H` (the source uses `t`, `p` and `h`).
- **2026-10-15 — comment semicolon**: the section title `"Heat balance over the condenser";` does not parse (`Could not parse line`). The semicolon is not an equation and was deleted. The equations are unchanged.
- **2026-10-15 — square system**: 29 equations and 29 variables, system square. The cycle data are already equations in the equation window, so no diagram-window input was restored and no stored unknown was replaced by a value. No diagram-state arrays were added.
- **Level**: equations 29 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; not multi-zone or discretised → 0; no semi-empirical, off-design or dynamic physics → 0; converges from default guesses in 8 iterations, with no `coolsolve.conf` → 0. Score 0 → level 1. No pedagogical move.

## Limitations and CoolSolve gaps

The window fixes the three refrigerant temperatures and pressures and the
water temperatures. It does not size heat-transfer area, and it does not
compute a theoretical maximum refrigeration load. Absolute R134a enthalpy and
entropy use the CoolSolve reference state, so they differ from the EES values
by the offset above. No CoolSolve gap blocks the file.

## Related models

None. Other R134a condenser exercises in the library are different
calculations, and `related` is empty.
