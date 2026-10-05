# Rankine cycle of a 60 MW steam power plant

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0004`

A simple Rankine cycle with a complete set of real-machine imperfections:
boiler pressure drop and efficiency, turbine and pump isentropic efficiencies,
alternator and pump-motor efficiencies. From a given net electrical output
(60 MW), the model computes the steam flow rate, the boiler power, the
cooling-water flow rate, the cycle efficiency and the back-work ratio. The
four state points are stored in arrays, ready for the T-s or P-h diagram.

| | |
|---|---|
| **Category** | Cycles and machines › Steam power cycles |
| **Fluids** | Water |
| **Size** | 41 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), exercise session R07, exercise 1 (EES file `R07_E01_2022.EES`) |
| **Authors** | TBD (see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

In a 60 MW steam power plant, steam enters the turbine at 70 bar and 500 °C.
The other characteristics of the cycle are:

- water-cooled condenser pressure: 0.2 bar,
- boiler pressure drop: about 4 bar,
- boiler overall efficiency: 90 %,
- turbine isentropic efficiency: 85 %,
- alternator efficiency: 95 %,
- cooling-water temperature rise in the condenser limited to 10 °C,
- pump isentropic efficiency and drive-motor efficiency: 0.85 and 0.94.

Determine the boiler power, the steam flow rate, the cooling-water flow rate
and the Rankine-cycle efficiency.

## Model

Standard Rankine cycle, steady flow, kinetic and potential energy neglected:

- **turbine**: $h_4 = h_3 - \eta_{is,t}(h_3 - h_{4s})$ with $s_{4s} = s_3$;
- **pump**: $h_2 = h_1 + (h_{2s} - h_1)/\eta_{is,p}$, saturated liquid at the
  condenser outlet ($x_1 = 0$);
- **boiler**: $\eta_{ch}\,\dot Q_{ch} = \dot m_{vap}(h_3 - h_2)$, with a
  pressure drop $\Delta p_{ch}$ between pump outlet and turbine inlet;
- **condenser**: heat rejected $\dot Q_{cond} = \dot m_{vap}(h_1 - h_4)$,
  carried away by the cooling water ($c_{eau}$ = 4184 J/kg-K);
- **plant**: $\dot W_{el} = \eta_{alt}\,\dot W_t$ (negative: delivered),
  $\eta_{Rankine} = |\dot W_{el} + \dot W_{pump,el}|/\dot Q_{ch}$,
  $bwr = |\dot W_{pump,el}/\dot W_{el}|$.

The original sign convention is kept (powers delivered by the system are
negative).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T[3]` live-steam temperature | 500 °C | `m_dot_vap` steam flow | 63.43 kg/s |
| `p[3]` live-steam pressure | 70 bar | `Q_dot_ch` boiler heat release | 222.1 MW |
| `p[4]` condenser pressure | 0.2 bar | `m_dot_eau` cooling-water flow | 3281 kg/s |
| `DELTAp_ch` boiler pressure drop | 4 bar | `eta_rankine` cycle efficiency | 26.75 % |
| `eta_ch` boiler efficiency | 0.90 | `bwr` back-work ratio | 0.99 % |
| `eta_is_t` / `eta_alt` | 0.85 / 0.95 | `rapport_Q` condenser/boiler heat | 61.8 % |
| `eta_is_p` / `eta_mot` | 0.85 / 0.94 | `x_4` turbine-outlet quality | 0.918 |
| `DELTAT_eau` water temperature rise | 10 K | | |
| `W_dot_el` net electrical power | −60 MW | | |

## How to run

Open `rankine_cycle_60mw.eescode` in the CoolSolve GUI and press *Solve*, or
from a terminal:

```bash
coolsolve ./rankine_cycle_60mw.eescode
```

The system is fully explicit (41 blocks of size 1): no guess values needed.

## Results

| Point | T [°C] | p [bar] | h [kJ/kg] | s [kJ/kg-K] |
|---|---:|---:|---:|---:|
| 1 — condenser outlet / pump inlet | 60.1 | 0.2 | 251.4 | 0.832 |
| 2 — pump outlet / boiler inlet | 60.7 | 74.0 | 260.2 | 0.836 |
| 3 — boiler outlet / turbine inlet | 500 | 70 | 3411.4 | 6.800 |
| 4 — turbine outlet / condenser inlet | 60.1 | 0.2 | 2415.7 | 7.327 |

Main results: steam flow 63.43 kg/s, boiler heat release 222.1 MW, electrical
efficiency 26.75 %, cooling water 3281 kg/s. The back-work ratio is about
1 %: pumping a liquid needs almost no power compared with the vapour
expansion, one reason why steam cycles were operated long before gas-turbine
cycles.

The native state arrays `T[i]`, `p[i]`, `h[i]`, `s[i]` (i = 1…4) plot the
cycle directly in the CoolSolve *Diagram* tab (*Overlay array path*,
*Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the cycle,
     figures/rankine_cycle_60mw_ts.png -->

## Verification

1. **Faithful import vs EES.** The converted model was compared with the
   solution stored in the source EES file
   (`compare_solution.py --ees-units`): all 40 common variables agree within
   2·10⁻⁵ relative (largest deviation on `T[1]`, `T[4]`; enthalpies within
   8·10⁻⁶). This confirms both the property formulation agreement (EES 10.8
   vs CoolProp, water/IAPWS) and the unit conversion.
   `m`, `n`, `R`, `W_dot_alt` appear in the EES variable list only as
   leftovers of another exercise; they are absent from the equations.
2. **Cross-check with the CoolSolve example `rankine1` (CSX-036)**, the same
   exercise in SI units with a condenser pressure of 0.1 bar instead of
   0.2 bar: with `p[4] = 10e3` the model reproduces the example's results —
   steam flow 59.08 / 59.09 kg/s, boiler heat release 210.76 / 210.74 MW,
   cooling water 3036 / 3035 kg/s, turbine-outlet quality 0.899 / 0.899
   (within 0.06 %; the example uses `cp_w` = 4186 J/kg-K vs 4184 here). The
   efficiencies differ by definition only: 28.21 % here (pump electrical
   power netted in the numerator) vs 28.40 % in the example (pump mechanical
   power added to the boiler heat in the denominator).

## Source and attribution

Exercise solution of the ULiège course *Thermodynamique appliquée*
(MECA0002), exercise session R07, 2022-2023 version. The EES file names no
author (the `{$ID$}` tag is the laboratory licence); the companion Python
files of the session are authored by the repetition assistant N. Paulus, and
the 2017 original belongs to the THD course session of S. Bertagnolio /
S. Borguet — the maintainer will confirm the author attribution (`TBD`).

Source file (EES 10.836, comments in French, kPa/kJ/kW with decimal comma),
collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R7/R07_E01_2022.EES`
(inventory candidate `TM-0443`, duplicate group `DG-0106`).

## Conversion log

- **2026-10-04 — import** (`tools/ees_extract.py`, CoolSolve repository):
  decimal comma converted automatically by the tool; the EES licence tag was
  removed. Unit system converted **by hand** from `SI MASS DEG KPA C KJ` to
  `SI MASS DEG PA C J` (ees_import.md §6): `p[3]` 7000 kPa → 7000e3 Pa,
  `p[4]` 20 kPa → 20e3 Pa, `DELTAp_ch` 400 kPa → 400e3 Pa,
  `W_dot_el` −60e3 kW → −60e6 W, `C_eau` 4.184 kJ/kg-K → 4184 J/kg-K; all
  other equations are homogeneous and stay unchanged (property calls now
  take Pa/°C and return J). Comments translated to English; two comments
  that spanned two lines in the original were joined (CoolSolve does not
  parse multi-line `"…"` comments, gap `CS-GAP-MULTILINE-COMMENT`, non
  blocking — comment-only edit). No change to the equations; no `.initials`
  needed (fully explicit model). Verified against the EES stored solution
  (see above).
- **2026-10-04 — merge of the duplicate group.** The group members are the
  2017 original `THD10_R06_E1.EES` (TM-0519: same exercise and values,
  variable names `q_m_vap`/`q_m_eau`, less documented) and the zipped copy
  `R7.zip!/R07_E01_2022.EES` (TM-0547: identical equations to TM-0443); both
  are marked `duplicate` of this model. The CoolSolve example
  `rankine1.eescode` (CSX-036, same exercise in SI units, 0.1 bar condenser,
  no state arrays) is superseded by this model and stays in the CoolSolve
  repository as a test case.

## Limitations and CoolSolve gaps

- The cycle is idealised: no reheat, no regeneration, no turbine or
  condenser pressure losses; the subcooled liquid is taken at saturation.
- `CS-GAP-MULTILINE-COMMENT` (new, non blocking for this model): EES accepts
  `"…"` comments spanning several lines; CoolSolve fails to parse them
  (reproducer in the CoolSolve gap register). This model joins them onto one
  line.
- The EES file stores unit annotations in percent on `eta_rankine`, `bwr`,
  `rapport_Q`; the `[%]` annotations are kept (dimensionless).

## Related models

- `CSL-0019` *orc_simple_r245fa*: same category family (vapour power cycle
  with an organic working fluid and imposed component performance).
- CoolSolve example `rankine1.eescode` (CSX-036), superseded by this model.
