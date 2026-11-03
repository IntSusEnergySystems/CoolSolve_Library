# Evaporative condenser with catalogue data (BAC VXC) and operating checks

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0303`

Evaporative condenser of the Laborelec 2002 toolkit: the heat flow rate from
the condensing ammonia (R717) to the air/spray water is computed on the air
side with the fictitious-fluid theory (air leaving saturated, capacity rate
defined between the wet-bulb states) and on the refrigerant side with a
condensing resistance; the air-side resistance follows an off-design law on
the air mass flow, and the nominal parameters come from a catalogue lookup
table (BAC VXC series, 14 models) or from user-defined inputs. Check
procedures issue caution messages for an out-of-range isentropic
effectiveness, manufacturer limits, fooling factor and subcooling. The
original is an EES Diagram-Window model; this import reproduces its stored
operating point (see *Conversion log*).

| | |
|---|---|
| **Category** | Cycles › Refrigeration & heat pumps |
| **Fluids** | R717 (ammonia), AirH2O (humid air) |
| **Size** | 75 equations, largest block: 11 (the condenser/air loop) |
| **Source** | ULiège/Laborelec toolkit 2002, `Evaporative_condenser_simulation.EES` (EES 6.596, Diagram Window), collection of S. Quoilin |
| **Authors** | Felipe Trebilcock (ULiège Thermodynamics Laboratory, for Laborelec, Dec 2002); reviewers J. Lebrun, E. Winandy |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

The catalogue condenser `VXC-714 (Q_dot_cd=3076 [kW])` (air-side resistance
5.29e-6 K/W at nominal flow, condensing resistance 1.613e-6 K/W, nominal air
volume flow 68.6 m³/s, nominal capacity 3076 kW) rejects the heat of an R717
cycle condensing at 36 °C with 5 K of subcooling; the compressor (isentropic
effectiveness 0.75) sucks saturated vapour at −5 °C with 5 K of superheating.
Ambient air: 25 °C, 60 % relative humidity, 101 300 Pa; fooling factor 100 %.
The model computes the condenser duty, the air-outlet state, the spray-water
temperature, the refrigerant mass flow, the compressor power and the COP, and
checks the operating point against the catalogue limits.

## Model

- **Air side** (exhaust air saturated): $\dot Q = \dot m_a (h_{a,ex} - h_{a,su})
  = \dot C_{af}\,(t_{wb,ex} - t_{wb,su})$ with the fictitious capacity
  $\dot C_{af} = \dot m_a c_{p,af}$, $c_{p,af}$ following from the air-side
  balance between the two wet-bulb states (fictitious fluid defined at the
  wet-bulb temperature, as in the original).
- **Refrigerant side**: $\dot Q = \dot m_r (h_{r,su} - h_{r,ex}) =
  (t_{cd} - t_w)/R_r$, with $t_{cd}$ the condensing temperature and $t_w$ the
  spray-water temperature.
- **Effectiveness form**: $\dot Q = \varepsilon\, \dot C_{min}\,(t_w - t_{wb,su})$
  with $\varepsilon = 1 - e^{-NTU}$ (one fluid at constant temperature),
  $NTU = 1/(R_{af}\dot C_{af})$.
- **Heat transfer resistances**: $R_r = R_{r,N}$ (no refrigerant-flow
  dependence, as in the original); $R_{af} = R_a\, c_{p,a}/(c_{p,af}\,
  Fooling\_F)$ with $R_a = R_{a,N}(\dot m_a/\dot m_{a,N})^{-0.5}$ (off-design
  law on the air mass flow).
- **Compressor**: $w = w_s/\epsilon_s$ (isentropic), adiabatic, suction state
  from $t_{ev}$ + superheating, discharge pressure = condensing pressure.
- **Practitioner variables**: $\dot Q_{ev} = \dot Q_{cd} - \dot W_{cp}$ and
  $COP = \dot Q_{ev}/\dot W_{cp}$.
- **Checks** (procedures, as in the original): isentropic effectiveness within
  0–1, wet-bulb temperature within 10–28 °C and condensing temperature within
  29–45 °C (manufacturer limits), fooling factor within 0–100 %, subcooling
  ≤ 10 K; messages in the string variables `NOTE1$`–`NOTE5$` (empty at the
  stored point).

The catalogue lookup (`CONDENSERDATA` procedure) reads the column selected by
`Condenser$` from the table `condenserdata` (14 BAC VXC models, hand-decoded
from the binary `.LKT`, see *Conversion log*); `Condenser$ = 'User defined'`
takes the four `*_input` values instead.

## How to run

```bash
coolsolve ./evaporative_condenser_catalogue.eescode
```

The companion table `evaporative_condenser_catalogue-condenserdata.csv`
(hand-decoded from the binary `condenserdata.LKT` of the original) must stay
next to the file. The implicit loop needs the guess values of
`evaporative_condenser_catalogue.initials` (the stored EES values); without
them the condenser block does not converge from a cold start.

## Results

Default run (stored operating point), EES stored value / CoolSolve (SI units;
the EES values of the kJ/kPa quantities ×1000):

| Variable | EES | CoolSolve |
|---|---:|---:|
| `Q_dot_cd` condenser duty [W] | 3 329 955 | 3 337 594 |
| `Q_dot_ev` cooling capacity [W] | 2 687 912 | 2 694 343 |
| `W_dot_cp` compressor power [W] | 642 043 | 643 251 |
| `COP` [-] | 4.1865 | 4.1886 |
| `t_w_cd` spray-water temperature [°C] | 30.629 | 30.616 |
| `t_a_ex_cd` air outlet (= `t_wb_ex_cd`, saturated) [°C] | 29.518 | 29.505 |
| `epsilon_af_cd` effectiveness [-] | 0.90047 | 0.90028 |
| `w_s` isentropic specific work [J/kg] | 201 162 | 201 024 |

`M_dot_r` = 2.400 kg/s in CoolSolve (not stored in the EES file; it follows
from $\dot Q_{cd} = \dot m_r \Delta h_r$). The check messages `NOTE1$`–`NOTE5$`
are empty: the operating point is inside the manufacturer limits.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep (e.g.
     condenser duty or approach vs air flow rate), figures/evaporative_condenser_catalogue_<type>.png -->

## Verification

Compared with the solution stored in the source file (67 variable records;
the 32 kJ/kPa reference values converted by hand — ×1000, the K/kW
resistances ÷1000 — most variables being stored without a unit).
`compare_solution.py`: **67 common variables, 21 differ (rtol=0.001);
only in EES: 0; only in CoolSolve: 8**.

- 6 of the differences are the **ammonia reference-state offset** between EES
  and CoolProp on the absolute `h`/`s` (`h_r_ex_cd`, `h_r_ex_cp`, `h_r_exs_cp`,
  `h_r_su_cd`, `h_r_su_cp`: offset +145.1…+145.5 kJ/kg; `s_r_su_cp`:
  +482 J/kg-K). The derived differences agree: `w_s` 6.9e-04,
  `h_r_su_cd − h_r_ex_cd` 2.7e-04.
- The 15 others (max **4.27e-03** on `W_su_cd`) are all downstream of the
  humid-air property differences between EES 6.596 and CoolProp — the same
  family as the sibling model `CSL-0290` (max 3.97e-03).
- Excluded from the comparison: `M_dot_r` (computed here, absent from the EES
  storage; consistent with the stored `W_dot_cp` and `Q_dot_cd`) and the 7
  string variables (`fluid$`, `Condenser$`, `NOTE1$`–`NOTE5$`), which EES does
  not store; the strings are checked by eye in the `.sol` file (messages
  empty, as expected at the stored point).

## Source and attribution

Laborelec 2002 toolkit (evaporative equipment section), ULiège Thermodynamics
Laboratory: F. Trebilcock, December 2002, for Laborelec; reviewers J. Lebrun
and E. Winandy. The ULiège collection is published under the library license
(MIT). Source file:
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/2_Evaporative Equipments/2_2_Simulation Models - Diagram Window/Evaporative Condenser/Evaporative_condenser_simulation.EES`
(inventory candidate `TM-0300`; catalogue table `condenserdata.LKT`, candidate
`TM-0299`).

## Conversion log

- **2026-10-22 — import** (`tools/ees_extract.py`): EES 6.596, unit system
  `SI MASS DEG KPA C KJ` → converted by hand to SI-°C-Pa-J: `P_atm`
  101.3 → 101 300 Pa; `Q_dot_cd_N_input` 1000 kW → 1e6 W; `R_a_cd_N_input`
  0.0035 K/kW → 3.5e-6 K/W, `R_r_cd_N_input` 0.001 K/kW → 1e-6 K/W; the
  property calls now return Pa/J (no factor kept around them); the check
  thresholds, temperatures and dimensionless values unchanged; the 32
  reference values of the kJ/kPa/K-per-kW quantities converted by hand for
  the comparison. No `$UnitSystem` line kept. No equation changed apart from
  these input values.
- **2026-10-22 — catalogue table** (`TM-0299`): `condenserdata.LKT` is a
  binary EES-6 lookup table (not decoded by the tool). Hand-decoded
  (80-bit Extended floats): 4 rows × 14 columns; each column is a condenser
  named `VXC-<size> (Q_dot_cd=<capacity> [kW])` (VXC-185 to VXC-1360), the
  rows being `R_a_cd_N` [K/kW in the file → K/W], `R_r_cd_N` [K/kW → K/W],
  `V_dot_a_cd_N` [m³/s] and `Q_dot_cd_N` [kW → W]; e.g. VXC-714 =
  [0.00529, 0.001613, 68.6, 3076] in the original units. The decoding is
  proven by the stored solution, which matches the VXC-714 column exactly
  (`R_a_cd_N` = 0.00529, `R_r_cd_N` = 0.001613, `V_dot_a_cd_N` = 68.6,
  `Q_dot_cd_N` = 3076); the 13 other columns are unverified (no stored run
  of them). The commented line `V_dot_a_cd_N = 15.7` of the original matches
  the first column (VXC-185), an earlier parameterisation of the file.
- **2026-10-22 — Diagram-window operating point**: the original is an EES
  Diagram-Window model; its mode pop-down menus include hidden equation
  snippets (the `.TXT` companion files of the inventory row). The stored
  solution identifies the active modes: air flow = **nominal air flow**
  (`V_dot_a_cd = V_dot_a_cd_N`, copied at the end of the model — the only
  air-side mode that introduces no new interface variable, and it reproduces
  the exact equalities `V_dot_a_cd` = `V_dot_a_cd_N` = 68.6 m³/s and
  `M_dot_a_cd` = `M_dot_a_N_cd` of the stored run), condenser = **condensing
  temperature** (`T_cd` imposed = 36 °C) and compressor = **isentropic
  effectiveness** (`epsilon_s` = 0.75). The interface values of `T_cd` and
  `epsilon_s` are entered directly (their diagram inputs `flow_rate` /
  `comp_perf` have no stored record; a commented line of the original keeps
  older values 37 °C and `DELTAt_sc` = 1). The 12 other mode snippets (air
  mass/volume/wet-bulb modes, cooling/heating capacity, refrigerant mass
  flow, compressor power, displacer volume flow) are not reproduced; their
  variables are not in the model. `RH_AIR` = 60, `t_a_su_cd` = 25,
  `P_atm` = 101.3 kPa, `t_ev` = −5 °C, `DELTAt_sh` = 5 K, `F_F` = 100 and
  the four `*_input` values of the user-defined mode keep their stored
  values; `fluid$ = 'R717'` comes from a commented line of the original;
  `Condenser$` carries the exact string of the active catalogue column.
- **2026-10-22 — dead code**: the commented block `{R_a_cd_N = 3.5*R_r_cd;
  R_r_cd_N = 0.00545}` (older parameterisation, matches no catalogue value)
  and the commented input lines are removed; the comments are
  translated/paraphrased in English (the original is in English); the
  original's description of the fictitious-fluid theory is kept ("as in the
  original").
- **Level**: equations 75 (1) + largest block 11 (1) + procedures (1) +
  multi-zone no (0) + semi-empirical off-design law and catalogue data (1) +
  curated guesses required, no cold start (1) = 5 → level 3 (matches the
  inventory `level_guess`).

## Limitations

- The Diagram-window interface of the original (mode pop-downs, input fields)
  is not reproducible in CoolSolve: switching mode means editing the mode
  equations at the end of the file. No CoolSolve gap is involved (the physics
  runs natively); only the stored operating point is reproduced.
- The 13 catalogue columns other than VXC-714 could not be verified (no
  stored run of them).
- Absolute ammonia `h`/`s` carry a reference-state offset between EES and
  CoolProp (see *Verification*); only differences and derived results are
  comparable.
- A transient CoolProp warning (`enthalpy()` NaN) can appear during the
  iterations when a trial state falls inside the two-phase dome; the final
  state is subcooled liquid and the solution satisfies all equations.

## Related models

- `CSL-0290` *direct_contact_tower_catalogue*: the Diagram-Window sibling of
  the same toolkit, cooling-tower side (water loop, B.A.C. catalogue); same
  fictitious-fluid theory and check-procedure pattern.
- `CSL-0227` *evaporative_condenser_effectiveness*: the evaporative
  condenser of the MSTh course (R22, semi-isothermal exchanger with a
  constant effectiveness).
