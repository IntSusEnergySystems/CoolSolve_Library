# Fluid cooler (indirect-contact cooling tower): catalogue identification

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0286`

Identification and simulation of a fluid cooler (closed-loop or indirect-contact
cooling tower) from manufacturer catalogue data, from the Laborelec 2002
evaporative-equipment toolkit. The cooler is represented as an equivalent
counterflow heat exchanger between the cooled fluid and a fictitious air
defined at the wet-bulb temperature (wet-coil theory); the identified
resistances reproduce the catalogue duty of a B.A.C. VXI-70-3 unit within a
few percent over a 205-point catalogue table.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | AirH2O (humid air), Water (constant specific heat) |
| **Size** | 40 equations (largest block: 13) |
| **Source** | ULiège/Laborelec toolkit 2002, `Indirect_contact_identification.EES` (EES 6.350), collection of S. Quoilin |
| **Authors** | Felipe Trebilcock (ULiège Thermodynamics Lab, Dec 2002, for Laborelec); reviewers J. Lebrun, E. Winandy |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — blocked by `CS-GAP-HX`; the runnable variant `indirect_contact_tower_identification_coolsolve.eescode` is verified (see *Verification*) |

## Problem statement

The catalogue data of a fluid cooler (fluid inlet/outlet temperatures, wet-bulb
temperature, fluid flow) are used to identify the two parameters of the model —
the nominal air-side resistance `R_a_ct_N` and the ratio to the nominal
fluid-side resistance `R_fl_ct_N/R_a_ct_N` — by minimising the percentage error
between the simulated and the catalogue heat flow rate over the catalogue
operating points. The identified values are then used in the simulation model
of the same toolkit (`Indirect_contact_simulation.EES`, candidate TM-0296). The
default values of the original are kept: the B.A.C. VXI-70-3 unit,
`R_a_ct_N = 0.0275 K/kW` and a ratio of 5.2 (flow exponents −0.6 on the air
side, −0.8 on the fluid side).

## Model

The humid air is replaced by a fictitious perfect gas whose temperature is the
wet-bulb temperature (as in the original): its capacity rate is
`C_dot_af_ct = M_dot_a_ct·c_p_af_ct` with
`c_p_af_ct = (h_a_ex_ct − h_a_su_ct)/(t_wb_ex_ct − t_wb_su_ct)`. The heat flow
rate is then that of a counterflow exchanger on the fictitious fluids:

- `Q_dot_ct = epsilon_ct · C_dot_min_ct · (t_fl_su_ct − t_wb_su_ct)`, with
  `epsilon_ct = HX('counterflow', NTU_ct, C_dot_af_ct, C_dot_fl_ct, 'epsilon')`
  (EES built-in) and `NTU_ct = UA_ct/C_dot_min_ct`;
- the total resistance splits into `R_ct = R_af_ct + R_fl_ct` with
  `R_af_ct = R_a_ct·c_p_a_ct/c_p_af_ct`,
  `R_a_ct = R_a_ct_N·(M_dot_a_ct/M_dot_a_ct_N)^(−0.6)` and
  `R_fl_ct = R_fl_ct_N·(M_dot_fl_ct/M_dot_fl_ct_N)^(−0.8)`;
- the operating point is read from catalogue table `lookup_1`
  (`t_wb_su_ct`, `approach`, `Range_cat`, `M_dot_fl_ct` at row `i`);
  `t_fl_ex_ct = approach + t_wb_su_ct`, `t_fl_su_ct = t_fl_ex_ct + Range`;
- the percentage error against the catalogue is
  `ERRQ_dot_ct = (Q_dot_ct − Q_dot_ct_cat)/Q_dot_ct_cat·100` with
  `Q_dot_ct_cat = C_dot_fl_ct·Range_cat`.

Inputs: `V_dot_a_ct` = 22.9 m³/s, `M_dot_fl_ct_N` = 20 kg/s, `c_fl` = 4180
J/kg-K, `RH_su_ct` = 0.5, `RH_ex_ct` = 1, `i` = 205 (catalogue row: wet-bulb
26 °C, approach 16 K, range 22 K, fluid flow 23.67 kg/s), `P_atm` = 101325 Pa.

## How to run

The native file keeps the EES built-in `HX('counterflow', …)` call and is
blocked by `CS-GAP-HX` (CoolSolve has no `HX` function). The runnable variant
`indirect_contact_tower_identification_coolsolve.eescode` writes the
counterflow effectiveness–NTU relation explicitly — the only change, logged in
the conversion log — and is regression-tested as `CSL-0286:coolsolve`:

```bash
coolsolve ./indirect_contact_tower_identification_coolsolve.eescode
```

The `.initials` hold the EES stored solution (resistances converted K/kW →
K/W). Other catalogue rows are run by editing `i` (1–205); the other VXI units
of the original (VXI-27-3, VXI-145-3, VXI-215-3, their own lookup tables and
default parameters, listed in the original file comments) are not reproduced —
only the default VXI-70-3 table ships.

## Results

Default point (row `i` = 205, VXI-70-3):

| Quantity | EES (stored) | CoolSolve (variant) |
|---|---:|---:|
| `Q_dot_ct` heat flow rate | 2099.3 kW | 2105.5 kW |
| `Q_dot_ct_cat` catalogue duty | 2176.7 kW | 2176.7 kW |
| `ERRQ_dot_ct` percentage error | −3.56 % | −3.27 % |
| `epsilon_ct` effectiveness | 0.5701 | 0.5708 |
| `NTU_ct` | 1.084 | 1.085 |
| `UA_ct` | 107.2 kW/K | 107.3 kW/K |
| `t_a_su_ct` / `t_a_ex_ct` | 34.83 / 39.55 °C | 34.83 / 39.54 °C |
| `Range` | 21.22 K | 21.28 K |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): plot of the percentage
     error ERRQ_dot_ct over the catalogue rows i, figures/indirect_contact_tower_identification_error.png -->

## Verification

The **variant** was compared with the solution stored in the EES source file
(48 records; the reference values converted kJ/kW → J/W by hand, the
resistances K/kW → K/W divided by 1000): 40 common variables, maximum relative
difference **8.08e-02** on `ERQ_dot_ct`/`ERRQ_dot_ct` — the amplification of
the 2.97e-03 deviation of `Q_dot_ct` on the small difference-to-catalogue term
— all other deviations below **4.2e-03**, downstream of the humid-air property
differences EES 6.35 vs CoolProp (h_a 2.6e-03, c_p_af 4.0e-03), as in
`CSL-0290` (3.97e-03) and `CSL-0076` (4.51e-03). The catalogue table decoded
from the binary was checked against two in-file references: row 205 reproduces
the stored solution (26 / 16 / 22 / 23.67) and row 100 the worked example
commented in the file (20 / 16 / 6 / 53.2). The native file fails only on the
`HX` call (block 22, 13 variables: *Unknown or unsupported function: HX with 5
arguments*).

## Niche

Nearest library models: `CSL-0290` *direct_contact_tower_catalogue* (same
toolkit, catalogue identification, same fictitious-air theory — but an **open**
tower: single dry-coil UA with a fooling factor, water in direct contact with
the air) and `CSL-0076` *cooling_tower_direct_contact_refsim* (open-tower
reference simulation model with air-side pressure drop). This model adds the
**indirect-contact** topology: a closed fluid loop separated from the air
loop, a two-resistance model with air/fluid mass-flow exponents (−0.6/−0.8)
instead of one UA correlation, and the identification procedure against a
205-point catalogue table. The direct-contact siblings TM-0293/TM-0294 of the
same toolkit were merged into `CSL-0076` by the 2026-10-22 pre-screen; the
indirect-contact files were kept as a card.

## Source and attribution

Model by **Felipe Trebilcock** (ULiège Thermodynamics Laboratory, December
2002) for the Laborelec evaporative-equipment toolkit; reviewers J. Lebrun and
E. Winandy (identified from the inventory; the file itself names no author).
The catalogue data are B.A.C. VXI fluid coolers.

Source file (EES 6.350, comments in English, kPa/kJ units, decimal comma):
`~/Nextcloud/thermo_models/modeles/LABORELEC_2002/2_Evaporative Equipments/2_1_Toolkit Models/2_1_2_Cooling_towers/Indirect_contact_identification.EES`
(inventory candidate `TM-0295`).

## Conversion log

- **2026-10-23 — import** (`tools/ees_extract.py`, CoolSolve repository): unit
  system `SI MASS DEG KPA C KJ` converted by hand to SI-°C-Pa-J: `P_atm`
  101.325 kPa → 101325 Pa, `c_fl` 4.18 kJ/kg-K → 4180 J/kg-K, and the constant
  `R_a_ct_N = 0.0275` K/kW → `0.0275E-3` K/W (the resistance equations are
  homogeneous, only this constant changes); enthalpy/capacity/UA results are
  read in J, W and W/K. The stored solution had 8 stale variables of an
  earlier program (`C_dot`, `R`, `epsilon`, `V_dot`, `rho`, `R_a`, `w`, `COP`),
  not in the equations: dropped. Comments kept (English), nomenclature and
  worked-example comment blocks moved to this README, standard header added.
- **2026-10-23 — catalogue table recovered by hand.** The extractor decoded no
  lookup table (EES 6.350 stores the tables in a layout its heuristic does not
  read; its "parametric 433×2/422×2" report entries are false positives). The
  binary was hand-decoded: four catalogue tables named after the B.A.C. units
  (VXI-70-3: 205 rows × 4 columns `t_wb`, `Approach`, `DELTAT`, `M_dot_fl,ct,cat`
  — 80-bit extended values, 24–27 bytes of pointer junk after each 31-byte
  header). The one read by the nameless `lookup(i, col)` of the original is the
  VXI-70-3 table (verified at rows 100 and 205, see *Verification*); it ships
  as `indirect_contact_tower_identification-lookup_1.csv` (and as
  `…_coolsolve-lookup_1.csv` for the variant, identical values).
- **2026-10-23 — runnable variant** (only change forced by `CS-GAP-HX`):
  `epsilon_ct = HX('counterflow',NTU_ct,C_dot_af_ct,C_dot_fl_ct,'epsilon')`
  replaced by `epsilon_ct = (1 − exp(−NTU_ct·(1 − Cr_ct)))/(1 − Cr_ct·exp(−NTU_ct·(1 − Cr_ct)))`
  with `Cr_ct = C_dot_min_ct/C_dot_max_ct` (the standard counterflow
  effectiveness–NTU relation, as in `CSL-0290`; EES-valid, no CoolSolve-only
  syntax). Everything else, variable names included, is identical.
- **2026-10-23 — inputs**: `i` (catalogue row), `t_a_su_ct` and `t_a_ex_ct`
  are inputs of the original (no defining equation); the stored-run values
  `i = 205` are set in the equations, the two air temperatures follow from the
  wet-bulb calls at the stored `RH_su_ct` = 0.5 / `RH_ex_ct` = 1.
- **Level**: score of taxonomy.md §3: equations 40 (< 50) = 0; largest block 13
  (6–30) = 1; no functions/arrays = 0; no multi-zone structure = 0;
  semi-empirical calibration = 1; stored-solution guesses suffice = 0.
  Score 2 → **level 2**. The inventory `kind_guess` was `optimization`, but the
  original minimises the error manually (user-adjusted constants, no EES
  Min/Max): the model is `steady` with the tag `parameter identification`.

## Limitations and CoolSolve gaps

- `CS-GAP-HX`: the EES built-in heat-exchanger function `HX(Type$, NTU, C_dot_1,
  C_dot_2, Param$)` is not implemented in CoolSolve; the native file is blocked
  by it, the variant replaces the single call (see *Conversion log*).
- The fictitious-air hypothesis collapses the humid-air state to the wet-bulb
  temperature; the exhaust air is taken saturated (`RH_ex_ct` = 1), as in the
  original.
- The fluid side uses a constant specific heat `c_fl` = 4180 J/kg-K.
- Catalogue table columns carry no units in the original; the values are
  °C, K, K and kg/s respectively (verified through the stored solution).

## Related models

- `CSL-0076` *cooling_tower_direct_contact_refsim*: direct-contact (open)
  cooling tower reference model of the same collection; the wet-coil theory
  with an air-side pressure-drop submodel.
- `CSL-0290` *direct_contact_tower_catalogue*: the catalogue-identification
  counterpart for open towers (same toolkit, same fictitious-air theory, one
  UA with flow exponents and a fooling factor).
