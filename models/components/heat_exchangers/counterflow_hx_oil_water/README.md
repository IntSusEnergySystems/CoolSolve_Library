# Counterflow heat exchanger — oil cooled by water (effectiveness–NTU)

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0002`

A counterflow heat exchanger cools an oil of constant specific heat with
water. The model applies the classical effectiveness–NTU method for
counterflow arrangement: capacity rates, capacity rate ratio, NTU,
effectiveness, then the outlet temperatures of both fluids and the transferred
power through the energy balances. It is the reference introductory model of
the library for the ε-NTU sizing/rating of a heat exchanger.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | Water (CoolProp properties); oil with constant c = 2100 J/(kg·K) |
| **Size** | 20 equations, all explicit (largest block: 1) |
| **Source** | ULiège exercise session (répétition 12, exercise 1) — CoolSolve example `exchangers1` + original EES file |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise, 2005); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the solution stored in the original EES file |

## Problem statement

A counterflow heat exchanger with a heat transfer area of 12.5 m² is used to
cool oil (c = 2100 J/(kg·K)) entering at 100 °C with water entering at 1 bar
and 20 °C. The oil and water flow rates are 2 and 0.48 kg/s respectively.
Knowing that the overall heat transfer coefficient is estimated at
400 W/(m²·K), what are the outlet temperatures of the two fluids and the
transferred power? Pressure drops in the heat exchanger are neglected.

## Model

Effectiveness–NTU method for a counterflow exchanger:

- capacity rates $dot C = dot m c$, with the water specific heat evaluated
  by CoolProp at the inlet state (T_w_su, P_w_su) and a constant oil c;
- capacity rate ratio $omega = dot C_{min}/dot C_{max}$ (water is the
  minimum-capacity fluid);
- $NTU = AU/dot C_{min}$ with $AU = U\\,A$;
- counterflow effectiveness
  $\\varepsilon = \\dfrac{1-\\exp(-NTU\\,(1-\\omega))}{1-\\omega\\,\\exp(-NTU\\,(1-\\omega))}$;
- transferred power $dot Q = \\varepsilon dot C_{min} (T_{oil,su}-T_{w,su})$,
  closed by the energy balance on each side.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `A` area | 12.5 m² | `epsilon` effectiveness | 0.836 |
| `U` overall coefficient | 400 W/(m²·K) | `NTU` | 2.49 |
| `c_oil` oil specific heat | 2100 J/(kg·K) | `Q_dot` transferred power | 134.4 kW |
| `T_oil_su` / `M_dot_oil` | 100 °C / 2 kg/s | `T_oil_ex` oil outlet | 68.0 °C |
| `T_w_su` / `P_w_su` | 20 °C / 1 bar | `T_w_ex` water outlet | 86.9 °C |
| `M_dot_w` water flow | 0.48 kg/s | `omega` / `C_dot_min` | 0.478 / 2008 W/K |

## How to run

Open `counterflow_hx_oil_water.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./counterflow_hx_oil_water.eescode
```

The system is fully explicit (20 blocks of 1 equation); no guess values are
needed.

## Results

| ε [-] | NTU [-] | ω [-] | Q̇ [kW] | T_oil,ex [°C] | T_w,ex [°C] |
|---:|---:|---:|---:|---:|---:|
| 0.836 | 2.490 | 0.478 | 134.4 | 68.01 | 86.91 |

The water, being the minimum-capacity fluid, heats up by 66.9 K (close to the
inlet-temperature difference of 80 K), while the oil only cools by 32 K.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric
     sweep plot, e.g. Q_dot and outlet temperatures vs M_dot_w (Parametric tab) -->

## Verification

Reference: the solution stored in the original EES file `exchangers1.EES`
(EES 9.920, `misc/EES_ok.zip` of the CoolSolve repository), compared with
`tools/compare_solution.py`:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `c_w` | 4183.003 J/(kg·K) | 4184.055 J/(kg·K) | 0.025 % |
| `NTU` | 2.4902 | 2.4896 | 0.025 % |
| `epsilon` | 0.83640 | 0.83631 | 0.010 % |
| `Q_dot` | 134 348.7 W | 134 368.6 W | 0.015 % |
| `T_oil_ex` | 68.012 °C | 68.007 °C | < 0.01 % |
| `T_w_ex` | 86.912 °C | 86.905 °C | < 0.01 % |

All 20 variables agree within 0.03 %; the small deviations all trace back to
the difference between the water cp of EES 9.920 and CoolProp at the water
inlet state (0.025 %), well within the property tolerance of
CoolSolve `docs/ees_import.md` §11.

## Source and attribution

Original exercise (in French) by **Vincent Lemort** (ULiège Thermodynamics
Laboratory), header `VL050517` — exercise session (*répétition*) 12,
exercise 1, 2005 (the header `VL050517` reads 2005-05-17); the exact course could not be identified from the file.
The model was rewritten in English as the CoolSolve example
`examples/exchangers1.eescode` by S. Quoilin; this library model supersedes
that example, which remains in the CoolSolve repository as a test case.

Sources (not copied into the library):

- CoolSolve example: `~/git/CoolSolve/examples/exchangers1.eescode`
  (inventory candidate `CSX-016`);
- original EES file with its stored solution:
  `~/git/CoolSolve/misc/EES_ok.zip` → `EES_ok/exchangers1.EES` (EES 9.920).

## Conversion log

- **2026-10-04 — import** (`tools/ees_extract.py` on the original
  `exchangers1.EES`): unit system already SI-°C-Pa-J (no conversion needed);
  EES licence tag (`Jean Lebrun`, the lab licence, not the author) and `{$PX$}`
  display tag removed; no tables, no external functions (only `cp`, `exp`,
  `min`, `max`, all CoolSolve built-ins); full stored solution available.
  Faithful run of the raw extraction: 20/20 variables identical to EES.
- **2026-10-04 — curation**: standard header added, comments translated from
  French to English, section titles added. No change to any equation or value.
- **2026-10-04 — correction (annotation only)**: the units annotation of
  `c_oil` read `[J/g.K]` in the original while the exercise statement says
  2100 J·kg⁻¹·K⁻¹ and the value 2100 J/(kg·K) is the one actually used
  (`C_dot_oil` = 4200 W/K = 2 kg/s × 2100 J/(kg·K)); the CoolSolve example
  had already fixed it. No numerical impact.
- **Decision — no diagram state arrays**: the workflow asks for `P[i]`, `h[i]`,
  `T[i]`, `s[i]` arrays on real-fluid models; here the hot fluid is an oil
  without CoolProp properties and the model uses a single water cp call, so a
  thermodynamic-diagram overlay is not meaningful. The figure will be a
  parametric sweep (see placeholder above).

## Limitations and CoolSolve gaps

- Constant oil specific heat and water cp evaluated once at the inlet state
  (a 0.03 % effect on these temperature ranges).
- No pressure drops, no wall/fin resistances, U given as a constant.
- No CoolSolve gaps encountered during the import.

## Related models

- `CSL-0008` *condenser_three_zones*: three-zone ε-NTU model of an air-cooled
  condenser, each zone with its own effectiveness law (this model is the
  single-zone counterflow case).
- `CSL-0014` *hx_constant_pinch*: three-zone condenser sized by an imposed pinch.
- See also the CoolSolve examples `exchangers2` (crossflow HX) and `exchangers3`
  (shell-and-tube condenser) for the companion exercises of the same session.
