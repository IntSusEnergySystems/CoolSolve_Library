# Engine dynamometer test

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0244`

Teaching exercise (ULiège MCI, TP3, exercise 5): shaft power, friction power,
brake mean effective pressure and torque of a four-stroke engine. The shaft
power is the dynamometer reading divided by the dynamometer efficiency. The
indicated power follows from the mechanical efficiency. The brake mean
effective pressure uses the theoretical volume flow. The torque follows from
the shaft power and the angular speed.

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | none |
| **Size** | 14 equations (largest block: 1) |
| **Source** | `~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP3_EX-1-2-3-4-5/MCI_TP3_Ex 5.EES` (EES X10.589) |
| **Authors** | P. Ngendakumana, R. Dickes |
| **License** | MIT |
| **CoolSolve** | 0.3.0@4ded1eb — verified against the EES stored solution (max rel. diff 2.34e-10) |

## Problem statement

The equation window is titled `MCI_TP3_Exercice 5` and stamped `PNG07032019`.

Data, as written in the file:

- `n_c = 3` cylinders
- `i = 0.5`, the intermittency factor for a four-stroke engine
- `W_dot_sh_dyna = -70.4e3` W, the power measured by the dynamometer
- `eta_dyna = 0.93`, the dynamometer efficiency
- `N = 4000` 1/min, the engine rotational speed
- `V_s_tot = 2.4e-3` m³, the engine displacement
- `eta_m = 0.82`, the mechanical efficiency

The dynamometer power is negative, as written. `n_c` is stated and no other
equation uses it.

## Model

Shaft power, indicated power and friction power:

\[
\dot W_{sh} = \dot W_{sh,\mathrm{dyna}} / \eta_{\mathrm{dyna}}, \qquad
\dot W_i = \dot W_{sh} / \eta_m, \qquad
\dot W_f = \dot W_i - \dot W_{sh}
\]

Theoretical volume flow and brake mean effective pressure. The factor
\(10^{-5}\) is the one written in the file; the original comment on `bmep`
says bar:

\[
\dot V_{th} = i\, V_{s,\mathrm{tot}}\,(N/60), \qquad
\mathrm{bmep} = -(\dot W_{sh}/\dot V_{th})\times 10^{-5}
\]

Angular speed and torque. The second equation for `W_dot_sh` leaves `Tau`
as the unknown. The window writes `pi`:

\[
\omega = 2\pi\,(N/60), \qquad \dot W_{sh} = -\omega\,\mathrm{Tau}
\]

| Quantity | Role | Value |
|---|---|---|
| `W_dot_sh_dyna` | dynamometer power | −70.4×10³ W |
| `eta_dyna` | dynamometer efficiency | 0.93 |
| `eta_m` | mechanical efficiency | 0.82 |
| `N` | rotational speed | 4000 1/min |
| `V_s_tot` | displacement | 2.4×10⁻³ m³ |
| `i` | intermittency factor | 0.5 |
| `n_c` | number of cylinders | 3, unused by the other equations |
| `W_dot_sh`, `W_dot_i`, `W_dot_f` | shaft, indicated and friction power | solved, W |
| `V_dot_th` | theoretical volume flow | solved, m³/s |
| `bmep` | brake mean effective pressure | solved, bar |
| `omega`, `Tau` | angular speed and torque | solved, rad/s and N·m |

Every block has size 1 (largest block 1). `n_c = 3` is kept: it is an
equation of the window.

## How to run

From this folder:

```bash
../../../../../CoolSolve/build/coolsolve ./engine_dynamometer_test.eescode
```

`engine_dynamometer_test.initials` holds the stored values of the 14 names
that exist in the equation window. With that file the solver reports 2
iterations. Without it, 3 iterations. The two solutions are identical. The
shipped `.sol` is the run with the initials file. No `coolsolve.conf` and
no variant.

## Results

Closed form of the data: `W_dot_sh = -70400/0.93`, `W_dot_i = W_dot_sh/0.82`,
`W_dot_f = W_dot_i - W_dot_sh`, `V_dot_th = 0.5*2.4e-3*(4000/60) = 0.08`,
`bmep = -(W_dot_sh/0.08)*1e-5`, `omega = 2*pi*(4000/60)`,
`Tau = -W_dot_sh/omega`.

| Quantity | CoolSolve | EES stored |
|---|---:|---:|
| `W_dot_sh` [W] | −75698.92473118 | −75698.92473 |
| `W_dot_i` [W] | −92315.76186730 | −92315.76187 |
| `W_dot_f` [W] | −16616.83713611 | −16616.83714 |
| `V_dot_th` [m³/s] | 0.08 | 0.08 |
| `bmep` [bar] | 9.462365591398 | 9.462365591 |
| `omega` [rad/s] | 418.8790204786 | 418.8790205 |
| `Tau` [N·m] | 180.7178708656 | 180.7178709 |

Orders of magnitude: a dynamometer reading of 70.4 kW at efficiency 0.93 is
a shaft power of about 75.7 kW. At a mechanical efficiency of 0.82 the
friction power is about 16.6 kW, 18% of the indicated power. The volume
flow 0.08 m³/s at that shaft power is a brake mean effective pressure of
about 9.46 bar. At 4000 1/min the torque is about 181 N·m. For a 2.4 L
engine those figures are a plausible full-load point.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/<name>_ph.png)  + one-line caption -->

The equations define no thermodynamic state. No diagram-state arrays were
added. The figure placeholder is left for the maintainer.

## Verification

Reference: the solution stored in `MCI_TP3_Ex 5.EES` (16 names decoded by
`ees_extract.py`). The unit system is already `SI MASS DEG PA C J`, so the
comparison is without `--ees-units`. `compare_solution.py` on
`engine_dynamometer_test.sol` against `reference/ees_variables.csv`:

> 14 common variables, 0 differ (rtol=0.001); only in EES: 2; only in CoolSolve: 1

Maximum relative difference over all common variables, as printed in the
tool's table: **2.34e-10** (`W_dot_f`). Nothing exceeds rtol 0.001.

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `W_dot_f` | −16616.8 | −16616.8 | 2.34e-10 |
| `Tau` | 180.718 | 180.718 | 1.90e-10 |
| `omega` | 418.879 | 418.879 | 5.11e-11 |
| `bmep` | 9.46237 | 9.46237 | 4.21e-11 |
| `W_dot_i` | −92315.8 | −92315.8 | 2.92e-11 |
| `W_dot_sh` | −75698.9 | −75698.9 | 1.56e-11 |

`eta_dyna`, `eta_m`, `i`, `N`, `n_c`, `V_dot_th`, `V_s_tot` and
`W_dot_sh_dyna` agree exactly (rel. diff `0.00e+00`).

The gaps are the rounding of the stored EES values. The CoolSolve numbers
match the closed form above. `bmep` is compared in bar, the unit of the
equation as written.

The names present only in the decoded EES list are `D` (0.24) and `L`
(0.36). They do not appear in the equation window, so they were not
restored. The name present only in the CoolSolve solution is `pi`.

With the stored guesses, and from the default guess, every equation is
satisfied (max relative residual 0).

## Source and attribution

Source file
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP3_EX-1-2-3-4-5/MCI_TP3_Ex 5.EES`
(EES X10.589, plain-text equations). The equation window is stamped
`PNG07032019`. The `{$ID$}` tag is the EES licence of Philippe
Ngendakumana (ULG Thermotechnics, Liège), licence holder `#3804`. The
inventory row TM-0238 names P. Ngendakumana and R. Dickes. ULiège course
MCI, TP3, exercise 5. Published under the library licence (MIT).

## Conversion log

- **2026-10-16 — import** (`ees_extract.py`): EES X10.589, plain-text
  equations, `{$ID$}`/`{$PX$}`/`{$ST$}` tags removed, no lookup or
  parametric table, 16 names decoded, no extract warnings. Unit system
  already `SI MASS DEG PA C J`: `$UnitSystem` removed, no value rescaled.
  The formatting directive `$TABSTOPS` was removed. The factor `1e-5` in
  the `bmep` equation is unchanged, so `bmep` stays in bar. The extract
  with the `$UnitSystem` line removed (`$TABSTOPS` still present) is
  square (14 equations, 14 variables). `D` and `L` stay out of the model.
  `n_c = 3`, `W_dot_sh_dyna = -70.4e3` and `W_dot_sh = - omega*Tau` are
  unchanged. `omega = 2*pi*(N/60)` keeps the window spelling `pi`; with
  that spelling the system is square. Comments translated to English;
  variable names kept. No diagram-state arrays: the file has no fluid call
  and no cycle diagram.
- **Level**: equations 14 (< 50) → 0; largest block 1 (≤ 5) → 0; no user
  function, procedure, array or `DUPLICATE` → 0; one engine, no multi-zone
  discretisation and no set of three coupled components → 0; the
  efficiencies are given data (no calibration, off-design, part-load or
  dynamics) → 0; converges from the default guess in 3 iterations, without
  a tuned configuration → 0. Score 0 → **level 1**.

## Limitations and CoolSolve gaps

- `n_c = 3` is stated and unused. The volume flow uses the total
  displacement `V_s_tot`.
- The dynamometer power is negative, as written, and the shaft, indicated
  and friction powers stay negative. The leading minus in the `bmep`
  equation makes that pressure positive.
- `bmep` is in bar because of the factor `1e-5`.
- `D` and `L` are stored in the EES file and are absent from the equation
  window.
- No CoolSolve gap blocks this file. `missing_features` is empty.

## Related models

- `CSL-0273` *engine_data_coherence_derating*: worked example checking engine
  data-sheet coherence (shaft power from the torque among them).
- `CSL-0275` *square_v6_engine_exercise*: MCI TP3 exercises 1-3 on a square
  V6 engine (same TP series; shaft power, bmep and friction losses in its
  exercise 2).
- `CSL-0279` *engine_bsfc_bore_stroke_afr*: the same shaft/indicated chain of
  the mechanical efficiency, with the fuel flow and the specific fuel
  consumptions added (MCI TP7, exercise 2).
