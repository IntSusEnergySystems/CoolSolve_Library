# Plate heat exchangers: heat-transfer and pressure-drop correlations (function library)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0111`

Ten EES `PROCEDURE`s for the corrugated channel of a chevron plate heat
exchanger, transcribed from the ULiège procedure file used by the laboratory's
plate-HX models. Six correlations are single-phase (Kumar, Thonon, Muley,
Bogaerts, Martin, Wanniarachchi) and four are two-phase condensation or flow
boiling (Kuo-Lie-Hsieh-Lin, Hsieh-Lin, Yan-Lio-Lin, Han-Lee-Kim); each returns
a heat-transfer coefficient and a pressure drop for one side. The properties
are evaluated inside the procedures from `fluid$` and the state, so a calling
model only passes the state, the mass flow rate and the geometry. Related
model: `CSL-0096`, an independent transcription of the overlapping
single-phase correlations from the Python library `ht`.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | R410A (demonstration; the procedures take any `fluid$`) |
| **Size** | 39 main-program equations (largest block: 4) + ~200 equations in the 10 procedure bodies |
| **Source** | ULiège collection: `~/Nextcloud/thermo_models/procedures EES/PHEX correlations SQ150128.EES` (TM-0585, S. Quoilin) and `~/Nextcloud/thermo_models/procedures EES/single phase hx  martin - SQ080229.EES` (TM-0496, S. Bertagnolio and S. Quoilin) |
| **Authors** | Sylvain Quoilin (procedures); Stéphane Bertagnolio (martin procedure of TM-0496) |
| **License** | MIT |
| **CoolSolve** | **verified** against the EES stored solution of TM-0585 and against `ht` 1.2.0 Python values (HT-010) |

## Problem statement

Give the wall heat-transfer coefficient and the pressure drop of one side of a
chevron plate heat exchanger: `h = Nu·k/D_h` from a Nusselt correlation and
`DELTAp = f·2·G²·L/(rho·D_h)` from a friction correlation, for the geometry
(number of plates, channel spacing, plate width and length, chevron angle,
enlargement factor). The correlations are written for different fluids and
regimes; the choice is left to the user. In these correlations `beta` (the
chevron angle) is defined **as in the original file** as the angle between the
axial flow and the corrugations: `beta = 0` parallel to the flow, `beta = 90`
perpendicular. Note that `ht`/`CSL-0096` and Martin's paper use the
complementary angle (to the vertical axis); a correlation selected for a given
`beta` in one convention must be read at `90 − beta` in the other.

## Model

| Procedure | Arguments (after `fluid$`) | Returns | Reference (as quoted in the source file) |
|---|---|---|---|
| `kuo` | P, M_dot, q, N_p, b, W, L | h_tp_cd, DELTAp | Kuo, Lie, Hsieh, Lin, condensation of R410A in a vertical plate HX, *Int. J. Heat Mass Transfer* 48 (2005) 5205-5220 |
| `Hsieh` | P, M_dot, q, N_p, b, W, L | h_tp_ev, DELTAp | Hsieh, Lin, saturated flow boiling of R410A, *Int. J. Heat Mass Transfer* 45 (2002) 1033-1044 |
| `Kumar` | P, T, M_dot, N_p, b, W, L, beta, mu_ratio, phi | h, DELTAp | Kumar, *The Plate Heat Exchanger: Construction and Design*, IChemE Symp. Series 86 (1984); coefficients as tabulated by Ayub (2003) |
| `Thonon` | P, T, M_dot, N_p, b, W, L, beta, mu_ratio, phi | h, DELTAp | Thonon, *Design Method for Plate Evaporators and Condensers*, 1st Int. Conf. Process Intensification, BHR (1995); via Ayub (2003) |
| `Muley` | P, T, M_dot, N_p, b, W, L, beta, mu_ratio, phi | h, DELTAp | Muley, Manglik, turbulent flow in a chevron plate HX, *Trans. ASME* (1999) |
| `Bogaerts` | P, T, M_dot, N_p, b, W, L, mu_ratio | h, DELTAp | Bogaert, Boles, global performance of a prototype brazed plate HX, *Experimental Heat Transfer* 8 (1995) 293-311 |
| `martin` | A_bar, lambda, beta, k_w, t, L_p, W, N_p, T_m, T_w, P_m, M_dot_f, mu_ratio | R_f, DELTAp, h_f, A_hex | Martin, A theoretical approach to predict the performance of chevron-type plate heat exchangers, *Chem. Eng. Processing* 35 (1996) 301-310 (VDI Heat Atlas friction factor) |
| `Wanniarachchi` | T, p, M_dot, N_p, b, W, L, phi, mu_ratio, beta | h, DELTAp | Wanniarachchi, Ratnam, Tilton, Dutta, *Approximate correlations for chevron-type plate heat exchangers*, ASME (1995) |
| `Han` | P, M_dot, N_p, b, W, L, beta, phi | h, DELTAp | Han, Lee, Kim, condensation in brazed plate HXs with different chevron angles (2003) |
| `Yan` | P, M_dot, q, N_p, b, W, L | h, DELTAp | Yan, Lio, Lin, condensation of R134a in a plate HX, *Int. J. Heat Mass Transfer* 42 (1999) 31 |

Geometry arguments: `N_p` number of plates `[-]`, `b` channel spacing `[m]`,
`W` plate width `[m]`, `L`/`L_p` effective plate length `[m]`, `beta` chevron
angle `[degrees]`, `phi` area enlargement factor `[-]`, `A_bar` corrugation
amplitude `[m]`, `lambda` corrugation wavelength `[m]`, `t` plate thickness
`[m]`, `k_w` plate thermal conductivity `[W/m-K]`, `q` heat flux `[W/m²]`,
`mu_ratio` bulk-to-wall viscosity ratio `[-]` (1 to disable the correction).
State arguments: `P`/`p` pressure `[Pa]`, `T` temperature `[°C]`, `T_m`/`T_w`
bulk/wall temperature `[°C]`, `M_dot` mass flow rate `[kg/s]`. Two-phase
procedures evaluate saturated liquid/vapour properties at their pressure.

The demonstration main program is the default operating point of the source
file: R410A, `M_dot` = 0.3 kg/s, `p` = 1 MPa, `q` = 10 kW/m², `N_p` = 25,
`b` = 2 mm, `W` = 0.21 m, `L` = 0.5 m, `beta` = 60°, `phi` = 1.2,
`T` = 10 °C (superheated vapour: `T_sat` = 7.22 °C at 1 MPa). The output names
are those of the original main program; note that it feeds `kuo` into `h_ev`
and `Hsieh` into `h_cd` (the two procedures are the other way round), kept as
in the original.

## How to run

```bash
coolsolve ./plate_hx_correlations.eescode
```

No `.initials` needed: the demonstration solves from the default guesses
(18 iterations). Models that need these procedures copy the definitions into a
`{--- Library functions copied from CSL-0111 ---}` block until CoolSolve
supports `$INCLUDE library:<name>` (`CS-FEAT-IMPORT`).

## Results

At the default operating point (CoolSolve; EES stored value in parentheses):

| Quantity | CoolSolve | EES (stored) |
|---|---:|---:|
| `h_ev` (kuo) [W/m²-K] | 1262.5 | 1256.7 |
| `h_cd` (Hsieh) [W/m²-K] | 5350.0 | 5325.3 |
| `h_yan` [W/m²-K] | 4132.2 | 4129.1 |
| `h_thonon` [W/m²-K] | 1060.4 | 1083.9 |
| `h_kumar` [W/m²-K] | 876.0 | 893.5 |
| `h_Muley` [W/m²-K] | 639.1 | 656.5 |
| `h_bogaerts` [W/m²-K] | 1049.5 | 1068.9 |
| `h_martin` [W/m²-K] | 474.0 | 485.1 |
| `h_wan` [W/m²-K] | 807.7 | 824.6 |
| `R_f` (martin) [K/W] | 6.664e-4 | 6.512e-4 |
| `A_hex` (martin) [m²] | 3.1657 | 3.1657 |
| `DELTAp_martin` [Pa] | 2892.6 | 2878.9 |
| `DELTAp_ev` (kuo) [Pa] | 14 783 | 14 960 |
| `DELTAp_cd` (Hsieh) [Pa] | 10 539 | 10 699 |
| `DELTAp_yan` [Pa] | 313.1 | 314.5 |
| `DELTAp_bogaerts` [Pa] | 61 157 | 61 154 |
| `T_sat` [°C] | 7.2200 | 7.2200 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. a parametric
     sweep of one single-phase h over the Reynolds number. -->

## Verification

**1. EES stored solution of TM-0585** (`compare_solution.py plate_hx_correlations.sol reference/ees_variables.csv`):
38 common variables, 19 differ at `rtol=0.001`; maximum relative deviation
**5.83e-2 on `mu`** (and `Re`), the R410A viscosity — a property-backend
difference (EES R410A formulation vs the CoolProp pseudo-pure model), not a
correlation difference. All correlation outputs follow the viscosity through
`Re ∝ 1/mu` and stay within **2.66e-2** (`h_Muley`); the pure geometry outputs
(`A_hex`, `T_sat`) agree to <1e-6. Seven variables of the EES reference are
excluded as stale records of earlier runs, absent from the last equations
window: `A_bar`, `L_p`, `mu_ratio` (call-site variables of an earlier
argument list), `h`, `DELTAp` (earlier main-program names) and `h_han`,
`DELTAp_han` (values of a run that still had the Han call active). The 2005
Hsieh/2005 Kuo deviations (0.46-1.5e-2) are consistent with the same
viscosity ratio.

**2. `ht` 1.2.0 Python values (family HT-010, cf. `CSL-0096`)**, at the
CoolSolve operating point, each implementation with its own internal Re:

| Correlation | Nu (this model) | Nu (`ht` 1.2.0) | rel. diff |
|---|---:|---:|---:|
| Martin VDI | 116.921 | 116.921 | 4.6e-13 |
| Kumar | 217.135 | 217.329 | 9.0e-4 |
| Muley-Manglik | 190.090 | 345.425 | 4.5e-1 (the original file's typo, below) |

- **Kumar**: the EES file's `beta >= 60` coefficient row (C1 = 0.348,
  m = 0.663) is `ht`'s row for a chevron angle of **30°** — the two sources
  use complementary chevron-angle conventions (angle to the flow axis vs to
  the vertical axis); compared at `90 − beta` the two agree within 9e-4.
- **Martin**: identical equation and coefficients (VDI Heat Atlas friction
  factor); agreement is at round-off level.
- **Muley**: the source file writes `− 10.51·phi³` in the enlargement-factor
  polynomial where the published correlation (and `ht`) has `− 10.1507·phi³`;
  all its other constants match the published values. The file's own stored
  solution (h_Muley = 656.5) confirms the author's file really uses 10.51, so
  the typo is **kept** (faithful transcription). With the published constant
  the coefficient becomes 345.8, within 1e-3 of `ht`. Impact of the typo as
  published: −45 % on Nu at `phi` = 1.2. The other single-phase correlations
  of this file have no counterpart in `ht` (Thonon, Bogaerts, Wanniarachchi)
  or are two-phase forms not present in `ht/boiling_plate.py` (Kuo, Hsieh,
  Yan-condensation, Han-condensation); the HT-005 family of `ht`
  (internal laminar flow) concerns tubes, not plate channels, so no HT-005
  value applies.

## Conversion log

From `PHEX correlations SQ150128.EES` (EES X9.721, unit system already
`SI MASS DEG PA C J` — no unit conversion) and `single phase hx  martin -
SQ080229.EES`:

- **Workarounds forced by CoolSolve bugs** (the EES syntax of the source is
  valid; each change is behaviour-preserving):
  - `pi` → `pi()` inside the `martin`, `Muley` and `Han` bodies: the constant
    `pi` evaluates as 1 in a subprogram body (`CS-BUG-PI-FUNCTION`; `pi()`
    works).
  - `g#` → literal `9.80665 m/s²` in `kuo` (`Fr_l`): the EES constant `g#`
    (standard gravitational acceleration) also evaluates as 1 in a subprogram
    body — same bug class, verified with a reproducer (t7 of the import
    notes); same workaround as `g` in `CSL-0096`.
- **Han not demonstrated**: the original main program leaves the Han call
  commented out, and for a reason: with its `Ge` coefficients built on
  `(p/D_h)^4.17` where `p` is the fluid pressure (the paper presumably used a
  geometric pitch ratio), the procedure returns absurd pressure drops at any
  realistic pressure. The procedure is transcribed unchanged; the call stays
  commented as in the original (documented decision).
- The commented-out alternative friction factor of `Hsieh`
  (`f_tp = 23820·Re^-1.12`) and the commented-out beta-dependency terms of
  `Han` are dead code of the original, kept as comments.
- The martin procedure is the TM-0585 variant (arguments `W` and `mu_ratio`,
  wall viscosity `mu/mu_w = VISCOSITY(...)/mu_ratio`). The TM-0496 variant has
  argument `L_w` instead of `W`, no `mu_ratio` (wall viscosity taken at `T_w`
  directly) and computes `DELTAp` in the algebraically identical form
  `f·rho·u²·L_p/(2·d_h)`; TM-0561 (`AU_Martin_rudy.EES`, C-121 `duplicate` of
  TM-0496) carries the same procedure with a 50 % glycol demonstration. The
  library ships the TM-0585 form once.
- Comments translated to English; French fragments of the original comments
  paraphrased; trailing whitespace removed.

## Level justification

Taxonomy §3 score: ~240 equations including the procedure bodies (50-300: 1
point), largest algebraic block 4 (≤ 5: 0), procedures present (1), single
empirical correlations without calibration or off-design (0), default guesses
suffice (0) → score 2 → **level 2**, same rating as the comparable `CSL-0096`.

## Source and attribution

- ULiège collection (maintainer's laboratory, MIT): `PHEX correlations
  SQ150128.EES` (TM-0585, 2015-01-28, S. Quoilin — representative of the
  DG-0129 group per the C-121 triage) and `single phase hx  martin -
  SQ080229.EES` (TM-0496, S. Bertagnolio and S. Quoilin, martin procedure and
  its `martin_hx` demonstration). The scientific basis of each correlation is
  the paper cited in its comment block (table above).
- Related models: `CSL-0096` (`ht` HT-010 transcription of the Kumar, Martin
  and Muley-Manglik single-phase correlations, independent source), the
  ULiège plate-HX component models that embed copies of these procedures
  (e.g. `condenser_3_zones_plate_correlations`,
  `evaporator_3_zones_plate_correlations`), and `CSL-0161`
  (`plate_hx_thermal_resistances`, the 2008 single-phase plate-HX resistance
  model whose inline Martin equations this library supersedes as procedures).
