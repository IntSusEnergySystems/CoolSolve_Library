# Three-zone plate evaporator with heat-transfer correlations (Thonon/Hsieh)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ☑️ **Runs** &nbsp;|&nbsp; `CSL-0114`

Plate heat exchanger evaporating R245fa, heated by thermal oil (a glycol
polynomial `prop_htf` procedure is also provided, as in the original). The
refrigerant side is described by three zones in series (subcooled liquid,
boiling two-phase, superheated vapour), the secondary fluid flows through
them in series, overall counterflow. Each zone is sized with a LMTD and zone
heat-transfer coefficients from plate-heat-exchanger correlations: Thonon for
the single-phase zones (constants tabulated per chevron angle) and Hsieh &
Lin for the two-phase zone. The model computes the required plate area
`A_ev`, the refrigerant-side pressure drop `DELTAp_ev` and the oil-side
pressure drop `DELTAp_hf_ev`, and (as in the original) writes the zone
boundary data into the lookup table `ev` for use by another model. An
auto-size variant file (`..._autosize.eescode`, R123/water demo case) comes
from the sibling source file of the same family.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | R245fa (refrigerant), oil (secondary), glycol polynomial optional |
| **Size** | 37 equations (largest block: 3) |
| **Source** | ULiège Thermodynamics Laboratory — `procedures EES/evaporator 3zones with correlations for PHX.EES` (variant: `procedures EES/PHE auto size SQ101020.EES`) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory); auto-size variant S. Quoilin |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; compared with the EES stored solutions of both source files (see *Verification*) |

## Problem statement

A plate evaporator (100 plates, 0.191 m wide, 1.9 mm channel gap, 45°
chevron angle, enlargement factor 1.2) evaporates 0.1364 kg/s of R245fa
entering subcooled at 55 °C and leaving superheated at 145 °C, at the
saturation pressure of 140 °C (≈ 2.837 MPa). The thermal oil (ρ = 800
kg/m³, cp = 2290 J/kg-K, ν = 1.85 cSt, k = 0.125 W/m-K) enters
counterflow at 175 °C, 0.186 kg/s, 15 bar. Compute the required
heat-transfer area `A_ev`, the refrigerant-side pressure drop `DELTAp_ev`
and the oil-side pressure drop `DELTAp_hf_ev`.

## Model

The refrigerant side has three zones delimited by the saturation states at
`p_ev`: liquid (subcooled supply → saturated liquid), two-phase (saturated
liquid → saturated vapour) and vapour (saturated vapour → superheated
exhaust). Zone heat rates come from the enthalpy differences; the oil
temperature drops through the vapour, two-phase and liquid zones in series
(overall counterflow). Each zone gives an `AU` from a LMTD (the `LMTD`
procedure returns a damped fallback when a temperature difference reaches
zero, as in the original), combined with the zone heat-transfer coefficient:

- single-phase zones and oil side: **Thonon correlation** — `Nu = C1·Re^m·Pr^(1/3)`,
  `f = C2·Re^(-pp)` with constants per chevron angle (25/30/45/60°) and Re
  range, as tabulated in the original file;
- two-phase zone: **Hsieh & Lin correlation** (Int. J. Heat Mass Transf. 45
  (2002) 033–1044, cited in the original) — liquid coefficient
  `h_l = 0.2092·(k_l/D_h)·Re_l^0.78·Pr_l^(1/3)` multiplied by `88·Bo^0.5`;
  friction `f_tp = 61000·Re_eq^(-1.25)` at the mean quality x_m = 0.5;
- `A_zone = AU_zone/U_zone` with `1/U = 1/h_sf + 1/h_r`, zone lengths
  `L = A/L_w_tot`, total area `A_ev = A_v + A_l + A_tp`;
- the `hx_ev` procedure finally writes the six zone boundary points
  (`M_dot_r·h`, refrigerant temperature, secondary-fluid temperature) into
  the lookup table `ev` (6 rows × 3 columns), as in the original.

As in the original, `hx_ev` calls `Hsieh` with a heat flux of 1E4 W/m² and a
unit plate length, and the plate length does not enter the area calculation
(the `Thonon` calls pass a unit length; zone lengths come out of
`A/L_w_tot`).

| Inputs | Value | Outputs | Value |
|---|---:|---|---:|
| `N_p` plates | 100 | `A_ev` area | 17.84 m² |
| `W` plate width / `b` gap | 0.191 m / 0.0019 m | `DELTAp_ev` refrigerant Δp | 1189 Pa |
| `beta` chevron angle / `PHI` | 45° / 1.2 | `DELTAp_hf_ev` oil-side Δp | 1243 Pa |
| `T_su_ev` / `T_su_exp` | 55 / 145 °C | `p_ev` evaporation pressure | 2.837 MPa |
| `T_ev` (saturation) | 140 °C | installed plate area `A` | 9.71 m² |
| `M_dot` / `M_dot_hf` | 0.1364 / 0.186 kg/s | | |
| `T_hf_su_ev` / `P_sf` | 175 °C / 15 bar | | |

## How to run

```bash
coolsolve ./evaporator_3_zones_plate_correlations.eescode
```

Solves from its inputs alone (`.initials` provided but not required). The
variant file `evaporator_3_zones_plate_correlations_autosize.eescode` (R123/
water demo case of the auto-size source file) is regression-tested as
`CSL-0114:autosize`.

## Results

At the default operating point the zone duties are 18.63 kW (liquid),
10.64 kW (two-phase) and 1.53 kW (superheating), 30.79 kW in total; the oil
leaves at 102.7 °C and the two-phase-zone pinch is 6.4 K. The required area
17.84 m² is larger than the installed plate area `A` = 9.71 m² (i.e. this
duty would need about twice the plates at this geometry). The arrays
`P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 subcooled supply, 2 saturated liquid,
3 saturated vapour, 4 superheated exhaust) give the evaporator path on the
P-h or T-s diagram (post-processing block, no effect on the results).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): evaporator path on the P-h diagram,
     figures/evaporator_3_zones_plate_correlations_ph.png -->

## Verification

**Native file vs TM-0570 stored solution** (EES 8.940, saved with its last
solution): `compare_solution.py` reports "19 common variables, 4 differ
(rtol=0.001)". All 15 inputs agree exactly, and so do the computed `A`
(9.714642 m²), `W_tot` and `L_w_tot` identities. The 4 differing variables:

- `p_ev`: 2.81518e6 (EES) vs 2.837e6 Pa (CoolSolve), rel. diff 7.69e-03 —
  the R245fa saturation pressure at 140 °C from the 2008-era EES property
  library vs CoolProp, consistent with the R245fa saturation deviations
  documented in `CSL-0019` and `CSL-0112`; within the "older EES fluid
  models: up to a few %" tolerance of CoolSolve `docs/ees_import.md` §11;
- `A_ev`, `DELTAp_ev`, `DELTAp_hf_ev`: the EES file stores 1 for all three
  call outputs — the EES guess value, not a solved result (the same stale
  record stores `L_h` = 0.5, a variable that no longer exists in the
  equations; the identities prove the stored inputs are real). The EES file
  therefore carries **no reference for the `hx_ev` outputs**.

With no stored reference available for the outputs, they are checked for
physical consistency: the energy balance `M_dot·(h[4] − h[1])` =
0.1364 kg/s × 225.75 kJ/kg = 30.79 kW closes with the oil side
(30.79 kW = 0.186 kg/s × 2290 J/kg-K × 72.3 K); the oil temperature drops
175 → 171.4 → 146.4 → 102.7 °C through the vapour, two-phase and liquid
zones, giving a positive two-phase pinch of 6.4 K against `T_ev` = 140 °C.

**Variant vs TM-0582 stored solution** (EES 8.652, 30 variables):
`compare_solution.py` reports "22 common variables, 5 differ (rtol=0.001)".
The 17 agreeing variables are all inputs plus the exact identities
(`L_w_tot` = 2.52 m) and the computed `h_sf_su_ev` = 719 395.6 J/kg
(water enthalpy at 10 bar / 170 °C, EES vs CoolProp ≤ 0.1 %). The 5
differing variables (`A_ev` 1.37e-01, `DELTAp` 3.08e-02, `DELTAp_sf`
1.70e-03, `h_sf_ex_ev` 9.92e-03, `Q_dot_ev` 2.89e-02) cannot be counted as
reference values, for two reasons:

1. The stored EES record is internally inconsistent: it stores
   `A_ev` = −0.948 m² but also `A_l` + `A_tp` + `A_v` = 1.145 + 0.565 +
   7.900 = 9.610 m², which the file's own equation `A_ev = A_v + A_l + A_tp`
   contradicts — the stored outputs are a stale mixture from an earlier
   revision/run of the file (as for TM-0569, documented in `CSL-0112`).
2. The R123/water demo case sits on the wrong side of the saturation line:
   `T_r_su_ev` = 50 °C vs `T_sat`(2 bar) = 48.05 °C, so the supply is 1.95 K
   superheated and the "liquid" zone runs backwards: CoolSolve zone duties
   −16.28 + 16.13 + 3.93 kW = 3.79 kW — a small difference of large,
   cancelling enthalpy differences, highly sensitive to the R123 property
   backend (both tools give a negative `A_ev`).

**Parametric table of TM-0582**: the extraction decodes an 851 × 2
parametric table (`v`, `H_dot`); its decoded content is mostly empty cells
with scattered values and no usable reference run — it was checked against
the file (row/column counts and values) and is documented here as a leftover
of the auto-size study, not reproduced in the library (CoolSolve has no
parametric-table file, `CS-GAP-PARAMETRIC`).

## Source and attribution

Evaporator file from the ULiège Thermodynamics Laboratory collection; the
file names no author and only carries the EES licence tag of the laboratory
(J. Lebrun), so the author is recorded as TBD. The auto-size source file
`PHE auto size SQ101020.EES` is signed `SQ101020` in its file name
(S. Quoilin, 2010-10-20, matching the inventory `authors` entry). The
Thonon single-phase correlation and the Hsieh & Lin plate-boiling
correlation are cited by name in the original files; the published sources
are B. Thonon et al. (plate heat exchanger design correlations, single
phase) and Y.-Y. Hsieh, T.-F. Lin, "Saturated flow boiling heat transfer and
pressure drop of refrigerant R410a in a vertical plate heat exchanger",
Int. J. Heat and Mass Transfer 45 (2002) 033–1044.

Source files (EES 8.940 / 8.652), collection of S. Quoilin:
`~/Nextcloud/thermo_models/procedures EES/evaporator 3zones with correlations for PHX.EES`
(inventory candidate `TM-0570`) and
`~/Nextcloud/thermo_models/procedures EES/PHE auto size SQ101020.EES`
(inventory candidate `TM-0582`); external lookup table
`~/Nextcloud/thermo_models/procedures EES/evaporator 1 2 & 3 zones SQ080603.lkt`.

## Conversion log

- **2026-10-07 — import** (`tools/ees_extract.py`): unit system already
  SI-°C-Pa-J in both files (no manual conversion); the EES licence tag was
  removed; comments translated to English where needed (the oil block of
  `prop_htf`: "en cSt" → "in cSt" etc.) and the standard header added; the
  `$bookmark` navigation lines are kept as in the original. Equations,
  variable names and the default operating points are unchanged
  (TM-0570 as the native file, TM-0582 as the `autosize` variant file —
  the two source files differ in the secondary-fluid path (enthalpy-based
  with `temperature(fluidev$, h=…, p=…)` calls vs constant `cp`), in the
  `DELTAp` normalisation by `L_h` and in the `Thonon` length argument; both
  transcriptions are native EES). The external `.lkt` table `ev` (binary
  W8.051 layout, not decoded by the tool — `CS-GAP-LKT`) is shipped as the
  companion table `evaporator_3_zones_plate_correlations-ev.csv` (6 × 3,
  `E_r_W`, `T_r_C`, `T_sf_C`) filled with the values the model writes at
  the default operating point. Post-processing state-point arrays added for
  the CoolSolve diagrams (results unchanged).
- **Level**: equations 37 (< 50 → 0), largest block 3 (≤ 5 → 0),
  procedures present (→ 1), multi-zone (three zones → 1), semi-empirical
  correlations (→ 1), numerics: solves from the inputs alone (→ 0);
  score 3 → level 2.

## Limitations and CoolSolve gaps

- The `lookup('ev', …)` write statements of `hx_ev` are **silently dropped**
  by CoolSolve (`CS-BUG-LOOKUP-WRITE`, registered; the same statements in a
  main program make the system non-square). The physics results are
  unaffected; the companion table `…-ev.csv` keeps the default values the
  model would write, for the models that read the `ev` table (the original
  design passes it to another model of the same cycle).
- The `hsieh` zone-average heat-transfer coefficient depends on the imposed
  heat flux (1E4 W/m² as in the original): the two-phase area `A_tp`
  inherits this choice, as in the original file.
- The `prop_htf` polynomials are only reached for `fluid$ = 'glycol'` or
  `'oil'` (the default operating point uses oil).
- No CoolSolve gap blocks the native file (`missing_features` is empty, as
  for `CSL-0112`, which carries the same lookup-write statements).

## Related models

- `CSL-0112` *three_zone_hx_procedures*: the epsilon-NTU/parametric
  procedures of the same three-zone family (`hx_ev_three_zones`,
  `lmtd_xi1000`), imported from the sibling source files.
- `CSL-0113` *condenser_3_zones_plate_correlations*: the three-zone plate
  condenser of the same family (Thonon/Kuo, R123/water).
- `CSL-0115` *hx_fem_evaporator_discretised*: the same evaporator duty
  treated fully discretised (N finite-volume cells) instead of three lumped
  zones.
- `CSL-0079` *brineprop_secondary_refrigerants*: property library for
  aqueous secondary refrigerants (glycol), an alternative to the `prop_htf`
  glycol polynomial.
- `CSL-0121` *heat_transfer_fluid_properties*: library version of the source
  `prop_htf` procedure (renamed `prop_heat_transfer_fluid`, with the
  `therminol66`/`TherminolVP-1` branches and a built-in fluid fallback).

- `CSL-0153` *orc_whr_refprop_cost*: three-zone plate evaporator (Thonon/Hsieh).
