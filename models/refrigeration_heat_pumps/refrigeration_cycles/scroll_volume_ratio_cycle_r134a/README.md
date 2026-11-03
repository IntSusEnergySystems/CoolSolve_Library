# Scroll refrigeration cycle (R134a): built-in volume ratio vs isentropic efficiency and COP

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0148`

Which internal (built-in) compression ratio should a scroll compressor of a
refrigeration machine be built for? The model computes, for any evaporation and
condensation temperature and any built-in volume ratio, the pressure ratio that
the machine actually develops, its isentropic efficiency and the COP of the
cycle. It is the discussion model of a scroll compressor on R134a, where the
geometry of the machine — and not an external pressure ratio — fixes the
compression.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R134a (any CoolProp fluid can be selected through `fluid$`) |
| **Size** | 47 equations, all explicit (largest block: 1): 31 for the model, 16 for the diagram state points |
| **Source** | ULiège exercise (répétition 2, exercise 3), EES file `VL050926_2-3-1 questionsVL051023.EES` |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@2d15382 — verified against the solutions stored in the original EES file |

## Problem statement

*Translated from the original file.* A scroll compressor driving a refrigeration
machine is discussed: which internal compression ratio should be provided for it?
The refrigerant is R134a. The evaporation and condensation temperatures vary
respectively between −15 and 0 °C and between 30 and 55 °C. Show how the
isentropic efficiency of the compressor and the COP of the cycle vary with these
temperatures, as a function of the chosen internal compression ratio. The
refrigerant is considered saturated at the evaporator outlet and at the
condenser outlet.

## Model

As in the original, the refrigerant is saturated at the evaporator outlet
(`h_ex_ev = h_su_cp`) and at the condenser outlet (`h_ex_cd = enthalpy(P_cd, x=0)`),
and there is no throttling device between the condenser and the evaporator
(`h_su_ev = h_ex_cd`), no pressure drop anywhere in the cycle and no superheat at
the compressor inlet (`T_su_cp = T_ev`, "simplification: no superheat" in the
original).

The compressor is a **volumetric machine**: its geometry imposes the built-in
volume ratio $r_{v,in} = v_{su,cp}/v_{in}$, not an external pressure ratio. The
compression has two steps:

1. **isentropic down to the built-in volume** — the state at the built-in volume
   is obtained from $(s_{su,cp}, v_{in})$, which fixes the adapted pressure
   $P_{in} = p(s_{su,cp}, v_{in})$ ("PV^gamma = cste" in the original) and the
   isentropic work $w_{in,s} = h_{in} - h_{su,cp}$;
2. **isochoric up to the discharge pressure** — the gas is then pushed out at
   constant volume $v_{in}$ until the condenser pressure is reached, for a work
   $w_{in,v} = v_{in}(P_{ex,cp} - P_{in})$.

The total compression work is $w_{in} = w_{in,s} + w_{in,v}$ and the isentropic
efficiency of the machine is $\varepsilon_s = w_s/w_{in}$, with
$w_s = h_{ex,cp,s} - h_{su,cp}$ the isentropic work between the cycle pressures.
The condenser rejects $q_{cd} = h_{ex,cp} - h_{ex,cd}$, the evaporator produces
$q_{ev} = h_{ex,ev} - h_{su,ev}$ and $COP = q_{ev}/w_{in}$.

Two ratios are reported: the external one, $r_p = P_{cd}/P_{ev}$, and the one the
machine develops internally, $r_{p,in} = P_{in}/P_{su,cp}$. The isentropic
efficiency is maximal when the two are equal, as discussed in the original
comment of the file; the sign of the isochoric work tells on which side of that
maximum the machine stands (a negative $w_{in,v}$ means that the discharge
pressure is reached *before* the built-in volume).

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `fluid$` refrigerant | R134a | `epsilon_s` isentropic efficiency | 0.9938 |
| `T_ev` evaporation temperature | −15 °C | `COP` | 4.577 |
| `T_cd` condensation temperature | 30 °C | `r_p` / `r_p_in` pressure ratios | 4.698 / 5.404 |
| `r_v_in` built-in volume ratio | 5 | `w_in_s` / `w_in_v` / `w_in` works | 35.11 / −2.79 / 32.32 kJ/kg |
| | | `P_ev` / `P_cd` pressures | 1.639 / 7.702 bar |
| | | `q_ev` / `q_cd` cooling / heat rejected | 147.9 / 180.2 kJ/kg |
| | | `T[2]` compressor discharge temperature | 36.8 °C |

## How to run

```bash
coolsolve scroll_volume_ratio_cycle_r134a.eescode
```

No guess file is needed: every equation stands alone (largest block 1) and the
model converges in two iterations from the default guesses. Two warnings are
harmless and expected: `PRESSURE(): t=30 looks like Fahrenheit` (the default
condensation temperature 30 °C triggers the heuristic, CoolSolve uses Celsius) and
`ENTHALPY(): v=… is unusually large` (the specific volume of saturated R134a
vapour, ~0.12 m^3/kg at −15 °C, entered through the $(s, v)$ call).

The original file drives the model from a **parametric table** that sweeps
`T_ev`, `T_cd` and `r_v_in`; CoolSolve does not read parametric tables
(`CS-GAP-PARAMETRIC`, *not blocking* — the default run of the table is written in
the equations). To reproduce a sweep, change the three input values.

## Results

Default operating point (`T_ev` = −15 °C, `T_cd` = 30 °C, `r_v_in` = 5, the
first row of the original parametric table):

| Quantity | Value |
|---|---|
| `P_ev` / `P_cd` | 163 940 Pa / 770 196 Pa |
| `r_p` / `r_p_in` | 4.698 / 5.404 |
| `P_in` pressure at the built-in volume | 885 945 Pa |
| `v_su_cp` / `v_in` | 0.12067 / 0.024134 m^3/kg |
| `w_in_s` / `w_in_v` / `w_in` | 35 110 / −2 794 / 32 317 J/kg |
| `w_s` / `epsilon_s` | 32 117 J/kg / 0.9938 |
| `q_ev` / `q_cd` | 147 906 / 180 223 J/kg |
| `COP` | 4.577 |
| `T[2]` discharge temperature | 36.8 °C |

At this point the machine stands on the "overcompression" side
($r_{p,in} = 5.40 > r_p = 4.70$): the isochoric step is a *decompression* and
$w_{in,v}$ is negative (−2.8 kJ/kg). The state points are the four cycle states
of the arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` at the end of the file (the
discharge state is superheated vapour, 36.8 °C at 7.7 bar).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/scroll_volume_ratio_cycle_r134a_ph.png)  + one-line caption -->

## Verification

**Against the solution stored in the original EES file** (inventory row TM-0042,
EES X7.458). Five of its thirty variables are not cleared; at the default
operating point:

| Variable | EES | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `T_cd` | 30 | 30 | 0 |
| `r_v_in` | 5 | 5 | 0 |
| `P_cd` | 770 641.9 | 770 196.3 | 5.8e-4 |
| `h_ex_cd`, `h_su_ev` | 93 582.95 | 241 722.39 | excluded (reference state) |

`compare_solution.py` prints *"5 common variables, 2 differ (rtol=0.001)"*: the
three above agree within **5.8e-4**, and the two absolute enthalpies differ by
the constant 148 139 J/kg of the reference state, as in `CSL-0001`. The offset is
the EES reference state of R134a ($h = 0$, $s = 0$ for saturated liquid at
−40 °C): the saturated liquid at −40 °C has $h = 148\,144$ J/kg and
$s = 795.61$ J/kg·K in the CoolProp/IIR frame, i.e. the enthalpy offset is
reproduced to 11 J/kg (7e-5) and the entropy offset to 0.11 J/kg·K.

**Against the stored solution of the duplicate-group copy** TM-0043
(`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 02/VL050926_2-3-1.EES`,
EES X7.403), whose thirty variables are all stored. The equations are identical
(checked by diffing the extracted equation windows, comments excluded) and its
stored operating point is `T_ev` = 0 °C, `T_cd` = 30 °C, `r_v_in` = 5. Re-running
this model at that point:

> `compare_solution.py`: **30 common variables, 11 differ (rtol=0.001)**; the 17
> others agree within **9.1e-4** (`P_in` and `r_p_in`, worst), 6.7e-4 on `COP`
> and 4.0e-4 on `epsilon_s` (EES 0.84100, CoolSolve 0.84066).

Excluded variables and why:

- `h_in`, `h_su_cp`, `h_ex_cp`, `h_ex_cp_s`, `h_su_cd`, `h_ex_cd`, `h_ex_ev`,
  `h_su_ev` and `s_su_cp`: constant reference-state offset
  (+148 114…148 169 J/kg, +795.50 J/kg·K, see above); after removing the mean
  offset the enthalpies agree within **3.8e-4**;
- `v_su_cp` and `v_in` (1.06e-3): saturated-vapour specific volume of R134a at
  0 °C, 0.0693087 m^3/kg in CoolProp against 0.0693824 in EES X7.403 — a property
  backend difference, propagated by `v_su_cp = r_v_in*v_in`;
- `T_ev` and `T_su_cp` (−3.9e-18 in EES, 0 here): both zero.

**Energy balance**: $q_{cd} - q_{ev} - w_{in} = -3.0\times10^{-8}$ J/kg on
$q_{cd}$ = 180 223 J/kg (1.7e-13 relative), and $w_{in} = w_{in,s} + w_{in,v}$ to
1e-9 J/kg.

No unit conversion was needed: the file is in `SI MASS DEG PA C J`.

## Source and attribution

Vincent Lemort (ULiège Thermodynamics Laboratory), course *Machines et systèmes
thermiques*, repetition session 2, exercise 3; header `VL050926` (2005-09-26).
The published collection is under the library licence (MIT). Source file:
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 02/VL050926_2-3-1 questionsVL051023.EES`
(EES X7.458, inventory row TM-0042, duplicate group DG-0006, representative).

## Conversion log

- **2026-10-15 — import**: `ees_extract.py` extraction of the RTF equations
  (30 variables, no lookup table, unit system `SI MASS DEG PA C J`, nothing to
  convert); `$UnitSystem` directive and the `{$ID$…}` tag removed; comments
  translated to English; equations, variable names and all values kept. The
  file's parametric table was not stored by EES (its variables are cleared, see
  the extraction warning) — the default operating point of the model is the
  first parametric-table row written in the file (`T_ev` = −15 °C, `T_cd` = 30 °C,
  `r_v_in` = 5), and it is also the regression baseline.
- **2026-10-15 — parametric table** (decision of workflow §3): `T_ev` was only
  defined by the parametric table, so the first row of that table was written as
  an input equation (`CS-GAP-PARAMETRIC`, *not a blocking gap*). The extraction is
  square without it only in that sense: 29 equations for 30 variables
  (`coolsolve -d` on the unmodified extraction: *"System square: No"*), and
  adding `T_ev` gives 30/30.
- **2026-10-15 — fluid made a variable**: the refrigerant of the property calls,
  hardcoded `R134a` in the original, is now `fluid$ = 'R134a'`; no equation and
  no result changes (library style, as `CSL-0001`). The lowercase `r134a` of the
  line `h_ex_cp_s` was capitalised.
- **2026-10-15 — state points added**: the block `P[i]`, `h[i]`, `T[i]`, `s[i]`
  (i = 1…4, compressor suction / discharge / condenser outlet / evaporator inlet)
  is post-processing; the 31 model equations and all their results are unchanged.
- **2026-10-15 — comments**: the French comments were paraphrased, not
  interpreted. The line `h_su_ev = h_ex_cd` is labelled *"détente isenthalpique"*
  in the original although no isenthalpic expansion is modelled; the comment
  kept here states what the equation does.
- **Level**: taxonomy §3 score — equations 47 (<50) → 0; largest block 1 (≤5) → 0;
  structure: state arrays → 1; multi-zone/discretised → 0; physics: parametric
  study of an off-design machine → 1; numerics → 0. Total 2 → **level 2**.

## Limitations and CoolSolve gaps

- The model is a discussion tool, not a design model: the built-in volume ratio
  is an input, and the sign of $w_{in,v}$ tells whether the machine is over- or
  undercompressed for the imposed cycle pressures.
- No throttling device, no pressure drop and no superheat are modelled, as in
  the original; states 3 and 4 therefore share the same enthalpy and the
  P-h loop has no throttle segment.
- **No gap blocks the file.** Two registered items apply but are *not* blocking
  and are handled here: `CS-GAP-PARAMETRIC` (parametric table as input → the
  default run of the table is written in the equations) and `CS-GAP-PROP-SV`
  (the `(s, v)` property input pair of `CS-GAP-PROP-SV` is **not** a gap for
  R134a: CoolProp supports the (S, D) inputs for this fluid, so the native
  `(s, v)` calls run as they are; the gap only shows on the fluid of `CSL-0078`).

## Related models

- `CSL-0001` *refrigeration_cycle_simple_compressor*: same series (ULiège MSTh)
  with a reciprocating compressor described by a clearance-volume volumetric
  efficiency; the volume ratio of the machine there is an output of the
  compression, here it is the geometric input.
- `CSL-0068` *heat_pump_scroll_compressor_data_check*: the same scroll compressor
  at the data-consistency level (R407C, manufacturer capacities), with the same
  definition $\varepsilon_s = w_s/w_{in}$.
- See also `CSL-0015` *refrigeration_cycle_basic_r134a* (basic R134a cycle,
  constant isentropic efficiency).