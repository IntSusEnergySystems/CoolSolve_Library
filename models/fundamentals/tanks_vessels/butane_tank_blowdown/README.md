# Emptying a butane tank (blowdown, saturated-liquid outflow)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0351`

A rigid tank of 0.54 l contains 0.23 kg of n-butane at 25 °C (slightly two-phase:
`Phase_1$` = `twophase`). The tank is emptied at a constant mass flow rate of
0.035 g/s for 20 min and the outflow is **saturated liquid** (x = 0), as in the
original example; the saturated-vapour alternative of the original file is kept
as a comment and is not used. The model solves the unsteady uniform-state mass
and energy balances of the tank, integrating the internal energy over time, and
gives the state of the tank and of the outflow after 20 min.

| | |
|---|---|
| **Category** | Fundamentals › Tanks and vessels |
| **Fluids** | n-Butane |
| **Size** | 21 equations (1 integrated state, 20 algebraic variables; RK4, 1000 steps) |
| **Source** | Klein & Nellis, *Thermodynamics*, Cambridge University Press, 2011, example 4.5-3 (F-Chart Software EES example, EES-Community/ees-examples) |
| **Authors** | S. A. Klein and G. F. Nellis (F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@00a4daa — verified (see verification field) |

## Problem statement

Example 4.5-3 of Klein & Nellis (2011): a rigid tank of 0.54 l contains 0.23 kg
of butane at 25 °C. The tank is emptied at 0.035 g/s during 20 min, the escaping
fluid being saturated liquid at the state of the tank. Find the state of the
tank after 20 min.

## Model

Uniform-state unsteady balance on the tank contents, with the total internal
energy `U_tot` as the integrated state variable (the original file's commented
block calls it an "arbitrary state variable"):

- mass: `0 = m_dot_out*time + m − m_1`
- state: `v = Vol/m`, `u = U_tot/m`, `(T, P)` from the (u, v) pair of n-Butane
- outflow: saturated liquid at the tank pressure, `h_out = enthalpy('n-Butane',P=P,x=0)`
- energy: `0 = m_dot_out*h_out + dUdt`, integrated
  `U_tot = U_tot_1 + Integral(dUdt, time, 0, 1200 s)`

Inputs: `Vol`, `m_1`, `T_1`, `m_dot_out`. Outputs: the tank state `m, v, u, T, P`
and the outflow `h_out, dUdt` at 20 min (`time_min`).

## How to run

```bash
coolsolve ./butane_tank_blowdown.eescode
```

No guess file needed (the model solves from the built-in defaults); no
`coolsolve.conf`. The dynamic solver owns the integration variable `time` and
the state `U_tot`; at the end of the run every variable holds its value at
t = 1200 s, which is the state compared with the EES reference.

## Results (t = 20 min)

| Variable | Value | Unit |
|---|---:|---|
| `m` | 0.188 | kg |
| `T` | 24.680 | °C |
| `P` | 240.88 | kPa |
| `u` | 260 508 | J/kg |
| `v` | 0.0028723 | m³/kg |
| `h_out` | 258 679 | J/kg |
| `dUdt` | −9.0537 | W |
| `U_tot` | 48 975.6 | J |

Mass balance at 20 min: `m_dot_out*time` = 3.5·10⁻⁵ kg/s × 1200 s = **0.042 kg**
= `m_1 − m` = 0.23 − 0.188 = **0.042 kg**. Energy balance: `dUdt` = −9.0537493 W
= −`m_dot_out*h_out` = −3.5·10⁻⁵ × 258 678.55 J/kg (exact closure; the equation
is satisfied to 10⁻¹²). The tank internal energy drops by `U_tot_1 − U_tot` =
59 857.0 − 48 975.6 = **10 881.4 J** over the 20 min.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g. the trajectory of T and P from the Integral tab + one-line caption -->

## Verification

Compared with the solution stored by EES in the binary `.eez` companion of the
source file (20 common variables, `compare_solution.py --ees-units`; the EES
file stores temperatures in K and `P_kPa` in kPa). Summary quoted from the tool:

> Converted EES reference values: T_1 (K->C), T (K->C), P_kPa (kPa x1000)
>
> 20 common variables, 3 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 2

The three differences are explained:

- `P_kPa`: unit scale only. The original stores the reporting variable in kPa
  (241.296); the CoolSolve model computes it in kPa too (240.88), while the
  tool converts the kPa reference to Pa for the comparison. The same quantity
  is `P` (in Pa), which agrees to 1.7·10⁻³.
- `P` (1.72·10⁻³) and `P_1` (1.78·10⁻³): the n-butane property models of EES
  and CoolProp differ slightly (u and T agree to ≈3·10⁻⁴); the deviations are
  within the ≤ 0.5 % typical band of ees_import.md §11 for different
  equations of state.

Every other variable agrees within 3.2·10⁻⁴ relative (`ees-stored-solution`).
The two "only in CoolSolve" variables are `h_1` and the string `Phase_1$`, both
added by the `Phase$` rewrite of the conversion log. Checks:
`ees-stored-solution`, `energy-balance`.

## Source and attribution

- S. A. Klein and G. F. Nellis, *Thermodynamics*, Cambridge University Press,
  2011, example 4.5-3 "Emptying a butane tank"; EES example © F-Chart Software,
  MIT, distributed in the EES-Community/ees-examples collection (commit 5c703d0,
  `uncategorized/example_4.5-3.ees`) with the binary `.eez` companion
  (EES 11.912) whose stored solution is the verification reference.
- The file header points to the original download page
  `https://fchartsoftware.com/ees/examples/examples_thermodynamics_2011/chapter%204/example%204.5-3.eez`.
- Library source inventory: `sources/ees_examples/inventory.csv`, row `EEX-021`.

## Conversion log

- **2026-11-15 — import**: extraction of the `.eez` companion (EES 11.912,
  unit system `SI MASS RAD PA K J`) with `tools/ees_extract.py`; 20 stored
  variables taken as the verification reference. The original equations are
  unchanged except the items below.
- **2026-11-15 — unit conversion** (by hand, ees_import.md §6, K → °C):
  `Vol` = 0.00054 m³ (0.54 liter in the original), `T_1` = 25 °C (the original
  `ConvertTemp(C,K,25 [C])` removed), `m_dot_out` = 3.5·10⁻⁵ kg/s (0.035 g/s);
  `T` is already in °C so `T_C = T` (original `ConvertTemp(K,C,T)` removed);
  `P_kPa = P/1000` (original `P*Convert(Pa,kPa)`); integral upper limit 1200 s
  (20 min); `time_min = time/60` (original `Convert(s,min)`). No `$UnitSystem`
  directive in the CoolSolve file.
- **2026-11-15 — `Phase$` rewrite** (decision D11/D12 style, unsupported state
  pair): the original `Phase$('n-Butane',T=T_1,v=v_1)` is not accepted by
  CoolSolve (`phase$` takes its state among T/P/H/S/D/x, not `v`), and the
  (T, P) flash is refused by CoolProp for a state exactly on the saturation
  line, which the initial state is. Rewritten as
  `Phase$('n-Butane',P=P_1,h=h_1)` with the exact identity
  `h_1 = u_1 + P_1*v_1`: same state, supported pair, same result (`twophase`).
  The other pairs of the original ((T, v), (u, v)) are accepted by CoolSolve
  and kept.
- **2026-11-15 — directives dropped** (card decision): `$IntegralTable`,
  `$ShowWindow`, `$HideWindow` and `$TABSTOPS` are not in the library file; the
  model is shipped at the 20-min end state, which is the state the EES file
  stores. CoolSolve does support `$IntegralTable` (space- or comma-separated),
  so this drop is presentational, not a workaround. The brace comments of the
  original (the commented-out "arbitrary state variable" block and the
  commented-out saturated-vapour `h_out` line) parse as they are and are kept.
- **Level**: 21 equations → 0; largest algebraic block ≤ 5 → 0; no
  functions/arrays → 0; not multi-zone → 0; dynamics → 1; no curated guesses → 0.
  Score 1 → level 1 (the inventory guessed 2; the textbook exercise is chapter-4
  first-law material).

## Limitations and CoolSolve gaps

None blocking: the native file runs in CoolSolve as transcribed (every change
is logged above). `missing_features` is empty.

## Related models

None listed (`related` is empty). Nearest neighbours in the library are the
steady rigid-tank exercises of this category, e.g. `CSL-0003`
(methane_tank_evaporation) and `CSL-0048` (two_tanks_connected_valve_r12);
this model is the unsteady (integrated) blowdown variant.
