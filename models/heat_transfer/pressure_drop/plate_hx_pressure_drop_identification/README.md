# Plate heat exchanger: two-phase pressure drops and heat-transfer coefficients, with a fictitious-orifice condenser pressure drop

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0124`

Plate-heat-exchanger correlations for the pressure drop and heat-transfer
coefficient of a chevron plate pack (chevron angle 25/30/45/60°): Thonon
(single-phase), Kuo et al. (condensation, quality-integrated two-phase
coefficient and frictional pressure drop), Hsieh & Lin (flow boiling), plus an
identified fictitious orifice reproducing the measured pressure drop of two
condensers in series. Properties of the mixture R245fa+R134a are CoolProp
property calls (the source used the EES REFPROP interface); the stored EES run
uses `MM_fraction = 1` (pure R245fa).

| | |
|---|---|
| **Category** | Heat transfer › Pressure drop |
| **Fluids** | R245fa+R134a (CoolProp mixture string `R245fa[x]&R134a[1-x]`; the stored run is pure R245fa, x = 1) |
| **Size** | 37 equations (largest block: 2) + 3 procedures |
| **Source** | ULiège — J. Lebrun laboratory, `optim/` folder (~2011), file `Identification pressure drops.EES` |
| **Authors** | TBD (ULiège, J. Lebrun laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — **verified** against the EES stored solution (see *Verification*) |

## Problem statement

Working file of a pressure-drop identification study (~2011, expander/ORC
context): the pressure drops of a plate condenser and evaporator are computed
with published plate-HX correlations, and the measured condenser pressure drop
is approximated by a fictitious orifice whose area `A_thr` was identified on
measurements with R245fa ("identified on the measurement with 245fa and the
two condensers in series", original comment). Geometry: L_h = 0.25 m between
port-hole centres, L_w = 0.112 m between gaskets, 37 plates of gap b = 2.4 mm
minus thickness, chevron angle β = 45°. Operating point: 0.1 kg/s at
p = 160 kPa, T = 88 °C (gas, condenser side), T_sat = 27 °C, q = 10 kW.

## Model

Three `PROCEDURE`s, each retrieving its properties with CoolProp calls on the
mixture string `WorkingFluidMix$`, which is an input argument of each of them (the
source's REFPROP calls, rewritten per decision D12; the saturated enthalpies of
`kuo` and `Hsieh_new` are in J/kg, so that the latent heat in the boiling number
Bo = q/(G·i_fg) is in J/kg):

- **Thonon**(fluid$, P, T, M_dot, b, L_w_tot, L_h, β, WorkingFluidMix$: h, Δp) — single-phase:
  D_h = 2b, Re = G·D_h/μ with G = ṁ/(b·L_w_tot); Nu = C₁·Re^m·Pr^(1/3) and
  f = C₂·Re^(−pp), the coefficients being tabulated per chevron angle with a
  Reynolds breakpoint; Δp = (f·2·G²/ρ·L_h)/D_h. (The `D_h = 2*b` line carries
  the original's own open question *"or 2*b/phi ?????"*.)
- **kuo**(fluid$, P, M_dot, q, N_p, b, L_w, L_h, coef, WorkingFluidMix$: Δp, α_tp_cd) —
  condensation: liquid-only Reynolds-based coefficient h_r_l = 0.2092·(k_l/D_h)·Re_l^0.5·Pr_l^(1/3)
  ("identified experimentally with water", original comment), enhanced by the
  Kuo et al. convective/boiling term with the confinement number Co and
  boiling number Bo, integrated in quality from x = 0.01 to 0.95 (REPEAT
  loop) and averaged; frictional drop with an two-phase friction factor
  f_tp = 21500·Re_eq^(−1.14)·Bo^(−0.085) at X_m = 0.5 ("average value of the
  vapor quality between inlet and outlet", original comment).
- **Hsieh_new**(fluid$, T_sat, M_dot, q, b, L_w_tot, L_h, WorkingFluidMix$: Δp, h_tp_ev) — flow
  boiling after Hsieh & Lin (2002, R410A in a vertical plate HX, reference
  quoted in the file): h_l = 0.2092·(k_l/D_h)·Re_l^0.78·Pr_l^(1/3),
  h_tp_ev = 88·Bo^0.5·h_l; f_tp = 61000·Re_eq^(−1.25). The latent heat is
  `i_fg = h_sat_v - h_sat_l` (saturated enthalpies at T_sat, J/kg); `h_l` is the
  liquid heat-transfer coefficient only.
- Fictitious orifice: V_thr = V_dot_su_cd/A_thr,
  Δp_cd_approx = V_thr²/(2·v_r_su_cd), with A_thr = 0.00012 m² (identified).

Unused legacy inputs of the surrounding study (pinch points, expander/pump
efficiencies) are kept as in the original.

## How to run

```bash
coolsolve ./plate_hx_pressure_drop_identification.eescode     # 37 equations, SUCCESS (6 iterations)
```

The fluid is the CoolProp mixture string `WorkingFluidMix$ = 'R245fa[1]&R134a[0]'`
(molar fractions `MM_fraction` and `1-MM_fraction`, written as numbers): at the
composition of the stored EES run, `MM_fraction = 1`, its properties are those of
pure R245fa; another composition needs the two numbers of the string changed
together with `MM_fraction` (CoolProp's predictive mixture model, see
*Limitations*). `.initials` holds the stored EES values as guesses; the model also
converges without them. Regression: `tools/test_models.py CSL-0124`.

## Results (stored operating point)

| Quantity | CoolSolve | EES stored | rel. diff |
|---|---:|---:|---:|
| `MM` molar mass [kg/kmol] | 134.048 | 134.048 | 0 |
| `h` single-phase HTC, Thonon [W/m²-K] | 260.77 | 259.43 | 5.12e-03 |
| `DELTAp` single-phase Δp, Thonon [Pa] | 479.21 | 479.24 | 6.01e-05 |
| `v_r_su_cd` supply specific volume [m³/kg] | 0.136124 | 0.136048 | 5.58e-04 |
| `DELTAp_cd_approx` orifice Δp [Pa] | 47 265 | 47 239 | 5.58e-04 |
| `DELTAp_ev` evaporator Δp, Hsieh [Pa] | 33 098 | 33 742 | 1.91e-02 |
| `DELTAp_tp` condenser Δp, Kuo [Pa] | 38 824 | 33 222 | 1.44e-01 |
| `alpha_tp_cd` condensation HTC, Kuo [W/m²-K] | 211.1 | 588.1 | 6.41e-01 |
| `h_tp_ev` boiling HTC, Hsieh [W/m²-K] | 2112 | 3848 | 4.51e-01 |

`rel. diff` is `|CoolSolve − EES| / max(|CoolSolve|, |EES|)`, as printed by
`tools/compare_solution.py`. The three two-phase outputs `alpha_tp_cd`,
`DELTAp_tp` and `h_tp_ev` are the ones affected by the corrections of the
original (see *Verification*). A figure (e.g. Δp vs mass flux for the three
correlations) can be added by the maintainer.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. pressure drop vs mass flow for the three correlations,
     figures/plate_hx_pressure_drop_identification_dp.png -->

## Verification

Reference: the EES stored solution (`~/Nextcloud/thermo_models/optim/
Identification pressure drops.EES`, 34 variables decoded), compared with
`tools/compare_solution.py --ees-units` (rtol = 0.001).

- **29 of the 34 common variables agree** within the tolerance at the stored
  operating point: the molar mass `MM`, the geometry and hypothesis inputs, the
  single-phase pressure drop `DELTAp` (6.0e-05) and the orifice block (≤ 5.6e-04).
- **`alpha_tp_cd`, `DELTAp_tp`, `h_tp_ev` differ by 14–64 %.** These three
  depend on the boiling number Bo, which the original computed with two errors,
  corrected here:
  1. in `kuo` and `Hsieh_new` the saturated enthalpies taken from REFPROP were
     molar (J/mol) while the densities and heat capacities were mass-based, so
     Bo = q/(G·i_fg) was about 7.5 times too large for R245fa (M = 134 kg/kmol);
  2. in `Hsieh_new` the liquid heat-transfer coefficient overwrote `h_l` before
     `i_fg = h_v − h_l` was evaluated, so the "latent heat" contained a
     heat-transfer coefficient.

  The corrected values are the reliable ones: `alpha_tp_cd` 211.1 (EES 588.1),
  `DELTAp_tp` 38 824 (33 222), `h_tp_ev` 2112 (3848). A scratch run with the
  original's molar convention and the `h_l` overwrite gives 628, 32 727 and
  3 868, within 7 % of the stored values: the stored EES values carry the two
  errors.
- **`h` and `DELTAp_ev` differ by 0.5 % and 1.9 %**, they are not affected by the
  corrections and follow from the R245fa property backend (CoolProp, at the
  revision pinned by CoolSolve, against the REFPROP 8 of EES; see *CoolProp pin
  and baselines* in the library workflow).

Regression: `tools/test_models.py CSL-0124` solves the file and compares it
with `plate_hx_pressure_drop_identification.sol`.

## Source and attribution

Working file of the ULiège Thermodynamics Laboratory (J. Lebrun laboratory
EES licence stamp; the `optim/` folder also holds the signed ORC files
`R245fa SQ101129`); no author named in the file — `TBD`, to be completed by
the maintainer. The Thonon, Kuo and Hsieh & Lin correlations are the standard
plate-HX ones (see the reference quoted inside `Hsieh_new`: Hsieh YY, Lin TF,
*Saturated flow boiling heat transfer and pressure drop of refrigerant R410a
in a vertical plate heat exchanger*, Int. J. Heat Mass Transfer 45 (2002)
1033–1044).

Source file (EES 8.652, comments mostly English), collection of S. Quoilin:
`~/Nextcloud/thermo_models/optim/Identification pressure drops.EES`
(inventory candidate `TM-0554`).

## Conversion log

- **2026-10-07 — import** (`tools/ees_extract.py`, CoolSolve v0.3.0@7addbbc):
  unit system already SI-°C-Pa-J; the EES licence tag was removed; no lookup
  or parametric tables; 34 variables with a stored solution. The three
  `//`-commented French input lines (alternative pinch points) were dropped
  (dead code); French comments translated ("surchauffe", "sous
  refroidissement", "rapport volumétrique de l'expanseur"…). Equations
  unchanged. `.initials` written from the stored values (the model also
  converges without them).
- **Level** (taxonomy §3): equations 37 (< 50 → 0); largest block 2 (→ 0);
  procedures present (→ 1); not multi-zone (→ 0); semi-empirical
  correlations + identified parameter A_thr (→ 1); default guesses suffice
  (→ 0). Score 2 → **level 2**.
- **2026-10-10 — REFPROP calls rewritten (decision D12)**: the 11 `CALL EES_REFPROP` blocks replaced by CoolProp calls on `WorkingFluidMix$` at the same states; `MM` mole-weighted; `h_l`, `h_v` in J/kg.
- **2026-10-10**: `$COMMON` of `Thonon`, `kuo` and `Hsieh_new` replaced by input arguments (not supported by CoolSolve): `WorkingFluidMix$` is the last input of each procedure and of each `CALL`.
- Two errors of the original are corrected: molar enthalpies in the boiling number of `kuo`/`Hsieh_new`, and `h_l` overwritten before `i_fg` in `Hsieh_new`.

## Limitations and CoolSolve gaps

- Mixtures: the property calls use the CoolProp mixture string
  `WorkingFluidMix$ = 'R245fa[1]&R134a[0]'` (x = `MM_fraction`, written as a number in
  the string); other compositions use CoolProp's predictive mixture model (CoolSolve
  warns that mixture properties may be less reliable).
- The original's own quirk is kept: `D_h = 2*b` with its open question
  *"or 2*b/phi ??????"*.
- No EES run of the corrected equations exists: the stored EES values of
  `alpha_tp_cd`, `DELTAp_tp`, `h_tp_ev` reflect the two errors of the original
  (see *Verification*); a freshly solved EES run of the corrected file is needed
  to verify them in EES.

## Related models

- `CSL-0113` *condenser_3_zones_plate_correlations*: three-zone plate
  condenser using the same correlation family (Thonon, Kuo); its REFPROP
  variant (TM-0562) is described, not imported.
- `CSL-0115` *hx_fem_evaporator_discretised*: R245fa evaporator of the same
  lab ORC model set (discretised, three U-value zones).

- `CSL-0153` *orc_whr_refprop_cost*: same plate-HX correlations (Thonon, Kuo, Hsieh) on the same CoolProp mixture string.
