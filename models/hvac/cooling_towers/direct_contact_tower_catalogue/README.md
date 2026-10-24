# Direct-contact cooling tower with catalogue data and nominal checks

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0290`

Open (direct-contact) cooling tower of the Laborelec 2002 toolkit: a
counter-flow heat exchanger between the cooling water and the air leaving the
tower saturated, the air side described by the fictitious fluid defined at the
wet-bulb temperature (the theory of the wet cooling coil). The tower
parameters (dry heat transfer coefficient, water/air flow exponents) and the
nominal values come from a catalogue lookup table (B.A.C. towers) or are
entered by the user; check procedures issue caution messages for an
out-of-range fooling factor, water flow and fan speed. The original is an EES
Diagram-Window model; this import reproduces its stored operating point (see
*Conversion log*).

| | |
|---|---|
| **Category** | HVAC › Cooling towers |
| **Fluids** | AirH2O (humid air), Water (variable specific heat) |
| **Size** | 63 equations, largest block: 11 (the counter-flow exchanger loop) |
| **Source** | ULiège/Laborelec toolkit 2002, `Direct Contact Cooling Tower.EES` (EES 6.596, Diagram Window), collection of S. Quoilin |
| **Authors** | Felipe Trebilcock (ULiège Thermodynamics Laboratory, for Laborelec, Dec 2002); reviewers J. Lebrun, E. Winandy |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

The catalogue tower `VTL-059-H (B.A.C.)` (dry heat transfer coefficient
16 434.7 W/K at nominal conditions, water/air flow exponents m = −0.02495 and
n = 0.6, nominal air volume flow 7.3 m³/s, nominal water flow 12 kg/s,
recommended water flow 6–20 kg/s) cools 12 kg/s of water entering at 45 °C
with 7.1 kg/s of ambient air at 25 °C, 80 % relative humidity and 101 325 Pa.
The fooling factor is 100 %. Determine the outlet water temperature, the range
and approach, the cooling power and the state of the exhaust air, and check
that the operating point stays within the catalogue limits.

## Model

- **Air side** (exhaust air saturated): $\dot Q = \dot C_{af}\,(t_{wb,ex} - t_{wb,su})
  = \dot m_a (h_{a,ex} - h_{a,su})$ with the fictitious capacity
  $\dot C_{af} = \dot m_a c_{p,af}$, the exhaust enthalpy evaluated at
  $(t_{wb,ex}, R=1)$ and $t_{wb,ex} = $ wetbulb$(t_{a,ex}, R=1)$.
- **Water side**: $\dot Q = \dot m_w c_w (t_{w,su} - t_{w,ex})$.
- **Equivalent counter-flow exchanger**: $\dot Q = \varepsilon_f \dot C_{min,f}
  (t_{w,su} - t_{wb,su})$ with the classical counter-flow effectiveness on the
  fictitious capacity rates, $NTU_f = AU_f/\dot C_{min,f}$ and
  $\omega_f = \dot C_{min,f}/\dot C_{max,f}$.
- **Heat transfer coefficient**: $AU_f = AU_{dry}\,(c_{p,af}/c_{p,a})\,Fooling\_F$,
  $AU_{dry} = AU_{dry,n}\,(\dot m_w/\dot m_{w,n})^{m}\,(\dot m_a/\dot m_{a,n})^{n}$
  (off-design law on both flow rates); $c_{p,af}$ follows from the air-side
  balance between the two wet-bulb states.
- **Practitioner variables**: approach $t_{w,ex} - t_{wb,su}$, range
  $t_{w,su} - t_{w,ex}$, capacity ratio $E_{ct} = range/(range + approach)$.
- **Checks** (procedures, as in the original): fooling factor within 0–100 %,
  water flow within the recommended range, fan speed between 40 % and 130 % of
  the nominal value (the latter only in the simulated-air-flow mode); messages
  in the string variables `NOTE1$`–`NOTE4$` (empty at the stored point).

The nominal air mass flow is $\dot m_{a,n} = 1.2\,\dot V_{a,N}$ (factor as in
the original). Inputs: `air_flow`, `t_w_su_ct`, `t_a_su_ct`, `RH_AIR`,
`P_atm`, the tower selection `Directcontac$` and the user-defined catalogue
inputs; outputs: `Q_dot_ct`, `t_w_ex_ct`, `t_a_ex_ct`, `approach`, `range`,
`E_ct`, `T_DEW`, the check messages.

## How to run

```bash
coolsolve ./direct_contact_tower_catalogue.eescode
```

The companion table `direct_contact_tower_catalogue-directcontactdata.csv`
(hand-decoded from the binary `directcontactdata.LKT` of the original) must
stay next to the file. The implicit loop needs the guess values of
`direct_contact_tower_catalogue.initials` (the stored EES values); without
them the exchanger block does not converge from a cold start.

## Results

Default run (stored operating point), EES stored value / CoolSolve:

| Variable | EES | CoolSolve |
|---|---:|---:|
| `Q_dot_ct` tower duty [kW] | 626.58 | 628.04 |
| `t_w_ex_ct` water outlet [°C] | 32.518 | 32.483 |
| `t_a_ex_ct` air outlet (saturated) [°C] | 38.503 | 38.482 |
| `range` [K] | 12.482 | 12.517 |
| `approach` [K] | 10.137 | 10.104 |
| `E_ct` capacity ratio [-] | 0.5518 | 0.5533 |
| `epsilon_f_ct` effectiveness [-] | 0.7128 | 0.7119 |
| `V_dot_a_ct` air volume flow [m³/s] | 6.151 | 6.149 |

The check messages `NOTE1$`–`NOTE4$` are empty: the operating point is inside
the catalogue limits (water flow 12 kg/s within 6–20 kg/s).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep (e.g. water
     outlet temperature or cooling power vs air flow rate), figures/direct_contact_tower_catalogue_<type>.png -->

## Verification

Compared with the solution stored in the source file (60 variable records;
the reference values of the 15 kJ/kPa quantities converted ×1000 by hand, the
`--ees-units` option being unable to convert the variables stored without a
unit). `compare_solution.py`: **56 common variables, 16 differ (rtol=0.001);
only in EES: 4; only in CoolSolve: 7**, maximum relative difference
**3.97e-03** (`omega_f_ct`).

- All 16 differences are downstream of the humid-air property differences
  between EES 6.596 and CoolProp (`h_a_su_ct`/`h_a_ex_ct` 2.3e-03, `c_p_af_ct`
  3.6e-03, `c_w` 4.3e-04) — the same family as the sibling model `CSL-0076`
  (max 4.51e-03); the 40 algebraic results agree to better than 1e-03 or
  follow these properties.
- Excluded from the comparison: the 4 variables of the non-active
  Diagram-window modes that EES keeps from earlier runs (`DELTAp_ct`, `rpm_fan`,
  `V_dot_a_ct_fan`, `V_dot_a_ct_rpm`) and the 7 string variables (`fluid$`,
  `Directcontac$`, `airflow$`, `NOTE1$`–`NOTE4$`), which EES does not store;
  the strings are checked by eye in the `.sol` file (messages empty, as
  expected at the stored point).

## Source and attribution

Laborelec 2002 toolkit (evaporative equipment section), ULiège Thermodynamics
Laboratory: F. Trebilcock, December 2002, for Laborelec; reviewers J. Lebrun
and E. Winandy. The ULiège collection is published under the library license
(MIT). Source file (comments in English):
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/2_Evaporative Equipments/2_2_Simulation Models - Diagram Window/Direct Contact Cooling Tower/Direct Contact Cooling Tower.EES`
(inventory candidate `TM-0297`; catalogue table `directcontactdata.LKT`,
candidate `TM-0298`).

## Conversion log

- **2026-10-22 — import** (`tools/ees_extract.py`): EES 6.596, unit system
  `SI MASS DEG KPA C KJ` → converted by hand to SI-°C-Pa-J: `P_atm` 101.325 →
  101325 Pa; `Q_dot_ct`, `C_dot_af_ct`, `C_dot_w_ct`, `C_dot_min_f_ct`,
  `C_dot_max_f_ct`, `AU_f_ct`, `AU_dry_ct`, `AU_dry_n_ct` (kW/K), `AU_dry_n_input`,
  `h_a_ex_ct`, `h_a_su_ct`, `c_p_af_ct`, `c_p_a_ct`, `c_w` (kJ/kg-K): ×1000;
  the check thresholds, temperatures and dimensionless values unchanged; the
  15 converted reference values ×1000 for the comparison. No `$UnitSystem`
  line kept.
- **2026-10-22 — catalogue table** (`TM-0298`): `directcontactdata.LKT` is a
  binary EES-6 lookup table (not decoded by the tool). Hand-decoded
  (80-bit Extended floats): 2 columns × 7 rows, `VXT-10 (B.A.C.)` =
  [3000, 0.3, 0.6, 1.79, 4.0, 1.6, 6.6] and `VTL-059-H (B.A.C.)` =
  [16434.7, −0.02495, 0.6, 7.3, 12.0, 6.0, 20.0] (rows: `AU_dry_n` [W/K],
  `m_ct`, `n_ct`, `V_dot_a_N` [m³/s], `M_dot_w_n`, `M_dot_w_min`, `M_dot_w_max`
  [kg/s]; the AU column ×1000 from the original kW/K). Each column name
  precedes its values in the binary (layout as in the toolkit's
  `Pipedata.LKT`, imported in `CSL-0158`). The stored solution pins the
  active column to [16434.7, −0.02495, 0.6, 7.3, 12, 6, 20] (identical
  `AU_dry_n_ct`, `m_ct`, `n_ct`, `V_dot_a_N_ct`, `M_dot_w_n_ct`,
  `M_dot_w_min`, `M_dot_w_max`), hence `Directcontac$ = 'VTL-059-H (B.A.C.)'`;
  the `VXT-10` column is unverified (no stored run of it).
- **2026-10-22 — Diagram-window operating point**: the original is an EES
  Diagram-Window model whose air-flow, water-flow and fan modes are pop-down
  menus that include hidden equation snippets (the `.TXT` companion files of
  the inventory row). The stored solution identifies the active modes: air
  flow = `M_dot_a [kg/s]` (`M_dot_a_ct = air_flow` = 7.1,
  `V_dot_a_ct = M_dot_a_ct·v_a_ct`, `rpm_fan_tmp = rpm_FAN_n_ct`; snippet
  `air mass flow.TXT`) and water flow = `M_dot_w : Nominal`
  (`M_dot_w_ct = M_dot_w_n_ct`; snippet `water nominal.TXT`). The 4 equations
  of these two snippets are copied at the end of the model; the 10 other
  modes (air volume flow, nominal air flow, simulated air flow with the
  fan/pressure-drop submodel of `simulated.TXT`, imposed water flow, the
  imposed temperatures and the fan-speed modes) are not reproduced; their
  variables are not in the model. The interface values of
  `t_w_su_ct = 45 °C` and `t_a_su_ct = 25 °C` are entered directly (the
  diagram inputs `T_water`/`T_air_ct` have no stored record); `RH_AIR = 80`,
  `air_flow = 7.1`, `P_atm`, `rpm_FAN_n_ct = 2900`, `eta_FAN_ct = 0.65`,
  `F_F = 100` and the seven `*_input` values of the user-defined mode keep
  their stored values. The original's commented call to `RPMFLOW` (a
  procedure the file does not define) is kept as a comment; `airflow$` and
  `Directcontac$` carry the exact strings of the original menus/table.
- **2026-10-22 — comments**: translated/paraphrased in English; the
  description of the fictitious-fluid theory ("as in the original") kept
  short; no equation changed apart from the unit conversions above.
- **Level**: equations 63 (1) + largest block 11 (1) + procedures (1) +
  multi-zone no (0) + semi-empirical off-design law and catalogue data (1) +
  curated guesses required, no cold start (1) = 5 → level 3 (matches the
  inventory `level_guess`).

## Limitations and CoolSolve gaps

- The Diagram-window interface of the original (mode pop-downs, input fields)
  is not reproducible in CoolSolve: switching mode means editing the 4 mode
  equations and the `airflow$`/`Directcontac$` strings at the end of the file.
  No CoolSolve gap is involved (the physics runs natively); the fan and
  pressure-drop submodel of the `Simulate` mode is not part of this import.
- The second catalogue column (`VXT-10`) could not be verified (no stored run).
- The exhaust air is assumed saturated and the wet-bulb/dry-bulb temperatures
  of the exhaust are then equal by definition (`t_wb_ex_ct = wetbulb(t_a_ex_ct,
  R=1)`), as in the original; the water consumption of the tower is not
  computed (it is in `CSL-0076`).

## Related models

- `CSL-0076` *cooling_tower_direct_contact_refsim*: the same component and the
  same fictitious-fluid theory in the 2008 ULiège model bank version (free
  areas, fan curve, water consumption); the catalogue/check procedures and the
  B.A.C. lookup table are specific to this import.
- `CSL-0227` *evaporative_condenser_effectiveness*: the evaporative equipment
  of the same toolkit family, condenser side (R22, catalogue effectiveness).
- `CSL-0303` *evaporative_condenser_catalogue*: the Diagram-Window sibling of
  the same toolkit, evaporative-condenser side (R717, BAC VXC catalogue); same
  fictitious-fluid theory and check-procedure pattern.
- `CSL-0286` *indirect_contact_tower_identification*: the fluid-cooler
  (indirect-contact, closed fluid loop) identification model of the same
  toolkit, same fictitious-fluid theory with an air/fluid resistance split.
