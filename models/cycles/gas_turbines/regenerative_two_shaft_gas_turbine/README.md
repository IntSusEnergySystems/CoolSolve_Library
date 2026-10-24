# Regenerative two-shaft gas turbine (THD10 R05 exercise 4)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0296`

A gas turbine plant on ideal-gas air: a compressor, a regenerator, a
combustion chamber, a high-pressure turbine that only drives the compressor
and a low-pressure (power) turbine expanding to ambient pressure. All seven
stations are solved simultaneously — the regenerator couples the air side
(station 3) to the gas side downstream (station 6) — and the model returns
the enthalpies, temperatures and entropies at every station, the LP shaft
power, the regenerator heat rate and the combustion-chamber heat rate.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines |
| **Fluids** | Air (ideal gas) |
| **Size** | 43 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (THD10), repetition 5 (2010), exercise 4 (EES file `THD10_R05_E4.EES`, inside `THD10_R05.zip`) |
| **Authors** | TBD (no author named in the file; the inventory credits S. Bertagnolio and S. Borguet for the 2010 THD exercise sets) |
| **License** | MIT |
| **CoolSolve** | v0.4.0@9768373 — verified against the EES stored solution (see *Verification*) |

## Problem statement

A gas turbine is made of a compressor, a combustion chamber, two turbines
(HP and LP) and a regenerator. Air enters the compressor at 25 °C and
1 bar and is compressed to 4 bar. The HP turbine inlet temperature is
1150 K and the aspirated air flow rate is 1 kg/s. Determine:

a) the enthalpy of the air at the different stations;
b) the representation of these points on a T-s diagram;
c) the power available at the LP shaft;
d) the thermal power exchanged in the regenerator;
e) the thermal power consumed in the combustion chamber.

Working hypotheses: air as a perfect gas; combustion products treated as
air; isentropic efficiency of the compressor and of the expanders 95 %;
regenerator effectiveness 90 %; the HP turbine only drives the compressor;
isobaric heat exchangers.

## Model

One equation block per station, walked from 1 to 7 but solved
simultaneously (as in the original: *"Nous allons en pratique résoudre les
points a) à e) simultanément"*):

- stations 1–2 (compressor): `h[1]`, `s[1]` from (T[1], p[1]); the
  isentropic efficiency `eta_is_c = (h_2_is − h[1])/(h[2] − h[1])` with
  `h_2_is` at (s[1], p[2]); compressor power `W_dot_cmp = q_m (h[2] − h[1])`;
- station 3 (regenerator, air side): `p[3] = p[2]` and
  `eta_regen = Q_dot_regen_reel_air / Q_dot_regen_max` with
  `Q_dot_regen_max = q_m (h[6] − h[2])` — the coupling with station 6;
- station 4 (combustion chamber): `p[4] = p[3]`, `h[4]` from T[4] = 877 °C
  (1150 K in the original), `Q_dot_cc = q_m (h[4] − h[3])`;
- stations 5–6 (turbines): each with
  `eta_is_t = (h − h_in)/(h_is − h_in)`; HP-shaft balance
  `W_dot_thp + W_dot_cmp = 0`; `p[6] = p[1]` (full expansion to ambient);
  LP power `W_dot_tbp = q_m (h[6] − h[5])`;
- station 7 (regenerator, gas side): `p[7] = p[1]` and the heat balance
  `Q_dot_regen_reel_gaz + Q_dot_regen_reel_air = 0`.

Default operating point (kept from the file, the regression case): 1 bar /
25 °C suction, 4 bar discharge, TET 1150 K (as `1150 − 273` in the
original), `q_m` = 1 kg/s, `eta_is_c` = `eta_is_t` = 0.95, `eta_regen` = 0.9.

## How to run

```bash
coolsolve ./regenerative_two_shaft_gas_turbine.eescode
```

The model solves from CoolSolve's default guesses too (159 iterations);
`.initials` holds the EES stored solution, converted to SI.

## Results

| Quantity | EES | CoolSolve |
|---|---:|---:|
| `T[2]` compressor outlet [°C] | 176.54 | 176.38 |
| `T[3]` regenerator air outlet [°C] | 516.41 | 516.35 |
| `p[5]` HP turbine outlet [Pa] | 237 730 | 237 757 |
| `T[5]` [°C] | 744.44 | 744.46 |
| `T[6]` LP turbine outlet [°C] | 552.66 | 552.62 |
| `T[7]` regenerator gas outlet [°C] | 215.50 | 215.34 |
| `W_dot_cmp` [W] | 153 209 | 153 205 |
| `W_dot_tbp` LP shaft power [W] | −215 734 | −215 841 |
| `Q_dot_regen_reel_air` [W] | 359 004 | 359 243 |
| `Q_dot_cc` [W] | 408 832 | 408 963 |

The states are stored in the arrays `p[i]`, `T[i]`, `h[i]`, `s[i]`
(i = 1 compressor inlet … 7 regenerator gas outlet), ready for the CoolSolve
T-s diagram (task b of the exercise).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the cycle or
     efficiency/power vs pressure ratio sweep, figures/regenerative_two_shaft_gas_turbine_ts.png -->

## Verification

EES stored solution of `THD10_R05_E4.EES` (EES X8.423, kPa/kJ units;
`compare_solution.py … --ees-units`), printed result:

> 42 common variables, 17 differ (rtol=0.001); only in EES: 3; only in
> CoolSolve: 1

- The 17 variables flagged **DIFF** are exactly the absolute `h[i]`,
  `h_2_is`, `h_5_is`, `h_6_is` and `s[i]`: EES ideal-gas `Air` and CoolProp
  `Air` have different reference states, offsets of **+125.9 to +126.2
  kJ/kg** on `h` and **−1814 J/kg·K** on `s`, constant over all ten states
  (documented in CoolSolve `docs/ees_import.md` §11). Their **differences**
  agree to **6.7e-04** (worst `h`) and **1.9e-03** (worst `s[3]−s[7]`).
- All 25 derived variables (pressures, temperatures, powers, heat rates)
  agree within **9.3e-04** (worst `T[2]`, 176.54 → 176.38 °C), i.e. within
  the different-property-backend tolerance; the residuals grow with the
  temperature span of each process, as expected from the slightly different
  air cp of the two backends.
- `Only in EES reference: n, P_1, R`: three leftover entries of the EES
  variable list that appear in no equation of the window (dropped from the
  `.initials`); `fluid$` exists only in CoolSolve's solution listing.
- Energy balances: the model equations themselves enforce the HP-shaft
  balance (`W_dot_thp + W_dot_cmp = 0`, −153 205 W both sides) and the
  regenerator balance (`Q_dot_regen_reel_gaz = −359 243 W` =
  `−Q_dot_regen_reel_air`); the computed values satisfy them.

## Source and attribution

Exercise solution of the ULiège course *Thermodynamique appliquée*
(THD10), repetition 5, exercise 4 (2010). No author is named in the file;
the EES licence stamp is a student/staff licence of the ULiège
Thermodynamics Laboratory, and the sources/thermo_models inventory credits
S. Bertagnolio and S. Borguet for the 2010 THD exercise sets.

Source file (EES X8.423, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2017-2018/THD10_R05.zip!/THD10_R05_E4.EES`
(inventory candidate `TM-0518`).

## Niche

Nearest models of the library: `CSL-0050`
*gas_turbine_two_shaft_intercooled_regenerative* (same course family,
2022 session: two compression stages with intercooler **and a second
combustion chamber** around its regenerator, fuel and alternator,
sequential station-by-station sizing) and `CSL-0060`
*gas_turbine_reheat* (two compression stages, regenerator and reheat,
polytropic efficiencies). This model is the **minimal regenerative
two-shaft machine** of the family: single compression stage, one
combustion chamber, HP turbine on the compressor shaft and LP turbine on
the load shaft, no intercooler and no reheat — a different (simpler)
topology and level of detail than CSL-0050/CSL-0060, verified against its
own EES stored solution. `CSL-0011` and `CSL-0293` are two-shaft machines
without regenerator, focused on off-design compressor/expander maps.

## Conversion log

- **2026-10-24 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system `SI MASS DEG KPA C KJ` + decimal comma (converted by the
  extractor) → hand conversion to SI-°C-Pa-J: `p[1] = 100E3` and
  `p[2] = 400E3` (100/400 kPa in the original); the stored `p[3]…p[7]`,
  `h`, `s`, `W`, `Q` values in the `.initials` were multiplied by 1000. All
  remaining equations are homogeneous (efficiency ratios, `q_m·Δh`
  products with `q_m` in kg/s) and needed no change. `T[4] = 1150 − 273`
  is kept exactly as written in the original (877 °C, the original
  subtracts 273, not 273.15). Comments translated to English (paraphrase);
  standard header added; no equation of the original changed. Fluid `air`
  (lowercase, as in the original) is the ideal-gas `Air`.
- **Level**: score of taxonomy.md §3 — equations 43 (< 50) = 0; largest
  block 1 = 0; functions/arrays = 0; ≥ 3 coupled components (compressor,
  regenerator, combustion chamber, two turbines) = 1; semi-empirical /
  off-design = 0; curated guesses (converges from defaults) = 0 → score 1,
  moved +1 to **level 2**: a complete regenerative two-shaft plant, at the
  level of the sibling THD10 cycle models.

## Limitations and CoolSolve gaps

- Combustion products are treated as air (hypothesis of the original); no
  fuel flow, no air-fuel ratio, so no cycle efficiency is computed — the
  outputs are the station states and the three powers of the statement.
- The regenerator is isobaric on both sides (hypothesis of the original).
- No CoolSolve gap blocks the model (`missing_features` empty).

## Related models

- `CSL-0050` *gas_turbine_two_shaft_intercooled_regenerative*: same
  course family, richer two-shaft machine (intercooler, second combustion
  chamber, fuel and alternator) of the 2022 session.
- `CSL-0060` *gas_turbine_reheat*: intercooler + regenerator + reheat,
  polytropic efficiencies.
- `CSL-0011` *two_shaft_gas_turbine_compressor_map* and `CSL-0293`
  *two_shaft_gas_turbine_expander_map*: two-shaft machines at nominal and
  reduced regime, without regenerator, driven by compressor/expander maps.
