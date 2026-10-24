# Reverse Brayton air refrigeration cycle with intercooling (exercise 3)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0212`

Open reverse Brayton cycle on ideal-gas air. The air enters at 25 °C and
ambient pressure and is delivered at 15 °C and the same pressure. Compression
is in two stages. Each stage is followed by cooling back to the inlet
temperature. The expander drives the second compressor. The result of the
exercise is the COP. Teaching exercise 3 of ULiège *Thermodynamique appliquée*,
THD10 repetition 9 (2010/2017 file, kept in the 2022-2023 course `old` folder).

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | Air |
| **Size** | 46 equations (largest block: 1) |
| **Source** | thermo_models, file `THD10_R9_E3.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@62d92f0 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Calculate the COP of an air refrigeration cycle that would bring air from
25 °C to 15 °C, given:

- compression is divided into two stages, each followed by cooling back to the initial temperature;
- the mechanical efficiency of the first stage is 0.9;
- the power delivered by the expander equals the power required to drive the second compression stage;
- the isentropic efficiencies of compression and of expansion are 80 %;
- the ambient pressure is 1 bar.

The equation window sets that ambient pressure to 100 kPa.

## Model

Ideal-gas `Air`, as named in the file. Enthalpy depends only on temperature.
The stations follow the original:

1. Inlet of the first compressor: ambient pressure, 25 °C.
2. Outlet of the first compressor. The isentropic efficiency is written
   \(\eta_\mathrm{is}(h_2 - h_1) = h_{2,\mathrm{is}} - h_1\), so \(h_2\) is not
   a denominator.
3. Outlet of the first heat exchanger: cooled back to the inlet temperature.
   The exchanger is taken as isobaric, so \(p_2 = p_3\).
4. Outlet of the second compressor. \(h_4\) comes from the shaft balance below.
5. Outlet of the second heat exchanger: again cooled to the inlet temperature,
   isobaric, so \(p_4 = p_5\).
6. Turbine outlet: ambient pressure and 15 °C, the delivery state of the statement.
7. Extra point that closes the cycle on a T-s diagram: \(T_7 = T_1\),
   \(p_7 = p_1\), \(s_7 = s_1\). The equation window does not define \(h_7\).

The expander supplies the second compression stage:

\[
w_{c2} + w_t = 0, \qquad w_{c2} = h_4 - h_3, \qquad w_t = h_6 - h_5
\]

The useful effect is the enthalpy drop of the air from the inlet state to the
delivery state, and the mechanical efficiency applies only to the first stage:

\[
q_\mathrm{ut} = h_1 - h_6, \qquad \mathrm{COP} = \frac{q_\mathrm{ut}}{w_{c1}/\eta_\mathrm{mec}}
\]

\(r_{p,\min}\) is a separate constant-\(\gamma\) estimate with \(\gamma = 1.4\)
and the original \(+273\) (not 273.15). It does not close the cycle. The cycle
states use the Air property functions.

| Input | Value |
|---|---|
| `T_air_su` | 25 °C |
| `T_air_ex` | 15 °C |
| `p_amb` | 100 kPa (1×10⁵ Pa); 1 bar in the statement, 100 kPa in the equation window |
| `eta_is` | 0.8 |
| `eta_mec` | 0.9 |
| `fluid$` | `Air` |

46 equations, 46 variables, system square. No diagram-window input was added.
The stored solution also holds `P`, `p_2`, `h_1` and `h_2`. Those names are not
in the equation window (`h_1` and `p_2` appear only inside comments). Their
stored values (`P = 1`, `p_2 = 1230` kPa, `h_1 = 260.2` kJ/kg,
`h_2 = 252.9` kJ/kg) are not the cycle states `h[1]`, `h[2]` and `p[2]`.

## How to run

```bash
coolsolve ./reverse_brayton_intercooling.eescode
```

Every block has size 1. CoolSolve reports 10 iterations with the shipped
`.initials` and 16 iterations without them. Both runs reach the same root.
The `.initials` are the EES stored solution with pressures, specific energies
and specific entropies converted to Pa, J/kg and J/kg-K. The absolute enthalpy
and entropy guesses are those EES numbers; they are not the CoolSolve Air
reference state. There is no `abs()` call and no second physical root to reject.
No `coolsolve.conf`.

## Results

| Quantity | CoolSolve | EES stored (SI) | rel. diff. |
|---|---:|---:|---:|
| `COP` [-] | 1.46677 | 1.47004 | 2.23e-03 |
| `q_ut` [J/kg] | 10061.5 | 10043.9 | 1.75e-03 |
| `w_c1` [J/kg] | 6173.66 | 6149.13 | 3.97e-03 |
| `w_c2` [J/kg] | 10061.5 | 10043.9 | 1.75e-03 |
| `w_t` [J/kg] | −10061.5 | −10043.9 | 1.75e-03 |
| `p[1]`, `p[6]`, `p[7]` [Pa] | 100000 | 100000 | 0 |
| `p[2]`, `p[3]` [Pa] | 105889 | 105875 | 1.36e-04 |
| `p[4]`, `p[5]` [Pa] | 116204 | 116168 | 3.06e-04 |
| `T[2]` [°C] | 31.134 | 31.120 | 4.60e-04 |
| `T[4]` [°C] | 34.9965 | 34.9952 | 3.71e-05 |
| `r_p` [-] | 1.16204 | 1.16168 | 3.06e-04 |
| `r_p1` [-] | 1.05889 | 1.05875 | 1.36e-04 |
| `r_p2` [-] | 1.09741 | 1.09723 | 1.70e-04 |
| `r_p_min` [-] | 1.126894391 | 1.126894391 | 3.0e-10 |

`w_c2 = -w_t = q_ut` in both solutions, because ideal-gas enthalpy depends only
on temperature and stations 1, 3 and 5 share that temperature.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot
     (ideal-gas Air; no T-s diagram yet), e.g.  ![COP against pressure ratio](figures/reverse_brayton_intercooling_cop.png)  + one-line caption -->

## Verification

Reference: the solution stored in `THD10_R9_E3.EES` (EES X8.423, 49/49 variables),
compared with `compare_solution.py --ees-units`. The tool's summary line is:

`45 common variables, 21 differ (rtol=0.001); only in EES: 4; only in CoolSolve: 1`

`--ees-units` scaled every stored `kPa` value to Pa and every stored `kJ` value
to J (enthalpies, entropies, `q_ut`, `w_c1`, `w_c2`, `w_t`). Temperatures were
already in °C. `COP` is stored with unit `-`, and `eta_is`, `eta_mec`, `gamma`,
`r_p`, `r_p1`, `r_p2` and `r_p_min` have a blank unit string, so those were not
scaled. They are dimensionless and match. No common variable is stored as
lowercase `kj` or uppercase `KJ`. The model enthalpies are in J because
`enthalpy()` returns J/kg; that is the converted unit, not a missed factor
of 1000.

`verification.max_rel_diff` is the maximum relative difference the tool prints
over all 45 common variables: `3.21e-01` on `s[5]` (unrounded 0.320885).

The 21 variables above rtol 0.001 are the absolute Air properties and the
quantities that inherit the temperature dependence of that offset.

Ideal-gas Air keeps CoolProp's reference state. CoolSolve − EES is
+125843 J/kg to +125889 J/kg on the nine enthalpies (`h[1]` through `h[6]`,
`h_2_is`, `h_4_is`, `h_6_is`), about +126 kJ/kg. CoolSolve − EES is
−1814.89 J/kg-K to −1815.07 J/kg-K on `s[1]` through `s[7]`, about −1815 J/kg-K.
`h[1]`, `h[3]` and `h[5]` share one offset (+125864.67 J/kg at 25 °C).
`s[7]` equals `s[1]`.

The offset is not constant. Between 25 °C and 15 °C it changes by 17.597 J/kg,
which is the whole difference on `q_ut`, `w_c2` and `w_t` (10061.5 J/kg versus
10043.9 J/kg, rel 1.75e-03). Between `T[2]` and 25 °C it changes by 24.529 J/kg,
which is the whole difference on `w_c1` (6173.66 J/kg versus 6149.13 J/kg,
rel 3.97e-03). The COP, \(q_\mathrm{ut}\,\eta_\mathrm{mec}/w_{c1}\), is
1.46677 versus 1.47004 (rel 2.23e-03). Those five residuals are the \(c_p(T)\)
difference between EES and CoolProp, reported separately from the reference
offsets.

Pressures, temperatures and pressure ratios stay inside rtol. The largest
pressure difference is 35.6 Pa on `p[4]` and `p[5]` (rel 3.06e-04). `r_p_min`
matches to 3×10⁻¹⁰.

Only in the EES reference: `h_1`, `h_2`, `P`, `p_2` (see *Model*). Only in
CoolSolve: `fluid$`. The `.sol` writes that string variable as `0`, and
`compare_solution.py` reads the number. The EES csv has no numeric `fluid$`.
The fluid used in the property calls is `Air`.

CoolSolve prints a hint that `t=31.1343` and `t=34.9965` look like Fahrenheit
(it quotes −0.48 °C and 1.66 °C). Those numbers are the solved Celsius values
of `T[2]` and `T[4]`. The solution keeps 31.134 °C and 34.9965 °C. The hint
was not followed. The file names dry `Air`, not `AirH2O`; the fluid was not
changed.

## Source and attribution

The equation window names no person. The EES licence tag is the student and
staff licence of the Laboratoire de Thermodynamique, University of Liège, not
an author. The inventory attributes the MECA0002 course to S. Quoilin.
Repetition assistants N. Paulus and B. Dechesne appear in companion metadata
and are not named in this file, so they are not listed as authors.
Authors: S. Quoilin.

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R8/old/THD10_R9_E3.EES`.

## Conversion log

- **2026-10-15 — import**: `tools/ees_extract.py` on `THD10_R9_E3.EES` (EES X8.423, plain text, decimal commas already rewritten as dots). Unit system `$UnitSystem SI MASS DEG KPA C KJ` deleted; CoolSolve is SI, °C, Pa, J. The only converted input is `p_amb = 100e3` Pa (100 kPa in the original). Property calls are left in Pa and J. Balances are unchanged: every term scales the same way. `r_p_min` keeps the original `+273` and `gamma = 1.4`. No `$TABSTOPS`, `$Export`, `concat$` or `EESFILEDIR$`.
- **2026-10-15 — curation**: comments translated to English (paraphrase of the original). The original wrote `T=t[4]`; EES names are case-insensitive, so the file uses `T[4]`. The closing point `T[7] = T[1] : p[7] = p[1] : s[7] = s[1]` is the same three equations on three lines. The original's quoted alternatives `h_4_is = enthalpy(...)` and `h_6_is = enthalpy(...)` stay as comments; the solved equations are the entropy forms. No diagram-window value was turned into an equation: the system is square without `P`, `p_2`, `h_1` and `h_2`. No extra diagram-state array was added (`h[7]` is not in the equation window). `.initials` converted from the stored solution (pressures ×1000, specific energies and entropies ×1000).
- **Level**: equations 46 (< 50) → 0; largest block 1 (≤ 5) → 0; arrays present → 1; five components of one cycle (two compressors, two coolers, turbine) → 1; no semi-empirical, off-design, part-load or dynamic physics → 0; the same root is reached from default guesses (16 iterations, no `coolsolve.conf`) → 0. Score 2 → level 2.

## Limitations and CoolSolve gaps

The coolers are isobaric, the isentropic efficiencies are constant, and the
mechanical efficiency multiplies only the first-stage fluid work. `gamma = 1.4`
is used only in `r_p_min`. Absolute enthalpy and entropy follow CoolProp's Air
reference, so they are not the EES numbers; differences and the COP carry the
small \(c_p(T)\) residual described above.

No CoolSolve gap blocks the file. `missing_features` is empty. The maintainer's
figure for this ideal-gas cycle is a parametric sweep: CoolSolve has no
ideal-gas diagram yet.

## Related models

The equation window is not the same calculation as another model in the library; the cycle skeleton is shared with:
- `CSL-0254` *recuperated_brayton_hthp*: the same turbomachinery + recuperator skeleton on air run as a high-temperature heat pump (DTU case study, translated from TESPy).
