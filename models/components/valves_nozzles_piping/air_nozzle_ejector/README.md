# Air nozzle ejector (primary nozzle and entrainment)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** (runnable variant ✅ verified) &nbsp;|&nbsp; `CSL-0118`

An **air ejector**: a pressurised primary air flow (index 1) expands through a
converging nozzle into a duct and entrains a low-pressure secondary air flow
(index 0); both flows mix at the nozzle exit plane and diffuse to the
discharge duct. Given the total free air delivery `FAD_tot` and the secondary
mass fraction `FF`, the model computes the mass flows, the nozzle exit state
(isentropic relation, "the geometry is not taken into account", as in the
original), the mixing state, a diffuser efficiency correlated with the nozzle
diameter and `FF`, and the resulting suction pressure `p_0_su_ej` (the
ejector "suction effect"). A `warning_error` procedure checks the validity
range of the six inputs.

Note on the card wording: the primary nozzle is *not* choked at the stored
operating point — the nozzle pressure ratio `tau_noz` = 0.94 is far above the
critical ratio (~0.528 for gamma = 1.4) and the mass flow is computed with a
subsonic orifice-type equation (contraction factor `K_noz`, iso-velocity
expansion factor `epsilon_noz_iso`); no choking criterion appears in the
equations.

| | |
|---|---|
| **Category** | Components › Valves, nozzles and piping |
| **Fluids** | Air (ideal gas) |
| **Size** | 65 equations (largest block: 6), one `warning_error` PROCEDURE |
| **Source** | ULiège collection — `~/Nextcloud/thermo_models/Steady-state models/air-nozzle ejector.EES` (EES 7.793) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory; EES licence stamp of the J. Lebrun lab, no author named in the file) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file **blocked** (`CS-GAP-CALL-WARNING`, `CS-GAP-AIR-ENTHALPY-REF`); runnable variant `air_nozzle_ejector_coolsolve.eescode` verified against the EES stored solution (see *Verification*) |

## Problem statement

An ejector sucks atmospheric air with a pressurised motive flow. The inputs
are the total free air delivery `FAD_tot` [l/s] (260), the secondary mass
fraction `FF` [-] (0.1), the primary supply state `T_1_su_ej` [°C] (30),
`p_1_su_ej` [Pa] (800 000), the secondary supply temperature `T_0_su_ej` [°C]
(30) and the nozzle outlet diameter `D_in_ex_noz` [m] (0.02). The outputs are
the suction pressure `p_0_su_ej`, the suction effect `DELTAp_su_ej` =
`p_1_su_ej` − `p_0_su_ej`, the discharge pressure rise `DELTAp_ex_diff`, the
mass flows and the states of the nozzle exit, mixing plane and discharge.

The commented block of the original file holds another operating point
(`FF` = 0.4254, `FAD_tot` = 140 l/s, `T_1_su_ej` = 143.2 °C, `T_0_su_ej` =
143.6 °C, `p_1_su_ej` = 800 764 Pa, `D_in_ex_noz` = 0.02 m) for which no
reference solution is stored.

## Model

- **Mass flows**: `M_dot_tot = FAD_tot*rho_fad/1000` with `rho_fad` the air
  density at 20 °C / 101 325 Pa; `M_dot_1 = M_dot_tot*(1-FF)`,
  `M_dot_0 = M_dot_tot*FF`, `FAD_1 = M_dot_1/rho_fad`.
- **Primary nozzle**: flow from a subsonic orifice-type equation
  `M_dot_1 = epsilon_noz_iso*K_noz*A_1_ex_noz*sqrt(2*rho_1_su_noz*DELTAp_1_noz)`
  with the contraction (discharge) factor `K_noz` = 0.99 and the iso-velocity
  expansion factor `epsilon_noz_iso` of a square-edged orifice in `beta_noz`
  and `tau_noz = p_0_su_ej/p_1_su_noz`. This equation closes the model: it
  determines `DELTAp_1_noz`, hence the suction pressure `p_0_su_ej`.
- **Nozzle exit state** (isentropic, geometry not taken into account):
  `h_1_ex_noz/h_tot_1_su_noz = (p_0_su_noz/p_tot_1_su_noz)^((gamma-1)/gamma)`,
  `C_1_ex_noz^2/2 = h_tot_1_su_noz - h_1_ex_noz`.
- **Mixing** at the nozzle exit plane: momentum `M_dot_1*C_1_ex_noz =
  M_dot_tot*C_mix_ex_noz`, energy `M_dot_1*h_tot_1_su_noz + M_dot_0*h_tot_0_su_noz
  = M_dot_tot*h_tot_mix_ex_noz`, `p_mix_ex_noz = p_0_su_noz` (hypothesis of
  the original).
- **Diffuser**: `p_mix_ex_diff = p_0_su_noz + DELTAp_ex_diff`; the diffuser
  efficiency is correlated linearly with the nozzle diameter and `FF`
  (`epsilon_diff` polynomial), used through
  `epsilon_diff = C_mix_ex_noz_s^2/C_mix_ex_noz^2` and the isentropic
  discharge relations, from which `DELTAp_ex_diff` (an output) follows.
- `gamma` = `cp/cv` of air at 25 °C; `gamma_noz` at `t_1_su_noz`.

The `warning_error` PROCEDURE checks the six input ranges (e.g. `FF` between
0.18 and 0.46, `FAD_tot` between 126 and 265 l/s) and copies its inputs to
outputs. Note that the stored operating point has `FF` = 0.1, **outside** the
announced range: its warning branch is taken (see *Verification*).

## How to run

```bash
coolsolve ./air_nozzle_ejector_coolsolve.eescode    # variant (verified)
coolsolve ./air_nozzle_ejector.eescode              # native file: blocked, see below
```

- `coolsolve.conf` sets the full solver pipeline (`Newton, TrustRegion, …`).
  With the default Newton-only pipeline, the block containing
  `rho_mix_ex_diff = density(air,h=h_mix_ex_diff,p=p_mix_ex_diff)` fails with
  *SingularJacobian* (the analytic Jacobian carries no ∂ρ/∂h entry; KINSOL
  reports rank 0/3); the full pipeline solves it. Documented here, not
  registered as a gap: nothing shows that EES converges from the same guesses.
- `.initials`: EES stored values as guesses; the `h*` guesses are shifted by
  the enthalpy-reference offset `DELTAh_ref` = 125 873 J/kg (better guesses in
  the CoolSolve reference, see the conversion log). The same file serves the
  variant.
- The native file fails at the default point with *"Unknown procedure:
  warning"*: the `FF` = 0.1 value takes the first range-check branch, and
  `CALL WARNING` is not implemented (registered gap `CS-GAP-CALL-WARNING`).

## Results (default operating point, variant)

| Variable | EES stored | CoolSolve variant | Unit |
|---|---:|---:|---|
| `M_dot_tot` | 0.31309 | 0.31319 | kg/s |
| `M_dot_1` (primary) | 0.281784 | 0.281871 | kg/s |
| `M_dot_0` (secondary) | 0.0313094 | 0.031319 | kg/s |
| `p_0_su_ej` (suction pressure) | 752 245 | 752 322 | Pa |
| `DELTAp_su_ej` (suction effect) | 47 754.9 | 47 677.9 | Pa |
| `DELTAp_ex_diff` (discharge rise) | 18 650.2* | 18 619 | Pa |
| `C_1_ex_noz` (nozzle exit velocity) | 103.962 | 104.039 | m/s |
| `epsilon_diff` (diffuser efficiency) | 0.490109* | 0.490109 | − |
| `p_mix_ex_diff` (discharge pressure) | 770 895 | 770 941 | Pa |

\* The stored cells `FF` = 0.4 and `DELTAp_ex_diff` = 5000 are **post-solve
edits** (see *Verification*); the consistent stored run gives 0.1 and
18 650.2, which the model reproduces.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/ -->

## Verification

Reference: the EES stored solution of the source file
(`reference/ees_variables.csv` of the extraction), for the **runnable
variant**. **Provenance of the inputs**: the equations window leaves 6
degrees of freedom; there is no parametric table and no equation for four of
them — they were fixed in EES through the Variable Information dialog. The
commented decimal-comma block of the file (`FF=0,4254, FAD_tot=140,
T_1_su_ej=143,2, T_0_su_ej=143,6, p_1_su_ej=800764, D_in_ex_noz=0,02`) is an
inactive older operating point; none of its values matches the stored cells.
The audit below shows that the stored set is **one consistent solved run**
whose inputs are those of the last column:

| Input | In the EES file | Stored cell | Value in the solved run (audit) |
|---|---|---:|---|
| `FF` | no equation; commented block 0.4254 | 0.4 | **0.1** — `M_dot_0 = M_dot_tot*FF` rel 3e-11, `M_dot_1 = M_dot_tot*(1-FF)` rel 2e-10, `epsilon_diff` polynomial = `C_mix_ex_noz_s^2/C_mix_ex_noz^2` = 0.490109 (exact), `var1_out` = 0.1 (the copy the range-check procedure made during that run) |
| `FAD_tot` | `FAD_tot = M_dot_tot/rho_fad*1000` | 260 | 260 (closes exactly: `M_dot_tot` = 0.313094 = 260/1000·`rho_fad`) |
| `T_1_su_ej` | no equation; commented block 143.2 °C | 30 | 30 (`rho_1_su_noz` = 9.19405 = ρ(30 °C, 8 bar); `h_tot_1_su_noz` = h(30 °C)) |
| `T_0_su_ej` | no equation; commented block 143.6 °C | 30 | 30 (same check on the secondary side) |
| `p_1_su_ej` | `p_1_su_ej = p_0_su_ej + DELTAp_su_ej`; commented block 800 764 | 800 000 | 800 000 (closes with the stored `DELTAp_su_ej` = 47 754.9) |
| `D_in_ex_noz` | no equation; commented block 0.02 | 0.02 | 0.02 |

**FF = 0.4254 and the stored cell FF = 0.4 are both excluded**: they predict
`M_dot_0` = 0.1332 / 0.1252 against the stored 0.0313 (rel 3.3 / 3.0),
`M_dot_1` = 0.1799 / 0.1879 against 0.2818 (rel 0.36 / 0.33), and —
decisively — the two `epsilon_diff` equations would contradict *each other*
(polynomial 0.853 / 0.825 vs `C_s^2/C^2` = 0.490109), which cannot happen in
a solved state; with FF = 0.1 both give exactly 0.490109. The two stale
cells (`FF` = 0.4, `DELTAp_ex_diff` = 5000; plus `epsilon_diff` = 0.824691,
its consequence through the polynomial) are the only 3 of the 65 stored
values that violate closure — the user edited them after the last solve and
saved without re-solving. The import therefore fixes the inputs at the
stored-solution point and the comparison uses the consistent values for the
three stale cells.

`python3 tools/compare_solution.py air_nozzle_ejector_coolsolve.sol reference/ees_variables.csv`
→ *65 common variables, 24 differ (rtol=0.001); only in EES: 0; only in
CoolSolve: 2* (`DELTAh_ref` and its duplicate). The 24 differences fall into
four explained groups:

1. **Stale stored cells** (3 variables): `FF` (7.50e-01, stored 0.4 vs solved
   0.1), `DELTAp_ex_diff` (7.31e-01, stored 5000 vs solved 18 619) and
   `epsilon_diff` (4.06e-01, stored 0.824691 = polynomial at FF = 0.4 vs
   0.490109 = polynomial at FF = 0.1, which also equals
   `C_mix_ex_noz_s^2/C_mix_ex_noz^2` exactly). Post-solve edits, see above.
2. **Enthalpy reference offset** (7 `h*` variables, rel. diff 2.9e-01 to
   3.0e-01): the CoolSolve ideal-gas `Air` enthalpy keeps CoolProp's
   arbitrary reference, 125 873 J/kg above the EES reference at 30 °C. The
   enthalpy *differences* used by the model (kinetic energies, mixing) agree;
   `DELTAh_ref` removes the offset from the three ratio equations of the
   variant.
3. **Property backend** (CoolProp vs EES air data, the remaining 14
   variables): `gamma` 1.27e-03 (CoolSolve 1.40177 vs EES 1.39999), densities
   up to 2.83e-03, and the derived velocities/pressure drops; the largest is
   `p_dyn_mix_ex_diff` at **3.44e-03** — within the "different equation of
   state" tolerance (≤ 0.5 %) of CoolSolve `docs/ees_import.md` §11. The main
   outputs agree to 1.0e-04 (`p_0_su_ej`), 6.0e-05 (`p_mix_ex_diff`) and
   7.4e-04 (`C_1_ex_noz`).

Without the `DELTAh_ref` correction (i.e. in the native file, if it ran), the
reference-sensitive equations would deviate far beyond any tolerance:
`C_1_ex_noz` +19 % (+41 % on `C_1_ex_noz^2/2`), silently.

## Source and attribution

- Source: `~/Nextcloud/thermo_models/Steady-state models/air-nozzle ejector.EES`
  (EES 7.793, file dated 2010-03-30; companion `air-nozzle ejector.pdf` in the
  same folder). Inventory row TM-0593 of `sources/thermo_models/inventory.csv`,
  triage card C-121 (batch B-10), import card C-129.
- Authors: none named in the file; EES licence stamp `{$ID$ #1206: Jean
  Lebrun, Laboratoire de Thermodynamique, Univ. Liege}` → TBD (ULiège
  Thermodynamics Laboratory).
- No external reference is cited in the file; the `epsilon_noz_iso` factor is
  the ISO-5167-style iso-velocity expansion factor of a square-edged orifice
  (form only; no source given in the original, as in the original).

## Conversion log

- **2026-10-07 — import**: extracted with `tools/ees_extract.py` (EES 7.793,
  unit system already `SI MASS DEG PA C J` — no unit conversion; decimal
  point convention; no lookup or parametric tables). Comments kept (English;
  the French inline "hypothèse" is kept as a quoted comment). The PROCEDURE
  was moved after the main-program equations (Cosmetic; equations unchanged).
- **2026-10-07 — inputs restored**: the equations window leaves 6 degrees of
  freedom; four of the six inputs of the author's commented block (`FF`,
  `T_1_su_ej`, `T_0_su_ej`, `D_in_ex_noz`) have no equation (fixed in EES
  through the Variable Information dialog, bounds ±inf), `FAD_tot` and
  `p_1_su_ej` have one. The import gives the six values of the
  stored-solution run as equations (provenance table in *Verification*;
  `FF` = 0.1 — the commented 0.4254 and the stored 0.4 both contradict the
  solution). No unknown of the original was fixed to a stored value; the
  stored unknowns went to `.initials`.
- **2026-10-07 — variant `air_nozzle_ejector_coolsolve.eescode`** (each
  change forced by a registered gap, file still valid EES):
  1. `CS-GAP-AIR-ENTHALPY-REF`: the three absolute-enthalpy *ratio* equations
     (nozzle exit state, diffuser isentropic relations) are written with
     EES-reference enthalpies `(h - DELTAh_ref)`, with the constant
     `DELTAh_ref = enthalpy(air,t=30) - 303595.0691` (the EES stored enthalpy
     of air at 30 °C, the anchor temperature of this model). All enthalpy
     *difference* equations are unchanged (reference-invariant), as are the
     `(h,P)` and `(h)` property calls (self-consistent within each backend).
  2. `CS-GAP-CALL-WARNING`: the six range-check `IF … then call warning(…)`
     statements of `warning_error` are removed (their branch cannot execute
     in CoolSolve); the input copies remain.
- **Guesses**: `.initials` = EES stored values; the `h*` entries shifted by
  +125 872.97 J/kg (CoolSolve reference). Needed for the native file as well.
- **No D10/D11 rewrites**: no MODULE/SUBPROGRAM, no (T,H) property pair.
- **Level**: equations 65 → 1; largest block 6 → 1; procedure present → 1;
  single component → 0; semi-empirical correlation (`epsilon_diff` polynomial)
  → 1; curated guesses + pipeline needed → 1. Score 5 → **level 3**.

## Limitations and CoolSolve gaps

- The `epsilon_diff` polynomial is fitted on the lab rig around the explored
  range (its warning ranges: `FF` 0.18–0.46, `FAD_tot` 126–265 l/s, supply
  temperatures 10–160 °C, `p_1_su_ej` 6.2–8.2 bar, `D_in_ex_noz` 0.018–0.02 m);
  the stored operating point (`FF` = 0.1) lies outside the `FF` range.
- `CS-GAP-CALL-WARNING` (registered): `CALL WARNING` raises *"Unknown
  procedure: warning"* when its branch is taken — the case here at the
  default point (`FF` < 0.18). Blocks the native file.
- `CS-GAP-AIR-ENTHALPY-REF` (registered by this import): the ideal-gas `Air`
  enthalpy of CoolSolve keeps CoolProp's arbitrary reference (EES: ∫₀ᵀ cp dT,
  303 595.07 J/kg at 30 °C); this model takes ratios of absolute enthalpies,
  which are reference-dependent — silently wrong results (+19 % on the nozzle
  exit velocity). Blocks the native file.
- Solver note (not a gap): the `density(air,h=…,p=…)` block needs the full
  solver pipeline of `coolsolve.conf` (see *How to run*).

## Related models

None in the library yet. The discarded fragment TM-0573 (nozzle throat
SUBPROGRAM) was superseded partly by this model (triage card C-121).
`CSL-0122` *nozzle_discharge_coefficients* ships the near-identical
six-input `warning_error` range checker of the same lab toolkit (with the
TM-0581 ranges) as a function library.
