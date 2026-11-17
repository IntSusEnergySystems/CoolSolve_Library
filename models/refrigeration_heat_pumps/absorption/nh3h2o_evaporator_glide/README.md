# Evaporator temperature glide of ammonia-water (Herold et al., Example 9.1)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0362`

Three equilibrium states of an ammonia-water absorption system, as in
Example 9.1 of Herold, Radermacher and Klein, *Absorption Chillers and Heat
Pumps* (CRC Press, 2015): the desorber vapour in equilibrium with the entering
rich solution, the evaporator fed with saturated liquid of that composition at
0 °C, and the saturated two-phase evaporator outlet at constant pressure. The
model outputs the vapour mass fractions, the saturation pressures, the
evaporator outlet temperature, the temperature glide, the outlet vapour
quality and the minimum liquid mass fraction `x_e2_min`. It is the
property-level exercise behind the temperature glide of the NH3/H2O cycle
models.

| | |
|---|---|
| **Category** | Refrigeration and heat pumps › Absorption chillers |
| **Fluids** | NH3H2O (ammonia mass fraction `x`, quality `Q`) |
| **Size** | 16 equations, all explicit (largest block: 1) |
| **Source** | EES example `ex9_1.ees` (F-Chart Software) — textbook Example 9.1 of Herold et al. (2015) |
| **Authors** | S. A. Klein (F-Chart Software); book example by K. E. Herold, R. Radermacher and S. A. Klein |
| **License** | MIT |
| **CoolSolve** | 0.4.0@a53de60 — verified (see [Verification](#verification)) |

## Problem statement

In the desorber of an NH3/H2O absorption system, the rich solution enters at
150 °C with ammonia mass fraction 0.3; the vapour produced is in equilibrium
with this liquid (point *d*). Saturated liquid of the same mass fraction as
the vapour enters the evaporator at 0 °C (point *e1*). The evaporator outlet
is a saturated two-phase mixture whose liquid has ammonia mass fraction 0.25,
the whole evaporation taking place at constant pressure (point *e2*).
Determine: 1) the ammonia mass fraction of the desorber vapour, 2) the mass
fraction of the vapour in equilibrium with the evaporator inlet liquid, 3) the
temperature glide across the evaporator and the outlet vapour quality.

## Model

State 1 (desorber): `T[1] = 150 °C`, `x[1] = 0.3`; saturation pressure
`P[1] = Pressure(NH3H2O, T, x, Q=0)` and vapour composition
`y[1] = MassFraction(NH3H2O, T, P, Q=1)`. State 2 (evaporator inlet):
`T[2] = 0 °C`, `x[2] = y[1]`; `P[2]` and `y[2]` from the same two equilibrium
calls. State 3 (evaporator outlet): `P[3] = P[2]`, `x[3] = 0.25`;
`T[3] = Temperature(NH3H2O, P, x, Q=0)`, `y[3] = MassFraction(NH3H2O, P, T,
Q=1)`, outlet quality `Q[3]` from the evaporator mass balance
`Q[3]*y[3] + (1-Q[3])*x[3] = x[2]`, glide `T_glide = T[3] - T[2]`. Finally
`T_e2_min` (saturated-vapour temperature at `P[3]` and composition `y[1]`, as
in the original) and `x_e2_min`, the saturated liquid paired with that vapour.

## Niche

The absorption subcategory holds cycle models of the NH3/H2O single-stage
family (`CSL-0249`, `CSL-0347`, `CSL-0360`, …). This model is not a cycle: it
is the textbook three-state equilibrium exercise that demonstrates the large
evaporator temperature glide (about 75 K) characteristic of ammonia-water, the
property behaviour the cycle models rely on. It is also a minimal NH3H2O
property example (three `Pressure`/`Temperature`/`MassFraction` calls, one
mass balance).

## How to run

```bash
coolsolve ./nh3h2o_evaporator_glide.eescode
```

## Results (CoolSolve 0.4.0, EES stored solution in parentheses)

| Quantity | CoolSolve | EES |
|---|---:|---:|
| `P[1]` desorber pressure [Pa] | 2.7043e6 (27.04 bar) | 2.5871e6 (25.87 bar) |
| `y[1] = x[2]` desorber vapour mass fraction [kg/kg] | 0.85284 | 0.85299 |
| `P[2] = P[3]` evaporator pressure [Pa] | 3.6598e5 (3.660 bar) | 3.7288e5 (3.729 bar) |
| `y[2]` vapour in equilibrium at evaporator inlet [kg/kg] | 0.99996 | 0.99996 |
| `T[3] = T_glide` outlet temperature = glide [°C] | 75.10 | 77.47 |
| `y[3]` outlet vapour mass fraction [kg/kg] | 0.92172 | 0.91473 |
| `Q[3]` outlet vapour quality | 0.89745 | 0.90712 |
| `T_e2_min` [°C] | 87.84 | 88.64 |
| `x_e2_min` [kg/kg] | 0.19331 | 0.20019 |

The evaporator glide is 75–77 K (over the 0 °C inlet): the characteristic
large glide of ammonia-water, with the vapour much richer in ammonia
(`y ≈ 0.85–0.92`) than the liquid (`x = 0.25`). The evaporator mass balance
closes in both tools: `Q[3]*y[3] + (1-Q[3])*x[3] = 0.85287 ≈ x[2] = 0.85284`
(CoolSolve) and `0.85299 ≈ 0.85299` (EES).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric or
     equilibrium plot illustrating the glide, e.g.
     figures/nh3h2o_evaporator_glide_glidetable.png -->

## Verification

The solved CoolSolve model was compared with the solution stored in the
original binary EES file (`Ex9_1.EES` inside `ex9_1.eez`, EES 11.926) with
`tools/compare_solution.py nh3h2o_evaporator_glide.sol reference/ees_variables.csv
--ees-units` (bar→Pa conversion of the reference). Its printed table:

```
| Variable | EES | CoolSolve | rel. diff | |
|---|---:|---:|---:|---|
| P[1] | 2.58706e+06 | 2.70433e+06 | 4.34e-02 | **DIFF** |
| P[2] | 372882 | 365979 | 1.85e-02 | **DIFF** |
| P[3] | 372882 | 365979 | 1.85e-02 | **DIFF** |
| Q[3] | 0.907123 | 0.897445 | 1.07e-02 | **DIFF** |
| T[3] | 77.4655 | 75.0985 | 3.06e-02 | **DIFF** |
| T_e2_min | 88.6439 | 87.8354 | 9.12e-03 | **DIFF** |
| T_glide | 77.4655 | 75.0985 | 3.06e-02 | **DIFF** |
| x_e2_min | 0.200186 | 0.193307 | 3.44e-02 | **DIFF** |
| y[3] | 0.91473 | 0.921724 | 7.59e-03 | **DIFF** |

16 common variables, 9 differ (rtol=0.001); only in EES: 11; only in CoolSolve: 0
Only in EES reference: P[4], P[5], P[6], Q[1], Q[2], T[4], T[5], T[6], x[4], x[5], x[6]
```

Judgement: the rich-vapour mass fractions `y[1]` and `y[2]` agree within
0.02 %; `y[3]` differs 0.8 % and `x_e2_min` 3.4 %, the temperatures 0.9–3.1 %
(0.8–2.4 K). These deviations are the documented difference between the two
NH3H2O property formulations — EES uses Ibrahim & Klein (1993), CoolSolve
implements IAPWS G4-01 (Tillner-Roth & Friend 1998), see CoolSolve
`docs/nh3h2o_review.md` — already observed on the same family in `CSL-0347`
and `CSL-0360` (mass fractions within 3.5 % at identical inputs). The
pressures follow the same formulation difference (saturation pressures
1.9–4.3 % lower in CoolSolve); they are not off by a unit scale (the bar→Pa
conversion of the reference is applied). The "only in EES" records are stale
Variable-Information records of variables the equations do not define
(`Q[1]`, `Q[2]`, `T[4..6]`, `P[4..6]`, `x[4..6]`). No energy quantity appears
in the model. No independent reference beyond the EES stored solution.

## Source and attribution

EES example `ex9_1.ees` distributed by F-Chart Software with
*Absorption Chillers and Heat Pumps* (K. E. Herold, R. Radermacher,
S. A. Klein, CRC Press, 2nd ed., 2015), Example 9.1; the text copy carries the
download link of the original `.eez`. Distributed by the
EES-Community/ees-examples repository:
<https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/ex9_1.ees>
(inventory candidate `EEX-107`). Credit: (c) F-Chart Software / S. A. Klein,
MIT via EES-Community/ees-examples.

## Conversion log

- **2026-11-15 — import** (`tools/ees_extract.py` on the binary `Ex9_1.EES`
  extracted from the companion zip `ex9_1.eez`): EES 11.926, unit system
  `SI MASS DEG BAR C KJ`, 29 variable records, no lookup/parametric tables,
  no library functions. The text copy in the examples repository carries
  garbage characters after the last real equation (`x_e2_min`); the import
  stops there (the extraction of the binary ends at the same line).
- **Unit conversion (bar → Pa)**: the property results `P[1]`, `P[2]`, `P[3]`
  are used in Pa (no `/1e5`); no numeric pressure constant appears in the
  equations, so no equation changed value. Temperatures stay in °C; the kJ
  energy setting of the original is unused (no energy quantity). The
  `$UnitSystem` and `$TabStops` directives were removed.
- **`q=0` → `Q=0`** in the first `Pressure` call (capitalization of the
  quality keyword, as in the other calls of the original).
- Comments kept as in the original; typo "equilbrium" corrected; quantities
  annotated in SI units (mass fractions `[kg/kg]`); no `[-]` units.
- The EES file stores records for `Q[1]`, `Q[2]` and `T[4..6]`, `P[4..6]`,
  `x[4..6]`, which the equations do not define; they are stale records of
  earlier runs and are not part of the model.
- Property input pairs used: (T, x, Q), (T, P, Q), (P, x, Q), (P, T, Q) — all
  supported by CoolSolve; no (T, H) rewrite (decision D11) needed.

## Limitations and CoolSolve gaps

- None known. The NH3H2O fluid is supported by CoolSolve (IAPWS G4-01
  formulation; `ees_extract.py` flags NH3H2O as "unsupported fluids" as a
  heuristic warning, a false positive here).
- The verification relies on the EES stored solution only; the deviation
  level is that of the two NH3H2O property formulations (see *Verification*).

## Related models

- `CSL-0347` (*nh3h2o_absorption_ideal*) and `CSL-0360`
  (*nh3h2o_absorption_precooler*): the single-stage NH3/H2O absorption cycle
  models of the same textbook family (Herold chapter 9), of which this model
  is the evaporator-glide property exercise.
- `CSL-0249` (*nh3h2o_absorption_chiller*): detailed single-effect NH3/H2O
  chiller written for the library.
