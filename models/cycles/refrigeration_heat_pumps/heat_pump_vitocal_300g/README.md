# Vitocal 300G brine-to-water heat pump (scroll compressor, two plate heat exchangers)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0116`

Design/simulation model of a water-to-water heat pump of the Vaillant Vitocal
300G type: an R134a cycle whose scroll compressor is described either by the
semi-empirical model of Winandy et al. (2002) — supply heating-up, mixing with
the internal leakage flow, swept-volume flow, isentropic compression to the
adapted (built-in) pressure, isochoric compression to the discharge pressure,
exhaust pressure drop, exhaust cooling-down and a fictitious-envelope heat
balance — or by the ARI/Copeland third-order catalogue polynomial (switch
`compressortype$`; the stored run uses `'ari'`). The plate evaporator is
sized on a 30 % ethylene-glycol brine (Thonon single-phase and Hsieh
two-phase correlations), the plate condenser on the water circuit (Thonon and
Kuo); both return area, zone-by-zone pressure drops, pinch points and
refrigerant hold-up.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R134a; EG brine 30 % (EES incompressible library / BrineProp2) and water on the source/sink circuits |
| **Size** | ~392 equation lines, 8 FUNCTION/PROCEDURE definitions (`lmtd`, `thonon`, `kuo`, `hx_cd`, `hsieh`, `hx_evv`, `deltat_ln`, `copeland`); does not parse in CoolSolve (see *Limitations*) |
| **Source** | ULiège Thermodynamics Laboratory — consulting/study file `HeatPump_Vitocal 300G -110_CGSQ1112288.EES` |
| **Authors** | Sylvain Quoilin (ULiège Thermodynamics Laboratory) — from the file-name initials `SQ`; the `{$ID$}` tag names the EES licence holder (J. Lebrun), not the author |
| **License** | MIT |
| **CoolSolve** | **blocked** (native file; gap IDs below). No runnable variant: the compressor catalogue table `ZH38K4E-TFD` is not recoverable (see *How to run*) |

## Problem statement

Given the two plate heat exchangers (their geometry and area), the
compressor parameters (identified on the Copeland ZH38K4E-TFD catalogue) and
the operating conditions (condensing temperature, water inlet temperature,
brine supply temperature, flows), the model computes the refrigerant flow
rate, the compressor electrical power, the heating capacity, the COP, the
compressor exhaust temperature and wall temperature, and the detailed
exchanger results (areas, pressure drops, pinch points, hold-up).

## Model

- **Compressor** (Winandy et al. 2002 [1], parameters from the Copeland
  catalogue, as in `CSL-0007`): fictitious envelope at `t_w_cp` with
  NTU-effectiveness heat transfers to the suction and exhaust flows, ambient
  loss `AU_amb_cp*(t_w_cp - t_amb)`, internal leakage through an equivalent
  throat area `A_leak_cp` (isentropic flow to the throat, critical or
  adapted back-pressure), built-in volume ratio `r_v_in_cp = 2.8`
  (isentropic compression to the adapted pressure, then isochoric
  compression to the exhaust pressure), exhaust valve pressure drop
  (incompressible flow through `A_ex`), electromechanical losses
  `W_dot_loss0_cp + alpha_cp*W_dot_in_cp`. Volumetric effectiveness
  `epsilon_v_cp = M_dot_r/M_dot_s_cp`, isentropic effectiveness and pressure
  ratio are returned.
- **ARI catalogue mode** (`compressortype$ = 'ari'`, the stored run): the
  electrical power and mass flow are third-order polynomials of the
  Fahrenheit evaporation/condensation temperatures (10 coefficients read in
  the external lookup table `ZH38K4E-TFD`, columns `W`, `M`, `Vs`; the `M`
  result is converted with `convert(lbm/hr,kg/s)`); the exhaust state
  follows from the energy balance.
- **Plate evaporator** (`hx_evv`): two refrigerant zones (two-phase +
  superheated vapour), zone `AU = Q/DELTAT_log`, overall `U` from the
  Thonon single-phase correlations of both sides and the Hsieh & Lin (2002)
  flow-boiling correlation, area from `AU/U`, two-phase pressure drop of
  Kuo et al. form, pinch point, brine-side pressure drop; writes three rows
  into the lookup table `ev` (diagnostic).
- **Plate condenser** (`hx_cd`): three refrigerant zones (desuperheating,
  condensing, subcooling), same structure with the Kuo et al. condensation
  correlation, hold-up mass `M_fluid_cd`.
- **Brine properties**: `CALL BRINEPROP2('EG',30,-5:…)` (ULiège BrineProp2
  library, implicit USERLIB) on the evaporator side; the EES
  incompressible-substance library (`'EG'` with `C=30`) in `Thonon`, `hx_cd`
  and the condenser water-side `c_w` (the file sets `fluidcd$='EG'`, i.e.
  the sink side also uses the 30 % EG properties of the library although the
  description says water — as in the original).
- Cycle: isenthalpic expansion, evaporating/condensing temperatures defined
  at `x=0.5` (manufacturer convention), 3 K superheating and subcooling.
- State points `p[i]`, `T[i]`, `h[i]`, `s[i]` (i = 1..10) and the two
  secondary-fluid temperatures `T_hf[2]`, `T_hf[6]`, `T_cf[7]`, `T_cf[8]`
  are post-processing arrays for the CoolSolve diagrams.

## How to run

Blocked: the native file does not parse in CoolSolve and no runnable variant
is shipped. The `copeland` compressor correlation reads its coefficients in
an **external lookup table `ZH38K4E-TFD` (columns `W`, `M`, `Vs`) that is not
part of the source collection** (no `.lkt` file anywhere in
`~/Nextcloud/thermo_models/`), so the ARI mode of the stored solution cannot
be reconstructed faithfully. The four embedded 11×2 coefficient tables of the
binary (columns `A`/`M`/`index`/`C`, four compressor variants) do **not**
reproduce the stored values (`copeland` at the stored operating point gives
5.84 / 3.98 / 2.70 / 4.73 kW on their `A` columns and 424.1 lbm/hr on the
closest `M` column, against the stored `W_dot_ari` = 3004.195839 W and
`M_dot_ari` = 417.48 lbm/hr), so none of them is the missing table.

The catalogue table is not reproduced by the library model `CSL-0123` either: the five
named catalogues recovered from `TM-0560` are a different vintage than the table of the
stored runs. Both stored runs read `Vs` = 82.61 cm³, while the recovered ZH38K4E-TFD has
`Vs` row 1 = 211.22 cm³ and gives 12 100 W at the stored operating point (stored: 3004.2
W, factor ≈ 4); its `M` column gives 4.28 lbm/hr there (stored: 417.48). A variant built on
the recovered table would therefore contradict the stored solution by construction, and a
variant on the semi-empirical Winandy branch would not reproduce the stored run either (it
is an `'ari'` run) and would additionally need the BrineProp2 library and the EES
incompressible `EG` properties (`CS-GAP-INCLUDE`, `CS-GAP-INCOMPRESSIBLE`), which have no
faithful substitute, so no runnable variant is shipped and the status stays `blocked`.


## Results (EES stored solution, reference — not reproduced by CoolSolve)

The stored run uses `compressortype$ = 'ari'`. Inputs that the original
takes from its parametric table (stored run values, the regression case of
the card):

| Input | Value | Input | Value |
|---|---:|---|---:|
| `t_ev` | −0.5567 °C | `t_cd` | 60 °C |
| `T_gw_su_ev` | 7.5812 °C | `T_w_ex_cd` | 55.8977 °C |
| `M_dot_gw_ev` | 0.56757 kg/s | `M_dot_w_cd` | 0.48553 kg/s |
| `gamma_leak_cp` | 0.9955924 (fixed by the table) | `I` | 87 W/m² |
| `t_amb` | 0 °C | `A_cd` / `A_ev` | 2.318 / 1.171 m² |

| Result | Value | Result | Value |
|---|---:|---|---:|
| `W_dot_cp` = `W_dot_ari` | 3004.20 W | `M_dot_r` = `M_dot_ari` | 0.052602 kg/s |
| `Q_dot_cd` | 9237.10 W | `COP` | 3.0747 |
| `t_ex_cp` | 85.49 °C | `epsilon_v_ari` | 0.9291 |
| `Vs` (read in the catalogue table) | 82.61 | `c_w` = `cp('EG',…,C=30)*1000` | 3804.94 J/kg-K |
| `c_gw_ev` (BrineProp2 specheat × 1000) | 3660.58 J/kg-K | `h_cyl` (from the swept-volume equations) | 2.2782 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the cycle
     (the state-point arrays p[i], T[i], h[i], s[i] are already in the file);
     blocked model - add after a runnable variant exists -->

## Verification

**Not verified: the model does not run in CoolSolve** (native file blocked;
no runnable variant, see *How to run*). The reference for a future re-check
is the **EES stored solution** shipped in the file (234 variables with
values, `reference/ees_variables.csv` of the extraction; key values in the
table above). The card's verification target "EES stored solution" therefore
reduces to documenting that reference; the numbers above were read from it
and cross-checked arithmetically where equations allow it
(`Q_dot_cd = COP*W_dot_cp` = 3.074734603 × 3004.195839 = 9237.10 W ✓;
`M_dot_ari` = 0.0526 kg/s = 417.48 lbm/hr ✓ used in the catalogue-table
check above).

## Source and attribution

Study model of the **ULiège Thermodynamics Laboratory**, author **Sylvain
Quoilin** (file-name tag `SQ1112288`, i.e. 2008-12-11; the `{$ID$}` tag names
the EES licence of J. Lebrun, Laboratoire de Thermodynamique, ULiège). The
scroll compressor model is from Winandy, Saavedra & Lebrun (2002) [1], the
plate-heat-exchanger correlations from Thonon et al., Hsieh & Lin (2002) and
Kuo et al.; the catalogue correlation is the ARI/Copeland polynomial of the
ZH38K4E-TFD data sheet.

Source file (EES 8.940, comments in English), collection of S. Quoilin:
`~/Nextcloud/thermo_models/Steady-state models/HeatPump_Vitocal 300G -110_CGSQ1112288.EES`
(inventory candidate `TM-0596`).

## Conversion log

- **2026-10-07 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already `SI MASS DEG PA C J` (no unit conversion); three
  stray NUL bytes removed (they sit at the end of procedure bodies in the
  original text — `CS-BUG-EXTRACT-NUL` documents the extractor-side NUL
  issue); the `{$ID$}` licence tag removed by the extractor; the file was
  last solved from the main program (234/234 stored values, no −9999).
  Comments kept (already English). **No runnable variant**: see *How to
  run*. The roadmap note of the card ("needs … the expander of
  TM-0597/CSL-0037") is not correct for this file revision: the file
  contains its own copy of the Winandy compressor model (no `Expander`
  procedure and no `MODULE`); its actual external needs are the BrineProp2
  library (sister of `CSL-0079`) and the `ZH38K4E-TFD` catalogue table
  (absent from the collection).
- **Inputs**: the commented-out equations `//t_ev=1.3`, `//T_w_ex_cd=55`,
  `//T_gw_su_ev=5`, `{M_dot_gw_ev=0.7056 …}`, `{M_dot_w_cd=0.4639}` and the
  `$ifnot parametrictable` block are kept as in the original — these inputs
  were provided by the EES parametric table (80 runs; the stored run values
  are in *Results*). `gamma_leak_cp` is a parametric-table column too (the
  isentropic exponent of the leakage model, fixed at 0.9955924 in the stored
  run; the alternative `{gamma_leak_cp=1,03}` is commented out in the
  original).
- **Level**: score of docs/taxonomy.md §3 — equations 392 → 2; largest block
  estimated > 30 (the compressor envelope/leakage loop couples ~55
  variables) → 2; procedures + arrays → 1; ≥ 3 coupled components → 1;
  semi-empirical (catalogue-identified compressor) → 1; curated guesses → 0;
  total 7 → level 4 by the table, **moved to level 3** (±1 allowed): the
  block size is an estimate (the native file does not parse, so CoolSolve
  analysis is unavailable) and the rating stays consistent with the triage
  (C-121) and with the level-2 rating of the similar RefSim model `CSL-0078`
  (149 equations, same compressor physics).
## Limitations and CoolSolve gaps

The native file is blocked by every ID of `model.json` `missing_features`:

- To rewrite (decision D12, not a CoolSolve gap): the adapted-pressure state is evaluated with the
  (s, v) pair: `h_in_cp = enthalpy(fluid$, s=s_in_cp, v=v_in_cp)`,
  `p_in_cp = PRESSURE(fluid$, s=s_in_cp, v=v_in_cp)`; the corrected branch
  uses the (v, u) pair similarly.
- `CS-BUG-LOOKUP-WRITE` — the `lookup('ev',…) = …` diagnostic writes inside
  `PROCEDURE hx_evv` are silently dropped (the table keeps its values); the writes feed
  no equation, so they do not block the model.

- `CS-GAP-CONVERT-UNQUOTED` — `convert(lbm/hr,kg/s)` in the ARI mass-flow
  equation: the unquoted unit names are read as variables (silent wrong
  system: 6 unknowns instead of 2, checked with a reproducer).
- `CS-GAP-LKT` — the compressor catalogue coefficients live in an external
  lookup table `ZH38K4E-TFD` (read by name through `comp$`), which is not
  embedded in the file and not present anywhere in the collection
  (see *How to run*).
- `CS-GAP-INCLUDE` — `CALL BRINEPROP2('EG',30,-5:…)` is an implicit
  USERLIB procedure (ULiège BrineProp2 library) not shipped with the file;
  its single-output sibling `BRINEPROP` is library model `CSL-0079`.
- `CS-GAP-INCOMPRESSIBLE` — the EES incompressible-substance library calls
  `cp/density/viscosity/conductivity('EG',T=…,C=30)` (Thonon `EG` branch,
  `hx_cd`, `hx_evv`, condenser `c_w`): CoolSolve reads `C` as a Fahrenheit
  hint and fails with *"cp requires exactly 2 input properties, got 1"*.
- `CS-GAP-GE-ARROW` — the `=>` spelling of the greater-or-equal relational
  operator (`If (Z => 0.001) and (W>0)` in `FUNCTION deltat_ln`): parse
  error *"Could not parse IF condition"*.
- `CS-GAP-REPEAT-UNTIL-BARE` — `until i>9` without parentheses
  (`FUNCTION copeland`): *"REPEAT missing UNTIL(condition)"*; the
  parenthesised `until (x>0.95)` of `PROCEDURE kuo` parses.

Physical limitations (as in the original): the condenser water side uses the
EG-30 % incompressible properties (`fluidcd$='EG'`) although the description
says water; the absorbed-solar section (`$bookmark absorber`, `Q_dot_abs`,
`S_abs`) is leftover dead code of another study, solved but unused; the
`A_cd`/`A_ev` areas are imposed inputs (design mode), the exchanger
procedures then compute the resulting pinch points.

## Related models

- `CSL-0007` *scroll_compressor_semi_empirical*: the same Winandy et al.
  semi-empirical scroll compressor (identified on another Copeland machine).
- `CSL-0037` *scroll_expander_semi_empirical*: the expander counterpart of
  the same adapted-pressure/isochoric-expansion physics (the roadmap note of
  this card expected its `Expander` procedure here; this file revision has
  its own compressor copy instead).
- `CSL-0078` *brine_to_water_heat_pump_refsim*: the ULiège model-bank
  brine-to-water heat pump with the same five-step compressor model
  (parameters identified, exchangers as thermal resistances instead of
  sized plate HXs).
- `CSL-0079` *brineprop_secondary_refrigerants*: the single-output
  `BRINEPROP` procedure of the same ULiège brine-property library family
  (the file calls the six-output `BRINEPROP2`).
- `CSL-0123` *copeland_catalogue_correlation*: the ARI/Copeland catalogue
  polynomial of the `'ari'` compressor mode, with the five catalogue tables
  recovered from `TM-0560` (see *How to run* for the vintage caveat).

- `CSL-0155` *inverter_air_water_heat_pump*: air-to-water counterpart of this complete heat-pump system model (Daikin Altherma type, heating branch imported).

[1] Winandy, E., C. Saavedra O., J. Lebrun (2002), *Experimental analysis and
simplified modelling of a hermetic scroll refrigeration compressor*, Applied
Thermal Engineering 22, 107–120 (cited in the file header).
