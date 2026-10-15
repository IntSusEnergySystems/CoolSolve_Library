# CO2 transcritical booster refrigeration system (supermarket)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0145`

A CO2 (R744) booster refrigeration system of the kind used in supermarkets,
after the TESPy model-library notebook `co2_cycle.ipynb`: an LT evaporator
(13 bar, 25 kW) and an MT evaporator (26 bar, 75 kW) in parallel, a receiver
with flash-gas by-pass at 32 bar, an LT compressor (13 → 26 bar) and an MT
compressor (26 → gas-cooler pressure), a heat-recovery heat exchanger
(counter-flow, 5 K pinch, water heated from 30 °C to 55 °C) and a gas cooler.
At 57.3 bar / 15 °C outlet the heat rejection is subcritical (Case Study 1 of
the source book chapter); raising the gas-cooler pressure above the critical
pressure (100 bar, 35 °C outlet) gives the transcritical summer case.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R744, Water |
| **Size** | 157 equations, largest block 1 (fully explicit once states are given) |
| **Source** | TESPy `docs/model_library/co2_cycle.ipynb` ([oemof/tespy](https://github.com/oemof/tespy), commit `19425523`) |
| **Authors** | Francesco Witte (TESPy lead developer); cycle layout and boundary conditions from the book chapter *Modelling of a commercial refrigeration system in Python* by Francesco D'Ettorre and Christian Heerup (2026) |
| **License** | MIT (TESPy), library license for the translation |
| **CoolSolve** | v0.3.0@e635c85 — verified against a re-run of the source notebook (see *Verification*) |

## Problem statement

Reproduce Case Study 1 of the book chapter: LT evaporator at 13 bar
(≈ −33 °C) with 25 kW and MT evaporator at 26 bar (≈ −10.6 °C) with 75 kW
cooling load, both with 10 K of outlet superheating; receiver at 32 bar; MT
compressor with η_s = 0.80 discharging at 57.3 bar; LT compressor with
η_s = 0.85 discharging at the MT pressure; heat-recovery heat exchanger with
5 K pinch (dp = 0 on both sides) heating water from 30 °C to 55 °C at 3 bar;
gas cooler (dp = 0) with 15 °C outlet. Compute the mass flows (including the
flash gas by-passed from the receiver), the compressor powers, the heat
recovered, the gas-cooler duty and the COP. Then switch to transcritical
operation (gas cooler 100 bar, 35 °C outlet).

## Model

The TESPy network (17 CO2 connections `c1`…`c17`, 2 water connections
`w1`, `w2`) is translated into simultaneous equations; the connection labels
are kept as variable suffixes (`m_c3`, `h_c10`, `T_c6`, …). Python solver
plumbing (network objects, `CycleCloser`, iterative recovery) disappears:
every component becomes one or two equations.

- **Valves** (`hp-valve`, `by-pass-valve`, `lt-exp-valve`, `mt-exp-valve`,
  TESPy `Valve`): isenthalpic, `h_out = h_in`; outlet temperature from
  `(P, h)`.
- **Receiver** (TESPy `DropletSeparator`): outlets are saturated liquid and
  saturated vapour at the receiver pressure; the inlet vapour fraction is the
  lever rule `x_flash = (h_c3 − h′)/(h″ − h′)` (EES `QUALITY` not needed).
- **Splitter/merges**: mass balances, adiabatic energy balances, equal
  pressures (this is what fixes the LT compressor discharge pressure at the
  MT evaporation pressure, 26 bar).
- **Evaporators** (TESPy `SimpleHeatExchanger` with `pr = 1`, `Q` given):
  `Q̇ = ṁ·Δh` with the load imposed; outlet superheating `td_dew = 10 K`
  above dew point.
- **Compressors** (TESPy `Compressor` with `eta_s`): `(h_out − h_in)·η_s =
  h_out,s − h_in` with `h_out,s = h(s_in, p_out)`.
- **Heat-recovery heat exchanger** (TESPy `SectionedHeatExchanger`,
  `dp1 = dp2 = 0`, `td_pinch = 5`, counter-flow): CO2-side duty = water-side
  duty, and the pinch `T_c11 = T_w1 + 5 K`. TESPy discretises this component
  into 51 sections of equal heat transfer and imposes `min(T_hot,i − T_cold,i)
  = td_pinch`; for both shipped cases the minimum sits at the CO2-outlet /
  water-inlet end (checked numerically on the discretised profile: minimum
  5.0000 K at section 1, ΔT rising monotonically towards the hot end, 13.55 K
  in Case Study 1), so the pinch equation is applied there. This relies on
  the monotonic decrease of ΔT with duty at the cold end, which holds because
  the CO2 isobaric specific heat decreases with temperature over the range of
  the exchanger.
- **Cycle closure** (TESPy `CycleCloser`): not needed; the mass-flow set is
  closed by the receiver/splitter/merge balances (`m_c3` follows from the
  evaporator flows and the flash fraction, and `m_c9 = m_c3` is implied).
- **Performance indicators** (as in the original): `COP = (Q̇_LT + Q̇_MT −
  Q̇_hrhx)/(Ṗ_LT + Ṗ_MT)` — the recovered heat counts as useful — and
  `flash_gas_fraction = ṁ_c16/ṁ_c3`.

State points are exported as arrays `T[i]`, `P[i]`, `h[i]`, `s[i]`
(`i` = 1…16, process order, TESPy connection labels in the comments) for the
CoolSolve diagram overlay.

## Results (Case Study 1, baseline `.sol`)

| Quantity | TESPy (notebook re-run) | CoolSolve | rel. diff |
|---|---|---|---|
| COP | 4.942799 | 4.942799 | 7.4e-12 |
| Total compressor power | 25.1679 kW | 25.1679 kW | 1.9e-11 |
| Heat recovery `Q̇_hrhx` | −24.3996 kW | −24.3996 kW | 6.0e-11 |
| Flash gas fraction | 0.189657 | 0.189657 | 4.1e-11 |
| Discharge temperature `T_c10` | 68.5544 °C | 68.5544 °C | 3.6e-11 |
| Gas cooler duty `Q̇_gc` | −100.768 kW | −100.768 kW | 9.4e-12 |
| Mass flow `m_c3` | 0.48140 kg/s | 0.481403 kg/s | 6e-6* |
| LT flow `m_c5 = m_c7` | 0.09806 kg/s | 0.0980580 kg/s | 2e-5* |
| MT flow `m_c12 = m_c14` | 0.29204 kg/s | 0.292043 kg/s | 1e-5* |
| Flash gas `m_c16` | 0.09130 kg/s | 0.0913016 kg/s | 2e-5* |
| Water flow `m_w` | 0.23350 kg/s | 0.233502 kg/s | 8e-6* |
| Receiver temperature `T_c3` | −3.189 °C | −3.18862 °C | 1.2e-4* |

\* the printed TESPy connection table carries only 5 significant digits; the
differences are its rounding, not model differences.

Energy balance of the solution: `|Q̇_gc| = Q̇_LT + Q̇_MT + Q̇_hrhx + Ṗ_LT +
Ṗ_MT` = 100.768 kW (closed to 1e-10 relative).

Transcritical check (gas cooler 100 bar, 35 °C outlet — inputs changed in a
work copy of the file): COP = 4.617918, total power = 55.2804 kW, heat
recovery = −155.2804 kW, flash gas fraction = 0.404557, discharge temperature
= 115.4173 °C, gas-cooler duty = 0 (the HRHX alone reaches the 35 °C gas
cooler inlet temperature, as in the notebook). All agree with the notebook
re-run to ≤ 2.3e-9 relative.

## Verification

The source notebook `co2_cycle.ipynb` was re-run in a throw-away virtual
environment (`work/c190/venv`, tespy 0.11.3.dev0 installed from the local
clone at commit `19425523`, CoolProp 8.0.0): the model class and Case Study 1
inputs were executed as in the notebook, the KPIs collected with the
notebook's own `get_results` and the connection table printed from the solved
network. `work/c190/compare_with_tespy.py` compares them with the CoolSolve
`.sol`: maximum relative difference 6.0e-11 over the full-precision KPIs
(2.3e-9 for the transcritical case). Both sides use CoolProp with the same
equation of state, so this validates the equation translation. The work
folder (including the venv) was deleted after the comparison; the numbers are
recorded here and in `model.json`.

## Source and attribution

- Original model: TESPy notebook `docs/model_library/co2_cycle.ipynb`
  ([oemof/tespy](https://github.com/oemof/tespy), commit `19425523`), by
  Francesco Witte and the TESPy contributors (MIT licence). Local clone:
  `~/git/tespy`.
- Cycle layout, component set and boundary conditions: book chapter
  *Modelling of a commercial refrigeration system in Python*, Francesco
  D'Ettorre and Christian Heerup (2026); the work in the chapter was funded
  by ELFORSK (project "Super-Integration: Sector-coupled flexible
  supermarkets", ELF231-511591), as acknowledged in the notebook.
- Translation to EES/CoolSolve equations: this library (task C-190,
  batch B-12), published under the library license.

## Conversion log

- Physics translated to simultaneous equations; TESPy components mapped as
  described under *Model*. No correlations were taken from libraries (fixed
  η_s compressors, pinch-conditioned heat exchanger), so no external
  function is cited beyond TESPy itself.
- `CycleCloser` removed: the mass-flow closure is implied by the receiver,
  splitter and merge balances (adding it would over-determine the system).
- `DropletSeparator` flash: vapour fraction by the lever rule with
  `ENTHALPY(fluid$, P=…, x=0/1)` instead of the `QUALITY(P, H)` call.
- `SectionedHeatExchanger` `td_pinch` (minimum over 51 equal-heat sections)
  replaced by the end-point pinch equation `T_c11 = T_w1 + td_pinch`;
  justified and checked in *Model* above ( CoolSolve has no section-wise
  discretisation; a `min()` over a discretised profile is not expressible as
  simultaneous equations).
- Units: the notebook works in bar/°C/kW (TESPy defaults); converted to
  SI-°C-Pa-J (pressures ×1e5, powers ×1e3, enthalpies ×1e3).
- State-point arrays `T[i]`, `P[i]`, `h[i]`, `s[i]` (16 points, process
  order) added for the diagram overlay (post-processing, no effect on the
  results).

## Level justification (taxonomy §3 score)

Equations 157 (1) + largest block 1 (0) + arrays present (1) + ≥ 3 coupled
components (1) + no semi-empirical/off-design physics (0) + no curated
guesses needed (0) = score 3 → level 2.

## Related models

- `CSL-0013` `heat_pump_basic_tespy` — other TESPy translation (single-stage
  heat pump).
- `CSL-0014` `hx_constant_pinch` — constant-pinch heat-exchanger component.

![placeholder: P-h or T-s diagram of the cycle, to be made by the maintainer](figures/)

## Limitations

- Fixed isentropic efficiencies; no compressor map, no off-design.
- The pinch equation assumes the minimum temperature difference at the
  CO2-outlet end (valid for the shipped cases; re-check if the boundary
  conditions move far from them).
- The notebook's sensitivity sweep and pymoo optimisation of the gas-cooler
  and receiver pressures are solver plumbing, not translated: run CoolSolve
  parametric studies on `p_c10` and `p_c3` instead.
