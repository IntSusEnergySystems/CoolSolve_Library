# Evaporation of liquid methane in a tank

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0003`

A small property exercise on phase change: heat leaking into a tank of liquid
methane evaporates part of it, and the vapour is reheated before leaving. From
the measured drop of the liquid level, the model computes the evaporated mass
and the volumetric flow rate of the gas, using the real-fluid properties of
methane on both sides of the dome.

| | |
|---|---|
| **Category** | Fundamentals › Properties |
| **Fluids** | Methane (real fluid, not the ideal gas `CH4`) |
| **Size** | 24 equations, all explicit (largest block: 1): 12 for the model, 12 for the diagram state points |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition session 1, exercise 3 (EES file `R1_E3_2022.EES`) |
| **Authors** | TBD — exercise of the course *Thermodynamique appliquée* (repetition assistants N. Paulus and B. Dechesne per companion course files) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

A tank contains liquid methane at 500 kPa and has a cross-section of 0.5 m².
Because of a heat input to the methane, part of it evaporates and, in one
hour, the level drops by 30 mm. The vapour leaving the tank passes through a
heater and leaves it at 500 kPa and 275 K.

Compute the volumetric flow rate of the methane at the heater outlet.

## Model

- Mass evaporated over one hour, from the level drop and the saturated-liquid
  specific volume at the tank pressure:
  $m_{evap} = A_t\,\Delta h / v_l$, with $v_l = v(P_t, x=0)$;
- Volume of gas produced: $V_{gaz} = m_{evap}\, v_g$, with
  $v_g = v(P_r, T_r)$ the superheated-vapour specific volume at the heater
  outlet;
- Volumetric flow rate: $\dot v = V_{gaz}/\Delta t$.

The exercise note (kept in the model) asks for the real-fluid `methane` and
not `CH4`, which EES treats as an ideal gas.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `A_t` tank cross-section | 0.5 m² | `m_evap` mass evaporated in 1 h | 5.776 kg |
| `p_t` tank pressure | 500 kPa | `v_l` saturated-liquid specific volume | 2.597·10⁻³ m³/kg |
| `DELTAh` level drop in 1 h | 30 mm | `v_g` gas specific volume | 0.2818 m³/kg |
| `p_r`, `T_r` heater outlet | 500 kPa, 275 K (1.85 °C) | `q_v` volumetric flow rate | 4.520·10⁻⁴ m³/s |
| `DELTAt` duration | 3600 s | (= 1.63 m³/h) | |

## How to run

Open `methane_tank_evaporation.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./methane_tank_evaporation.eescode
```

The model is fully explicit; no guess values are needed.

## Results

| Variable | Value | Unit |
|---|---:|---|
| `V_evap` | 0.015 | m³ |
| `m_evap` | 5.7755 | kg |
| `V_gaz` | 1.6274 | m³ |
| `q_v` | 4.5205·10⁻⁴ | m³/s |

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 saturated liquid in the tank,
2 saturated vapour leaving the tank, 3 vapour at the heater outlet) give the
process path on the P-h or T-s diagram (CoolSolve *Diagram* tab, *Overlay
array path*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of methane with
     the evaporation + reheat path, figures/methane_tank_evaporation_ph.png -->

## Verification

Compared with the solution stored by EES in the source file
(`compare_solution.py --ees-units`, reference values converted kPa → Pa and
K → °C): all 12 variables of the original model agree; largest relative
deviation 2.6·10⁻⁵ (vapour specific volume `v_g`), i.e. both tools use the
same reference equation of state of methane within property tolerance.

| Variable | EES (converted) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `v_l` [m³/kg] | 2.59715·10⁻³ | 2.59716·10⁻³ | 2.8·10⁻⁶ |
| `m_evap` [kg] | 5.775562 | 5.775546 | 2.8·10⁻⁶ |
| `v_g` [m³/kg] | 0.2817605 | 0.2817678 | 2.6·10⁻⁵ |
| `q_v` [m³/s] | 4.52035·10⁻⁴ | 4.52045·10⁻⁴ | 2.3·10⁻⁵ |

This import is the test case of CoolSolve `docs/ees_import.md` §12, Example 3.

## Source and attribution

Solution of repetition exercise 3 (exercise 3.31 of the course textbook) of
the ULiège course *Thermodynamique appliquée* (MECA0002). The EES file names
no author (its `{$ID$}` tag is the laboratory's student/staff licence); the
companion course files attribute the repetition sessions to the assistants
N. Paulus and B. Dechesne (course by S. Quoilin) — to be confirmed by the
maintainer.

Source file (EES X10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R1/R1_E3_2022.EES`
(inventory candidate `TM-0380`, representative of a 4-file duplicate group:
`TM-0385` and `TM-0542` identical, `TM-0508` the 2017 version of the same
exercise).

## Conversion log

- **2026-10-04 — import** (`tools/ees_extract.py`, CoolSolve repository):
  decimal comma detected and converted by the tool (`0,5` → `0.5`, argument
  separator `;` → `,`); unit system `SI MASS DEG KPA K KJ` converted **by
  hand** to `SI MASS DEG PA C J`: `p_t` and `p_r` 500 kPa → `500E3 [Pa]`,
  `T_r` 275 K → `1.85 [°C]`. No energy term (no kJ variable) and no relation
  using an absolute temperature outside the property calls — nothing else to
  convert. Comments translated to English, standard header added, equations
  otherwise unchanged. Verified against the EES stored solution (see above).
- **2026-10-04 — diagram support**: block of 12 post-processing equations
  (state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`) added at the end of the model
  for the CoolSolve diagrams. State 2 (saturated vapour leaving the tank) is
  implied by the exercise statement but not computed by the original
  equations; it was added in post-processing only. The results of the model
  are unchanged.

## Limitations and CoolSolve gaps

- Thermally simple: the heat input is not modelled, only its effect (level
  drop) is given; the tank is at uniform pressure and the vapour leaves as
  saturated vapour (state 2).
- No CoolSolve gap found: unquoted EES fluid name (`volume(methane,…)`) and
  decimal-comma source both handled.

## Related models

None yet in the library.
