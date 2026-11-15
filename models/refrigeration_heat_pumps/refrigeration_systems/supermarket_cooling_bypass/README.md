# Supermarket cooling system with cooling-coil bypass

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0337`

Mixed-air air-conditioning of a retail space (a supermarket): outdoor air mixes
with return air, a fraction of the mix bypasses a cooling coil whose outlet is
saturated, the two streams re-mix and are reheated to the supply state. The
model computes the cooling-coil and reheat loads as functions of the bypass
fraction. It is one of the two case studies of Klein & Al-Habdan (1993) that
illustrate the built-in psychrometric functions of EES.

| | |
|---|---|
| **Category** | Refrigeration and heat pumps › Refrigeration systems and chillers |
| **Fluids** | AirH2O (humid air) |
| **Size** | 35 equations, all explicit (largest block: 1) |
| **Source** | EES example `Supermkt.ees` (F-Chart Software), case study of *Computer Applications in Engineering Education* Vol 1(3), 1993 |
| **Authors** | S. A. Klein |
| **License** | MIT — © F-Chart Software / S. A. Klein, MIT via EES-Community/ees-examples |
| **CoolSolve** | v0.4.0 — blocked by `CS-GAP-PSYCHRO-SAT`; runnable variant `supermarket_cooling_bypass_coolsolve.eescode` verified (see *Verification*) |

## Niche

This is the only library model of a **supermarket mixed-air system with a
bypassed cooling coil**: the bypass fraction is the free design/operation
parameter, and the coil outlet is closed by saturation (`R = 1`) rather than
by a contact factor. It is **not** a variant of `CSL-0145`
`refrigeration_co2_transcritical_booster`, which is a TESPy R744
transcritical booster refrigeration cycle (different fluid, different cycle,
no air side): the two models only share the category. The physics closest to
it are the coil/reheat air-handling models `CSL-0028` and `CSL-0292` (HVAC
exercises with the same saturated-coil closure), linked in *Related models*.

## Problem statement

A supermarket is conditioned with 4000 cfm (1.888 m³/s) of supply air at
62 °F (16.67 °C) and 55 % relative humidity. The return air is at 74 °F
(23.33 °C) and 54 % RH; the outdoor air (15 % of the supply flow) is at 82 °F
(27.78 °C) and 48 % RH, at atmospheric pressure. The outdoor and return airs
mix; (1 − ByPass) of the mixture goes through a cooling coil whose outlet is
saturated, the rest bypasses the coil; the two streams re-mix and a reheat
coil brings the mixture back to the supply state (same humidity ratio as the
supply, reheat at constant humidity). Determine the coil load `Q_C` and the
reheat load `Q_H` for bypass fractions from 0 to 0.75 (original parametric
table, 16 runs). The original problem statement is in the Diagram window of
the EES file, which is **not imported**.

## Model

All states are humid air (`AirH2O`); the mass flows are of dry air. States:
1 outdoor, 2 coil inlet mix, 3 coil outlet (saturated), 4 mix of coil outlet
and bypass, 5 supply (after reheat), 6 return, 7 coil-branch inlet, 8 bypass
branch. Mixing junctions close their water and energy balances on the dry-air
flows; the coil outlet is the saturated state at the humidity ratio `w[3]`
fixed by the humidity balance of the second mixing junction
(`w[4] = w[5]`, reheat at constant humidity). Loads:
`Q_C = m_dot[3]*(h[3] - h[2])` (negative: cooling) and
`Q_H = (h[5] - h[4])*m_dot[5]`.

| Inputs | Value (SI, converted) | Outputs (ByPass = 0.75) | Value |
|---|---|---|---|
| `Vol[5]` supply volume flow | 1.8878 m³/s (4000 cfm) | `m_dot[5]` supply dry-air flow | 2.277 kg/s |
| `T[5]` / `rh[5]` supply | 16.67 °C (62 F) / 0.55 | `w[3]` coil-outlet humidity ratio | 0.000881 kg/kg |
| `T[6]` / `rh[6]` return | 23.33 °C (74 F) / 0.54 | `T[3]` coil-outlet temperature | −16.58 °C |
| `T[1]` / `rh[1]` outdoor | 27.78 °C (82 F) / 0.48 | `T[2]` coil-inlet mix | 25.18 °C |
| `P_atm` atmospheric pressure | 101 353 Pa (14.7 psia) | `T[4]` mix after bypass | 9.02 °C |
| `ByPass` bypass fraction | 0.75 (last table run) | `Q_C` cooling-coil load | −54.6 kW |
| | | `Q_H` reheat load | 17.7 kW |

The system is fully explicit (largest block 1); no guess values are needed.

## How to run

The native file keeps the original equations and is **blocked** in CoolSolve:
the saturated coil-outlet state is evaluated with
`enthalpy/temperature(AirH2O, P=…, w=…, R=1)`, which CoolProp refuses
(registered gap `CS-GAP-PSYCHRO-SAT`; the message itself suggests
`dewpoint()`). The runnable variant
`supermarket_cooling_bypass_coolsolve.eescode` changes only that closure
(see *Conversion log*):

```bash
coolsolve ./supermarket_cooling_bypass_coolsolve.eescode
```

To reproduce the original parametric study, change `ByPass` (0 to 0.75) and
re-solve; CoolSolve parametric studies cannot sweep it here without editing
the file (the value is a plain input).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): psychrometric-style plot,
     e.g. Q_C and Q_H versus ByPass re-created as a parametric sweep
     (figures/supermarket_cooling_bypass_sweep.png) -->

## Results

ByPass = 0.75 (the stored EES run):

| Quantity | EES (SI) | CoolSolve (variant) |
|---|---:|---:|
| `w[3]` [kg/kg] | 0.000879 | 0.000881 |
| `T[3]` [°C] | −16.56 | −16.58 |
| `Q_C` [kW] | −54.50 | −54.60 |
| `Q_H` [kW] | 17.72 | 17.74 |

Parametric check (variant vs Table 1 converted to SI): ByPass = 0 →
`T[3]` 7.594/7.596 °C, `Q_C` −57.81/−57.90 kW, `Q_H` 21.04/21.03 kW;
ByPass = 0.4 → `T[3]` 3.429/3.430 °C, `Q_C` −51.69/−51.77 kW, `Q_H`
14.91/14.91 kW. The loads have a shallow minimum around ByPass ≈ 0.6: over
the sweep the coil load stays within 13 % (−57.8 to −50.1 kW) while the
reheat load drops by about 37 % (21.0 to 13.3 kW), as in the original study.

## Verification

**The variant is verified; the native file is blocked** (`CS-GAP-PSYCHRO-SAT`
in `missing_features`). The variant was compared with
`tools/compare_solution.py` against the solution stored in `Supermkt.ees`
(converted to SI by hand from the stored English units: F, psia, cfm,
ft³/lbm, lbm/min, Btu/lbm, Btu/min), 35 common variables, "35 common
variables, 15 differ (rtol=0.001)":

- `Q_C` −54 498 / −54 603 W (rel. diff 1.93e-03), `Q_H` 17 720 / 17 739 W
  (1.03e-03), `T[3]` −16.5625 / −16.5826 °C (1.21e-03);
- humidity ratios `w[i]` +0.24 to +0.45 % (EES vs CoolProp humid-air
  formulation, same magnitude as on `CSL-0028`);
- absolute enthalpies `h[i]` differ by a near-constant **+17.8 to +17.9
  kJ/kg of dry air** — a reference-state offset (the EES 8.868 humid-air
  reference, ≈ dry air at 0 °F, vs the CoolProp/ASHRAE one, dry air at 0 °C).
  Enthalpy *differences* agree: coil Δh within 0.157 %, reheat Δh within
  0.066 %;
- all remaining variables (temperatures, flows, `v[5]`, inputs) within
  1e-03.

Parametric table (Table 1, 16 × 4, checked against the file: its last row
equals the stored solution): rows ByPass = 0, 0.4 and 0.75 re-solved in
CoolSolve agree within 0.16 % (largest: `Q_C` at ByPass = 0).

## Source and attribution

Case study of **S. A. Klein**, *Computer Applications in Engineering
Education*, Vol 1(3), pp. 265–275, 1993 (with N. M. Al-Habdan), distributed
as an EES example (`Supermkt.ees`, the problem statement and a psychrometric
plot are in the file's Diagram/Plot windows). Copyright © F-Chart Software /
S. A. Klein, MIT licence, via EES-Community/ees-examples
(`Case_Study/supermkt.ees`, commit 5c703d0). The problem statement is
paraphrased here; the paper and the Diagram window are not reproduced.
Source file (stored solution and parametric table):
`~/Nextcloud/thermo_models/EES_library/Supermkt.ees`
(inventory candidate `EEL-110`).

## Conversion log

- **2026-11-12 — import** (`tools/ees_extract.py`): EES 8.868, unit system
  ENG mass with English-unit results (the inventory cell "ENG MASS DEG KPA C
  KJ" is the raw byte decoding, flagged unverified; the stored solution units
  are F/psia/Btu/lbm). Converted by hand to SI-°C-Pa-J:
  `Vol[5]` 4000 cfm → 1.8878 m³/s, `T[5]` 62 F → 16.667 °C, `T[6]` 74 F →
  23.333 °C, `T[1]` 82 F → 27.778 °C, `P_atm` 14.7 psia → 101 353 Pa; every
  other equation is a homogeneous balance or a property call and is
  unchanged. `$TabStops`/`$ShowWindow Plot` directives and the EES licence
  tag removed. Comments kept/paraphrased from the original (English); the
  file-level description paraphrases the problem (paper and Diagram window
  not reproduced).
- **2026-11-12 — parametric input**: `ByPass` is defined only by the
  original parametric table; `ByPass = 0.75` (the stored EES run, last table
  row) is set as the default run so the committed baseline matches the
  stored solution.
- **2026-11-12 — runnable variant** `supermarket_cooling_bypass_coolsolve.eescode`
  (gap `CS-GAP-PSYCHRO-SAT`): `h[3]`/`T[3]` from
  `enthalpy/temperature(AirH2O, P=…, w=w[3], R=rh[3])` with `rh[3]=1`
  replaced by `T[3] = dewpoint(AirH2O, P=P_atm, w=w[3], T=T[1])` (the
  saturated coil-outlet temperature is its dew point) followed by
  `h[3] = enthalpy(AirH2O, P=P_atm, w=w[3], T=T[3])`; both forms are valid
  EES. No other equation or value changed. The variant is what is verified
  above; it needs no guess values (fully explicit system).
- **Level**: equations 35 < 50 → 0; largest block 1 ≤ 5 → 0;
  functions/arrays → 1; ≥ 3 coupled components (mixing junctions, coil,
  bypass, reheat) → 1; no calibration/off-design → 0; no curated guesses → 0.
  Score 2 → level 2 (matches the inventory guess).

## Limitations and CoolSolve gaps

- **Blocked (native file)** by `CS-GAP-PSYCHRO-SAT` — saturated-state
  temperature/enthalpy of humid air at given humidity ratio
  (`temperature/enthalpy(AirH2O, P=…, w=…, R=1)`); already registered, with
  reproducer and suggested `dewpoint()` workaround (used by the variant
  here). When the gap closes, the native file can be re-checked
  (`T-RECHECK`); the `T[3]` difference between the tools (0.02 K here) will
  remain a property-formulation difference.
- The Diagram window of the original EES file (problem statement, psychrometric
  plot) is **not imported** (card C-518 owns diagram-window handling).
- Humidity ratios differ from EES by up to 0.45 % (CoolProp vs EES humid-air
  formulation); absolute enthalpies carry the reference-state offset
  described in *Verification*.
- `CS-GAP-PSYCHRO-SAT` also means the built-in psychrometric chart cannot be
  produced for this model yet (`CS-FEAT-PSYCHRO` tracks the chart itself).

## Related models

- `CSL-0028` *air_handling_unit_moist_air*: AHU with cooling coil closed by
  a contact factor and post-heating; blocked by the same gap, same
  `dewpoint()` pattern in its `_coolsolve` variant.
- `CSL-0292` *room_air_conditioning_coil_reheat*: room conditioning with a
  cooling coil and reheat (same saturated-coil closure, room air recirculation
  instead of a bypass fraction).
