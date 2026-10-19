# Centrifugal compressor with a lookup-table performance map (air)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0035`

Constant-speed centrifugal air compressor characterised by a measured
performance map: the reduced mass flow rate `M_dot·sqrt(T1)/p1` and the
isentropic efficiency are read by interpolation from a three-point lookup
table as functions of the pressure ratio; the model returns the air mass
flow rate and the absorbed power.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air |
| **Size** | 14 equations (largest block: 1) |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 4 (2004-10-12), exercise 6 (EES file `MSTH_041012_exercice_8.EES`) |
| **Authors** | TBD (ULiège MSTh course — *Machines et systèmes thermiques*; course team J. Lebrun, V. Lemort, S. Bertagnolio; individual author not identified) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@4798e2b — verified against the EES stored solution (see *Verification*) |

## Problem statement

As in the original (translated): for a constant-speed centrifugal air
compressor the following performance map data is available (temperatures in
K, pressures in bar):

| p2/p1 | M·sqrt(T1)/p1 | eta_s |
|---|---|---|
| 5.0 | 32.9 | 0.86 |
| 4.7 | 33.8 | 0.79 |
| 4.5 | 34.3 | 0.77 |

Determine the variation of the air flow rate and of the power absorbed by
this compressor for: inlet pressure 0.9 bar, discharge pressure variable
from 4.3 to 4.8 bar, inlet temperature constant at 20 °C.

## Model

- Reduced (map) quantities, with the pressures in bar as in the map:
  pressure ratio `r_p = p_ex/p_su`, reduced mass flow
  `M_r = M_dot·sqrt(t_su+273)/p_su` [kg/s-K^0.5/bar].
- Both `M_r` and the isentropic efficiency `epsilon_s` are interpolated from
  the map (`lookup_1`) at `r_p`; the system is closed by the map definition
  of `M_r` (two coupled equations).
- Isentropic compression: `w_s = h(p_ex, s_su) − h_su`; absorbed power
  `W_dot = M_dot·w_s/epsilon_s`.

| Inputs (default run) | Value | Outputs (default run, r_p = 5.0) | Value |
|---|---|---|---|
| `p_su` suction pressure | 0.9 bar | `M_dot` air mass flow rate | 1.7298 kg/s |
| `t_su` suction temperature | 20 °C | `W_dot` absorbed power | 345.80 kW |
| `p_ex` discharge pressure | 4.5 bar | `epsilon_s` isentropic efficiency | 0.86 (map node) |
| | | `w_s` isentropic specific work | 171.92 kJ/kg |
| | | `M_r` reduced mass flow | 32.9 (map node) |

In the original, `p_ex` is given by a parametric table (sweep 4.3 to
5.4 bar, see *Conversion log*); the library file fixes the default run at
4.5 bar (a map node, as the exercise range 4.3–4.8 bar → r_p = 4.78–5.33
mostly lies at or beyond the last map node r_p = 5.0).

## How to run

```bash
coolsolve ./centrifugal_compressor_lookup_map.eescode
```

The file is the native EES model (the `INTERPOLATE` call form with the named input column). No `.initials` is needed (the equations
solve sequentially). Lookup table: `centrifugal_compressor_lookup_map-lookup_1.csv`.

## Results

Default run (r_p = 5.0, a map node): `M_dot` = 1.7298 kg/s, `W_dot` =
345.80 kW, `epsilon_s` = 0.86, `M_r` = 32.9, `w_s` = 171.92 kJ/kg.

EES stored solution point (`p_ex` = 5.4 bar, r_p = 6, the last run saved in the file; set `p_ex = 5.4E5`): `epsilon_s` = 1.0933 and `M_r` = 29.9 (linear
extrapolation of the map beyond its last node, as in EES), `M_dot` = 1.5721 kg/s, `W_dot` = 283.01 kW (EES: 282.74 kW); see *Verification*.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep plot
      (M_dot and W_dot vs p_ex over the exercise range 4.3–4.8 bar), saved in figures/ -->

## Verification

Reference: the **EES stored solution** of the original file (TM-0061, EES 7.210, 12 variables — internally consistent run at `p_ex` = 5.4 bar, r_p = 6.0; the
extractor's "stored values equal the guesses" warning is refuted by the energy balances, which close to 7 digits). The native file is solved with `p_ex = 5.4E5`
(reference pressures converted bar → Pa by hand: EES stored no units) and compared with the stored values:

| Group | Variables | rel. diff | Explanation |
|---|---|---|---|
| exact | `p_su`, `p_ex`, `r_p`, `t_su` | 0 | — |
| map (extrapolated) | `epsilon_s` (1.093333), `M_r` (29.9), `M_dot` (1.572099) | ≤ 3e-9 | EES `INTERPOLATE` extrapolates linearly beyond the table ends and so does CoolSolve |
| property model | `w_s` (196 824 vs 196 636 J/kg), `W_dot` (283 013 vs 282 742 W) | 9.6e-04 | EES 7 vs CoolProp `Air` (different equations of state, ≤ 0.5 %); with the EES `w_s` the stored `W_dot` follows exactly |
| reference-state offset | `h_su` (+125.87 kJ/kg), `h_exs` (+126.06 kJ/kg), `s_su` (−1814.8 J/kg-K) | ~0.2–0.3 | constant EES-7-vs-CoolProp `Air` offsets (as documented for `CSL-0020`/`CSL-0023`); the 188 J/kg spread between the two `h` offsets is exactly the 9.6e-04 relative `w_s` deviation |

Within the map range (4.5 ≤ r_p ≤ 5.0) the interpolation is exact at the nodes (default run) and linear between them (checked at r_p = 4.85: `epsilon_s` = 0.825,
`M_r` = 33.35). The equation `M_r = M_dot·sqrt(t_su+273)/p_su` keeps the 273 of the original: the stored `M_dot` (1.572098986 kg/s at `M_r` = 29.9) reproduces `29.9·0.9/sqrt(293)`
to 10 digits.

The **parametric table** of the original (127×2, columns `W_dot`, `M_r`) could **not** be used as reference: the map it was computed with is lost (external `.lkt` file,
not in the collection), and its 50 non-empty `W_dot` values are inconsistent with the map published in the exercise statement (e.g. its first row has the node values
`M_r` = 32.9, `epsilon_s` = 0.86 — hence r_p = 5.0, `M_dot` = 1.7298 kg/s — but `W_dot` = 371 309 W, which would require `w_s` = 184.7 kJ/kg, i.e. 7.4 % more than the isentropic
enthalpy drop at r_p = 5.0). The table is most likely a leftover of earlier runs with other map data; the last of its solved rows (row 50, `W_dot` = 282 742.2534 W) matches the
stored solution at 5.4 bar exactly.

## Source and attribution

Exercise of the ULiège course *Machines et systèmes thermiques*,
repetition 4 (2004-10-12), exercise 6 (the statement heading says
"exercice 6"; the file is `MSTH_041012_exercice_8.EES`, 8th file of the
series). The EES licence tag names the ULiège Thermodynamics Laboratory
(J. Lebrun), which identifies the laboratory but not the individual author.

Source file (EES 7.210, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 04/MSTH_041012_exercice_8.EES`
(inventory candidate `TM-0061`). No EES original exists in CoolSolve
`misc/EES_ok.zip` for this example. The CoolSolve example
(`examples/turbocompressor_interpolate.eescode`, CSX-045) is a transcription
of the same exercise and stays in the CoolSolve repository; the library
model follows the EES original.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES 7.210, unit system `SI MASS DEG BAR C J`, decimal comma converted to
  dots by the tool, `{$ID$ #202: Laboratoire de Thermodynamique, U. de
  Liege}` tag removed. Manual unit conversion to SI-°C-Pa-J
  ([ees_import.md §6](https://github.com/CoolProp/CoolSolve/blob/main/docs/ees_import.md)):
  `p_su = 0.9E5 [Pa]` (0.9 bar in the original) and `p_ex` likewise; since
  the map data (and therefore `r_p` and `M_r`) is defined with the
  pressures **in bar**, local variables `p_su_bar`/`p_ex_bar` [bar] feed
  `r_p` and `M_r` (§6.2 step 4: correlations fitted in the original units);
  all property calls now take Pa directly. Computed values are unchanged
  (`r_p`, `M_r` identical to the original; `W_dot`, `M_dot` unchanged).
- **2026-10-05 — inputs restored**: `p_ex` is commented out in the original
  (given by the parametric table, 127 rows sweeping `W_dot`/`M_r`; sweep
  values not stored). Default run set at `p_ex` = 4.5 bar (map node, value
  of the CoolSolve example; the stored EES run was 5.4 bar). The commented
  alternatives of the original (`"p_ex=4.5"`, `"epsilon_s=0.79 / M_r=33"`,
  a constant-efficiency solution without the map) are kept as comments,
  as in the original.
- **2026-10-05 — lookup table recovered from the exercise statement**: the
  map `lookup 1` was an **external** file (`*.lkt`) lost with the original
  collection; the three map nodes are however published in the file's own
  problem-statement comment and reproduced exactly by the stored solution
  (linear extrapolation check, see *Verification*). They are shipped as the
  companion table `<name>-lookup_1.csv`, in ascending `r_p` order (4.5,
  4.7, 5.0 — EES accepts both orders; ascending avoids `CS-BUG-INTERP-DESC`
  on v0.3.0 builds); table name renamed `'lookup 1'` → `'lookup_1'`
  (companion-CSV convention, references updated).
- **2026-10-05 — note on `sqrt(t_su+273)`**: the equation is kept exactly as
  in the file (273, not 273.15). The stored `M_dot` (1.572098986 kg/s at
  `M_r` = 29.9) reproduces `29.9·0.9/sqrt(293)` to 10 digits (C-38 check:
  `sqrt(293.15)` would give 1.57170, 0.026 % lower), so the stored run uses
  the same equation as the file.
- **Level** (taxonomy.md §3): 14 equations (0) + largest block 1 (0) + no
  functions/arrays (0) + no multi-zone (0) + semi-empirical performance-map
  component (1) + no curated guesses needed (0) = score 1 → level 1, moved
  +1 → **level 2** as carded (applied-thermodynamics exercise introducing
  interpolation in measured compressor performance data).

## Limitations and CoolSolve gaps

- The map has three nodes and the exercise range (r_p = 4.78–5.33) lies at
  or beyond the last node: most of the sweep is extrapolation, which EES
  does linearly (efficiency > 1 possible, as the stored run shows). Physical
  validity is limited to the vicinity of the map.
- No CoolSolve gap blocks the model.

## Related models

- `CSL-0023` (centrifugal turbocompressor performance, air): same course
  and repetition (MSTh TP 04), velocity-triangle design model of the same
  compressor type; this model is its map-based off-design counterpart.
- `CSL-0011` (two-shaft gas turbine with compressor map): same native EES
  `INTERPOLATE` form and map-based modelling on air.
- CoolSolve example `turbocompressor_interpolate.eescode` (CSX-045): same
  exercise, kept in CoolSolve as a test case (differs from the EES original:
  `p_ex` imposed at 4.5 bar, map data in comments only).
- `CSL-0069` (centrifugal compressor design and similarity, air): same
  component and same course and repetition (MSTh TP 04), sized from the flow
  and enthalpy factors of its best-performance point rather than from a
  measured map.
- `CSL-0157` *reciprocating_catalogue_r717*: catalogue rows in a companion
  lookup table turned into effectiveness maps for an R717 reciprocating
  compressor.
