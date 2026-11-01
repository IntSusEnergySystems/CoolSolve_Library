# Solar-driven R245fa ORC with a discretised parabolic-trough collector and plate heat exchangers

🔴 **Level 4 · Research** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0329`

A small parabolic-trough field (46 m of collector, glycol heat-transfer fluid) heats the
evaporator of an organic Rankine cycle on R245fa. The collector is divided into
20 segments along its length; in each segment the 1D radial heat balance of the receiver
(Forristall model: HTF, absorber tube, annulus, glass envelope, ambient and sky) is solved
together with the HTF enthalpy march, so the field outlet temperature and the collector
efficiency are results, not inputs. The cycle has a three-zone plate evaporator and a plate
recuperator whose number of plates is solved from an imposed pressure drop (Thonon
single-phase and Hsieh boiling correlations), a condenser fixed by a pinch to the ambient, a
pump, a fan power polynomial and a **two-stage hermetic scroll expander** whose intermediate
pressure ratio is the one that maximises the overall isentropic effectiveness
(`xi = 0`). The file is the CoolSolve example `orc_solar_complex.eescode` (equation-identical to the
EES original), rewritten to follow the library decisions D10 (`MODULE doubleexpander` flattened)
and D13 (`$COMMON` replaced by arguments).

**Status.** The native file (valid EES) is **blocked**: one array element indexed by a
variable (`cp_1ave[mean]`, `mean = ceil(imax#/2)`) is not resolved by CoolSolve
(`CS-GAP-INDEX-VAR`) and the system has 979 equations for 980 unknowns. The runnable
variant `orc_solar_complex_coolsolve.eescode` differs only by `cp_1ave[10]` in that
line (valid EES too); it solves and was compared with the EES stored solution.

| | |
|---|---|
| **Category** | Renewables › Solar thermal |
| **Fluids** | R245fa (cycle), Water (condenser coolant), Air (receiver annulus and wind convection), glycol (HTF: polynomial fits of the file, not a CoolProp fluid) |
| **Size** | variant: 979 equations, 979 unknowns, 335 blocks, largest block 644; native: 979 equations, 980 unknowns |
| **Source** | CoolSolve example `examples/orc_solar_complex.eescode` (original EES file `EES_ok/orc_solar_complex.EES`, EES 9.920, in CoolSolve `misc/EES_ok.zip`) |
| **Authors** | S. Quoilin (ULiège Thermodynamics Laboratory), probable, to be confirmed by the maintainer; collector part after R. Forristall (NREL), modifications marked `AVM` in the file (person not identified) |
| **License** | MIT |
| **CoolSolve** | native **blocked** by `CS-GAP-INDEX-VAR`; variant `_coolsolve` verified (0.4.0@9768373) |

## Niche

Nearest library models: `CSL-0040` *orc_biomass_chp* (same research family, MODULE
flattening, biomass instead of solar heat, blocked), `CSL-0129` *parabolic_trough_collector_discretised*
(discretised collector with a datasheet efficiency map, water, no cycle), `CSL-0082`
*parabolic_trough_receiver_forristal* (one receiver element of the same Forristall model, from
the ThermoCycle Modelica library, no field, no cycle) and `CSL-0147` *segs_solar_power_plant*
(steam Rankine plant behind a solar field at design point, solar field as a source of heat).
What this model adds: the only library model in which the **field outlet temperature comes from a
segment-by-segment radial heat balance and drives the cycle** (the evaporator pinch, the plate
count and the expander operating point all feed back on the HTF return temperature), an ORC
whose heat exchangers are **sized from pressure drops**, and a **two-stage scroll expander with
optimal intermediate pressure** inside a complete system. It is the full-system case of the
Forristall and expander sub-models that the library holds separately (`CSL-0082`, `CSL-0117`).

## Model

**Collector** (`EQUATIONS - SOLAR THERMAL COLLECTORS` of the file). Parameters of a user-defined
receiver (`D_2 … D_5`, `L = 46 m`, aperture width 2.5 m, `L_HCE = 1 m`, `Number_HCE = 10`),
`I_beam = 800 W/m²`, `T_amb = 15 °C`, wind 2 m/s, `m_dot_HTF = 1.27 kg/s`; `imax# = 20` segments.
Per segment `i`: HTF in/out temperature and velocity (`T_1in/out`, `v_1in/out`), pressure drop
(friction factor of the file), convection HTF–absorber (`q_12conv`), conduction through the
absorber (`k_23`), annulus convection and radiation (`q_34conv`, `q_34rad`), glass conduction,
convection to ambient and radiation to the sky (`q_56conv`, `q_57rad`), bracket loss
(`q_cond_bracket`); the segment balance closes with `q_45cond`, `q_56conv`, `q_12conv` and
`q_3SolAbs` (1D radial model). `OptEff_env`, `OptEff_abs` come from `OpticalEfficiency`, the
selective-coating emissivities `EPSILON_3[i](T_3[i])` from `SelectiveCoatingProperties`.
Results: `T_htf_ex_col`, `DELTAP_htf_col`, `Q_dot_col = Σ q_12conv·ΔL`, `ETA_Col = Q_dot_col/Q_dot_sol`.
The HTF return temperature `T_htf_su_col` is an unknown of the loop.

**ORC.** `fluid$ = R245fa`, `T_ev = 135 °C`, superheat `DELTAT_ex_ev = 5 K`, condenser pinch
`pinch_cd = 8 K` above the ambient (`T_cd = T_amb + pinch_cd = 23 °C`), subcooling 5 K, coolant
water with `DELTAT_cf_cd = 15 K`, `epsilon_pp = 0.7`, `epsilon_rec = 0.8`, `N_rot_exp = 3000 rpm`.
Evaporator: three zones against the HTF (`M_dot_hf = M_dot_htf`, `cp_hf` mean of the first and
last segment) with the pinch `pinch_ev = 8 K`; `hx_ev` (liquid and vapour Thonon, two-phase
Hsieh, glycol side Thonon) returns `A_ev` and the pressure drops, the number of plates `N_p`
is solved from `DELTAp_ev = 100e2 Pa`. Recuperator: `epsilon_rec`, log-mean area, plates `N_p_rec`
solved from `DELTAP_vap_rec = 100e2 Pa`. The condenser is a three-zone energy balance on the
coolant with `W_dot_fan_cd` from a polynomial of the Witt condenser data sheet (the plate
condenser area block of the file is commented out in the original). Pump: `epsilon_pp`.
**Expander** (`twostage$ = 'yes'`): `MODULE doubleexpander` (flattened below): filling factor and
isentropic effectiveness of each stage from the hermetic-scroll correlations of Lemort, Quoilin
and Pire (`hermeticexpander`), swept volumes `V_s_exp_1/2` from the mass flow, intermediate
pressure ratio `r_p_1_dbl` from `xi_dbl = 0` (derivatives `der_rp`, `der_rho`). The single-stage
`hermeticexpander` and the open-drive `opendriveexpander` procedures stay in the file and are
not used in the two-stage run.

| Inputs (defaults) | Value |
|---|---|
| `I_beam`, `T_amb`, `p_amb`, wind | 800 W/m², 15 °C, 0.83 bar, 2 m/s |
| `m_dot_HTF` | 1.27 kg/s |
| `T_ev`, `pinch_ev`, `pinch_cd` | 135 °C, 8 K, 8 K |
| `N_rot_exp` | 3000 rpm |

Outputs: `M_dot`, `W_dot_net`, `eta_cycle`, `eta_overall = eta_cycle·eta_col`, `Q_dot_col`,
`ETA_Col`, `T_htf_su_col`, `T_htf_ex_col`, `N_p`, `N_p_rec`, `A_ev`, `A_rec`, `r_p_1_dbl`, the state arrays
`s[i]`, `t[i]`, `p[i]`, `h[i]` (1–11) of the T-s diagram and the heat-exchanger temperature
profiles `T_hf[]`, `T_cf[]`.

## How to run

```bash
coolsolve orc_solar_complex_coolsolve.eescode      # runnable variant (reads orc_solar_complex_coolsolve.initials)
coolsolve orc_solar_complex.eescode                # native file: "979 equations and 980 unknowns"
```

Good guesses are needed: the 644-variable block does not converge from default guesses
(`LineSearchFailed`/`SingularJacobian`). `orc_solar_complex_coolsolve.initials` (a copy of
`orc_solar_complex.initials`) holds the converged CoolSolve solution; the variant also converges
from the EES stored values of the original file (tested in the work folder: the stored
`ees_variables.csv` as `.initials`, with the module variables renamed `_dbl` and
`beta_dbl = 1 - h_ex_exp_s/h_su_exp`). The run prints `CALL WARNING` messages of the original
(`fq_34conv` range of `Ra_D4`) and one warning per `lookup('ev', …) = …` line of `hx_ev` (a write to a
table that CoolSolve does not store; no effect on the results). The variant is tested as
`CSL-0329:coolsolve`.

## Results

Variant, default inputs (CoolSolve 0.4.0@9768373, CoolProp 8.1.0dev):

| Quantity | EES stored | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `M_dot` [kg/s] | 0.220372 | 0.219765 | 2.75e-03 |
| `W_dot_net` [W] | 5423.29 | 5400.19 | 4.26e-03 |
| `eta_cycle` [-] | 0.105892 | 0.105729 | 1.54e-03 |
| `eta_overall` [-] | 0.0589481 | 0.0586970 | 4.26e-03 |
| `Q_dot_col` [W] | 51214.9 | 51075.4 | 2.72e-03 |
| `ETA_Col` [-] | 0.556683 | 0.555167 | 2.72e-03 |
| `T_htf_su_col` [°C] | 135.332 | 135.305 | 2.0e-04 |
| `T_htf_ex_col` [°C] | 148.714 | 148.652 | 4.2e-04 |
| `W_dot_exp` [W] | 6908.04 | 6884.74 | 3.37e-03 |
| `N_p` (evaporator plates) | 11.0753 | 10.3663 | 6.40e-02 |
| `N_p_rec` | 23.2810 | 23.2129 | 2.92e-03 |

Besides: `r_p_1_dbl` = 3.0095, `r_p_2_dbl` = 5.7824 (product 17.402 = `p_su_exp/p_ex_exp`), `p_int_exp_dbl` = 8.553e5 Pa,
`epsilon_s_exp` = 0.5815 (stages 0.6144 and 0.5470), `T_ex_exp` = 71.6 °C (superheated
exhaust, the cycle runs with its recuperator), net power 5.40 kW for 92 kW of solar power
on the aperture (`eta_overall` 5.9 %).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the R245fa cycle from the arrays s[i], t[i]
     (Array overlay, Close loop), saved in figures/, e.g.  ![T-s diagram of the cycle](figures/orc_solar_complex_ts.png) -->

## Verification

The variant was compared with the **solution stored in the original EES file**
(`EES_ok/orc_solar_complex.EES`, extracted with `ees_extract.py`: 1064 variables decoded) with
`compare_solution.py orc_solar_complex_coolsolve.sol ees_variables.csv`:
**927 common variables, 302 differ (rtol=0.001); only in EES: 137; only in CoolSolve: 53**.
The largest difference is `x` (100 in EES, 0 in CoolSolve: the quality of a superheated state,
registered `CS-GAP-QUALITY-DOME`, a diagnostic output that feeds no equation). Among the others
the maximum printed is 1.25e-01 (`DELTAp_hf_ev`, the glycol-side evaporator pressure drop), then
8.05e-02 (`A_ev`), 8.01e-02 (`L_rec`), 7.04e-02 (`L_w_tot`), 6.40e-02 (`N_p`), 5.59e-02 and
5.41e-02 (`h_vap_rec`, `h_liq_rec`, the plate heat-transfer coefficients), 5.03e-02 (`k[5]`);
the median of the 301 deviations other than `x` is 2.8e-03 and 98 of them exceed 1e-2. The deviations are
the plate-heat-exchanger sizes and heat-transfer coefficients, which depend on R245fa transport
properties (`k[5]`, the vapour conductivity at the expander inlet, differs by 5.03e-02 and `k[6]` by 4.19e-02;
the saturation pressure at `T_ev` = 135 °C differs by 6.2e-03, `p_ev`), and the quantities that
follow from them through the loop; the first-law results differ by less than 1e-2 (above).
The attribution to the CoolProp R245fa properties is not isolated by a separate run.
The collector sub-model agrees closely (`DELTAP_htf_col` 3.1e-05, `T_htf_su_col` 2.0e-04 relative).

Not compared (not in the CoolSolve solution, so listed as "only in EES"): the module variables of
`doubleexpander` under their module-local names (their stored values are stale, e.g. the
stored `r_p_1 = r_p_2 = 3.807` have a product of 14.49 against `p_su_exp/p_ex_exp` = 17.38 of the
stored run: `CS-BUG-EXTRACT-STALE`), and EES-only variables such as `HeatLoss[i]`, `glazing`.
The renamed `_dbl` variables have no entry in the reference; the module outputs `epsilon_s_exp`,
`epsilon_s_exp_1/2`, `W_dot_exp_1/2`, `FF_exp` are compared under their actual names
(1.04e-03, 5.85e-04, 1.76e-03, 7.34e-03, 8.52e-04, 7.33e-04).

**Energy balances** of the CoolSolve solution (variant), recomputed from the `.sol`:
`Q_dot_ev + W_dot_pp` = 51641.7 W = `W_dot_exp + Q_dot_cd` (difference 5e-10 W);
`M_dot_hf·cp_hf·(T_hf_su_ev − T_hf_ex_ev)` = 51075.918 W = `Q_dot_ev`; `Q_dot_col` = 51075.354 W
(sum over the 20 segments; 0.56 W, 1.1e-05 relative, consistent with the mean `cp_hf` of the first and last segment used in the evaporator balance); recuperator
`M_dot·Δh` is 8845.617 W on both sides; `W_dot_net = W_dot_exp − W_dot_pp − W_dot_fan_cd` = 5400.19 W.
`Q_dot_col_bis` (the `cp_1ave[mean]` line) is 51054.0 W.

The native file was not verified: it does not solve (structural analysis). The check concerns the variant.

## Source and attribution

CoolSolve example `examples/orc_solar_complex.eescode` (CoolSolve repository, MIT), curated
here; the EES original `orc_solar_complex.EES` (EES 9.920, licence stamp of the ULiège
Thermodynamics Laboratory) is in CoolSolve `misc/EES_ok.zip`; an equation diff (comments, blank
lines, `$bookmark` and `$UnitSystem` removed, case and spaces ignored: 1042 lines each) shows **no
difference** between the example and the original. The thermo_models collection has no row for this file.

- Cycle, heat exchangers, expander and coupling: S. Quoilin (ULiège Thermodynamics Laboratory),
  probable author, to be confirmed by the maintainer. Expander correlations: V. Lemort, S. Quoilin and
  C. Pire, *Experimental Investigation on a Hermetic Scroll Expander*, 7th International
  Conference on Compressors, Papiernicka, 2009 (correlation procedures signed by S. Quoilin, 30 September 2010);
  open-drive expander: V. Lemort, S. Quoilin, C. Cuevas, J. Lebrun, *Testing and modeling a scroll
  expander integrated into an Organic Rankine Cycle*, Applied Thermal Engineering 29 (14-15), 2009, 3094-3102.
  Boiling in plate exchangers (`Hsieh`): Y.-Y. Hsieh and T.-F. Lin, *Saturated flow boiling heat transfer and pressure drop of
  refrigerant R410a in a vertical plate heat exchanger*, Int J Heat Mass Trans 2002;45, pages as printed in the file ("033-1044");
  single-phase plate correlation `Thonon` (as in the file, "tested for various chevron angles").
- Collector: the scientific model and most functions are those of **R. Forristall, *Heat Transfer
  Analysis and Modeling of a Parabolic Trough Solar Receiver Implemented in Engineering Equation
  Solver*, NREL/TP-550-34169, October 2003**, adapted to a 1D, user-defined receiver by the
  author marked `AVM` in the comments of the file (identity not established; not guessed).
- Glycol property fits, the fan polynomial of the Witt condenser data sheet: as in the file.

## Conversion log

- **2026-10-31 — import (card C-450, CSX-033)**. Unit system of the original is `SI MASS DEG PA C J` (no
  conversion). Header replaced by the library header; runs of blank lines collapsed; the French
  comment `Perte de charge` translated; `$bookmark` lines and all equations unchanged.
- **`$COMMON` of 12 routines replaced by input arguments (decision D13)** (not supported by CoolSolve), added
  after the existing inputs and passed in every `CALL`/function call in the same order:

  | Routine | Arguments added |
  |---|---|
  | `q_56conv` | `D_5, L, P_6, v_6, GlazingIntact$` |
  | `q_57rad` | `EPSILON_5, D_5, L, GlazingIntact$` |
  | `q_37rad`, `q_34rad` | `D_3, D_4, L, EPSILON_4` (after the already passed `EPSILON_3[1..imax#]`) |
  | `fq_36conv`, `fq_34conv` | `D_3, D_4, L, P_a` |
  | `q_12conv` | `D_h, D_2, L, TestType$` |
  | `SelectiveCoatingProperties` | `TAU_envelope_UD, Alpha_abs_UD, EPSILON_3_100_UD, EPSILON_3_400_UD, SelectiveCoating$` |
  | `OpticalEfficiency` | `K, Reflectivity, TAU_envelope, GlazingIntact$, Shadowing_UD, TrackingError_UD, GeomEffects_UD` |
  | `q_cond_bracket` | `L_HCE, Number_HCE, L_aperture, T_6, P_6, v_6, DELTAL` |
  | `HCEdimensions` | `TestType$` (never called: its call is commented out in the file) |
  | `k_23` | none: its first formal `AbsorberMaterial$` is the `$COMMON` variable; only the `$COMMON` line is removed |

- **`MODULE doubleexpander` flattened (decision D10)**, tag `_dbl`, one call. Formal → actual
  arguments: `epsilon_overall` → `epsilon_s_exp`, `epsilon_1` → `epsilon_s_exp_1`, `epsilon_2` →
  `epsilon_s_exp_2`, `V_s_1` → `V_s_exp_1`, `V_s_2` → `V_s_exp_2`; `fluid$`, `p_su_exp`, `p_ex_exp`,
  `T_su_exp`, `N_rot_exp`, `M_dot`, `W_dot_exp_1`, `W_dot_exp_2`, `FF_exp` keep their names (the module
  writes `t_su_exp` for the formal `T_su_exp`, same variable in EES). The 36 module-internal
  variables get the suffix `_dbl`: `r_p`, `r_p_1`, `r_p_2`, `r_p_1_nom`, `rho_su_exp`, `rho_int_exp`,
  `s_su_exp`, `s_int_exp`, `h_su_exp`, `h_int_exp`, `h_int_exp_s`, `h_int_exp_s_bis`, `h_ex_exp`,
  `h_ex_exp_s`, `h_ex_exp_s_2`, `h_ex_exp_s_2_bis`, `p_int_exp`, `epsilon_s_exp_1`, `epsilon_s_exp_2`,
  `FF_exp_2`, `beta`, `beta_1`, `beta_2`, `beta_1_der`, `beta_2_der`, `gamma`, `epsilon_appr`,
  `epsilon_1_der`, `epsilon_2_der`, `der_lnrp_epsilon_1`, `der_lnrp_epsilon_2`, `der_lnrho_epsilon_2`,
  `der_rp_epsilon_1`, `der_rp_epsilon_2`, `der_rho_epsilon_2`, `xi`. Collisions with main-program
  variables that this avoids: `r_p`, `rho_su_exp`, `s_su_exp`, `h_su_exp`, `h_ex_exp`, `h_ex_exp_s`,
  `beta` (the chevron angle of the file, 45), `epsilon_s_exp_1/2` (the actual arguments). The
  `"<inputs outputs>"` marker of `M_dot` was dropped with the `MODULE`/`CALL` lines.
- **Missing input of the first rewrite attempts.** The flattened file had 979 equations for 980
  unknowns. It is not a Diagram-window input: the extra unknown is `cp_1ave[mean]` (`mean = 10`,
  an equation of the main program), which CoolSolve treats as a variable of its own, apart from
  `cp_1ave[10]`. The EES stored solution proves that EES resolves it (`Q_dot_col_bis` = 51193.36 W =
  `M_dot_htf·cp_1ave[10]·ΔT`; elements 9 and 11 give 51138.4 and 51248.2 W). Registered as `CS-GAP-INDEX-VAR`.
  The variant replaces this one index by `[10]`; nothing else differs between the two files.
- **Level**: equations 979 (2) + largest block 644 (2) + functions/arrays (1) + discretised, more than 3 coupled
  components (1) + semi-empirical correlations (1) + curated guesses needed (1) = 8 → level 4.

## Limitations and CoolSolve gaps

- `CS-GAP-INDEX-VAR` (blocks the native file; reproducer in the register, the variant avoids it).
- `CS-GAP-QUALITY-DOME` (not blocking): `x = quality(fluid$,h=h_ex_exp,p=p_cd)` returns 0 for the superheated exhaust, EES 100.
- Physical: the receiver is a user-defined, vacuum-free HCE (`vacuum = 0`, `D_p = 0`) with the glycol fits of the
  file (valid range not stated); the collector output depends on `L_HCE`, `Number_HCE` of the bracket loss; the plate
  condenser area block is commented out (condenser not sized); `calcarea$`, `twostage$` and the
  other switches are string constants of the file (`$IF` branches resolved at compile time).
- The model has no solar geometry: `I_beam`, `THETA = 0` (incident-angle modifier 1) are inputs.

## Related models

- `CSL-0040` *orc_biomass_chp*: same family (research ORC of the ULiège laboratory with MODULE blocks flattened, D10), heated by a biomass boiler.
- `CSL-0129` *parabolic_trough_collector_discretised*: discretised collector with a datasheet efficiency map (LaboThapPy), without cycle.
- `CSL-0082` *parabolic_trough_receiver_forristal*: one receiver element of the Forristall model (ThermoCycle translation).
- `CSL-0147` *segs_solar_power_plant*: solar-field + steam Rankine plant at design point (TESPy).
- `CSL-0117` *double_stage_scroll_expander*: the same two-stage expander module as a stand-alone model.
