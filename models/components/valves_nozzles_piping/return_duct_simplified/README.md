# Simplified return duct model

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0170`

Curve fit of a return duct from the ULiège model bank. The pressure drop
and the mass, temperature and humidity effectiveness are power laws of
the exit mass flow. With no condensation the humidity effectiveness
equals the mass effectiveness, as written in the original.

| | |
|---|---|
| **Category** | Components › Valves, nozzles and piping |
| **Fluids** | none (the humidity ratio `W` is an algebraic variable) |
| **Size** | 25 equations (largest block: 1) |
| **Source** | ULiège model bank, simplified return duct model (2008-03-17) |
| **Authors** | Jean Lebrun |
| **License** | MIT |
| **CoolSolve** | 0.3.0@b3c0d78 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Given the exit mass flow rate, the supply pressure, temperature and
humidity ratio, the environment temperature and humidity ratio, and the
nominal values of the curve fit, compute the pressure drop, the exit
state and the supply mass flow rate. The stored run is one operating
point of that fit, at half the nominal exit mass flow.

## Model

The original comments call the power laws "curve fit results" and the
ratios "Output of the parametric study".

- `M\M_ex_duct_n = M_dot_ex_duct/M_dot_ex_duct_n`, with `M_dot_ex_duct_n = 1` kg/s.
- Pressure drop, as in the original: `DELTAp\DELTAp_duct_n = M\M_ex_duct_n^1.89`, and `DELTAp_duct = (DELTAp\DELTAp_duct_n)·DELTAp_duct_n`.
- Exit pressure `p_ex_duct = p_su_duct − DELTAp_duct`.
- Mass effectiveness `epsilon\epsilon_M_duct_n = M\M_ex_duct_n^0.26`, with `epsilon_M_duct = abs(M_dot_leakage_duct/M_dot_ex_duct)` and `M_dot_leakage_duct = M_dot_su_duct − M_dot_ex_duct`.
- Temperature effectiveness `epsilon\epsilon_t_duct_n = M\M_ex_duct_n^(−0.44)`, with `epsilon_t_duct = (t_ex_duct − t_su_duct)/(t_env_duct − t_su_duct)`.
- Humidity: `epsilon_W_duct = epsilon_M_duct` ("if no condensation"), and `epsilon_W_duct = (W_ex_duct − W_su_duct)/(W_env_duct − W_su_duct)`.
- `epsilon_w_duct_n = epsilon_M_duct_n`, as in the original. `epsilon_w_duct` in the ratio `epsilon\epsilon_w_duct_n` is the same variable as `epsilon_W_duct`.

The absolute value does not fix the sign of `M_dot_leakage_duct`. Both signs satisfy the equations. The stored solution is the negative one (`M_dot_su_duct` below `M_dot_ex_duct`).

| Inputs (default run, stored solution) | Value | Nominal values | Value |
|---|---|---|---|
| `M_dot_ex_duct` exit mass flow rate | 0.5 kg/s | `M_dot_ex_duct_n` | 1 kg/s |
| `p_su_duct` supply pressure | 100000 Pa | `DELTAp_duct_n` | 234.2 Pa |
| `t_su_duct` supply temperature | 20 °C | `epsilon_M_duct_n` | 0.1908 |
| `W_su_duct` supply humidity ratio | 0.01 kg/kg | `epsilon_t_duct_n` | 0.3192 |
| `t_env_duct` environment temperature | 10 °C | `epsilon_w_duct_n` | `epsilon_M_duct_n` |
| `W_env_duct` environment humidity ratio | 0.005 kg/kg | | |

`M_dot_ex_duct_n = 1` kg/s is an equation of the original. The other nominals, and the six boundary values, are Diagram-window inputs restored from the stored solution (see the conversion log).

## How to run

```bash
coolsolve ./return_duct_simplified.eescode
```

The sibling `.initials` holds the EES stored values, including the negative leakage. With that file the solve takes 7 iterations and reproduces the stored solution. Without it the solve still converges, in 14 iterations, on the positive leakage: `M_dot_leakage_duct = +0.07966738751` kg/s and `M_dot_su_duct = 0.5796673875` kg/s. Every block has size 1.

## Results

The stored operating point. The EES column is the value stored in the file.

| Quantity | CoolSolve | EES |
|---|---:|---:|
| `DELTAp_duct` | 63.18881325 Pa | 63.18881325 Pa |
| `p_ex_duct` | 99936.81118675 Pa | 99936.81119 Pa |
| `M_dot_leakage_duct` | −0.07966738751 kg/s | −0.07966738751 kg/s |
| `M_dot_su_duct` | 0.4203326125 kg/s | 0.4203326125 kg/s |
| `t_ex_duct` | 15.66971899 °C | 15.66971899 °C |
| `W_ex_duct` | 0.009203326125 kg/kg | 0.009203326125 kg/kg |
| `epsilon_M_duct` | 0.159334775 | 0.159334775 |
| `epsilon_t_duct` | 0.4330281013 | 0.4330281013 |
| `epsilon_W_duct` | 0.159334775 | 0.159334775 |
| `M\M_ex_duct_n` | 0.5 | 0.5 |

`p_ex_duct` is `100000 − 63.18881325`. The file stores that pressure as 99936.81119.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against the stored solution. Five ratio names that contain a backslash are missing from the `ees_extract` CSV (its variable-name pattern does not allow `\`); they were read from the variable-information records and added to the comparison. `epsilon\epsilon_t_duct_n` is among them: its record does not use the usual format byte, and its stored value is 1.356604327447672.

> 25 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0

No variable differs above rtol = 0.001. The maximum relative difference over the 25 common variables is **1.69e-10** (`epsilon\epsilon_w_duct_n`).

That ratio is stored as 0.8350879194283695, which is `0.5^0.26`. CoolSolve returns 0.8350879192872, which is the stored `epsilon_M_duct` 0.159334775 divided by 0.1908. Those two stored numbers differ by this relative amount: `0.159334775/0.1908` is not `0.5^0.26`. Started from the stored values, CoolSolve stops at a maximum equation residual of 3.0000e-10 (solution check: 25 satisfied, 0 violated). At rtol = 0 the tool also lists `p_ex_duct` at 3.25e-11; the stored pressure is 99936.81119 and `100000 − 63.18881325` is 99936.81118675. The same rounding shows on `epsilon\epsilon_t_duct_n` (2.42e-13), `epsilon\epsilon_M_duct_n` (3.67e-14) and `DELTAp\DELTAp_duct_n` (2.53e-14).

Along the duct the pressure falls (`DELTAp_duct` = 63.18881325 Pa). `t_ex_duct` lies between `t_su_duct` and `t_env_duct`, and `W_ex_duct` lies between `W_su_duct` and `W_env_duct`.

## Source and attribution

Jean Lebrun, University of Liège, Thermodynamics Laboratory, 17 March 2008. The file name is `JL080317` (initials and date). The equation window is titled "Simplified return duct model JL080317". EES licence stamp: Jean Lebrun, Laboratoire de Thermodynamique, Université de Liège (`{$ID$ #1206}`), EES X7.888.

The equation window does not name a project or a report. The comments in the file are "Simplified model", "Output of the parametric study", "curve fit results" and "(if no condensation)".

Source:
`~/Nextcloud/thermo_models/Model data bank/Distribution_Systems/Ducts/Return_Duct_Simplified_Model_JL080317.zip!/Return_Duct_Simplified_EES_Model_JL080317.EES`
(inventory `TM-0483`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py` on the unzipped `.EES` member only): equations stored as plain text; unit system already `SI MASS DEG PA C J`, so no value was converted; `$UnitSystem` removed; licence tag removed; no lookup or parametric table; no warning in the extract report. The zip also contains an EXE, which was not copied.
- **Unmodified extract.** With the Diagram strings left as comments: 15 equations, 25 variables, `System square: No`.
- **Diagram-window inputs restored as equations.** Quoted strings in the equation window: `DELTAp_duct_n = 234.2` Pa, `epsilon_M_duct_n = 0.1908`, `epsilon_t_duct_n = 0.3192`, and `epsilon_w_duct_n = epsilon_M_duct_n`. Six further variables are used and never assigned: `M_dot_ex_duct = 0.5` kg/s, `p_su_duct = 100000` Pa, `t_su_duct = 20` °C, `W_su_duct = 0.01`, `t_env_duct = 10` °C, `W_env_duct = 0.005`. Their variable-information records carry the same input mark as the four quoted strings, and the Diagram window has an Inputs group displaying 0.5, 100000, 20, 0.01, 100000, 10 and 0.005. The curve-fit equations are unchanged, so computed unknowns are not replaced by stored numbers (those stay in `.initials`). With the ten assignments the system is square: 25 equations, 25 variables.
- **Names containing `\`).** `M\M_ex_duct_n`, `DELTAp\DELTAp_duct_n`, `epsilon\epsilon_M_duct_n`, `epsilon\epsilon_t_duct_n` and `epsilon\epsilon_w_duct_n` are kept. CoolSolve accepts a backslash between two parts of a name. `ees_extract.py` did not write them to `ees_variables.csv`.
- **Unit labels.** Temperatures are annotated `[°C]`, pressures `[Pa]`, mass flows `[kg/s]`, humidity ratios `[kg/kg]`. The original annotates only `M_dot_ex_duct_n` as `[kg/s]`, `DELTAp_duct_n` as `[Pa]` and the two effectiveness nominals as `[-]`. The numbers are the same.
- The variable-information table also holds names of a longer duct calculation (friction factor, leakage geometry, `AirH2O` enthalpies). Those names are not in the equation window, so they are not equations of this model.
- Comments are short English trailing comments. The original section titles are kept. No equation of the curve fit was rewritten.
- **Level**: 25 equations (0), largest block 1 (0), no procedure or array (0), one component (0), the pressure drop and the effectiveness are power-law curve fits of the flow rate, so the off-design criterion scores 1, and the stored negative leakage is reached only from the shipped `.initials` (the default guesses converge on the other root of `abs`), so the numerics criterion scores 1 → score 2 → level 2.

## Limitations and CoolSolve gaps

The nominal coefficients are fixed numbers. One operating point is stored; the same equations accept another exit mass flow. The humidity closure is the original statement `epsilon_W_duct = epsilon_M_duct` under "if no condensation". The model does not call a humid-air property function. `abs` leaves the sign of `M_dot_leakage_duct` to the guess.

No CoolSolve gap. The file uses assignments, `abs` and powers, including names that contain `\`.

## Related models

- `CSL-0311` (*return_duct_paramid*): the reference duct model (pressure drop,
  leakage, heat gain) that generated the parametric study whose curve fits are
  the equations of this simplified model; its normalized ratios carry the same
  names with the `\n` suffix.
