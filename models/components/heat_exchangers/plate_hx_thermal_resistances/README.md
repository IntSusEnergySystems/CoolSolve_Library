# Single-phase plate heat exchanger: thermal-resistance model (Martin)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0161`

Heat-transfer coefficient, thermal resistance and pressure drop of a
chevron-type plate heat exchanger on the single-phase side, computed from the
plate geometry (corrugation amplitude and wavelength, plate length and width,
chevron angle, number of plates) with **Martin's 1996 correlation**: area
enlargement factor φ, hydraulic diameter, laminar or turbulent friction
factors, Nusselt number and pressure drop. The fluid properties are either
those of water (EES built-in calls) or, on the alternate branch selected with
`$IF fluid$`, those of an ethylene-glycol brine from the `BRINEPROP2` procedure
of the ULiège BrineProp library. A small building block of the ULiège
plate-HX modelling work of 2008.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | Water; ethylene-glycol brine (BrineProp2, not a CoolProp fluid) |
| **Size** | 37 equations (largest block: 4), one `PROCEDURE` |
| **Source** | ULiège Thermodynamics Laboratory — `~/Nextcloud/thermo_models/modeles/plate_heat_exchanger_SB080104.EES` (inventory `TM-0319`) |
| **Authors** | Stéphane Bertagnolio; Sylvain Quoilin (2008) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7addbbc — **blocked**: the native file does not parse/solve (`CS-GAP-IF-DIRECTIVE`, `CS-BUG-HASH-IDENT`, `CS-GAP-CALL-EXPR-OUT`); the runnable variant `plate_hx_thermal_resistances_coolsolve.eescode` (stored water run) is **verified** against the EES stored solution |

## Problem statement

Size a chevron plate heat exchanger thermally from its geometry: for a given
volume flow and mean fluid state, Martin's theoretical approach to
chevron-type plate exchangers gives the friction factor and the Nusselt
number of the corrugated channel, from which the model computes the
heat-transfer coefficient `h_f`, the thermal resistance `R_f = 1/(h_f·A_hex)`
and the pressure drop `DELTAP`. This 2008 building block (S. Bertagnolio,
S. Quoilin) is an earlier, self-contained companion of the RefSim plate-HEX
model (inventory `TM-0305`-family, `…/Single_Phase_plate_HEX` RefSim version)
and of the correlation libraries `CSL-0096`/`CSL-0111`.

## Model

Geometry and correlations (as in the original, Martin 1996; Garcia-Cascales
et al. 2007 as secondary reference):

| Step | Equation |
|---|---|
| corrugation parameter | `X = 2·π·A_bar/Λ` |
| area enlargement factor | `PHI = (1 + √(1+X²) + 4·√(1+X²/2))/6` |
| hydraulic diameter | `d_h = 4·A_bar/PHI` |
| mean flow cross-section | `A_cs = round(L_w/Λ)·L_w·2·A_bar` |
| Reynolds number | `Re_f = rho_f·u_f·d_h/mu_f` with `u_f = V_dot_f/A_cs` (PROCEDURE `REYNOLDS`) |
| friction factors `f_0`, `f_1` | laminar (`Re_f < 2000`): `64/Re_f`, `597/Re_f + 3.85`; turbulent: `(1.8·log10(Re_f) − 1.5)⁻²`, `39/Re_f^0.289` |
| friction factor | `1/√f = cosβ/√(0.18·tanβ + 0.36·sinβ + f_0/cosβ) + (1−cosβ)/√(3.8·f_1)` (implicit) |
| Nusselt number | `Nu_f = Pr_f^(1/3)·(mu_f/mu_w)^(1/6)·0.122·(f·Re_f²·sin2β)^0.374` |
| heat-transfer coefficient | `h_f = Nu_f·k_f/d_h` |
| thermal resistance | `R_f = 1/(h_f·A_hex)` with `A_hex = L_w·(L_p − D_p)·PHI·N_p` |
| pressure drop | `DELTAP = f·rho_f·u_f²·L_p/(2·d_h)` |

Fluid properties: water branch `rho_f, mu_f, mu_w, k_f, Pr_f, c_p_f` from the
EES built-in property functions; ethylene-glycol branch through two calls of
`BRINEPROP2` (density, specific heat, conductivity, viscosity, Prandtl number
and freezing point of the EG solution at `X_EG` %), the second-generation
procedure of the BrineProp library (shipped with the `Brineprop2.LIB` of the
same ULiège folder, inventory `TM-0480`, merged into `CSL-0079`). Only the
`R_f` thermal resistance is computed in this version: no wall/plate
resistance in series (the plate conductivity `k_w` and thickness `t` are
inputs but unused by the equations; as in the original — note that in its EG
branch the original reuses `k_w` as the brine-conductivity output of the
second `BRINEPROP2` call, overwriting the plate conductivity).

Inputs: geometry (`A_bar`, `LAMBDA`, `L_p`, `L_w`, `beta`, `t`, `N_p`, `D_p`,
`k_w`), `T_m`, `T_w`, `P_m`, `V_dot_f_m3h`, `fluid$`, `X_EG`. Outputs:
`Re_f`, `f`, `Nu_f`, `h_f`, `A_hex`, `R_f`, `DELTAP` and the regime string
`Regime$`.

## How to run

The native file `plate_hx_thermal_resistances.eescode` is valid EES and does
not solve in CoolSolve:

```
Parse failed:
  Line 71: Could not parse line        (Nu#_f = …, CS-BUG-HASH-IDENT)
  Line 73: Could not parse line        (Nu#_f = …, CS-BUG-HASH-IDENT)
warning (line 51): Unknown function 'BRINEPROP2'
```

(the warning on line 51 shows that the `$IF fluid$='EG'` branch is kept
although `fluid$ = 'Water'`: `CS-GAP-IF-DIRECTIVE`). The faithful runnable
transcription of the stored run is

```bash
coolsolve ./plate_hx_thermal_resistances_coolsolve.eescode
```

It solves in 14 iterations without special guesses (no `.initials` needed);
its baseline is `plate_hx_thermal_resistances_coolsolve.sol`
(regression-tested as `CSL-0161:coolsolve`). The variant changes only what
the gaps force (see *Conversion log*); it stays valid EES, with no
CoolSolve-only syntax. No lookup tables.

## Results

Stored operating point (water, 25 °C, 1 bar, 150 m³/h, 105 plates,
β = 45°), values of the variant:

| Quantity | EES (stored) | CoolSolve |
|---|---:|---:|
| `Re_f` [-] | 4852.07 | 4854.66 |
| regime | — | TURBULENT (`Regime$`) |
| `f` [-] | 0.83549 | 0.83547 |
| `PHI` [-] | 1.22094 | 1.22094 |
| `A_hex` [m²] | 109.03 | 109.03 |
| `k_f` [W/m-K] | 0.59477 | 0.60652 |
| `Pr_f` [-] | 6.2631 | 6.1358 |
| `Nu_f` [-] | (not stored) | 119.41 |
| `h_f` [W/m²-K] | 5454.51 | 5526.47 |
| `R_f` [K/W] | 1.6815e-06 | 1.6596e-06 |
| `DELTAP` [Pa] | 5387.35 | 5387.12 |

<!-- FIGURE (maintainer, docs/model_workflow.md §7): e.g. parametric sweep of
     h_f and DELTAP versus volume flow (0–300 m³/h) or chevron angle. -->

## Verification

Status **blocked** (the native file does not parse); the **runnable variant**
`plate_hx_thermal_resistances_coolsolve.eescode` is compared with the **EES
stored solution** of the source file (38 variables, last run = water):
`34 common variables, 4 differ (rtol=0.001); only in EES: 4; only in
CoolSolve: 4`. Maximum relative deviation **2.03e-02** (`Pr_f`).

- The four flagged variables (`k_f`, `Pr_f`, `h_f`, `R_f`; `h_f` and `R_f`
  inherit the conductivity deviation) come from the **water property
  backend**: EES 7.888 (2008) returns `k_f` = 0.59477 W/m-K at 25 °C where
  CoolProp (IAPWS, as in CoolSolve) returns 0.60652 W/m-K — the IAPWS value
  at 25 °C is 0.607 W/m-K, so the old EES library is the outlier, by 2 %.
  All other properties agree (`rho_f` 1.4e-05, `c_p_f` 5.6e-05, `mu_f`
  5.5e-04 relative) and the purely geometric/algebraic outputs match to
  ≤ 4.2e-05 (`DELTAP`). Within the "older EES fluid models: up to a few %"
  tolerance of the import procedure, with the explanation above.
- Only in EES: `a`, `c`, `u` — stored by EES but defined by no equation of
  the current text (leftovers of earlier edits of the file, values 1, 1 and
  0.8818 m/s); `T_freezing` = −10.959 °C — a stale value of an earlier run
  with the EG branch (it is the freezing point of EG 25 % per BrineProp);
  the stored water run does not compute it and neither does the variant.
- Only in CoolSolve: `fluid$` (string variables are not exported by EES to
  the reference), `PI`, `Regime$`, and `Nu_f` — the `Nu#_f` of the original,
  renamed in the variant (`CS-BUG-HASH-IDENT`); EES does not store `Nu#_f`
  either (the value follows from the stored `h_f`, `d_h`, `k_f`:
  120.18 with the EES `k_f`).

## Source and attribution

ULiège Thermodynamics Laboratory, collection of S. Quoilin:
`~/Nextcloud/thermo_models/modeles/plate_heat_exchanger_SB080104.EES`
(EES X7.888, inventory `TM-0319`, header "Author: S.Bertagnolio, S.Quoilin",
licence stamp of the J. Lebrun laboratory removed by the extractor). The
scientific references are those of the original header: H. Martin (1996),
*A theoretical approach to predict the performance of chevron-type plate
heat exchangers*, Chemical Engineering and Processing 35, 301–310; and
J.R. Garcia-Cascales, F. Vera-Garcia, J.M. Corberan-Salvador,
J. Gonzalvez-Macia (2007), *Assessment of boiling and condensation heat
transfer correlations in the modelling of plate heat exchangers*,
International Journal of Refrigeration. The `BRINEPROP2` procedure called on
the EG branch is `Brineprop2.LIB` of the same laboratory
(`~/Nextcloud/thermo_models/Model data bank/AHU_Components/Recovery_Systems/GLYCOLRECOVERYLOOP_REFSIM_EES_MODEL_SB080116.zip!/UserLib/BrineProp/Brineprop2.LIB`,
inventory `TM-0480`). The copy `Steady-state models/plate_heat_exchanger_SB080104.EES`
(inventory `TM-0601`) has identical equations (duplicate group DG-0125).

## Conversion log

- **2026-10-08 — import** (`T-IMPORT`, roadmap card C-153): extracted with
  `tools/ees_extract.py`. Unit system already `SI MASS DEG PA C J` → **no
  unit conversion**. Comments already in English; standard header added; the
  literature citations of the original header kept verbatim (including its
  "theoritical" typo, part of the cited title). The `{$ID$}` licence tag was
  removed by the extractor.
- **2026-10-08 — data block restored** (allowed edit, both files): the whole
  data block of the original is commented out in the stored text while EES
  stores values for every one of those variables (the file was solved before
  the block was commented out). The values were restored from the stored
  solution (this is the "inputs only in the stored solution" case of the
  import procedure): `A_bar = 0.004`, `LAMBDA = 0.025`, `L_p = 1.55`,
  `L_w = 0.63`, `beta = 45`, `t = 0.0006`, `N_p = 105`, `D_p = 0.2`,
  `k_w = 17`, `T_m = 25`, `P_m = 1E5`, `V_dot_f_m3h = 150`, and
  `fluid$ = 'Water'` (the stored run). `X_EG = 25` (stored value; the
  original comment says 50 %). One input had no line even in the commented
  block: `T_w = 25` was restored from the stored solution (confirmed by
  `mu_w` = `mu_f` = viscosity of water at 25 °C). With the data block active
  the model is square (37/37); the original equations are otherwise
  unchanged.
- **2026-10-08 — runnable variant** `plate_hx_thermal_resistances_coolsolve.eescode`
  (valid EES, no CoolSolve-only syntax). Changes forced by the gaps, logged
  in the variant header:
  1. `CS-GAP-IF-DIRECTIVE`: the `$IF fluid$` branches are resolved for the
     stored run — the water property block is kept unconditional and the
     ethylene-glycol `BRINEPROP2` branch is removed (kept as a comment). The
     brine route is available in the library through `CSL-0079`
     (BrineProp) and `CSL-0111` (plate correlations);
  2. `CS-BUG-HASH-IDENT`: the Nusselt variable `Nu#_f` is renamed `Nu_f`
     (same workaround as `CSL-0111`; valid EES, no equation change).
- **Level 2** although the raw score is 1 (37 equations → 0, largest block
  4 → 0, one procedure → 1, no multi-zone, no calibration, no curated
  guesses): moved +1 to the inventory guess — a complete component model
  built on an empirical correlation with a regime-dependent implicit
  friction factor is the typical level-2 content; the equation-count
  criterion penalises this compact correlation model.

## Limitations and CoolSolve gaps

The native file is **blocked**; `missing_features` lists every gap that
blocks it:

- `CS-GAP-IF-DIRECTIVE` — the compile-time directives `$IF fluid$='Water'` /
  `$IF fluid$='EG'` / `$ENDIF` are parsed and ignored: both branches are
  kept, so the EG branch (its `BRINEPROP2` calls, its `rho_f` redefinition)
  is solved together with the water branch;
- `CS-BUG-HASH-IDENT` — the Nusselt variable is named `Nu#_f`: an identifier
  containing `#` is a parse error in the main program (lines 71 and 73);
- `CS-GAP-CALL-EXPR-OUT` — the EG branch calls `BRINEPROP2` with an
  expression output (`… : c_p_f/1000`), not recognised by CoolSolve.

Worked around, not blocking: `CS-GAP-INCLUDE` (the `BRINEPROP2` procedure is
implicit in EES — `USERLIB`; the variant removes the EG branch instead of
copying the procedure, which has no runnable CoolSolve form in the library
yet, see `CSL-0079`). Physics: single-phase side only, one fluid at a mean
state (no temperature profile, no LMTD); the correlations are valid for
chevron plates inside the tested geometry (10 ≤ β ≤ 80° per Martin).

## Related models

- `CSL-0079` *brineprop_secondary_refrigerants* — the BrineProp function
  library whose second-generation procedure `BRINEPROP2` (candidate
  `TM-0480`, merged there) computes the brine properties of the EG branch.
- `CSL-0111` *plate_hx_correlations* — ULiège procedure library for plate
  heat exchangers; its `martin` procedure (and the same `Nu#_f` workaround)
  implements the same Martin correlation with more plate-HX correlations
  around it.
- `CSL-0162` *glycol_runaround_recovery_loop*: imported in the same wave with
  the same pattern (native file blocked by `$IF`/`CALL` gaps, runnable
  variant resolved for the stored run).
