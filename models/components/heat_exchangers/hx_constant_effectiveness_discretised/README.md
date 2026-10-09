# Discretised constant-effectiveness heat exchanger with a minimum pinch (sCO2 recuperator)

🔴 **Level 4 · Research** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0127`

A counterflow heat exchanger split into `n_disc` equal-enthalpy segments, whose duty
`Q_dot = epsilon*Q_dot_max` is limited three times: by an external (ideal-outlet)
maximum heat, by an internal zero-pinch limit, and by a minimum temperature
difference `Pinch_min` that must hold at *every* segment — the pinch-limited
effectiveness model of LaboThapPy used for sCO₂ recuperators and gas coolers,
where the near-critical specific-heat variation makes interior segments pinch
first. The Python effectiveness loops (1 % decrements) and the internal
bisection are recast as simultaneous equations closed by two min-based
complementarity conditions.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | R744 (CO₂, both sides), Water (variant) |
| **Size** | 329 equations, largest block 128 (main file, `n_disc` = 20); the gas-cooler variant has 1449 equations, largest block 608 (`n_disc` = 100) |
| **Source** | [LaboThapPy](https://github.com/PyLaboThap/LaboThapPy) component `HexCstEffDisc`, commit `f03f7f47` |
| **Authors** | Basile Chaudoir, Elise Neven (ULiège Thermodynamics Laboratory) |
| **License** | MIT (this library); original code Apache-2.0/MIT (dual declaration, see below) |
| **CoolSolve** | v0.3.0 — verified against the original Python example (see *Verification*) |

## Problem statement

Given both inlet states (fluid, temperature, pressure, mass flow), the pressure
drops `DP_h`/`DP_c`, a user maximum effectiveness `eta_max`, a number of
segments `n_disc` and a minimum temperature difference `Pinch_min`, find the
heat duty, the effectiveness finally used, the outlet states and the
temperature profiles. The model is the design/off-design building block for
transcritical CO₂ cycles: the source ships it as the recuperator (`RecupHT`
case, CO₂/CO₂) and as a gas cooler (`GasCooler` case, CO₂/water) of its
example `hex_csteff_disc_example.py`.

## Model

Per segment (equal enthalpy steps, so the profiles are linear in the segment
index; counterflow, index *i* counted from the hot-inlet end, pressure drops
equally distributed as in the original):

- `h_hot[i] = h_su_H - (i-1)*Q_dot/(n_disc*M_dot_H)`,
  `h_cold[i] = h_su_C + Q_dot/M_dot_C - (i-1)*Q_dot/(n_disc*M_dot_C)`,
  temperatures from `(h, P)` (real-fluid property calls), `DT[i] = T_hot[i] - T_cold[i]`;
- `DT_pinch = min_i DT[i]` (cascade of two-argument `MIN`s);
- external limit: `Q_max_ext = min(M_dot_H*(h_su_H - h_H_id), M_dot_C*(h_C_id - h_su_C))`
  with the ideal outlet enthalpies `h_H_id` (hot cooled to the cold inlet
  temperature) and `h_C_id` (cold heated to the hot inlet temperature), as in
  `find_Q_dot_max` of the original;
- internal limit: the same profile equations at the unknown `Q_dot_max`,
  whose minimum difference `DT2_pinch` closes
  `Q_dot_max = min(Q_max_ext, Q_dot_max)` — the zero-pinch "fictive
  effectiveness" search of the original (its 1e-3 bisection) becomes the
  complementarity `MIN(Q_max_ext - Q_dot_max, DT2_pinch) = 0`;
- final selection: the 1 % effectiveness loop of the original
  (`epsilon = eta_max`, `while DT_pinch <= Pinch_min: epsilon -= 0.01`)
  becomes the complementarity
  `MIN(DT_pinch - Pinch_min, eta_max*Q_dot_max - Q_dot) = 0`:
  the duty is the smaller of the heat whose minimum segment difference equals
  `Pinch_min` and of the `eta_max` share of `Q_dot_max`; `epsilon = Q_dot/Q_dot_max`.

Both complementarities have a unique solution because both `MIN` arguments
decrease with the duty. The `MIN`/`MAX` cascade is exactly the "smooth min"
recasting suggested in the task card; no `IF` on the active segment is needed.
The degenerate-input branches of the Python `solve()` (`T_su_H <= T_su_C` or
zero flow → `Q_dot = 0`) are solver plumbing, not equations, and are not
translated: the model is valid for `T_su_H > T_su_C` and non-zero flows, as in
both examples.

| Inputs | Main file (`RecupHT`) | Variant (`gascooler`) |
|---|---|---|
| `fluid_H$` / `fluid_C$` | R744 / R744 | R744 / Water |
| `T_su_H` / `T_su_C` | 52.254 / 34.605 °C | 176.85 / 15 °C |
| `P_su_H` / `P_su_C` | 150 / 39.916 bar | 180 / 10 bar |
| `M_dot_H` / `M_dot_C` | 30 / 30 kg/s | 0.16 / 0.1 kg/s |
| `eta_max` / `Pinch_min` | 0.95 / 0 K | 0.95 / 10 K |
| `n_disc` | 20 | 100 |
| `DP_h` / `DP_c` | 0 / 0 Pa | 50 000 / 50 000 Pa |

## How to run

```bash
coolsolve ./hx_constant_effectiveness_discretised.eescode
coolsolve ./hx_constant_effectiveness_discretised_gascooler.eescode   # variant
```

the `.initials` files hold the segment profiles of the reference solution
(near-critical property calls need them); `coolsolve.conf` raises
`maxIterations` to 500 and relaxes `tolerance` to 1e-6: at the GasCooler
solution the internal zero-pinch limit sits a few hundredths of a percent
below the external one, the zero-pinch profiles touch tangentially and Newton
stagnates at a residual of 1.4e-7 — physically negligible (duties are ~5e4 W).
The main file converges to the default tolerance as well; the shared
`coolsolve.conf` applies to both files of the folder.

## Results

| Quantity | RecupHT: Python example / CoolSolve | GasCooler: Python example / CoolSolve |
|---|---|---|
| `Q_dot` [W] | 618 759.40 / 619 438.94 | 51 734.63 / 52 264.40 |
| `Q_dot_max` [W] | 651 325.69 / 652 040.99 | 55 628.63 / 55 679.71 |
| `epsilon` [-] | 0.95 / 0.95 | 0.93 / 0.9387 |
| `DT_pinch` [K] | 0.9356 / 0.9183 | 11.5006 / **10.000 000** |
| `T_ex_C` [°C] | 51.318 / 51.336 | 138.070 / 139.308 |
| `T_ex_H` [°C] | 45.384 / 45.373 | 26.512 / 25.000 |

The GasCooler pinch is exactly `Pinch_min` (self-check of the card); its active
difference sits at the cold end and a near-tied interior segment (in the
Python run at ε = 0.93 the interior segment is the active one, 11.5006 K vs
11.5120 K at the end). The arrays `T_hot[i]`, `T_cold[i]`, `DT[i]` (`i` = 1…
`n_disc`+1 from the hot-inlet end) give the temperature profiles.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): temperature profiles
     T_hot[i]/T_cold[i] vs i (array plot of the main file or of the variant) -->

## Verification

The source's own example (`labothappy/component/examples/heat_exchanger/
hex_csteff_disc_example.py`, both case studies, commit `f03f7f47`) was re-run
in a throw-away virtual environment (CoolProp 8.0.0, the local LaboThapPy
clone) with a driver that copies its inputs verbatim and prints the results;
`compare_c172.py` compared the printed values with the CoolSolve `.sol`
baselines (table above, `work/` deleted after the card). Deviations, by cause:

1. **1 % effectiveness steps of the original** (GasCooler `Q_dot` +1.02 %,
   `epsilon` 0.93 vs 0.9387, `DT_pinch` 11.50 vs 10.00 K): the original stops
   at the last 1 % step whose pinch clears `Pinch_min`, so its result lies
   within one step (ΔQ = 530 W < one step = 557 W) above the continuous
   solution; the CoolSolve model enforces `min_i DT[i] = Pinch_min` exactly,
   as the task card specifies.
2. **Bisection tolerance of the original** (both cases, `Q_dot_max` +0.09 to
   +0.11 %): `find_Q_dot_max` bisects until |Δη| < 1e-3 and returns the lower
   bracket, so its `Q_dot_max` underestimates the exact zero-pinch heat
   (651 325.7 vs 651 973.6 W in the RecupHT case).
3. **Property backend** (~0.01–0.02 %): the original evaluates states with
   CoolProp `BICUBIC&HEOS` tables, CoolSolve uses HEOS.

A tightened reference (same profiles, exact zero-pinch root by `brentq`)
confirms the translation: `Q_dot` agrees to +0.012 % (RecupHT) and +0.015 %
(GasCooler) — the property backend alone — and `DT_pinch` to 7.6e-5 K
(RecupHT) and 0.0 K (GasCooler). `max_rel_diff` against the source example,
1.33 % (`h_ex_H`, GasCooler), is the `Q_dot` difference of item 1 propagated
by the energy balance.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of `HexCstEffDisc` from LaboThapPy, file
`labothappy/component/heat_exchanger/hex_csteff_disc.py`, commit `f03f7f47`.
LaboThapPy — <https://github.com/PyLaboThap/LaboThapPy>
Copyright (C) 2025 Université catholique de Louvain (UCLouvain), Université de
Liège (ULiège), Université de Mons (UMONS). Original authors: E. Neven,
B. Chaudoir et al. (see AUTHORS.txt; git history of the file: B. Chaudoir,
E. Neven).
Changes: translated from Python to CoolSolve; the effectiveness decrement loop
and the zero-pinch bisection replaced by simultaneous equations (min-based
complementarities); discretisation loops as `DUPLICATE` arrays; property calls
`AbstractState('BICUBIC&HEOS')` → CoolSolve property functions. The example
inputs, the model equations and the documentation page
(`docs/source/documentation/component/heat_exchanger/heat_exchanger_models/hex_csteff_disc.rst`)
of the original were used as the model description. Scientific basis: none
cited in the source (internal LaboThapPy model description).

Local source clone: `~/git/LaboThapPy` (commit `f03f7f47`); inventory candidate
`LTP-012` (`sources/labothappy/inventory.csv`).

## Conversion log

- **2026-10-09 — translation** (`T-TRANSLATE`): equations as described under
  *Model*; the two `MIN` complementarities replace the Python loops
  (`counterflow_discretized` is reproduced equation by equation, including its
  array directions: `h_cold[1]` is the cold *outlet* at the hot-inlet end, as
  in the original). Fluid names: CoolProp `'CO2'` → EES `R744` (bare `CO2`
  would be the ideal-gas species); temperatures converted K → °C.
- **2026-10-09 — cold-side pressure pairing**: the original evaluates each
  cold-side temperature at a pressure counted from the *opposite* end of the
  exchanger (`p_cold[j]` paired with the enthalpy of position n−j — an index
  mismatch in `counterflow_discretized`); here every enthalpy is paired with
  the pressure at the same flow position. Impact on the GasCooler case
  (liquid water, `DP_c` = 50 kPa): v·ΔP/c_p ≈ 0.012 K on the cold profile,
  i.e. ≪ the property-backend difference; zero for the main file (`DP_c` = 0).
- **2026-10-09 — CoolSolve language workarounds** (native files stay valid EES):
  with `DUPLICATE i=1,N` an index expression such as `h[i+1]` is not folded
  (`CS-BUG-DUPLICATE-INDEX-EXPR`); the equal-enthalpy-step profiles are
  therefore written in closed form (linear in the segment index, identical
  equations) and the `MIN` cascades are unrolled. `DUPLICATE` bounds are
  literals (`CS-BUG-DUPLICATE-VAR-BOUND`). These IDs are listed in
  `missing_features` as the workarounds the native file uses (convention of
  `CSL-0129`); **no gap blocks the model**.
- **2026-10-09 — solver settings**: `coolsolve.conf` (`maxIterations = 500`,
  `tolerance = 1e-6`) for the tangential zero-pinch contact of the GasCooler
  case (see *How to run*).
- **Level**: 329 equations (2 pts, 50–300 exceeded), largest block 128 (2 pts,
  > 30), `DUPLICATE` arrays (1), discretised (1), no semi-empirical physics
  (0), curated guesses + tuned `coolsolve.conf` (1) → score 7 → level 4
  (docs/taxonomy.md §3).

## Limitations and CoolSolve gaps

- No CoolSolve gap blocks the model; `missing_features` lists
  `CS-BUG-DUPLICATE-INDEX-EXPR` because the native file works around it (see
  conversion log).
- Physics: no heat loss, equal enthalpy steps, pressure drops imposed (not
  correlated), counterflow only; the effectiveness is a pure input split
  (no UA/NTU calculation). Degenerate inputs (`T_su_H <= T_su_C`, zero flow)
  are out of scope (see *Model*).
- CoolSolve emits a spurious hint warning ("looks like Fahrenheit") on
  `T_su_C = 34.6` for R744; the value is used as Celsius, as the `.sol`
  confirms (warning only, not registered).

## Related models

- `CSL-0126` *hx_constant_effectiveness*: the same library's non-discretised
  constant-effectiveness HX (single `Q_dot_max`, no segment profiles, no pinch
  constraint) — the simpler sibling of this model.
- `CSL-0014` *hx_constant_pinch*: the LaboThapPy constant-pinch
  condenser/evaporator (three moving-boundary zones instead of equal enthalpy
  segments; pinch enforced at the zone interfaces only).
- `CSL-0090` *hx_effectiveness_ntu*: the ε-NTU alternative, where the
  effectiveness follows from UA instead of being imposed and pinch-limited.
- `CSL-0115` *hx_fem_evaporator_discretised*: the other discretised HX of the
  library (finite-volume cells, UA-based, procedure-driven).
- CSL-0138 (hx_moving_boundary_bell): moving-boundary (Bell 2015) translation of the same zone-delimited heat-exchanger family (TESPy TSP-014).
