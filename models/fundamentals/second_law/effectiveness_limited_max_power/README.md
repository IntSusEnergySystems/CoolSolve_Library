# Effectiveness-limited heat engine at maximum power

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0359`

Maximum power of an endoreversible heat engine whose heat exchange with the hot
and the cold stream is limited by the effectivenesses of its boiler and
condenser (effectiveness–NTU relations). The engine runs at the
Curzon–Ahlborn-type efficiency `eta_mp = 1 − sqrt(T_C_in/(phi·T_H_in))` with an
irreversibility factor `phi`, and the maximum power `W_dot_max` follows from the
two effectiveness relations. This is the active block of EES example 8.6-1; the
toluene Rankine plant of the original sits inside one comment block and is not
imported.

| | |
|---|---|
| **Category** | Fundamentals › Second law and exergy |
| **Fluids** | none (property calls; `F$ = 'Toluene'` is an unused string label) |
| **Size** | 26 equations (largest block: 1, fully explicit) |
| **Source** | EES example `Case_Study/example_8.6-1.ees` (F-Chart Software, [repository mirror](https://github.com/EES-Community/ees-examples/blob/5c703d0/Case_Study/example_8.6-1.ees), binary + stored solution in `ees-examples-raw/Case_Study/example_8.6-1.eez`) |
| **Authors** | S.A. Klein, G.F. Nellis |
| **License** | MIT |
| **CoolSolve** | 0.4.0@a53de60 — verified (see verification field) |

## Problem statement

As in the original example: a heat engine is coupled to a hot water stream
(65 gpm, 180 °C, ρ = 1000 kg/m³, c = 4200 J/kg-K) and to a cooling-air stream
(23 500 cfm, 25 °C, ρ = 1 kg/m³, c = 1000 J/kg-K) through a boiler of
conductance 33 kW/K and a condenser of conductance 35 kW/K. The engine is
endoreversible with irreversibility factor `phi = eta_HPt = 0.87`, so its
maximum-power efficiency is the Curzon–Ahlborn form
`eta_mp = 1 − sqrt(T_C_in/(phi·T_H_in))` and the Carnot bound with the same
factor is `eta_max = 1 − T_C_in/(phi·T_H_in)`. The maximum power is

```
W_dot_max = eff_cond·C_dot_C · eff_b·C_dot_H · phi·(sqrt(T_H_in) − sqrt(T_C_in/phi))²
            / (eff_b·C_dot_H + eff_cond·C_dot_C·phi)
```

with `eff_b = 1 − exp(−UA_b/C_dot_H)` and `eff_cond = 1 − exp(−UA_cond/C_dot_C)`.
(Temperatures under the square roots are absolute; the file stores °C and adds
273.15 inside those formulas.) The full derivation is Example 8.6-1 of the
source book; the library model imports only the resulting active block, not the
Rankine design that motivates it.

## Model

One explicit block: stream data → capacitance rates → effectivenesses →
efficiencies → maximum power. 26 equations, 26 unknowns, largest block 1; no
iteration (CoolSolve solves in 0 iterations, no `.initials` needed).

| Input | Value | Unit |
|---|---|---|
| T_H_in | 180 | °C |
| V_dot_H | 65 gpm = 4.10086277e-3 | m³/s |
| rho_H | 1000 | kg/m³ |
| c_H | 4200 | J/kg-K |
| T_C_in | 25 | °C |
| V_dot_C | 23 500 cfm = 11.09076491 | m³/s |
| rho_C | 1 | kg/m³ |
| c_C | 1000 | J/kg-K |
| UA_b | 33 kW/K = 33 000 | W/K |
| UA_cond | 35 kW/K = 35 000 | W/K |
| eta_HPt (= phi) | 0.87 | – |

Declared but unused by the active equations (kept as in the original, they feed
its commented Rankine section): `F$`, `T_t_in`, `eta_LPt`, `eta_HPp`, `eta_LPp`.

## How to run

```bash
coolsolve effectiveness_limited_max_power.eescode
```

No `.initials`, no `coolsolve.conf`: every equation is an explicit assignment.

## Results

| Variable | Value | Unit |
|---|---|---|
| m_dot_H | 4.100863 | kg/s |
| C_dot_H | 17 223.624 | W/K |
| eff_b | 0.852801 | – |
| m_dot_C | 11.090765 | kg/s |
| C_dot_C | 11 090.765 | W/K |
| eff_cond | 0.957395 | – |
| phi | 0.87 | – |
| eta_mp | 0.130365 | – |
| eta_max | 0.243736 | – |
| W_dot_max | 43 675.461 | W |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![W_dot_max vs phi](figures/effectiveness_limited_max_power_w.png)  + one-line caption -->

## Verification

Compared with the solution stored by EES in the companion binary
(`ees-examples-raw/Case_Study/example_8.6-1.eez`), extracted with
`ees_extract.py` and compared with

```bash
python3 compare_solution.py effectiveness_limited_max_power.sol reference/ees_variables.csv --ees-units
```

(output in the work folder; unit conversions K→°C applied by the tool to the
`T*` variables stored in K). Quoted result:

> 25 common variables, 0 differ (rtol=0.001); only in EES: 50; only in CoolSolve: 1

The 50 EES-only records are the toluene Rankine cycle of the commented block
(`h[i]`, `s[i]`, `P[i]`, `T[i]`, `W_dot_*`, `eta`, `m_dot`, `f`…) plus older-run
leftovers (`eta_t`, `eta_p`), which the card excludes from scope; the 1
CoolSolve-only entry is `F$` (string, no stored record). Largest relative
deviation on the common variables: 5.7e-08 (`m_dot_H`, `C_dot_H`; EES stores
7-digit values). Key values, EES stored vs CoolSolve: W_dot_max 43 675.46189 vs
43 675.46139 W, eff_b 0.8528014639 vs 0.8528014800, eff_cond 0.9573947907 vs
0.9573947899, eta_mp 0.1303654446 vs 0.1303654456, eta_max 0.2437357400 vs
0.24373573999 — all within the real-fluid tolerance of ees_import.md §11
(easy algebra, so 1e-7-level agreement is expected).

## Source and attribution

Example 8.6-1 of *THERMODYNAMICS*, S.A. Klein and G.F. Nellis, Cambridge
University Press, 2011, from the F-Chart Software EES example set; published
under the MIT licence by the EES-Community/ees-examples repository (local
inventory row `sources/ees_examples/inventory.csv`, candidate `EEX-302`).
Imported per the task card: only the active block from the hot-fluid inlet
through `W_dot_max`; `PROCEDURE Turbine`, `PROCEDURE Pump` and the
brace-commented toluene Rankine cycle are not imported.

## Conversion log

- **2026-11-15 — extraction**: `ees_extract.py` on the inner `Example 8.6-1.EES`
  of the `.eez` companion (the `.eez` is a zip; it was unzipped first).
  EES X11.912, RTF equations, unit system `SI MASS RAD PA K J` — conversion
  required; 75 variable records, no lookup/parametric tables; functions called
  but not defined: none outside the two imported-away PROCEDUREs.
- **2026-11-15 — unit conversion** (ees_import.md §6, by hand): temperatures
  from K to °C (`T_H_in = 180 °C` for 453.15 K, `T_C_in = 25 °C` for 298.15 K,
  `T_t_in = 170 °C` for 443.15 K); `ConvertTemp(C,K,…)` calls removed; the
  273.15 offsets appear only inside the formulas that need absolute
  temperatures (`eta_mp`, `eta_max`, both square roots of `W_dot_max`);
  temperature *differences* unchanged. `65 gpm` → `65·6.30901964e-5 m³/s`,
  `23 500 cfm` → `23 500·4.71947443e-4 m³/s`, `33 kW/K` → `33 000 W/K`,
  `35 kW/K` → `35 000 W/K` (no `Convert`/`ConvertTemp` calls remain).
  `RAD`→`deg` trig setting irrelevant (no trig calls besides `sqrt`).
- **2026-11-15 — scope**: `PROCEDURE Turbine`, `PROCEDURE Pump` and the
  brace-commented toluene Rankine block are not imported (per the card); the
  five declared constants that only feed that block (`F$`, `T_t_in`, `eta_LPt`,
  `eta_HPp`, `eta_LPp`) are kept so the active block stays complete; `phi`
  keeps its original link `phi = eta_HPt`. `$TabStops` dropped (GUI setting).
- **2026-11-15 — level**: equations 26 (< 50) → 0; largest block 1 (≤ 5) → 0;
  no functions/arrays → 0; no multi-zone → 0; no off-design/dynamics → 0; no
  curated guesses → 0. Score 0 → level 1 (inventory guessed 2; the chain is a
  textbook-level explicit calculation).

## Limitations and CoolSolve gaps

None: the native file runs as-is, no gap registered for this card. The maximum
power is obtained in closed form by the original derivation (the book shows a
Min/Max route that lives in the commented Rankine block); no optimiser is
needed here (`CS-GAP-OPTIM` does not apply to this file).

## Related models

CSL-0350 (endoreversible Carnot engine at maximum power, Curzon–Ahlborn): same
maximum-power principle with conductance-limited heat exchange on both
reservoirs; the present model is its effectiveness-form counterpart, with the
irreversibility factor phi and maximum-power efficiency
1 − sqrt(T_C_in/(phi·T_H_in)).
