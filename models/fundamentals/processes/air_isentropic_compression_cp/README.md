# Isentropic compression of air: constant cp versus property functions (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0237`

Air is compressed isentropically in a closed system from 100 kPa and 17 °C
to 800 kPa. The model computes the exit temperature and the specific work
twice: with specific heats held at the inlet value, and with the air
property functions at variable heat capacity. Teaching exercise Cengel 7-75
from the KU Leuven `thermo_kuleuven` collection.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Air |
| **Size** | 13 equations (largest block: 1) |
| **Source** | thermo_models, file `07-75.EES` |
| **Authors** | TBD (KU Leuven) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7d66c3b — verified against the EES stored solution (see *Verification*) |

## Problem statement

Air is compressed isentropically in a closed system from 100 kPa and 17 °C
to 800 kPa. The file name and the inventory identify the problem as Cengel
7-75. The equation window asks for the exit temperature and the specific
work in two ways.

The first way holds \(c_p\) at the inlet temperature, so \(k\) is constant,
and uses the isentropic relation written in the window. The original comment
calls that relation an isentropic evolution for a real gas. The specific
work is the closed-system expression \(w = c_v(T_2 - T_1)\).

The second way uses the property functions, which account for a variable
heat capacity. The exit state is at the exit pressure and the inlet entropy,
and the specific work is the change of specific internal energy.

## Model

One compression, as written in the equation window. No diagram-state array
is added.

Constant specific heats, evaluated at the inlet temperature:

\[
c_p = c_p(T_1), \quad c_v = c_p - r, \quad r = R/M, \quad k = c_p/c_v
\]

\[
\frac{T_2 + 273.15}{T_1 + 273.15} = \left(\frac{p_2}{p_1}\right)^{(k-1)/k},
\qquad w = c_v(T_2 - T_1)
\]

\(T_1\) and \(T_2\) stay in °C. The 273.15 terms convert the temperature
ratio to kelvin. Property calls take °C, and \(T_1\) is already in °C.

Variable heat capacity, as in the original:

\[
s_1 = s(T_1, p_1), \quad u_2 = u(p_2, s_1), \quad w_{\mathrm{bis}} = u_2 - u_1
\]

| Input | Value |
|---|---|
| `p_1` | 100 kPa (`100E3` Pa) |
| `T_1` | 17 °C |
| `p_2` | 800 kPa (`800E3` Pa) |

Those three assignments are already equations. The system is square without
any further assignment (13 equations, 13 variables). The diagram-window RTF
is empty. No stored unknown was added.

The window writes `t_1` in `cp` and `entropy`, and `T_1` in the temperature
assignment and in the isentropic relation. CoolSolve treats the two
spellings as one variable. The converted window is square, so both spellings
stay.

`u_1` is `intenergy(Air, T=T_1, P=p_1)`. The call without a pressure is
rejected. For an ideal gas the internal energy does not depend on pressure,
and `p_1` is already in the window. `u_2 = intenergy(Air, P=p_2, s=s_1)` is
the original call and is accepted. The fluid stays `Air`. `cp(Air, t=t_1)`,
`molarmass(Air)` and `R#` are kept.

## How to run

```bash
coolsolve ./air_isentropic_compression_cp.eescode
```

CoolSolve reports 2 iterations with the shipped `.initials` and 3 iterations
without them. There is no `abs()`, so the guesses do not select a root. The
`.initials` file is the EES stored solution with no value rescaled. There is
no `coolsolve.conf` and no runnable variant.

## Results

| Quantity | CoolSolve | EES stored | rel. diff. printed by the tool |
|---|---:|---:|---:|
| `T_2` [°C] | 252.011 | 252.550 | 2.13e-03 |
| `w` [J/kg] | 168974.36 | 168941.99 | 1.92e-04 |
| `w_bis` [J/kg] | 169134.19 | 169561.78 | 2.52e-03 |
| `u_1` [J/kg] | 333135.92 | 207254.46 | 3.78e-01 |
| `u_2` [J/kg] | 502270.11 | 376816.25 | 2.50e-01 |
| `c_p` [J/kg-K] | 1006.055 | 1004.254 | 1.79e-03 |
| `c_v` [J/kg-K] | 719.008 | 717.225 | 2.48e-03 |
| `s_1` [J/kg-K] | 3856.91 | 5671.84 | 3.20e-01 |

`T_2` is 252.011 °C in CoolSolve and 252.550 °C in the stored solution.
The constant-cp work `w` is 168974.36 J/kg against 168941.99 J/kg. The
property-function work `w_bis` is 169134.19 J/kg against 169561.78 J/kg.

The absolute internal energies sit about +126 kJ/kg above the stored
values, and the offset is not the same at the two states: +125881.46 J/kg
on `u_1` and +125453.87 J/kg on `u_2`. The −427.59 J/kg remainder is the
whole of the `w_bis` residual. `s_1` carries a separate entropy offset
(−1814.93 J/kg-K). `w` is reported separately from those absolute internal
energies: it stays inside rtol 0.001.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in `07-75.EES` (EES X9.920, 13 variables),
compared with `compare_solution.py` without `--ees-units`. The tool's
summary line is:

`13 common variables, 7 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 1`

The one name only in CoolSolve is `R#`, the built-in constant in
`r = R#/molarmass(Air)`. It is not an extra unknown: the statistics are
13 equations and 13 variables.

The maximum relative difference over all common variables, as printed by
the tool, is **3.78e-01** on `u_1` (unrounded 0.377868).

Every difference above rtol 0.001:

- `u_1` prints 3.78e-01 and `u_2` prints 2.50e-01. CoolSolve minus the
  stored value is +125881.46 J/kg and +125453.87 J/kg. The offset is about
  +126 kJ/kg and it is not constant.
- `s_1` prints 3.20e-01 (3856.91 against 5671.84 J/kg-K).
- `w_bis` prints 2.52e-03. The equations are satisfied (max relative
  residual 1.23e-16), and the residual is the difference of the two
  internal-energy offsets.
- `c_p` prints 1.79e-03 at 17 °C (1006.055 against 1004.254 J/kg-K).
  `c_v` prints 2.48e-03 and `T_2` prints 2.13e-03, both following that
  `c_p`.

`w` prints 1.92e-04. `k` prints 6.90e-04 and `r` prints 6.45e-05. `p_1`,
`p_2` and `T_1` match.

## Source and attribution

The equation window names nobody. The EES licence tag is the J. Lebrun
laboratory licence (University of Liège) and is not the author. The file is
a Cengel exercise in the `thermo_kuleuven` collection, so the authors field
is TBD (KU Leuven).

Source file (not copied into the library):
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/07-75.EES`.

Candidate TM-0345. No duplicate group. Teaching exercise, not an exam.
EES X9.920. The comments in the equation window are English. The
diagram-window RTF is empty.

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `07-75.EES` (EES X9.920, plain text, 13 variables, no tables, no warnings). Unit system `$UnitSystem SI MASS DEG PA C J`, already pascal, Celsius and joule. No number was rescaled: `p_1 = 100E3`, `T_1 = 17` and `p_2 = 800E3` stay. `$UnitSystem` was deleted. The file contains no `$TABSTOPS` and no `$Export`. `$Export` is not a missing feature and not a variant. The licence tag was not copied. With `$UnitSystem` removed, the window is square: 13 equations, 13 variables, largest block 1. No diagram input and no stored unknown was turned into an equation. The diagram-window RTF is empty. No diagram-state array was added.
- **Case**: the window writes `t_1` and `T_1`. CoolSolve treats them as one variable. The converted window is square, so both spellings stay. They were not unified.
- **Internal energy**: `u_1 = intenergy(Air, t=t_1)` with no pressure is rejected with `Ideal gas property 'intenergy' requires pressure input`. That is the known behaviour CS-BUG-IDEAL-INTENERGY. In the main file the call is `u_1 = intenergy(Air, T=T_1, P=p_1)`. For an ideal gas the internal energy does not depend on pressure, and `p_1` is already in the window. This is not a variant, and CS-BUG-IDEAL-INTENERGY is not listed in `missing_features`. `u_2 = intenergy(Air, P=p_2, s=s_1)` is accepted. `cp(Air, t=t_1)`, `molarmass(Air)` and `R#` stay. The fluid stays `Air`. The moist-air hint on `Air` was not followed. No Fahrenheit hint was printed, and `T_1` stays 17, which matches the stored value.
- **Level**: equations 13 → 0; largest block 1 → 0; no function, procedure, array or `DUPLICATE` → 0; one compression, not discretised → 0; no calibration, off-design or dynamics → 0; converges from the default guess (3 iterations without `.initials`, 2 with the stored solution) → 0. Score 0 → level 1. No ±1 shift.

## Limitations and CoolSolve gaps

The window compares a constant-specific-heat compression with the same
compression evaluated from the air property functions. Absolute internal
energy and entropy follow the CoolProp reference state of ideal-gas `Air`.
The enthalpy-style offset on internal energy against EES is about +126 kJ/kg
and is not constant, so `w_bis` keeps a residual of 427.59 J/kg while the
equations stay satisfied. The constant-cp work `w` stays close to the stored
value.

No CoolSolve gap is listed. The pressure argument on `u_1` is the known
ideal-gas `intenergy` behaviour, written in the main file. There is no
variant.

## Related models

None.
