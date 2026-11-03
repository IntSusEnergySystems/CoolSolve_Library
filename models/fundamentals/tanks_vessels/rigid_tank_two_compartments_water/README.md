# Entropy change of water in a two-compartment rigid tank (exercise)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0172`

A rigid tank is divided into two hermetic compartments of equal volume. One
compartment holds 2.5 kg of compressed liquid water at 400 kPa and 60 °C; the
other is under vacuum. After the compartments are connected the pressure is
40 kPa. The model reads the initial and final states of Water and computes
the entropy change of the water. Teaching exercise 7 of repetition R4
(ULiège MECA0002, 2022-2023).

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | Water |
| **Size** | 19 equations (largest block: 1) |
| **Source** | thermo_models, file `R04_E7_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@b3c0d78 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A rigid tank is divided into two hermetic parts of equal volume. One part is
filled with 2.5 kg of compressed liquid water at 400 kPa and 60 °C, while the
second is under vacuum. The two parts are then connected and the pressure
falls to 40 kPa. Calculate the entropy change of this process.

## Model

The initial state is fixed by pressure and temperature. The final pressure is
given. All of the mass starts in one compartment, and the two compartment
volumes are equal, so the final specific volume is twice the initial specific
volume. Entropy is a real-fluid property of Water. The entropy change is the
mass times the change of specific entropy, as written in the source.

- \(v_1 = v(p_1, T_1)\)
- \(s_1 = s(p_1, T_1)\)
- \(v_2 = 2\,v_1\)
- \(s_2 = s(p_2, v_2)\)
- \(\Delta S = m\,(s_2 - s_1)\)

| Input | Value |
|---|---|
| `p1` | 400 kPa (400×10³ Pa) |
| `T1` | 60 °C |
| `m` | 2.5 kg (`2,5` in the source) |
| `p2` | 40 kPa (40×10³ Pa) |

`p1`, `T1`, `m` and `p2` are already equations in the EES equation window.
The system is square without any further assignment (11 equations, 11
variables). The stored values of the unknowns are guesses in `.initials`,
not equations.

The eight equations `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 before the
compartments are connected, i = 2 after) are post-processing for the
CoolSolve diagram. They do not change the eleven physical results.

## How to run

```bash
coolsolve ./rigid_tank_two_compartments_water.eescode
```

Every block is explicit. CoolSolve reports 0 iterations with the shipped
`.initials` and 0 iterations without them. The `.initials` file is the EES
stored solution converted to Pa and J.

## Results

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `p1` | 400000 Pa | 400000 Pa |
| `p2` | 40000 Pa | 40000 Pa |
| `T1` | 60 °C | 60 °C |
| `v1` | 0.00101696 m³/kg | 0.00101696 m³/kg |
| `v2` | 0.00203391 m³/kg | 0.00203391 m³/kg |
| `s1` | 831.091 J/kg·K | 831.091 J/kg·K |
| `s2` | 1027.75 J/kg·K | 1027.75 J/kg·K |
| `x1` | 0 | −100 |
| `x2` | 0.000252392 | 0.000252373 |
| `DELTAS` | 491.644 J/K | 491.640 J/K |
| `T[2]` | 75.8568 °C | not stored |

`T[2]` is the post-processing temperature at `p2` and `v2`. EES did not store
it. The final state is a trace of vapour (`x2` ≈ 2.52×10⁻⁴) at about the
saturation temperature of water at 40 kPa. `DELTAS`, `s1`, `s2` and `x2` are
printed at the digits of `compare_solution.py`.

CoolSolve prints a hint on `entropy(Water, P=p2, v=v2)`: `v=0.00203391` m³/kg
is unusually large and might be a density. `v2` is the specific volume. The
stored specific volumes match EES.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
`R04_E7_2022.EES` (EES X10.836, 11 stored variables). The tool converted
`p1` (kPa ×1000), `s1` (kJ ×1000), `p2` (kPa ×1000), `s2` (kJ ×1000) and
`DELTAS` (kJ ×1000):

> 11 common variables, 1 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8

The one difference, quoted as the tool prints it:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `x1` | −100 | 0 | 1.00e+00 |

Maximum relative difference over all common variables: **1.00e+00** (`x1`).

`x1` is the quality used in the source to check that the initial water is
liquid. EES returns −100 for a compressed liquid. CoolSolve returns 0
(`CS-GAP-QUALITY-DOME`). The original comment says the call checks the liquid
state. `x1` is not used in any other equation, so the entropy change is
unchanged. The gap does not block the file.

Water absolute entropy does not carry a reference-state offset here. `s1`
agrees to a relative difference of 6.54e-10 (CoolSolve − EES = 5.4×10⁻⁷
J/kg·K) and `s2` to 1.54e-06 (CoolSolve − EES = 0.00159 J/kg·K). EES stored
no enthalpy, so there is no enthalpy offset to report. The diagram enthalpies
`h[1]` = 251499.5 J/kg and `h[2]` = 318209.4 J/kg are CoolSolve-only.

The tool's other common variables stay under rtol = 0.001 (`--all`):

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `DELTAS` | 491.64 | 491.644 | 8.07e-06 |
| `s2` | 1027.75 | 1027.75 | 1.54e-06 |
| `s1` | 831.091 | 831.091 | 6.54e-10 |
| `x2` | 0.000252373 | 0.000252392 | 7.40e-05 |
| `v1` | 0.00101696 | 0.00101696 | 4.31e-10 |
| `v2` | 0.00203391 | 0.00203391 | 6.05e-11 |
| `m` | 2.5 | 2.5 | 0.00e+00 |
| `p1` | 400000 | 400000 | 0.00e+00 |
| `p2` | 40000 | 40000 | 0.00e+00 |
| `T1` | 60 | 60 | 0.00e+00 |

The eight names only in the CoolSolve solution are the diagram arrays
`P[1]`, `h[1]`, `T[1]`, `s[1]`, `P[2]`, `h[2]`, `T[2]`, `s[2]`.

## Source and attribution

S. Quoilin, ULiège course *Thermodynamique appliquée* (MECA0002), 2022-2023,
repetition R4, exercise 7. The EES file names no person. The licence tag is
the Laboratoire de Thermodynamique, University of Liège, not an author.
Source file:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R4/R04_E7_2022.EES`
(EES X10.836, inventory row TM-0427). The comments in the source are French.

## Conversion log

- **2026-10-15 — import**: extracted with `ees_extract.py` (EES X10.836, unit
  system `SI MASS DEG KPA C KJ`, 11 variables, no tables). Decimal comma
  `2,5` written as `2.5`; semicolons in the property calls written as commas.
  Pressures converted by hand from kPa to Pa: `p1` 400 kPa → `400e3` Pa,
  `p2` 40 kPa → `40e3` Pa. `T1` stays 60 °C. `m` stays 2.5 kg. Specific
  volumes `v1` and `v2` are already in m³/kg. `entropy` then returns J/kg·K
  and `DELTAS = m*(s2-s1)` is in J/K; the EES stored values of `s1`, `s2`
  and `DELTAS` were in kJ and are compared after ×1000 by
  `compare_solution.py --ees-units`. No `*1000` factor was removed from an
  equation: the source had none. The `$UnitSystem` directive was deleted.
  No Diagram-window input had to be restored: the four inputs above are
  already equations, and the system is square (11 equations, 11 variables).
  Comments translated to English (paraphrases of the original French
  statement and of the two equation comments). Variable names unchanged.
  Guesses in `.initials` are the stored solution in SI: `p1` = 400000 Pa,
  `p2` = 40000 Pa, `s1` = 831.0908744 J/kg·K, `s2` = 1027.747064 J/kg·K,
  `DELTAS` = 491.6404728 J/K. `v1`, `v2`, `T1`, `m`, `x1` and `x2` are
  unchanged from the EES stored numbers.
- **2026-10-15 — diagram states**: added `P[i]`, `h[i]`, `T[i]`, `s[i]` for
  i = 1, 2. `T[1]` is `T1`. `T[2]` is `temperature(Water, P=p2, v=v2)`.
  `h[1]` is `enthalpy(Water, P=p1, T=T1)` and `h[2]` is
  `enthalpy(Water, P=p2, v=v2)`. A solve of the equation window alone
  (11 equations) and a solve of this file give the same eleven original
  variables (relative difference 0).
- **Level**: equations 19 → 0; largest block 1 → 0; arrays present (the
  diagram states) → 1; no multi-zone or discretised component → 0; no
  semi-empirical, off-design or dynamic physics → 0; explicit, 0 iterations
  with or without guesses → 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

The final pressure is an assigned input, as in the source. EES
`quality` returns −100 for this compressed liquid; CoolSolve returns 0
(`CS-GAP-QUALITY-DOME`, not blocking: `x1` is a diagnostic output only).
The `.sol` file labels `v1` and `v2` as kg/m³ (`CS-BUG-UNIT-VOLUME`); the
values are specific volumes in m³/kg. No gap blocks the file.

## Related models

None linked. `CSL-0044` is a different exercise: one rigid tank holding a
liquid-vapour water mixture, with the phase masses and volumes as the
results. This file is the two-compartment entropy change.
