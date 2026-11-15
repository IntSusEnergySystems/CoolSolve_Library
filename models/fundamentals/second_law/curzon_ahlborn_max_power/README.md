# Endoreversible Carnot engine at maximum power (Curzon–Ahlborn)

🟢 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0350`

A heat-transfer-limited (endoreversible) Carnot cycle: internally reversible,
but the heat exchange with the hot reservoir (1273 K) and the cold reservoir
(298 K) occurs at finite rates through overall conductances A and B. The cycle
temperatures T_1 and T_2 that maximise the power output are determined by the
Lagrange undetermined-multiplier equations of the original (`$ifnot MinMax`
branch): the stationarity conditions dW/dT_i + λ·dψ/dT_i = 0 with the
endoreversibility constraint ψ = 0 are solved as a square steady system. At
the optimum the thermal efficiency is 1 − √(T_L/T_H), independent of A and B —
the Curzon–Ahlborn efficiency — below the Carnot efficiency 1 − T_L/T_H.

| | |
|---|---|
| **Category** | Fundamentals › Second law and exergy |
| **Fluids** | none |
| **Size** | 17 equations (largest block: 9) |
| **Source** | EES example `maxpower1.ees` (F-Chart Software, [repository mirror](https://github.com/EES-Community/ees-examples/blob/5c703d0/uncategorized/maxpower1.ees); also [fchartsoftware.com](https://fchartsoftware.com/ees/examples/maxpower1.ees)) |
| **Authors** | S.A. Klein / F-Chart Software |
| **License** | MIT |
| **CoolSolve** | 0.4.0@00a4daa — verified (see verification field) |

## Problem statement

As in the original example: an endoreversible Carnot engine delivers power
between two thermal reservoirs. Heat is received at the cycle high temperature
T_1 through conductance A (`Q_dot_H = A·(T_H − T_1)`) and rejected at the cycle
low temperature T_2 through conductance B (`Q_dot_L = B·(T_2 − T_L)`).
Internally the cycle is a Carnot cycle (`eta = 1 − T_2/T_1`). The maximum
power and the efficiency at that optimum are sought. The original demonstrates
two routes: a Min/Max search (not used here) and the Lagrange undetermined
multiplier method (used here).

## Model

- Heat exchange: `Q_dot_H = A*(T_H − T_1)`, `Q_dot_L = B*(T_2 − T_L)`, with
  A = 2700 W/K and B = 2100 W/K.
- Engine: `W_dot = Q_dot_H − Q_dot_L`, `eta = W_dot/Q_dot_H`,
  `eta = 1 − T_2/T_1` (absolute temperatures), `eta_Carnot = 1 − T_L/T_H`.
- Optimality (`$ifnot MinMax` branch, kept as in the original): derivatives
  `dW\dT1 = −A`, `dW\dT2 = −B`, constraint
  `psi = Q_dot_L/Q_dot_H − T_2/T_1` and its partial derivatives
  `dpsi\dT1`, `dpsi\dT2`, stationarity
  `dW\dTi + lambda*dpsi\dTi = 0`. 17 equations, 17 unknowns, one block of 9.

The system is solved as a square steady model; no Min/Max call is made.

## How to run

```bash
coolsolve curzon_ahlborn_max_power.eescode
```

Guess values are in `curzon_ahlborn_max_power.initials` (near the optimum);
without them Newton does not converge in 100 iterations.

## Results

| Variable | Value | Unit |
|---|---|---|
| T_1 | 712.38 | °C (985.53 K) |
| T_2 | 203.68 | °C (476.83 K) |
| Q_dot_H | 776 179 | W |
| Q_dot_L | 375 540 | W |
| W_dot | 400 639 | W |
| eta | 0.516169 | – |
| eta_Carnot | 0.765907 | – |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![Power output vs T_1](figures/curzon_ahlborn_max_power_w.png)  + one-line caption -->

## Verification

The plain-text source carries no stored solution and no companion `.eez`
file, so the results were checked analytically (the two checks requested for
this import):

- **Curzon–Ahlborn efficiency**: `eta − (1 − sqrt(T_L/T_H))` with the
  reservoir temperatures in kelvin is **3.29e-11 absolute (6.36e-11
  relative)** (solved 0.5161687335539 vs 0.5161687335210510).
- **Energy balance**: `W_dot − (Q_dot_H − Q_dot_L)` is **0.00e+00 W**
  (relative 0.00e+00), i.e. the balance holds to machine precision.

In addition, T_1, T_2, W_dot and eta match the closed-form optimum of the
endoreversible engine with unequal conductances, `T_1 = (A·T_H +
B·sqrt(T_H·T_L))/(A+B)` and `T_2 = T_1·sqrt(T_L/T_H)`, to 8 significant
digits (712.376276 °C, 203.678426 °C, 400 639.4 W, 0.51616873), and
`lambda = −(dW\dT1)/(dpsi\dT1)` = 1 241 961 W as solved.

## Source and attribution

EES example `maxpower1.ees` of F-Chart Software (S.A. Klein), demonstrating
the `$IF/$IFNOT` directive and the Lagrange-multiplier route to the maximum
power of an endoreversible Carnot cycle; published under the MIT licence by
the EES-Community/ees-examples repository (local inventory row
`sources/ees_examples/inventory.csv`, candidate `EEX-036`, path
`uncategorized/maxpower1.ees`). Imported at the Lagrange-branch optimum only,
as instructed by the task card; the Min/Max route of the original is not used.

## Conversion log

- **2026-11-15 — import**: plain-text export of the F-Chart example (not a
  binary `.ees` file: `ees_extract.py` does not apply, and there is no stored
  solution or `.eez` companion). Equations transcribed unchanged; comments
  kept and completed with SI units. The Diagram-window sentence and the
  `$ShowWindow Solution` line of the original are not transcribed (GUI
  features). `$TabStops` dropped (GUI display setting).
- **2026-11-15 — unit conversion** (ees_import.md §6): reservoir temperatures
  from kelvin to °C (`T_H = 999.85 °C` for 1273 K, `T_L = 24.85 °C` for
  298 K); every absolute-temperature ratio gained `+273.15`
  (`eta = 1 − (T_2+273.15)/(T_1+273.15)`, `eta_Carnot`, `psi`, `dpsi\dT1`,
  `dpsi\dT2`), while temperature *differences* (`T_H − T_1`, `T_2 − T_L`)
  are unchanged. Conductances A and B from kW/K to W/K
  (`A = 2700 W/K` for 2.7 kW/K, `B = 2100 W/K` for 2.1 kW/K). The original
  typo in the `Q_dot_L` comment ("Q_H = heat transfer rate from engine") is
  paraphrased as "heat transfer rate from the engine".
- **2026-11-15 — variable names**: the backslash names `dW\dT1`, `dW\dT2`,
  `dpsi\dT1`, `dpsi\dT2` are kept in the native file (valid EES, and CoolSolve
  accepts `\` in identifiers). No runnable variant is needed: the native file
  runs unchanged.
- **2026-11-15 — level**: equations 17 (< 50) → 0; largest block 9 (6–30) → 1;
  no functions/arrays → 0; no multi-zone → 0; no off-design/dynamics → 0;
  curated guesses needed (`.initials`) → 1. Score 2 → level 2 (equal to the
  inventory guess).

## Limitations and CoolSolve gaps

None: the native file runs as-is. The `$ifnot MinMax` branch of the original
is the only branch compiled (`MINMAX` is false in a CoolSolve solve, as in an
EES Solve command); no gap is registered for this card. The maximum power
itself is not searched numerically — it is imposed by the Lagrange
stationarity equations, so the model needs no optimiser (`CS-GAP-OPTIM` does
not apply to this file).

## Related models

None yet (`related` stays empty per the card): `CSL-0186` (Carnot engine
driving a Carnot refrigerator) treats reversible Carnot cycles between
reservoirs, without the heat-transfer limit.
