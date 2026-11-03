# Brayton cycle with 70 MW net power, pressure ratio 12 (Cengel exercise 9-76)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0204`

Cold air-standard Brayton cycle on ideal-gas Air. Specific heats are evaluated
once at state 1 and held constant. The model returns the isentropic and actual
compression and expansion, the heat input, the thermal efficiency and the mass
flow that delivers 70 MW net power.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines and gas cycles |
| **Fluids** | Air (ideal gas) |
| **Size** | 25 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/thermo_kuleuven/exercices/09-76b.EES` (EES X9.920) |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@6730bcf — verified against the EES stored solution (max rel. diff 8.28e-03) |

## Problem statement

Brayton cycle, as written in the equation window (Cengel exercise 9-76). The
original comment says the temperatures are in kelvin.

Data:

- pressure ratio `r_p = 12`
- state 1: `p_1 = 1E5` Pa, `T_1 = 300` K
- state 3: `T_3 = 1000` K
- net power `W_dot_net = 70e6` W
- isentropic efficiencies `eta_cp = 0.85` and `eta_exp = 0.85`

`cp` and `cv` of Air are taken at state 1 and held constant. Compression (1–2)
and expansion (3–4) are written with an isentropic reference state (`T_2s`,
`T_4s`) and the actual work at the given efficiency. The pressures are
`p_2 = p_1*r_p`, `p_3 = p_2` and `p_4 = p_1`. The heat input is
`q_comb = c_p*(T_3 - T_2)`. The original comments that this stands for
`h_3 - h_2`; the equation uses `c_p`. The mass flow follows from
`W_dot_net = m_dot*w_net`.

## Model

Cold air-standard closure, with `k = c_p/c_v` at state 1:

\[
c_p = c_p(T_1),\qquad c_v = c_v(T_1)
\]

CoolSolve property calls take Celsius. `T_1` stays at 300 K, so the calls are
`cp(Air, T=T_1-273.15)` and `cv(Air, T=T_1-273.15)`, which is 26.85 °C.
The original writes `cv(air, t=t_1)`; `t_1` is the same variable as `T_1`.

Isentropic relations, as in the equation window:

\[
\frac{T_1}{T_{2s}} = \left(\frac{p_1}{p_2}\right)^{(k-1)/k},
\qquad
\frac{T_3}{T_{4s}} = \left(\frac{p_3}{p_4}\right)^{(k-1)/k}
\]

\[
\eta_{cp} = \frac{w_{cp,s}}{w_{cp}},
\qquad
\eta_{exp} = \frac{w_{exp}}{w_{exp,s}}
\]

with `w_cp_s = c_p*(T_2s - T_1)`, `w_cp = c_p*(T_2 - T_1)`,
`w_exp_s = c_p*(T_3 - T_4s)` and `w_exp = c_p*(T_3 - T_4)`.

\[
q_{comb} = c_p\,(T_3 - T_2),
\qquad
w_{net} = w_{exp} - w_{cp},
\qquad
\eta = \frac{w_{net}}{q_{comb}},
\qquad
\dot W_{net} = \dot m\, w_{net}
\]

| Quantity | Role | Value |
|---|---|---|
| `r_p` | pressure ratio | 12 |
| `p_1` | pressure at state 1 | 1×10⁵ Pa |
| `T_1` | temperature at state 1 | 300 K |
| `T_3` | temperature at state 3 | 1000 K |
| `W_dot_net` | net power | 70×10⁶ W |
| `eta_cp`, `eta_exp` | isentropic efficiencies | 0.85 |
| `T_2`, `T_4` | temperatures after the actual compression and expansion | solved |
| `T_2s`, `T_4s` | isentropic reference temperatures | solved |
| `q_comb` | heat input | solved [J/kg] |
| `w_cp`, `w_exp`, `w_net` | specific works | solved [J/kg] |
| `eta` | thermal efficiency | solved |
| `m_dot` | mass flow | solved [kg/s] |

Every block has size 1 (25 explicit equations). The system is square
(25 equations, 25 variables).

## How to run

From this folder:

```bash
../../../../../CoolSolve/build/coolsolve ./brayton_cycle_cengel_9_76.eescode
```

`brayton_cycle_cengel_9_76.initials` is the EES stored solution, with
temperatures still in kelvin. It selects that stored root. The file has no
`abs()`. With the initials the solver reports 18 iterations. Without them it
reports 81 iterations and the same solution. No `coolsolve.conf` and no
variant.

## Results

Temperatures below are kelvin. Net power is the given input, 70 MW.
`T_2` is above `T_1` and above `T_2s`. `T_4` is below `T_3` and above `T_4s`.

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `W_dot_net` [W] | 7.000000000×10⁷ | 7.000000000×10⁷ |
| `eta` [-] | 0.1994576574 | 0.2005002327 |
| `m_dot` [kg/s] | 1045.529944 | 1036.874001 |
| `w_net` [J/kg] | 66951.69316 | 67510.61354 |
| `q_comb` [J/kg] | 335668.7031 | 336710.8988 |
| `T_1` [K] | 300 | 300 |
| `T_2` [K] | 666.4572675 | 664.8661072 |
| `T_2s` [K] | 611.4886774 | 610.1361911 |
| `T_3` [K] | 1000 | 1000 |
| `T_4` [K] | 567.0150804 | 567.9394693 |
| `T_4s` [K] | 490.6059770 | 491.6934933 |
| `c_p` [J/kg-K] | 1006.373908 | 1004.7056 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

Ideal-gas cycle: the maintainer's figure is a parametric sweep (for example
`eta` against `r_p`), saved as `figures/brayton_cycle_cengel_9_76_sweep.png`.

## Verification

Reference: the solution stored in `09-76b.EES` (25 values, EES X9.920). The
unit system is `SI MASS DEG PA K J`. Pressures are already in Pa and energies
in J. The comparison does not use `--ees-units`. Temperatures stay in kelvin.

`compare_solution.py` on `brayton_cycle_cengel_9_76.sol` against
`reference/ees_variables.csv`:

> 25 common variables, 14 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0

Maximum relative difference over all common variables, as printed in the tool's
table: **8.28e-03** (`w_net`; `m_dot` prints the same 8.28e-03).

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `w_net` | 67510.6 | 66951.7 | 8.28e-03 |
| `m_dot` | 1036.87 | 1045.53 | 8.28e-03 |
| `w_cp` | 366583 | 368793 | 5.99e-03 |
| `w_cp_s` | 311596 | 313474 | 5.99e-03 |
| `eta` | 0.2005 | 0.199458 | 5.20e-03 |
| `w_exp` | 434094 | 435745 | 3.79e-03 |
| `w_exp_s` | 510698 | 512641 | 3.79e-03 |
| `q_comb` | 336711 | 335669 | 3.10e-03 |
| `T_2` | 664.866 | 666.457 | 2.39e-03 |
| `T_2s` | 610.136 | 611.489 | 2.21e-03 |
| `T_4s` | 491.693 | 490.606 | 2.21e-03 |
| `T_4` | 567.939 | 567.015 | 1.63e-03 |
| `c_p` | 1004.71 | 1006.37 | 1.66e-03 |
| `k` | 1.39994 | 1.40169 | 1.25e-03 |

`c_v` is under the tolerance (717.972 against 717.677, rel. diff 4.11e-04).
`r_p`, `p_1`, `p_2`, `p_3`, `p_4`, `T_1`, `T_3`, `W_dot_net`, `eta_cp` and
`eta_exp` print 0.00e+00. Nothing is only in the EES list or only in the
CoolSolve solution.

The root difference is `cp(Air)` at 26.85 °C, which is `T_1 - 273.15` with
`T_1 = 300` K: CoolProp 1006.374 J/kg-K, EES 1004.706 J/kg-K (1.66e-03).
`k = c_p/c_v` follows it (1.25e-03) because `c_v` is inside the tolerance.
From that `k` and that `c_p`:

- `T_2s` and `T_4s` come from the same exponent `(k-1)/k` and the same
  pressure ratio, both 2.21e-03. `T_2 = T_1 + (T_2s - T_1)/eta_cp` is
  2.39e-03. `T_4 = T_3 - eta_exp*(T_3 - T_4s)` is 1.63e-03.
- `w_cp_s = c_p*(T_2s - T_1)` and `w_cp = w_cp_s/eta_cp` are 5.99e-03.
  `w_exp_s = c_p*(T_3 - T_4s)` and `w_exp = eta_exp*w_exp_s` are 3.79e-03.
- `q_comb = c_p*(T_3 - T_2)` is 3.10e-03.
- `w_net = w_exp - w_cp` is 8.28e-03. Both works are higher than the stored
  values, and the rise in `w_cp` is larger than the rise in `w_exp`, so the
  net work is lower. That subtraction is the largest relative difference.
  `m_dot = W_dot_net/w_net` prints the same 8.28e-03 because `W_dot_net`
  matches. `eta = w_net/q_comb` is 5.20e-03.

Passing `t=T_1` with `T_1 = 300` makes CoolSolve read 300 °C. That run gives
`c_p = 1045.11` J/kg-K, `eta = 0.211269` and `w_net = 78175.3` J/kg, and the
largest relative difference is 1.36e-01 on `w_net` and `m_dot`. The call
therefore receives `T_1 - 273.15` (26.85 °C). CoolSolve's own warning on the
unconverted call says that 300 K is written `T=26.85`.

The equation window does not call `enthalpy`. The usual CoolProp ideal-gas Air
enthalpy offset, about +126 kJ/kg against EES, does not appear. The `c_p` gap
is 1.67 J/kg-K. Work, heat and efficiency differ only through that `c_p` and
the `k` that follows from it.

## Source and attribution

Source file
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/09-76b.EES`
(EES X9.920). The equation window names nobody. The `{$ID$}` tag is the EES
licence of Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege, which is
the licence holder and not an author. The inventory row TM-0347 attributes the
KU Leuven course to S. Quoilin, so `authors` is `["S. Quoilin"]`. Cengel
exercise 9-76 is the textbook problem; the file does not list Cengel as an
author. Published under the library licence (MIT).

## Conversion log

- **2026-10-15 — import** (`ees_extract.py`, card C-230): EES X9.920, plain-text
  equation window, `{$ID$}` and `{$PX$}` removed, no lookup or parametric
  table, 25 stored values, 25 equations. `$UnitSystem SI MASS DEG PA K J`
  removed. Pressures were already in Pa and energies in J, so none of those
  values were rescaled. `T_1 = 300` and `T_3 = 1000` are kept, and the solved
  temperatures are in kelvin. The unmodified extract is square (25 equations,
  25 variables, largest block 1), so no Diagram-window value was restored and
  no computed unknown was replaced by a stored number. The diagram window
  carries the label "compression (1 to 2)" and the line `p_2*V_2 = m*R*T_2`;
  that line is not in the equation window and was not added. No state-point
  arrays were added. The stored solution is the `.initials` file.
- **2026-10-15 — property temperature**: `cp(air, t=T_1)` and `cv(air, t=t_1)`
  are written `cp(Air, T=T_1-273.15)` and `cv(Air, T=T_1-273.15)`. CoolSolve
  reads a temperature argument as °C; with `T_1` left at 300 K the call would
  be evaluated at 300 °C and the stored solution would not match. The fluid
  stays ideal-gas Air. `t_1` in the original is the same variable as `T_1`.
- **Level**: equations 25 (< 50) → 0; largest block 1 (≤ 5) → 0; no function,
  procedure, array or `DUPLICATE` → 0; one cycle, no multi-zone discretisation
  → 0; constant specific heats, no calibration, off-design, part-load or
  dynamics → 0; the same solution is reached without curated guesses → 0.
  Score 0 → **level 1**.

## Limitations and CoolSolve gaps

- Cold air-standard: `c_p` and `c_v` are constant, taken at state 1. The file
  does not treat variable specific heats or a change of composition.
- The heat input is `c_p*(T_3 - T_2)`. The commented form `h_3 - h_2` is not
  a property call.
- CoolSolve warns that moist air should use `AirH2O`. The fluid in the file
  is ideal-gas Air, and it is unchanged.
- No CoolSolve gap blocks this file. `missing_features` is empty.

## Related models

`related` is empty. This equation window is Cengel exercise 9-76. A different
Brayton exercise is a different calculation.
