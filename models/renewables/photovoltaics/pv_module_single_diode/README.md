# PV module single-diode I-V curve

🟢 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** (verified variant) &nbsp;|&nbsp; `CSL-0160`

Five-parameter single-diode model of a flat-plate PV module: the module
parameters are read by name from an embedded `PVModules` lookup table and the
I-V (and P-V) curve is computed in 100 voltage points at a given cell
temperature and irradiance. The native file is blocked by CoolSolve lookup
gaps; the verified variant `pv_module_single_diode_coolsolve.eescode` runs it.

| | |
|---|---|
| **Category** | Renewables › Photovoltaics |
| **Fluids** | — (electrical/thermal model, no fluid) |
| **Size** | 337 equations, largest block 1 (the implicit I[j] diode equation, one per point) |
| **Source** | ULiège Thermodynamics Laboratory course file `modeles/photovoltaique/PV_model.EES` (EES X7.991), derived from the University of Wisconsin Solar Energy Laboratory PV module model |
| **Authors** | TBD (ULiège Thermodynamics Laboratory); original formulation: W. De Soto, S. A. Klein, W. A. Beckman (Solar Energy Laboratory, UW-Madison) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native blocked (`CS-GAP-END-PROCEDURE`, `CS-GAP-LOOKUPROW`, `CS-GAP-LOOKUP-PROC`, `CS-BUG-LOOKUP-STRING`, `CS-GAP-CONVERT-UNQUOTED`); variant verified against the EES stored solution |

## Problem statement

Given a module of the catalogue (`PVModules` table: NOCT, area, number of
cells, STC currents/voltages and the five single-diode parameters), compute
the I-V characteristic of the module in 100 points between 0 and `V_oc_ref`
for a cell temperature `T_c` and an irradiance `G`, and locate the maximum
power point. Default run (the values set in the diagram window of the
original): module `II-10`, `T_c` = 32 °C, `G` = 1000 W/m².

## Model

The equations are the standard five-parameter single-diode formulation (De
Soto et al. 2006, the model of the UW F-Chart PV package):

- light current `I_L = G/G_ref·(I_L_ref + alpha_sc·(TK_c − TK_c_ref))`;
- diode saturation current from the band gap `epsilon` = 1.12 eV, with the
  band-gap temperature dependence `e_g` and the Boltzmann constant
  `k` = 8.67343·10⁻⁵ eV/K;
- modified ideality factor `a = a_ref·TK_c/TK_c_ref`, series resistance
  `R_s = R_s_ref·(1 + delta·(TK_c − TK_c_ref))`, shunt resistance
  `R_sh = R_sh_ref·G_ref/G`;
- curve (implicit in `I[j]`, a Lambert-W type equation, solved per point):
  `I[j] = I_L − I_o·(exp((V[j] + I[j]·R_s)/a) − 1) − (V[j] + I[j]·R_s)/R_sh`
  with `V[j] = (j−1)·V_oc_ref/99`, `P[j] = V[j]·I[j]`.

The original reads the module row with `LOOKUP$ROW` on the string column
`PV Name` inside `PROCEDURE ReadPV` (16 named-column lookups).

## How to run

```bash
coolsolve ./pv_module_single_diode_coolsolve.eescode
```

The variant selects the module row by number (`Row`, 1…8; the mapping of the
8 module names is in the comment at `Row`). The native
`pv_module_single_diode.eescode` documents the original EES formulation and is
kept in valid EES syntax.

## Results

Default run (module II-10, T_c = 32 °C, G = 1000 W/m²):

| Quantity | Value |
|---|---:|
| `a` / `I_L` / `I_o` / `R_s` / `R_sh` at operating point | 0.9541 V / 2.5617 A / 7.210·10⁻¹⁰ A / 0.8794 Ω / 146.85 Ω |
| `I[1]` (current at V = 0) | 2.5464 A |
| Maximum power point | 37.19 W at 16.30 V, 2.282 A |

The STC maximum power of II-10 is `I_mp_ref·V_mp_ref` = 38.70 W; the −3.9 %
obtained at T_c = 32 °C is consistent with the catalogue power coefficient
`gamma_r` = −0.562 %/K applied to the 7 K above STC.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): I-V and P-V
     curves of module II-10 at the default point, figures/pv_module_single_diode_iv.png -->

## Verification

1. **Variant vs EES stored solution** (`compare_solution.py`): 333 common
   variables, 1 differ at `rtol=0.001` — `P[1]` only: EES −2.04506e-08 W,
   CoolSolve 0 W (V[1] = 0; absolute difference 2·10⁻⁸ W). Excluding it, the
   largest relative deviation on the 332 remaining variables is 1.37e-06
   (`I[97]`); all module parameters and model variables agree to better than
   1e-6 relative. The `only in EES` variables are stale array records left in
   the binary by earlier file versions (I/V/P[888…1001], `inf` values), not
   model variables; the 4 `only in CoolSolve` variables are the inputs the
   original took from its diagram window (`PVModule$`, `T_c`, `G`) and `Row`.
2. **I-V parametric table.** The original stores a 100-row × 3-column
   parametric table (`I[i]`, `P[i]`, `V[i]`) — the plotted curve of the last
   run. Its 300 cells were decoded by hand from the binary (the extractor
   mis-decoded it, see *Conversion log*) and match the EES stored solution
   exactly (300/300 within 1e-9 relative), so the CoolSolve curve was
   verified against both.
3. The extractor reported a "table1 (20×2)" parametric table: it is a
   mis-decode of the `Date`/`Time` columns of the `PVModules` table (entry
   timestamps of the 8 rows, 6/20/2007), not a reference table.

## Source and attribution

Course file of the ULiège Thermodynamics Laboratory
(`~/Nextcloud/thermo_models/modeles/photovoltaique/PV_model.EES`, EES X7.991,
comments in French, inventory candidate `TM-0316`; no author named in the
file, EES licence tag of the J. Lebrun laboratory). The identical copy
`TandS_Imput_IV_Model_Output_RsAdjust.EES` (TM-0317) carries the EES licence
stamp of the Solar Energy Laboratory, University of Wisconsin-Madison
(F-Chart group).

The model is the UW single-diode PV formulation: equations as published in
W. De Soto, S. A. Klein, W. A. Beckman, *Improvement and validation of a model
for photovoltaic array performance*, Solar Energy 80 (2006) 78–88 (the basis
of the F-Chart/SAM PV model, Duffie & Beckman, *Solar Engineering of Thermal
Processes*). The derivation is visible in the file itself: the diagram-window
module list still contains the F-Chart catalogue names
(`Siemens_Single-crystal_Si`, `USSC_a-Si/a-Si/a-Si_Ge`, `Sanyo_a-Si/x-Si_HIT`)
alongside the 8 ULiège course modules of the local `PVModules` table. The
import credits both the original formulation (UW Solar Energy Laboratory) and
the local course adaptation; the local catalogue data (II-xx modules) are
ULiège course data.

## Conversion log

- **2026-10-08 — import** (`tools/ees_extract.py`): unit system
  `SI MASS DEG KPA C J` — the only difference to CoolSolve is kPa vs Pa and
  the model contains no pressure quantity: no value converted (checked
  equation by equation). `ConvertTemp(C,K,·)` calls kept in the native file
  (quotes are optional in EES). French comments translated to English,
  standard header added, `$Bookmark` directives and the EES licence tag
  removed. The unused variables `S` and `M` (left over from an earlier file
  version, referenced by no equation) are not imported.
- **Diagram-window inputs.** `PVModule$`, `T_c` and `G` are set in the diagram
  window of the original and have no stored variable record; the default run
  was recovered from the stored solution (`TK_c` = 305.15 K → `T_c` = 32 °C;
  `R_sh` = `R_sh_ref` → `G` = 1000 W/m²; table row 2 `II-10` matches all 16
  stored module parameters) and added as equations: `PVModule$ = 'II-10'`,
  `T_c = 32`, `G = 1000`.
- **Tables.** The extractor found no embedded table and reported a false
  `table1 (20×2)`; the `PVModules` lookup table (8 rows × 22 columns,
  string-keyed `PV Name` column, with `BIPV`, `Date`, `Time`, `Adjust`,
  `Version` metadata columns that the model does not read) and the 100×3 I-V
  parametric table were decoded by hand from the binary: header (31 bytes),
  10-byte values per row, one `01` byte per row, then `04 03 00` and, for
  string columns, `uint32(len+1) + len` strings — the trailing per-row bytes
  are what the extractor's heuristic does not skip (cf.
  `CS-BUG-EXTRACT-LOOKUP-STRING`). The hand decoding was validated against the
  EES stored solution (all 8 rows × 16 parameters of module II-10 and the
  300 I-V cells match exactly). The native file ships the table as EES expects
  it (`pv_module_single_diode-pvmodules.csv`, all 22 columns, string key); the
  variant has its own numeric-key companion table
  (`pv_module_single_diode_coolsolve-pvmodules.csv`: `Row` + the 16 parameter
  columns, same values).
- **Variant changes** (each forced by a registered gap, valid EES throughout):
  1. `END ReadPV` → no PROCEDURE: `PROCEDURE ReadPV` is flattened into the
     main program (`CS-GAP-LOOKUP-PROC`; CoolSolve also rejects the named
     terminator, `CS-GAP-END-PROCEDURE` — *"Procedure 'ReadPV' missing END"*).
  2. `Row = LOOKUP$ROW('PVModules','PV Name',PVModule$)` → `Row = 2` with the
     name→row mapping in a comment (`CS-GAP-LOOKUPROW`).
  3. The 16 named-column lookups → positional numeric lookups
     `Lookup('pvmodules', Row, <col nr>)` on the numeric-key companion table
     (`CS-BUG-LOOKUP-STRING` string columns; column-name strings avoided per
     `CS-BUG-LOOKUP-COLNAME`). Table name lowercase `pvmodules` = companion
     file name convention; EES table names are case-insensitive.
  4. `ConvertTemp(C,K,·)` → `ConvertTemp('C','K',·)` (`CS-GAP-CONVERT-UNQUOTED`:
     unquoted unit names become variables, system not square).
  Variable names, equations and values are otherwise unchanged.
- **Level**: score 4 of taxonomy §3 (equations band 2 for 337 equations,
  structures 1, semi-empirical parameters 1) → moved to level 2: the 300
  DUPLICATE equations are an output curve sweep (largest block 1, each point
  independent), the model itself is a 37-equation explicit parameter update
  plus one scalar implicit diode equation per point, with default guesses.

## Limitations and CoolSolve gaps

- Native file blocked (all registered; the file stays in valid EES):
  `CS-GAP-END-PROCEDURE` (parse fails first), `CS-GAP-CONVERT-UNQUOTED`
  (not square: `C`/`K` taken as variables), then `CS-GAP-LOOKUPROW`,
  `CS-GAP-LOOKUP-PROC` and `CS-BUG-LOOKUP-STRING` on the table read.
- The `II-06` entry of the original diagram-window module list has no row in
  the local `PVModules` table (8 rows); selecting it in EES would fail — the
  default run uses `II-10`.
- Curve points beyond the maximum power point return negative currents
  (as in the original: the last point is `V_oc_ref`, where the single-diode
  equation with shunt gives `I[100]` ≈ −0.47 A); the table stores them too.

## Related models

- (first model of `renewables/photovoltaics`; no other PV model in the
  library yet.)
