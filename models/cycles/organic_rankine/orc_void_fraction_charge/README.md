# Low-temperature ORC (R134a) with void-fraction charge of the heat exchangers

🔴 **Level 4 · Research** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0159`

Low-temperature organic Rankine cycle (R134a) from the ULiège laboratory work
(~2007): pump, evaporator and condenser are each split into liquid / two-phase
/ vapour zones whose share of the heat-exchanger area is weighted by the
refrigerant mass they contain, and the **refrigerant charge `M_charge` is an
output** of a global void-fraction balance, solved so that the condenser
outlet is subcooled by the imposed `DELTAt_sc_ex_cd` = 3 K. The expander is
modelled in detail (supply-throat pressure drop, leakage, isochoric expansion
to the built-in volume ratio, supply/exhaust cooling, ambient losses).

| | |
|---|---|
| **Category** | Cycles and machines › Organic Rankine cycles |
| **Fluids** | R134a (working fluid), AirH2O (condenser air) |
| **Size** | 312 equations (largest block: 112); the runnable variant adds 1 |
| **Source** | ULiège — laboratory ORC model, file `ORC simple model with void fraction.EES` (EES 8.139) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory; comments signed "ARA") |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file blocked by `CS-BUG-HUMIDAIR-PROPS`; the `_coolsolve` variant is verified against the EES stored solution |

## Problem statement

As in the original file: *"Program run to adjust the data so that the results
are reasonable: find the charge that gives 3 K of subcooling after the
condenser and the secondary-fluid (glycol water) flow that gives a 63 °C
evaporator outlet"*. The imposed inputs are the evaporator duty
`Q_dot_ev` = 12 990 W and the superheating at the evaporator outlet
`DELTAt_oh_ex_ev` = 10 K; the pump speed `rpm_pump` (≈ 1596 min⁻¹) and the
refrigerant charge `M_charge` (≈ 0.393 kg) are outputs.

## Model

- **Pump** (§1): volumetric pump, `M_dot*v_su = epsilon_vol_pump*N_pump*V_s_pump`;
  isentropic work approximated by `w_s = v_su*Δp` (as in the original,
  `epsilon_s_pump` = 0.6).
- **Evaporator** (§2, plate HX, 22 plates): three zones (liquid / two-phase /
  vapour), each with an epsilon-NTU balance and `U_liquid_ev` = 1000,
  `U_twophase_ev` = 3600, `U_vapor_ev` = 1000 W/m²-K. The zone shares
  `alpha_*_ev = Volume_*/Volume_ev` come from the mass contained in each zone,
  the volumes from mean specific volumes at the zone states.
- **Expander** (§3): supply pressure drop through a throat of diameter
  `d_thr_su` = 5.5 mm, supply cooling against the casing, leakage flow through
  `A_leak` = 2·10⁻⁶ m², isentropic expansion to the adapted (built-in volume
  ratio) pressure, isochoric expansion to the exhaust pressure, exhaust
  cooling, ambient losses through `AU_amb_exp` = 11 W/K, mechanical loss
  `T_loss_exp*omega`. Overall isentropic effectiveness computed as post-processing.
- **Condenser** (§4, finned-tube air coil, 40 tubes): three zones as the
  evaporator; the air side uses humid-air properties (`AirH2O`, r = 0.5) with
  the air flow from the frontal area and the air speed `C_rad_air` = 3.35 m/s.
- **Global charge balance** (§5): `M_ev + M_line + M_cd = M_charge`, with
  `Volume_line` = 10⁻⁴ m³ of liquid line.
- The `T[i]`/`H_dot[i]` arrays (i = 1–16) give the T-Ḣ diagrams of both heat
  exchangers, as in the original. Indices 21–24 give the four cycle points
  (post-processing) for the CoolSolve diagrams.

| Inputs | Value | Outputs (variant) | Value |
|---|---:|---|---:|
| `Q_dot_ev` imposed duty | 12 990 W | **`M_charge` refrigerant charge** | 0.3934 kg |
| `DELTAt_oh_ex_ev` superheating | 10 K | `rpm_pump` pump speed | 1595 min⁻¹ |
| `DELTAt_sc_ex_cd` subcooling | 3 K | `W_dot_Rankine` net power | 681 W |
| `t_sf_su_ev` glycol inlet | 88.47 °C | `eta_Rankine` efficiency | 0.0524 |
| `t_sf_su_cd` air inlet | 20 °C | `M_ev` / `M_cd` / `M_line` | 0.209 / 0.067 / 0.118 kg |
| `V_s_cp` expander swept volume | 110·10⁻⁶ m³ | `p_su_exp` / `p_ex_exp` | 22.46 / 8.92 bar |

The cycle efficiency is low (5.2 %) because the heat source is a 88 °C
glycol-water loop; the evaporator runs at 72.8 °C, the condenser at 35.2 °C.

## How to run

The **native file is blocked**: CoolSolve silently returns 1E4 kg/m³ for
`Density(AirH2O,…)`, which makes the condenser air flow ~10 000 × too large
without any error (`CS-BUG-HUMIDAIR-PROPS`). The native file is kept in valid
EES syntax. The runnable variant is:

```bash
coolsolve ./orc_void_fraction_charge_coolsolve.eescode
```

Its only change is the registered workaround
`rho_sf_cd = (1+w_air_cd)/Volume(AirH2O,…)` (EES `density` = 1/`volume` for
AirH2O); see the conversion log. Convergence needs the reference-offset-corrected
guesses shipped in `orc_void_fraction_charge_coolsolve.initials` (see
*Verification*); the 112-equation loop does not converge from raw guesses.

## Results

Variant vs EES (see *Verification*): the charge is `M_charge` = 0.39339 kg
(EES 0.39342, −0.009 %), `eta_Rankine` = 0.05242 (EES 0.05230), `W_dot_Rankine`
= 680.9 W (EES 679.4 W), `rpm_pump` = 1595 (EES 1596), all temperatures within
0.25 %. Note that `w_exp_2` = −3050 J/kg is negative: the expander is
under-expanded (adapted pressure below exhaust pressure), as in the original.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s or P-h diagram of the cycle
     (state arrays P[21..24], h[21..24], T[21..24], s[21..24]),
     figures/orc_void_fraction_charge_ts.png -->

## Verification

Reference: the EES stored solution shipped in the source file (298 of 299
stored values valid; 5 stored values belong to equations that are commented
out in the file version). `compare_solution.py` on the **variant**:
293 common variables; excluding the absolute-enthalpy/entropy variables
(`h_*`, `s_*`, `H_dot[1..16]`, constant EES↔CoolProp reference-state offset,
see below) and the three diagnostic qualities, the maximum relative difference
is **1.21e-02** (`Q_dot_ex_exp`, −13.5 vs −13.3 W, small denominator), then
1.12e-02 on `w_exp_2` and 7.6e-03 on `rho_sf_cd`/`M_dot_sf_cd` (humid-air
density backend, see below); the charge and all pressures/temperatures agree
within **2.4e-03** (`M_charge`: 8.6e-05, i.e. −0.009 %).

- **Absolute h/s**: EES and CoolProp use different reference states for R134a
  (constant offsets Δh = −148.15 kJ/kg, Δs = −795.7 J/kg-K, determined on
  saturated-liquid/superheated calls). Enthalpy *differences* and the derived
  works/powers agree within ~2.4e-03 (e.g. `h_ex_ev − h_su_ev`: 197 193 vs
  197 303 J/kg, 5.6e-04; `w_in_exp`: 2.3e-03). The `.sol`
  therefore stores CoolProp-scale values and the comparison of the shifted
  variables is meaningful through their differences only.
- **`X_ex_ev` / `X_ex_exp` / `X_ex_cd`**: EES returns ±100 outside the dome,
  CoolSolve returns 0 — registered deviation `CS-GAP-QUALITY-DOME` (the three
  states are superheated, superheated, subcooled; the value feeds no equation).
- **`rho_sf_cd`**: 1.1994 vs 1.1903 kg/m³ (+0.76 %), the EES-vs-CoolProp
  humid-air difference; it propagates to `M_dot_sf_cd`/`C_dot_sf_cd`
  (+0.73 %) and dominates the zone-share deviations of the condenser.
- Only in the EES reference: `DELTAt_ln_ev_vapor`, `h_exs_pump`, `M_dot`,
  `s_su_pump`, `W_dot_exp` (commented-out equations of the original). Only in
  CoolSolve: `w_air_cd` (variant), `c_p_sf_cd` (defined in the file but absent
  from the EES stored table), `pi`, the string variables and the state-point arrays.
- The **native file** was not compared numerically: it solves to silently
  wrong values (`rho_sf_cd` = 1E4 kg/m³), which is exactly the registered bug.

A first solve from the raw stored values failed (`SingularJacobian` on the
112-equation loop): the reference offset makes every property-call equation
wrong by ~148 kJ/kg at the start point. The shipped `.initials` therefore
contain the stored EES values shifted by the reference offsets
(+148 160 J/kg on `h_*`, +795.62 J/kg-K on `s_*`); they are guesses, not
equations, and with them the variant converges in ~32 iterations.

## Source and attribution

ULiège Thermodynamics Laboratory ORC model (file comments mention 09/09/2007
and are partly signed "ARA"; the EES licence tag is the J. Lebrun laboratory
licence). No personal name could be identified from the file alone → author
TBD. Comments are in English with a few Spanish/French fragments (translated).

Source file (EES 8.139), collection of S. Quoilin:
`~/Nextcloud/thermo_models/modeles/ORC simple model with void fraction.EES`
(inventory candidate `TM-0314`, duplicate group DG-0124 with the identical
`Steady-state models/` copy TM-0600).

## Conversion log

- **2026-10-08 — import** (`tools/ees_extract.py`): unit system already
  `SI MASS DEG PA C J` (no conversion); EES licence tag removed; no lookup or
  parametric tables. Comments translated to English, standard header added,
  dead commented-out code removed (provisory parameters, an alternative
  supply-line model without pressure drop, an alternative evaporator input
  mode imposing `t_sf_ex_ev`/`M_dot_sf_ev`, an old ln-mean-ΔT line of the
  vapour zone, guess-update values) — the kept commented lines
  (`rpm_pump`, ideal pump work, `M_cd`, `M_charge` = 0.41 kg) document
  earlier versions of the model. The "ARA" signature and a Spanish comment
  about a 22/06/2007 error fix were dropped with their dead code.
- **2026-10-08 — decision D11** (1 rewrite, file stays valid EES): the
  (T, H) property call `X_ex_exp=Quality(fluid$,T=T_ex_exp,h=h_ex_exp)` is
  rewritten as `X_ex_exp=Quality(fluid$,P=P_ex_exp,h=h_ex_exp)` — same state,
  since `h_ex_exp=enthalpy(fluid$,P=P_ex_exp,T=t_ex_exp)` defines it at
  `P_ex_exp` (`CS-GAP-PROP-TH` applies but is not listed in
  `missing_features`: not planned, rewritten per the library workflow §6).
- **2026-10-08 — variant `orc_void_fraction_charge_coolsolve`** (the only
  change of the variant; valid EES syntax, no CoolSolve-only construct):
  `rho_sf_cd=Density(fluid3$,T=…,r=0.5,P=101325)` is replaced by
  `w_air_cd=humrat(…)` + `rho_sf_cd=(1+w_air_cd)/Volume(fluid3$,…)`, the
  registered workaround of `CS-BUG-HUMIDAIR-PROPS` (CoolSolve returns the
  1E4 fallback for `Density(AirH2O,…)`, silently). Verified against the same
  EES reference as the native file (see *Verification*).
- **2026-10-08 — diagram support**: block of 16 post-processing equations
  (state arrays `P[21..24]`, `h[21..24]`, `T[21..24]`, `s[21..24]`; indices
  1–16 are taken by the original T-Ḣ arrays) added at the end; checked to
  leave every model variable unchanged (max difference 0).
- **Level**: equations 296 → 1; largest block 112 (> 30) → 2; arrays present → 1;
  ≥ 3 coupled components → 1; semi-empirical calibration (AU scaling
  `(M_dot/M_dot_nom)^0.6`, calibrated leakage/throat) → 1; curated guesses
  (already in the original: its comments keep guess-update values) → 1.
  Score 7 → **level 4** (calibrated multi-component system, demanding numerics).

## Limitations and CoolSolve gaps

- `CS-BUG-HUMIDAIR-PROPS` (P1, silent): `Density(AirH2O,…)` returns 1E4 kg/m³,
  which blocks the native file (the condenser air flow would be ~10 000 × too
  large without any error or warning). The `_coolsolve` variant applies the
  registered workaround. Re-check the native file once the bug is fixed.
- `CS-GAP-QUALITY-DOME` (not blocking): the diagnostic qualities return 0
  instead of EES's ±100 outside the saturation dome.
- The three `epsilon_*_ev`/`epsilon_*_cd` effectiveness equations are solved
  implicitly although they are explicit in form (as in the original).
- The model is a data-adjustment run: `Q_dot_ev`, the U values and the
  expander calibration parameters are imposed; no off-design validation.

## Related models

- `CSL-0153` *orc_whr_refprop_cost*: same ULiège ORC family (WHR ORC with
  scroll expander and REFPROP mixtures); here a low-temperature R134a cycle
  with a charge balance instead of a cost model.
- `CSL-0036` *orc_extraction_r134a*: R134a ORC with extraction.
- `CSL-0037` *scroll_expander_semi_empirical*: semi-empirical scroll expander
  (the detailed expander here is a custom volumetric/leakage model).
- `CSL-0084` *orc_expander_pump_empirical_maps*: ORC with empirical expander
  and pump maps.
