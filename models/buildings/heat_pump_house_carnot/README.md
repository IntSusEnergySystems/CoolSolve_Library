# Carnot heat pump for a house in winter and summer

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0184`

Teaching exercise: a heat pump heats a house in winter and, reversed, cools
it in summer. The fabric loss is proportional to the indoor-outdoor
temperature difference, and the machine is an ideal Carnot heat pump between
the indoor air and the outdoor air. The model computes the winter heating
COP and the electric power, then the highest outdoor temperature that same
power can hold in summer.

| | |
|---|---|
| **Category** | Buildings |
| **Fluids** | none |
| **Size** | 17 equations (largest block: 4) |
| **Source** | thermo_models, ULiège MECA0002, repetition R4 exercise 6 (2022-2023), file `R04_E6_2022.EES` |
| **Authors** | S. Quoilin |
| **License** | MIT |
| **CoolSolve** | 0.3.0@96e4c95 — verified against the EES stored solution and the closed form (see *Verification*) |

## Problem statement

A heat pump heats a house in winter and, with its operation reversed, cools
it in summer. The indoor temperature is held at 20 °C in winter and 25 °C
in summer. Heat loss through the walls and the roof is 2400 kJ per hour per
degree of difference between indoors and outdoors.

(a) The outdoor temperature in winter is 0 °C. What is the minimum power
required to run the heat pump?

(b) With the power kept equal to the result of (a), what is the highest
outdoor temperature at which the indoor temperature can still be held at
25 °C?

The quoted statement in the file asks, in (b), for the outdoor temperature
at which an outdoor temperature of 25 °C can be kept. The equation-window
comment and the equations hold the indoor temperature at 25 °C
(`T_h_s = 25 °C`) and solve for the outdoor temperature `T_ext_s_MAX`.
This import follows the equation window. The stored solution does not
contain a solved value of `T_ext_s_MAX` either (see *Verification*).

## Model

The heat pump is a Carnot machine. Winter heat delivered to the house
replaces the fabric loss. Summer, the same electric power extracts heat
from the house.

- Fabric loss coefficient `K_loss = 2400×1000/3600` W/K (2400 kJ/h per kelvin in the original).
- Winter loss `Q_dot_loss = K_loss (T_h_w − T_ext_w)`, and the heat delivered is `Q_dot_C = |Q_dot_loss|`.
- Heating COP `COP_a = Q_dot_C / W_dot = 1 / (1 − T_ext_w_K / T_h_w_K)`, with `T_K = T + 273.15`.
- Cooling COP `COP_b = Q_dot_F / W_dot = 1 / (T_ext_s_MAX_K / T_h_s_K − 1)`.
- Cooling load `Q_dot_F = |K_loss (T_h_s − T_ext_s_MAX)|`.
- `T_ext_s_MAX_C` repeats `T_ext_s_MAX` in °C, as the original unit check did.

| Input | Value |
|---|---|
| `T_h_w` | 20 °C |
| `T_ext_w` | 0 °C |
| `T_h_s` | 25 °C |
| `K_loss` | 2400 kJ/h-K, written as 666.667 W/K |

`T_h_w`, `T_h_s`, `T_ext_w` and `K_loss` are equations. The system is square
(17 equations, 17 variables) with the four absolute-temperature definitions
included. No Diagram-window value was substituted. The stored names `COP`
and `Pertes` have no equation in the file; they are left out.

The summer outdoor temperature, its absolute value, the cooling load and
`COP_b` form one algebraic block of 4. Everything else is explicit.

## How to run

```bash
coolsolve ./heat_pump_house_carnot.eescode
```

CoolSolve reports 24 iterations without `.initials` and 2 iterations with
the shipped `.initials`. Both runs succeed. The iterations are the Newton
solve of the summer block. No `coolsolve.conf` is used.

## Results

Winter (the stored EES solution was solved for these names):

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `COP_a` | 14.6575 | 14.6575 |
| `Q_dot_C` | 13333.333 W | 13.33333333 kW |
| `Q_dot_loss` | 13333.333 W | 13.33333333 kW |
| `W_dot` | 909.659 W | 0.9096594462 kW |
| `T_h_w` | 20 °C | 293.15 K |
| `T_ext_w` | 0 °C | 273.15 K |

Summer. The electric power stays at the winter value. CoolSolve solves the
equation window. The EES file still holds the guesses for these names
(see *Verification*).

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `COP_b` | 14.7820 | 1 (guess) |
| `Q_dot_F` | 13446.6 W | 1 kW (guess) |
| `T_ext_s_MAX` | 45.1698 °C | 273 K (guess and lower bound) |
| `T_ext_s_MAX_C` | 45.1698 °C | 1 °C (guess) |
| `T_h_s` | 25 °C | 298.15 K |

Closed form of the same equations: `COP_a = 293.15/20 = 14.6575`,
`W_dot = 909.659446245` W, `T_ext_s_MAX = 45.169840` °C,
`COP_b = 14.781971`, `Q_dot_F = 13446.560` W.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

## Verification

`compare_solution.py --ees-units` against `reference/ees_variables.csv` from
`R04_E6_2022.EES` (EES X10.836, 15 stored variables). The tool's summary line:

> 13 common variables, 5 differ (rtol=0.001); only in EES: 2; only in CoolSolve: 4

The printed maximum relative difference over all common variables is
**1.00e+00** (`T_ext_s_MAX`). The unrounded ratio is 1.00332:
`|45.1698 − (−0.15)| / 45.1698`, where −0.15 °C is the stored 273 K after
the K→°C conversion.

| Variable | EES (after `--ees-units`) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `T_ext_s_MAX` | −0.15 °C | 45.1698 °C | 1.00e+00 |
| `T_ext_s_MAX_adimentionel` | 1 | 318.320 | 9.97e-01 |
| `T_ext_s_MAX_C` | 1 °C | 45.1698 °C | 9.78e-01 |
| `COP_b` | 1 | 14.7820 | 9.32e-01 |
| `Q_dot_F` | 1000 W | 13446.6 W | 9.26e-01 |
| `Q_dot_C`, `Q_dot_loss` | 13333.33333 W | 13333.33333 W | 2.50e-10 |
| `K_loss` | 666.6666667 W/K | 666.6666667 W/K | 4.99e-11 |
| `W_dot` | 909.6594462 W | 909.6594462 W | 4.92e-11 |
| `COP_a`, `T_h_w`, `T_h_s`, `T_ext_w` | assigned | assigned | 0 |

The five differences are the summer unknowns. In `ees_variables.csv` each
stored value equals its guess: `COP_b = 1`, `Q_dot_F = 1` kW,
`T_ext_s_MAX = 273` K (also the lower bound), `T_ext_s_MAX_C = 1`,
`T_ext_s_MAX_adimentionel = 1`. Those five numbers are not a solution of
the equations. `COP_b = Q_dot_F / W_dot` would be about 1.1 if
`Q_dot_F` were 1 kW, and `T_ext_s_MAX_C` would be −0.15 °C if
`T_ext_s_MAX` were 273 K. The winter names were solved and saved; they
match after the unit conversion, and the residuals are the stored solution
written with fewer digits.

Only in the EES reference: `COP` (14.65, which rounds `COP_a = 14.6575`)
and `Pertes` (−175.1018087 kW). Both are absent from the equation window.
The system is square without them, so they were not restored. `Pertes`
does not equal the fabric loss.

Only in CoolSolve: `T_h_w_K`, `T_h_s_K`, `T_ext_w_K`, `T_ext_s_MAX_K`, the
absolute temperatures added so the Carnot ratios stay in kelvin.

Closed form, with `dT = T_ext_s_MAX − T_h_s`:

`COP_a = T_h_w_K / (T_h_w_K − T_ext_w_K) = 14.6575`,

`W_dot = K_loss (T_h_w − T_ext_w) / COP_a`,

`dT² = W_dot · T_h_s_K / K_loss`,

`COP_b = T_h_s_K / dT`, `Q_dot_F = K_loss · dT`.

That gives `T_ext_s_MAX = 45.169840` °C, `COP_b = 14.781971` and
`Q_dot_F = 13446.560` W. The shipped solution matches those digits. A
start from the default guesses stops about 2×10⁻⁸ relative short of the
same closed form (solver residual about 1.4×10⁻⁶), still inside rtol.

## Source and attribution

Repetition exercise 6, session R4, of the ULiège course *Thermodynamique
appliquée* (MECA0002), 2022-2023. The EES file names no person. The
`{$ID$}` tag is the laboratory licence, not an author. Authors:
S. Quoilin, as the course instructor named in the inventory.

Source: `~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R4/R04_E6_2022.EES`

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` on `R04_E6_2022.EES` (EES X10.836). Unit system `$UnitSystem SI MASS DEG KPA C KJ`, deleted. The extractor rewrote the decimal commas (`273,15` → `273.15`, `1,0` → `1.0`). No lookup table, no parametric table, no `$Export`. 13 equations in the equation window, 15 stored variables. The system is square, so no Diagram-window value was restored.
- **2026-10-15 — units**: thermodynamic temperatures are stored in °C, and each Carnot temperature keeps an absolute-temperature equation `T_K = T + 273.15`.
  - `T_h_w`: `20 + 273.15` K → `20` °C, with `T_h_w_K = T_h_w + 273.15`
  - `T_h_s`: `25 + 273.15` K → `25` °C, with `T_h_s_K = T_h_s + 273.15`
  - `T_ext_w`: `0 + 273.15` K → `0` °C, with `T_ext_w_K = T_ext_w + 273.15`
  - `T_ext_s_MAX`: unknown, was K → unknown in °C, with `T_ext_s_MAX_K = T_ext_s_MAX + 273.15`
  - `K_loss`: `2400 [kJ] / 3600 [s-K]` = 0.6666666667 kW/K → `2400*1000/3600` = 666.6666667 W/K
  - `Q_dot_C`, `Q_dot_loss`, `Q_dot_F`, `W_dot`: follow from `K_loss`, so kW → W (×1000)
  - Carnot ratios use the `_K` variables. The loss equation uses a temperature difference, unchanged
  - `T_ext_s_MAX_C`: the original `(T_ext_s_MAX/1[K])*1[C] − 273.15` becomes `T_ext_s_MAX_K − 273.15`. The factors 1 do not change the number
  - No pressure in the file
- **2026-10-15 — statement**: question (b) in the pasted statement says “température extérieure de 25 °C”. The equation window holds the house at 25 °C and solves for the outdoor temperature. The equations were kept.
- **Level**: equations 17 → 0 (< 50); largest block 4 → 0 (≤ 5); no procedure, function, array or `DUPLICATE` → 0; one loss and one Carnot machine → 0; no calibration, off-design or dynamics → 0; converges from the default guesses (24 iterations), no `coolsolve.conf` → 0. Score 0 → level 1. Four of the 17 equations are the kelvin conversions; the equation window has 13.

## Limitations and CoolSolve gaps

The loss is linear in the indoor-outdoor temperature difference, and the
heat pump is reversible and Carnot. The summer electric power is fixed at
the winter minimum. The model has no refrigerant loop and no part-load map.

No CoolSolve gap blocks this file.

## Related models

- `CSL-0186` (*carnot_engine_refrigerator*): the previous exercise in the
  same session, a Carnot engine driving a Carnot refrigerator.
