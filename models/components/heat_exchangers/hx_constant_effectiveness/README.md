# Heat exchanger with a constant effectiveness (enthalpy-based)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0126`

A counterflow heat exchanger with an *imposed* constant effectiveness: the duty
is $\eta$ times the largest heat rate an ideal exchanger (infinite area, no
temperature cross) could transfer between the two inlet states, and both
outlet states follow from the two energy balances. This is the workhorse of
simple cycle models — recuperators, internal heat exchangers (IHX) and gas
coolers — where the exchanger is *not* sized: the effectiveness is given and the
duty and outlet states are computed. Translation of the LaboThapPy component
`HexCstEff`.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | Water (any single-phase fluid, ideal or real) |
| **Size** | 44 equations (largest block: 1) |
| **Source** | LaboThapPy (Apache-2.0), file `labothappy/component/heat_exchanger/hex_csteff.py`, commit `f03f7f47` |
| **Authors** | Basile Chaudoir, Elise Neven (ULiège Thermodynamics Laboratory; LaboThapPy contributors, see `AUTHORS.txt`) |
| **License** | MIT (translation with credits, roadmap decision D3) |
| **CoolSolve** | 0.3.0@7addbbc — verified against the LaboThapPy example (see *Verification*) |

## Problem statement

Reproduce the LaboThapPy `HexCstEff` example: a water recuperator with hot
water entering at 110 °C, 10 bar, 0.3 kg/s and cold water entering at 60 °C,
3 bar, 1 kg/s. The effectiveness is 0.95. Compute the duty, the outlet
temperature and enthalpy of both streams, and the state that sets the maximum
heat rate.

## Model

The maximum heat rate is built from the two *ideal* outlet enthalpies, obtained
at the supply pressures and the temperature of the **opposite inlet** (the
infinite-area counterflow limit: the hot stream leaves at $T_{su,C}$, the cold
stream at $T_{su,H}$), as in the original:

$$h_{H,id} = h(fluid_H, T_{su,C}, P_{su,H}), \qquad
  h_{C,id} = h(fluid_C, T_{su,H}, P_{su,C})$$

$$\dot Q_{max} = \min\!\big(\dot m_H\,|h_{su,H} - h_{H,id}|,\ \dot m_C\,|h_{C,id} - h_{su,C}|\big),
  \qquad \dot Q = \eta\,\dot Q_{max}$$

The absolute values are those of the original (they guard against a
non-monotonic enthalpy); the two branches are reported separately so the
limiting stream is visible (`Q_dot_max_h` < `Q_dot_max_c`: hot-limited, as in
the shipped case).

Outlet states — two energy balances, no other closure:

$$h_{ex,H} = h_{su,H} - \dot Q/\dot m_H, \qquad h_{ex,C} = h_{su,C} + \dot Q/\dot m_C$$

$$P_{ex,H} = P_{su,H} - \Delta P_h, \qquad P_{ex,C} = P_{su,C} - \Delta P_c$$

$$T_{ex,H} = T(fluid_H, h_{ex,H}, P_{ex,H}), \qquad T_{ex,C} = T(fluid_C, h_{ex,C}, P_{ex,C})$$

The pressure drops `DP_h`/`DP_c` are the optional parameters of the original
(0 in its default). Because $\dot Q_{max}$ is written with enthalpies, the
equations need no quality or phase logic, which is why the same relations can
be reused for an IHX or a gas cooler; whether the property calls accept a
two-phase state is a property-backend question — the original guards them with
a `try/except` (see *Limitations*).

Diagnostics shipped with the model: `Q_dot_bal_H` and `Q_dot_bal_C` (both equal
to `Q_dot` by construction — energy balance of each stream) and
`Delta_T_cold_end` (cold-end temperature difference, 0 for $\eta = 1$).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_su_H` / `P_su_H` / `M_dot_H` | 110 °C / 10 bar / 0.3 kg/s | `Q_dot` duty | 59.860 kW |
| `T_su_C` / `P_su_C` / `M_dot_C` | 60 °C / 3 bar / 1 kg/s | `Q_dot_max` | 63.011 kW (hot-limited) |
| `eta` | 0.95 | `T_ex_H` / `h_ex_H` | 62.510 °C / 262.505 kJ/kg |
| `DP_h` / `DP_c` | 0 Pa | `T_ex_C` / `h_ex_C` | 74.293 °C / 311.276 kJ/kg |

## How to run

```bash
coolsolve ./hx_constant_effectiveness.eescode
```

No `.initials` file is needed: the system is explicit (largest algebraic block
of 1 equation) and solves in 0 Newton iterations. Change `fluid_C$`/`fluid_H$`,
the six supply conditions, `eta` and the two pressure drops to size another
duty; every fluid name follows §9 of the workflow (chemical formulas such as
`CO2` are the *ideal-gas* species in EES — use `R744` for the real fluid).

## Results

Default case (the LaboThapPy `hex_csteff_example.py` inputs, water on both
sides, $\eta = 0.95$): the hot stream gives up 59.86 kW of the 63.01 kW an
infinite-area exchanger would transfer, so it leaves 47.49 K below its inlet,
2.51 K above the cold inlet (cold-end approach), and the cold stream is heated
by 14.29 K.
The duty is limited by the hot stream (`Q_dot_max_h` = 63.01 kW <
`Q_dot_max_c` = 210.11 kW).

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (1 cold supply, 2 cold outlet,
3 hot supply, 4 hot outlet) give the two paths of the exchanger on the T-s or
h-s diagram (CoolSolve *Diagram* tab, *Overlay array path*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the
      two water paths through the recuperator, figures/hx_constant_effectiveness_ts.png -->

## Verification

The reference is the LaboThapPy source itself, re-run in a throw-away virtual
environment (local clone `~/git/LaboThapPy`, commit `f03f7f47`, installed with
`pip install ~/git/LaboThapPy`; CoolProp 8.0.0, matplotlib needed only because
`base_component.py` imports `pyplot`). The exact commands were:

```bash
python3 -m venv work/hx_constant_effectiveness/venv
work/hx_constant_effectiveness/venv/bin/pip install ~/git/LaboThapPy matplotlib
MPLBACKEND=Agg work/hx_constant_effectiveness/venv/bin/python \
    ~/git/LaboThapPy/labothappy/component/examples/heat_exchanger/hex_csteff_example.py
```

1. **The source's own example**, run unmodified
   (`labothappy/component/examples/heat_exchanger/hex_csteff_example.py`):

   ```
   === Heat Exchanger Results ===
   Q: 59860.06830657225
   === Heat Exchanger States ===
     - su_C: fluid=Water, T=333.15, p=300000.0, m_dot=1
     - su_H: fluid=Water, T=383.15, p=1000000.0, m_dot=0.3
     - ex_C: fluid=Water, T=347.442730364788, p=300000.0, m_dot=1
     - ex_H: fluid=Water, T=335.660263317977, p=1000000.0, m_dot=0.3
     - Q_dot: 59860.06830657225
   ```

2. **Value-by-value comparison.** A short script (`compare_ref.py`, written in
   the temporary work folder, now deleted) read the `.sol` of the model and a
   `reference_values.json` produced by instrumenting the *original* `solve()`
   (same inputs, no copy of the class, so the values are the ones of
   LaboThapPy itself), and compared the 29 common quantities —
   `h_H_id`, `h_C_id`, `Q_dot_max_h`, `Q_dot_max_c`, `Q_dot_max`, `Q_dot`, both
   outlet states and the four entropies — with the model temperatures in °C and
   the reference in K:

   | Quantity | LaboThapPy | CoolSolve | rel. dev. |
   |---|---:|---:|---|
   | `h_su_C` [J/kg] | 251 415.5339 | 251 415.5349 | 3.9·10⁻⁹ |
   | `h_su_H` [J/kg] | 462 038.6373 | 462 038.6378 | 9.4·10⁻¹⁰ |
   | `h_H_id` [J/kg] | 252 003.3099 | 252 003.3099 | 3.6·10⁻¹⁴ |
   | `h_C_id` [J/kg] | 461 529.1534 | 461 529.1534 | 7.7·10⁻¹⁴ |
   | `Q_dot_max_h` [W] | 63 010.5982 | 63 010.5983 | 2.1·10⁻⁹ |
   | `Q_dot_max_c` [W] | 210 113.6195 | 210 113.6185 | 4.6·10⁻⁹ |
   | `Q_dot` [W] | 59 860.0683 | 59 860.0684 | 2.1·10⁻⁹ |
   | `h_ex_H` [J/kg] | 262 505.0763 | 262 505.0763 | 8.2·10⁻¹¹ |
   | `h_ex_C` [J/kg] | 311 275.6022 | 311 275.6033 | 3.5·10⁻⁹ |
   | `T_ex_H` [K] | 335.660263 | 335.660263 | 9.8·10⁻¹⁰ |
   | `T_ex_C` [K] | 347.442730 | 347.442730 | 6.0·10⁻¹⁰ |
   | `s[4]` = `s_ex_H` [J/kg·K] | 862.176320 | 862.176289 | 3.6·10⁻⁸ |

   **Maximum relative deviation over the 29 compared variables: 2.253·10⁻⁷**
   (model and reference values are as in `model.json`,
   `verification.max_rel_diff`). It is reached on the cold-supply entropy
   `s[1]` (831.144076 vs 831.144263 J/kg·K, i.e. 1.9·10⁻⁴ J/kg·K in absolute
   terms) and comes from the property backend (both use CoolProp HEOS, but the
   reference value is read through the LaboThapPy connector, which goes
   through its own state caching); every energy quantity agrees to 10⁻⁹.
   Entropies are listed because they are absolute quantities of the model
   (diagram-ready state points).

3. **`eta = 1` cold-inlet self-check** (the exact property of the enthalpy-based
   formulation: the hot stream must leave exactly at the cold inlet state).
   Same inputs, `eta = 1`: `T_ex_H` = 60.000000 °C = `T_su_C`
   (`Delta_T_cold_end` = −1.0·10⁻¹² K), `h_ex_H` = `h_H_id` to 3.6·10⁻¹⁴
   relative, `Q_dot` = `Q_dot_max` = 63 010.598 W. The LaboThapPy run of the
   same case returns `T_ex_H` = 333.1499999445999 K, i.e. the same state to
   5.5·10⁻⁸ K; `Q_dot` = 63 010.598217 W agrees with the model to 2.1·10⁻⁹.
4. **Cold-limited branch** (`M_dot_C` = 0.2 kg/s, other inputs unchanged,
   $\eta$ = 0.95), to exercise the other side of the `MIN`: `Q_dot_max_c` =
   42 022.7237 W < `Q_dot_max_h` = 63 010.5983 W, so `Q_dot_max` =
   `Q_dot_max_c` = 42 022.7237 W and `Q_dot` = 39 921.5875 W in CoolSolve;
   the original gives 42 022.72389038859 W and 39 921.58769586916 W
   (relative deviation of `Q_dot` 4.6·10⁻⁹, maximum over the compared
   variables 2.253·10⁻⁷ as above). Here the cold stream is heated from 60 °C to
   107.51 °C while the hot stream leaves at 78.38 °C, so the cold outlet stays
   2.49 K below the hot inlet (no temperature cross).
5. **Internal balances**, in all three cases: `Q_dot_bal_H` = `Q_dot_bal_C` =
   `Q_dot` to the printed precision (the model computes the outlet enthalpies
   from the balances, so this is an exact algebraic identity, kept as a
   readable check in the main program).

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of `HexCstEff` from LaboThapPy, file
`labothappy/component/heat_exchanger/hex_csteff.py`, commit `f03f7f47`.
LaboThapPy — https://github.com/PyLaboThap/LaboThapPy —
Copyright (C) 2025 Université catholique de Louvain (UCLouvain), Université
de Liège (ULiège), Université de Mons (UMONS). Original authors: B. Chaudoir,
E. Neven (see `AUTHORS.txt`). Licence of the source: Apache-2.0 /
`LICENSE.txt` (permissive); the translation is published under the library
license (MIT).
Changes: translated from Python to EES-language equations; the Python
`try/except` around the property calls and the `AbstractState` objects become
ordinary property calls; the four `MassConnector` outputs become the outlet
state variables `h_ex_*`, `P_ex_*`, `T_ex_*`; the optional `DP_h`/`DP_c`
parameters are kept as inputs (0 by default, as in the original defaults);
`abs` and `min` kept as `ABS`/`MIN`; 16 post-processing state-array equations
added for the diagrams (results unchanged). Scientific basis: the
constant-effectiveness method; the source documents it in
`docs/source/documentation/component/heat_exchanger/heat_exchanger_models/hex_csteff.rst`
(no external paper cited, *References* section empty). The capacity-rate
relations it would need for the fallback branch are the classical ε-NTU ones,
available as functions in this library (`CSL-0090`).

Source files (not copied into the library):
`~/git/LaboThapPy/labothappy/component/heat_exchanger/hex_csteff.py` and
`~/git/LaboThapPy/labothappy/component/examples/heat_exchanger/hex_csteff_example.py`;
URL + paths as above. No student names or personal data involved.

## Conversion log

- **2026-10-08 — translation**: the physics of `solve()`/`update_connectors()`
  transcribed as simultaneous equations (the Python class has no iterative
  solver; nothing had to be turned into an unknown). Temperatures converted from
  K to °C (the original works in K, the connector prints K; input comments keep
  the original values: `T_su_H = 110` ← 383.15 K). Comments paraphrased from
  the original's own comments and from the model documentation page; "as in the
  original" is used where the original is terse. State names kept (`h_su_*`,
  `h_ex_*`, `Q_dot_max_*`), with `H_h_id`/`H_c_id` of the Python code renamed
  `h_H_id`/`h_C_id` for consistency with the EES state naming. The
  `self.su_H.m_dot = self.su_C.m_dot` default of the original (one mass flow
  copied to the other connector) is not shipped: an EES model takes both mass
  flow rates as inputs. 16 state-array equations added for the diagrams.
- **2026-10-08 — capacity-rate fallback dropped**: the `except:` branch of the
  Python code (used when the (P, T) property call fails, e.g. a two-phase
  state, and computing `Q_dot_max = C_min*(T_su_H - T_su_C)`) is a
  Python-error-handling artefact, not a second physical branch; it is documented
  in the README instead of shipped (see *Limitations*). The equivalent
  relation is available as a function in `CSL-0090`.
- **Level**: rubric of docs/taxonomy.md §3 — equations 44 (< 50) = 0, largest
  block 1 (≤ 5) = 0, structure: arrays present = 1, multi-zone/discretised or
  ≥ 3 coupled components = 0, semi-empirical calibration/off-design/part-load
  = 0, numerics (curated guesses, bootstrap, *Try Harder*) = 0. Score 1 → level 1.

## Limitations and CoolSolve gaps

- **Single phase, no admissibility check.** The model is a *constant-duty*
  relation: it does not check that $\eta \le \eta_{max}$, i.e. that the duty is
  admissible for a real exchanger. Check it with the ε-NTU relations of
  `CSL-0090` / `CSL-0102`, or by looking at the array `T[i]` (the two paths
  must not cross). Note also that the *enthalpy-based* limit is not exactly the
  classical capacity-rate limit $C_{min}(T_{su,H} - T_{su,C})$ when $c_p$ varies
  between the inlet and the ideal outlet state: in the cold-limited
  verification case (§4) the two differ by 0.4 % (42 022.7 W against
  41 845.1 W). The enthalpy-based definition is the one of the original and is
  kept unchanged.
- **No size, no off-design behaviour**: `eta` is an input, not a prediction;
  this is not a model of the exchanger area, of the UA distribution or of
  fouling. For a pinch-sized phase-changing exchanger see `CSL-0014`.
- **Pressure drops are constant by construction** (`DP_h`, `DP_c`), as in the
  original; the ideal enthalpies are evaluated at the *supply* pressures, so a
  large `DP_h`/`DP_c` makes `Q_max` slightly inconsistent with the outlet
  states (faithful to the original).
- **Fallback branch not shipped**: when the (P, T) ideal-enthalpy calls fail
  (two-phase state outside the single-phase range of the property
  backend), the original falls back to `C_min*(T_su_H - T_su_C)` with `c_p` at
  the supply states. In CoolSolve, an equivalent formulation is written
  directly with the ε-NTU relations; use it instead of relying on an exception.
- **CoolSolve gaps**: none — the native file runs unmodified, so
  `missing_features` is empty. (Unrelated observation, *unverified
  suggestion*, not registered: the property function `SPECIFICHEAT`, which the
  EES manual documents, is accepted by the evaluator but not recognised by the
  parser's thermophysical-function list — `warning (line 61): Unknown function
  'SPECIFICHEAT'. Did you mean 'specheat'?`. The capacity-rate diagnostics of
  the original were therefore not shipped; no model in the library or in
  `~/Nextcloud/thermo_models` uses that name, so there is no EES file
  reference and the behaviour was not registered as a gap.)

## Related models

- `CSL-0014` (*hx_constant_pinch*, level 2): translation of the sibling
  LaboThapPy component `HexCstPinch`; the *design* counterpart of this model
  (pinch imposed and the saturation pressure solved instead of the duty given).
- `CSL-0090` (*hx_effectiveness_ntu*, level 2): ε-NTU relations as FUNCTIONs
  (`C_min`, `Cr`, `eps(NTU, Cr)` and its inverse); use them to size an
  exchanger for the duty computed here or to check that `eta` is admissible
  (no temperature cross).

- `CSL-0128` *hx_eps_ntu_plate_pipe* (level 2): the same LaboThapPy plate
  heat exchanger with the conductance-area product computed from the plate
  geometry (Gnielinski film coefficients, plate conduction and fouling)
  instead of a prescribed effectiveness.
- `CSL-0127` *hx_constant_effectiveness_discretised* (level 4): the same
  LaboThapPy family pushed further — the exchanger is split into `n_disc`
  enthalpy segments and the duty is additionally limited by a minimum segment
  temperature difference `Pinch_min` and by an internal zero-pinch limit
  (`HexCstEffDisc`), for sCO2 recuperators and gas coolers.
