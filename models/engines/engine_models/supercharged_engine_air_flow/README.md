# Supercharged engine air flow and compressor

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0221`

Teaching exercise (ULiège MCI, sixth exercise session, statement 1): air
mass flow of a supercharged six-cylinder four-stroke engine, then the
turbocharger compressor and the intercooler. The volumetric efficiency is
defined on the ambient density, so the given value is greater than one. The
same flow referred to the cylinder-inlet density is an order-of-magnitude
check. The compressor uses a given isentropic efficiency. Pressure losses
between the compressor outlet and the cylinder inlet are neglected.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | Air (ideal gas) |
| **Size** | 29 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP6/EX1_PNG_2019.EES` (EES X10.589) |
| **Authors** | P. Ngendakumana |
| **License** | MIT |
| **CoolSolve** | 0.3.0@332d95a — verified against the EES stored solution (max rel. diff 0.31853 on the Air entropy) |

## Problem statement

Sixth exercise session, statement 1. The window heading is
`PNG17042016`: initials plus a date, not a full name.

Data, as written in the file:

- total displacement `V_tot = 4.8e-3` m³
- `n_c = 6` cylinders
- intermittency factor `i = 0.5` for a four-stroke engine
- rotational speed `N = 3500` 1/min (the original says rpm)
- volumetric efficiency `epsilon_v = 1.58`, defined on the ambient conditions
- isentropic efficiency of the compressor `epsilon_s_cp = 0.92`
- ambient air `T_amb = 23` °C, `p_amb = 98e3` Pa
- cylinder inlet `T_su_cyl = 65` °C, `p_su_cyl = 180e3` Pa

`epsilon_v` is greater than 1 because the original defines it on the ambient
density while the cylinder is supercharged (`p_su_cyl` is 180 kPa and
`p_amb` is 98 kPa). The value is the given data.

The air mass flow follows from that definition. `epsilon_v_bis` is the same
flow referred to the density at the cylinder inlet, written as an
order-of-magnitude check. The turbocharger compressor takes ambient air to
the cylinder-inlet pressure. The intercooler cooling rate is the air enthalpy
change from the compressor outlet to the cylinder inlet.

## Model

Swept volume of one cylinder and air mass flow. `rho_a` is
`Density(Air, T=T_amb, P=P_amb)`. The assignment is `p_amb`; the property
call writes `P_amb`. The two spellings are one variable.

\[
V_s = V_{tot}/n_c, \qquad
\dot{M}_a = \epsilon_v \, \rho_a \, V_s \, (N/60) \, n_c \, i
\]

Order-of-magnitude check, with `rho_a_bis = Density(Air, T=T_su_cyl, P=P_su_cyl)`:

\[
\epsilon_{v,\mathrm{bis}} = \dot{M}_a / \big(\rho_{a,\mathrm{bis}} \, V_s \, (N/60) \, n_c \, i\big)
\]

Turbocharger compressor. Inlet state from the ambient air. Outlet pressure
equal to the cylinder inlet, because pressure losses in the intercooler and
the intake manifolds are neglected, as in the original.

\[
T_{su,cp} = T_{amb}, \quad p_{su,cp} = p_{amb}, \quad p_{ex,cp} = p_{su,cyl}
\]

\[
s_{ex,cp,s} = s_{su,cp}, \qquad
\epsilon_{s,cp} = \frac{h_{ex,cp,s} - h_{su,cp}}{h_{ex,cp} - h_{su,cp}}
\]

\[
w_{cp} = h_{ex,cp} - h_{su,cp}, \qquad \dot{W}_{cp} = \dot{M}_a \, w_{cp}
\]

`T_ex_cp` is `temperature(AIR, h=h_ex_cp)`, written in the original for an
order of magnitude. `T_ex_cp_s` is the isentropic outlet temperature.

Intercooler, as written (the air enthalpy falls, so the rate is negative):

\[
\dot{Q}_{ic} = \dot{M}_a \, (h_{su,cyl} - h_{ex,cp})
\]

| Quantity | Role | Value |
|---|---|---|
| `V_tot` | total displacement | 4.8×10⁻³ m³ |
| `n_c` | number of cylinders | 6 |
| `i` | intermittency factor | 0.5 |
| `N` | rotational speed | 3500 1/min |
| `epsilon_v` | volumetric efficiency on ambient density | 1.58 |
| `epsilon_s_cp` | compressor isentropic efficiency | 0.92 |
| `T_amb`, `p_amb` | ambient air | 23 °C, 98000 Pa |
| `T_su_cyl`, `p_su_cyl` | cylinder inlet | 65 °C, 180000 Pa |
| `M_dot_a` | air mass flow | solved |
| `epsilon_v_bis` | efficiency on the cylinder-inlet density | solved |
| `T_ex_cp`, `T_ex_cp_s` | compressor outlet temperatures | solved |
| `w_cp`, `W_dot_cp` | specific work and compressor power | solved |
| `Q_dot_ic` | intercooler rate | solved |

The only implicit unknown is `h_ex_cp` (one equation). Every other equation
is explicit. There is no `square` and no `abs`.

## How to run

From this folder:

```bash
../../../../../CoolSolve/build/coolsolve ./supercharged_engine_air_flow.eescode
```

`supercharged_engine_air_flow.initials` holds the 29 stored values of the
variables that exist in the equation window. `L` and `D` are not among them.
With that file the solver reports 121 iterations. Without it, 121 iterations.
Both runs solve the same one-equation block for `h_ex_cp` and satisfy all 29
equations. The efficiency equation has one root; the stored enthalpies sit in
the EES reference frame, and the run with those guesses still returns the
CoolProp-frame root. The shipped `.sol` is the run with the initials. No
`coolsolve.conf` and no variant.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `rho_a` [kg/m³] | 1.153199 | 1.152817 |
| `M_dot_a` [kg/s] | 0.255088 | 0.255003 |
| `rho_a_bis` [kg/m³] | 1.854563 | 1.854424 |
| `epsilon_v_bis` [-] | 0.982471 | 0.982219 |
| `T_su_cp` [°C] | 23 | 23 |
| `T_ex_cp_s` [°C] | 79.1415 | 79.0475 |
| `T_ex_cp` [°C] | 83.8799 | 83.9104 |
| `w_cp` [J/kg] | 61351.85 | 61301.83 |
| `W_dot_cp` [W] | 15650.09 | 15632.15 |
| `Q_dot_ic` [W] | −4859.55 | −4860.32 |

Absolute enthalpies and entropies are not in this table. They carry the
CoolProp reference of `AIR` and are compared in Verification.

Orders of magnitude: 4.8 L over six cylinders is 0.8 L each; at 3500 1/min
with `i = 0.5` the intake volume flow at the ambient density is about
0.22 m³/s, so the air mass flow is about 0.26 kg/s. The pressure ratio
180 kPa / 98 kPa is about 1.84, and the compressor outlet is near 84 °C for
an isentropic efficiency of 0.92. The compressor power is about 16 kW. The
intercooler brings the air from that temperature to 65 °C and rejects about
4.9 kW. `epsilon_v_bis` is about 0.98, below one, once the flow is referred
to the density at the supercharged cylinder inlet.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

Air-flow exercise: the maintainer's figure is a schematic of the air path
(ambient, compressor, intercooler, cylinder inlet), saved as
`figures/supercharged_engine_air_flow_airpath.png`.

## Verification

Reference: the solution stored in `EX1_PNG_2019.EES` (31 variables decoded
by `ees_extract.py`, 29 with a stored value). The unit system is already
`SI MASS DEG PA C J`, so the comparison is without `--ees-units`.
`compare_solution.py` on `supercharged_engine_air_flow.sol` against
`reference/ees_variables.csv`:

> 29 common variables, 8 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 0

Maximum relative difference over all common variables: **0.31853**
(`s_su_cp`, the same value on `s_ex_cp_s`). The table printed by the tool
gives `3.19e-01` for both.

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `s_su_cp` | 5698.48 | 3883.32 | 3.19e-01 |
| `s_ex_cp_s` | 5698.48 | 3883.32 | 3.19e-01 |
| `h_su_cp` | 296577 | 422423 | 2.98e-01 |
| `h_su_cyl` | 338819 | 464725 | 2.71e-01 |
| `h_ex_cp_s` | 352975 | 478867 | 2.63e-01 |
| `h_ex_cp` | 357879 | 483775 | 2.60e-01 |
| `T_ex_cp_s` | 79.0475 | 79.1415 | 1.19e-03 |
| `W_dot_cp` | 15632.2 | 15650.1 | 1.15e-03 |

`M_dot_a` is 0.255088 kg/s versus 0.255003 kg/s (rel 3.31e-04). `T_ex_cp` is
83.8799 °C versus 83.9104 °C (rel 3.63e-04, −0.030 K). `T_su_cp` is 23 °C
on both sides. `rho_a` is 1.153199 kg/m³ versus 1.152817 kg/m³ (rel
3.31e-04). Near room temperature, CoolProp `Density(Air)` and EES differ by
a few parts in 10⁴ (3.24e-04 at 25 °C and 101325 Pa); here the state is
23 °C and 98000 Pa. `epsilon_v_bis` follows that density (rel 2.56e-04). `w_cp` is
61351.85 J/kg versus 61301.83 J/kg (rel 8.15e-04). `Q_dot_ic` is −4859.55 W
versus −4860.32 W (rel 1.59e-04). Those five stay inside rtol 0.001.

The entropy offset is −1815.17 J/(kg·K). The enthalpy offset is not a
constant: +125847 J/kg on `h_su_cp`, +125893 J/kg on `h_ex_cp_s`,
+125897 J/kg on `h_ex_cp` and +125906 J/kg on `h_su_cyl` (about +126 kJ/kg).
`T_ex_cp` is recovered from that CoolProp enthalpy, so it is reported above
separately from the absolute enthalpies. `T_ex_cp_s` is the temperature
returned from the isentropic entropy at `p_ex_cp`; the 0.094 K gap is the
property backend, and the relative difference on the Celsius value is
1.19e-03. `W_dot_cp` exceeds rtol because the specific-work gap (the
enthalpy offset is not constant) and the mass-flow gap multiply: rel
1.15e-03, about +18 W.

CoolSolve reports all 29 equations satisfied (max relative residual
2.55e-08, on the isentropic-efficiency equation).

The two decoded names that are only on one side are `L` and `D`. Each has a
guess (0.09623567124) and no stored value, and neither name appears in the
equation window. They are not in the comparison (`only in EES: 0`).

## Source and attribution

Source file
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP6/EX1_PNG_2019.EES`
(EES X10.589). The equation window is headed
`6ème séance d'exercices : énoncé 1 : PNG17042016`. `PNG17042016` is initials
plus a date, not a full name. The `{$ID$}` tag is the EES licence of
Philippe Ngendakumana (ULG Thermotechnics, Liège). The window does not name
another person. Author in `model.json`: P. Ngendakumana. ULiège course MCI,
TP6, sixth exercise session, statement 1. Published under the library
licence (MIT).

## Conversion log

- **2026-10-15 — import** (`ees_extract.py`): EES X10.589, plain-text
  equations, `{$ID$}`/`{$PX$}`/`{$ST$}` tags removed, no lookup or parametric
  table, 31 variables decoded, no extract warnings. Unit system already
  `SI MASS DEG PA C J`: `$UnitSystem` removed, no value rescaled. `$TABSTOPS`
  removed. The file has no `$Export` line. The unmodified extract, with only
  those directives removed, is square (29 equations, 29 variables, largest
  block 1). CoolSolve treats `p_amb` and `P_amb` as one variable, and
  `p_su_cyl` and `P_su_cyl` as one variable, so both spellings are left as
  written. `L` and `D` were not restored: the system is square without them,
  and neither has a stored value. Comments translated to English; variable
  names and the calls `Density(Air, …)` and `enthalpy(AIR, …)`,
  `entropy(AIR, …)`, `temperature(AIR, …)` kept. No diagram-state arrays.
  `epsilon_v = 1.58` is unchanged.
- **Level**: equations 29 (< 50) → 0; largest block 1 (≤ 5) → 0; no user
  function, procedure, array or `DUPLICATE` → 0; the engine flow, the
  compressor and the intercooler are sequential assignments, not a multi-zone
  model and not three coupled component models → 0; the two efficiencies are
  given data (no calibration, off-design map, part-load or dynamics) → 0;
  converges from the default guess in 121 iterations, without a tuned
  configuration → 0. Score 0 → **level 1**.

## Limitations and CoolSolve gaps

- `epsilon_v = 1.58` is the data of the exercise. It is greater than one
  because the original defines it on the ambient density.
- `Q_dot_ic` is negative: the original writes the air enthalpy rise across
  the intercooler.
- Absolute `AIR` enthalpy and entropy use the CoolProp reference. The
  enthalpy offset is about +126 kJ/kg and is not constant. `T_ex_cp_s` and
  `W_dot_cp` are the two results, besides those absolute properties, that
  exceed rtol 0.001. The equations are satisfied.
- Calling `Density` on `Air` prints a warning that moist air should use
  `AirH2O`. The fluid in the file is ideal-gas `Air`; the warning is the name
  check, and the fluid is unchanged.
- No CoolSolve gap blocks this file. `missing_features` is empty.

## Related models

- CSL-0279 (*engine_bsfc_bore_stroke_afr*): same volumetric-efficiency
  definition of the air flow, applied to a naturally aspirated engine with
  bore, stroke and specific fuel consumptions.
