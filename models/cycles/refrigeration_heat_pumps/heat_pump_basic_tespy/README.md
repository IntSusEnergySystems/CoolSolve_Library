# Basic heat pump (TESPy tutorial)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0013`

A single-stage R134a vapour-compression heat pump after the TESPy basic
tutorial *Heat Pump*: evaporator and condenser (each with a 2 % pressure
drop), a compressor with isentropic efficiency η_s and an isenthalpic
expansion valve. The cycle delivers a prescribed condenser heat output from
saturated vapour at the evaporator outlet to saturated liquid at the
condenser outlet, and reproduces the tutorial's COP parametric studies
(source/sink temperature, compressor efficiency).

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R134a |
| **Size** | 41 equations, all explicit (largest block: 1): 25 for the model, 16 for the diagram state points |
| **Source** | TESPy tutorial `tutorial/basics/heat_pump.py` ([oemof/tespy](https://github.com/oemof/tespy), commit `19425523`), companion docs `docs/basic_tutorials/heat_pump.rst` |
| **Authors** | Francesco Witte (TESPy lead developer) and the TESPy contributors |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; translation verified against TESPy (see *Verification*) |

## Problem statement

A heat pump working with R134a delivers a condenser heat output of
1000 kW. The evaporator outlet is saturated vapour at 20 °C, the condenser
outlet is saturated liquid at 80 °C, the compressor isentropic efficiency
is 0.85, and both heat exchangers have a pressure ratio of 0.98.
Determine the refrigerant mass flow rate, the compressor power, the
discharge temperature and the COP. Then study how the COP depends on the
source temperature, the sink temperature and the compressor efficiency,
and how the operating point moves when the specification set is changed
(fixed mass flow, fixed pressure ratio, measured discharge temperature).

## Model

States (TESPy connection labels in parentheses): evaporator outlet /
compressor suction (c2, saturated vapour at `T_2`), compressor discharge
(c3), condenser outlet (c4, saturated liquid at `T_4`), evaporator inlet
after the valve (c0 = c1).

- Saturation states: `p_2 = Psat(T_2)`, `p_4 = Psat(T_4)` with `h_2`, `s_2`
  and `h_4` on the saturation curves.
- Heat-exchanger pressure drops (TESPy `SimpleHeatExchanger pr`):
  `p_2 = pr_ev·p_1`, `p_4 = pr_co·p_3`.
- Compressor (TESPy `Compressor eta_s`):
  `(h_3 − h_2)·η_s = h_3s − h_2` with `h_3s = h(s_2, p_3)`;
  `T_3`, `s_3` from `(h_3, p_3)`.
- Valve (TESPy `Valve`) and cycle closer (TESPy `CycleCloser`):
  `h_0 = h_4`, `p_0 = p_1`; `T_0`, `x_0` from `(h_0, p_0)`.
- Balances: `Q̇_cond = ṁ·(h_3 − h_4)`, `P_comp = ṁ·(h_3 − h_2)`,
  `COP = Q̇_cond/P_comp` (heating COP; TESPy reports
  `|Q_cond|/P` identically).

| Inputs | Base value | Outputs (base case) | Value |
|---|---|---|---|
| `Q_dot_cond` condenser heat output | 1000 kW | `m_dot` refrigerant flow | 8.059 kg/s |
| `T_2` evaporator outlet (sat. vapour) | 20 °C | `P_comp` compressor power | 296.0 kW |
| `T_4` condenser outlet (sat. liquid) | 80 °C | `T_3` discharge temperature | 91.17 °C |
| `eta_s` compressor efficiency | 0.85 | `x_0` evaporator inlet quality | 0.517 |
| `pr_ev` / `pr_co` pressure ratios | 0.98 / 0.98 | `COP` heating COP | 3.378 |

## How to run

Open `heat_pump_basic_tespy.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./heat_pump_basic_tespy.eescode
```

No `.initials` or `coolsolve.conf` needed: the system is fully explicit
and solves directly. The tutorial's alternative specification sets are
obtained by swapping inputs (see *Verification*): fix `m_dot` instead of
`Q_dot_cond` (sec_7), fix `p_3 = 4·p_2` and free `T_4` (sec_8), or fix
`T_3` and free `eta_s` (sec_9). The COP sweeps are CoolSolve parametric
studies over `T_2`, `T_4` and `eta_s`.

## Results

Base case (TESPy tutorial sec_5/sec_6):

| Point | TESPy connection | p [bar] | T [°C] | h [kJ/kg] | x [-] |
|---|---|---:|---:|---:|---:|
| 1 suction | c2 | 5.717 | 20.00 | 409.75 | 1 |
| 2 discharge | c3 | 26.869 | 91.17 | 446.48 | — (superheated) |
| 3 condenser outlet | c4 | 26.332 | 80.00 | 322.39 | 0 |
| 4 evaporator inlet | c0 = c1 | 5.834 | 20.66 | 322.39 | 0.517 |

`ṁ = 8.059 kg/s`, `Q̇_cond = 1000 kW`, `P_comp = 296.0 kW`, `COP = 3.378`.

Parametric COP study (TESPy reference values, reproduced point-wise in
CoolSolve — see *Verification*):

| `T_2` source sweep (`T_4` = 80 °C, η_s = 0.85) | COP | `T_4` sink sweep (`T_2` = 20 °C, η_s = 0.85) | COP | η_s sweep (`T_2`/`T_4` = 20/80 °C) | COP |
|---:|---:|---:|---:|---:|---:|
| 0 °C | 2.419 | 60 °C | 5.615 | 0.75 | 3.099 |
| 8 °C | 2.736 | 68 °C | 4.537 | 0.79 | 3.210 |
| 16 °C | 3.136 | 76 °C | 3.723 | 0.83 | 3.322 |
| 24 °C | 3.656 | 84 °C | 3.062 | 0.87 | 3.434 |
| 32 °C | 4.355 | 92 °C | 2.476 | 0.91 | 3.546 |
| 40 °C | 5.335 | 100 °C | 1.802 | 0.95 | 3.658 |

(Full 11-point sweeps in `0–40 °C`, `60–100 °C`, `0.75–0.95` were run in
TESPy; the table shows every other point, all of them direct TESPy outputs.)

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 suction, 2 discharge,
3 condenser outlet, 4 evaporator inlet) give the cycle on the P-h or T-s
diagram (CoolSolve *Diagram* tab, *Overlay array path*, *Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the R134a cycle,
     figures/heat_pump_basic_tespy_ph.png -->

## Verification

TESPy has no stored numbers for this tutorial (`tests/test_basic_tutorials.py`
only executes the scripts), so the tutorial itself was run in a throw-away
virtual env (Python 3.11, TESPy installed from the local snapshot at commit
`19425523`, CoolProp 8.0.0) and every result below is a direct TESPy output.
Chronological CoolSolve runs agree to ≤ 6e-9 relative (same CoolProp
equation of state on both sides), i.e. far inside the property tolerance of
CoolSolve `docs/ees_import.md` §11.

1. **Base case** (sec_5/sec_6: `Q̇_cond` = 1000 kW): all 8 key quantities
   (`ṁ`, `COP`, `|Q̇|`, `P`, `p_2`, `p_3`, `p_4`, `T_3`) agree exactly
   (max. relative deviation 2e-13; `COP` = 3.37838 both sides).
2. **Specification variants** (the tutorial's flexibility section, each run
   as a CoolSolve model with the swapped input set):
   - sec_7, `ṁ` = 5 kg/s instead of `Q̇_cond`: `|Q̇|` = 620.441 kW,
     `P` = 183.651 kW, same `COP` (max. deviation 2.4e-13);
   - sec_8, compressor `pr` = 4, `T_4` free: `T_4` = 72.57 °C,
     `T_3` = 82.45 °C, `COP` = 4.04860 (max. deviation 1.6e-13);
   - sec_9, measured `T_3` = 97.3 °C, η_s free: η_s = 0.6819,
     `COP` = 2.90794 (max. deviation 5.8e-09).
3. **Parametric sweeps** (sec_10: `T_2` 0–40 °C, `T_4` 60–100 °C, η_s
   0.75–0.95, 11 points each): the end points re-solved in CoolSolve by
   editing the corresponding input agree to ≤ 8e-09
   (`T_2` = 0 °C → `COP` 2.41944; `T_4` = 100 °C → 1.80165;
   η_s = 0.75 → 3.09857). The sweeps themselves are CoolSolve parametric
   studies (GUI *Parametric* tab); TESPy's `heat_pump_parametric.svg`
   figure is the counterpart of that plot.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the TESPy basic tutorial *Heat Pump*, file
`tutorial/basics/heat_pump.py`, commit 19425523.
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy
Copyright (c) Francesco Witte and the TESPy contributors (see CITATION.cff / version control history).
Original model released under the MIT License.
Changes: translated from Python to CoolSolve; iterative network solver
replaced by simultaneous equations; units normalised to SI-°C-Pa-J
(TESPy displays bar/°C/kJ/kg/kW); heating COP reported as a positive
quantity; parametric loops documented as CoolSolve parametric studies.
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in Python",
J. Open Source Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.
Scientific basis: none beyond the tutorial itself (textbook vapour-compression cycle).

Source file (Python, comments in English), local snapshot of S. Quoilin:
`~/git/tespy/tutorial/basics/heat_pump.py`
(companion: `docs/basic_tutorials/heat_pump.rst`; test: `tests/test_basic_tutorials.py`)
(inventory candidate `TSP-035`).

## Conversion log

- **2026-10-05 — translation** (workflow `T-TRANSLATE`): TESPy network
  (`CycleCloser`, 2 × `SimpleHeatExchanger`, `Compressor`, `Valve`, 5
  connections) rewritten as 25 simultaneous EES equations: the cycle
  closer disappears (state 0 = state 1 written once), the valve is
  `h_0 = h_4` / `p_0 = p_1`, the compressor is the textbook
  `(h_3 − h_2)·η_s = h_3s − h_2` relation of
  `sources/tespy/README.md` §5. Units already SI-like; only the display
  units change (bar → Pa, kJ/kg → J/kg, kW → W). Verified as above.
- **2026-10-05 — diagram support**: block of 16 post-processing equations
  (state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`) added at the end of the
  model for the CoolSolve diagrams; the results of the model are unchanged.
- **Decision**: the model ships the base case only; the three spec
  variants and the sweeps are documented input swaps (verified during the
  task in the work folder), not separate files — they are tutorial content
  about TESPy's specification flexibility, not different physics.

## Limitations and CoolSolve gaps

- No CoolSolve gap encountered: the model uses only property calls,
  arithmetic and one `QUALITY` call, and solves with no guesses.
- Modelling note: near the saturated-liquid condenser outlet, the state
  must be addressed with `(T, x)` inputs, not `(P, T)` — a `(P, T)` call
  exactly on the saturation dome is ambiguous for the CoolProp flash
  (returns NaN). This is a CoolProp property-call limitation, not a
  CoolSolve gap, and the model avoids it by construction.
- TESPy sign convention (`Q_cond` negative = heat rejected) vs this
  model (`Q_dot_cond` positive = heat delivered); magnitudes compared.
- The tutorial's matplotlib figure (`heat_pump_parametric.svg`) has no
  counterpart file in the library; the CoolSolve parametric plot is made
  in the GUI (figure step, workflow §7).

## Related models

- `CSL-0001` (*refrigeration_cycle_simple_compressor*, same category):
  same R134a vapour-compression physics with a clearance-volume compressor
  model and a fluid comparison; this model uses the textbook
  constant-`eta_s` compressor of the TESPy tutorial and adds the COP
  parametric study.
- `CSL-0015` *refrigeration_cycle_basic_r134a*: the same basic R134a cycle as a
  refrigeration exercise (EES original).
- See also the CoolSolve examples `refrigeration1.eescode` (R134a basic
  refrigeration cycle) and `refrigeration2.eescode` (R22 heat pump) of the
  `G-refrig` group.
- `CSL-0054` *heat_pump_r410a_air_evaporator*: air/water heat pump on the
  zeotropic R410A, with the evaporator pressure drop and air-side heat balance.
