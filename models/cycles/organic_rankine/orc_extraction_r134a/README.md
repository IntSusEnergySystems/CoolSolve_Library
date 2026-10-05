# ORC with two-stage expander and intermediate extraction (R134a)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0036`

Organic Rankine Cycle on R134a (evaporation at 90 °C, condensation at 30 °C)
whose screw/scroll-type expander is described **stage by stage**: an isentropic
first expansion, the extraction of a fraction of the flow at an intermediate
pressure, an isentropic second expansion and a constant-volume discharge down to
the condensation pressure. The extracted vapour is mixed with the expander
exhaust, then used as the hot side of an internal heat exchanger (recuperator)
that precools the pumped liquid. The expander power (5 kW) and the pump
isentropic efficiency (0.5) are specified, as in the original; the model gives
the displaced volume of the expander (21.2 cm³ per revolution), the extracted
fraction (13.2 %), 35.6 kW of boiler duty and a cycle efficiency of 11.7 %.

| | |
|---|---|
| **Category** | Cycles and machines › Organic Rankine cycles |
| **Fluids** | R134a |
| **Size** | 163 equations (largest block: 21), incl. the 30 equations of the state arrays `T[i]`, `s[i]`, `P[i]`, `h[i]` (1…14) for the diagrams |
| **Source** | ULiège Thermodynamics Laboratory, `modeles/cycle a extraction.EES` (EES 7.991, July 2010) — CoolSolve example `orc_extraction` + the same file saved as EES 9.920 in `CoolSolve/misc/EES_ok.zip` |
| **Authors** | S. Quoilin / ULiège Thermodynamics Laboratory (probable, see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | 0.3.0@536d427 — converges in 21 Newton iterations with the shipped `.initials`; verified against the solution stored in the original EES file |

## Problem statement

An ORC on R134a evaporates at 90 °C and condenses at 30 °C. The working fluid
is superheated by 5 K at the expander inlet and subcooled by 5 K at the
condenser outlet. The expander runs at 3000 tr/min, delivers 5 kW, has an
overall inlet volume ratio of 3 (first stage 2.5, second stage 1.2) and
expands the vapour down to the condensation pressure in two isentropic stages
separated by an intermediate pressure (0.9 × the second-stage inlet pressure).
A fraction of the flow is extracted after the first stage, mixed with the
expander exhaust, and cooled by 5 K in the internal heat exchanger, whose
effectiveness is 0.9 (the extracted vapour gives up its heat to the pumped
liquid). The pump isentropic efficiency is 0.5. The original file has no
problem statement; the model determines the displaced volume of the expander,
the extracted fraction, the pressures, the state points, the pump power, the
boiler and condenser duties and the cycle efficiency.

## Model

- evaporator and condenser at imposed saturation temperatures $T_{ev}$,
  $T_{cd}$ (phase-change plateaus, no pressure drop); superheat
  $\Delta T_{f,su,exp}$ = 5 K and subcooling $\Delta T_{f,ex,cd}$ = 5 K;
- mass flow rate from the expander kinematics:
  $\dot V_{s,exp} = N/60 \cdot V_{s,exp}$,
  $\dot m_{f,ev} = \dot V_{s,exp}/v_{f,su1,exp}$; the displaced volume
  $V_{s,exp}$ is **not an input**: it is sized by the specified expander power
  $\dot W_{exp}$ = 5000 W;
- expander, four successive specific works (as in the original):
  isentropic first expansion at constant volume ratio $r_{v,in,1}$
  ($w_{in,1} = h_{su1} - h_{in1}$), constant-volume drop in1→in2
  ($w_{in,2} = v_{in1}(p_{in1} - p_{in2})$), isentropic second expansion
  ($w_{in,3} = h_{in2} - h_{in3}$) and constant-volume discharge
  ($w_{in,4} = v_{in3}(p_{in3} - p_{ex})$); the expander power is the sum of
  the stage works weighted by the flow rates;
- extraction chamber: energy balance on the internal energy between the
  extracted flow (leaving at $h_{in1}$) and the throttled remainder, and the
  second-stage specific volume from the displaced volume of the reduced flow;
  the extracted fraction $x_{ext}$ is **not an input** either (the original
  comments out $x_{ext}$ = 0.2 and 0.01 as alternatives): it follows from the
  recuperator equations below;
- intermediate pressure: $p_{int} = 0.9\,p_{in2}$, saturation temperature
  $T_{int}$; the dimensionless ratio $P_{int}^{*} = p_{int}/\sqrt{p_{ev}p_{cd}}$
  is reported (0.737);
- mixing chamber (section 2 of the original): enthalpy balance between the
  expander exhaust and the extracted vapour gives the condenser inlet state
  (quality 0.862 at 30 °C);
- condenser and evaporator: state points at the vapour and liquid limits
  (`*_tp`, clipped with `min` as in the original), which makes the model robust
  when the exchanger is not fully used;
- pump: specified isentropic efficiency $\varepsilon_{s,pp}$ = 0.5, i.e.
  $w_{pp} = w_{pp,s}/\varepsilon_{s,pp}$ with $w_{pp} = h_{ex,pp} - h_{su,pp}$;
- internal heat exchanger (three statements of the duty, as in the original):
  from its effectiveness
  $\dot Q_{hex} = \varepsilon_{hex}\,\dot C_{f,hex}(T_{int} - T_{su,hex})$
  with $\varepsilon_{hex}$ = 0.9, from the hot-side balance
  $\dot Q_{hex} = \dot m_{f,ext}(h_{int,exp} - h_{ex,hex,h})$ with
  $T_{ex,hex,h} = T_{int} - \Delta T_{ex,hex,h}$, and from the cold-side
  balance $\dot Q_{hex} = \dot m_{f,ev}(h_{ex,hex} - h_{ex,pp})$, which give
  the extracted flow and the preheated liquid state;
- performance: $\dot Q_{ev}$, $\dot Q_{cd}$, $\dot W_{exp}$,
  $\dot W_{pp}$, $\eta$ and the cycle energy-balance residual `res`.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `fluid$` working fluid | R134a | `P_ev` / `P_cd` | 32.44 / 7.702 bar |
| `T_ev` / `T_cd` | 90 / 30 °C | `P_int` / `P_int_star` | 11.65 bar / 0.7367 |
| `W_dot_exp` expander power | 5000 W | `T_int` | 45.15 °C |
| `N` speed | 3000 tr/min | `V_s_exp` displaced volume | 21.17 cm³ |
| `DELTAT_f_su_exp` / `DELTAT_f_ex_cd` | 5 / 5 K | `M_dot_f_ev` / `M_dot_f_ext` | 0.2012 / 0.02654 kg/s |
| `r_v_in` / `r_v_in_2` | 3 / 1.2 | `x_ext` extracted fraction | 0.1319 |
| `epsilon_s_pp` pump isentropic efficiency | 0.5 | `Q_dot_ev` / `Q_dot_cd` | 35.65 / 31.47 kW |
| `epsilon_hex` / `DELTAT_ex_hex_h` | 0.9 / 5 K | `Q_dot_hex` | 4.425 kW |
| | | `W_dot_pp` / `eta` | 0.821 kW / 0.1172 |

## How to run

Open `orc_extraction_r134a.eescode` in the CoolSolve GUI and press *Solve*, or

```bash
coolsolve ./orc_extraction_r134a.eescode
```

The shipped `orc_extraction_r134a.initials` is **required**: from the default
guesses the solver stops with `SingularJacobian` in a block of 21 variables (the
expander block). It holds the values stored by EES, from which the enthalpy,
internal energy and entropy entries were removed (they are expressed in EES's
reference state for R134a, see *Verification*, and would be misleading as
guesses), the quality sentinels and `res`; with it the model converges in 21 Newton
iterations. Stored values of the unknowns (`V_s_exp`, `x_ext`, `w_pp`…) appear
only there, never in the equations.

## Results

| Quantity | Value |
|---|---:|
| `P_ev` evaporation pressure | 32.44 bar |
| `P_cd` condensation pressure | 7.702 bar |
| `P_int` intermediate (extraction) pressure | 11.65 bar |
| `P_int_star` = $p_{int}/\sqrt{p_{ev}p_{cd}}$ | 0.7367 |
| `T_int` intermediate saturation temperature | 45.15 °C |
| `V_s_exp` expander displaced volume (sized by 5 kW) | 21.17 cm³ |
| `M_dot_f_ev` evaporator flow rate | 0.2012 kg/s |
| `M_dot_f_ext` extracted flow rate | 0.02654 kg/s |
| `x_ext` extracted fraction | 0.1319 |
| `T_f_su_exp` expander inlet | 95.0 °C |
| `T_f_ex_exp` expander exhaust | 30.0 °C (quality 0.862 at the condenser inlet) |
| `x_f_su_cd` quality at the condenser inlet | 0.8622 |
| `T_f_ex_cd` condenser outlet | 25.0 °C |
| `T_f_ex_pp` pump outlet | 27.80 °C |
| `T_f_ex_hex` recuperator cold-side outlet | 43.08 °C |
| `T_f_ex_hex_h` recuperator hot-side outlet | 40.15 °C |
| `Q_dot_ev` boiler duty | 35.65 kW |
| `Q_dot_cd` condenser duty | 31.47 kW |
| `Q_dot_hex` recuperator duty | 4.425 kW |
| `W_dot_exp` expander power (specified) | 5.000 kW |
| `W_dot_pp` pump power | 0.821 kW |
| `eta` cycle efficiency | 0.1172 |
| `epsilon_s_exp` overall isentropic efficiency | 0.9084 |
| `res` cycle energy balance | −1.1·10⁻¹¹ W |

The arrays `T[i]`, `s[i]`, `P[i]`, `h[i]` (1 expander inlet … 14 second-stage
inlet) give the cycle on the T-s or P-h diagram (CoolSolve *Diagram* tab,
*Overlay array path*, *Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the cycle,
     figures/orc_extraction_r134a_ts.png -->

## Verification

Faithful import vs the solution stored in the original EES file
(`CoolSolve/misc/EES_ok.zip`, `EES_ok/orc_extraction.EES`, EES 9.920, 132 stored
variables; the equations are byte-identical to `modeles/cycle a extraction.EES`,
EES 7.991 — see *Conversion log*). All 133 equations of the original are in the
model unchanged; the inputs are those of the original. `compare_solution.py`
prints:

> 132 common variables, 72 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 31

The largest printed relative difference over all common variables is 1.00e+00,
for `res` and the three quality sentinels below. The 72 differences are:

1. **Reference state of the fluid** (52 variables `h_*`, `u_*`, `s_*`, `s[i]`):
   EES uses its default R134a reference, CoolProp the IIR one. The difference is
   a constant offset, +148.19 kJ/kg on the 24 `h` and `u` variables (range
   148.11 to 148.30 kJ/kg) and +795.80 J/(kg·K) on the 28 `s` variables (range
   795.53 to 796.08 J/(kg·K)) — consistent with EES ($h = 0$, $s = 0$ for
   saturated liquid at −40 °C) against the IIR reference ($h = 200$ kJ/kg,
   $s = 1$ kJ/(kg·K) at 0 °C). After removing the mean offset all 52 agree
   within 7.5·10⁻⁴ (`h`, `u`) and 6.7·10⁻⁴ (`s`) relative to the EES value.
2. **Equation of state of R134a** (EES vs CoolProp), 16 physical variables
   between 1.1·10⁻³ and 2.6·10⁻³: the specific volumes at the expander inlet are
   0.21 % higher in CoolSolve (95 °C, 32.4 bar), the intermediate pressures
   follow within 0.11 %, and the sizing amplifies these differences in the
   displaced volume (+0.11 %), the extracted flow (−0.26 % in `M_dot_f_ext`, with
   `x_ext` −0.17 %), the recuperator duty (−0.20 %) and the pump power
   (−0.18 %). The other 60 physical variables agree within 1·10⁻³. The largest
   printed difference after removing items 1 and 3 is **2.62e-03**
   (`M_dot_f_ext`).
3. **Conventions, no physical difference**: EES stores `x_f_su_pp = x_f_ex_pp = −100`
   and `x_f_int_exp = 100` (out-of-dome sentinel/percent convention of
   `quality()`), CoolSolve returns 0 for all three; `res` is 1.1·10⁻⁴ W in EES (its
   solver tolerance) and −1.1·10⁻¹¹ W here.

| Quantity | EES | CoolSolve | rel. diff. (printed) |
|---|---:|---:|---:|
| `P_ev` [Pa] | 3.24689e6 | 3.24418e6 | 8.35e-04 |
| `P_cd` [Pa] | 770642 | 770196 | 5.78e-04 |
| `P_int` [Pa] | 1.16581e6 | 1.16453e6 | 1.10e-03 |
| `P_int_star` [−] | 0.736998 | 0.736709 | 3.93e-04 |
| `V_s_exp` [m³] | 2.11456e-05 | 2.117e-05 | 1.15e-03 |
| `x_ext` [−] | 0.132147 | 0.13192 | 1.72e-03 |
| `M_dot_f_ev` [kg/s] | 0.201364 | 0.201183 | 8.98e-04 |
| `M_dot_f_ext` [kg/s] | 0.0266097 | 0.02654 | 2.62e-03 |
| `T_f_ex_pp` [°C] | 27.7977 | 27.7952 | 9.14e-05 |
| `T_f_int_exp` [°C] | 46.6088 | 46.64 | 6.69e-04 |
| `T_f_ex_hex` [°C] | 43.0958 | 43.0764 | 4.48e-04 |
| `Q_dot_ev` [W] | 35655.2 | 35647.7 | 2.11e-04 |
| `Q_dot_cd` [W] | 31478 | 31469 | 2.86e-04 |
| `Q_dot_hex` [W] | 4433.98 | 4425.13 | 2.00e-03 |
| `W_dot_pp` [W] | 822.806 | 821.32 | 1.81e-03 |
| `epsilon_s_exp` [−] | 0.908162 | 0.908434 | 3.00e-04 |
| `eta` [−] | 0.117155 | 0.117222 | 5.67e-04 |

`W_dot_exp` (5000 W), `epsilon_s_pp` (0.5), `T_f_ex_exp` (30 °C) and the
specified inputs agree exactly.

The two states 1 and 13 of the original are identical (`T[13] = T_f_su_exp`,
`s[13] = s_f_su_exp`, a leftover of the original); state 14 was added by the
library for the second-stage inlet. The 31 variables that exist only in the
CoolSolve solution are the string variable `fluid$` (never exported to
`.initials`/reference by the tool) and the arrays added for the diagrams:
`P[1…14]`, `h[1…14]`, `T[14]` and `s[14]`; no variable of the original is
missing.

## Source and attribution

Model of the ULiège Thermodynamics Laboratory, found in the laboratory
collection as `~/Nextcloud/thermo_models/modeles/cycle a extraction.EES`
(EES 7.991, file dated July 2010, equations stored as RTF, no author in the
file; the `{$ID$ #1206: Jean Lebrun, …}` tag is the EES licence of the
laboratory, not the author) and saved a few months later as
`CoolSolve/misc/EES_ok.zip: EES_ok/orc_extraction.EES` (EES 9.920), which is the
copy used here as verification reference: its equations are **byte-identical**
to the 2010 file, the only differences being the `$UnitSystem` line written by
`ees_extract.py` and the three French comments of the diagram section
translated into English. The second save also drops the parametric table
(a sweep of `P_int_star`) of the 2010 file.

The style of the model (EES file names `modeles/…`, R134a ORC, expander
modelled by volume ratios, `modeles/ExpanderSimpleModelSQ080318.EES` and
`simple_ORC_model SQ120220.EES` in the same folder) points to **S. Quoilin**
(ULiège Thermodynamics Laboratory), whose ORC models are in this collection;
the authors field is left as *probable* for the maintainer to confirm.

The CoolSolve example `examples/orc_extraction.eescode` (inventory candidate
`CSX-030`) is a transcription of the same file: its equations are identical to
the EES original apart from the blank lines, the English title/solver note and
the same three translated comments. It stays in the CoolSolve repository as a
test case; this curated model supersedes it in the library.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py` on `EES_ok/orc_extraction.EES`):
  unit system already `SI MASS DEG PA C J` (no conversion needed); equations
  were RTF, licence tag (Jean Lebrun, laboratory) and `{$PX$96}` display tag
  removed; 132 variables with their stored solution; **no lookup table, no
  parametric table, no function or procedure** (all calls are CoolSolve
  built-ins). The extractor leaves a **trailing NUL byte** at the end of the
  RTF-converted text, which CoolSolve refuses to parse — see
  `CS-BUG-EXTRACT-NUL` in the gap register; the byte was removed by hand.
- **Original equations restored (review C-38).** A first version of this model
  (by a worker) had rearranged the specification of the original —
  `V_s_exp`, `x_ext` and `w_pp` imposed with the values of the stored solution,
  `W_dot_exp` and `epsilon_s_pp` turned into outputs, the `Q_dot_hex` equation
  with the effectiveness dropped. That rearrangement was reverted after the
  review C-38: the unmodified original is a square system (133 equations in 133 unknowns), a
  design problem in which the specified `W_dot_exp` = 5000 W sizes `V_s_exp`,
  `epsilon_s_pp` = 0.5 fixes the pump work and the three statements of
  `Q_dot_hex` determine `x_ext` and the recuperator outlet. The model now
  carries the 133 equations of the original unchanged (checked with a
  normalised diff against a fresh extraction). The stored values of the
  unknowns are used only as initial guesses.
- **2026-10-05 — curation**: standard header; SI units added to the input
  comments (the original had none); the three French comments of the diagram
  section translated; the commented-out alternatives of the original
  (`V_s_exp`, `x_ext`, `h_f_in2_exp`, `h_f_su_cd`) kept as comments that say
  so; the section titles and their order left as in the original, the numbering
  of section 5 completed (the original has two sections `5.3`: they are `5.3`,
  `5.4`, `5.5`, `5.6` here); **state arrays completed** — `P[i]` and `h[i]`
  added next to the `T[i]`/`s[i]` of the original, and state 14 (second-stage
  inlet) added, so that the P-h and T-s overlays work (docs/model_workflow.md
  §3 step 5). These 30 added equations change no result: `coolsolve -d` reports
  163 equations in 163 unknowns, largest block 21.
- **Curated `.initials`**: the 76 reference-independent values stored by EES
  (the 52 `h`, `u`, `s` entries, the three quality sentinels and `res`
  dropped); required, see *How to run*.
- **Level** (docs/taxonomy.md §3): 1 (163 equations) + 1 (largest block 21) +
  1 (state arrays) + 1 (seven coupled components) + 1 (semi-empirical expander
  described by volume ratios) + 1 (curated guesses needed) = 6 → level 3.

## Limitations and CoolSolve gaps

- The model is a design-point (nominal) model of the expander, not a
  performance map (contrast `CSL-0007` *scroll_compressor_semi_empirical*): no
  pressure drops in the heat exchangers, no heat losses, no leakage and no
  mechanical efficiency. The expander power and the pump efficiency are
  specified; the displaced volume and the extracted fraction are results, so
  changing `W_dot_exp`, `epsilon_hex` or the volume ratios re-sizes the
  machine; to impose `V_s_exp` or `x_ext` instead, replace the equation that
  determines it (`W_dot_exp = 5000` or the effectiveness statement of `Q_dot_hex`).
- Needs the shipped `.initials` (the Newton solver stops on a singular block
  from the default guesses); this is a numerics limit, not a CoolSolve gap.
- EES `quality()` outside the saturation dome: `x_f_su_pp` and `x_f_ex_pp`
  store −100 (compressed liquid) and `x_f_int_exp` stores 100 (superheated)
  where CoolSolve returns 0 — a display convention, no effect on the physics.
- No CoolSolve gap blocks this model (`missing_features` is empty).

## Related models

- `CSL-0019` *Simple ORC with imposed component performance (R245fa)*: the same
  category, a screening ORC of the Quoilin thesis with imposed effectivenesses
  and pinch constraints instead of a stage-by-stage expander.
- `CSL-0004` *Rankine cycle of a 60 MW steam plant*: extraction in a steam
  Rankine cycle (open feedwater heater), water instead of an organic fluid.
- `CSL-0007` *Scroll compressor semi-empirical model*: the compression
  counterpart of the screw/scroll-type expander modelled here.
- CoolSolve examples `orc_extraction.eescode` (`CSX-030`, same model, kept in
  CoolSolve as a test case, superseded here) and `expander_module.eescode`
  (`CSX-019`, a *single-stage* semi-empirical scroll expander with internal
  leakage and heat transfer to the ambient — the same machine type, a different
  level of detail), superseded by `CSL-0037` *scroll_expander_semi_empirical*
  (the EES `MODULE` of the example flattened into the main program, decision
  D10).
- `~/Nextcloud/thermo_models/modeles/cycle a extraction.EES` (`TM-0267`): the
  2010 copy of the same EES file (identical equations), recorded as a duplicate
  of this model.
