# Three-zone plate condenser with heat-transfer correlations (Thonon/Kuo)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0113`

Plate heat exchanger condensing R123, cooled by water (a glycol polynomial
`prop_htf` procedure is also provided, as in the original). The refrigerant
side is described by three zones in series (desuperheating, condensation,
subcooling), the secondary fluid flows through them in series, overall
counterflow. Each zone is sized with a LMTD and zone heat-transfer
coefficients from plate-heat-exchanger correlations: Thonon for the
single-phase zones (constants tabulated per chevron angle) and Kuo for the
two-phase zone. The model computes the required plate area, the refrigerant
and secondary-side pressure drops and the refrigerant hold-up mass.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | R123 (refrigerant), Water (secondary), glycol polynomial optional |
| **Size** | 35 equations (largest block: 4) |
| **Source** | ULiège Thermodynamics Laboratory — `procedures EES/condenser 3 zones with correlations.EES` |
| **Authors** | TBD (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — verified against the EES stored solution (5.56e-02 max rel. diff, see *Verification*) |

## Problem statement

A plate condenser (75 plates, 0.112 m wide between gaskets, 2.4 mm channel
gap, 45° chevron angle) condenses 0.1976 kg/s of R123 entering superheated at
84.56 °C and leaving subcooled at 36.02 °C, at a condensing pressure of
159 463 Pa. The cooling water enters at 15 °C, 0.5 kg/s, 1 bar. Compute the
required heat-transfer area `A_cd`, the refrigerant-side pressure drop
`DELTAp_cd`, the water-side pressure drop `DELTAp_sf_cd`, the refrigerant
hold-up mass `M_fluid_cd` and the condenser volume `V_cd`.

## Model

The refrigerant side has three zones delimited by the saturation states at
`p_cd`: vapour (superheated supply → saturated vapour), two-phase (saturated
vapour → saturated liquid) and liquid (saturated liquid → subcooled
exhaust). Zone heat rates come from the enthalpy differences; the water
temperature rises through the liquid, two-phase and vapour zones in series
(overall counterflow). Each zone gives an `AU` from a LMTD (the `LMTD`
procedure returns a damped fallback when a temperature difference reaches
zero, as in the original), combined with the zone heat-transfer coefficient:

- single-phase zones and water side: **Thonon correlation** — `Nu = C1·Re^m·Pr^(1/3)`,
  `f = C2·Re^(-pp)` with constants per chevron angle (25/30/45/60°) and Re
  range, as tabulated in the original file;
- two-phase zone: **Kuo correlation** — liquid-dominant coefficient
  `h_r_l = 0.2092·(k_l/D_h)·Re_l^0.5·Pr_l^(1/3)` (identified experimentally
  with water, comment of the original) multiplied by a quality-dependent
  enhancement factor integrated from x = 0.01 to 0.95; friction
  `f_tp = 21500·Re_eq^(-1.14)·Bo^(-0.085)`;
- `A_zone = AU_zone/U_zone` with `1/U = 1/h_sf + 1/h_r`, zone lengths
  `L = A/L_w_tot`, total area `A_cd = A_v + A_tp + A_l`;
- `M_fluid_cd = (A_l + A_tp/2)·b·ρ_l` (hold-up of the liquid zone plus half
  of the two-phase zone).

As in the original, `hx_cd` calls `kuo` with a heat flux of 1E5 W/m² and
unit values of `N_p` and `coef`, and the plate length does not enter the area
calculation (the `Thonon` calls pass a unit length; zone lengths come out of
`A/L_w_tot`).

| Inputs | Value | Outputs | Value |
|---|---:|---|---:|
| `N_p_cd` plates | 75 | `A_cd` area | 5.59 m² |
| `L_w` plate width | 0.112 m | `DELTAp_cd` refrigerant Δp | 48.4 kPa |
| `b` channel gap | 0.0024 m | `DELTAp_sf_cd` water-side Δp | 373 Pa |
| `beta` chevron angle | 45° | `M_fluid_cd` hold-up | 7.63 kg |
| `T_r_su_cd` / `T_r_ex_sc_cd` | 84.56 / 36.02 °C | `V_cd` volume | 0.0134 m³ |
| `M_dot_r` / `M_dot_w` | 0.1976 / 0.5 kg/s | | |
| `p_cd` / `p_w` | 159 463 / 100 000 Pa | | |

## How to run

```bash
coolsolve ./condenser_3_zones_plate_correlations.eescode
```

Solves from its inputs alone (`.initials` provided but not required).

## Results

The desuperheating duty is 6.4 kW (16 % of the 39.9 kW total), the
condensation duty 32.5 kW and the subcooling duty 1.0 kW. The arrays
`P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 superheated supply, 2 saturated vapour,
3 saturated liquid, 4 subcooled outlet) give the condenser path on the P-h
or T-s diagram (post-processing block, no effect on the results).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): condenser path on the P-h diagram,
     figures/condenser_3_zones_plate_correlations_ph.png -->

## Verification

Against the EES stored solution of the source file (EES 8.940, saved with its
last solution): `compare_solution.py` reports "17 common variables, 5 differ
(rtol=0.001)" with relative differences 3.71e-02 (A_cd), 5.56e-02
(DELTAp_cd), 3.69e-02 (DELTAp_sf_cd), 5.26e-02 (M_fluid_cd), 3.71e-02
(V_cd); all other common variables (every input) agree exactly; `L_h` exists
only in the EES reference (vestigial stored value of an earlier version of
the file, not defined by the current equations).

The five differing variables are the integrated outputs, and all of them
inherit the same cause: the model equations and inputs are identical, so the
deviation can only come from the property values. The results are sensitive
through the desuperheating duty `Q_dot_v = M_dot_r·(h_su − h_sat_v)`, a small
difference of large enthalpies (CoolProp: 438.4 − 406.1 = 32.3 kJ/kg,
≈ 16 % of the total duty) evaluated 43.6 K above saturation; the 2008-era EES
R123 property library differs from CoolProp's Helmholtz formulation in this
region. The CoolProp saturation values check against published R123 tables:
T_sat = 40.97 °C and h_fg = 164.5 kJ/kg at 159.463 kPa. The deviation is
within the "older EES fluid models: up to a few %" tolerance of CoolSolve
`docs/ees_import.md` §11, explained here; the 5.56e-02 on `DELTAp_cd` is the
same zone-split difference amplified by the pressure-drop correlation.

## Source and attribution

File from the ULiège Thermodynamics Laboratory collection (2011); the file
names no author and only carries the EES licence tag of the laboratory
(J. Lebrun), so the author is recorded as TBD. The Thonon single-phase
correlation and the Kuo et al. plate-condensation correlation are cited by
name in the original file (bookmarks `thonon`, `kuo`); the published sources
are B. Thonon et al., plate heat exchanger design correlations (single
phase), and W. S. Kuo, Y. M. Lie, Y. Y. Hsieh, T. F. Lin, "Condensation heat
transfer and pressure drop in plate heat exchangers", Int. J. Heat and Mass
Transfer 48 (2005) 5205–5219 (two phase).

Source file (EES 8.940), collection of S. Quoilin:
`~/Nextcloud/thermo_models/procedures EES/condenser 3 zones with correlations.EES`
(inventory candidate `TM-0563`).

## Conversion log

- **2026-10-07 — import** (`tools/ees_extract.py`): unit system already
  SI-°C-Pa-J; the file uses the European decimal-comma display convention
  (`36,02`, `;` argument separators), converted to the dot convention by the
  extraction — a display convention of EES, no equation changed; the EES
  licence tag was removed; comments translated to English where not already
  English (the file was in English) and the standard header added; the
  `$bookmark` navigation lines are kept as in the original. Equations,
  variable names and the default operating point are unchanged. Post-
  processing state-point arrays added for the CoolSolve diagrams (results
  unchanged).
- **Level**: equations 35 (< 50 → 0), largest block 4 (≤ 5 → 0),
  procedures present (→ 1), multi-zone (three zones → 1), semi-empirical
  correlations (→ 1), numerics: solves from the inputs alone (→ 0);
  score 3 → level 2.

## Limitations and CoolSolve gaps

- The kuo zone-average heat-transfer coefficient depends on the imposed heat
  flux (1E5 W/m² as in the original) and unit correction coefficients: the
  zone area `A_tp` inherits these choices, as in the original file.
- The `prop_htf` glycol polynomial is only reached for `fluidcd$ = 'glycol'`
  (the default operating point uses water); its T input is in °C, as in the
  original.
- No CoolSolve gap blocks this model.

## Related models

- `CSL-0008` *condenser_three_zones*: three-zone condenser at the parametric
  level of detail (epsilon-NTU with fitted conductances, air-cooled).
- `CSL-0096` *plate_hx_heat_transfer*: single-phase plate heat exchanger
  model.
- `CSL-0079` *brineprop_secondary_refrigerants*: property library for aqueous
  secondary refrigerants (glycol), an alternative to the `prop_htf` glycol
  polynomial.

- `CSL-0115` *hx_fem_evaporator_discretised*: the same two-phase heat
  exchanger treated fully discretised (N finite-volume cells, cell-by-cell U
  switching smoothed over a quality window) instead of three lumped zones.
- `CSL-0124` *plate_hx_pressure_drop_identification*: pressure-drop and
  two-phase heat-transfer correlations of the same plate-HX family
  (Thonon, Kuo) in their REFPROP-mixture source version (blocked; R245fa
  variant).
- `CSL-0121` *heat_transfer_fluid_properties*: library version of the source
  `prop_htf` procedure (renamed `prop_heat_transfer_fluid`, with the
  `therminol66`/`TherminolVP-1` branches and a built-in fluid fallback).
- `CSL-0114` *evaporator_3_zones_plate_correlations*: the evaporator counterpart of the same lab file family (same zone structure, Thonon single phase and Hsieh & Lin boiling instead of Kuo; R245fa/oil default point and an auto-size variant file).
