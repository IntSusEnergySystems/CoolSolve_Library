# Air-standard Otto cycle, compression ratio 9.5 (Cengel exercise 9-37)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0192`

Cold air-standard Otto cycle on ideal-gas Air. Specific heats are evaluated
once at the intake temperature and held constant. The model returns the four
states, the heat added at constant volume, the specific compression and
expansion work, and the thermal efficiency.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal gas) |
| **Size** | 23 equations (largest block: 2) |
| **Source** | `~/Nextcloud/thermo_models/thermo_kuleuven/exercices/9-37.EES` (EES X9.920) |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@3e9c1b6 — verified against the EES stored solution (max rel. diff 6.58e-03) |

## Problem statement

Air-standard Otto cycle, as written in the equation window (Cengel exercise 9-37).

Data:

- compression ratio `r_c = 9.5`
- state 1: `p_1 = 1E5` Pa, `T_1 = 35 + 273.15` K, `V_1 = 600e-6` m³
- state 4: `T_4 = 800` K

`cp` and `cv` of Air are taken at the intake temperature and held constant.
Compression (1–2) and expansion (3–4) are isentropic. Heat addition (2–3) and
heat rejection (4–1) are at constant volume. The file checks the efficiency
against the course formula on slide 10, `1 - 1/r_c^(k-1)`. The original says
the mean effective pressure is not computed.

Solved temperatures are in kelvin: the equation window adds 273.15 to 35, and
`T_4` is the value 800.

## Model

Cold air-standard closure, with `k = c_p/c_v` at state 1:

\[
c_p = c_p(T_1),\qquad c_v = c_v(T_1)
\]

CoolSolve property calls take Celsius. `T_1` stays in kelvin, so the calls are
`cp(Air, T=T_1-273.15)` and `cv(Air, T=T_1-273.15)`, which is 35 °C.

Ideal-gas law at each state, `p V = m R T` with `T` in kelvin and
`R = R#/molarmass(Air)`. Volumes: `V_2 = V_1/r_c`, `V_3 = V_2`, `V_4 = V_1`.

Isentropic relations, as in the equation window:

\[
\frac{T_1}{T_2} = \left(\frac{p_1}{p_2}\right)^{(k-1)/k},
\qquad
\frac{T_3}{T_4} = \left(\frac{p_3}{p_4}\right)^{(k-1)/k}
\]

Heat added and specific work:

\[
Q_\mathrm{comb} = m\, c_v\, (T_3 - T_2),
\qquad
w_\mathrm{cp} = c_v\, (T_2 - T_1),
\qquad
w_\mathrm{exp} = c_v\, (T_3 - T_4)
\]

`Q_dot_comb` is the name in the file. The balance is an energy in J.

\[
\eta = \frac{m\,(w_\mathrm{exp} - w_\mathrm{cp})}{Q_\mathrm{comb}}
= 1 - r_c^{1-k}
\]

The equation window does not name a net-work variable. The net work in the
efficiency is `m*(w_exp - w_cp)` [J]; the specific net work is
`w_exp - w_cp` [J/kg].

| Quantity | Role | Value |
|---|---|---|
| `r_c` | compression ratio | 9.5 |
| `p_1` | pressure at state 1 | 1×10⁵ Pa |
| `T_1` | temperature at state 1 | 308.15 K |
| `V_1` | volume at state 1 | 6×10⁻⁴ m³ |
| `T_4` | temperature at state 4 | 800 K |
| `T_2`, `p_2` | end of compression | solved |
| `T_3`, `p_3` | end of heat addition | solved |
| `p_4` | pressure at state 4 | solved |
| `Q_dot_comb` | heat added | solved [J] |
| `w_cp`, `w_exp` | specific works | solved [J/kg] |
| `eta_otto`, `eta_th_otto` | efficiency from the balance, and the course formula | solved |

Two algebraic blocks of size 2: `(T_2, p_2)` and `(T_3, p_3)`. Every other
equation is explicit. The system is square (23 equations, 23 variables).

## How to run

From this folder:

```bash
../../../../../CoolSolve/build/coolsolve ./otto_cycle_cengel.eescode
```

`otto_cycle_cengel.initials` holds the EES stored solution, with temperatures
still in kelvin. With that file the solver reports 12 iterations. Without it
the compression block `(T_2, p_2)` reaches the iteration limit and does not
return a solution: a negative pressure guess makes `(p_1/p_2)^((k-1)/k)`
undefined, which is the numerical note in the original. No `coolsolve.conf`
and no variant.

## Results

Temperatures below are kelvin. The maximum temperature is `T_3` and the
maximum pressure is `p_3`.

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `eta_otto` [-] | 0.5948715054 | 0.5933727413 |
| `eta_th_otto` [-] | 0.5948715053 | 0.5933725762 |
| `T_3` [K] | 1974.682133 | 1967.403357 |
| `p_3` [Pa] | 6.087775519×10⁶ | 6.065335677×10⁶ |
| `w_exp - w_cp` [J/kg] | 518818.6664 | 515403.5175 |
| `m*(w_exp - w_cp)` [J] | 351.9256458 | 349.6316150 |
| `T_2` [K] | 760.6228739 | 757.818929 |
| `p_2` [Pa] | 2.344935032×10⁶ | 2.336290711×10⁶ |
| `Q_dot_comb` [J] | 591.5994338 | 589.2276316 |
| `c_p` [J/kg-K] | 1006.696305 | 1005.126794 |
| `k` [-] | 1.401347791 | 1.399707374 |

`eta_otto` and `eta_th_otto` agree with each other. State 1 is 308.15 K and
1×10⁵ Pa; state 4 is 800 K.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

Ideal-gas cycle: the maintainer's figure is a parametric sweep (for example
`eta_otto` against `r_c`), saved as `figures/otto_cycle_cengel_sweep.png`.

## Verification

Reference: the solution stored in `9-37.EES` (25 values, EES X9.920). The unit
system is `SI MASS DEG PA K J`. Pressures are already in Pa and energies in J.
The comparison does not use `--ees-units`. Temperatures stay in kelvin, so a
K→°C conversion of the `T` names would move them off the stored values.

`compare_solution.py` on `otto_cycle_cengel.sol` against `reference/ees_variables.csv`:

> 23 common variables, 11 differ (rtol=0.001); only in EES: 2; only in CoolSolve: 1

Maximum relative difference over all common variables, as printed in the tool's
table: **6.58e-03** (`w_cp`; `w_exp` prints the same 6.58e-03).

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `w_cp` | 322906 | 325046 | 6.58e-03 |
| `w_exp` | 838310 | 843865 | 6.58e-03 |
| `Q_dot_comb` | 589.228 | 591.599 | 4.01e-03 |
| `T_2` | 757.819 | 760.623 | 3.69e-03 |
| `p_2` | 2.33629e+06 | 2.34494e+06 | 3.69e-03 |
| `p_3` | 6.06534e+06 | 6.08778e+06 | 3.69e-03 |
| `T_3` | 1967.4 | 1974.68 | 3.69e-03 |
| `eta_th_otto` | 0.593373 | 0.594872 | 2.52e-03 |
| `eta_otto` | 0.593373 | 0.594872 | 2.52e-03 |
| `c_p` | 1005.13 | 1006.7 | 1.56e-03 |
| `k` | 1.39971 | 1.40135 | 1.17e-03 |

`c_v` is under the tolerance (718.377 against 718.098, rel. diff 3.89e-04).
`R` and `m` differ by 6.45e-05, the molar mass of Air. `p_4` is 1.39e-10.
`V_2` and `V_3` are 5.00e-11. `r_c`, `p_1`, `T_1`, `T_4`, `V_1` and `V_4`
print 0.00e+00.

The root difference is `cp(Air)` at 35 °C: CoolProp 1006.696 J/kg-K, EES
1005.127 J/kg-K (1.56e-03). `k = c_p/c_v` follows it (1.17e-03) because `c_v`
is inside the tolerance. From that `k`:

- `eta_th_otto = 1 - 1/r_c^(k-1)` and `eta_otto` (the same cold air-standard
  result) are 2.52e-03.
- The compression block gives `T_2` and `p_2` at 3.69e-03. The expansion block
  gives `T_3` and `p_3` at 3.69e-03.
- `Q_dot_comb = m*c_v*(T_3-T_2)` is 4.01e-03.
- `w_cp = c_v*(T_2-T_1)` and `w_exp = c_v*(T_3-T_4)` are 6.58e-03. The
  temperature change carries the `k` difference, and that is the largest
  relative difference.

No enthalpy is computed, so the usual CoolProp ideal-gas Air enthalpy offset
(about +126 kJ/kg against EES) does not appear. The `c_p` gap is 1.57 J/kg-K.

Names only in the EES list: `cp` (1004.616) and `cv` (717.587). They are not
in the equation window and they are not equal to `c_p` and `c_v`. The name
only in the CoolSolve solution is the built-in `R#`.

Passing `t=T_1` with `T_1 = 308.15` makes CoolSolve read 308.15 °C. That run
gives `c_p = 1046.94` J/kg-K and `eta_otto = 0.573251`, which does not match
the stored solution. The call therefore receives `T_1 - 273.15` (35 °C).
CoolSolve also warns that 35 looks like Fahrenheit and mentions 1.67 °C. The
solved `c_p` is the 35 °C value, 1006.696 J/kg-K, the same number as
`cp(Air, T=35)`.

## Source and attribution

Source file
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/9-37.EES`
(EES X9.920). The equation window names nobody. The `{$ID$}` tag is the EES
licence of Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege, which is
the licence holder and not an author. The inventory row TM-0354 attributes the
KU Leuven course to S. Quoilin, so `authors` is `["S. Quoilin"]`. The file
cites slide 10 of the course and does not name the course. Cengel exercise
9-37 is the textbook problem; the file does not list Cengel as an author.
Published under the library licence (MIT).

## Conversion log

- **2026-10-15 — import** (`ees_extract.py`, card C-218): EES X9.920, plain-text
  equation window, `{$ID$}` and `{$PX$}` removed, no lookup or parametric
  table, 25 stored values, 23 equations. `$UnitSystem SI MASS DEG PA K J`
  removed. Pressures were already in Pa and energies in J, so none of those
  values were rescaled. `T_1 = 35 + 273.15` and `T_4 = 800` are kept, and the
  solved temperatures are in kelvin. The unmodified extract is square, so no
  Diagram-window value was restored and no computed unknown was replaced by a
  stored number. The stored solution is the `.initials` file. `cp` and `cv`
  are in that stored list and not in the equation window; they are not
  equations.
- **2026-10-15 — property temperature**: `cp(air, t=T_1)` and `cv(air, t=T_1)`
  are written `cp(Air, T=T_1-273.15)` and `cv(Air, T=T_1-273.15)`. CoolSolve
  reads a temperature argument as °C; with `T_1` left at 308.15 K the call
  would be evaluated at 308.15 °C and the stored solution would not match.
  The fluid stays ideal-gas Air. The isentropic equations are the ones in the
  equation window. The original's commented assignments `T_2 = 500` and
  `T_3 = 1000` are the guess procedure described in its comment about a
  negative base; they are not active equations and are not a variant. The
  original comment on the compression relation says "Isentropic expansion";
  the pressures rise from state 1 to state 2, so the comment in the file says
  "isentropic relation".
- **Level**: equations 23 (< 50) → 0; largest block 2 (≤ 5) → 0; no function,
  procedure, array or `DUPLICATE` → 0; one cycle, no multi-zone discretisation
  → 0; constant specific heats, no calibration, off-design, part-load or
  dynamics → 0; the compression block does not converge without the stored
  guesses → 1. Score 1 → **level 1**.

## Limitations and CoolSolve gaps

- Cold air-standard: `c_p` and `c_v` are constant, taken at state 1. The file
  does not treat variable specific heats or a change of composition.
- The original does not compute the mean effective pressure. No bore, speed
  or cylinder count is in the equation window.
- CoolSolve warns that moist air should use `AirH2O`. The fluid in the file
  is ideal-gas Air, and it is unchanged.
- The property call at 35 °C draws a warning that the value looks like
  Fahrenheit. The solved `c_p` is the 35 °C result.
- No CoolSolve gap blocks this file. `missing_features` is empty.

## Related models

- `CSL-0049` (*otto_cycle_air_standard*): another air-standard Otto exercise
  (MECA0002), with specific heats that vary from one process to the next.
  This model holds `c_p` and `c_v` at the intake temperature and solves
  Cengel exercise 9-37 (compression ratio 9.5).
