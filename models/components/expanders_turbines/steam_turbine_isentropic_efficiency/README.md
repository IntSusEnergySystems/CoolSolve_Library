# Steam turbine with isentropic efficiency (Cengel 7-104)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0174`

Steam at 8 MPa and 500 °C expands to 30 kPa in a turbine. The mass flow rate
is 3 kg/s and the isentropic efficiency is 90 %. The model computes the
power output. Textbook exercise Cengel 7-104.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | Water |
| **Size** | 27 equations (largest block: 1) |
| **Source** | thermo_models, KU Leuven exercises, file `07-104.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution (see *Verification*) |

## Problem statement

3 kg/s of steam at 8 MPa and 500 °C expands to 30 kPa in a turbine with an
isentropic efficiency of 90 %. The exercise asks for the power output and the
entropy generation. Textbook exercise Cengel 7-104.

## Model

The inlet state is fixed by pressure and temperature. The isentropic exit
has the inlet entropy and the exit pressure. The given isentropic efficiency
defines the real specific work, and the real exit enthalpy follows from that
work. Enthalpies and entropies are real-fluid properties of Water. The power
is the mass flow times the enthalpy drop, as written in the source.

- \(s_{2s} = s_1\), \(p_{2s} = p_2\), \(h_{2s} = h(p_{2s}, s_{2s})\)
- \(w_s = h_1 - h_{2s}\)
- \(\varepsilon_s = w / w_s\), \(w = h_1 - h_2\)
- \(\dot W_\mathrm{out} = \dot m\,(h_1 - h_2)\)

| Input | Value |
|---|---|
| `p_1` | 8 MPa (8×10⁶ Pa) |
| `T_1` | 500 °C |
| `M_dot` | 3 kg/s |
| `p_2` | 30 kPa (30×10³ Pa) |
| `epsilon_s` | 0.9 |

`p_1`, `T_1`, `M_dot`, `p_2` and `epsilon_s` are already equations in the
EES equation window. The system is square without any further assignment
(15 equations, 15 variables). The stored values of the unknowns are guesses
in `.initials`, not equations.

The source does not write an entropy-generation rate, and the stored
solution has no exit entropy. For this energy balance the generation rate of
an adiabatic turbine is \(\dot m(s_2 - s_1)\). Formed from the diagram
entropy `s[3]` it is 991.553 W/K. That number is not an equation of the file
and was not compared with EES.

The twelve equations `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 inlet, i = 2
isentropic exit, i = 3 real exit) are post-processing for the CoolSolve
diagram. They do not change the fifteen physical results.

## How to run

```bash
coolsolve ./steam_turbine_isentropic_efficiency.eescode
```

Every block is explicit. CoolSolve reports 4 iterations with the shipped
`.initials` and 20 iterations without them. The `.initials` file is the EES
stored solution.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `p_1` | 8000000 Pa | 8000000 Pa |
| `p_2` | 30000 Pa | 30000 Pa |
| `T_1` | 500 °C | 500 °C |
| `epsilon_s` | 0.9 | 0.9 |
| `T_2` | 69.0952 °C | 69.1135 °C |
| `h_2` | 2381429 J/kg | 2380743 J/kg |
| `w` | 1018062 J/kg | 1017788 J/kg |
| `W_dot_out` | 3054187 W | 3053365 W |

`T[2]` and `T[3]` are both 69.0952 °C. At 30 kPa the saturated-liquid and
saturated-vapour enthalpies are 289273 J/kg and 2624548 J/kg. Both `h_2s`
(2268311 J/kg) and `h_2` lie between them, so both exits are in the
two-phase region and both temperatures are the saturation temperature. EES
stored `T_2` and did not store a temperature of the isentropic exit.
`W_dot_out`, `T_2` and `h_2` are printed at the digits of
`compare_solution.py`.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against `reference/ees_variables.csv` from `07-104.EES`
(EES X9.920, 15 stored variables):

> 15 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 12

No common variable exceeds rtol = 0.001. The maximum relative difference
over all common variables is **3.36e-04** (`s_1` and `s_2s`), the value
`compare_solution.py --all` prints. The exact ratio is 3.358613e-04.

`h_1`, `h_2`, `h_2s`, `s_1` and `s_2s` are the absolute enthalpies and
entropies. They are not a reference-state offset: a shift would add the
same constant to every enthalpy and the same constant to every entropy.
Saturated liquid Water at 0.01 °C in this binary is \(h = 0.612\) J/kg and
\(s \approx 0\), the IAPWS triple-point reference, and the stored EES
values already sit within about 1 kJ/kg and 2.3 J/kg·K of CoolSolve.

| Variable | EES | CoolSolve | CoolSolve − EES | rel. diff |
|---|---:|---:|---:|---:|
| `s_1`, `s_2s` | 6724.326982 | 6726.586182 | +2.2592 | 3.36e-04 |
| `h_2s` | 2267655.016 | 2268311.134 | +656.118 | 2.89e-04 |
| `h_2` | 2380742.627 | 2381429.186 | +686.559 | 2.88e-04 |
| `h_1` | 3398531.123 | 3399491.652 | +960.529 | 2.83e-04 |
| `w_s` | 1130876.106 | 1131180.518 | +304.412 | 2.69e-04 |
| `W_dot_out` | 3053365.487 | 3054187.398 | +821.911 | 2.69e-04 |
| `w` | 1017788.496 | 1018062.466 | +273.970 | 2.69e-04 |
| `T_2` | 69.11354033 | 69.09517418 | −0.018366 | 2.66e-04 |

`s_2s = s_1`, so those two names share one residual. The three enthalpy
residuals are not equal. Their spread is the whole difference of the
isentropic work (304.412 J/kg). The power carries that same relative
difference, 2.69e-04, which is below rtol = 0.001 and smaller than the
entropy residual.

The other common variables are exact (`--all`):

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `epsilon_s` | 0.9 | 0.9 | 0.00e+00 |
| `M_dot` | 3 | 3 | 0.00e+00 |
| `p_1` | 8000000 | 8000000 | 0.00e+00 |
| `p_2`, `p_2s` | 30000 | 30000 | 0.00e+00 |
| `T_1` | 500 | 500 | 0.00e+00 |

The twelve names only in the CoolSolve solution are the diagram arrays
`P[1]`, `h[1]`, `T[1]`, `s[1]`, `P[2]`, `h[2]`, `T[2]`, `s[2]`, `P[3]`,
`h[3]`, `T[3]`, `s[3]`.

## Source and attribution

S. Quoilin, KU Leuven course exercises. Textbook problem Cengel 7-104. The
EES licence tag in the file is the J. Lebrun laboratory licence (University
of Liège), not the author. Source file:
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/07-104.EES`
(EES X9.920, inventory row TM-0340). The comments in the source are English.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X9.920, unit
  system `SI MASS DEG PA C J`, 15 variables, no tables, no warnings). The
  unmodified equation window, with the `$UnitSystem` line removed, is square
  (15 equations, 15 variables), so no Diagram-window input was restored.
  No unit was converted: pressures are already in Pa, the temperature already
  in °C, and the enthalpies already in J/kg. The `$UnitSystem` directive was
  removed. The fluid name `water` was written `Water`. EES names are
  case-insensitive, so the property calls were written with `T=` and `T_1`,
  the name of the inlet-temperature assignment. Comments were already
  English; each dimensional quantity was given its SI unit. Variable names
  and equations are otherwise unchanged. The shipped `.initials` is the EES
  stored solution.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  i = 1 (inlet), i = 2 (isentropic exit) and i = 3 (real exit). `T[2]` is
  `temperature(Water, p=p_2s, h=h_2s)`. `s[3]` is `entropy(Water, p=p_2, h=h_2)`.
  A solve of the equation window alone and a solve of this file give the same
  fifteen original variables (relative difference 0).
- **2026-10-15 — not CSL-0135**: the equations were compared with
  `turbine_stodola_offdesign` (CSL-0135). That model is Stodola's cone law
  at a design point and an off-design point, with an efficiency
  characteristic. This file is the constant-efficiency textbook expansion,
  so it is a separate model and is not linked.
- **Level**: equations 27 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone or discretised component → 0; no
  semi-empirical, off-design or dynamic physics → 0; converges with and
  without guesses, no `coolsolve.conf` → 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

The power is written `W_dot_out = M_dot*(h_1 - h_2)`, as in the original,
so a heat transfer and changes of kinetic and potential energy are absent.
The source does not write the entropy generation the textbook asks for.
No CoolSolve gap blocks the file. The solver prints a hint that the inlet
temperature 500 °C is Celsius and not 500 K. The value used is still 500 °C,
and `T_1` matches the stored solution. `T_2` is 69.1 °C, which is not within
3 of 32, 77 or 212, so the hint `CS-BUG-HINT-FAHRENHEIT` does not print.
`quality()` is not called.

## Related models

- `CSL-0189` (*r134a_turbine_power*): an R134a turbine with the same
  isentropic-efficiency closure, driving a compressor. This model is a
  steam turbine.
