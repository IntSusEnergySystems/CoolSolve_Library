# Discretised (finite-volume) evaporator with three U-value zones

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0115`

Counterflow evaporator discretised in N cells (finite volumes, `PROCEDURE hxfem`):
the refrigerant is heated from subcooled liquid through the two-phase dome and
each cell exchanges `Q_dot = (T_hf - T)·A/N·U` with the secondary fluid, with
the overall heat-transfer coefficient U passing smoothly from `U_l` to `U_tp`
to `U_v` over a quality window of 0.1 — the smoothing that removes the random
non-convergence of the earlier sharp-switching revision (TM-0275, and its copy
TM-0598). The secondary-fluid (water) inlet temperature is imposed and its
outlet temperature is solved by iteration over the procedure.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | R245fa (refrigerant), Water (secondary fluid) |
| **Size** | 32 equations (largest block: 4), one `PROCEDURE` with a `REPEAT-UNTIL` cell loop |
| **Source** | ULiège collection, `procedures EES/hx - fem SQ011025.EES` (EES X8.423) |
| **Authors** | Sylvain Quoilin (ULiège Thermodynamics Laboratory) — file signed `SQ`, author named in the inventory |
| **License** | MIT |
| **CoolSolve** | native file runs (6 iterations); verified against the EES stored solution (max 2.2e-03) |

## Problem statement

The file documents its own validation: with `hf$='air_ha'`, `fluid$='r245Fa'`,
`T_hf_su = 170 °C`, `M_dot_hf = 1 kg/s`, `p = 6e5 Pa`, `t_su = 40 °C`,
`M_dot = 0.4127 kg/s`, `A = 5 m²`, `U_l = 300`, `U_tp = 400`, `U_v = 200 W/m²K`
(these U values are kept in a comment in the file), `N = 30`, the finite-volume
model gives `Q_dot = 89033 W` against `90153 W` for the moving-boundary model
*Evaporator 1, 2 & 3 zone SQ080603* (calculation times 0.3 s vs 0.2 s). The
author also notes *"random non-convergence problems with the discretized model
for certain working conditions and 10<N<20"*, which this smoothed revision
fixes. The shipped default run is the file's own last operating point: water
cooling from 170 °C, R245fa evaporating at 20 bar.

## Model

`PROCEDURE hxfem` marches cell i = 1…N from the refrigerant inlet
(`h = h_su`, water side at `T_hf_ex`, i.e. counterflow):

- `U = U_tp`, blended towards `U_l` for quality `x < width` and towards `U_v`
  for `x > 1 - width` (`width = 0.1`), with `max(x,0)`/`min(x,1)` so that the
  single-phase zones (quality ±100 in EES) sit on the end values;
- `Q_dot = (T_hf - T)·A/N·U`, then `h ← h + Q_dot/M_dot`,
  `T_hf ← T_hf + Q_dot/C_dot_hf`, with `C_dot_hf` evaluated at the mean water
  temperature;
- the procedure returns `h_ex` and `T_hf_su` = the water temperature reached at
  the refrigerant-inlet end. The main program imposes `T_hf_su = 170 °C`, so
  `T_hf_ex` is the unknown closed by the `CALL` (an iterative block, as in EES).

The original also writes the cell profile into the embedded lookup table
`tprofile` (write-only: the model never reads it). CoolSolve does not execute
lookup-cell writes: it reports each as a warning (`P009`) and does not store
the value; the cell results are in the solution of the solve itself.

## How to run

```bash
coolsolve ./hx_fem_evaporator_discretised.eescode
```

It solves in 6 iterations with the `.initials` shipped (also without: 45).
The companion table `hx_fem_evaporator_discretised-tprofile.csv` is the table
embedded in the source file (write-only in the model). The solve prints seven
`P009` warnings, one per `Lookup('tprofile',i,k) = …` line of the procedure
(see *Limitations*).

## Results (default run)

| Variable | EES | CoolSolve |
|---|---:|---:|
| `T_hf_ex` water outlet | 158.078 °C | 158.045 °C |
| `Q_dot` transferred power | 15 547 W | 15 581 W |
| `h_ex` refrigerant outlet enthalpy | 480 890 J/kg | 481 772 J/kg |
| `T_ex` / `DELTAT_ex` | 121.838 °C / 0 K | 121.770 °C / 0 K |

The refrigerant leaves inside the two-phase dome (`T_ex = t_sat` exactly,
`DELTAT_ex = 0`), so `Q_dot` is limited by the area, not by the water inlet.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. a sweep of N or of U_tp,
     figures/hx_fem_evaporator_discretised_*.png -->

## Verification

The model was solved and compared with the EES stored solution of the source
file (`compare_solution.py`, rtol=0.001):

```text
21 common variables, 3 differ (rtol=0.001); only in EES: 2; only in CoolSolve: 11
| h_ex | 480890 | 481772 | 1.83e-03 | DIFF |
| h_su | 325419 | 325959 | 1.66e-03 | DIFF |
| Q_dot | 15547.1 | 15581.3 | 2.20e-03 | DIFF |
```

Maximum deviation **2.20e-03**, on the R245fa absolute enthalpies `h_su`,
`h_ex` and on `Q_dot` (EES vs CoolProp property backend; within the ≤ 0.5 %
tolerance of CoolSolve `docs/ees_import.md` §11). All temperatures, `T_hf_ex`,
`t_sat`, `DELTAT_ex` and the U-value combinations agree. "Only in EES":
`DELTAt_ex_sp`, `h_ex_sp` — values stored by EES for lines that are commented
out in the source (alternative superheat mode, kept as comments). "Only in
CoolSolve": the 2-point diagram state arrays.

## Source and attribution

Source file (EES X8.423, comments in English), collection of S. Quoilin:
`~/Nextcloud/thermo_models/procedures EES/hx - fem SQ011025.EES`
(inventory candidate `TM-0575`, file name signed `SQ011025`). Earlier
revisions: `modeles/hx - fem SQ011025.EES` (TM-0275) and its copy
`Steady-state models/hx - fem SQ011025.EES` (TM-0598) — same equations with a
sharp switching between the three U values, superseded by this smoothed
revision. The header names the EES licence of the J. Lebrun laboratory
(ULiège); the author is identified from the `SQ` signature and the inventory
`authors` column.

## Conversion log

- **2026-10-07 — import** (`tools/ees_extract.py`): unit system already
  SI-°C-Pa-J, no conversion (D5 n/a); licence tag removed; the embedded table
  `Tprofile` renamed `tprofile` (file-name safety, references updated). The
  EES-syntax default `t_hf_su = T_hf` (lowercase) kept as in the original.
  Comments translated/kept as in the original. Two commented-out trial values
  of the original (`//T_hf_ex = 100`, `//T_hf_ex = 430.5 - 273.15`) dropped;
  the alternative superheat mode (`//DELTAt_ex_sp …`) and the validated-case U
  values (`{U_l = 300 …}`) kept as comments, as in the original.
- **Embedded tables checked.** The stored `tprofile` (110×3: T, T_hf, Q_dot;
  the procedure writes columns 2–5, the stored table holds 3 named columns)
  **matches the stored solution**: its row 1 (T = 90.9, T_hf = 158.0779,
  Q_dot = 5824.32 W = (158.0779 − 90.9) · 0.3 · 289, i.e. cell 1 at `U_l`,
  the subcooled inlet — EES quality = −100 → `max(x,0)/width` = 0) reproduces
  the stored run; rows 12–110 are blank (only N = 10 cells are written). The
  model never reads the table, so it ships as embedded data only, write-only.
  The parametric table `Table 1` (98×2, `Q_dot` vs `node`, values
  76 644 / 82 392 / inf…) belongs to an older or failed run (it does not
  match the stored solution) and was not used for verification.
- **State points.** A 2-point state array (`P[i]`, `h[i]`, `T[i]`, `s[i]`,
  i = 1 supply, 2 exhaust) is appended for the CoolSolve diagrams; the other
  results are unchanged. The rest of the file is the original EES code.
- **Level**: equations 32 (<50) → 0; largest block 4 (≤5) → 0; procedure +
  cell loop → 1; discretised structure → 1; physics (no calibration/off-design
  law, U values imposed) → 0; numerics (solves without curated guesses) → 0.
  Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The seven `Lookup('tprofile',i,k) = …` cell writes of the procedure (the EES
  way a subprogram writes into a lookup table) are not executed by CoolSolve:
  each is reported as warning `P009` and the `tprofile` table is not filled.
  They are diagnostic output only; no equation of the model reads the table.
- `CS-GAP-QUALITY-DOME` (not blocking the default run): CoolSolve `quality`
  returns 0 outside the dome instead of ±100. For the stored operating point
  the refrigerant leaves two-phase and every value agrees; at operating points
  where the vapour appears before the outlet, the model would pick the wrong
  branch U (U_l instead of U_v) after the transition, where EES uses U_v.
- The `U_lbis`/`U_tpbis`/`U_vbis` series-fraction equations of the original are
  kept (they document where the U values come from); they are not used by the
  procedure.

## Related models

- `CSL-0008` *condenser_three_zones*: three-zone (moving-boundary) condenser —
  the discrete-zone counterpart at the condenser side; the source file itself
  compares against a moving-boundary evaporator.
- `CSL-0113` *condenser_3_zones_plate_correlations*: three-zone plate
  condenser with zone-wise heat-transfer correlations.
- `CSL-0031` *refrigeration_evaporator_wet_coil*: evaporator with wet-air
  cooling, zone-wise effectiveness model.
- `CSL-0124` *plate_hx_pressure_drop_identification*: plate-HX
  pressure-drop correlations (Thonon, Kuo, Hsieh) of the same lab model
  set, on the R245fa+R134a REFPROP mixture (blocked; R245fa variant).
- `CSL-0114` *evaporator_3_zones_plate_correlations*: the same evaporator duty with three lumped correlation-based zones (Thonon/Hsieh) instead of the finite-volume discretisation.
- `CSL-0127` *hx_constant_effectiveness_discretised* (level 4): the other
  discretised heat exchanger of the library — single-phase counterflow
  segments with an imposed effectiveness closed by pinch complementarities
  (LaboThapPy `HexCstEffDisc`), instead of UA-based finite-volume cells.
