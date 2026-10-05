# Heat exchanger with an imposed pinch (three zones)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0014`

A phase-changing heat exchanger sized by an imposed pinch (minimum
temperature difference between the streams) and an imposed
superheating/subcooling. The model is the condenser branch of the LaboThapPy
component `HexCstPinch`: three refrigerant zones in series — desuperheating,
two-phase condensation, subcooling — against a single-phase coolant. The
saturation pressure is the implicit unknown, closed by the pinch condition
evaluated as the minimum over the three candidate locations (hot end,
dew-point interface, cold end).

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | R744 (CO2), Water |
| **Size** | 51 equations (largest block: 18), incl. 16 diagram equations |
| **Source** | LaboThapPy (Apache-2.0), file `labothappy/component/heat_exchanger/hex_cstpinch.py`, commit `f03f7f47` |
| **Authors** | Basile Chaudoir, Elise Neven, Titouan Janod (ULiège Thermodynamics Laboratory; LaboThapPy contributors, see `AUTHORS.txt`) |
| **License** | MIT (translation with credits, roadmap decision D3) |
| **CoolSolve** | main 2026-10-05 — runs; verified against the LaboThapPy example (see *Verification*) |

## Problem statement

Size a CO2 condenser for the LaboThapPy `COND_CO2` example: hot CO2 enters at
30 °C, 60 bar, 15 kg/s; cooling water enters at 15 °C, 5 bar, 100 kg/s.
Design parameters: pinch 5 K, subcooling 0.1 K. Find the condensing pressure,
the zone duties and the outlet states such that the minimum temperature
difference between the streams equals the pinch.

## Model

Hot side (refrigerant, as in the original `system_cond` with `DP_h = 0`, the
default of the example):

- saturated states at the unknown pressure: $T_{sat}$, $h_g$, $h_f$;
- $Q_{sh} = \dot m_H\,(h_{su,H} − h_g)$ (superheated inlet assumed, see
  *Limitations*), $Q_{tp} = \dot m_H\,(h_g − h_f)$;
- outlet $T_{ex,H} = T_{sat} − \Delta T_{sh,sc}$,
  $h_{ex,H} = h(P_{sat}, T_{ex,H})$,
  $Q_{sc} = \dot m_H\,(h_f − h_{ex,H})$; $Q = Q_{sh} + Q_{tp} + Q_{sc}$.

Cold side (water, single phase, $P_{su,C}$ throughout, as in the original):

- $h_{C,x0} = h_{su,C} + Q_{sc}/\dot m_C$,
  $h_{C,x1} = h_{C,x0} + Q_{tp}/\dot m_C$,
  $h_{ex,C} = h_{C,x1} + Q_{sh}/\dot m_C$, temperatures from $(h, P)$.

Pinch closure (the Python `brentq` on `P_sat` becomes an equation):

- $PP_{hot} = T_{su,H} − T_{ex,C}$,
  $PP_{int} = T_{sat} − T_{C,x1}$,
  $PP_{cold} = T_{ex,H} − T_{su,C}$;
- $PPTD = \min(PP_{hot}, \min(PP_{int}, PP_{cold})) = Pinch$.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_su_H` / `P_su_H` / `M_dot_H` | 30 °C / 60 bar / 15 kg/s | `P_sat` condensing pressure | 63.54 bar |
| `T_su_C` / `P_su_C` / `M_dot_C` | 15 °C / 5 bar / 100 kg/s | `T_sat` | 24.46 °C |
| `Pinch` | 5 K | `Q_dot` total duty | 2 382 kW |
| `Delta_T_sh_sc` | 0.1 K | `Q_dot_sh` / `Q_dot_tp` / `Q_dot_sc` | 517 / 1 856 / 9 kW |

## How to run

```bash
coolsolve ./hx_constant_pinch.eescode
```

**The shipped `.initials` file is required** (the 18-equation block does not
converge from default guesses): the guesses are seeded with the LaboThapPy
reference solution.

## Results

Model solution vs the clean LaboThapPy re-run (same inputs, see
*Verification*); the active pinch is the internal one (dew-point interface),
5.00 K in both. (The LaboThapPy fluid name `CO2` maps to EES `R744`, the real
fluid — bare `CO2` is the ideal-gas species in EES.)

| Quantity | LaboThapPy | CoolSolve | rel. diff. |
|---|---|---:|---|
| `P_sat` [bar] | 63.7517 | 63.5440 | 0.33 % |
| `T_sat` [°C] | 24.599 | 24.457 | 0.14 K |
| `Q_dot_sh` [kW] | 525.1 | 516.8 | 1.6 % |
| `Q_dot_tp` [kW] | 1 840.6 | 1 856.5 | 0.9 % |
| `Q_dot_sc` [kW] | 84.1 | 9.0 | see text |
| `Q_dot` [kW] | 2 449.8 | 2 382.3 | 2.8 % |
| `T_ex_C` [°C] | 20.855 | 20.693 | 0.16 K |
| `PP_hot` / `PP_int` / `PP_cold` [K] | 9.15 / 5.00 / 9.50 | 9.31 / 5.00 / 9.36 | – |

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (1 hot supply, 2 saturated vapour,
3 saturated liquid, 4 subcooled outlet) give the refrigerant path on the P-h
or T-s diagram (CoolSolve *Diagram* tab, *Overlay array path*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the
      CO2 path through the condenser, figures/hx_constant_pinch_ph.png -->

## Verification

1. **LaboThapPy example reproduced.** The `COND_CO2` case of
   `labothappy/component/examples/heat_exchanger/hex_cstpinch_example.py`
   (LaboThapPy snapshot `~/git/LaboThapPy`, commit `f03f7f47`) was run in a
   throw-away virtual env (CoolProp 8.0.0, SciPy; plotting calls skipped):
   it converges (`solved: True`, pinch residual 5·10⁻¹⁰ K) to `P_sat` =
   63.75170 bar, `Q_dot` = 2 449 842 W.
2. **Clean re-run.** The example's `solve()` bracketing loop permanently
   raises `su_H.T` while searching the root (here +3.7 K on the displayed
   supply temperature — a latent defect of the original, cosmetic here
   because the hot-end pinch is not active and the connector enthalpy is
   cached at `set_inputs`). A clean re-run driving the original
   `system_cond` with an independent `brentq` (inputs unmutated) agrees
   with `solve()` to 1·10⁻⁷ — the reference above.
3. **Model vs reference** (table in *Results*): all state enthalpies agree
   within 0.3 % except the subcooled outlet (1.7 %, see below); `P_sat`
   within 0.33 %; the pinch is exactly satisfied in both. The only outlier
   is the subcooling duty: LaboThapPy evaluates the outlet enthalpy
   0.1 K below saturation with its `BICUBIC&HEOS` tables as 5 607 J/kg under
   $h_f$, while the reference EOS (HEOS, used by both LaboThapPy's own
   `PropsSI` calls and CoolSolve) gives 608 J/kg — consistent with
   $c_p$ ≈ 6.0 kJ/kg·K at that state (the table value implies an
   impossible 56 kJ/kg·K). The translation is therefore faithful; the
   deviation sits in the original's tabular backend, 0.1 K from the dome.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the condenser branch of `HexCstPinch` from LaboThapPy,
file `labothappy/component/heat_exchanger/hex_cstpinch.py`, commit `f03f7f47`.
LaboThapPy — https://github.com/PyLaboThap/LaboThapPy —
Copyright (C) 2025 Université catholique de Louvain (UCLouvain), Université
de Liège (ULiège), Université de Mons (UMONS). Original authors: B. Chaudoir,
E. Neven, T. Janod (see `AUTHORS.txt`).
Changes: translated from Python to CoolSolve; the scalar `brentq`
root-find on `P_sat` replaced by an unknown closed by the pinch equation;
the `max(0,·)` zone clamps dropped (superheated-inlet / subcooled-outlet
regime fixed, verified for the shipped case); pressure drops kept at zero
(the example defaults); the `min` over pinch candidates kept as nested
`MIN`; evaporator branch not translated (see *Limitations*). Scientific
basis: none cited in the source beyond the pinch-design method; the
moving-boundary generalisation is Bell et al., Appl. Therm. Eng. 79 (2015).

Source files (not copied into the library):
`~/git/LaboThapPy/labothappy/component/heat_exchanger/hex_cstpinch.py`
(812 lines) and
`~/git/LaboThapPy/labothappy/component/examples/heat_exchanger/hex_cstpinch_example.py`
(default case `COND_CO2`); reference: URL above + path
`labothappy/component/heat_exchanger/hex_cstpinch.py`.
No student names or personal data involved.

## Conversion log

- **2026-10-05 — translation**: condenser branch of `system_cond`
  transcribed zone by zone (comments paraphrased from the original's own
  comments, marked "as in the original" where terse); temperatures in °C
  (LaboThapPy uses K); `DP_c`/`DP_h` omitted (= 0, the example defaults);
  16 post-processing state-array equations added for the diagrams (results
  unchanged). Level 2: rubric score 5 (51 equations, block of 18, arrays,
  multi-zone, curated guesses needed) lowered by one — small explicit
  design-point structure converging in 4 Newton iterations.
- **2026-10-05 — curated initials**: the shipped `.initials` file is
  seeded with the LaboThapPy reference solution; the block fails from
  default guesses (`LineSearchFailed`).

## Limitations and CoolSolve gaps

- **Condenser only.** The evaporator branch (`system_evap`) is not
  translated: it mirrors the condenser (roles of the streams swapped,
  pinch candidates at the bubble-point interface and the cold end); the
  same equation pattern applies.
- **Fixed regime**: superheated hot inlet and subcooled hot outlet are
  assumed (the original's `max(0,·)` clamps dropped). Out of this regime
  (e.g. two-phase hot supply) the zone duties lose meaning — add an
  explicit regime check before reuse.
- CoolSolve warns `T=30 looks like Fahrenheit` on the hot-supply property
  calls — spurious heuristic (30 °C is legitimate; values checked against
  CoolProp, exact agreement).

## Related models

- `CSL-0008` (*condenser_three_zones*, level 3): air-cooled condenser with
  fitted ε-NTU conductances per zone (off-design model); this model is the
  design-point counterpart (pinch imposed, pressure solved).
- `CSL-0002` (*counterflow_hx_oil_water*, level 1): single-phase
  counterflow exchanger (ε-NTU); no phase change, no pinch closure.
