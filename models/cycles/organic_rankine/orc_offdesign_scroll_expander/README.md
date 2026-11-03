# CSL-0312 · `orc_offdesign_scroll_expander`

Off-design organic Rankine cycle (R1233zd(E)) with a Lemort semi-empirical scroll
expander, a pump on similarity laws with rated curves and two SWEP P200THx140
brazed-plate heat exchangers in a moving-boundary formulation. Translation of
LaboThapPy `machine/examples/ORC/fpi_orc_example.py`, study case `off_design`.

> 🔴 **Level 4 · Research** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** (adapted from the original; review of 2026-11-01) &nbsp;|&nbsp; `CSL-0312`

| | |
|---|---|
| Category | `cycles/organic_rankine` |
| Kind | steady (one operating point, imposed `m_dot`) |
| Status | **verified (adapted)** — after correcting errors of the source correlations and of the translation (see *Adaptation of 2026-11-01*), the cycle converges (57 Newton iterations from the shipped `.initials`); energy balances closed, second law respected |
| Fluids | R1233zd(E), Water |
| Origin | software library (LaboThapPy, ULiège) |

## Problem statement

Simulate the **off-design** operating point of an organic Rankine cycle on
R1233zd(E): a Lemort semi-empirical scroll expander, a pump on similarity laws
with rated curves and two SWEP P200THx140 brazed-plate heat exchangers in a
moving-boundary formulation, at an imposed refrigerant flow (translation of
LaboThapPy `machine/examples/ORC/fpi_orc_example.py`, study case
`off_design`). The expander speed, pump speed, pressures and heat-transfer
coefficients all float (see *Niche*).

## Model (structure of the translation)

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


## How to run

```bash
coolsolve ./orc_offdesign_scroll_expander.eescode
```

The cycle converges with the default Newton from the shipped
`.initials` (57 iterations; from the earlier initials it needs Try Harder,
1023 iterations; it was first obtained by a decomposition — pump outlet fixed,
duty imposed, then released). No `coolsolve.conf` is needed for the adapted
model.

## Results

Default operating point (shipped `.sol`): R1233zd(E) 0.45 kg/s between 4.03 bar (60 °C, fixed as in
the source) and 1.089 bar (condensing at 20.1 °C, 7 K subcooling): `Q_ev` = 106.4 kW, `Q_cd` = 99.6 kW, expander
6.85 kW (η_is 0.615, ε_v 1.04, 9210 rpm), pump 0.495 kW (1760 rpm, η 0.20), net 6.36 kW, `eta_th` = 5.97 %
(Carnot between the 70 °C and 10 °C water inlets: 17.5 %). Area fractions: evaporator 0.30 (liquid) / 0.18
(boiling) / 0.53 (superheat, the vapour leaves at 69.92 °C, 0.08 K below the water inlet: the 17.8 m² exchanger is
oversized for this flow); condenser 0.34 / 0.42 / 0.25. HTCs: refrigerant liquid 287, boiling 6650, vapour
220 W/(m²·K); condensation 1730; water about 10⁴. **Checks**: cycle energy balance closed to 1·10⁻⁹ W, expander to
2·10⁻⁸ W, expander wall balance to 3·10⁻¹⁰ W; no temperature-difference clamp active; water-side balances; second
law. The pump and expander translations were verified against the source components in the first import (the
expander change of item 9 moves its results by the 12 W of suction heat at this point).


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

- **Full cycle: solved since the adaptation of 2026-11-01** (see that section); the text below is the record of the first import: The system is square (226/226)
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

## Adaptation of 2026-11-01 (failing → verified)

The model was re-checked equation by equation against the LaboThapPy source and against physics. The
non-convergence came from **errors**, not from the solver: once they are corrected the cycle converges and is
thermodynamically consistent. Every change is marked `ADAPTED` in the file.

Errors of the **source** (LaboThapPy `f03f7f47`), corrected:

1. **Amalfi boiling correlation, mass flux**: `G = m_dot/(2*amplitude*width)` is the whole refrigerant flow
   through one channel cross-section; the per-channel flux `m_dot/(N_ch*b*W)` is used (500 times lower here).
2. **Amalfi, conductivity**: the linear fit `0.09513*T − 17.963` mW/(m·K) gives the **vapour** conductivity of
   R1233zd(E) (13.7 mW/(m·K) at 60 °C), whereas Amalfi's Nusselt number uses the liquid one; CoolProp's
   saturated-liquid conductivity is used.
3. **Amalfi, boiling number**: the source divides the heat needed to evaporate the remaining liquid by the total
   plate area; the heat flux of the boiling zone is used (`qflux_2p_ev = k_2p_ev*LMTD_2p_ev`, identical to
   `Q_2p_ev/(w_2p_ev*A_ev)`).
4. **Surface tension**: CoolProp has **no surface-tension model for R1233zd(E)** ("surface tension curve not
   provided", also in CoolProp 8.0.0): the source's Amalfi call cannot even be evaluated. The correlation of
   Kondou et al., *Int. J. Refrig.* 53 (2015) 80–89, `sigma = 61.95*(1 − T/438.75 K)^1.277` mN/m (274–350 K,
   ±0.05 mN/m), is used (FUNCTION `SigmaR1233zdE`).
5. **Friction pressure drop**: `DeltaP_f = 1.95*KEV*1000` with KEV already in Pa; Longo's correlation is
   ΔP_f [kPa] = 1.95·KEV [kJ/m³], i.e. the same number in Pa: the factor 1000 is removed (Amalfi and Shah).
6. **Gravity term in the condenser**: added as a loss; in down-flow condensation it is a pressure gain.
7. **Evaporator plate "amplitude"**: 0.15 mm, marked "to adjust!!" in the source geometry and contradicting its own
   channel thickness (2.16 mm); the channel gap is taken from the channel cross-section (`b = CS/W`, 2.15 mm
   evaporator, 2.39 mm condenser).
8. **R1233zd(E) conductivity function** (`conductivity_R1233zd_LTP`, copied from `CSL-0132`): it uses the critical
   constants of **R1234ze(E)** (382.52 K, 489.24 kg/m³); +9 % (liquid) to +20 % (vapour) against CoolProp's
   R1233zd(E) model, which is now used in the Martin correlation (`CSL-0132` documents this and also ships the
   function with the published constants of Perkins & Huber).
9. **Expander state su2**: the source computes the suction pressure drop and heat transfer, then resets the state
   to the suction state before the expansion (lines commented out), so `Q_dot_su` entered the wall balance without
   leaving the gas (energy not conserved whenever it is non-zero). Lemort's model is restored (expansion from su2,
   signed heat transfers without `max(0, …)` clamps). At this operating point the calibrated 6.48 mm suction port
   would see a **supersonic** velocity (690 m/s, kept as output `C_su_x`), where the drop formula has no meaning:
   the suction pressure drop is neglected, the source's default (`d_su1 = 0`).
10. `gamma_x` guard `Max(0.01, …)` → `Max(1.01, …)` (γ/(γ−1) is infinite at γ = 1; inactive at the solution).

Errors of the **translation**, corrected:

11. **Trigonometric units**: CoolSolve (like EES with its DEG setting) takes trigonometric arguments in degrees;
    the Martin procedure passed `(90 − beta)·π/180` in radians, i.e. cos(1.05°) instead of cos(60°): single-phase
    HTCs were 8 times too low (38 instead of 290 W/(m²·K)).
12. **Evaporator water nodes**: `h_w_n2_ev = h_wi_ev + Q_sh_ev/m_w_ev` — the hot water must **lose** the zone heat
    (minus); as written the water reached 76 °C inside the exchanger with a 70 °C inlet.
13. The LMTD guard bug found in the first review (5th argument of the inline `IF`).

**Solver notes / CoolSolve hints**: with the corrected model the cycle converges with the default Newton from the
shipped `.initials` (57 iterations); from the earlier initials it needs Try Harder (1023 iterations), and it was
first obtained by a decomposition (pump outlet fixed, duty imposed, then released). Hint: a CoolSolve diagnostic
listing the equations with the largest residual at the stall point (the best iterate, not the start) would have
pointed at the zone balances immediately.

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

## Limitations and CoolSolve gaps

-  the expander runs at 9210 rpm and 4.5 times its nominal flow
(`m_dot_n_x` = 0.1 kg/s), with a supersonic calibrated suction port: the semi-empirical parameters are used far
outside their calibration. The high pressure is fixed (the source's single iteration variable is the low
pressure), so this is a "given flow, given high pressure" simulation, not a fully free off-design point.


- Deviations of the translation (see *Conversion log*, to be re-examined on a
  re-check): the refrigerant pressure-drop feedback is removed (zone states at
  the inlet pressure, drops post-processed — the biggest physical deviation);
  the adaptive cell scheme is replaced by a 3-zone (SH/2P/SC) formulation; the
  two-phase correlations are evaluated once at the mean quality instead of
  averaged over 100 qualities.
- The R1233zd(E) conductivity function of `CSL-0132` is copied into the file
  per workflow §4 (`$INCLUDE` not available yet, `CS-GAP-INCLUDE`); the
  friction-drop factor `1.95*KEV*1000` of the two-phase correlations is kept
  as coded (likely an author unit slip, kept for faithfulness).
- Unverified suggestions, not registered (see *Conversion log*): the chained
  equality `x = f(t)^2 = y` is not accepted by CoolSolve; If/Then/Else blocks
  are rejected in the main program (the inline `IF(A,B,X,Y,Z)` is used).

## Related models

`CSL-0134` (design-point preheated/recuperated ORC), `CSL-0153` (design-point
ORC with economics), `CSL-0138` (moving-boundary HX component, Bell 2015),
`CSL-0111` (chevron plate correlations, Martin), `CSL-0113`/`CSL-0114`
(3-zone plate condenser/evaporator), `CSL-0159` (ORC void-fraction charge),
`CSL-0132` (R1233zd(E) conductivity correlation used here), `CSL-0013`
(TESPy heat-pump cycle translation).

## Figure

*(no figure yet; the model solves since 2026-11-01; the state-point arrays `P[i]`,
`T[i]`, `h[i]`, `s[i]` of §8 are in place for the maintainer's diagram once it
does.)*
