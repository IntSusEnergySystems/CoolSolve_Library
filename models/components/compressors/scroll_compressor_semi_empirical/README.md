# Semi-empirical hermetic scroll compressor in a refrigeration cycle

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0007`

Semi-empirical ("reference") model of a hermetic scroll refrigeration compressor,
after Winandy, Saavedra & Lebrun (2002): the refrigerant path is decomposed into
six steps — supply pressure drop, heating-up by a fictitious wall of uniform
temperature, isentropic compression up to the *adapted pressure* imposed by the
internal built-in volume ratio, isochoric compression/re-expansion to the
exhaust pressure, exhaust cooling-down, exhaust pressure drop — with an internal
leakage flow and electromechanical losses (constant + proportional to the
internal power). A dozen physically meaningful parameters, identified on a
Copeland ZR72KC-TFD catalogue, cover the flow-rate characteristic, the heat
transfers and the losses; the model predicts the mass flow rate, the electrical
power and the discharge temperature at any rating condition. A **simplified
variant** without leakage (the ancestor of the CoolSolve example
`scroll_compressor`, converted from bar/kJ to SI units) is included.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | R22 |
| **Size** | 149 equations, largest block 46 (variant: 127 equations, largest block 34) |
| **Source** | ULiège Thermodynamics Laboratory — reference model of Winandy et al. (2002) implemented by V. Lemort (2008), collection of S. Quoilin |
| **Authors** | Vincent Lemort (ULiège); scientific model: E. Winandy, C. Saavedra O., J. Lebrun |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — verified against the EES stored solution of the source file (see *Verification*) |

## Problem statement

Predict the performance (mass flow rate, electrical power, discharge
temperature, isentropic and volumetric effectiveness) of a hermetic scroll
compressor of the Copeland ZR72KC-TFD family between an evaporator and a
condenser at imposed saturation temperatures, and reproduce the manufacturer
rating points with a limited number of physically meaningful parameters.
The default run is the last run stored in the EES source file
(t_ev = 7 °C, t_cd = 45 °C, ambient 25 °C, R22).

## Model

Winandy et al. (2002) decomposition of the compression (see the header of the
`.eescode` file for the complete nomenclature):

- **Supply** su → su1: fixed-area nozzle pressure drop (negligible here);
  su1 → su2: heating-up in a fictitious exchanger of wall temperature
  $t_w$: $\epsilon = 1-e^{-NTU}$, $NTU = AU_{su}/\dot m_r c_p$, with $AU$
  scaled as $(\dot m_r/\dot m_{r,n})^{0.8}$;
- **Leakage** ex2 → su1: isentropic nozzle of area $A_{leak}$, choked or not
  (`max(P_thr_crit, P_su2)`), mixed back into the supply flow (su1 → su2);
- **Flow rate**: $\dot m_s = \dot V_s (1+corr)/v_{su2}$ (swept volume 20.5 m³/h
  at 3500 tr/min, i.e. $V_s$ = 97.7 cm³/rev);
- **Compression** su2 → in: isentropic, to the adapted pressure
  $p_{in} = P(s_{su2},\, v_{su2}/r_{v\,in})$ with $r_{v\,in}$ = 2.55;
  in → ex2: constant-volume evolution,
  $w_{in2} = v_{in}(p_{ex2}-p_{in})$;
- **Electrical power**: $\dot W = \dot W_{in} + \dot W_{loss0} + \alpha\,\dot W_{in}$
  (242 W + 0.2·$\dot W_{in}$);
- **Exhaust** ex2 → ex1: cooling-down in the same fictitious exchanger;
  ex1 → ex: incompressible nozzle pressure drop (compressible alternative
  computed as `M_dot_r_bis`);
- **Wall balance**: $\dot W_{loss} = \dot Q_{su} + \dot Q_{ex} + \dot Q_{amb}$
  closes the model and yields $t_w$;
- **Cycle**: evaporator and condenser at imposed saturation temperatures
  ($x=0.5$ convention of the catalogue data), 5 K superheat and 5 K subcooling.

| Inputs | Value | Outputs (default run) | Value |
|---|---|---|---|
| `t_ev` / `t_cd` | 7 / 45 °C | `M_dot_r` refrigerant flow | 0.1384 kg/s |
| `t_amb` | 25 °C | `W_dot_cp` electrical power | 5179 W |
| `DELTAt_oh_ev` / `DELTAt_sc_cd` | 5 / 5 K | `t_ex_cp` discharge temperature | 75.6 °C |
| `fluid$` | R22 | `Q_dot_ev` / `Q_dot_cd` | 22.38 / 27.14 kW |
| 13 identified parameters | see §2 of the file | `epsilon_v_cp` / `epsilon_s_cp` | 0.942 / 0.697 |
| | | `t_w_cp` fictitious wall | 66.9 °C |

## How to run

Open `scroll_compressor_semi_empirical.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./scroll_compressor_semi_empirical.eescode
```

The model **requires the guess values** of `scroll_compressor_semi_empirical.initials`
(the EES solution): without them the 46-equation block does not converge
(SingularJacobian). With them it converges in 12 iterations. The state points
are available as the arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`
(1 su, 2 su2, 3 adapted, 4 ex2, 5 ex1, 6 ex, 7 condenser outlet) for the
CoolSolve diagrams (*Overlay array path*).

**Variant** `scroll_compressor_semi_empirical_simplified.eescode`: same model
without leakage and without pressure drops, with the parameter set of the
larger machine of the EES original (swept volume 174 cm³/rev, $r_{v\,in}$ =
2.775, reference flow 0.25 kg/s); its default run (t_ev = 30 °C, t_cd = 40 °C)
is a strong over-compression case ($p_{ad}$ = 35 bar ≫ $p_{ex}$ = 15.3 bar),
the last run stored in the EES file. It also needs its `.initials` file
(27 iterations).

## Results

Default run (see above) and, for comparison, the two EES references:

| Run | t_ev/t_cd [°C] | ṁ [kg/s] | Ẇ [W] | Q̇_ev [W] | ε_v | ε_s | t_w [°C] |
|---|---|---:|---:|---:|---:|---:|---:|
| Main model (CoolSolve) | 7/45 | 0.1384 | 5179 | 22 382 | 0.942 | 0.697 | 66.95 |
| Main model (EES) | 7/45 | 0.1384 | 5180 | 22 370 | 0.942 | 0.697 | 66.93 |
| Variant (CoolSolve) | 30/40 | 0.4030 | 7071 | 70 795 | 0.972 | 0.352 | 59.50 |
| Variant (EES) | 30/40 | 0.4032 | 7071 | 70 786 | 0.972 | 0.352 | 59.48 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the R22 cycle
     through the compressor (states 1-7), figures/scroll_compressor_semi_empirical_ph.png -->

## Verification

1. **Main model vs EES stored solution** (`TM-0481`, last run stored in the
   file; `compare_solution.py`, 120 common variables): all key outputs within
   **0.1 %** — M_dot_r 0.13835/0.13842, W_dot_cp 5179.0/5179.7,
   Q_dot_ev 22 382/22 370, Q_dot_cd 27 142/27 130, t_ex_cp 75.55/75.53,
   t_w_cp 66.95/66.93, epsilon_s_cp 0.6971/0.6971, epsilon_v_cp 0.9420/0.9421,
   M_dot_leak_cp 3.01e-3/3.01e-3. 14 variables deviate by 0.1–1.5 %, all on
   secondary derived quantities whose small value amplifies the property
   differences between EES 7.9 and CoolProp (R22): worst case `w_in2_cp`
   942.5/956.6 J/kg (1.5 %, an isochoric work term of 3 % of w_in), c_p and
   NTU within 0.6 %.
2. **Variant vs EES stored solution** of `EES_ok/scroll_compressor.EES`
   (converted to SI, `compare_solution.py`, 95 common variables): key outputs
   within **0.1 %** — M_dot 0.4030/0.4032, W_dot 7071/7071, Q_dot_ev
   70 795/70 786, COP_c 10.011/10.013, epsilon_s_cp 0.3523/0.3525, t_w_cp
   59.50/59.48. Differences beyond tolerance only on the two cells that were
   intentionally converted/corrected (see the conversion log): `C_sd_cp`
   (0.004 kW⁻¹ written as 4e-6 W⁻¹) and `DELTAp_su1_cp` (kPa-era `/2000`
   replaced by the correct `/2`: 2.7e-3 Pa instead of 0.27 Pa; negligible
   either way).

## Source and attribution

Model of **Winandy, Saavedra O. and Lebrun** (2002), EES implementation and
parameter identification on Copeland ZR72KC-TFD catalogue data by
**Vincent Lemort** (ULiège Thermodynamics Laboratory), file dated 2008-02-29.
Scientific reference: Winandy E., Saavedra O. J., Lebrun J. (2002),
*Experimental analysis and simplified modelling of a hermetic scroll
refrigeration compressor*, Applied Thermal Engineering 22, 107-120; and
Winandy's PhD thesis (University of Concepción, 1999).

Source files (collection of S. Quoilin):
- main model, candidate `TM-0481`:
  `~/Nextcloud/thermo_models/Model data bank/Compressors/SCROLLCOMPRESSOR_REFSIM_MODEL_VL080228.zip!/scrollCompressor_RefSim_EES_Model_VL080228.EES`
  (EES 7.888, native SI-°C-Pa-J; carries the lab disclaimer "freely
  distributed, may not be sold, cite origin");
- variant, EES original of the CoolSolve example `CSX-042`:
  `../CoolSolve/misc/EES_ok.zip:EES_ok/scroll_compressor.EES` (EES 9.920,
  bar/kJ).

## Conversion log

- **2026-10-05 — triage (task C-06).** Three near-duplicates of the Winandy
  reference model were processed together: `TM-0481` (ULiège collection),
  `CSX-042` (CoolSolve example) and its EES original
  `EES_ok/scroll_compressor.EES`. `TM-0481` was kept as the representative
  (native SI units, most complete physics — leakage and exhaust pressure drop
  are missing from the other two —, nomenclature and named author) and
  imported as the main model; the other two were merged as the *simplified*
  variant. The CoolSolve example stays in the CoolSolve repository.
- **2026-10-05 — import (main model).** `ees_extract.py` on `TM-0481`: unit
  system already SI-°C-Pa-J, no lookup/parametric table, 276 equation lines.
  Twelve inputs/parameters were given by the EES **Diagram window** (their
  equations commented out): restored as active equations with the **stored
  last-run values** (t_ev 7 °C, t_cd 45 °C, AU_su_n 18 W/K, AU_ex_n 35 W/K,
  AU_amb 10 W/K, W_dot_loss0 242 W, alpha 0.2, d_ex 7.5 mm, corr 0.0314,
  r_v_in 2.55, V_dot_s 20.52 m³/h, M_dot_r_n 0.091 kg/s), the values of the
  documented identification being kept in the comments (they differ). The
  equation `A_leak_cp=3.888e-7` postdates the stored solution (A_leak = 4.5e-7
  in the last run): the last-run value is used and the older one is kept in
  the comment. Dead code removed: the back-calculation of the diagram
  variable `cd` (redundant with `P_ex_cp = P_cd`), the commented-out
  manufacturer-data block, obsolete commented alternatives; duplicated
  section numbers fixed; the unused parameters `C` and `d_su` of the original
  are kept and flagged. Section titles converted from `"!…"` strings to
  comments, trailing units cleaned. 28 post-processing equations (state-point
  arrays) added for the diagrams; results unchanged.
- **2026-10-05 — variant (hand conversion bar/kJ → Pa/J**, `ees_import.md` §6).
  From `EES_ok/scroll_compressor.EES` (identical to the CoolSolve example
  `CSX-042` except `T_ev`): parameter values ×1000 (W_dot_loss0 0.2 kW →
  200 W; AU_su1 0.05 kW/K → 50 W/K, scaled by (M_dot/M_dot_ref)^0.8;
  AU_ex2 0.05 → 50 W/K; AU_amb 0.01 → 10 W/K; C_sd 0.04/10 kW⁻¹ → 4e-6 W⁻¹);
  guess values converted accordingly (pressures ×1e5, energies/entropies/
  powers ×1e3); `w_nad = v_fi*(p_ex2-p_ad)*1E+5/1E+3` → `w_nad =
  v_fi*(p_ex2-p_ad)` (the bar→Pa and J→kJ factors cancel in SI). Two genuine
  (numerically negligible) errors of the original fixed: the supply pressure
  drop `C²/(2000·v)` (a kPa-units leftover, giving 0.27 Pa instead of
  2.7e-3 Pa) becomes `C²/(2·v)` in Pa; the comment `C_dot [kW/K]` → `[W/K]`.
  Default `T_ev` = 30 °C (last run of the EES original, also the verification
  point); the CoolSolve example uses −1 °C.
- **2026-10-05 — finding on `CSX-042`.** The CoolSolve example solves, but to
  a **spurious solution** (N_cp = 0.58 rev/s, M_dot = 0.002 kg/s, IMEP =
  1.9 MPa): its bar/kJ parameter values (AU = 0.05, W_dot_loss0 = 0.2, the
  ×100 factor on w_nad) were left unchanged while the property calls return
  Pa/J. The converted variant reproduces the EES reference instead. Not a
  CoolSolve bug (any solver converges to a solution of the equations it is
  given); the example would deserve a fix in the CoolSolve repository.

## Limitations and CoolSolve gaps

- The parameters are identified on one compressor family (Copeland ZR72KC-TFD,
  R22); the model itself is fluid- and machine-independent once the parameters
  are re-identified.
- The AU scaling exponent (0.8) and the leakage area are empirical; the
  exhaust pressure drop uses the incompressible nozzle equation of the
  original (the compressible alternative `M_dot_r_bis` is computed for
  comparison).
- Lubricant circulation, oil sump and liquid flood-back are not modelled
  (as in Winandy et al. 2002).
- No CoolSolve gap met: `max()`, `specheat` and `$ifnot parametrictable` are
  all supported.

## Related models

- `CSL-0001` refrigeration cycle with a simple compressor model: same
  component at level 1 (clearance-volume volumetric efficiency + linear loss
  law) instead of the full semi-empirical decomposition.
- CoolSolve example `scroll_compressor.eescode` (`CSX-042`): simplified
  version of this model (stays in the CoolSolve repository as a test case);
  LaboThapPy has a Python implementation of the same model family.
