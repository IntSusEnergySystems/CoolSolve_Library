# Air nozzle ejector (primary nozzle and entrainment)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0118`

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
| **Size** | 70 equations (largest block: 6), one `warning_error` PROCEDURE |
| **Source** | ULiège collection — `~/Nextcloud/thermo_models/Steady-state models/air-nozzle ejector.EES` (EES 7.793) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory; EES licence stamp of the J. Lebrun lab, no author named in the file) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 

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
- **Nozzle exit state** (isentropic, constant `gamma`, geometry not taken into
  account), with absolute temperatures:
  `(T_1_ex_noz+273.15)/(t_1_su_noz+273.15) = (p_0_su_noz/p_tot_1_su_noz)^((gamma-1)/gamma)`,
  `h_1_ex_noz = enthalpy(air,t=T_1_ex_noz)`,
  `C_1_ex_noz^2/2 = h_tot_1_su_noz - h_1_ex_noz`.
- **Mixing** at the nozzle exit plane: momentum `M_dot_1*C_1_ex_noz =
  M_dot_tot*C_mix_ex_noz`, energy `M_dot_1*h_tot_1_su_noz + M_dot_0*h_tot_0_su_noz
  = M_dot_tot*h_tot_mix_ex_noz`, `p_mix_ex_noz = p_0_su_noz` (hypothesis of
  the original).
- **Diffuser**: `p_mix_ex_diff = p_0_su_noz + DELTAp_ex_diff`; the diffuser
  efficiency is correlated linearly with the nozzle diameter and `FF`
  (`epsilon_diff` polynomial), used through
  `epsilon_diff = C_mix_ex_noz_s^2/C_mix_ex_noz^2` and the isentropic
  discharge relations (constant `gamma`, absolute temperatures `T_mix_ex_noz`,
  `T_tot_mix_ex_diff_s`, `T_tot_mix_ex_diff`, `T_mix_ex_diff` taken from or
  converted to the enthalpies by property calls), from which `DELTAp_ex_diff`
  (an output) follows.
- `gamma` = `cp/cv` of air at 25 °C; `gamma_noz` at `t_1_su_noz`.

The `warning_error` PROCEDURE checks the six input ranges (e.g. `FF` between
0.18 and 0.46, `FAD_tot` between 126 and 265 l/s) and copies its inputs to
outputs. Note that the stored operating point has `FF` = 0.1, **outside** the
announced range: its warning branch is taken (see *Verification*).

## How to run

```bash
coolsolve ./air_nozzle_ejector.eescode
```

- `coolsolve.conf` sets the full solver pipeline (`Newton, TrustRegion, …`).
  With the default Newton-only pipeline and without the guesses of the
  `.initials`, the block containing
  `rho_mix_ex_diff = density(air,h=h_mix_ex_diff,p=p_mix_ex_diff)` fails with
  *SingularJacobian* (the analytic Jacobian carries no ∂ρ/∂h entry); the full
  pipeline, or the guesses, solve it. 
- `.initials`: EES stored values as guesses; the `h*` guesses are shifted by
  125 873 J/kg, the difference between the reference enthalpy of `Air` in EES
  and in CoolProp at 30 °C (better guesses for CoolSolve, see the conversion
  log).
- The run reports the `CALL WARNING` of `warning_error` that hold at the
  solution (diagnostic `W001`, on the standard error): `FF` = 0.1 is below the
  announced range 0.18–0.46 and, only through a CoolSolve round-off (see
  *Limitations*), `D_in_ex_noz` = 0.02 is reported as above the upper bound 0.02.
  The calculation goes on; the results are not affected.

## Results (default operating point)

| Variable | EES stored | CoolSolve | Unit |
|---|---:|---:|---|
| `M_dot_tot` | 0.31309 | 0.31319 | kg/s |
| `M_dot_1` (primary) | 0.281784 | 0.281871 | kg/s |
| `M_dot_0` (secondary) | 0.0313094 | 0.031319 | kg/s |
| `p_0_su_ej` (suction pressure) | 752 245 | 752 322 | Pa |
| `DELTAp_su_ej` (suction effect) | 47 754.9 | 47 677.9 | Pa |
| `DELTAp_ex_diff` (discharge rise) | 18 650.2* | 18 621 | Pa |
| `C_1_ex_noz` (nozzle exit velocity) | 103.962 | 104.295 | m/s |
| `epsilon_diff` (diffuser efficiency) | 0.490109* | 0.490109 | − |
| `p_mix_ex_diff` (discharge pressure) | 770 895 | 770 944 | Pa |

\* The stored cells `FF` = 0.4 and `DELTAp_ex_diff` = 5000 are **post-solve
edits** (see *Verification*); the consistent stored run gives 0.1 and
18 650.2, which the model reproduces.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/ -->

## Verification

Reference: the EES stored solution of the source file
(`reference/ees_variables.csv` of the extraction), for the native file.
**Provenance of the inputs**: the equations window leaves 6
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

`python3 tools/compare_solution.py air_nozzle_ejector.sol reference/ees_variables.csv`
→ *65 common variables, 27 differ (rtol=0.001); only in EES: 0; only in
CoolSolve: 6* (the five temperatures added to the isentropic relations and
`pi`). The 27 differences fall into four explained groups:

1. **Stale stored cells** (3 variables): `FF` (7.50e-01, stored 0.4 vs solved
   0.1), `DELTAp_ex_diff` (7.31e-01, stored 5000 vs solved 18 621) and
   `epsilon_diff` (4.06e-01, stored 0.824691 = polynomial at FF = 0.4 vs
   0.490109 = polynomial at FF = 0.1, which also equals
   `C_mix_ex_noz_s^2/C_mix_ex_noz^2` exactly). Post-solve edits, see above.
2. **Enthalpy reference offset** (8 `h*` variables, rel. diff 2.9e-01 to
   3.0e-01): the CoolSolve ideal-gas `Air` enthalpy keeps CoolProp's
   arbitrary reference, 125 873 J/kg above the EES reference at 30 °C. The
   enthalpy *differences* used by the model (kinetic energies, mixing) agree,
   and the isentropic relations, written with absolute temperatures, do not
   depend on the reference.
3. **Property backend** (CoolProp vs EES air data, 13 variables): `gamma`
   1.27e-03 (CoolSolve 1.40177 vs EES 1.39999), densities up to 2.83e-03, and
   the derived pressure drops and dynamic pressures; the largest is
   `p_dyn_mix_ex_diff` at **3.44e-03** — within the "different equation of
   state" tolerance (≤ 0.5 %) of CoolSolve `docs/ees_import.md` §11. The main
   outputs agree to 1.0e-04 (`p_0_su_ej`), 6.3e-05 (`p_mix_ex_diff`) and
   3.1e-04 (`M_dot_tot`, `M_dot_1`, `M_dot_0`).
4. **Isentropic relation form** (the three velocities `C_1_ex_noz`,
   `C_mix_ex_noz`, `C_mix_ex_noz_s`, 3.19e-03; the nozzle-exit, mixing and
   diffuser-exit temperatures, derived from the stored enthalpies, agree to
   0.035 K): EES takes the ratio of absolute enthalpies (h = ∫₀ᵀ cp dT), while
   the model written with the temperature ratio is the isentropic relation of
   constant `gamma`. With a variable `cp`, `h/T` (1001.5 J/kg-K at 30 °C) is
   not `cp` (1006.5 J/kg-K): the kinetic energy of the nozzle,
   `C_1_ex_noz^2/2`, is 0.49 % larger with the temperature ratio (5 439 vs
   5 412 J/kg), i.e. +0.25 % on the velocity, on top of the 7.4e-04 of the
   property backend. An isentropic state at constant entropy (variable `cp`,
   `entropy(air,t=…,p=…)`) would give 5 451 J/kg (+0.23 %).

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
- **2026-10-11 — isentropic relations**: written with absolute-temperature
  ratios instead of absolute-enthalpy ratios, valid for any enthalpy reference
  (`(T_ex+273.15)/(T_su+273.15) = (p_ex/p_su)^((gamma-1)/gamma)` with the
  enthalpy from `enthalpy(air,t=…)`/`temperature(air,h=…)`; five temperature
  variables added: `T_1_ex_noz`, `T_mix_ex_noz`, `T_tot_mix_ex_diff_s`,
  `T_tot_mix_ex_diff`, `T_mix_ex_diff`). The enthalpy *difference* equations
  and the `(h,P)`/`(h)` property calls are unchanged.
- **Guesses**: `.initials` = EES stored values; the `h*` entries shifted by
  +125 872.97 J/kg (CoolProp's reference of `Air`).
- **No D10/D11 rewrites**: no MODULE/SUBPROGRAM, no (T,H) property pair.
- **Level**: equations 70 → 1; largest block 6 → 1; procedure present → 1;
  single component → 0; semi-empirical correlation (`epsilon_diff` polynomial)
  → 1; curated guesses + pipeline needed → 1. Score 5 → **level 3**.

## Limitations and CoolSolve gaps

- The `epsilon_diff` polynomial is fitted on the lab rig around the explored
  range (its warning ranges: `FF` 0.18–0.46, `FAD_tot` 126–265 l/s, supply
  temperatures 10–160 °C, `p_1_su_ej` 6.2–8.2 bar, `D_in_ex_noz` 0.018–0.02 m);
  the stored operating point (`FF` = 0.1) lies outside the `FF` range.
- The six range checks of `warning_error` are `CALL WARNING` statements and
  CoolSolve reports the ones that hold at the solution, not those of the
  Newton iterates. At the default point `FF` = 0.1 lies below its range (0.18–0.46),
  which is reported. A second warning, `D_in_ex_noz` = 0.02 above 0.02, is a
  CoolSolve round-off and not a property of the model: the solution of the
  equation `D_in_ex_noz = 0.02` is 0.02 + 1.7e-17 (the explicit solve computes
  it as `x0 − (x0 − 0.02)`), so the check `var6_in > 0.02` fires on the bound.
- The isentropic relations take a constant `gamma` (`cp/cv` at 25 °C), as in
  the source; at constant entropy with the variable `cp` of air the nozzle
  kinetic energy would be 0.23 % larger (see *Verification*).
- Solver note (not a gap): the `density(air,h=…,p=…)` block needs the full
  solver pipeline of `coolsolve.conf` or the `.initials` guesses (see *How to run*).

## Related models

None in the library yet. The discarded fragment TM-0573 (nozzle throat
SUBPROGRAM) was superseded partly by this model (triage card C-121).
`CSL-0122` *nozzle_discharge_coefficients* ships the near-identical
six-input `warning_error` range checker of the same lab toolkit (with the
TM-0581 ranges) as a function library.
- `CSL-0310` *isentropic_nozzle_critical*: the standalone isentropic nozzle with critical pressure and choking, of which the ejector primary nozzle is the unchoked orifice form.
