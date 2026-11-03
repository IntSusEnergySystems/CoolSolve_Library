# Isentropic nozzle with critical pressure (choked / unchoked flow)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0310`

A steady-flow nozzle on air, sized from a given mass flow rate: the total
enthalpy is conserved between the supply and the throat, the throat state is
isentropic, and the throat pressure is the larger of the imposed back
pressure and the critical pressure — so the model switches by itself between
the unchoked and the choked regime (`P_thr = max(P_ex, P_crit)`). The
isentropic exponent gamma is not fixed at 1.4: it is an unknown solved from
the isentropic temperature–pressure relation with the real-gas throat
temperature (a real-gas gamma, as the inventory row calls it).

| | |
|---|---|
| **Category** | Components › Valves, nozzles and piping |
| **Fluids** | Air (ideal gas) |
| **Size** | 16 equations, largest block 4 (13 blocks) |
| **Source** | ULiège — course *Machines et systèmes thermiques*, repetition 1 (EES file `Isentropic Noozle.EES`) |
| **Authors** | TBD (ULiège MSTh course team: J. Lebrun, V. Lemort, S. Bertagnolio) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — verified (see *Verification*) |

## Problem statement

Air at 15 °C and 1 bar flows at 0.5 kg/s through a nozzle to a back pressure
`P_ex`. The file (comments in French) models the isentropic nozzle with
critical pressure: compute the throat state, the throat velocity and the
throat area for a back pressure of 0.9 bar (the default run), and show the
choked behaviour when the back pressure falls below the critical pressure.
The original left `P_ex = 0.8E5` in a commented line; the EES-stored value of
the last run is 0.9 bar, kept as the default.

## Model

- supply state: `h_su = enthalpy(Air, T=T_su)`, `s_su = entropy(Air, T=T_su, P=P_su)`;
- total enthalpy conservation: `h_thr_s + C_thr^2/2 = h_su`;
- isentropic throat state: `h_thr_s = enthalpy(Air, P=P_thr, s=s_su)`,
  `T_thr = temperature(Air, s=s_su, P=P_thr)`;
- critical (choked) pressure: `P_crit = (2/(gamma+1))^(gamma/(gamma-1)) * P_su`;
- throat pressure: `P_thr = max(P_ex, P_crit)` — choked when `P_ex < P_crit`;
- real-gas gamma: `(T_thr+273)/(T_su+273) = (P_thr/P_su)^((gamma-1)/gamma)`
  (the original's provisional `gamma = 1.4` is a comment; the +273 is the
  original's, a 0.15 K approximation of T in K);
- continuity and sizing: `C_thr = V_dot_thr/A_thr`, `V_dot_thr = M_dot*v_thr`,
  `v_thr = volume(Air, h=h_thr_s, s=s_su)`;
- `DELTAP = P_su - P_ex` (extra variable of the original, "for a plot").

| Inputs | Value | Outputs (default run) | Value |
|---|---|---|---|
| `T_su` supply temperature | 15 °C | `P_thr` throat pressure | 90 000 Pa |
| `P_su` supply pressure | 1 bar | `T_thr` throat temperature | 6.44 °C |
| `P_ex` back pressure | 0.9 bar | `C_thr` throat velocity | 130.98 m/s |
| `M_dot` mass flow | 0.5 kg/s | `A_thr` throat area | 3.4026e-3 m² |
| | | `P_crit` critical pressure | 52 810 Pa |
| | | `gamma` (real gas) | 1.40109 |

## How to run

```bash
coolsolve ./isentropic_nozzle_critical.eescode
```

The `.initials` file holds the EES values of the last run (they are needed:
the property calls fail from the parser default guesses). Change `P_ex` to a
value below `P_crit` ≈ 0.528 bar to get the choked run (update `P_ex` in
`.initials` accordingly).

## Results — both regimes

| Run | `P_ex` [Pa] | `P_thr` [Pa] | `T_thr` [°C] | `C_thr` [m/s] | `A_thr` [m²] | regime |
|---|---:|---:|---:|---:|---:|---|
| default (EES) | 90 000 | 90 000 | 6.44 | 130.98 | 3.4026e-3 | unchoked (`P_ex > P_crit`) |
| choked | 30 000 | 52 804 (= `P_crit`) | −33.14 | 310.63 | 2.0988e-3 | choked (`P_thr = P_crit`) |

In the choked run the throat velocity equals the local speed of sound (see
*Verification*), as expected at choking.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric plot of
     P_thr and A_thr vs P_ex showing the choking plateau, figures/isentropic_nozzle_critical_sweep.png -->

## Verification

1. **EES stored solution** (5 of 16 variables stored in the source file —
   `compare_solution.py` vs `ees_variables.csv`: "4 common variables, 2 differ
   (rtol=0.001)"): `M_dot`, `P_su`, `T_su` are exact; the 2 DIFFs are `h_su`
   and `s_su`, which carry the documented Air reference-state offsets
   (EES − CoolSolve: −126 kJ/kg on h, +1815 J/kg-K on s; CoolSolve
   docs/ees_import.md §11).
2. **EES last-solution values** (the source file clears its stored values but
   keeps them in the guess column; the set is self-consistent — reference file
   assembled in the import notes): "16 common variables, 5 differ
   (rtol=0.001)". The 5 DIFFs: `h_su`, `h_thr_s`, `s_su` (same Air reference
   offsets), `DELTAP` (EES kept a stale default guess of 1; CoolSolve gives
   the exact 10000 Pa = P_su − P_ex) and `T_thr` at **max. rel. diff. 4.3e-03**
   (EES 7.458 vs CoolProp air properties). All remaining variables (`P_thr`,
   `P_ex`, `P_crit`, `gamma`, `v_thr`, `V_dot_thr`, `C_thr`, `A_thr`) agree
   within rtol 0.001.
3. **Analytical check of the choked run**: `C_thr` = 310.63 m/s vs the speed
   of sound √(gamma·R·T_thr) = √(1.4014·287·240.01) = 310.70 m/s (0.02 %):
   the throat is sonic at choking, as expected.

## Source and attribution

Exercise file of the ULiège course *Machines et systèmes thermiques*
(repetition 1, TP 01). The file names no author (EES licence stamp:
Laboratoire de Thermodynamique, ULiège); the course team is J. Lebrun,
V. Lemort and S. Bertagnolio — the maintainer completes the authors.

Source file (EES 7.458, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 01/Isentropic Noozle.EES`
(inventory candidate `TM-0002`).

## Niche

Nearest models (equations, fluids, topology):

- `CSL-0234` / `CSL-0207` / `CSL-0199` (turbo-expanders, MSTh repetition R4):
  their nozzle block is equation-for-equation the same physics (total
  enthalpy, isentropic throat, `max(P_ex, P_crit)`, gamma from the same
  temperature ratio — fixed at 1.4 in CSL-0199). But there the nozzle is
  embedded in a machine (Laval wheel, power, efficiency), it lives in
  *Expanders and turbines*, and the throat area is an identified or fixed
  equivalent area, not a design result. This model is the standalone nozzle
  component: it sizes `A_thr` from a given mass flow, shows both regimes
  against its own EES reference, and is verified on its own operating point.
- `CSL-0118` *air_nozzle_ejector*: primary-nozzle equation of an ejector,
  incompressible orifice form, no critical-pressure test.
- `CSL-0190` *steam_nozzle_exit*: steam, steady-flow energy balance on a
  given exit state, no choking.

What this adds: the only library model of the nozzle component alone, with
the choked/unchoked switch and throat sizing on air.

## Conversion log

- **2026-10-31 — import** (`tools/ees_extract.py`): unit system already
  SI MASS DEG PA C J (no conversion); the EES licence tag was removed;
  comments translated to English; variable names kept. The equations window
  leaves `P_ex` undefined (its line `P_ex=0.8E5` is commented out; the file
  was last run with 0.9 bar, value kept in the EES variable data) →
  `P_ex = 9E4` added as the default run, the commented 0.8E5 noted above.
  The provisional `gamma = 1.4` of the original is already a comment there;
  `gamma` is an unknown, as in the original.
- **2026-10-31 — verification**: the EES-stored values (5 of 16) and the
  self-consistent last-solution set kept in the EES guess column (see
  *Verification*); the choked run has no EES reference and was checked
  analytically (sonic throat).
- **Level**: equations 16 < 50 → 0; largest block 4 ≤ 5 → 0; no
  functions/arrays → 0; single component → 0; no calibration/off-design → 0;
  property calls need the `.initials` guesses → 1. Score 1 → **level 1**.

## Limitations and CoolSolve gaps

- Ideal-gas air: the "real-gas gamma" only accounts for the temperature
  dependence of cp through the CoolProp air model (gamma ≈ 1.4011 here);
  no humidity, no friction, no divergence losses.
- `(T_thr + 273)` inside the original temperature ratio is the original's
  0.15 K approximation (kept, as in the original).
- No CoolSolve gap blocks the model (`missing_features` empty): `max()`, the
  `(h, s)` and `(s, P)` property input pairs and the pressure-less
  `enthalpy(Air, T=…)` all work as in EES.

## Related models

- `CSL-0234` *turboexpander_ideal_nozzle_laval*: same nozzle equations
  embedded in a turbo-expander machine (MSTh R4), `related` back-link there.
- `CSL-0207` *turboexpander_parameter_identification*: the same nozzle core
  inside an expander whose throat area and wheel diameter are identified
  from data.
- `CSL-0199` *turboexpander_laval_wheel*: same machine with gamma fixed at
  1.4.
- `CSL-0118` *air_nozzle_ejector*: air nozzle of an ejector, unchoked
  orifice equation.
- `CSL-0190` *steam_nozzle_exit*: steam nozzle energy balance, no choking.
