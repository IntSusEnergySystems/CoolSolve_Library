# Ice storage tank discharge with phase change

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0041`

A 120 m³ water/ice thermal energy storage tank is discharged through a
glycol-water heat exchanger (90 kg/s of glycol at 5 °C, AU = 0.5 MW/K, no
ambient losses). The specific internal energy of the contents is integrated
over time with `INTEGRAL`; phase-change logic built on EES 5-argument `IF`
functions tracks the ice fraction and the tank temperature through the three
regimes: subcooled ice, melting at 0 °C, liquid warming. This is the library's
second dynamic model and its example of an EES phase-change (latent heat)
storage model.

| | |
|---|---|
| **Category** | Components › Storage |
| **Fluids** | Water (property calls of the original at/below 0 °C, replaced by constants in the variant — see *Limitations*) |
| **Size** | 39 equations + 1 integral state, all explicit per time step (largest block: 1); 10-s tabulation over 50 000 s |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 6, exercise 4, solution by S. Bertagnolio (EES file `MSTh-SB-R6-Ex4.EES`) |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file **blocked** by `CS-GAP-IF5`, `CS-GAP-INTEGRAL-LIMITS`, `CS-BUG-WATER-NEAR-FREEZING`, `CS-BUG-INTEGRAL-TABLE-SEP`, `CS-BUG-INTEGRAL-MAXSTEPS` and `CS-BUG-INTEGRAL-TABLE-CASE`; the variant `ice_storage_tank_discharge_phase_change_coolsolve.eescode` runs and is verified against an EES stored solution (see *Verification*) |

## Problem statement

A 120 m³ water/ice storage tank, initially all ice at −0.01 °C, is discharged
through a glycol loop: 90 kg/s entering at 5 °C, glycol cp = 3800 J/kg·K,
overall heat-transfer coefficient AU = 0.5 MW/K, no heat loss to the ambient.
Compute the discharge power curve and the state of the tank (ice fraction,
temperature, internal energy) over 50 000 s (13.9 h).

## Model

The tank is a lumped water/ice mass `M = V_sto·1000` = 120 000 kg whose
specific internal energy `u` is the state variable:

- glycol-side heat rate (effectiveness-NTU, cold side):
  $\dot Q = \varepsilon\, \dot m\, c_p\,(T_{su} - T_w)$ with
  $\varepsilon = 1 - e^{-NTU}$, `NTU = AU/Ċ` = 1.462, ε = 0.768;
- state equation: $\Delta u = $ `INTEGRAL(u_dot, tau, tau_1, tau_2)`,
  $\Delta u = u - u_1$ with $u_1 = u_{ice,0}$;
- phase-change logic (EES 5-argument `IF(A,B,X,Y,Z)`):
  - `u_ice_0 = INTENERGY(Water, T=-0.01, P)` ≈ −333.45 kJ/kg (ice reference,
    liquid at melting point taken as `u_liq_0` = 0),
  - tank temperature `t_w`: t_ice_0 below u_ice_0, 0 °C while melting
    (`t_melt`), `t_liq` above 0,
  - ice fraction `x_ice`: 1 below u_ice_0, then
    `x_two_phase = u/(u_ice_0 - u_liq_0)`, 0 above,
  - mixture volume `v = x_ice·v_ice + (1-x_ice)·v_liq` from `VOLUME(Water,…)`
    at the ice/liquid reference temperatures.

The original EES file, this native file and the variant all use the same
equations; the variant only transcribes the blocked syntax (see the header of
each file and the *Conversion log*).

| Inputs | Value | Outputs |
|---|---|---|
| `V_sto` / `M_dot` | 120 m³ / 90 kg/s | `x_ice(τ)`, `u(τ)`, `T_w(τ)` trajectories |
| `AU` / `T_su` / `c_p` | 0.5 MW/K / 5 °C / 3800 J/kg·K | `Q_dot_br_sto(τ)` discharge power |
| `P` | 101 325 Pa | `DELTAU_sto` energy discharged [J] |
| `t_ice_0` / `t_liq_0` / `u_liq_0` | −0.01 / 0 °C / 0 J/kg | `t_melt`, `t_ice`, `t_liq`, `v` |

## How to run

The original file `ice_storage_tank_discharge_phase_change.eescode` keeps the
native EES syntax and does **not** run in CoolSolve v0.3.0 (see *Limitations
and CoolSolve gaps*). The runnable transcription is:

```bash
coolsolve ./ice_storage_tank_discharge_phase_change_coolsolve.eescode
```

(a few seconds; it needs `coolsolve.conf`, see `CS-BUG-INTEGRAL-MAXSTEPS`).
The trajectory is written every 10 s to
`ice_storage_tank_discharge_phase_change_coolsolve-integral.csv` (10 columns)
and shown in the GUI *Integral* tab.

## Results

| τ [ks] | 0 | 10 | 20 | 30 | 30.5 | 31 | 40 | 50 |
|---|---|---|---|---|---|---|---|---|
| `x_ice` [-] | 1 | 0.672 | 0.343 | 0.015 | 0 | 0 | 0 | 0 |
| `T_w` [°C] | −0.01 | 0 | 0 | 0 | 0.02 | 1.23 | 4.97 | 5.00 |
| `Q_dot_br_sto` [MW] | 1.316 | 1.314 | 1.314 | 1.314 | 1.309 | 0.99 | 0.009 | 0.048 |
| `u` [kJ/kg] | −333.5 | −224.0 | −114.5 | −5.0 | 0.07 | 5.2 | 20.8 | 20.93 |

The discharge power stays constant at 1.314 MW while the tank melts at 0 °C
(ε-NTU with a constant cold-side temperature): the ice melts linearly in
~30.5 ks (8.5 h), consuming 40.0 GJ. The liquid then warms towards the glycol
inlet temperature (first-order time constant `M·c_liq/(ε·M_dot·c_p)` ≈
1913 s), and the discharge power decays to zero. `v` rises from 0.001091
(ice) to 0.001000 m³/kg as the ice melts.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): x_ice, T_w and
     Q_dot_br_sto vs time from the Integral tab,
     figures/ice_storage_tank_discharge_phase_change_trajectory.png -->

## Verification

The stored solution of the source file itself is **cleared** (16 of 40 values
kept, all inputs/constants — the file was last run from a parametric table
that no longer exists). The EES reference used here is the **complete stored
solution of the sibling copy of the same exercise**
(`MSTH051024exercice4.EES`, thermo_models TM-0095: same equations with AU =
1 MW/K and P = 1 bar, different variable names; its 27 stored values include
the EES evaluation of the same near-freezing property call,
`u_ice_0` = −333 451.5211 J/kg). The runnable variant was re-run with those
inputs (temporary copy, `coolsolve` v0.3.0) and compared with
`compare_solution.py`:

- **19 common variables, 18 agree within 6.4·10⁻⁸**; the printed maximum is
  **5.23·10⁻³ on `u_dot`** (re-run at the C-46 review), excluded: at the final time `u_dot` =
  ε·Ċ·(5−T_w)/M ≈ 1.2·10⁻⁶ J/(kg·s) is proportional to 5 − T_w ≈ 4.3·10⁻⁷, a
  cancellation-limited residual of the last integration step — the states
  themselves agree to 2.5·10⁻¹⁰ on `u`, 3.5·10⁻¹⁰ on `T_w` and `t_melt`,
  6.33·10⁻⁸ on `u_ice_0`/`u_1` (rounding of the −333 451.5 constant), 6·10⁻⁸
  on `DELTAu`; ε, NTU, `x_melt` exact.
- This also verifies the phase-change `IF` logic and the `INTEGRAL`
  transcription against EES (EES evaluates `u_ice_0` on its Water substance,
  CoolSolve/CoolProp cannot: `CS-BUG-WATER-NEAR-FREEZING`).

For the shipped inputs (AU = 0.5 MW/K) no EES reference exists; the
trajectory was checked against the closed-form solution of the two phases:
constant 1.3137 MW while melting (melt complete at 30 460 s, tank energy
40.0 GJ), then `u(t) = 20 935·(1 − e^{−(t−30 460)/1913})` J/kg → final
`u` = 20 934.2 J/kg and `T_w` = 4.9998 °C, exactly the values of the
trajectory table.

## Source and attribution

Solution by **Stéphane Bertagnolio** (ULiège Thermodynamics Laboratory) for
the course *Machines et systèmes thermiques*, repetition 6, exercise 4
(file header "MSTh - SB - R6 - Exercice 4"; author identified from the `SB`
initials of the folder and file name, as for `CSL-0001`/`CSL-0022`).

Source file (EES 7.458, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 06/SB/MSTh-SB-R6-Ex4.EES`
(inventory candidate `TM-0104`). Sibling copies of the same exercise:
`TP 06/MSTH051024exercice4.EES` (TM-0095, with the EES stored solution used
above) and its TP 08 copy.

The CoolSolve example `ice_storage_tank.eescode` (CSX-023) is a CoolSolve
transcription of the same exercise with 3-argument `IF` and tabulated
constants; it stays in the CoolSolve repository and is superseded by this
model in the library.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`): unit system already
  `SI MASS DEG PA C J` (no conversion needed); licence tag removed; comments
  translated to English and standard header added; the duplicated
  (commented-out) `INTEGRAL` line and the duplicated `"$IntegralTable…"` line
  of the original were dropped as dead code; the equations are unchanged.
- **2026-10-05 — reference data.** The stored solution of the source file is
  cleared (inputs/constants only, no parametric table in the file). The
  sibling copy TM-0095 of the same exercise stores a complete 27-value
  solution of the same physics (AU = 1 MW/K, P = 1 bar), used as the EES
  reference (see *Verification*); it also provides the EES value of the
  near-freezing `INTENERGY(Water, T=-0.01, P)` call, −333 451.5211 J/kg.
- **2026-10-05 — runnable variant**
  `ice_storage_tank_discharge_phase_change_coolsolve.eescode`: identical
  physics, four syntactic transcriptions — symbolic limits `tau_1`, `tau_2`
  inlined as 0 and 50 000 (`CS-GAP-INTEGRAL-LIMITS`); the four EES
  5-argument `IF(A,B,X,Y,Z)` replaced by the 3-argument `if(cond,a,b)`
  comparing `u` with its threshold (CoolSolve-only syntax, not valid EES;
  `CS-GAP-IF5`; at the single point u = u_ice_0 the variant returns t_ice_0
  where EES returns 0 — no effect on the trajectory); the three Water
  property calls at or below 0 °C replaced by constants — `u_ice_0` =
  −333 451.5 J/kg (the EES value above), `v_ice` = 0.001091 m³/kg (ice at
  0 °C), `v_liq` = 0.001000 m³/kg (liquid water at 0 °C; the CoolSolve
  example uses 0.001004), original calls kept in comments
  (`CS-BUG-WATER-NEAR-FREEZING`), the then-unused `T_ice_ref`/`T_liq_ref`
  equations dropped; `$IntegralTable` space-separated
  (`CS-BUG-INTEGRAL-TABLE-SEP`) with the `t_w` column written `T_w`
  (case-sensitive column matching, `CS-BUG-INTEGRAL-TABLE-CASE`).
  `coolsolve.conf` raises `integralMaxSteps` to 6000 (5000 steps of 10 s;
  the default 1000 silently truncates the run at 40 000 s,
  `CS-BUG-INTEGRAL-MAXSTEPS`). Verified against the TM-0095 stored solution
  (see *Verification*).
- **Level 2** (score 2: coupled algebraic block of ~20 equations solved at
  each time step + the *dynamics* criterion; the block statistics of
  `coolsolve -d` are unusable for dynamic models, `CS-DOC-SQUARE-INTEGRAL`;
  in line with the inventory guess).

## Limitations and CoolSolve gaps

- Fully mixed tank (no stratification), constant cp for ice and liquid,
  linear phase-change relation between `u_ice_0` and `u_liq_0`, ε-NTU with a
  constant cold-side coefficient — the level of detail of the exercise.
- The main file is **blocked** by (see CoolSolve
  `docs/model_library_support.md`):
  - `CS-GAP-IF5` — the EES intrinsic `IF(A,B,X,Y,Z)` (5 arguments) is not
    supported; the whole phase-change logic uses it (4 calls);
  - `CS-GAP-INTEGRAL-LIMITS` — `INTEGRAL` limits must be constants; the
    model uses the variables `tau_1`, `tau_2`;
  - `CS-BUG-WATER-NEAR-FREEZING` — `INTENERGY`/`VOLUME` of Water at or below
    0 °C return NaN (CoolProp has no ice/metastable-liquid region), EES
    evaluates them (stored value −333 451.5211 J/kg in TM-0095);
  - `CS-BUG-INTEGRAL-TABLE-SEP` — comma-separated `$IntegralTable` columns
    silently produce empty columns;
  - `CS-BUG-INTEGRAL-MAXSTEPS` — the integration silently stops after
    4·`integralMaxSteps` steps (worked around with `coolsolve.conf`);
  - `CS-BUG-INTEGRAL-TABLE-CASE` — `$IntegralTable` columns are matched
    case-sensitively; the `t_w`/`T_w` mixed case of the original leaves the
    column silently empty.
- `t_ice` and `t_liq` are extrapolated one-regime outputs (as in the
  original): during melting `t_ice` keeps rising with `u` and `t_liq` is
  strongly negative; only `t_w` is the physical tank temperature.

## Related models

- `CSL-0009` *dhw_tank_dynamic*: the other dynamic storage model of the
  library (same `INTEGRAL`/`$IntegralTable` pattern, blocked by the same
  gaps, with its own runnable variant).
- The DG-0023 copies of this exercise (TM-0092/TM-0095/TM-0123, AU = 1 MW/K)
  are recorded as duplicates of this model.
