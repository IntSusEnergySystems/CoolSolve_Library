# Heat-transfer fluids: MEG, Therminol VP-1/66 and oil properties (function library)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0121`

EES `PROCEDURE prop_heat_transfer_fluid` (renamed `prop_htf` of the source file) computing
density, specific heat, thermal conductivity and dynamic viscosity of four
heat-transfer/secondary fluids against temperature, by the empirical correlations of the
source file. It is the companion of the BrineProp library `CSL-0079` for the
heat-transfer-fluid circuits (glycol loops, oil loops) of the heat-exchanger models of the
library, e.g. the plate condenser/evaporator models `CSL-0113`/`CSL-0114` whose copied
`prop_htf` block is an earlier transcription of the same source procedure.

| | |
|---|---|
| **Category** | Fundamentals › Properties |
| **Fluids** | monoethylene glycol (MEG), Therminol VP-1, Therminol 66, thermal oil, Water (built-in branch) |
| **Size** | 27 equations (largest block: 4) |
| **Source** | ULiège, J. Lebrun laboratory collection, `procedures EES/heat transfer fluids.EES` |
| **Authors** | Sylvain Quoilin; TBD (ULiège, J. Lebrun laboratory) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@7addbbc — verified against the EES stored solution (6/6 variables, max 1.9e-10) |

## Problem statement

The heat-transfer-fluid circuits of heat-pump and heat-recovery models need the transport
and thermodynamic properties of the secondary fluid at each iteration. The laboratory
procedure provides them for the four fluids used in the ULiège models, selected by the
string `fluid$`, with `T` in °C:

| `fluid$` | Fluid | Correlations |
|---|---|---|
| `'glycol'` | monoethylene glycol (MEG) | μ, ρ: polynomials in T and 1/T; cp, k: linear in T |
| `'TherminolVP-1'` | Therminol VP-1 | fits of the HEDH heat-transfer-fluid data sheet HTF-VP1 (cited in the file): ρ, cp, k cubic/quartic in T; ν from an exponential fit, μ = ν·ρ |
| `'therminol66'` | Therminol 66 | ρ, cp, k quadratic in T; ν exponential, μ = ν·ρ |
| `'oil'` | thermal oil | constant ρ = 800 kg/m³, cp = 2290 J/kg-K, k = 0.125 W/m-K, ν = 1.85 cSt, μ = ν·ρ |

Any other `fluid$` is routed to the built-in property functions `viscosity`, `density`,
`cp`, `conductivity` with the (T, P) input pair, so real fluids can be used directly.

## Model

The procedure has the signature

```
PROCEDURE prop_heat_transfer_fluid(fluid$, T, p : mu, rho, cp, k)
```

`p` [Pa] is only used by the built-in branch. All correlations are transcribed unchanged
from the source file (see the `.eescode` file for the coefficients). The demonstration
program calls the procedure for the four correlated fluids and for `Water` (built-in
branch).

**Validity ranges**: the source file gives none; the correlations are used in the ULiège
models at the circuit temperatures of the source models (roughly 0–200 °C for the
glycol/Therminol branches). Outside their fit range the polynomials extrapolate without
warning — as in the original.

## How to run

```
coolsolve ./heat_transfer_fluid_properties.eescode
```

No guesses needed (`.initials` holds only the two inputs of the default run). Other
models use the procedure by copying the definitions into a
`{--- Library functions copied from CSL-0121 ---}` block until `$INCLUDE library:…`
is supported (`CS-FEAT-IMPORT`).

## Results

Default run (`fluid$ = 'therminol66'`, T = 180 °C — the run stored in the source file),
with the demonstration calls of the other fluids:

| Variable | glycol 40 °C | TherminolVP-1 100 °C | therminol66 180 °C | oil 60 °C | Water 50 °C |
|---|---:|---:|---:|---:|---:|
| ρ [kg/m³] | 1120.94 | 997.90 | 899.65 | 800 | 988.03 |
| cp [J/kg-K] | 2521.87 | 1773.53 | 2121.41 | 2290 | 4181.35 |
| k [W/m-K] | 0.2741 | 0.1276 | 0.1075 | 0.125 | 0.6406 |
| μ [Pa·s] | 8.648e-3 | 9.415e-4 | 1.0319e-3 | 1.480e-2 | 5.465e-4 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g. a parametric sweep of rho/cp/k/mu vs T for one fluid  + one-line caption -->

## Verification

Reference: the EES stored solution of the source file (`therminol66`, T = 180 °C,
6 variables). `compare_solution.py`: **6 common variables, 0 differ (rtol=0.001); only in
EES: 0; only in CoolSolve: 21** (the demonstration calls of the other fluids). Maximum
relative difference **1.9e-10** (on cp — the stored EES value is rounded to 10 significant
digits; μ 3.3e-11, ρ, k, T and p exact) — the correlations are recomputed identically.

The card also asks for a check against the HEDH HTF-VP1 data sheet
(`http://twt.mpei.ac.ru/TTHB/HEDH/HTF-VP1.PDF`, cited in the source file). The sheet could
not be reached from the import environment (no network access to the host), so that check
is **pending**: the VP-1 coefficients above are transcribed unchanged from the source file,
and the EES stored solution of the `therminol66` branch verifies the transcription
procedure itself.

## Source and attribution

- Source: `~/Nextcloud/thermo_models/procedures EES/heat transfer fluids.EES` (EES X8.962,
  inventory TM-0574, already in the SI-°C-Pa-J unit system).
- The file carries only the *J. Lebrun laboratory* licence tag (`{$ID$ #1206: Jean Lebrun,
  Laboratoire de Thermodynamique, Univ. Liege}`); the S. Quoilin attribution follows the
  C-121 triage note (`sources/thermo_models/README.md` §8). The VP-1 branch cites the HEDH
  heat-transfer-fluid data sheet HTF-VP1 (MPEI server) as its source.

## Conversion log

- **2026-10-07 — import**: extracted with `tools/ees_extract.py` (6 variables, no table,
  no warning). Unit system already `SI MASS DEG PA C J`: no conversion. Licence tag and
  `$bookmark prop_htf` (EES GUI tag) removed; comments translated/annotated with units.
  **No equation changed.**
- **2026-10-07 — rename**: `prop_htf` → `prop_heat_transfer_fluid`: function names must be
  unique across the library and `prop_htf` is already used by the copied blocks of
  `CSL-0113`/`CSL-0114` (their block drops the `p` argument of the signature). The
  correlations of the copied blocks are the same equations as the `glycol`/`oil` branches
  here; `therminol66`/`TherminolVP-1` and the built-in fallback branch are new in the
  library with this model.
- **2026-10-07 — demonstration program**: the main program of the source file (one call,
  `therminol66` at 180 °C) is kept as the default run and completed with calls of the other
  three correlated fluids and of `Water` (built-in branch); they are CoolSolve-only
  additions, not part of the EES stored solution.
- **Level**: 27 equations (< 50) = 0; largest block 4 (≤ 5) = 0; procedures present = 1;
  no multi-zone/discretisation = 0; empirical property correlations = 1; no curated guesses
  = 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- The correlations return properties of the **pure fluids** as fitted by the laboratory;
  the `'glycol'` branch is monoethylene glycol, not an aqueous solution (aqueous brines:
  see `CSL-0079`).
- No validity range is enforced (as in the original); a `fluid$` typo silently falls to the
  built-in branch and fails there with "Unknown fluid".
- No CoolSolve gap blocks this model (`missing_features` empty).

## Related models

- `CSL-0079` *brineprop_secondary_refrigerants*: companion function library for aqueous
  secondary refrigerants (brines) — the two cover the secondary fluids of the library
  between them.
- `CSL-0113` *condenser_3_zones_plate_correlations*, `CSL-0114`
  *evaporator_3_zones_plate_correlations*: carry an earlier transcription of the same
  source procedure as a copied `prop_htf` block (glycol/oil branches, without the `p`
  argument and the built-in fallback).
