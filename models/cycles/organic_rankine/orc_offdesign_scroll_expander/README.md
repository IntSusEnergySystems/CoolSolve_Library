# CSL-0312 · `orc_offdesign_scroll_expander`

Off-design organic Rankine cycle (R1233zd(E)) with a Lemort semi-empirical scroll
expander, a pump on similarity laws with rated curves and two SWEP P200THx140
brazed-plate heat exchangers in a moving-boundary formulation. Translation of
LaboThapPy `machine/examples/ORC/fpi_orc_example.py`, study case `off_design`.

> 🔴 **Level 4 · Research** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ❌ **Failing** (solver convergence; review of 2026-11-01) &nbsp;|&nbsp; `CSL-0312`

| | |
|---|---|
| Category | `cycles/organic_rankine` |
| Kind | steady (one operating point, imposed `m_dot`) |
| Status | **failing** — square system (226 equations / 226 unknowns), the coupled heat-exchanger block does not converge in CoolSolve (diagnosis below) |
| Fluids | R1233zd(E), Water |
| Origin | software library (LaboThapPy, ULiège) |

## Source and attribution

- **Original model**: Basile **Chaudoir** and Elise **Neven** (ULiège
  Thermodynamics Laboratory), LaboThapPy,
  https://github.com/PyLaboThap/LaboThapPy , commit `f03f7f47`,
  `labothappy/machine/examples/ORC/fpi_orc_example.py` (study case
  `off_design`), `labothappy/component/expander/expander_semi_empirical.py`,
  `labothappy/component/heat_exchanger/hex_MB_charge_sensitive.py`,
  `labothappy/component/pump/pump_curve_similarity.py`,
  `labothappy/toolbox/geometries/heat_exchanger/geometry_plate_hx_swep.py`,
  `labothappy/correlations/convection/plate_htc.py`. Local clone `~/git/LaboThapPy`.
- **Licence**: the source repository is Apache-2.0 (`LICENSE.txt`); credited and
  linked as above. This translation is published under the library licence (MIT).
- **Physics references** (cited by the source):
  - expander: V. Lemort, *Contribution to the Characterization of Scroll
    Machines in Compressor and Expander Modes*, PhD thesis, ULiège, 2008
    (semi-empirical model, as in the original);
  - heat exchangers: I. H. Bell, *A generalized moving-boundary algorithm to
    predict the heat transfer rate of counterflow heat exchangers for any phase
    configuration* (moving-boundary model of the source class);
  - correlations: H. Martin, Chem. Eng. Process. 35 (1996) 301–310 (VDI Heat
    Atlas, single-phase chevron plates, `martin_holger_plate_HTC`); M. Amalfi,
    F. Vakili-Farahani & J. R. Thome (boiling chevron plates,
    `amalfi_plate_HTC`); M. M. Shah 2021 with the Longo et al. 2015
    forced-convection term (condensation chevron plates,
    `shah_condensation_plate_HTC`); G. Longo & A. Gasparella (water side,
    `water_plate_HTC`); Zivi void fraction (charge); pump similarity laws.
  - the R1233zd(E) thermal conductivity used by the source (Perkins & Huber
    2017, `conducticity_R1233zd`) is the function of library model `CSL-0132`,
    copied into this file per workflow §4 (`$INCLUDE` not available yet,
    `CS-GAP-INCLUDE`).

## Niche

First **off-design** cycle of the library and the only model combining a
calibrated semi-empirical scroll expander (Lemort: suction drop, suction/exhaust
heat transfer, leakage, built-in volume ratio, mechanical losses) with a
similarity-law pump (speed solved from the head curves) and moving-boundary
plate heat exchangers with refrigerant charge (Zivi). Nearest models:
`CSL-0134` / `CSL-0153` (design-point ORCs on constant efficiencies),
`CSL-0138` (moving-boundary HX component alone), `CSL-0013` (steady heat-pump
cycle from TESPy). The off-design behaviour (expander speed, pump speed,
pressures and heat-transfer coefficients all floating) is the new physics.

## Structure of the translation

The sequential-modular Python circuit (DFS component solves, Wegstein
iteration, one residual variable: expander exhaust pressure vs 7 K pump-suction
subcooling) becomes one simultaneous system: the low pressure `P_1` is an
unknown closed by `T_1 = T_sat(P_1) - 7 K` (the source's iteration target), the
high pressure is the fixed source guess `P_2 = Psat(60 °C)`. The expander's
internal `fsolve` on the wall temperature becomes the wall energy balance
`Q_dot_su + W_dot_loss = Q_dot_ex + Q_dot_amb` (single unknown `T_w_x` in `P_M`
mode, as in the original). The pump's `root_scalar` head balance becomes the
similarity equation `H_curve(V_dot*2900/N_pu)*(N_pu/2900)^2 = H_req`. The
curves are piecewise-linear with linear extrapolation, written in ReLU form
(identical to a linear interpolation of the rated points).

Heat exchangers: zone-wise (SH / 2P / SC) moving-boundary formulation. Zone
areas are split proportionally to the zone heat rates — the same heat-rate
weighting the source uses for its cells (`Qdot_c_rel`); the per-zone `UA` uses
the source's plate formula `1/((1+fooling)/(alpha_h*A_h) + 1/(alpha_c*A_c))`.
The overall balance `Q = Σ UA_z*LMTD_z` replaces the source's `brentq` root
find on `Q`.

## Verification

- **Expander and pump: verified against a re-run of the source components**
  (standalone drivers on the same inputs, CoolProp 8.0.0; no transport
  properties needed by these two components):

  | variable | source re-run | CoolSolve | rel. diff |
  |---|---|---|---|
  | pump `N_pu` [rpm] | 1760.2913312 | 1760.2913313 | 6e-11 |
  | pump `eta_pu` [-] | 0.19893095459 | 0.19893095460 | 5e-12 |
  | pump `W_dot_pu` [W] | – | 495.27 | – |
  | expander `h_x_ex` [J/kg] | 455299.18 | 455301.83 | 5.8e-6 |
  | expander `W_dot_x` [W] | 7564.56 | 7564.56 | 2e-7 |
  | expander `eta_x_is` [-] | 0.622934 | 0.622934 | <1e-6 |
  | expander `N_x_rot` [rpm] | 10143.5 | 10143.52 | 2e-6 |
  | expander `eps_x_v` [-] | 1.0282 | 1.028232 | 3e-5 |
  | expander `T_w_x` [°C] | 93.44 (366.59 K, rounded) | 93.464 | 2.5e-4 |

  (`tools/compare_solution.py` was not applicable — the reference here is a
  printed Python output, not an EES variable file; the comparison was done with
  the driver scripts of the work folder, deleted after the import.)

- **Full cycle: not solved** (status `failing`). The system is square (226/226)
  but the 129–138-equation coupled block (both plate HXs + expander + pump)
  does not converge: Newton/TrustRegion/Levenberg-Marquardt and multi-start all
  stall between 3.5e7 and 4e8 initial residual, with ~72 000 CoolProp
  evaluations outside validity along the iterations. Attempts: extended
  `.initials`, `solverPipeline` variants, a fixed-coupler bootstrap file (its
  43-equation condenser block also stalls, best residual ~14 000), and removal
  of the pressure-drop feedback from the zone pressures (kept: see conversion
  log). Not attempted yet: tearing the HX zones into per-zone blocks, smarter
  initialisation of the condenser, or an even stronger decoupling.

- **The source example itself cannot be re-run as committed** (three
  independent causes at `f03f7f47`, established with driver scripts in the work
  folder):
  1. the circuit setup pass solves the evaporator with a cold-side `m_dot` of 0
     (pump output not yet propagated) → division by zero in
     `martin_holger_plate_HTC` (`Re = 0`) inside the first `brentq` bracket;
  2. CoolProp has **no transport model for R1233zd(E)** (tested up to 8.0.0:
     `PropsSI('V', …)` raises *"Viscosity model is not available for this
     fluid"*; `AbstractState.viscosity()` returns `inf`) → every plate
     correlation on the refrigerant side crashes. The CoolSolve build links a
     CoolProp 8.1.0dev **which has the viscosity**, so the EES translation is
     not affected;
  3. the plate heat exchangers request `pressure_drop_pipe_*` with plate
     correlation names (`martin_holger_plate_HTC`, `water_plate_HTC`, …) that
     the pipe pressure-drop dispatcher does not implement.
  Consequently no reference numbers exist for the two heat exchangers at this
  commit; their equations follow the source correlations and geometry but could
  only be checked for plausibility, not against source output.

## Source formulation (utilisation weights) and solver diagnosis

Second continuation (orchestrator review, 2026-10-31, ~60 min). The source's
own closure was read out of `hex_MB_charge_sensitive.py` and implemented:

- per zone (SH/2P/SC) the per-area conductance `k_z = 1/((1+fooling)/alpha_h +
  1/alpha_c)` — the source's `UA_avail[k]/A` with the **total** plate areas;
- the utilisation `w_z = UA_req,z/UA_avail,z = Q_z/(k_z*A*LMTD_z)` — the
  zone-wise image of the source's `w[k] = UA_required[k]/UA_available[k]`
  (an area fraction: `A_vec_h[k] = w[k]*A_h` there);
- the **closure** `sum(w) = 1` — the source's brentq objective `1 - w_sum`
  (the zones together share the whole plate area);
- the refrigerant pressure drops weighted by the utilisation, as the source's
  `DP_H*w[k]/max(sum(w),1)` (with `sum(w) = 1`);
- the charge volumes proportional to `w_z` (the source: volumes proportional
  to the area).

This replaces the earlier (infeasible) heat-share area split `A_z = A*Q_z/Q`:
with the source's closure the cycle point exists (the earlier no-root analysis
applied to the replaced formulation only).

Solver status: the system is square (231 equations / 231 unknowns, largest
block 134). Levenberg-Marquardt (coolsolve.conf:
`solverPipeline = LevenbergMarquardt, TrustRegion, Newton`) drives the block
residual from 2.2e5 to 25.5 in 500 iterations and to ~900 at 1500 — steady
convergence, but the iteration budget of any single run is exhausted before
the tolerance; Newton and TrustRegion reject their line searches in the same
block. Validity-window guards on the correlation inputs (inactive at the
solution) are in place. Status stays **failing**: a faithful model whose
134-equation block does not converge in CoolSolve within a practical iteration
budget. Next lever for a re-check: a split/teared solve of the block (HX by
HX), or CoolSolve LM with a larger iteration budget on faster hardware.

## Review of 2026-11-01 (failing models)

Classification: **failing, solver convergence** — the system is square and
a solution should exist (see below), but CoolSolve does not converge the
134-equation coupled block, also with **Try Harder**. Findings:

- **Bug of the translation, corrected.** The six LMTD guards were written
  `IF(-E, -1E-6, f, DTA, f)` with `f = (DTA − DTB)/ln(DTA/DTB)`: for
  `E = |DTA/DTB − 1| < 1e-6` the five-argument `IF` returns its *last*
  argument, i.e. `f` again (0/0), so the guard never protected the
  `DTA ≈ DTB` case. The last argument is now `DTA`.
- **Solver behaviour** (CoolSolve 0.4.0, also with the AD fix of the CoolSolve
  branch `fix/ad-pow-negative-base`; shipped `.initials`): Levenberg–Marquardt
  brings the block residual from 2.18·10⁵ to 6.2·10³ in about 50 iterations
  and then stalls: the damping saturates at 10⁸ and the step is zero for the
  remaining iterations, i.e. a **local minimum of ‖F‖**, not slow
  convergence (a 300-iteration LM run shows it in 24 s). With the shipped
  coolsolve.conf (`LevenbergMarquardt, TrustRegion, Newton`,
  `maxIterations = 20000`) the solver spends the whole budget after that
  stall and runs past 20 min; Try Harder also runs past its 15–25 min test
  timeouts. The most likely cause is the non-smooth clamps
  `Max(ΔT, 1E-6)` on the zone temperature differences: when one is active its
  derivative is zero and the residual surface is flat in that direction (a
  temperature cross inside a zone during the iterations).
- **Validity of the translation.** The physics of the source is sound, but
  (i) the source example cannot be run at commit `f03f7f47` (three
  independent errors, see *Verification*), so the cycle has no reference;
  (ii) the translation departs from the source (3-zone moving boundary
  instead of the source's cells, two-phase correlations at one mean quality,
  pressure-drop feedback removed from the zone states, the `1.95*KEV*1000`
  "kPa" factor kept as written); (iii) the expander and the pump are verified
  against the source components. If the model converged it would be
  `modified`, not `verified`.
- Correction of a statement below: EES does **not** accept IF–THEN–ELSE blocks
  in the main equations window either (only inside FUNCTION/PROCEDURE), so the
  inline five-argument `IF` used for the guards is the right EES form; there
  is no CoolSolve gap there.

Hints for CoolSolve: (a) when LM saturates its damping with a non-zero
residual, report it as a local minimum and restart from a perturbed point
(the multi-start of Try Harder perturbs only thermodynamic blocks from
reference states); (b) smooth `MAX`/`MIN` (soft-plus with a small width) as
an option would remove the flat regions; (c) the coupled block contains both
heat exchangers: tearing them apart (condenser at fixed `P_1`, evaporator at
fixed `P_2`, then the closure on the subcooling, as the source's
sequential-modular solver does) would give two smaller blocks. Hint for the
model: use a smooth LMTD approximation (e.g. Chen's) instead of the clamped
log form. The maintainer may also consider dropping the model (no reference
for the cycle, heavily modified translation); it is kept as `failing` here.

## Continuation attempt (orchestrator review, 2026-10-31)

A structured stepwise continuation was tried and is documented here:

- **A real bug was found and fixed** in the LMTD guards: the first version used
  `(DTA - DTB)/ln(Max(DTA/DTB, 1.0000001))`, which destroys every case with
  `DTA < DTB` — a perfectly valid LMTD situation (numerator and logarithm are
  both negative) — and returned garbage of either sign. The plain form holds
  for both orders; only `DTA = DTB` needs the limit. With the corrected guard
  and a hand-computed consistent state point as `.initials` (144 values,
  generated by an independent Python pass of the cycle equations), the initial
  residual of the coupled block fell from 4.7e8 to 5.8e5 (about 800x), and the
  system now fails only by line-search rejection in the first Newton step.
- The constant-UA simplification suggested for this round was shown
  infeasible at the fixed cycle point (duty pinned at ≈ 99 kW against ≈ 300 kW
  of transfer capability at the achievable LMTDs — no UA-LMTD root); this
  motivated implementing the source's utilisation formulation instead (section
  above).
- The state-point `.initials` are kept next to the native file (they remove
  the garbage-evaluation failure mode and are the natural restart point).

## Conversion log (deviations, all to be re-examined when the model converges)

1. Unit system converted by hand to SI-°C-Pa-J: source temperatures (K) → °C,
   `T_amb = 20 °C` (293 K); geometry, flows and pressures unchanged.
2. **Discretisation**: the source's adaptive cell scheme (n_disc = 0 / 10,
   heat-rate-weighted cells, cell-wise saturation tracking) is replaced by a
   3-zone (SH/2P/SC) moving-boundary formulation with zone areas proportional
   to the zone heat rates (the source's own cell weighting). The two-phase
   correlations, evaluated by the source as averages over 100 qualities at the
   zone pressure, are evaluated once at the mean quality (0.55 boiling, 0.495
   condensing, the means of the source's averaging ranges).
3. **Pressure-drop feedback removed** (modified): zone thermal states are
   evaluated at the inlet pressure (`P_2` evaporator, `P_cd_in` condenser) and
   the refrigerant drops `DP_ev_C`, `DP_cd_H` are post-processed with the
   source's zone-area-share weighting; the source feeds the drops back into the
   zone pressures. This decoupling was needed for convergence and is the
   biggest physical deviation; removing it re-couples the loops (see
   verification).
4. The friction drop of the two-phase correlations is kept **as coded**,
   including the factor `1.95*KEV*1000` with its `# kPa` comment — as written
   in `amalfi_plate_HTC` and `shah_condensation_plate_HTC` (likely an author
   unit slip: Longo's correlation is `1.95*KEV` in Pa). Kept for faithfulness.
5. Water-side pressure drops are neglected: the source sets `H_DP_ON/C_DP_ON`
   but its pipe-DP path has no plate correlation at this commit (cause 3
   above). The water side still enters the heat transfer (`WaterHTC`).
6. Expander: the state `su2` after the suction heat transfer is **overridden
   back to the suction state** (`rho_su2 = rho_su`, `s_su2 = s_su`,
   `h_su2 = h_su`) exactly as in the source code, where the active lines cancel
   the computed `su2` state; `Q_dot_su` only enters the wall balance. The
   `max`/`min` clamps of the source (throat pressure, mixing enthalpy bounds,
   LMTD guards) are kept.
7. The two-phase correlations use `Viscosity`/`Cp`/`Density` at
   `T_sat ± 0.001 °C` for the liquid/vapour viscosities, as in the source's
   CoolProp fallbacks; `surfacetension` at saturation, as `PropsSI` there.
8. Property input pairs: all calls are (P,H), (P,T), (P,Q), (P,S), (D,S), (D,P)
   — no (T,H) rewrite (decision D11 not triggered); no MODULE/SUBPROGRAM (D10
   not triggered).
9. The pump `NPSH_r` output is kept as information only (the source prints it;
   no equation uses it). The pump suction-quality reset of the source
   (`1 >= x > 0` → `x = 0`) is not needed here (suction always subcooled by
   construction) and is not translated.
10. EES/CoolSolve notes: `pi()` used instead of `pi` (as in CSL-0111,
    `CS-BUG-PI-FUNCTION`); the chained form `x = f(t)^2 = y` (valid EES chained
    equality) is not accepted by CoolSolve and was split into two equations
    (unverified suggestion, not registered); the `Water` fluid argument of
    `CALL WaterHTC` must be quoted (`'Water'`); the LMTD guards use the inline
    `IF(A,B,X,Y,Z)` function because CoolSolve rejects If/Then/Else blocks in
    the main program (unverified suggestion, not registered — EES allows them
    there to this translator's belief, no manual evidence at hand).

## Level justification (taxonomy §3)

Equations ≈ 226 (1 pt: 50–300), largest block > 30 (2 pts), functions +
procedures + arrays present (1 pt), ≥ 3 coupled components (1 pt), off-design +
semi-empirical calibration (1 pt), curated guesses needed (1 pt) = **7 → level
4**.

## Related models

`CSL-0134` (design-point preheated/recuperated ORC), `CSL-0153` (design-point
ORC with economics), `CSL-0138` (moving-boundary HX component, Bell 2015),
`CSL-0111` (chevron plate correlations, Martin), `CSL-0113`/`CSL-0114`
(3-zone plate condenser/evaporator), `CSL-0159` (ORC void-fraction charge),
`CSL-0132` (R1233zd(E) conductivity correlation used here), `CSL-0013`
(TESPy heat-pump cycle translation).

## Figure

*(no figure: the model does not solve yet; the state-point arrays `P[i]`,
`T[i]`, `h[i]`, `s[i]` of §8 are in place for the maintainer's diagram once it
does.)*
