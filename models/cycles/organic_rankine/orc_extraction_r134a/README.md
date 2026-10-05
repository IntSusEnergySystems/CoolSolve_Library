# ORC with two-stage expander and intermediate extraction (R134a)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0036`

Organic Rankine Cycle on R134a (evaporation at 90 °C, condensation at 30 °C)
whose screw/scroll-type expander is described **stage by stage**: an isentropic
first expansion, the extraction of a fraction of the flow at an intermediate
pressure, an isentropic second expansion and a constant-volume discharge down to
the condensation pressure. The extracted vapour is mixed with the expander
exhaust, then used as the hot side of an internal heat exchanger (recuperator)
that precools the pumped liquid. For the stored run the model gives a 4.99 kW
expander power, 35.6 kW of boiler duty and a cycle efficiency of 11.7 %.

| | |
|---|---|
| **Category** | Cycles and machines › Organic Rankine cycles |
| **Fluids** | R134a |
| **Size** | 163 equations (largest block: 1), incl. the state arrays `T[i]`, `s[i]`, `P[i]`, `h[i]` (1…14) for the diagrams |
| **Source** | ULiège Thermodynamics Laboratory, `modeles/cycle a extraction.EES` (EES 7.991, July 2010) — CoolSolve example `orc_extraction` + the same file saved as EES 9.920 in `CoolSolve/misc/EES_ok.zip` |
| **Authors** | S. Quoilin / ULiège Thermodynamics Laboratory (probable, see *Source and attribution*) |
| **License** | MIT |
| **CoolSolve** | main 2026-10-05 — converges in 4 Newton iterations from default guesses; verified against the solution stored in the original EES file |

## Problem statement

An ORC on R134a evaporates at 90 °C and condenses at 30 °C. The working fluid
is superheated by 5 K at the expander inlet and subcooled by 5 K at the
condenser outlet. The expander runs at 3000 tr/min, has a displaced volume of
21.15 cm³ per revolution, an overall inlet volume ratio of 3 (first stage 2.5,
second stage 1.2) and expands the vapour down to the condensation pressure in
two isentropic stages separated by an intermediate pressure (0.9 × the
second-stage inlet pressure); 13.2 % of the flow is extracted after the first
stage, mixed with the expander exhaust and cooled by 5 K in the internal heat
exchanger (the extracted vapour gives up its heat to the pumped liquid, which
leaves the pump at 27.8 °C). The pump isentropic efficiency is 0.5. Determine
the pressures, the state points, the expander and pump powers, the boiler and
condenser duties and the cycle efficiency.

## Model

- evaporator and condenser at imposed saturation temperatures $T_{ev}$,
  $T_{cd}$ (phase-change plateaus, no pressure drop); superheat
  $\Delta T_{f,su,exp}$ = 5 K and subcooling $\Delta T_{f,ex,cd}$ = 5 K;
- mass flow rate from the expander kinematics:
  $\dot V_{s,exp} = N/60 \cdot V_{s,exp}$,
  $\dot m_{f,ev} = \dot V_{s,exp}/v_{f,su1,exp}$;
- expander, four successive specific works (as in the original):
  isentropic first expansion at constant volume ratio $r_{v,in,1}$
  ($w_{in,1} = h_{su1} - h_{in1}$), constant-volume drop in1→in2
  ($w_{in,2} = v_{in1}(p_{in1} - p_{in2})$), isentropic second expansion
  ($w_{in,3} = h_{in2} - h_{in3}$) and constant-volume discharge
  ($w_{in,4} = v_{in3}(p_{in3} - p_{ex})$);
- extraction chamber: energy balance on the internal energy between the
  extracted flow (leaving at $h_{in1}$) and the throttled remainder, and the
  second-stage specific volume from the displaced volume of the reduced flow;
- intermediate pressure: $p_{int} = 0.9\,p_{in2}$, saturation temperature
  $T_{int}$; the dimensionless ratio $P_{int}^{*} = p_{int}/\sqrt{p_{ev}p_{cd}}$
  is reported (0.737);
- mixing chamber (section 2 of the original): enthalpy balance between the
  expander exhaust and the extracted vapour gives the condenser inlet state
  (quality 0.862 at 30 °C);
- condenser and evaporator: state points at the vapour and liquid limits
  (`*_tp`, clipped with `min` as in the original), which makes the model robust
  when the exchanger is not fully used;
- pump: $w_{pp} = h_{ex,pp} - h_{su,pp}$ with $\varepsilon_{s,pp}
  = w_{pp,s}/w_{pp}$ reported as a check (0.4995 for the stored run);
- internal heat exchanger: duty from the hot-side balance
  $\dot Q_{hex} = \dot m_{f,ext}(h_{int,exp} - h_{ex,hex,h})$ with
  $T_{ex,hex,h} = T_{int} - \Delta T_{ex,hex,h}$, and the same duty on the cold
  side, which gives the preheated liquid state;
- performance: $\dot Q_{ev}$, $\dot Q_{cd}$, $\dot W_{exp}$,
  $\dot W_{pp}$, $\eta$ and the cycle energy-balance residual `res`.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `fluid$` working fluid | R134a | `P_ev` / `P_cd` | 32.44 / 7.702 bar |
| `T_ev` / `T_cd` | 90 / 30 °C | `P_int` / `P_int_star` | 11.64 bar / 0.7365 |
| `V_s_exp` displaced volume | 21.15 cm³ | `T_int` | 45.14 °C |
| `N` speed | 3000 tr/min | `M_dot_f_ev` | 0.2010 kg/s |
| `DELTAT_f_su_exp` / `DELTAT_f_ex_cd` | 5 / 5 K | `M_dot_f_ext` | 0.02656 kg/s |
| `r_v_in` / `r_v_in_2` | 3 / 1.2 | `Q_dot_ev` / `Q_dot_cd` | 35.60 / 31.42 kW |
| `x_ext` extracted fraction | 0.1321 | `Q_dot_hex` | 4.428 kW |
| `DELTAT_ex_hex_h` | 5 K | `W_dot_exp` / `W_dot_pp` | 4.994 / 0.821 kW |
| pump isentropic efficiency | 0.5 (`epsilon_s_pp`, output) | `eta` | 0.1172 |

## How to run

Open `orc_extraction_r134a.eescode` in the CoolSolve GUI and press *Solve*, or

```bash
coolsolve ./orc_extraction_r134a.eescode
```

The model is fully explicit (largest algebraic block: 1) and converges in 4
Newton iterations from the default guesses: the shipped `.initials` is *not*
required. It holds the values stored by EES, from which the enthalpy, internal
energy and entropy entries were removed (they are expressed in EES's reference
state for R134a, see *Verification*, and would be misleading as guesses).

## Results

| Quantity | Value |
|---|---:|
| `P_ev` evaporation pressure | 32.44 bar |
| `P_cd` condensation pressure | 7.702 bar |
| `P_int` intermediate (extraction) pressure | 11.64 bar |
| `P_int_star` = $p_{int}/\sqrt{p_{ev}p_{cd}}$ | 0.7365 |
| `T_int` intermediate saturation temperature | 45.14 °C |
| `M_dot_f_ev` evaporator flow rate | 0.2010 kg/s |
| `M_dot_f_ext` extracted flow rate | 0.02656 kg/s |
| `T_f_su_exp` expander inlet | 95.0 °C |
| `T_f_ex_exp` expander exhaust | 30.0 °C (quality 0.862 at the condenser inlet) |
| `x_f_su_cd` quality at the condenser inlet | 0.8620 |
| `T_f_ex_cd` condenser outlet | 25.0 °C |
| `T_f_ex_pp` pump outlet | 27.80 °C |
| `T_f_ex_hex` recuperator cold-side outlet | 43.11 °C |
| `T_f_ex_hex_h` recuperator hot-side outlet | 40.14 °C |
| `Q_dot_ev` boiler duty | 35.60 kW |
| `Q_dot_cd` condenser duty | 31.42 kW |
| `Q_dot_hex` recuperator duty | 4.428 kW |
| `W_dot_exp` expander power | 4.994 kW |
| `W_dot_pp` pump power | 0.821 kW |
| `eta` cycle efficiency | 0.1172 |
| `epsilon_s_exp` overall isentropic efficiency | 0.9084 |
| `res` cycle energy balance | 1.9·10⁻¹⁰ W |

The arrays `T[i]`, `s[i]`, `P[i]`, `h[i]` (1 expander inlet … 14 second-stage
inlet) give the cycle on the T-s or P-h diagram (CoolSolve *Diagram* tab,
*Overlay array path*, *Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): T-s diagram of the cycle,
     figures/orc_extraction_r134a_ts.png -->

## Verification

Faithful import vs the solution stored in the original EES file
(`CoolSolve/misc/EES_ok.zip`, `EES_ok/orc_extraction.EES`, EES 9.920, 132 stored
variables; the equations are byte-identical to `modeles/cycle a extraction.EES`,
EES 7.991 — see *Conversion log*). `compare_solution.py` on the 132 variables
common to both solutions: 52 agree within 0.1 %, and the deviations are of two
kinds.

1. **Reference state of the fluid** (52 variables `h_*`, `u_*`, `s_*`): EES uses
   its default R134a reference, CoolProp the IIR one. The difference is a
   constant offset, +148.19 kJ/kg on `h` and `u` (spread ±100 J/kg) and
   +795.79 J/(kg·K) on `s` (spread ±0.24 J/(kg·K)) — consistent with EES
   ($h = 0$, $s = 0$ for saturated liquid at −40 °C) against the IIR reference
   ($h = 200$ kJ/kg, $s = 1$ kJ/(kg·K) at 0 °C). Removing the offset, **all 52
   enthalpies/internal energies and entropies agree within 0.09 %**
   (largest: `h_f_ex_hex_h`), i.e. within the property tolerance of
   `ees_import.md` §11 for a different equation of state.
2. **Equation of state of R134a** (EES vs CoolProp): the saturated vapour
   specific volumes are 0.21 % higher in CoolSolve at 95 °C / 32.4 bar, hence a
   mass flow rate 0.21 % lower; the intermediate pressures follow within
   0.14 %.

| Quantity | EES | CoolSolve | rel. diff. |
|---|---:|---:|---:|
| `P_ev` [Pa] | 3.246893e6 | 3.244183e6 | −8.3e-04 |
| `P_cd` [Pa] | 770642 | 770196 | −5.8e-04 |
| `P_int` [Pa] | 1.16581e6 | 1.16424e6 | −1.4e-03 |
| `P_int_star` [−] | 0.736998 | 0.736526 | −6.4e-04 |
| `M_dot_f_ev` [kg/s] | 0.201364 | 0.200951 | −2.0e-03 |
| `M_dot_f_ext` [kg/s] | 0.0266097 | 0.0265552 | −2.0e-03 |
| `T_f_ex_pp` [°C] | 27.79771 | 27.79781 | +3.6e-06 |
| `T_f_int_exp` [°C] | 46.60882 | 46.63383 | +5.4e-04 |
| `T_f_ex_hex` [°C] | 43.09575 | 43.10592 | +2.4e-04 |
| `Q_dot_ev` [W] | 35655.2 | 35597.9 | −1.6e-03 |
| `Q_dot_cd` [W] | 31478.0 | 31424.9 | −1.7e-03 |
| `Q_dot_hex` [W] | 4433.98 | 4428.03 | −1.3e-03 |
| `W_dot_exp` [W] | 5000.0 | 4994.08 | −1.2e-03 |
| `W_dot_pp` [W] | 822.81 | 821.12 | −2.0e-03 |
| `epsilon_s_exp` [−] | 0.908162 | 0.908406 | +2.7e-04 |
| `epsilon_s_pp` [−] | 0.5 | 0.499545 | −9.1e-04 |
| `eta` [−] | 0.117155 | 0.117225 | +6.0e-04 |
| `res` [W] | 1.1e-04 | 1.9e-10 | (EES solver tolerance) |

Two diagnostic variables are conventions, not results: EES stores
`x_f_su_pp = x_f_ex_pp = −100` and `x_f_int_exp = 100` (out-of-dome
sentinel/percent convention of `quality()`), CoolSolve returns 0 for all three;
the two-phase quality `x_f_su_cd = 0.8620` agrees within 3·10⁻⁴.

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
- **2026-10-05 — free inputs of the original restored.** Four variables of the
  EES file are never defined by an equation and are taken from the Variable
  Information dialog — `V_s_exp`, `x_ext`, `h_f_ex_pp`, `h_f_ex_hex` — and
  three more are defined more than once (`W_dot_exp` = 5000 [W] and then
  `W_dot_exp = W_dot_in_exp`; `epsilon_s_pp` = 0.5 and then
  `epsilon_s_pp = w_pp_s/w_pp`; `Q_dot_hex` three times), so the EES system is
  over-determined. Its stored solution is consistent (`res` = 1.1·10⁻⁴ W, and
  `w_pp = w_pp_s/0.5` to 10 digits), i.e. EES used the dialog values as extra
  inputs. Decisions:
  - `V_s_exp = 2.114557056E-5 [m^3]` (21.15 cm³, the stored value; the input
    line of the original, `V_s_exp = 100e-6 [cm^3]`, is commented out there);
  - `x_ext = 0.1321470819` (stored value; the original comments out
    `x_ext = 0.2` and `x_ext = 0.01` as alternatives);
  - `w_pp = 4086.162629 [J/kg]` (stored value) and `h_f_ex_pp = h_f_su_pp+w_pp`:
    the original leaves `h_f_ex_pp` free, but an *enthalpy* cannot be used as an
    input because of the reference-state difference between EES and CoolProp
    (see *Verification*); the equivalent specific work is reference-independent
    and reproduces the stored `epsilon_s_pp = 0.5`;
  - `epsilon_s_pp = 0.5` removed (kept as the reported value of the check
    `epsilon_s_pp = w_pp_s/w_pp`, which returns 0.4995), and the three
    definitions of `Q_dot_hex` reduced to one: the hot-side balance defines the
    duty and the cold-side balance is written as
    `h_f_ex_hex = h_f_ex_pp+Q_dot_hex/M_dot_f_ev`. The approximate duty
    `Q_dot_hex = epsilon_hex*C_dot_f_hex*(T_int-T_f_su_hex)` of the original
    (marked `"0"` there, i.e. already superseded) is dropped; `epsilon_hex`,
    `C_dot_f_hex` and `c_f_ex_pp` are kept as diagnostics. **No equation of the
    physics was changed** — only the redundant re-definitions — and the results
    reproduce the EES solution (see *Verification*). The shipped `.initials`
    keeps the 89 reference-independent values stored by EES (the 43 `h_*`,
    `s_*`, `u_*` entries and the quality sentinels were dropped, see *How to
    run*).
  To impose the pump efficiency instead of the specific work, replace
  `w_pp = 4086.162629` by `epsilon_s_pp = 0.5` and
  `h_f_ex_pp = h_f_su_pp+w_pp_s/epsilon_s_pp`.
- **2026-10-05 — curation**: standard header; SI units added to the input
  comments (the original had none); the three French comments of the diagram
  section translated; the commented-out alternatives of the original kept as
  comments that say so (`V_s_exp`, `x_ext`, `h_f_in2_exp`, `h_f_su_cd`);
  the section titles and their order left as in the original, the numbering of
  section 5 completed (`5.4`, `5.5`, `5.6`); **state arrays completed** — `P[i]` and
  `h[i]` added next to the `T[i]`/`s[i]` of the original, and state 14
  (second-stage inlet) added, so that the P-h and T-s overlays work
  (docs/model_workflow.md §3 step 5). These 30 added equations change no
  result: `coolsolve -d` reports 163 equations in 163 explicit blocks.

## Limitations and CoolSolve gaps

- **The cycle is over-determined in EES** (three variables defined twice or
  three times, four never defined by an equation) and CoolSolve, like a square-system
  solver, rejects it until the redundancies are resolved as described above.
  The resolutions are rearrangements, not new physics, and the comparison with
  the stored EES solution shows they are faithful. *Not registered as a gap: no
  evidence that the EES syntax/behaviour is valid (an EES file with the same
  duplicates was found — this one — but EES' own tolerance of over-determined
  systems was not checked in the EES manual).*
- The model has no pressure drops in the heat exchangers, no heat losses, no
  leakage and no mechanical efficiency: it is a design-point (nominal) model of
  the expander, not a performance map (contrast `CSL-0007`
  *scroll_compressor_semi_empirical*).
- EES `quality()` outside the saturation dome: `x_f_su_pp` and `x_f_ex_pp`
  store −100 (compressed liquid) and `x_f_int_exp` stores 100 (superheated)
  where CoolSolve returns 0 — a display convention, no effect on the physics.
- No CoolSolve gap blocks this model (`missing_features` is empty).
- Level score (docs/taxonomy.md §3): 1 (163 equations) + 0 (largest block 1) +
  1 (state arrays) + 1 (seven coupled components) + 1 (semi-empirical expander
  described by volume ratios) + 0 (converges from default guesses) = 4 →
  level 3.

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
  (`CSX-019`, blocked by `CS-GAP-MODULE`): a *single-stage* semi-empirical scroll
  expander with internal leakage and heat transfer to the ambient — the same
  machine type, a different level of detail.
- `~/Nextcloud/thermo_models/modeles/cycle a extraction.EES` (`TM-0267`): the
  2010 copy of the same EES file (identical equations), recorded as a duplicate
  of this model.
