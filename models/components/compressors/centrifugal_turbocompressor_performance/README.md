# Centrifugal turbocompressor performance (air)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0023`

Air flow rate drawn by a centrifugal turbocompressor (impeller + vaneless
diffuser) modelled at constant isentropic efficiencies: velocity triangles
at the impeller outlet, Euler turbine equation, pressure recovery in the
diffuser. The model solves the nominal operating point; raising the
discharge pressure drives the flow towards the theoretical maximum pressure
ratio (solved at M_dot → 0 in the corrected original).

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Air |
| **Size** | 32 equations (largest block: 9) |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 4 (2004-10-12), exercise 2 (EES file `MSTH_041012_exercice_2_corrigé.EES`) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory, course *Machines et systèmes thermiques*, repetition of 2004-10-12, exercise 2; author not identified) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — verified against the EES stored solution (see *Verification*) |

## Problem statement

Evaluate the air flow rate drawn by a centrifugal turbocompressor under the
following conditions: impeller diameter 7 cm, peripheral blade width 1 cm,
blade outlet angle 130°, suction temperature and pressure 20 °C and 1 bar,
discharge pressure 1.5 bar, rotation speed 100 000 rpm (impeller isentropic
efficiency 0.85, diffuser efficiency 0.75).

## Model

- **Impeller** (subscript 2 = impeller outlet): outlet area
  `A_2 = π·D_2·e`, flow `V_dot_2 = A_2·W_2·sin(β_2)`,
  `M_dot = V_dot_2/v_2`; Euler equation
  `w = U_2² + U_2·W_2·cos(β_2)` with `U_2 = π·D_2·N`; total enthalpy
  `h_t_2 = h_2 + C_2²/2`; impeller pressure ratio `r_p_i = p_2/p_1`.
- **Losses** at constant efficiencies: impeller
  `h_2s + C_2²/2 − h_1 = ε_s_i·w`, adiabatic diffuser
  `h_3s − h_2 = ε_s_d·C_2²/2` with `h_3 = h_2 + C_2²/2` (outlet kinetic
  energy recovered as enthalpy).
- Overall pressure ratio `r_p = p_3/p_1` with `p_3 = p_ex`.

| Inputs | Value | Outputs (nominal point) | Value |
|---|---|---|---|
| `D_2` impeller diameter | 0.07 m | `M_dot` air flow rate | 0.666 kg/s |
| `e` peripheral blade width | 0.01 m | `w` specific work | 56.53 kJ/kg |
| `beta_2` blade outlet angle | 130° | `r_p_i` impeller pressure ratio | 1.050 |
| `t_su` / `p_su` | 20 °C / 1 bar | `r_p` overall pressure ratio | 1.500 |
| `p_ex` discharge pressure | 1.5 bar | `C_2` absolute outlet velocity | 296.3 m/s |
| `rpm` | 100 000 | `U_2` blade tip speed | 366.5 m/s |
| `epsilon_s_i` / `epsilon_s_d` | 0.85 / 0.75 | `V_dot_2` outlet volume flow | 0.556 m³/s |

## How to run

Open `centrifugal_turbocompressor_performance.eescode` in the CoolSolve GUI
and press *Solve*, or from a terminal:

```bash
coolsolve ./centrifugal_turbocompressor_performance.eescode
```

The `.initials` file (CoolProp-consistent guesses, see *Conversion log*) is
required: the Newton solver alone fails on the 9-variable implicit block
without initial values (as noted in the CoolSolve example). To reproduce the
maximum-pressure-ratio sweep of the corrected original, raise `p_ex`
towards 3 bar (the flow then vanishes).

## Results

| Quantity | EES (nominal point) | CoolSolve | rel. diff. |
|---|---:|---:|---:|
| `M_dot` [kg/s] | 0.66593 | 0.66601 | 0.013 % |
| `w` [J/kg] | 56 527 | 56 531 | 0.007 % |
| `p_2` [Pa] | 105 021 | 105 024 | 0.003 % |
| `v_2` [m³/kg] | 0.83549 | 0.83534 | 0.018 % |
| `r_p_i` [-] | 1.05021 | 1.05024 | 0.003 % |
| `W_2` / `C_2` [m/s] | 330.27 / 296.30 | 330.25 / 296.30 | ≤ 0.005 % |
| `V_dot_2` [m³/s] | 0.55637 | 0.55635 | 0.005 % |
| `h_1`, `h_2`, `h_2s`, `h_3`, `h_3s`, `h_t_2` | — | — | constant reference offset (see *Verification*) |
| `s_1`, `s_2` | — | — | constant reference offset (see *Verification*) |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): velocity-triangle
      sketch or parametric sweep plot (M_dot vs p_ex towards the maximum pressure
      ratio), saved in figures/ -->

## Verification

Vs the EES stored solution of TM-0055 (`MSTH_041012_exercice_2.EES`,
EES 7.210 — same 32 equations as the imported corrigé TM-0056, solved at
the nominal point with all 33 stored values present): 24 of 32 comparable
variables agree within 0.1 % (largest: `v_2` 0.018 %, `M_dot` 0.013 %).
The 8 remaining deviations are the absolute enthalpies and entropies,
shifted by the difference between the EES 7 and CoolProp `Air` reference
states — a constant offset, not a physics deviation:

| Quantity | EES | CoolSolve | offset |
|---|---:|---:|---|
| `h_1` / `h_2` / `h_2s` / `h_3` / `h_3s` | 293 534 / 306 164 / 297 685 / 350 062 / 339 087 J/kg | +125 871 … +125 876 J/kg | +125.87 kJ/kg (spread 5 J/kg) |
| `s_1` / `s_2` | 5 682.13 / 5 710.25 J/kg-K | 3 867.26 / 3 895.39 J/kg-K | −1 814.9 J/kg-K (spread 0.01) |

All energy differences agree (`w = h_t_2 − h_1`: 56 527 vs 56 531 J/kg,
i.e. 0.007 %), within the tolerances for different equations of state
(CoolSolve `docs/ees_import.md` §11; same EES-vs-CoolProp `Air` offset as
documented for `CSL-0020`).

## Source and attribution

Exercise of the ULiège course *Machines et systèmes thermiques*
(repetition 4 of 2004-10-12, exercise 2; EES files `20041012_Exercice_2.EES`,
`MSTH_041012_exercice_1/2.EES` and the corrected version
`MSTH_041012_exercice_2_corrigé.EES`). The EES licence tags name the ULiège
Thermodynamics Laboratory (J. Lebrun), which identifies the laboratory but
not necessarily the individual author. Transcribed equation-for-equation
into the CoolSolve example by **S. Quoilin** (see *Conversion log* for the
differences).

Source file (EES 7.210, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 04/MSTH_041012_exercice_2_corrigé.EES`
(inventory candidate `TM-0056`, representative of duplicate group `DG-0013`).
No EES original exists in CoolSolve `misc/EES_ok.zip` for this example. The
CoolSolve example (`examples/turbocompressor.eescode`, CSX-044) is kept in
the CoolSolve repository as a test case.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already SI-°C-Pa-J, no conversion needed; the EES licence tag
  was removed; no lookup or parametric tables; no external functions.
  Representative TM-0056 imported; its commented-out discharge pressure
  (`"p_ex=1.5E5"`, swept towards higher pressure ratios in the original)
  restored as `p_ex = 1.5E5` (default run), which makes the equations
  identical to the nominal-point variants TM-0054/TM-0055. Comments
  translated to English, standard header added, SI units added to the
  trailing comments, the embedded EES solution printout removed (the
  reference values live in the inventory enrichment and in *Verification*
  above). No equation changed otherwise.
- **2026-10-05 — curated `.initials`** (workflow §3, step 5): the EES stored
  absolute enthalpies/entropies use the EES 7 `Air` reference state and make
  CoolSolve's Newton solver fail with NaN Jacobian entries (verified in the
  debug folder: `SingularJacobian` on the 9-variable block from the raw EES
  guesses). Guesses curated to the CoolProp reference state
  (`h_*` +125.87 kJ/kg, `s_*` −1814.9 J/kg-K, from the CoolSolve example's
  `.initials` at the same point, `r_p_i` set to the computed 1.0502);
  all other guesses are the EES stored values. With these, Newton converges
  in 2 iterations; the solution is the EES nominal point (see
  *Verification*).
- **2026-10-05 — differences vs the CoolSolve example** (CSX-044, kept in
  CoolSolve; model follows the EES original): the example was transcribed
  equation-for-equation from TM-0055 except that it comments out
  `r_p_i = p_2/p_1` (`//r_p_i=...`) and imposes `r_p_i = 1.25`
  ("provisional estimate, without diffuser" made permanent), so its
  equations no longer determine the impeller pressure ratio from the
  compression — and its embedded "Solution:" printout (`p_2 = 105021`,
  `r_p_i = 1.05`) is the EES original's, not the variant's. Impact on the
  library model: none (native `r_p_i = p_2/p_1` kept). The maintainer may
  want to align the example with the original (restore `r_p_i = p_2/p_1`,
  comment out `r_p_i = 1.25`) or document the imposed-ratio variant.
- **Level 2** (taxonomy.md §3): 32 equations (0) + largest block 9 (1) +
  imposed-efficiency (semi-empirical) component physics (1) + curated
  guesses required (1) = 3 → Intermediate.

## Limitations and CoolSolve gaps

- Very coarse model (as the original itself states): constant impeller and
  diffuser efficiencies, no surge/choking modelling, no slip factor. Below a
  certain pressure ratio the sonic regime is reached; solving for `r_p` as
  a function of `M_dot` can give two theoretical solutions (both remarks as
  in the original).
- No CoolSolve gap blocks this model. The `enthalpy(): fluid 'air'` hint
  (suggesting `AirH2O` for moist air) is spurious here — dry-air ideal-gas
  properties are intended.

## Related models

- `CSL-0020` (dry-air screw compressor with internal leakage): same fluid
  (`Air`) with the same EES-7-vs-CoolProp reference-state offset on `h`
  and `s`.
- CoolSolve example `turbocompressor.eescode` (CSX-044): same exercise,
  kept in CoolSolve as a test case (imposed-`r_p_i` transcription — see
  *Conversion log*).
- `thermo_models` TM-0066 (`MSTh-SB-R4-Ex3.EES`, SB impeller + adiabatic
  diffuser on air): same physics, different exercise — candidate for a
  future related model (left `todo`).
