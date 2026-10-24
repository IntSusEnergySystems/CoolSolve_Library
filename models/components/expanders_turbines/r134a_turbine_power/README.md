# R134a turbine of 5 kW driving a compressor (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0189`

An R134a turbine with an isentropic efficiency of 78 % delivers 5 kW of
mechanical power. After the alternator and a mechanical link, 57 % of the
electricity drives a generator and then an R134a compressor. The two
machines use the same mass flow. The model computes that flow and the
compressor outlet pressure. Teaching exercise, ULiège MECA0002, repetition
R4, exercise 3 (2022-2023).

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | R134a |
| **Size** | 48 equations (largest block: 1) |
| **Source** | thermo_models, ULiège MECA0002, file `R04_E3_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@3e9c1b6 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A turbine with an isentropic efficiency of 78 % produces 5 kW of mechanical
power and drives an alternator through a mechanical link. The mechanical
link has an efficiency of 95 % and the alternator an efficiency of 92 %.
Of the electrical production at the alternator, 57 % is consumed on site by
a generator with an efficiency of 92 %, which drives a compressor with an
isentropic efficiency of 82 % through a mechanical link of efficiency 95 %.
The working fluid is R134a in both machines. At the compressor inlet the
fluid is saturated. At the turbine inlet the fluid is superheated by 40 °C.
The mass flow is the same in the compressor and in the turbine. The turbine
inlet and outlet pressures are 3000 kPa and 1000 kPa. The compressor inlet
pressure equals the turbine outlet pressure. Calculate the refrigerant mass
flow and the compressor outlet pressure.

The pasted statement and the equation window agree on these values. The
statement says the compressor inlet is saturated. The equation window sets
the quality to 1, and its comment says the fluid is gaseous, so the inlet
is saturated vapour.

## Model

The turbine inlet pressure and 40 °C of superheat fix the inlet state. The
isentropic turbine exit has the inlet entropy and the turbine outlet
pressure. The given isentropic efficiency then fixes the real exit enthalpy.
The same mass flow goes through the compressor. The compressor inlet is
saturated vapour at the turbine outlet pressure. Its isentropic efficiency
uses the compressor form of the enthalpy ratio, and the outlet pressure is
the pressure of the isentropic compressor exit. Enthalpies and entropies are
real-fluid properties of R134a. Both machines are taken as adiabatic because
the process is fast, as in the original comments. The first law in the file
is a mass flow times an enthalpy change.

- \(T_\mathrm{in,turb} = T_\mathrm{sat}(p_\mathrm{in,turb}) + 40\)
- \(\eta_\mathrm{is,turb} = (h_\mathrm{out,turb} - h_\mathrm{in,turb}) / (h_\mathrm{out,turb,is} - h_\mathrm{in,turb})\)
- \(\dot W_\mathrm{turb} = \dot m\,(h_\mathrm{out,turb} - h_\mathrm{in,turb}) = -5000\,\mathrm{W}\)
- \(\dot W_\mathrm{elec} = -\dot W_\mathrm{turb}\,\eta_\mathrm{turb\to cp}\,\eta_\mathrm{alt}\,\eta_\mathrm{meca}\)
- \(\dot W_\mathrm{cp} = \dot W_\mathrm{elec}\,\eta_\mathrm{alt}\,\eta_\mathrm{meca}\)
- \(\eta_\mathrm{is,cp} = (h_\mathrm{out,cp,is} - h_\mathrm{in,cp}) / (h_\mathrm{out,cp} - h_\mathrm{in,cp})\)
- \(p_\mathrm{out,cp} = p(h_\mathrm{out,cp,is}, s_\mathrm{in,cp})\)

`eta_alt` (0.92) and `eta_meca` (0.95) are each used twice: once between the
turbine and the alternator, and once between the generator and the
compressor. That matches the two efficiencies of 92 % and the two mechanical
links of 95 % in the statement.

| Input | Value |
|---|---|
| `eta_is_turb` | 0.78 |
| `W_dot_turb` | −5000 W (−5 kW in the original) |
| `p_in_turb` | 3 MPa (3000 kPa in the original) |
| `p_out_turb` | 1 MPa (1000 kPa in the original) |
| `eta_is_cp` | 0.82 |
| `x_in_cp` | 1 (saturated vapour) |
| `eta_alt` | 0.92 |
| `eta_meca` | 0.95 |
| `eta_turb_to_cp` | 0.57 |
| superheat | 40 °C |

The equation window is square: 24 equations and 24 variables. No
Diagram-window input was restored. The stored values of the unknowns are
guesses in `.initials`. The twenty-four equations `P[i]`, `h[i]`, `T[i]`,
`s[i]` (i = 1 turbine inlet, i = 2 isentropic turbine exit, i = 3 real
turbine exit, i = 4 compressor inlet, i = 5 isentropic compressor exit,
i = 6 real compressor exit) are post-processing for the CoolSolve diagram.
They do not change the twenty-four physical results.

## How to run

```bash
coolsolve ./r134a_turbine_power.eescode
```

Every block has size 1. CoolSolve reports 10 iterations with the shipped
`.initials` and 10 iterations without them. The `.initials` file is the EES
stored solution with kPa, kJ and kW converted to Pa, J and W. The enthalpy
and entropy guesses therefore sit on the EES reference state, about
148 kJ/kg and 796 J/kg·K below the CoolProp solution, and they do not
reduce the iteration count. Each efficiency equation is linear in the
unknown enthalpy, so the physical root is unique. There is no `abs()` call.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `W_dot_turb` | −5000 W | −5000 W |
| `W_dot_turb_elec` | 2490.9 W | 2490.9 W |
| `W_dot_cp` | 2177.0466 W | 2177.0466 W |
| `m_dot_turb` | 0.231233 kg/s | 0.231286 kg/s |
| `T_in_turb` | 126.203 °C | 126.164 °C |
| `p_in_turb` | 3.000000×10⁶ Pa | 3.000000×10⁶ Pa |
| `p_out_turb`, `p_in_cp` | 1.000000×10⁶ Pa | 1.000000×10⁶ Pa |
| `p_out_cp` | 1.467011×10⁶ Pa | 1.466977×10⁶ Pa |

EES stored no other temperature. From the diagram states, the real turbine
exit `T[3]` is 85.175 °C, the compressor inlet `T[4]` is 39.388 °C, and the
real compressor exit `T[6]` is 57.169 °C.

The absolute enthalpies and entropies carry the R134a reference offset and
are listed under *Verification*. The enthalpy changes, which determine the
power, are:

| Change | CoolSolve | EES stored |
|---|---:|---:|
| `h_out_turb - h_in_turb` | −21623.165 J/kg | −21618.245 J/kg |
| `h_out_cp - h_in_cp` | 9414.927 J/kg | 9412.785 J/kg |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
`R04_E3_2022.EES` (EES X10.836, 24 stored variables). Stored unit strings
kPa, kJ/kg, kJ/(kg·K) and kW were scaled by the tool.

> 24 common variables, 8 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 24

The maximum relative difference over all common variables is **4.65e-01**
(`s_in_cp`), the value `compare_solution.py` prints. The exact ratio is
0.4649716293. That maximum is the reference offset on the absolute entropy.
It is the value stored in `verification.max_rel_diff`.

The eight variables above rtol = 0.001 are the six enthalpies and the two
entropies. EES sets the enthalpy and entropy of saturated liquid R134a at
−40 °C to zero. In this CoolSolve binary that state is

- \(h = 148144.046\,\mathrm{J/kg}\)
- \(s = 795.610\,\mathrm{J/kg{\cdot}K}\)

| Variable | EES | CoolSolve | CoolSolve − EES | after the −40 °C reference |
|---|---:|---:|---:|---:|
| `h_in_turb` | 341200.5015 | 489399.006 | +148198.504 | +54.458 J/kg |
| `h_out_turb` | 319582.2564 | 467775.841 | +148193.585 | +49.539 J/kg |
| `h_out_turb_is` | 313484.8026 | 461676.9996 | +148192.197 | +48.151 J/kg |
| `h_out_cp` | 280405.12 | 428576.730 | +148171.610 | +27.564 J/kg |
| `h_out_cp_is` | 278710.8186 | 426882.043 | +148171.224 | +27.178 J/kg |
| `h_in_cp` | 270992.3346 | 419161.802 | +148169.468 | +25.422 J/kg |
| `s_in_turb` | 1043.649588 | 1839.398442 | +795.748854 | +0.1384 J/kg·K |
| `s_in_cp` | 915.5786686 | 1711.271250 | +795.692581 | +0.0821 J/kg·K |

The shift is the reference state plus a residual of 25 to 54 J/kg on
enthalpy and 0.082 to 0.138 J/kg·K on entropy. The residual is an
equation-of-state difference between CoolSolve and EES. It is why the
turbine enthalpy drop differs by −4.920 J/kg. With the turbine power fixed
at −5000 W, the mass flow carries that same relative difference, 2.28e-04,
which is below rtol = 0.001.

The physical results, which do not carry the reference offset:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `W_dot_turb` | −5000 | −5000 | 0 |
| `W_dot_turb_elec` | 2490.9 | 2490.9 | 0 |
| `W_dot_cp` | 2177.0466 | 2177.0466 | 0 |
| `m_dot_turb`, `m_dot_cp` | 0.231286 | 0.231233 | 2.28e-04 |
| `T_in_turb` | 126.164 | 126.203 | 3.15e-04 |
| `p_out_cp` | 1.46698×10⁶ | 1.46701×10⁶ | 2.33e-05 |
| `p_in_turb` | 3×10⁶ | 3×10⁶ | 0 |
| `p_out_turb`, `p_in_cp` | 1×10⁶ | 1×10⁶ | 0 |
| `eta_is_turb`, `eta_is_cp`, `eta_alt`, `eta_meca`, `eta_turb_to_cp`, `x_in_cp` | given values | same | 0 |

`m_dot`, `T_in_turb` and `p_out_cp` are printed at the digits of
`compare_solution.py`. The twenty-four names only in the CoolSolve solution
are the diagram arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` for i = 1…6.

## Source and attribution

The file itself names nobody. The `{$ID$}` tag is the laboratory licence
("For use only by students and staff at the Laboratoire de Thermodynamique,
University of Liege PoloUHB"), not an author. The inventory attributes the
course to S. Quoilin, so the authors entry is S. Quoilin. Teaching exercise,
ULiège MECA0002, repetition R4, exercise 3, 2022-2023. Source file:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R4/R04_E3_2022.EES`
(EES X10.836, inventory row TM-0423). The comments in the source are French.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X10.836, unit
  system `SI MASS DEG KPA C KJ`, 24 variables, no tables). The extractor
  rewrote decimal commas as dots. The equation window, with the
  `$UnitSystem` line removed, is square (24 equations, 24 variables), so no
  Diagram-window input was restored. Pressures 3000 kPa and 1000 kPa were
  written 3×10⁶ Pa and 1×10⁶ Pa. The turbine power −5 kW was written
  −5000 W. The 40 °C of superheat and the efficiencies are unchanged.
  Property calls then return J and J/kg·K. The `$UnitSystem` directive was
  deleted. Comments were translated into English. Variable names and
  equations are otherwise unchanged. The shipped `.initials` is the stored
  solution in Pa, J and W.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  the turbine inlet, the isentropic and real turbine exits, the compressor
  inlet, and the isentropic and real compressor exits. A solve of the
  equation window alone and a solve of this file give the same twenty-four
  original variables (relative difference 0).
- **Level**: equations 48 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; multi-zone / discretised / three coupled
  components: absent (turbine and compressor, plus scalar efficiencies) → 0;
  constant efficiencies at one operating
  point → 0; converges with and without guesses, no `coolsolve.conf` → 0.
  Score 1 → level 1.

## Limitations and CoolSolve gaps

The first law is a mass flow times an enthalpy change, as in the original,
so a heat transfer and changes of kinetic and potential energy are absent.
Both machines are adiabatic because the process is fast, as the original
comments say. No CoolSolve gap blocks the file. `quality()` is not called.
The solver output contains no Fahrenheit hint. The compressor and the
transmission efficiencies are the ones written in the equation window.

## Related models

`CSL-0174` (steam turbine with isentropic efficiency) uses the same turbine
closure: inlet state from pressure and temperature, isentropic exit from the
inlet entropy and the exit pressure, isentropic efficiency on the enthalpy
drop, and power equal to the mass flow times that drop. This exercise adds
the electrical split and the R134a compressor.

`CSL-0182` (geothermal steam turbine) expands saturated vapour to a
prescribed exit quality, with a flash vessel upstream. The related entry
for the isentropic-efficiency closure is `CSL-0174`.

`CSL-0282` (steam turbine driving a nitrogen compressor) is the same
exercise family on two fluids: a steam turbine feeding a nitrogen
compressor plus a generator, with a perfect-gas comparison for the
nitrogen instead of isentropic efficiencies.

