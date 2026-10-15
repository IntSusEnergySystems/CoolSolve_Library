# Reference pipe model

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0196`

Laboratory reference model of a water pipe, assembled from an elementary adiabatic pressure-drop model and an isobaric heat-gain model. The stored run is one operating point: 1 kg/s of water entering at 6 °C and 200 kPa, in a 50 m pipe.

| | |
|---|---|
| **Category** | Components › Valves, nozzles and piping |
| **Fluids** | Water |
| **Size** | 55 equations (largest block: 1) |
| **Source** | Laboratory reference model JL080103 (2008-01-03) |
| **Authors** | Jean Lebrun |
| **License** | MIT |
| **CoolSolve** | 0.3.0@f5b79cd — verified against the EES stored solution (see *Verification*) |

## Problem statement

The original calls the file a reference pipe model: an assembly of two elementary models, pressure drop (01) and heat gain (02). The control panel holds 3 outputs, 4 inputs and 6 parameters. Given the mass flow rate, the supply pressure and temperature, the environment temperature and the pipe geometry, compute the exit pressure, the exit temperature and the heat gain.

## Model

The pressure-drop model is an adiabatic pipe. The heat-gain model is isobaric and takes the exit pressure and exit temperature of the pressure-drop model as its inlet. The three pipe outputs are those sub-model results, as in the original: `p_ex_pipe = p_ex_pipe_01`, `t_ex_pipe = t_ex_pipe_02`, `Q_dot_pipe = Q_dot_pipe_02`.

Pressure drop, as written in the original. `v_pipe_01` is the specific volume, so `C^2/(2*v)` is `rho*C^2/2`.

- `DELTAp_pipe_01 = lambda_pipe_01*(L_pipe_01/D_hydr_pipe_01)*C_pipe_01^2/(2*v_pipe_01)`
- `1/sqrt(lambda_pipe_01) = -2*log10((epsilon_pipe_01/D_hydr_pipe_01)/3.71 + 2.51/(Re_pipe_01*sqrt(lambda_pipe_01)))`
- `Re_pipe_01 = abs(C_pipe_01)*D_hydr_pipe_01/nu_pipe_01`
- `h_ex_pipe_01 = h_su_pipe_01`, then `t_ex_pipe_01` from that enthalpy and the exit pressure

The friction-factor equation is the Colebrook equation. The original writes it and does not name it.

Heat gain, as written in the original. The overall resistance uses the insulation thickness on the outer insulation area. It has no cylindrical-log term and no conductivity for the pipe wall. The wall thickness enters only the outer diameter, `D_insulation_pipe_02 = D_in_pipe_02 + 2*(e_pipe_02 + e_insulation_pipe_02)`.

- `Q_dot_pipe_02 = epsilon_pipe_02*C_dot_pipe_02*(t_env_pipe_02 - t_su_pipe_02)`
- `epsilon_pipe_02 = 1 - exp(-NTU_pipe_02)`, `NTU_pipe_02 = AU_pipe_02/C_dot_pipe_02`
- `1/AU_pipe_02 = 1/(A_in*h_in) + e_insulation/(A_insulation*k_insulation) + 1/(A_insulation*h_out)`
- `h_in_pipe_02 = 1000` W/(m²·K). The original says it might be calculated from the water speed.
- `h_out_pipe_02 = 10` W/(m²·K). The original says it might also be calculated, combining convection and radiation.
- `Q_dot_pipe_02 = C_dot_pipe_02*(t_ex_pipe_02 - t_su_pipe_02)`

`abs(C_pipe_01)` does not open a second root at this operating point. `C_pipe_01 = V_dot_pipe_01/A_pipe_01` and `V_dot_pipe_01 = M_dot_pipe_01*v_pipe_01`, with `M_dot_pipe = 1` kg/s, so the velocity is positive. The shipped `.initials` are the stored solution, including that positive velocity.

| Inputs | Value | Parameters | Value |
|---|---|---|---|
| `M_dot_pipe` | 1 kg/s | `L_pipe` | 50 m |
| `p_su_pipe` | 200000 Pa | `D_in_pipe` | 0.035 m |
| `t_su_pipe` | 6 °C | `epsilon_pipe` | 0.0001 m |
| `t_env_pipe` | 30 °C | `e_pipe` | 0.005 m |
| | | `e_insulation_pipe` | 0.02 m |
| | | `k_insulation_pipe` | 0.035 W/(m·K) |

These ten values are control-panel inputs restored from the stored solution. `h_in_pipe_02` and `h_out_pipe_02` are already equations in the original.

## How to run

```bash
coolsolve ./reference_pipe.eescode
```

The sibling `.initials` holds the EES stored values. With that file the solve takes 8 iterations. Without it the solve still converges, in 122 iterations, on the same root. Every block has size 1. The friction factor is one implicit unknown.

## Results

The stored operating point. The EES column is the value stored in the file.

| Quantity | CoolSolve | EES |
|---|---:|---:|
| `DELTAp_pipe_01` | 23439.81082 Pa | 23440.45337 Pa |
| `p_ex_pipe` | 176560.1892 Pa | 176559.5466 Pa |
| `Q_dot_pipe` | 474.3061201 W | 474.3041201 W |
| `t_ex_pipe` | 6.118393565 °C | 6.118581062 °C |
| `c_p_pipe_02` | 4202.424522 J/(kg·K) | 4195.960667 J/(kg·K) |
| `C_dot_pipe_02` | 4202.424522 W/K | 4195.960667 W/K |
| `NTU_pipe_02` | 0.004714884336 | 0.004722147588 |
| `epsilon_pipe_02` | 0.004703786717 | 0.004711015778 |
| `AU_pipe_02` | 19.81394555 W/K | 19.81394555 W/K |
| `t_ex_pipe_01` | 6.005528689 °C | (see verification) |

Pressure falls along the pipe. The water warms slightly toward the environment temperature. The heat gain is about 474 W.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py` against the stored solution of `Reference pipe model JL080103.EES`. No `--ees-units` conversion: the file is already `SI MASS DEG PA C J`, and no stored unit string is kPa or kJ.

> 54 common variables, 4 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 2

The maximum relative difference over all 54 common variables is **1.538e-03**, on `c_p_pipe_02` (the same ratio on `C_dot_pipe_02`). The tool prints that difference as 1.54e-03.

`Cp(Water)` at the heat-gain inlet is 4202.424522 J/(kg·K). The file stores 4195.960667 J/(kg·K). That is the water specific heat of CoolProp against the value stored by EES, at the same temperature and pressure. The other three variables above rtol = 0.001 follow from it, and from nothing else:

- `M_dot_pipe_02 = 1` kg/s, so `C_dot_pipe_02` has the same relative difference.
- `AU_pipe_02` matches the stored 19.81394555 W/K, so `NTU_pipe_02 = AU/C_dot` moves by the same ratio (1.538e-03).
- `epsilon_pipe_02 = 1 - exp(-NTU)` then differs by 1.535e-03.

`Q_dot_pipe` stays at 474.3061201 W against 474.3041201 W (relative difference 4.22e-06): the rise in the capacity rate cancels the drop in effectiveness. `t_ex_pipe` is 6.118393565 °C against 6.118581062 °C (3.06e-05). `DELTAp_pipe_01` is 23439.81082 Pa against 23440.45337 Pa (2.74e-05). The viscosity difference is 4.75e-04, under the tolerance, and it is what moves the Reynolds number and the friction factor.

The stored specific enthalpy has a blank unit string. The value 25417.30434 is already in J/kg (about 25.4 kJ/kg for liquid water near 6 °C). CoolSolve returns 25421.65865 J/kg, relative difference 1.71e-04. That is not a unit error, and `--ees-units` would not scale it.

Only in CoolSolve: `pi`, and `t_ex_pipe_01`. The adiabatic-exit temperature is an equation of the original and is not in the extracted variable list. It equals `t_su_pipe_02`, which is compared (EES 6.005542795 °C, CoolSolve 6.005528689 °C).

The `.sol` file labels `v_pipe_01` as kg/m³. The number is the specific volume in m³/kg (0.001000008841), and it agrees with the stored 0.0009999780937.

Along the pipe the pressure falls and the exit temperature lies between the supply temperature and the environment temperature.

## Source and attribution

The file itself names nobody. The inventory attributes JL080103 to Jean Lebrun. The file name is `Reference pipe model JL080103.EES` (initials and the date 2008-01-03). The EES licence stamp is `{$ID$ #1206: Jean Lebrun, Laboratoire de Thermodynamique, Univ. Liege}`; that tag is not an author by itself. EES X7.966.

The equation window does not cite a report. Its comments are the assembly of the two elementary models, the control-panel list, and the two notes that the convection coefficients might be calculated.

Source: `~/Nextcloud/thermo_models/modeles/Pipe/Reference pipe model JL080103.EES` (inventory `TM-0318`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): equations stored as plain text; unit system already `SI MASS DEG PA C J`, so no value was converted; `$UnitSystem` removed; licence tag removed; no lookup or parametric table; no warning in the extract report. No `$Export`, `concat$`, `EESFILEDIR$` or `$TABSTOPS` line was present.
- **Unmodified extract.** With the control-panel values left unset: 45 equations, 55 variables, `System square: No`.
- **Control-panel inputs restored as equations.** The original says the 4 inputs and 6 parameters are given in the control panel, and those ten names are used and never assigned: `M_dot_pipe = 1` kg/s, `p_su_pipe = 200000` Pa, `t_su_pipe = 6` °C, `t_env_pipe = 30` °C, `L_pipe = 50` m, `D_in_pipe = 0.035` m, `epsilon_pipe = 0.0001` m, `e_pipe = 0.005` m, `e_insulation_pipe = 0.02` m, `k_insulation_pipe = 0.035` W/(m·K). Computed unknowns were not replaced by stored numbers (those stay in `.initials`). With the ten assignments the system is square: 55 equations, 55 variables, largest block 1.
- **Fluid name.** The original writes both `water` and `Water`. The calls use `Water`. EES treats the two spellings as the same fluid.
- **Enthalpy unit.** The stored enthalpy is already in J/kg. It was not rescaled.
- The variable-information table also holds names that are not in the equation window (CO2 fractions, leakage, and a fragment "Annexe 43"). No sentence of a report is in the equation window, so none is copied here. Those names are not equations of this model.
- Comments are short English trailing comments. The original section titles are kept. No equation of either elementary model was rewritten.
- **Level**: 55 equations (1), largest block 1 (0), no procedure or array (0), two elementary models, which is not three coupled components (0), no calibration, off-design sweep or dynamics (0), and the stored root is reached without curated guesses (0) → score 1 → level 1.

## Limitations and CoolSolve gaps

The internal and external coefficients are the fixed numbers of the original. One operating point is stored. The same equations accept another mass flow or another geometry. The heat-transfer resistance is the expression written in the file.

No CoolSolve gap. The file uses assignments, `abs`, `log10`, `exp`, `sqrt` and water property calls.

## Related models

None. `CSL-0170` (`return_duct_simplified`) is a curve-fit return duct. Its equations are not this pipe closure, so it is not listed in `related`.
