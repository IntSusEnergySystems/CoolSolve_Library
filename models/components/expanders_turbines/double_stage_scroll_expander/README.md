# Two-stage hermetic scroll expander (correlation model)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0117`

Correlation model of the two-stage hermetic scroll expander measured by
Lemort, Quoilin and Pire. The filling factor and the isentropic effectiveness
of *each stage* are polynomial correlations in ln(r_p) and ln(rho_su),
fitted on 770 operating points of the validated single-stage model. From the
imposed mass flow the model returns the swept volume of each stage, and the
intermediate pressure ratio is solved from the zero-derivative condition
xi = d(epsilon_overall)/d(r_p_1) = 0.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | R245fa |
| **Size** | 55 equations, largest block 24; 3 procedures (correlation + 2 partial derivatives) |
| **Source** | ULiège — EES file `double stage expander SQ101012.EES` (S. Quoilin, 30 September 2010) |
| **Authors** | Sylvain Quoilin (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@7addbbc — verified against the EES stored solution (max rel. diff 3.12e-02, explained) |

## Problem statement

An R245fa two-stage hermetic scroll expander receives 0.1 kg/s of vapour at
the saturation pressure of 130 °C (23.5 bar) superheated by 10 K (140 °C) and
discharges at 2 bar, at 3000 rpm. The correlations (fitted on the validated
single-stage hermetic-scroll model between rho_su = 30–200 kg/m³ and
r_p = 1.2–12) give, for each stage, the filling factor FF and the isentropic
effectiveness epsilon_s as functions of the stage pressure ratio and the
supply density at the stage inlet. The two mass-flow equations
(M_dot = FF·N/60·V_s·rho through each stage) size the swept volumes; the
intermediate pressure ratio r_p_1 is the unknown that zeroes the derivative
xi of the overall effectiveness.

## Model

- `hermeticexpander(r_p, rho_su: phi, epsilon)` — bivariate polynomial fits
  (R² = 99.98 for the filling factor, 99.96 for the effectiveness),
  `CALL WARNING` outside the validity range; `der_rp`/`der_rho` are the
  analytical partial derivatives d(epsilon)/d(ln r_p) and d(epsilon)/d(ln rho).
- Stage 1: expansion from p_su to p_int = p_su/r_p_1, effectiveness applied
  between h_su and the isentropic enthalpy at p_int; stage 2: from p_int to
  p_ex, properties evaluated at the stage-2 inlet density.
- beta = 1 − h_ex,s/h_su = 1 − r_p^((1−gamma)/gamma): the equivalent
  isentropic exponent gamma follows from the overall beta, then beta_1 and
  beta_2 per stage, and epsilon_appr, the approximation of the overall
  effectiveness from the stage effectivenesses.
- xi, the derivative of epsilon_overall w.r.t. r_p_1 (chain rule with
  beta_1_der, beta_2_der and the correlation derivatives), is set to zero.

Default operating point (as in the original file): fluid$ = 'R245fa',
T_sat = 130 °C, T_su_exp = 140 °C, p_ex_exp = 2 bar, N_rot_exp = 3000 1/min,
M_dot = 0.1 kg/s. `phi_single`/`epsilon_single` compare the correlations
applied to the overall pressure ratio (single stage) with the two-stage result.

## How to run

```bash
coolsolve ./double_stage_scroll_expander.eescode
```

## Results (CoolSolve)

| Quantity | Value | EES stored |
|---|---:|---:|
| p_su_exp supply pressure | 23.50 bar | 23.39 bar |
| r_p overall pressure ratio | 11.75 | 11.70 |
| r_p_1_mod / r_p_2_mod stage ratios | 2.730 / 4.303 | 2.727 / 4.289 |
| FF_exp_mod filling factor, stage 1 | 0.9671 | 0.9675 |
| epsilon_1_mod / epsilon_2_mod | 0.5834 / 0.5367 | 0.5825 / 0.5357 |
| epsilon_overall | 0.5643 | 0.5634* |
| W_dot_exp_1_mod / W_dot_exp_2_mod | 1101.5 / 1612.0 W | 1101.6 / 1605.3 W |
| V_s_1_mod / V_s_2_mod swept volumes | 15.11 / 47.50 cm³ | 15.23 / 47.71 cm³* |
| epsilon_single (single-stage comparison) | 0.4889 | 0.4898* |

\* recomputed from the stored enthalpies, filling factors and densities (the
variable was cleared in the EES store without a guess, see *Verification*).

The two-stage arrangement reaches a higher overall effectiveness (0.564) than
the correlations predict for one machine over the same overall pressure ratio
(0.489).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. epsilon_overall vs overall
     pressure ratio (parametric sweep), figures/double_stage_scroll_expander_epsilon.png -->

## Verification

`compare_solution.py double_stage_scroll_expander.sol reference.csv`
(reference = EES stored solution of the source file; module variables compared
under their flattened `_mod` names, see *Conversion log*):

- 54 common variables, 30 above the default rtol = 0.001; **maximum relative
  difference 3.12e-02** (on the derivative diagnostic `der_rp_epsilon_2_mod`).
- Root cause, common to all deviations: the R245fa property difference
  between EES 8.652 (2010) and CoolProp at the fixed state T_sat = 130 °C:
  saturation pressure 2 339 329 vs 2 349 520 Pa (0.44 %), supply density
  135.71 vs 136.90 kg/m³ (0.88 %), enthalpy 505 010 vs 505 211 J/kg (0.04 %),
  entropy 1842.25 vs 1843.45 J/kg-K (0.07 %).
- Downstream amplification: r_p_1_mod 0.11 %, stage effectivenesses
  0.17–0.18 %, epsilon_overall 0.16 %, W_dot_exp_2_mod 0.42 %, swept volumes
  0.4–0.8 %; the slope diagnostics (der_*) reach up to 3.12e-02. Enthalpies,
  entropies, beta and gamma values and W_dot_exp_1_mod agree within 1e-3.
- Reference values: 44 stored EES values; 6 cleared variables whose guess
  column kept the last EES solve (`p_su_exp`, `r_p`, `rho_su_exp`,
  `rho_su_exp_mod`, `phi_single`, `epsilon_single`); 3 cleared without a usable
  guess and recomputed from stored values (`epsilon_overall` from the stored
  enthalpies, `V_s_1_mod` and `V_s_2_mod` from the stored filling factors and
  densities); `r_p_mod` repeats `r_p` (identical equation).

Within the property tolerance of CoolSolve `docs/ees_import.md` §11 (older EES
fluid models: up to a few %, explained): **verified**.

## Source and attribution

Correlations established by **Sylvain Quoilin** (30 September 2010) on the
basis of the validated single-stage model of the hermetic scroll expander
described in: V. Lemort, S. Quoilin and C. Pire, *Experimental Investigation
on a Hermetic Scroll Expander*, 7th International Conference on Compressors
(citation as written in the source file). Measured boundaries:
6.3 < p_su < 18 bar, 89 < T_su < 139 °C, 0.036 < M_dot < 0.121 kg/s,
2.4 < r_p < 6.8, 31 < rho_su < 105 kg/m³; correlation validity range
30 < rho_su < 200 kg/m³, 1.2 < r_p < 12.

Source file (EES 8.652, comments in English), collection of S. Quoilin:
`~/Nextcloud/thermo_models/procedures EES/double stage expander SQ101012.EES`
(inventory candidate `TM-0565`).

## Conversion log

- **2026-10-07 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already SI-C-Pa-J; the EES licence tag (`J. Lebrun laboratory`)
  and the `$bookmark` directive were removed. The comment block of the
  correlation procedure is kept verbatim (citation and validity ranges).
- **MODULE flattened (library decision D10, `CS-GAP-MODULE`)**: the single
  `CALL doubleexpander(fluid$,p_su_exp,p_ex_exp,T_su_exp,N_rot_exp,M_dot:
  epsilon_overall,epsilon_1_mod,epsilon_2_mod,V_s_1_mod,V_s_2_mod)` is
  replaced by a copy of the module equations in the main program. Formal
  inputs map to the same-named main variables; the formal outputs map to the
  actual argument names `epsilon_overall`, `epsilon_1_mod`, `epsilon_2_mod`,
  `V_s_1_mod`, `V_s_2_mod`. Every module-internal variable is renamed with
  the tag `_mod`: r_p→r_p_mod, rho_su_exp→rho_su_exp_mod, s_su_exp→s_su_exp_mod,
  h_su_exp→h_su_exp_mod, r_p_1→r_p_1_mod, r_p_2→r_p_2_mod,
  p_int_exp→p_int_exp_mod, FF_exp→FF_exp_mod, FF_exp_2→FF_exp_2_mod,
  epsilon_s_exp_1→epsilon_s_exp_1_mod, epsilon_s_exp_2→epsilon_s_exp_2_mod,
  h_int_exp→h_int_exp_mod, h_int_exp_s→h_int_exp_s_mod, rho_int_exp→rho_int_exp_mod,
  s_int_exp→s_int_exp_mod, h_ex_exp→h_ex_exp_mod, h_ex_exp_s→h_ex_exp_s_mod,
  h_ex_exp_s_2→h_ex_exp_s_2_mod, h_int_exp_s_bis→h_int_exp_s_bis_mod,
  h_ex_exp_s_2_bis→h_ex_exp_s_2_bis_mod, W_dot_exp_1→W_dot_exp_1_mod,
  W_dot_exp_2→W_dot_exp_2_mod, beta→beta_mod, gamma→gamma_mod,
  beta_1→beta_1_mod, beta_2→beta_2_mod, epsilon_appr→epsilon_appr_mod,
  beta_1_der→beta_1_der_mod, beta_2_der→beta_2_der_mod,
  der_lnrp_epsilon_1→der_lnrp_epsilon_1_mod, der_lnrp_epsilon_2→der_lnrp_epsilon_2_mod,
  der_lnrho_epsilon_2→der_lnrho_epsilon_2_mod, der_rp_epsilon_1→der_rp_epsilon_1_mod,
  der_rp_epsilon_2→der_rp_epsilon_2_mod, der_rho_epsilon_2→der_rho_epsilon_2_mod,
  epsilon_1_der→epsilon_1_der_mod, epsilon_2_der→epsilon_2_der_mod,
  xi→xi_mod, r_p_1_nom→r_p_1_nom_mod. No collision with the main-program
  variables (`r_p` and `rho_su_exp` keep their single-stage call values; the
  module computed the same quantities under its local names). The three
  PROCEDUREs are kept as procedures.
- **Dead code removed**: the `FUNCTION gamma(fluid$,P_1,T_1,P_2)` of the
  original is never called (the name `gamma` is used in the module as a plain
  variable, the value of which is *derived* from beta, not computed by the
  function). The function is removed; the module variable is kept as
  `gamma_mod`.
- The argument comment `"<inputs outputs>"` of the original `Module`/`CALL`
  lines disappeared with the flattening (CoolSolve does not parse comments
  inside argument lists, `CS-GAP-PROC-COMMENT` — moot here).
- The commented-out alternative `//r_p_1 = r_p_1_nom` of the module (earlier
  design: equal pressure ratios) is kept as a comment; the active model solves
  `xi_mod = 0` for r_p_1_mod, which gives 2.730 (EES: 2.727) instead of the
  earlier variant r_p_1_nom_mod = sqrt(r_p_mod) = 3.427 (EES: 3.420); both
  values are stored in the EES file.
- `.initials` renamed accordingly; the stale variables of an earlier file
  version stored in the EES records (rho_su = 30, phi, epsilon,
  der_lnrp_epsilon, der_lnrho_epsilon — the current text never defines them)
  were dropped from the guesses.
- Level score (taxonomy §3): 55 equations → 1; largest block 24 → 1;
  procedures → 1; semi-empirical correlations → 1; total 4 → **level 3**.

## Limitations and CoolSolve gaps

- `CALL WARNING` (validity range check inside `hermeticexpander`) is the
  registered gap `CS-GAP-CALL-WARNING`; it only triggers outside the validity
  range, which is not the case here — CoolSolve prints a parse warning
  ("Unknown function 'WARNING'") but the run is unaffected. Not blocking.
- The correlations extrapolate the single-stage machine behaviour to each
  stage of the two-stage arrangement (as in the original); outside
  30 < rho_su < 200 kg/m³ and 1.2 < r_p < 12 the results carry no
  experimental guarantee (the original warns in EES).
- `epsilon_appr_mod` and the `_bis` enthalpies are diagnostic outputs of the
  original (consistency checks of the beta formalism), kept as computed.

## Related models

- `CSL-0037` *scroll_expander_semi_empirical*: the single-stage scroll
  expander at the semi-empirical level of detail (physical loss sub-models
  instead of correlations), also imported from a flattened EES MODULE.
- `CSL-0084` *orc_expander_pump_empirical_maps*: the same hermetic-scroll
  filling-factor and isentropic-effectiveness correlations in their
  ThermoCycle/Modelica form (R245fa ORC demonstration).
