# Two-stage compression of superheated steam with intercooling

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; 🎯 **Optimisation** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0010`

Superheated steam is compressed by a two-stage isentropic compressor with
intercooling, the intermediate pressure being the model's optimisation
variable: the equal-pressure-ratio rule (Cengel & Boles), which minimises the
work for ideal gases, is applied and shown to be near-optimal for real steam.
The model compares the compression power of four machines on the same duty —
single-stage isentropic, two-stage with intercooling, isothermal
($\int v\,\mathrm{d}P$) and a liquid pump — plus the heats rejected.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | Water (superheated vapour, saturated liquid) |
| **Size** | 56 equations, largest block: 2 (36 model equations + 20 diagram state points) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition session R04, exercise 2 (EES file `R04_E2_2022.EES`) |
| **Authors** | N. Paulus, B. Dechesne (repetition assistants) and S. Quoilin (course), per the source metadata — the EES file names no author |
| **License** | MIT |
| **CoolSolve** | **verified** against the EES stored solution (34/34 variables ≤ 4.5·10⁻⁶). The native file uses `INTEGRAL` limits that are variables and a factor in front of the call. `CS-GAP-OPTIM` stays listed for information: the optimisation step is not reproducible, the model is shipped at the optimum |

## Problem statement

Superheated steam at 100 °C above saturation (at the supply pressure) is
compressed in a two-stage isentropic adiabatic compressor with intermediate
cooling that brings the steam back to the supply temperature. The flow rate is
0.15 kg/s, the supply and discharge pressures 100 kPa and 625 kPa. Determine
the required power and compare it with a single-stage isentropic adiabatic
compressor and with a single-stage isothermal compressor. Also compare the
compression power if the water were liquid (incompressible: a pump, not a
compressor). Bonus: compute the heat rejected in the intercooler of the
two-stage compressor and the heat exchanged during the isothermal compression.
*(Translated from the French statement in the source file; kinetic and
potential energy changes neglected.)*

## Optimisation problem (kind = optimization)

- **Objective**: minimise the total power of the two-stage compressor,
  $\dot W_{bi} = \dot m\left[(h_2-h_1) + (h_4-h_3)\right]$.
- **Decision variable**: the intermediate pressure $p_{int}$ (where the
  intercooler sits); in EES it was fixed by the rule of equal stage pressure
  ratios, the analytical optimum for polytropic compression of ideal gases
  with constant specific heats (Cengel & Boles, 8th ed., cited in the source).
- **Bounds**: $p_{in} < p_{int} < p_{out}$ = 100–625 kPa.
- **Shipped optimum (EES stored solution)**: $p_{int} = \sqrt{p_{in} p_{out}}$
  = **250 kPa** (equal ratios of 2.5 per stage).
- **CoolSolve cannot search the optimum** (`CS-GAP-OPTIM`): the model is
  imported with $p_{int}$ fixed at that value and runs as a steady model.
- **Check of the optimum** (CoolSolve sweep of $p_{int}$): the
  work curve is very flat; the true minimum for real steam lies at
  $p_{int} \approx 251$ kPa, i.e. the equal-ratio value costs only ≈ 0.3 W of
  66.3 kW (+0.0003 %):

| $p_{int}$ [kPa] | 220 | 240 | 248 | 250 | 252 | 256 | 260 | 280 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| $\dot W_{bi}$ [kW] | 66.47 | 66.32 | 66.296 | **66.294** | **66.294** | 66.297 | 66.30 | 66.40 |

## Model

Supply state: superheated steam at $T_{in} = T_{sat}(p_{in}) + 100$ K
(≈ 200 °C). Four cases on the same duty (all energies from Water property
calls; differences of enthalpy for the isentropic adiabatic cases):

1. **Single-stage isentropic**: $\dot W_{mono} = \dot m (h_{out} - h_{in})$
   with $s_{out} = s_{in}$;
2. **Two-stage with intercooling**: stage 1 to $p_{int}$ ($s$ constant),
   cooled at constant $p_{int}$ back to $T_{in}$, stage 2 to $p_{out}$;
   intercooler heat $\dot Q = \dot m (h_3 - h_2)$; relative saving
   `Saving_Wcp` vs case 1;
3. **Isothermal** at $T_{in}$: $\dot W_{isoT} = \dot m \int_{p_{in}}^{p_{out}} v\,\mathrm{d}P$
   (EES `INTEGRAL`, 1 kPa step); its heat by Clausius
   $\dot Q = \dot m\,T\,\Delta s$ and by the first law (cross-check);
4. **Pump**: $\dot W_{pump} = \dot m\, v_f\,(p_{out}-p_{in})$ on saturated
   liquid, cross-checked with the isentropic compression of the liquid
   ($\int v\,\mathrm{d}P$ and $h$ difference).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `m_dot` steam flow | 0.15 kg/s | `W_dot_mono` single-stage isentropic | 74.35 kW |
| `p_in` / `p_out` | 100 / 625 kPa | `W_dot_bi_etage` two-stage | 66.29 kW |
| superheat | 100 K | `p_int` (optimum, fixed) | 250 kPa |
| `T_in` (computed) | 199.6 °C | `Q_dot_intercooler` | −34.36 kW |
| | | `W_dot_isoT` isothermal | 59.06 kW |
| | | `Q_dot_cp_isoT` (2 methods) | −63.00 kW |
| | | `W_pump` (3 methods) | 82.1 W |

## How to run

The native EES file keeps the EES syntax (the factor `m_dot` in front of
`integral(…)`, the limits `p_in`, `p_out` that are variables). Open
`two_stage_steam_compressor_intercooling.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./two_stage_steam_compressor_intercooling.eescode
```

No guess values or `coolsolve.conf` needed (525 fixed RK4 steps per integral:
the explicit step of 1000 Pa over 525 000 Pa); the limits follow `p_in` and
`p_out`. The baseline is `two_stage_steam_compressor_intercooling.sol`.

## Results

| Case | Power | Heat rejected | Comment |
|---|---:|---:|---|
| 1. Single-stage isentropic | 74.35 kW | 0 (adiabatic) | discharge at 7.83 kJ/kg·K entropy, superheated |
| 2. Two-stage + intercooling | 66.29 kW | 34.36 kW (intercooler) | 10.8 % work saving; stage powers 33.29 / 33.01 kW (not equal: steam is not an ideal gas) |
| 3. Isothermal | 59.06 kW | 63.00 kW (both methods agree) | minimum work: cooling keeps $v$ small |
| 4. Pump (liquid) | 82.1 W | ≈ 0 | ≈ 1000× less: liquid $v$ ≈ 1/2000 of the vapour's |

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1 supply, 2 stage-1 discharge,
3 intercooler outlet, 4 stage-2 discharge, 5 single-stage discharge) overlay
the compression paths on the P-h or T-s diagram (CoolSolve *Diagram* tab,
*Overlay array path*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the
     steam compression paths, figures/two_stage_steam_compressor_intercooling_ph.png -->

## Verification

EES stored solution of the source file (35 variables), after the hand
conversion kPa/kJ → Pa/J, compared with `compare_solution.py --ees-units`
on the **native file**: **34/34 common variables agree, maximum relative deviation
4.47·10⁻⁶** on `W_dot_isoT` (`Q_dot_cp_isoT2` 4.20·10⁻⁶, the value quoted at
import; every other variable ≤ 3.4·10⁻⁶; same water formulation in EES 10.836
and CoolProp). The two largest differences are the integral-based quantities:
EES gives 59 065.135 W, which is the trapezoidal rule with the 1 kPa step
(59 065.136 W recomputed with CoolProp), while CoolSolve integrates with RK4
and returns 59 064.871 W, the exact integral of the CoolProp specific volume
(59 064.8706 W with a high-accuracy quadrature). The 35th EES variable, `v_gaz`, was renamed `v_liq` (misleading
name: it is the liquid specific volume); the 21 extra CoolSolve variables are
`v_liq` and the 20 diagram state points added by this import. Key
values: $\dot W_{bi}$ 66 294/66 294 W (EES/CoolSolve), $\dot W_{isoT}$
59 065/59 065 W, intercooler −34 359/−34 359 W, `Saving_Wcp` −10.84 % (EES
writes −10.84: the saving is positive, the variable is signed as
`(bi − mono)/mono`).

## Source and attribution

Exercise solution for the repetition session R04 (2022–2023) of the ULiège
course *Thermodynamique appliquée* (MECA0002). The EES file names no author;
the attribution (repetition assistants N. Paulus and B. Dechesne, course by
S. Quoilin) comes from the companion metadata recorded in the source
inventory. Source file (EES 10.836, comments in French, decimal comma),
collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R4/R04_E2_2022.EES`
(inventory candidate `TM-0422`, used as the fallback of roadmap card C-09
because the primary candidate `TM-0101` is a cooling-tower model — see the
conversion log).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`): EES 10.836, decimal comma
  converted automatically; unit system `SI MASS DEG KPA C KJ` → **hand-converted
  to SI-C-Pa-J**: `p_in`, `p_out` ×1000 (with the original values kept in the
  comments), the two `INTEGRAL` steps 1 kPa → 1000 Pa, all energies/entropies
  now in J (property calls unchanged; balances homogeneous), `100[%]` kept as
  the literal 100. No absolute-temperature relation needed conversion except
  the existing `(T_in + 273.15)` of the Clausius heat. `$UnitSystem` line
  removed (CoolSolve has a single unit system). Comments translated to English; standard header
  added. Stored solution present (35 variables) → used as verification
  reference. Candidate `TM-0101` (primary of card C-09) was inspected and
  rejected for this card: it is a cooling-tower model (AirH2O, category
  `hvac/`), not a compressor, and its stored Min/Max state is unphysical
  (negative duty fraction); it stays `todo` in the inventory for the
  hvac/optimisation track.
- **2026-10-05 — variable renamed**: `v_gaz` → `v_liq` (it is the specific
  volume of *compressed liquid* water along the saturated-liquid isentrop,
  not a gas property; no result changes).
- **2026-10-05 — optimisation documented and checked**: objective, decision
  variable, bounds and the EES-stored optimum (250 kPa, equal stage pressure
  ratios) recorded above; CoolSolve sweep of `p_int` (210–290 kPa) confirms
  the minimum at ≈ 251 kPa, +0.0003 % at the shipped point. `kind =
  optimization`, blocked for the search itself by `CS-GAP-OPTIM`.
- **2026-10-05 — diagram support**: block of 20 post-processing equations
  (state arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`, 5 states) added at the end of
  both files; results unchanged.
- **Level**: scores 2 on the rubric only because of the 20 diagram equations
  added by the library (36 explicit exercise equations otherwise); exercise
  pedagogy → level 1 (±1 rule, docs/taxonomy.md §3).

## Limitations and CoolSolve gaps

- `CS-GAP-OPTIM`: no Min/Max optimiser in CoolSolve — the model is shipped at
  the optimum found by EES (decision variable fixed); the sweep table above
  documents the neighbourhood of the optimum.
- Physical limitations: ideal intercooling to exactly $T_{in}$; ideal
  isothermal compression; no pressure drops; the pump cases assume incompressible
  saturated liquid (checked in the model by three consistent methods).

## Related models

None yet in the library. `CSL-0001` (refrigeration cycle with a simple
compressor) covers single-stage compressor laws on refrigerants.

- `CSL-0047` *nonideal_gas_isothermal_work*: another `INTEGRAL` model of the
  same course (definite integral of P(v), symbolic limits, factor in front of
  the call), verified on its native file.
