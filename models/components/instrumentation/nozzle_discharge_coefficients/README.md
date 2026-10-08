# Nozzle discharge coefficients and airflow-rate procedures

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0122`

Procedure library for air flow metering with the ASHRAE 41.2 / ISO R859
discharge nozzles (a bank of up to four nozzles used simultaneously or
separately) and with an ISO 5167 **long-radius nozzle**, plus a
compressible-flow **admission** procedure (choked / subsonic mass flow
through a valve or nozzle opening) and three validity-range checkers.

| | |
|---|---|
| **Category** | Components › Instrumentation |
| **Fluids** | AirH2O (humid air at the nozzle states) |
| **Size** | 97 equations (largest block: 6): 6 procedures + demonstration program |
| **Source** | ULiège collection — `procedures EES/`: `airflow rate - ashrae 41.2.EES` (TM-0558), `airflowrate - long radius.EES` (TM-0559), `tuyere.EES` (TM-0587), `Out of range warning.EES` (TM-0581) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory, `procedures EES/` toolkit; EES licence stamp of the J. Lebrun lab) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — library file runs and is verified; the source files need `CS-GAP-SUM-INDEXED` and `CS-GAP-CALL-WARNING` (see *Limitations*) |

## Functions

| Function | Signature | Purpose / reference | Source |
|---|---|---|---|
| `velo` | `(d, M_dot_a, rho, A : V)` | Throat velocity of one nozzle [m/s]; `V = 0` for an unused nozzle (`d = 0`) | TM-0558 |
| `coeficiente` | `(Re : c_d)` | Nozzle discharge coefficient `c_d = 0.826270423 + 0.0130803659·ln(Re)` [-], the ASHRAE 41.2 / ISO R859 correlation (0 < Re, 0 otherwise) | TM-0558 |
| `admission` | `(theta, theta_ivo, theta_ivc, rho_0, C_d, A_v, c_0, gamma_a, p_0, p_valve : m_dot, choked)` | Mass flow rate through a valve or nozzle opening during the admission [kg/s]: zero when the valve is closed (theta outside theta_ivo…theta_ivc) or `p_valve > p_0`; otherwise the ideal-gas isentropic nozzle equation, choked below the critical ratio `(2/(γ+1))^(γ/(γ−1))`, subsonic above. `rho_0`, `c_0` are the upstream density and speed of sound | TM-0587 |
| `warning_error_ashrae` | `(v : v)` | Throat velocity between 15 and 35 m/s (ASHRAE 41.2 recommendation, as in the original) | TM-0558 |
| `warning_error_iso5167` | `(De, beta, Re_D : …)` | ISO 5167 validity ranges of the long-radius nozzle: pipe diameter 0.05–0.63 m, beta 0.2–0.8, pipe Reynolds 10⁴–10⁷ (as in the original) | TM-0559 |
| `warning_error_6` | `(6 inputs : 6 outputs)` | Generic six-input range checker (hard-coded ranges of the original file's nozzle/orifice model); reports with `CALL ERROR` | TM-0581 |

The two `CALL WARNING` checkers keep the original statements: the branches
fire only for out-of-range inputs (`CS-GAP-CALL-WARNING` — the demo points
stay in range, except where noted below). The functions `velo`,
`coeficiente` and `warning_error_ashrae` are the complete procedure part of
TM-0558; TM-0559 and TM-0558 share the generic `warning_error` shape with
TM-0581 and with the ejector file of `CSL-0118` (same lab toolkit; the three
copies differ only in the hard-coded ranges — see *Conversion log* for the
renames).

## Demonstration program

1. **ASHRAE 41.2 / ISO R859 four-nozzle bank** (the `MODULE flowrate` of
   TM-0558, flattened): four nozzles `d_nz[1..4]` (only `d_nz[3]` = 80 mm
   active, as in the original), `P_atm` = 1 bar, `RH_amb` = 0.5,
   `Dp_nz` = 500 Pa, air at 70 °C over 20 °C ambient. The nozzle bank
   returns the dry-air and humid-air mass flow rates. Throat velocity
   31.03 m/s — inside the 15–35 m/s recommendation.
2. **ISO 5167 long-radius nozzle** (the `MODULE flowrate` of TM-0559,
   flattened): De = 0.8 m, Di = 0.08 m, Δp = 500 Pa, same air state; Stolz
   discharge coefficient `C_D = 0.9965 − 0.00653·β^0.5·(10⁶/Re_D)^0.5`,
   expansibility factor with γ = 1.4. The stored operating point (β = 0.1,
   De = 0.8) is **outside** the ISO validity range of the original's own
   checker; EES printed a warning, CoolSolve would stop on
   `CALL WARNING` (`CS-GAP-CALL-WARNING`), so the checker is demonstrated on
   in-range values next to the flow calculation.
3. **Admission procedure** (TM-0587): choked case (pressure ratio 0.1),
   subsonic case (0.8) and closed-valve case, with a check against the
   published ideal-gas isentropic nozzle forms (relative difference printed
   as `diff_choked_adm`, `diff_sub_adm` — exactly 0).
4. **Range checker** `warning_error_6` with in-range values.

## How to run

```bash
coolsolve ./nozzle_discharge_coefficients.eescode
```

Other models can copy the definitions until `$INCLUDE library:…` works
(`CS-FEAT-IMPORT`).

## Results

At the default points (see `.sol`): nozzle bank `M_dot_ah_cd` = 0.15652 kg/s
with `c_d` = 0.9794 at Re = 1.218·10⁵; long-radius nozzle
`M_dot_a_noz` = 0.15469 kg/s with `C_D` = 0.9777, `epsilon_noz` = 0.9973,
`Re_D` = 1.203·10⁴; admission `m_dot_choked_adm` = 0.18667 kg/s (choked = 1),
`m_dot_sub_adm` = 0.15284 kg/s (choked = 0), `m_dot_closed_adm` = 0.

<!-- FIGURE (maintainer, docs/model_workflow.md §7): no thermodynamic diagram applies;
      a parametric sweep of c_d(Re) or C_D(beta) could serve. -->

## Verification

1. **ASHRAE bank vs the stored solution of TM-0558** (`compare_solution.py`,
   reference = the stored values consistent with the current inputs):

   | Variable | EES stored | CoolSolve | rel. diff |
   |---|---:|---:|---:|
   | `w_amb` = `w_a_su_nz` [-] | 0.0073596 | 0.0073912 | 4.3·10⁻³ |
   | `rho_a_su_nz` [kg/m³] | 1.0034089 | 1.0033581 | 5.1·10⁻⁵ |
   | `v_a_su_nz` [m³/kg] | 0.9966027 | 0.9966532 | 5.1·10⁻⁵ |
   | `v_ha_su_nz` [m³/kg] | 0.9893217 | 0.9893408 | 1.9·10⁻⁵ |
   | `rho_ah_su_nz` [kg/m³] | 1.0107936 | 1.0107741 | 1.9·10⁻⁵ |
   | `mu_a_su_nz` [Pa·s] | 2.0510·10⁻⁵ | 2.0460·10⁻⁵ | 2.4·10⁻³ |

   `7 common variables, 3 differ (rtol=0.001)`: only the humid-air `w` and
   viscosity differ above 10⁻³ (CoolProp vs EES backend, within the ≤ 0.5 %
   tolerance of `docs/ees_import.md` §11). The mass flow rate is not in the
   stored values (cleared before the next run), but the **guess value of the
   matching run** is: EES `M_dot_ah_cd` = 0.1565179395 vs CoolSolve
   0.1565215 (rel. diff 2.3·10⁻⁵); recomputing the bank by hand with the
   EES stored state gives 0.156518 — confirming the guess belongs to the
   current inputs.
2. **ISO 5167 long-radius part.** The stored solution of TM-0559 is
   **stale** (`CS-BUG-EXTRACT-STALE`): `beta_noz` = 0.3714 = 0.026/0.07 and
   `A_De_noz` = π·0.07²/4 belong to an older run (current inputs: 0.08/0.8 →
   β = 0.1), `C_D_noz` = 0.0066 is impossible with its own equation, and
   `Re_D_noz` = 562 is inconsistent with `G_noz`·De/μ. Two independent
   references are used instead:
   - **Equation identity with the CSL-0075 family**: the ISO 5167 part of
     TM-0559 (`E_noz`, `m_noz`, the Stolz `C_D_noz` equation, `tau_noz`,
     `epsilon_noz` and the mass-flow equation) is **character-identical** to
     the sibling file `Model data bank/EES_Functions/iso5167/ISO5167 flow
     rate calculation - long radius.EES` (TM-0256, the long-radius member of
     the CSL-0075 source family; its `warning_error` has the same three
     ranges), whose diaphragm sibling is library model `CSL-0075`.
   - **Recomputation of the demo point** with the EES humid-air state of
     TM-0558 (same state: 70 °C, 1 bar, w = 0.0073596): `M_dot_a_noz`
     0.154688 vs CoolSolve 0.154685 (2·10⁻⁵), `C_D` 0.97765 both,
     `epsilon_noz` 0.99732 both, `V_dot` 0.153036 both.
3. **Admission vs published values**: the choked and subsonic results equal
   the ideal-gas isentropic nozzle equations written with
   `p_0 = rho_0·R_a·T_0` to machine precision (`diff_choked_adm` =
   `diff_sub_adm` = 0): 0.186668 and 0.152845 kg/s at the demo point.

## Source and attribution

Four files of the `procedures EES/` folder of the ULiège collection (lab
toolkit; the `{$ID$}` stamp is the EES licence of the J. Lebrun laboratory,
not the author): `airflow rate - ashrae 41.2.EES` (EES 7.793, comments in
English, decimal comma), `airflowrate - long radius.EES` (EES 7.793),
`tuyere.EES` (EES 8.198, comment in French) and `Out of range warning.EES`
(EES 7.793). No author is named in the files.

Source files, collection of S. Quoilin:
`~/Nextcloud/thermo_models/procedures EES/airflow rate - ashrae 41.2.EES`,
`~/Nextcloud/thermo_models/procedures EES/airflowrate - long radius.EES`,
`~/Nextcloud/thermo_models/procedures EES/tuyere.EES`,
`~/Nextcloud/thermo_models/procedures EES/Out of range warning.EES`
(inventory candidates `TM-0558`, `TM-0559`, `TM-0587`, `TM-0581`).

## Conversion log

- **2026-10-07 — import** (`tools/ees_extract.py`, CoolSolve repository).
  TM-0558 is in `SI MASS DEG BAR C KJ` with decimal commas: converted by
  hand to SI-°C-Pa-J — `P_atm = 1 [bar]` → `1E5 [Pa]`; `Dp_nz = 500` was
  already used as **Pa** by the original flow equation (its own comment says
  `[Pa]` despite the bar setting) and is unchanged; no kJ value occurs. The
  three other files are already SI-PA-C-J. Comments kept or translated to
  English, standard header added.
- **2026-10-07 — MODULE flattened (decision D10), twice.** The
  `MODULE flowrate` of TM-0558 (call 1 → tag `_nz`) and of TM-0559 (call 2 →
  tag `_noz`) are copied into the main program; internal variables keep
  their names except `Re[i]` → `Re_nz[i]` (too generic) and the second
  module's `t_amb` → `t_amb_noz` (collision with demonstration 1). The files
  stay valid EES.
- **2026-10-07 — procedure renames** (function names must be unique in the
  library): the `warning_error` of TM-0558 → `warning_error_ashrae`, of
  TM-0559 → `warning_error_iso5167`, of TM-0581 → `warning_error_6` (the
  name `warning_error` is already used by `CSL-0075` and by `CSL-0118`,
  whose copy carries the ejector's own ranges — same generic toolkit
  procedure, near-identical shape).
- **2026-10-07 — property calls (CS-BUG-HUMIDAIR-PROPS).** `DENSITY(AirH2O,…)`
  returns the 1E4 fallback in CoolSolve: in demonstration 1
  `rho_a_su_nz = 1/VOLUME(AirH2O,…)` (per kg of dry air, as in the original)
  and in demonstration 2 `rho_a_su_noz = (1+w)/volume(AirH2O,…)` (per kg of
  mixture, as in the original). All other humid-air calls (`humrat`,
  `volume`, `viscosity`, `dewpoint`) keep their original form with `w=`.
- **2026-10-07 — indexed SUM (CS-GAP-SUM-INDEXED, registered with this
  model).** `M_dot_ah_cd = sum(M_dot_a_nz[i], i=1, 4)` of TM-0558 is not
  expanded by CoolSolve (the index and the element become symbolic
  unknowns); the demonstration uses the explicit 4-term sum — valid EES,
  same result. `DUPLICATE i=1.4` (decimal-comma range notation of the
  original) is written `i=1,4`.
- **2026-10-07 — dead code removed from `admission`** (TM-0587): the unused
  `m_dot_old` (a parenthesis typo of the choked formula) and the unused
  `M_dot_bis` (algebraically equivalent subsonic form). The equivalent
  published forms are recomputed in demonstration 3 as verification checks;
  no effect on the procedure outputs.
- **2026-10-07 — initial guesses** (`nozzle_discharge_coefficients.initials`,
  from the EES stored values of the matching run): without them the
  nozzle-bank loop has a second, degenerate solution (`c_d` = 0 → `M_dot` = 0
  → `Re` = 0), to which the solver converges from the default guesses.
- **Level justification** (taxonomy §3): 97 equations (1) + largest block 6
  (1) + procedures present (1) + no discretisation (0) + no calibration (0)
  + curated guesses (1) = score 4 → level 3 by the table, **moved to level
  2**: a function library of textbook metering correlations whose equation
  count comes from the demonstration program.

## Limitations and CoolSolve gaps

- The library file runs, but a faithful import of the **source files** would
  be blocked by two registered gaps: `CS-GAP-SUM-INDEXED` (TM-0558 uses the
  indexed `SUM`, worked around in the demonstration as above) and
  `CS-GAP-CALL-WARNING` (TM-0559's checker branches fire at its own
  operating point; in the library file the branches are not taken).
- `CS-GAP-MODULE` (not planned) is not a blocker: the modules are flattened
  (decision D10).
- The `warning_error_6` ranges are those of the original file (a
  nozzle/orifice model not in the collection); they are hard-coded, as in
  the original.
- The discharge coefficient `coeficiente` is the ASHRAE 41.2 / ISO R859
  correlation as written in the source (the current ASHRAE 41.2-2014 RS
  edition uses a different formulation); the Stolz `C_D` of demonstration 2
  is the ISO 5167 long-radius-nozzle equation, as in the original.
- The volume-flow diagnostics of demonstration 2 (`vit_noz`, `vit_noz_int`,
  `V_dot_mh_noz`) inherit the original's definition
  `M_dot_a_noz = V_dot_noz·rho_a_su_noz`, which mixes the dry-air mass flow
  with the mixture density; they are reported as computed (as in the
  original) and do not enter the mass-flow equation.

## Related models

- `CSL-0075` *iso5167_orifice_plate_flow_rate*: same ISO 5167 family
  (diaphragm with corner tappings, 1980 Stolz equation) and the same
  `warning_error`/`fluidprop` toolkit; the long-radius member of its source
  family (TM-0256) carries the identical ISO 5167 part used here.
- `CSL-0118` *air_nozzle_ejector*: choked primary-nozzle flow of the same
  lab toolkit; its `warning_error` copy is the near-identical six-input
  range checker with the ejector's own ranges.
