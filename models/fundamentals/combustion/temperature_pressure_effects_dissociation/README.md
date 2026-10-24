# Temperature and pressure effects on combustion-product dissociation

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0264`

Equilibrium dissociation of the products of octane (C8H18) combustion with
20 % excess dry air: the EES built-in `Chem_Equil` routine returns the mole
fractions of the 14 equilibrium product species (H2, O2, H2O, CO, CO2, OH, H,
O, N2, N, NO, NO2, CH4, Ar) at a given pressure and temperature, so the
exercise can show that dissociation grows with temperature and with
decreasing pressure. The two parametric sweeps of the original (one in
pressure, one in temperature) are kept as `$IF PARAMETRICTABLE` blocks.

| | |
|---|---|
| **Category** | Fundamentals › Combustion |
| **Fluids** | none (no property calls; the 14 equilibrium species appear as mole-fraction outputs only) |
| **Size** | 21 equations (largest block: 14 — the `CHEM_EQUIL` call) |
| **Source** | ULiège — course MCI, TP1 exercise 2 (EES file `Ex_2_T&P effects on dissociation.EES`) |
| **Authors** | P. Ngendakumana, R. Dickes (ULiège Thermotechnics; see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — native file blocked by `CS-GAP-CHEM-EQUIL`; no runnable variant |

## Problem statement

Study the influence of pressure and of temperature on the dissociation of the
combustion products of C8H18 burning with dry air at 20 % excess
(`C8H18 + 12.5*(O2+3.76*N2)*(1+0.20)`): compute the equilibrium composition
of the products at the operating point of the file (P = 10000 kPa, T = 2500 K)
and, in the original file, in two parametric sweeps (Table 1: pressure at
fixed T = 2500 K; Table 2: temperature at fixed P = 10000 kPa). The original
concludes (translated): *dissociation increases when temperature increases
and when pressure decreases*.

## Model

Element ratios of the reactant mixture (per oxygen atom), as in the original:

| Variable | Value | Meaning |
|---|---|---|
| `A\O` | 0 | inerts (argon) to oxygen atoms [-] |
| `C\O` | 8/30 | carbon to oxygen atoms [-] |
| `H\O` | 18/30 | hydrogen to oxygen atoms [-] |
| `N\O` | 3.76 | nitrogen to oxygen atoms [-] |

`CALL CHEM_EQUIL(P,T,A\O,C\O,H\O,N\O : x_H2 … x_Ar)` returns the 14
equilibrium mole fractions (EES built-in routine, valid EES); the closing
check `sumx = SUM(x_H2, …, x_Ar)` verifies that the mole fractions sum to 1.
Nothing else: no balance, no property call, no geometry — the whole physics is
inside the EES routine, which CoolSolve does not implement
(`CS-GAP-CHEM-EQUIL`).

## How to run

The native file `temperature_pressure_effects_dissociation.eescode` is valid
EES: open it in EES (the two sweeps are selected there by running the
parametric tables `Table 1`/`Table 2`; with no table running, the
`$IFNOT PARAMETRICTABLE` block gives the default point). In CoolSolve only the
default point is reachable (`PARAMETRICTABLE` has no value, so the two `$IF`
branches are dropped at parse time) and the file does **not** solve:
`Unknown procedure: CHEM_EQUIL` (see *Limitations and CoolSolve gaps*). No
`.sol` baseline exists and there is no runnable variant, so there is nothing to
run or to regression-test until `CS-GAP-CHEM-EQUIL` closes.

## Results (EES stored solution)

The file stores the solution of its last EES run, which is the **last row of
the temperature sweep** (Table 2: P fixed by its equation, T from the table),
not the default point of the equations window. 5 of the 10 stored variables
carry values:

| Quantity | EES stored value | in library units |
|---|---:|---:|
| `P` pressure | 10000 kPa | 1E7 Pa |
| `T` temperature | 3000 K | 2726.85 °C |
| `x_CH4` methane mole fraction | 0 | 0 |
| `x_Ar` argon mole fraction | 0 | 0 |
| `sumx` sum of the 14 mole fractions | 0.9999999992 | 0.9999999992 |

The five remaining stored names (`O2`, `H`, `O`, `N2`, `N`) carry no value and
do not occur in the equations window as shipped — leftovers of an earlier file
version in the stored solution (the call as shipped outputs the 14 `x_*`
variables). `x_Ar` = 0 agrees with `A\O` = 0 (no argon in the element ratios);
`sumx` ≈ 1 is the file's own consistency check.

## Verification

**Not verified** (status `blocked`, no runnable variant, no `.sol`): the EES
stored solution above could not be reproduced, because the only equation
system of the model is built around the `CHEM_EQUIL` call. What was checked
(2026-10-22, CoolSolve 0.4.0@9768373, run in the model folder):

- the unmodified extraction is **square** — *"Equations: 21, Variables: 21,
  System square: Yes, Total blocks: 8, Largest block: 14"* — so no equation
  was added or removed during the import (workflow §6, before calling a model
  over/under-determined);
- the run fails at exactly one place: *"warning (line 42): Unknown function
  'CHEM_EQUIL'"* and *"Block 6 (size 14, vars: x_OH, x_O2, x_O, …) failed:
  EvaluationError - [Newton] Unknown procedure: CHEM_EQUIL"* — the registered
  gap `CS-GAP-CHEM-EQUIL` (`compare_solution.py` is therefore not applicable:
  no `.sol` to compare with the reference).

Re-check plan (`T-RECHECK`): when a CoolSolve `CHEM_EQUIL` exists, solve at
the stored point (T = 2726.85 °C, P = 1E7 Pa — the last sweep row, not the
default 2226.85 °C) and compare with
`python3 tools/compare_solution.py temperature_pressure_effects_dissociation.sol reference/ees_variables.csv --ees-units`.

## Source and attribution

Exercise file of the ULiège course MCI, TP1 exercise 2, from the
`MCI_REMIDICKES` folder of the collection; the inventory attributes it to
**P. Ngendakumana** (the EES licence tag reads *"For use only by Philippe
Ngendakumana, ULG - Thermotechnics Unit, Liege, Belgium"* — a licence stamp,
which may differ from the author) and **R. Dickes** (the companion solution
files `Exo_…_resolution_RD.EES` of the same TP are initialled RD), as for
`CSL-0150` from the same series. To be confirmed by the maintainer.

Source file (EES 10.589, equations stored as plain text, comments in English),
collection of S. Quoilin:
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP1_Ex_1-5/Ex_2_T&P effects on dissociation.EES`
(inventory candidate `TM-0230`).

## Conversion log

- **2026-10-22 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `SI MASS DEG KPA C KJ`, plain-text equations (30 lines), no
  lookup or parametric tables decoded (the two parametric sweeps live in the
  `$IF` blocks and in the EES table objects, which the extractor did not
  report); converted by hand to SI-°C-Pa-J (ees_import.md §6):
  - `P = 10000 [kPa]` → `P = 1E7 [Pa]  "10000 kPa in the original"`;
  - `T = 2500 [K]` → `T = 2226.85 [°C]  "2500 K in the original"`
    (absolute temperature −273.15);
  - `.initials` converted likewise (stored guesses: P 10000 → 1E7, T 3000 →
    2726.85);
  - the `$UnitSystem` directive was deleted (workflow §9: CoolSolve has a
    single unit system; the model gets no `P010` warning);
  - comments translated/fixed (French conclusion → English, "oyxgen" →
    "oxygen", "equilibirum" → "equilibrium"); everything else is unchanged —
    the `$IF`/`$IFNOT` blocks with the swept variable commented out in braces
    (as in the original), the `A\O`-style variable names, the `CHEM_EQUIL`
    call signature and the variadic `SUM` check.
  - The call passes P and T as in the original; with the annotations now in
    Pa and °C, a future CoolSolve implementation of `CHEM_EQUIL` receives the
    library units (its data are in K, as in EES — cf. the note of `CSL-0150`).
- **Blocked in CoolSolve** (native file kept in valid EES): `CALL CHEM_EQUIL`
  → *"Unknown procedure: CHEM_EQUIL"* (`CS-GAP-CHEM-EQUIL`). No other gap: the
  `$IF` directives, the backslash names, the variadic `SUM` and the braces
  comments all parse (the run reaches the solver with a square system).
- **No runnable variant**: the equilibrium physics has no faithful substitute
  (same decision as `CSL-0150`, documented in the register row of
  `CS-GAP-CHEM-EQUIL`).
- **Category**: the card proposed `components/boilers_burners`; the equations
  contain no burner or boiler — they are a chemical-equilibrium exercise of
  the same TP series as `CSL-0150`, so the folder is `fundamentals/combustion`
  (taxonomy: *Fundamentals › Combustion — … chemical equilibrium and
  dissociation*).
- **Level**: equations 21 (score 0, < 50) + largest block 14 (1) + the file
  defines no function/procedure/array, the built-in `CHEM_EQUIL` call being a
  single statement (0) + no multi-zone (0) + no calibration (0) + no curated
  guesses (0) = 1 → level 1; consistent with the inventory guess (1).

## Limitations and CoolSolve gaps

- `CS-GAP-CHEM-EQUIL` (registered; this model is cited as evidence in the
  register row): the EES built-in `CHEM_EQUIL` procedure is unknown to
  CoolSolve — *"Unknown procedure: CHEM_EQUIL"* — and blocks the native file.
  No workaround keeps the equilibrium physics (a Gibbs minimisation would have
  to be re-implemented inside the model), so no variant is shipped.
- The two parametric sweeps (pressure at fixed T, temperature at fixed P) exist
  only as `$IF PARAMETRICTABLE` blocks in the file: the EES table objects were
  not extracted (0 tables reported) and CoolSolve has no parametric table
  attached to this file; the model as shipped evaluates the default point only.
- Physical scope: equilibrium composition only (no temperature rise, no
  energy balance) — the exercise stops at the composition, unlike `CSL-0150`,
  which closes the adiabatic flame balance on top of the same call.

## Related models

- `CSL-0150` *adiabatic_flame_dissociation*: same ULiège TP1 series, same
  `CHEM_EQUIL` call, but a full adiabatic flame-temperature balance for CH4 or
  fuel oil (also blocked by `CS-GAP-CHEM-EQUIL` and
  `CS-GAP-FLUIDS-NASA-SPECIES`). This model is the small pressure/temperature
  study that the register already cited as `TM-0230`.
