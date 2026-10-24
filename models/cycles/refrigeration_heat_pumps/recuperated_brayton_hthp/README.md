# Recuperated Brayton high-temperature heat pump (air / HITEC molten salt)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0254`

Steady design point of an air-cycle (Brayton) high-temperature heat pump: a
compressor raises ambient air to about 1.48 bar and 300 °C, the hot air gives
1 MW to a molten-salt (HITEC) loop heating it from 235 °C to 290 °C, and a
gas-gas recuperator preheats the ambient air with the turbine exhaust before
it is released to atmosphere. Translated from a TESPy (Python) model of a DTU
case study; the TES-integrated and intercooled layouts of the source are not
translated (see *Conversion log*).

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | Air; HITEC molten salt (tabulated incompressible in the source, cp fit here) |
| **Size** | 65 equations (largest block: 8) |
| **Source** | [SamueleGrandinDTU/recuperated_Brayton_HTHP](https://github.com/SamueleGrandinDTU/recuperated_Brayton_HTHP) (work in progress, commit `fbc50b4`), design-point model `main/standalone_base_recup_hthp.py` |
| **Authors** | Samuele Grandin (DTU) |
| **License** | No LICENSE file in the original repository (README silent); credited and linked, published in this library with full credit. Library version: MIT |
| **CoolSolve** | v0.4.0 — verified against a rerun of the source (see *Verification*) |

## Problem statement

Design-point case study of the source repository: with the compressor and
turbine isentropic efficiencies (0.80 / 0.90), the recuperator effectiveness
(0.94), the sink exchanger terminal temperature differences (10 K upper,
7 K lower), the HITEC inlet/outlet temperatures (235/290 °C) and the useful
heat (1 MW) imposed, compute the cycle: air mass flow, salt mass flow, the
pressure ratio, the compressor and turbine powers and the COP.

## Model

Air loop (states numbered as the source connections `0`…`5`; no pressure drop
anywhere: `pr1 = pr2 = 1` for both exchangers):

- `0` ambient air, 15 °C, 1 bar → recuperator cold side → `1` compressor inlet;
- `1 → 2` compressor (isentropic efficiency 0.80);
- `2 → 3` "sink" gas-to-HITEC exchanger: `T_2 = T_t2 + ttd_u` (300 °C),
  `T_3 = T_t1 + ttd_l` (242 °C), `Q_dot = m_air*(h_2 - h_3) = 1 MW`;
- `3 → 4` recuperator hot side: `h_4 = h_3 - (h_1 - h_0)`;
- `4 → 5` turbine back to 1 bar (isentropic efficiency 0.90).

The recuperator effectiveness is the **cold-side, enthalpy-based** definition
of TESPy (`eff_cold`): `(h_1 - h_0)/(h_3 - h_0) = eff_cold`. Because the
temperatures at the compressor inlet and outlet are fixed by the recuperator
effectiveness and the sink terminal differences, the isentropic-efficiency
equation `(h_2s - h_1)/(h_2 - h_1) = eta_s_compressor` is what **determines
the pressure ratio** (an output: 1.476).

HITEC molten salt: the source ships it as tabulated incompressible data
(TESPy `IncompressibleFluidWrapper`, 4 points 200–350 °C). Its heat capacity
is exactly linear in T (`cp = 1560.1 + 0.002*(T[K] - 473.15)` J/kg-K on all
four data points), so the enthalpy uses the exact quadratic integral of that
fit; only the energy balance `Q_dot = m_HITEC*(h_t2 - h_t1)` is needed.

`COP = Q_dot/(W_dot_compressor - W_dot_turbine)` (compressor and turbine on
the same shaft, as in the source). Air is the EES substance name `Air`
(CoolSolve/CoolProp air properties, the same reference as TESPy's `air`).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `Q_dot` useful heat | 1 MW | `P_2` pressure level | 1.476 bar |
| `T_0`, `P_0` ambient air | 15 °C, 1 bar | `m_air` air mass flow | 16.594 kg/s |
| `T_t1`, `T_t2` HITEC | 235 / 290 °C | `m_HITEC` salt mass flow | 11.653 kg/s |
| `ttd_u`, `ttd_l` sink TTDs | 10 / 7 K | `W_dot_compressor` | 1.230 MW |
| `eta_s_compressor` | 0.80 | `W_dot_turbine` | 0.477 MW |
| `eta_s_turbine` | 0.90 | `T_1` recuperator cold outlet | 228.6 °C |
| `eff_cold` | 0.94 | `COP` | 1.329 |

## How to run

```bash
coolsolve ./recuperated_brayton_hthp.eescode
```

`.initials` gives guess values (needed: property calls fail from the default
guesses of 1.0). `recuperated_brayton_hthp_benvenuti.eescode` is the
validation case of the source (`T_t1 = 193 °C`, "Benvenuti recuperated
configuration" reference data in `data/processed/` of the source
repository); it is regression-tested as `CSL-0254:benvenuti`.

## Results (design case)

| Quantity | TESPy rerun | CoolSolve |
|---|---:|---:|
| `T_1` compressor inlet [°C] | 228.6 | 228.56 |
| `P_2` / `T_2` compressor outlet | 1.476 bar / 300 °C | 1.4764 bar / 300 °C |
| `T_3` sink hot outlet [°C] | 242.0 | 242.0 |
| `T_4` turbine inlet [°C] | 28.84 | 28.86 |
| `T_5` turbine exhaust [°C] | 0.17 | 0.18 |
| `m_air` [kg/s] | 16.594 | 16.5937 |
| `m_HITEC` [kg/s] | 11.653 | 11.6533 |
| `w_compressor` [kJ/kg] | 74.08 | 74.10 |
| `w_turbine` [kJ/kg] | 28.74 | 28.75 |
| `q_sink` [kJ/kg] | 60.26 | 60.26 |
| `COP` [-] | 1.329 | 1.3288 |

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1…6 = source connections
`0`…`5`) give the cycle points for the CoolSolve diagram overlay
(no ideal-gas diagram yet, `CS-FEAT-DIAGRAM-IDEAL`).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram or
     parametric plot of the cycle, figures/recuperated_brayton_hthp_ts.png -->

## Verification

The source was re-run in a throw-away Python venv (TESPy + CoolProp, commit
`fbc50b4`, trimmed copy of `main/standalone_base_recup_hthp.py`: design-point
solve and tables only; the operational-strategy optimisations and LCOH steps
need pyomo/pandas data pipelines and are out of scope). Comparison above:
**maximum relative deviation 0.09 % over all compared quantities (most below
0.05 %), at the 4-digit print precision of the source** — same CoolProp air
properties on both sides. Energy balances close by construction
(`Q_dot = m_air*(h_2-h_3) = m_HITEC*(h_t2-h_t1)`); the COP 1.33 is below the
Carnot COP 2.05 between 288 K and 563 K (order of magnitude).

Validation variant (`benvenuti`): CoolSolve vs the TESPy rerun of the same
case agrees within 0.2 % on temperatures (0.02 % in K: `T_4` 26.37 vs
26.32 °C), 0.06 % on `P_2` (1.8821 vs 1.881 bar), 0.003 % on `m_air`
(9.6617 vs 9.662 kg/s). The source's own validation against the Benvenuti
reference CSV (`data/processed/Benvenuti_validation_recuperated.csv`) shows
deviations up to 14 K at point 3 (10.2 K at point 1): the upstream model
reproduces that reference only approximately (work in progress). The
CoolSolve model matches the TESPy rerun, not the Benvenuti CSV.

## Source and attribution

Translated from the TESPy model **`main/standalone_base_recup_hthp.py`**
(with `src/`, `src/input/*.json` specifications and the stored results of
`results/tables/`) of
[github.com/SamueleGrandinDTU/recuperated_Brayton_HTHP](https://github.com/SamueleGrandinDTU/recuperated_Brayton_HTHP)
(commit `fbc50b426924953f72cdee6c2555185b0861398b`, 2026-10-20), by
**Samuele Grandin** (DTU, author per the repository git history of the
translated files). The repository is work in progress and has **no LICENSE
file** (its README does not state a licence either); per the library
maintainer decision of 2026-10-22 it is published here with full credit and a
link to the original. Inventory candidate `LDS-008`.

## Conversion log

- **2026-10-22 — translation** (card C-281): the TESPy network becomes
  simultaneous equations; the Newton/tearing solver glue, plotting,
  operational-strategy optimisation (pyomo), LCOH and electricity-price
  analyses of the entry-point script are not part of the steady design point
  and were left out. The connection labels `0`…`5`, `t1`, `t2` of the source
  are kept as variable names (`T_0`…`T_5`, `T_t1`, `T_t2`); component
  parameters are the source's (`eta_s`, `ttd_u`, `ttd_l`, `eff_cold`,
  `Q = -1 MW` on the "sink" exchanger, `pr1 = pr2 = 1`).
- **Not translated** (documented, second step): the TES-integrated layouts
  (`main/tes_integr_*.py`, with storage tanks) and the intercooled variant
  (`main/standalone_interc_recup_hthp.py`); the four `examples/*.py`
  operational simulations (transient, electricity-price lookups, strategy
  optimisation = `CS-GAP-OPTIM` territory). The repository `main/README.md`
  describes them.
- **Units**: TESPy defaults (bar, °C, MW, kJ/kg) converted to SI-°C-Pa-J;
  HITEC cp fit in J/kg-K (exact on the 4 tabulated points).
- **Benvenuti variant**: same equations with `T_t1 = 193 °C` (the
  "Benvenuti" parameter set `standalone_base_recup_hthp_parameters_Benvenuti.json`
  of the source).
- **Level**: equations 65 → 1; largest block 8 → 1; no functions/arrays → 0;
  4 coupled components → 1; no off-design/dynamics → 0; curated guesses
  needed (`.initials`) → 1. Score 4 → **level 3**.

## Limitations

- Design point only; the source's part-load/operational behaviour (strategy
  optimisation, TES dispatch) is not covered.
- Air is modelled with CoolSolve's `Air` properties (CoolProp); the source
  uses the same CoolProp `air`, so no property-induced deviation is expected
  (and none is observed above print precision).
- HITEC is reduced to its heat capacity (the only property the design point
  uses); density/viscosity/conductivity data of the source are unused.
- Turbine exhaust at 0.2 °C: no internal heat exchanger below ambient is
  modelled; exhaust heat is simply rejected, as in the source.

## Related models

- `CSL-0212` *reverse_brayton_intercooling*: the reverse Brayton cycle on air
  (refrigeration, exercise); the same turbomachinery + recuperator skeleton
  running as a cooler instead of a heat pump.
- `CSL-0133` *heat_pump_propane_pinch*: vapour-compression high-temperature
  heat pump on propane, design point with imposed pinch points.
- `CSL-0039` *high_temp_heat_pump_pcm_storage*: another high-temperature heat
  pump case study (Zorlu geothermal plant, cyclopentane, PCM storage).
