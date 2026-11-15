# Emptying an adiabatic tank filled with an ideal gas

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0356`

Example 4.5-2 of Klein & Nellis: a rigid, well-insulated tank of ideal gas (air
with constant heat capacities) is blown down from 100 psi (689 475.7 Pa) to the
ambient pressure of 14.7 psi (101 352.9279 Pa). As in the original, the gas
remaining in the tank is treated with an isentropic-type relation on absolute
temperatures; the tank cools from 20 °C to about −104 °C.

| | |
|---|---|
| **Category** | Fundamentals › Tanks and vessels |
| **Fluids** | Air (ideal gas, molar mass only) |
| **Size** | 9 equations, all explicit (largest block: 1) |
| **Source** | Klein & Nellis, *Thermodynamics*, Cambridge University Press, 2011, example 4.5-2 (F-Chart Software EES example, EES-Community/ees-examples) |
| **Authors** | S. A. Klein and G. F. Nellis (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@00a4daa — verified (see verification field) |

## Problem statement

Example 4.5-2 of Klein & Nellis (2011): an adiabatic rigid tank is filled with
an ideal gas at 100 psi and 20 °C. A valve is opened and the tank is emptied
until the pressure falls to 14.7 psi. Find the final temperature of the gas
remaining in the tank.

## Model

The textbook treatment of the blowdown of a rigid adiabatic tank: the gas left
in the tank undergoes an isentropic-type expansion, so the final temperature
follows from the pressure ratio on **absolute** temperatures:

- `R = R#/MolarMass(Air)` — ideal gas constant of air [J/kg-K]
- `c_P = c_v + R` — constant-pressure specific heat [J/kg-K]
- `T_1_K = T_1 + 273.15`, `T_2_K = T_1_K*(P_2/P_1)^(R/c_P)`, `T_2 = T_2_K − 273.15`

Inputs: `T_1` = 20 °C, `P_1` = 689 475.7 Pa (100 psi in the original), `c_v` =
717.6 J/kg-K, `P_2` = 101 352.9279 Pa (14.7 psi in the original). Output:
`T_2` (and the intermediate `R`, `c_P`, `T_1_K`, `T_2_K`).

## How to run

```bash
coolsolve ./ideal_gas_tank_blowdown.eescode
```

No guess file needed (every equation is explicit; the solver needs 0
iterations); no `coolsolve.conf`.

## Results

| Variable | Value | Unit |
|---|---:|---|
| `R` | 287.047 | J/kg-K |
| `c_P` | 1004.65 | J/kg-K |
| `T_2_K` | 169.503 | K |
| `T_2` | −103.647 | °C |

The gas remaining in the tank cools by about 124 K while its pressure falls by
a factor 6.8 (100 psi → 14.7 psi): `P_2/P_1` = 0.147 exactly (both pressures
use the same 1 psi = 6894.757 Pa conversion), and
0.147^(287.047/1004.647) = 0.5782, applied to `T_1_K` = 293.15 K, gives
169.503 K. The temperature drop is physically consistent with the pressure
drop of an adiabatic blowdown.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. a parametric sweep of
     T_2 vs final pressure P_2 + one-line caption -->

## Verification

Compared with the solution stored by EES in the binary `.eez` companion of the
source file (8 variables, `compare_solution.py --ees-units`; the EES file
stores temperatures in K and `P_2_psi` in psi). Summary quoted from the tool:

> Converted EES reference values: T_1 (K->C), T_2 (K->C)
>
> 7 common variables, 0 differ (rtol=0.001); only in EES: 1; only in CoolSolve: 3
> Only in EES reference: P_2_psi

With `--all`, the largest printed relative deviation is 1.51e-05 on `R`
(molar mass of Air: EES 287.0431586 vs CoolProp-based 287.0474910 J/kg-K);
`T_2` agrees to 9.66e-06 (`ees-stored-solution`). The stored solution is not a
stale run: `P_2_psi` = 14.7 psi matches the stored `P_2`, and the shipped point
was recomputed by hand, `293.15*0.147^(287.043/1004.643)` = 169.50351 K
(`analytical`), which the stored `T_2` = 169.5035099 K confirms. The 3
"only in CoolSolve" variables are `T_1_K`, `T_2_K` (introduced by the °C
storage of temperatures) and the built-in constant `R#`. Checks:
`ees-stored-solution`, `analytical`.

## Source and attribution

- S. A. Klein and G. F. Nellis, *Thermodynamics*, Cambridge University Press,
  2011, example 4.5-2 "Emptying an Adiabatic Tank filled with Ideal Gas"; EES
  example © F-Chart Software, MIT, distributed in the
  EES-Community/ees-examples collection (`uncategorized/example_4.5-2.ees`)
  with the binary `.eez` companion (EES 11.912) whose stored solution is the
  verification reference.
- The file header points to the original download page
  `https://fchartsoftware.com/ees/examples/examples_thermodynamics_2011/chapter%204/example%204.5-2.eez`.
- Library source inventory: `sources/ees_examples/inventory.csv`, row `EEX-020`.

## Conversion log

- **2026-11-15 — import**: extraction of the `.eez` companion (zip → inner
  `.EES`, EES 11.912, unit system `SI MASS RAD PA K J`) with
  `tools/ees_extract.py`; 8 stored variables taken as the verification
  reference.
- **2026-11-15 — unit conversion** (by hand, ees_import.md §6, K → °C and psi
  → Pa; 1 psi = 6894.757 Pa, no `Convert` call): `T_1` = 20 °C (original
  `ConvertTemp(C,K,20 [C])` removed), `P_1` = 689 475.7 Pa (100 psi),
  `P_2` = 101 352.9279 Pa (14.7 psi; `P_2_psi` dropped, single final pressure
  kept as in the original default run), `T_1_K = T_1 + 273.15` and
  `T_2 = T_2_K − 273.15` added around the original relation
  `T_2_K = T_1_K*(P_2/P_1)^(R/c_P)`, which now uses absolute temperatures
  explicitly. `R = R#/MolarMass(Air)` and `c_P = c_v + R` unchanged. No
  `$UnitSystem` directive in the CoolSolve file.
- **2026-11-15 — directives dropped** (card decision): `$ifnot ParametricTable`
  / `$elseif` / `$ShowWindow` (the file had no parametric table; the default
  run with `P_2_psi` = 14.7 psi is the shipped state) and `$TABSTOPS`
  (display-only).
- **Level**: 9 equations → 0; largest algebraic block ≤ 5 → 0; no
  functions/arrays → 0; not multi-zone → 0; no dynamics → 0; no curated
  guesses → 0. Score 0 → level 1.

## Limitations and CoolSolve gaps

None blocking: the file runs in CoolSolve as transcribed (every change is
logged above); `missing_features` is empty. Physical limitation, as in the
original: constant heat capacities (air), and the blowdown is represented by
the single final state through the isentropic-type relation — no tank size, no
mass and no time are modelled.

## Related models

None listed (`related` is empty). Nearest neighbour in the library: `CSL-0351`
(butane_tank_blowdown), the unsteady uniform-state blowdown of a two-phase
real-fluid tank — same system, other level of detail (integrated balances on
n-butane instead of the ideal-gas closed-form relation).
