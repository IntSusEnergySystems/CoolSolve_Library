# Heat exchanger with UA from the plate geometry (eps-NTU, Gnielinski)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0128`

A plate/pipe heat exchanger whose conductance-area product $AU$ is *computed*
from its geometry: the two film coefficients come from the Gnielinski
correlation family of LaboThapPy, and the plate wall conduction and the
fouling resistances are added in series. The duty and the outlet states then
follow from the eps-NTU relation of the selected flow arrangement. The model
translates the LaboThapPy component `HexeNTU` (plate/pipe branch) into
EES-language equations; it is the sizing counterpart of the library models
that prescribe the duty or the effectiveness (CSL-0126, CSL-0014).

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | Water (any single-phase CoolProp/EES fluid) |
| **Size** | 99 equations (largest block: 1) |
| **Source** | LaboThapPy (Apache-2.0/MIT), `labothappy/component/heat_exchanger/hex_eNTU.py` + `labothappy/correlations/convection/pipe_htc.py` + `labothappy/correlations/heat_exchanger/e_NTU.py`, commit `f03f7f47` |
| **Authors** | Basile Chaudoir, Marie Peeters, Elise Neven (ULiège Thermodynamics Laboratory; LaboThapPy contributors, see `AUTHORS.txt`) |
| **License** | MIT (translation with credits, roadmap decision D3) |
| **CoolSolve** | `0.3.0@7addbbc` — verified against the LaboThapPy component and against the TESPy test `test_labothappy_reference` (see *Verification*) |

## Problem statement

Size a water-to-water plate heat exchanger from its geometry only. The plate
pack is described by its length, width, height, casing thickness, number and
thickness of plates, the number of canals on each side, the plate
conductivity, the total heat-transfer area and the fouling resistance. The
inlet states, the mass flow rates and the flow arrangement are given. Compute
the two film coefficients, the conductance-area product $AU$, the number of
transfer units, the effectiveness, the duty and the two outlet states.

Default run (the case of the TESPy test named in the task card): hot water
0.014 kg/s at 90 °C, cold water 0.08 kg/s at 12 °C, both at 4 bar,
counterflow.

## Model

Plate geometry (canal thickness, canal flow areas and hydraulic diameter
exactly as in the LaboThapPy component example, which builds them from the
SWEP plate-exchanger geometry):

- $t_{canal} = [(H - 2\,t_{casing}) - n_{plates}\,t_{plate}]/(2\,n_{canals})$,
  $A_{canal} = t_{canal}\,(W - 2\,t_{casing})\,n_{canals}$,
  $D_h = 4\,t_{canal}\,W/(2\,t_{canal} + 2\,W)$;
- as in the original component, one hydraulic diameter (the hot-side one) is
  used for both streams.

Film coefficients, from the Gnielinski family of the original (the branch is
selected on the Reynolds number, `Re = G D_h / mu`):

- laminar (`Re < 2300`): $Nu = 3.657 + 0.0677\,Re\,Pr\,(D_h/L)^{1.33}/[1 + 0.1\,Pr\,(Re\,D_h/L)^{0.3}]$;
- transition ($2300 \le Re \le 10000$): $f = (1.82\log_{10}Re - 1.64)^{-2}$,
  $Nu = (f/8)(Re-1000)Pr/[1 + 12.7\,(f/8)^{1/2}(Pr^{2/3}-1)]\,(1 + (D_h/L)^{2/3})$;
- turbulent (`Re > 10000`): $Nu = 0.027\,Re^{0.8}Pr^{1/3}(\mu/\mu_w)^{0.14}$;
- $h = Nu\,k/D_h$.

Conductance-area product and duty:

- $1/AU = 1/(h_H A) + 1/(h_C A) + t_{plate}/(k_{plate}A) + R_{foul}/A$;
  (the documentation of the original writes this as a *product* of the four
  resistances, a typo; the code sums them, as here — see *Conversion log*);
- $C_{min}$, $C_{max}$ from $m\,c_p$ with $c_p$ at the inlet state,
  $C_r = C_{min}/C_{max}$, $NTU = AU/C_{min}$;
- $\varepsilon$ from the relation of the selected flow arrangement (counter,
  parallel, crossflow unmixed, crossflow with $C_{min}$ mixed, 1-2 and
  $n$-pass shell-and-tube) — all six are computed in the main program;
- $Q_{max} = \min[\dot m_C(h_C(T_{su,H},P_{su,C}) - h_{su,C}),\ \dot m_H(h_{su,H} - h_H(T_{su,C},P_{su,H}))]$,
  $Q = \varepsilon Q_{max}$ (the enthalpy form of the code; the documented
  approximation $C_{min}(T_{su,H}-T_{su,C})$ is also printed as
  `Q_max_capacity`);
- outlet states from the energy balance on each stream, pressures unchanged
  (`P_ex_H = P_su_H`, `P_ex_C = P_su_C`, as in the original).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_su_H` / `P_su_H` / `M_dot_H` | 90 °C / 400 kPa / 0.014 kg/s | `h_H`, `h_C` film coefficients | 379.7 / 339.9 W/(m²·K) |
| `T_su_C` / `P_su_C` / `M_dot_C` | 12 °C / 400 kPa / 0.08 kg/s | `AU` conductance-area product | 132.07 W/K |
| `A_htx` | 0.752 m² | `NTU` / `C_r` / `eps` | 2.2437 / 0.1756 / 0.86665 |
| plate pack (see file) | B35TM0x10/1P-like | `Q_dot` duty | 3 961.5 W |
| `R_foul` | 1.0E-4 m²·K/W | `T_ex_H` / `T_ex_C` | 22.40 °C / 23.83 °C |

## How to run

```bash
coolsolve ./hx_eps_ntu_plate_pipe.eescode
```

No `.initials` file and no `coolsolve.conf` are needed: every quantity is
explicit (largest block 1, system square, solver converges in 0 iterations).
Change `Flow_Type$` to `'ParallelFlow'`, `'CrossFlow_Unmixed'`,
`'CrossFlow_Mixed'`, `'ShellAndTube_1_2'` or `'ShellAndTube_n_passes'`
(then `n_shell_pass`) to change the arrangement; change the plate geometry and
`R_foul` to size another exchanger.

## Results

Equations: 99, largest block 1, system square. Film coefficients
`h_H` = 379.68 W/(m²·K), `h_C` = 339.86 W/(m²·K) (both laminar, `Re_H` = 94.3,
`Re_C` = 137.3); `AU` = 132.070 W/K, `C_min` = 58.86 W/K, `C_r` = 0.1756,
`NTU` = 2.24366, `eps` = 0.86665, `Q_max` = 4 571.0 W (capacity-rate form
4 591.4 W), `Q_dot` = 3 961.5 W, `T_ex_H` = 22.402 °C, `T_ex_C` = 23.832 °C.
Effectiveness of the six arrangements for the same `NTU` and `C_r`:
counterflow 0.86665, parallel 0.78980, crossflow unmixed 0.85211, crossflow
`C_min` mixed 0.82731, 1-2 shell-and-tube 0.82551, 2-pass shell-and-tube
0.96299 (from `hx_eps_ntu_plate_pipe.sol`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7):
     ![T-s diagram of the two water streams](figures/hx_eps_ntu_plate_pipe_ts.png)
     T-s diagram of the counterflow plate exchanger: hot supply → hot outlet, cold supply → cold outlet. -->

## Verification

Two independent references, both re-run in a throw-away virtual environment
under `work/` (CoolProp 8.0.0, `pip install -e ~/git/LaboThapPy` and
`pip install -e ~/git/tespy`, `~/git/LaboThapPy` commit `f03f7f47`,
`~/git/tespy` commit `19425523`; the folder was deleted afterwards).

**1. LaboThapPy `HexeNTU`, same inputs and geometry.** The reference values are
the outputs printed by `HX.print_results()` (`work/hx_eps_ntu_plate_pipe/ref_ltp.py`,
water/water, counterflow, the plate geometry and `fouling = 1e-4 m²K/W` of the
model file). Comparison:

```bash
python3 tools/compare_solution.py models/components/heat_exchangers/hx_eps_ntu_plate_pipe/hx_eps_ntu_plate_pipe.sol \
    work/hx_eps_ntu_plate_pipe/reference_ees_variables.csv --ees-units --all --rtol 1e-3
```

| Variable | LaboThapPy | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `Q_dot` [W] | 3 961.4688 | 3 961.4690 | 4.7e-08 |
| `T_ex_H` [K] | 295.5515531 | 295.5515697 | 7.4e-07 |
| `T_ex_C` [K] | 296.9820266 | 296.9819848 | 1.8e-06 |
| `h_ex_H` [J/kg] | 94 332.553 | 94 332.554 | 1.1e-07 |
| `h_ex_C` [J/kg] | 100 313.729 | 100 313.905 | 1.8e-06 |
| `P_ex_H`, `P_ex_C` [Pa] | 400 000 | 400 000 | 0 |
| `m_dot_H`, `m_dot_C` [kg/s] | 0.014, 0.08 | 0.014, 0.08 | 0 |

`9 common variables, 0 differ (rtol=0.001)` — maximum relative difference
**1.8e-06** (`h_ex_C`); `Q_dot` agrees to 4.7e-08. The temperatures of the
reference are in K and are converted by `--ees-units`. Both codes use the same
CoolProp backend and the same property call state (inlet), so the residuals
come only from the Newton tolerance of the enthalpy inversion.

**2. TESPy test `test_labothappy_reference`** (the reference named in the
task card, `tests/test_components/test_ntu_heat_exchanger.py`): water/water,
0.014 kg/s at 90 °C, 0.08 kg/s at 12 °C, 4 bar, counterflow, `UA = 132.069586 W/K`.
The test passes in the virtual environment (`1 passed, 24 deselected`) and
expects `Q = 3961.899 W` (`rel = 2e-3`), `T_H,out = 295.54 K` and
`T_C,out = 296.98 K` (`abs = 0.1`). Against the model:

| Quantity | TESPy test | CoolSolve (geometry-based `AU`) | deviation | test tolerance |
|---|---:|---:|---:|---:|
| `Q_dot` | 3 961.899 W | 3 961.469 W | 1.1e-04 (rel.) | 2e-3 |
| `T_ex_H` | 295.54 K | 295.5516 K | 0.0116 K | 0.1 K |
| `T_ex_C` | 296.98 K | 296.9820 K | 0.0020 K | 0.1 K |

The TESPy component takes `UA` as an input and uses *effective* heat
capacities $m\,(h_2-h_1)/(T_2-T_1)$ between its inlet and outlet states, while
LaboThapPy (and this model) evaluate $c_p$ at the inlet states; the test itself
notes this and allows a relative tolerance of 2e-3 for the duty. The `UA` of
132.0696 W/K of the test is reproduced by the model geometry to 1e-10 relative
(`AU = 132.0695860402 W/K`).

## Source and attribution

```text
This CoolSolve model is a translation (EES-compatible language, equation-oriented)
of the component HexeNTU from LaboThapPy, file
labothappy/component/heat_exchanger/hex_eNTU.py, with the correlation families
labothappy/correlations/convection/pipe_htc.py (gnielinski_pipe_htc) and
labothappy/correlations/heat_exchanger/e_NTU.py (e_NTU), commit f03f7f47.
LaboThapPy - https://github.com/PyLaboThap/LaboThapPy
Copyright (C) 2025 Universite catholique de Louvain (UCLouvain), Universite de Liege (ULiege),
Universite de Mons (UMONS). Original authors of the component: B. Chaudoir, M. Peeters,
E. Neven (see AUTHORS.txt); the e_NTU relations are signed "marie" (M. Peeters).
Changes: translated from Python to CoolSolve; the connector/parameter plumbing of the
Python component became plain simultaneous equations; the flow arrangement is chosen
by a string variable instead of params['Flow_Type']; two unused parameters of the
component (V_HTX, co_pitch, chevron_angle) were dropped.
Scientific basis: eps-NTU relations as in F. P. Incropera, Fundamentals of Heat and
Mass Transfer (comment of the original e_NTU.py); Gnielinski and Sieder-Tate as in
W. Rohsenow, J. Hartnett, Y. Cho, Handbook of Heat Transfer, 3E, McGraw-Hill, 1998;
laminar entrance Nusselt number as in H. D. Baehr, K. Stephan, Heat and Mass Transfer,
Springer, 2013.
```

Plate geometry values (`A_htx`, `L_HTX`, `W_HTX`, `H_HTX`, `t_casing`,
`n_plates`, `t_plate`, `k_plate`, canals per side) are those of the component
example `labothappy/component/examples/heat_exchanger/hex_eNTU_example.py`
(SWEP-style B35TM0x10/1P plate exchanger), manufacturer data of the original
repository; `R_foul = 1.0E-4 m²·K/W` is chosen here to reproduce the
`UA = 132.0696 W/K` of the TESPy reference case (the reference quotes `UA`
only, without its geometry).

The correlations of the library that hold the same relations are **CSL-0087**
(`Nu_Gnielinski`, `Nu_Sieder_Tate` — turbulent internal flow), **CSL-0091**
(`Nu_laminar_entry_Baehr_Stephan` — laminar entry region) and **CSL-0090**
(`calc_Cmin`, `calc_Cmax`, `eps_counterflow`, `eps_parallel`,
`eps_crossflow_approx`, `eps_crossflow_mixed_Cmin` — eps-NTU relations); they
are cited in the comment blocks of the functions of this file. The shell-and-tube
relations (`ShellAndTube_1_2`, `ShellAndTube_n_passes`) of the original are not
in CSL-0090 yet.

## Conversion log

- **2026-10-08 — translation (T-TRANSLATE, card C-173)**: component class
  `HexeNTU` flattened into plain equations: the connector objects (`su_H`,
  `su_C`, `ex_H`, `ex_C`, `Q_hex`) became the state variables `T_su_*`,
  `P_su_*`, `M_dot_*`, `h_ex_*`, `T_ex_*`, `P_ex_*`, `Q_dot`; the parameter
  dictionary became the input block; `params['Flow_Type']` became
  `Flow_Type$`. `V_HTX`, `co_pitch` and `chevron_angle` are required parameters
  of the component but are not used by `solve()` — dropped (dead data). The
  three branch correlations and the six eps-NTU relations are one EES
  `FUNCTION` each (`Nu_Stephan_Preusser_HX`, `Nu_Gnielinski_transition_HX`,
  `Nu_Sieder_Tate_HX`, `h_conv_pipe_htc`, `e_NTU`, plus `calc_Cmin`,
  `calc_Cmax`, `calc_Q_max` for the `min`/`max` operations of the original) and
  all of them are called from the main program (each Nusselt branch and each
  flow arrangement is printed as a diagnostic).
- **2026-10-08 — corrected branch selection in `h_conv_pipe_htc`**: the original
  writes `if Re > 10000: ... if Re < 2300: ... else: ...`, so the turbulent
  Sieder-Tate value is always overwritten by the transition Gnielinski value
  (the `else` belongs to the second `if`). The three branches are kept here as
  the original intends them. Impact: none on the reference case
  (`Re_H` = 94.3 and `Re_C` = 137.3, laminar branch in both codes); for
  turbulent flow the model now uses the Sieder-Tate branch the original names.
- **2026-10-08 — `Q_max`**: the documentation page of the original gives
  `Q_max = C_min*(T_H,in - T_C,in)`, the code uses the minimum of the two
  enthalpy differences; the code is translated (it is what produced the
  reference values) and the documented form is kept in the model as
  `Q_max_capacity` (4 591.4 W against 4 571.0 W, 0.45 %).
- **2026-10-08 — documentation typo**: the Sphinx page of the original writes
  `1/AU` as a *product* of the four resistances; the code sums them. The
  summation (the physically correct series resistance) is used.
- **2026-10-08 — string branches**: `ELSEIF` is not available in CoolSolve (see
  *Limitations*), so the flow-arrangement dispatch is a nested
  `IF ... ELSE IF ... ENDIF` chain; the error branch keeps
  `CALL ERROR` with a literal message (string concatenation inside `CALL ERROR`
  is not evaluated by CoolSolve either). Everything else is standard EES.
- **2026-10-08 — state points**: the arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`
  (1 hot supply, 2 hot outlet, 3 cold supply, 4 cold outlet) were added for the
  CoolSolve diagram overlay; they do not change the results.
- **Level**: taxonomy §3 score 1 (99 equations) + 0 (largest block 1) + 1
  (functions) + 0 (no multi-zone/coupled components) + 1 (correlation-based,
  semi-empirical `AU` from geometry and fouling) + 0 (no curated guesses) = 3 →
  level 2.

## Limitations and CoolSolve gaps

Physical limitations, as in the original component: steady state, single
phase (no phase change, no condensation/evaporation), no pressure drop, no
heat loss to the environment, all properties at the inlet states, one
hydraulic diameter for both streams, a single fouling resistance for the whole
surface, and the effectiveness relations are singular at `C_r` = 1 (counterflow)
and at `NTU` = 0. The `ShellAndTube_n_passes` relation of the original is
*not* the classical one: with `n_shell_pass` = 2 it gives a higher
effectiveness (0.963) than the 1-2 relation (0.826), so it should be used with
care. The laminar branch needs `Re < 2300`; the transition branch
needs `2300 <= Re <= 10000`; validity ranges of `Pr` are those checked by the
original (laminar `Pr >= 0.6`, turbulent `0.1 <= Pr <= 1000`, `Re <= 1E6`).
No registered CoolSolve gap blocks this model (`missing_features` is empty).
Two known CoolSolve limitations of the register were met and worked around
(nothing new is registered): the single-word `ELSEIF` is accepted but its
condition is ignored — the dispatch is a nested `IF`/`ELSE` chain instead,
the behaviour recorded in `../CoolSolve/docs/model_library_support.md`
(note of 2026-10-06, card C-111 / `CSL-0102`, and `CS-GAP-ELSEIF-CHAIN`
for the two-word `ELSE IF` ladder) — and string concatenation inside
`CALL ERROR` is not evaluated (the message is a literal).

## Related models

- CSL-0090 (`hx_effectiveness_ntu`) — the eps-NTU relations of the `ht` library,
  for counter, parallel and crossflow; same closed forms as `e_NTU` here.
- CSL-0087 (`internal_turbulent_nusselt`) — `Nu_Gnielinski` and `Nu_Sieder_Tate`,
  the two turbulent Nusselt relations used by `h_conv_pipe_htc`.
- CSL-0091 (`internal_laminar_and_curved_nu`) — laminar entry-region Nusselt
  numbers, including the fully developed value 3.657 used by the laminar branch.
- CSL-0126 (`hx_constant_effectiveness`) — same exchanger with an imposed
  effectiveness instead of a computed `AU`.
- CSL-0014 (`hx_constant_pinch`) — the LaboThapPy condenser translation of the
  same library, for a phase-changing plate exchanger.