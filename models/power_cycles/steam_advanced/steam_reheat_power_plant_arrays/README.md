# Steam reheat power plant with T-s arrays (Cengel exercise 10-34b)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0208`

Steady reheat Rankine cycle on water, the array form of the 80 MW exercise.
Saturated liquid is pumped, heated, expanded, reheated once and expanded
again. Saturation states at the high pressure and at the condenser pressure
are evaluated so the `T[i]` and `s[i]` arrays can trace the cycle on a T-s
diagram. The net power is imposed; the model returns the thermal efficiency
and the steam mass flow.

| | |
|---|---|
| **Category** | Cycles and machines › Steam power cycles |
| **Fluids** | Water |
| **Size** | 74 equations (largest block: 1) |
| **Source** | KU Leuven thermodynamics exercise, file `10-34b.EES` (Cengel exercise 10-34b) |
| **Authors** | S. Quoilin — the file itself names nobody |
| **License** | MIT |
| **CoolSolve** | 0.3.0@5a522f7 — verified against the EES stored solution |

## Problem statement

Textbook exercise Cengel 10-34b, as solved in the source file: the extended
array form of the 80 MW reheat Rankine cycle. A steam power plant delivers a
net power of 80 MW. At the pump inlet the water is saturated liquid at 10 kPa.
The pump (isentropic efficiency 0.95) discharges at 10 MPa. Steam enters the
high-pressure turbine at 10 MPa and 500 °C, expands to 1 MPa (isentropic
efficiency 0.80), is reheated to 500 °C at that pressure, and expands to
10 kPa at the same isentropic efficiency. Determine the thermal efficiency
and the steam mass flow.

The equation window also evaluates the saturated liquid and saturated vapour
at 10 MPa (points 3 and 4) and the saturated vapour at 10 kPa (point 9), and
copies temperatures and entropies into `T[1..10]` and `s[1..10]`, with index
10 equal to point 1. Points 3, 4 and 9 do not appear in `w_net` or `q_in`.

## Model

Steady flow. Kinetic and potential energy are absent from the original
equations. One turbine efficiency is used for both stages. Pressures are
equal along the high-pressure line (`p_2 = p_3 = p_4 = p_5`) and across the
reheat connection (`p_6 = p_7`). The low-pressure turbine and the condenser
saturation states sit at `p_1`.

- **Pump inlet (1):** \(x_1 = 0\), \(p_1 = 10\,\mathrm{kPa}\).
- **Pump (1 → 2):** \(p_2 = p_5\) and \(\eta_\mathrm{pump} = (h_{2s} - h_1)/(h_2 - h_1)\) with \(s_{2s} = s_1\).
- **Saturation at the high pressure (3, 4):** \(x_3 = 0\), \(x_4 = 1\), \(T_4 = T_3\). Diagram states; not used in the cycle balances.
- **High-pressure turbine inlet (5):** \(T_5 = 500\,^\circ\mathrm{C}\), \(p_5 = 10\,\mathrm{MPa}\).
- **High-pressure turbine (5 → 6):** \(\eta_\mathrm{tur} = (h_5 - h_6)/(h_5 - h_{6s})\), \(p_6 = p_7 = 1\,\mathrm{MPa}\).
- **Reheat (6 → 7):** heat addition to \(T_7 = 500\,^\circ\mathrm{C}\) at \(p_7\).
- **Low-pressure turbine (7 → 8):** the same \(\eta_\mathrm{tur}\), exit at \(p_8 = p_1\). `x_8 = quality(Water, h=h_8, p=p_8)` is computed and used nowhere else.
- **Saturation at the condenser pressure (9):** \(x_9 = 1\), \(p_9 = p_1\).
- **Cycle:** \(w_\mathrm{net} = w_\mathrm{hp} + w_\mathrm{lp} - w_\mathrm{pump}\), \(q_\mathrm{in} = (h_5 - h_2) + (h_7 - h_6)\), \(\eta = w_\mathrm{net}/q_\mathrm{in}\), \(\dot W_\mathrm{net} = \dot m\, w_\mathrm{net}\).
- **Arrays:** `T[i]` and `s[i]` for i = 1..9 copy the state of the same index; `T[10] = T_1` and `s[10] = s_1`.

| Inputs | Value | Outputs | CoolSolve |
|---|---|---|---|
| `W_dot_net` | 80 MW | `eta_cycle` | 0.3405 |
| `p_5`, `T_5` | 10 MPa, 500 °C | `M_dot` | 62.65 kg/s |
| `p_7`, `T_7` | 1 MPa, 500 °C | `w_net` | 1.277 MJ/kg |
| `eta_tur` | 0.80 | `q_in` | 3.750 MJ/kg |
| `eta_pump` | 0.95 | `T_6` | 231.6 °C |
| `p_1`, `x_1` | 10 kPa, 0 | `T_8` | 88.08 °C |

## How to run

Open `steam_reheat_power_plant_arrays.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./steam_reheat_power_plant_arrays.eescode
```

The system is square: 74 equations, 74 variables, 74 blocks of size 1. The
turbine and pump efficiencies are linear in the unknown outlet enthalpy, so
there is one root. Without `.initials` CoolSolve reaches that root in 112
iterations. The shipped `.initials` are the stored EES solution, including
`x_1 = 0` and `x_3 = 0`, and bring the iteration count to 9.

CoolSolve prints a warning that `t=500` is read as 500 °C. That is the
temperature in the exercise; the value is not a kelvin figure.

The `T[i]` and `s[i]` arrays are the ones in the equation window. They are
the columns for a T-s diagram (CoolSolve *Diagrams* tab, fluid Water, *Array
overlay*, X = `s`, Y = `T`, *Close loop*).

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| Net power `W_dot_net` | 80 MW | 80 MW |
| Thermal efficiency `eta_cycle` | 0.340522 | 0.340540 |
| Steam flow `M_dot` | 62.651 kg/s | 62.661 kg/s |
| Net specific work `w_net` | 1.27691 MJ/kg | 1.27672 MJ/kg |
| Heat input `q_in` | 3.74986 MJ/kg | 3.74911 MJ/kg |
| Reheat state `T_7`, `p_7` | 500 °C, 1 MPa | 500 °C, 1 MPa |
| Reheat enthalpy `h_7` | 3.47910 MJ/kg | 3.47855 MJ/kg |
| HP turbine exit `T_6` | 231.583 °C | 231.709 °C |
| LP turbine exit `T_8` | 88.084 °C | 88.055 °C |
| Exit quality `x_8` | 0 | 100 |

`T_8` is above the condenser saturation temperature (`T_9` = 45.81 °C) and
`h_8` is above the saturated-vapour enthalpy `h_9`, so state 8 is superheated
vapour. The stored EES quality of that state is the sentinel 100.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the cycle,
     figures/steam_reheat_power_plant_arrays_ts.png -->

## Verification

Compared with the solution stored in `10-34b.EES` (`compare_solution.py`,
no `--ees-units`):

`74 common variables, 1 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0`

The only variable above rtol 0.001 is `x_8`: EES stores 100 and CoolSolve
returns 0 (relative difference 1.00e+00, the maximum the tool prints over all
74 common variables). That is the EES `quality()` sentinel for superheated
vapour (`CS-GAP-QUALITY-DOME`). `x_8` is assigned from `quality()` and feeds
no other equation, so the cycle results do not depend on it.

Every other common variable is within 5.60e-04 relative. The largest of those
is `h_3` (saturated liquid at 10 MPa). Water enthalpy residuals are property
differences between CoolProp and EES, not a constant reference-state shift
and not a kJ value left unscaled: about −28 J/kg on the liquid enthalpies
`h_1` and `h_2`, and +101 to +1129 J/kg on the vapour and saturation
enthalpies. The largest absolute residual is `h_5`, +1129 J/kg
(3.37513 MJ/kg against 3.37400 MJ/kg). Entropies stay within 4.57e-04.
The units column of `ees_variables.csv` is blank, and the stored enthalpies
are already in J (`h_1` ≈ 1.918×10⁵), so `--ees-units` was not used. A blank
or `kj`/`KJ` unit string would not scale those values either.

The energy balances hold in the solution: `w_hp + w_lp - w_pump - w_net` is
about −1.3×10⁻⁷ J/kg, `eta_cycle * q_in - w_net` is about −3.7×10⁻⁷ J/kg, and
`W_dot_net - M_dot * w_net` is about −9×10⁻⁶ W. Orders of magnitude match a
reheat Rankine plant: efficiency near 0.34, condenser saturation near 46 °C,
HP exit near 232 °C, LP exit superheated near 88 °C.

## Source and attribution

The file itself names nobody. The `{$ID$}` tag is the EES licence holder
(Jean Lebrun, University of Liège) and is not an author. The inventory
attributes the course to S. Quoilin (KU Leuven), so the author is S. Quoilin.

Source file (EES X9.920), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermo_kuleuven/exercices/10-34b.EES`
(inventory candidate `TM-0349`).

## Conversion log

- **2026-10-15 — import** (`tools/ees_extract.py`): unit system already
  `SI MASS DEG PA C J`. `$UnitSystem` was deleted. No kPa or kJ figure was
  converted by hand, and `compare_solution.py` was run without `--ees-units`.
  The source writes the fluid as `water`; the file uses `Water` (the name is
  case-insensitive). The temperature call at point 1 wrote `P_1`; that is the
  same variable as `p_1`, and it is written `p_1`. The system is square
  (74 equations, 74 variables), so no diagram-window input was turned into
  an equation. The equation-window arrays `T[1..10]` and `s[1..10]` are kept;
  no `P[i]` or `h[i]` arrays were added. Comments translated to English
  (the original section titles were already English labels). The extractor
  writes the EES default guess 1 when a stored value is 0; the shipped
  `.initials` restore the stored `x_1 = 0` and `x_3 = 0`, and keep the stored
  `x_8 = 100`. No `$Export`, `concat$`, `EESFILEDIR$` or `$TABSTOPS` lines
  were present.
- **Level**: equations 74 → 1; largest block 1 → 0; arrays present → 1;
  not multi-zone or discretised (sequential explicit states) → 0; constant
  efficiencies at one design point → 0; converges from default guesses in
  112 iterations → 0. Score 2 → level 2.

## Limitations and CoolSolve gaps

Constant isentropic efficiencies, one reheat, and no kinetic or potential
energy. The condenser heat rejection is not an output of the equation window.
`x_8` loses the EES superheat sentinel (`CS-GAP-QUALITY-DOME`: CoolSolve
returns 0 where EES stores 100). The value feeds no equation, so the gap
does not block the file and is not listed in `missing_features`.

## Related models

`CSL-0191` (Steam power plant with reheat, Cengel exercise 10-34): the same
80 MW reheat cycle without the saturation states at points 3, 4 and 9 and
without the `T[i]`, `s[i]` arrays. State numbers differ. The equations of
that model are not copied here.
