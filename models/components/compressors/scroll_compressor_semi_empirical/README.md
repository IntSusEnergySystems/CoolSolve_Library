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
`scroll_compressor`, converted from bar/kJ to SI units) is included, and a **test-campaign variant**
that drives the same simplified model with 28 measured R22 test points of the
identification file of the model and compares it with the measurements.

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

**Variant** `scroll_compressor_semi_empirical_test_campaign.eescode` (candidate
`TM-0278`): the same equations as the simplified variant, but the compressor
alone is driven by the measured suction pressure and temperature and the
measured discharge pressure of the test point `i` (default `i = 28`, the last
run stored in the EES file) read in
`scroll_compressor_semi_empirical_test_campaign-lookup_1.csv` (28 rows; bar,
°C, rpm, kg/s, W). It outputs the measured values and the errors `ERRm`,
`ERRw` (relative, (measured − model)/measured, in %) and `ERRtex_cp` (K). The variant
needs its `.initials` file (the converted EES stored solution; 18 iterations).
The 28 points are run one after the other (CoolSolve has no table run), each
point starting from the solution of the previous one (`-g` rewrites the
`.initials`), in a copy of the folder:

```bash
for i in $(seq 1 28); do
  sed "s/^i = [0-9]*/i = $i/" scroll_compressor_semi_empirical_test_campaign.eescode > work.eescode
  coolsolve -g work.eescode   # needs work.initials + work-lookup_1.csv: copies of the files of the variant
done
```

(the model file name gives the names of the companion files: copy
`..._test_campaign.initials` to `work.initials` and the table to
`work-lookup_1.csv`). The results of this loop (CoolSolve 0.4.0, every point
converged) are in `scroll_compressor_semi_empirical_test_campaign_results.csv`.

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

3. **Test-campaign variant vs EES stored solution** (`TM-0278`, last run
   stored in the file = row 28 of the table, SI-converted reference,
   `compare_solution.py`, 76 common variables, rtol = 1e-3): 52 variables are
   within 0.1 %; the 24 others stay within 1.3 % except the three discussed
   below. The stored solution does not contain `M_dot`, `W_dot` nor `ERRm`/
   `ERRw` (not decoded by `ees_extract.py`: the variable-name records of these
   variables could not be read); recomputed from the stored values
   (`M_dot = V_dot_su/v_su`, `W_dot = W_dot_in (1 + alpha) + W_dot_loss0`):
   M_dot 0.066750/0.066757 kg/s, W_dot 5271.1/5268.4 W (EES/CoolSolve); the
   other key values: t_ex_cp 126.33/125.95 °C, t_w_cp 116.86/116.54 °C,
   N_cp 48.946/48.946 rev/s, epsilon_v_cp 0.9025/0.9033, epsilon_s_cp
   0.6209/0.6211. Deviations: `DELTAp_su1_cp` (0.0416 Pa EES, 4.2e-4 Pa here,
   the same corrected `/2` instead of `/2000` as in the simplified variant,
   numerically irrelevant), `ERRtex_cp` (2.27/2.65 K: a 0.38 K difference of
   the property models on `t_ex_cp`, amplified by the subtraction),
   `Q_dot_amb_mes_cp` (3 %, a small difference of two large terms); the
   other small differences (`DELTAt_ex12_cp` 1.3 %, all others < 0.8 %) are
   consistent with the R22 properties of EES 6.4 vs CoolProp at 2.4 bar /
   140 °C (not isolated).
   The comment block *Solution run 10* of the EES file (row 10) is also
   reproduced: M_dot 0.1855/0.186 kg/s, W_dot 9379/9386 W, ERRm +0.80/+0.8 %,
   ERRw −1.24/−1.3 %, N_cp 48.12/48.12 rev/s.
4. **Model vs measurements, 28 test points** (see the next section): this is an
   experimental comparison, not a verification of the code.

## Comparison with the test campaign (`TM-0278`)

The identification file `3_3_1_Identification.EES` of J. Lebrun (JL080205)
holds the table of test points used by Winandy et al. (2002) to identify the
parameters of this model (R22, hermetic scroll compressor of 174 cm³, about
2900 rpm, ambient 30 °C): suction pressure 2.4–7.3 bar, discharge pressure
11.9–25.3 bar, suction temperature 18.3–25 °C, 28 points. The 11 columns are:
suction pressure, ΔP supply, suction temperature, temperature after heating-up
(T1'), discharge pressure, ΔP exhaust, discharge temperature, temperature at
the end of the compression (T2'), speed, mass flow rate and electrical power.
Only the suction state, the discharge pressure and the ambient temperature
(30 °C, a constant of the model) are inputs of the model; the speed is
predicted (motor slip). The two ΔP columns and T1', T2' are not used by the
model (their units could not be recovered from the EES file; the ΔP are
probably in mbar).

The model is run on every point with the identified parameters of the file
(no re-fit), CoolSolve 0.4.0, R22 by CoolProp. With `err = (measured −
model)/measured`:

| Quantity | mean abs. error | max abs. error | mean signed error |
|---|---:|---:|---:|
| Mass flow rate ṁ | 1.41 % | 3.20 % (point 26) | +0.74 % |
| Electrical power Ẇ | 0.95 % | 2.87 % (point 4) | −0.35 % |
| Discharge temperature t_ex | 1.56 K | 5.41 K (point 27) | −0.13 K |

The mass flow rate is within 3 % for 26 of 28 points (the two exceptions are
points 26 and 27, at 3 bar suction pressure and the second and third lowest
flow rates, where the model overestimates the flow by 3.2 and 3.1 %), the
power within 3 % for all 28 points. The model predicts the speed within
10 rpm (mean 4.5 rpm) of the measured one. The largest discharge-temperature
errors are at the lowest flow rates (points 26, 27: +4.7 and +5.4 K, and 28:
+2.7 K: the model is too cold, as `err` is measured − model); the identified parameters were tuned
manually against this table by the original authors, so the agreement is a
fit quality, not an independent validation.

| i | p_su [bar] | p_ex [bar] | ṁ meas. [kg/s] | ṁ model | err [%] | Ẇ meas. [W] | Ẇ model | err [%] | t_ex meas. [°C] | t_ex model | err [K] |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1 | 6.3 | 21.5 | 0.1940 | 0.1949 | -0.44 | 9252 | 9302 | -0.54 | 97.6 | 98.2 | -0.57 |
| 2 | 7.33 | 25.33 | 0.2242 | 0.2228 | +0.64 | 10820 | 10817 | +0.03 | 106.4 | 107.2 | -0.84 |
| 3 | 7.3 | 21.7 | 0.2292 | 0.2253 | +1.72 | 9291 | 9433 | -1.53 | 94.4 | 96.1 | -1.66 |
| 4 | 7.3 | 17.3 | 0.2339 | 0.2298 | +1.77 | 7520 | 7736 | -2.87 | 79.8 | 81.5 | -1.72 |
| 5 | 7.3 | 11.9 | 0.2382 | 0.2357 | +1.08 | 5653 | 5620 | +0.59 | 62.2 | 62.4 | -0.23 |
| 6 | 6.8 | 13.6 | 0.2171 | 0.2150 | +0.95 | 6153 | 6268 | -1.87 | 71.2 | 72.1 | -0.87 |
| 7 | 6.8 | 19.4 | 0.2118 | 0.2092 | +1.23 | 8369 | 8527 | -1.89 | 91.3 | 92.8 | -1.47 |
| 8 | 6.8 | 24.3 | 0.2062 | 0.2045 | +0.81 | 10347 | 10402 | -0.53 | 108.2 | 109.2 | -0.98 |
| 9 | 6.2 | 24.3 | 0.1785 | 0.1832 | -2.63 | 10321 | 10370 | -0.48 | 115.0 | 115.9 | -0.85 |
| 10 | 6.2 | 21.7 | 0.1870 | 0.1855 | +0.80 | 9264 | 9379 | -1.24 | 105.7 | 106.7 | -1.02 |
| 11 | 6.2 | 15.3 | 0.1937 | 0.1914 | +1.21 | 6729 | 6904 | -2.60 | 82.1 | 83.2 | -1.12 |
| 12 | 6.2 | 11.9 | 0.1967 | 0.1947 | +1.00 | 5555 | 5568 | -0.23 | 69.6 | 70.0 | -0.35 |
| 13 | 5.8 | 13.5 | 0.1819 | 0.1788 | +1.72 | 6126 | 6175 | -0.81 | 78.6 | 79.7 | -1.06 |
| 14 | 5.8 | 19.4 | 0.1778 | 0.1735 | +2.44 | 8430 | 8472 | -0.50 | 100.1 | 102.8 | -2.66 |
| 15 | 5.8 | 25.3 | 0.1720 | 0.1686 | +2.00 | 10998 | 10726 | +2.48 | 122.7 | 124.5 | -1.85 |
| 16 | 5 | 21.7 | 0.1445 | 0.1443 | +0.16 | 9353 | 9303 | +0.54 | 123.2 | 122.5 | +0.69 |
| 17 | 5 | 17.3 | 0.1478 | 0.1477 | +0.08 | 7546 | 7607 | -0.81 | 105.8 | 104.1 | +1.72 |
| 18 | 5 | 11.9 | 0.1524 | 0.1522 | +0.12 | 5460 | 5493 | -0.60 | 81.4 | 80.4 | +1.04 |
| 19 | 5 | 19.4 | 0.1479 | 0.1460 | +1.25 | 8357 | 8419 | -0.74 | 110.8 | 113.0 | -2.16 |
| 20 | 4.2 | 19.4 | 0.1211 | 0.1195 | +1.37 | 8360 | 8358 | +0.02 | 125.3 | 126.3 | -1.00 |
| 21 | 4.2 | 15.3 | 0.1235 | 0.1224 | +0.86 | 6743 | 6768 | -0.36 | 108.4 | 106.5 | +1.91 |
| 22 | 4.2 | 13.5 | 0.1253 | 0.1238 | +1.27 | 6046 | 6062 | -0.27 | 98.9 | 97.6 | +1.33 |
| 23 | 3.5 | 11.9 | 0.1026 | 0.1019 | +0.76 | 5404 | 5373 | +0.57 | 100.6 | 100.1 | +0.55 |
| 24 | 3.5 | 15.3 | 0.1024 | 0.0995 | +2.82 | 6687 | 6708 | -0.32 | 118.1 | 119.4 | -1.31 |
| 25 | 3.5 | 17.3 | 0.1012 | 0.0982 | +2.97 | 7500 | 7487 | +0.17 | 128.6 | 130.6 | -1.98 |
| 26 | 3 | 15.3 | 0.0810 | 0.0836 | -3.20 | 6793 | 6662 | +1.92 | 136.4 | 131.7 | +4.75 |
| 27 | 3 | 13.5 | 0.0822 | 0.0847 | -3.06 | 5993 | 5957 | +0.59 | 125.6 | 120.2 | +5.41 |
| 28 | 2.4 | 11.9 | 0.0674 | 0.0668 | +1.03 | 5343 | 5268 | +1.40 | 128.6 | 126.0 | +2.65 |

Full results (14 columns, also `epsilon_v_cp`, `epsilon_s_cp`, `t_w_cp`): `scroll_compressor_semi_empirical_test_campaign_results.csv`.

**Data provenance.** The table contains only measured compressor quantities
(no personal data). The EES file does not name the test rig nor the date of
the tests; it states that "the test results presented in the lookup table are
used to identify the parameters" of the model of Winandy, Saavedra & Lebrun
(2002), and belongs to the ULiège Thermodynamics Laboratory collection (file
by J. Lebrun, JL080205, `license_status` *own* in the inventory), hence its
publication with the model under the library licence. The inventory
description of `TM-0278` speaks of a "66-row" table: this came from the
mis-decoding of the table by `ees_extract.py` (it reports a spurious
`Lookup 1 (65×2)`); the table of the file has **28 data rows** (30 stored
rows, the last two empty), decoded by hand from the binary file (see the
conversion log).

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
  bar/kJ);
- test-campaign variant, candidate `TM-0278`:
  `~/Nextcloud/thermo_models/modeles/JL/new/scroll JL080205/3_3_1_Identification.EES`
  (EES 6.395, bar/kJ, author J. Lebrun, file JL080205).

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

- **2026-10-31 — test-campaign variant (`TM-0278`, task C-402, T-MERGE).**
  `ees_extract.py` on `3_3_1_Identification.EES` (EES 6.395, unit system
  `SI MASS DEG BAR C KJ`): the equations and the 91 stored variables are
  decoded, but the lookup table is **not**: the tool reports two spurious
  tables `Lookup 1 (65×2)` with two garbled columns (T2, Nrpm; one stray
  value −6.8e-40). The real table (11 columns P1, DP1, T1, T1', P2, DP2, T2,
  T2', Nrpm, Mr, Wmot; 30 stored rows, 28 filled) was decoded by hand: the
  column blocks are at a regular 342-byte stride (header, then 30 cells of
  10-byte x87 extended values), the 11 names and the values were checked
  against the *Solution run 10* comment of the file (row 10: t_su2 42.5,
  M_dot_mes 0.187, W 9264 W, N 2891 rpm, ΔP_ex 112.6) and against the stored
  last-run values (row 28: p_su 2.4 bar, p_ex 11.9 bar, t_ex_mes 128.6 °C,
  Madim 0.2698). Registered tool bug `CS-BUG-EXTRACT-TABLE-FP` (extra evidence added
  from this file). The model equations are the same as those of the simplified
  variant (identical equation blocks after diff, same parameters), converted
  from bar/kJ like it: parameters ×1000 (W_dot_loss0 0.2 kW → 200 W,
  AU 0.05/0.01 kW/K → 50/10 W/K, C_sd 0.04/10 kW⁻¹ → 4e-6 W⁻¹),
  `w_nad` without the 1E+5/1E+3 factor, the supply pressure drop
  `C²/(2000 v)` corrected to `C²/(2 v)`; the new part is the input block: the
  table is kept in the original units (bar, °C, rpm, kg/s, W; column
  `Wmot` is in W: the original divides it by 1000 to get kW) and converted in
  the equations (`p = lookup(i,1)*1E+5`, `W_dot_mes = lookup(i,11)`); the row
  `i` is a model constant (it was set in the EES Diagram window) with the
  last-run value 28. Table columns `T1'`, `T2'` are written `T1p`, `T2p` in
  the CSV header. Guess values: the stored solution converted to SI (the EES
  enthalpies and entropies are shifted by +155 279 J/kg and +824.6 J/kg-K to
  the CoolProp reference state; `M_dot`, `W_dot` recomputed from the stored
  values); without them the 34-equation block does not converge. The loop
  over the 28 points is the shell loop of *How to run* (CoolSolve has no
  table runs): every point converged. Results unchanged otherwise.

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
- `CSL-0020` dry air screw compressor with internal leakage: the same
  equivalent-nozzle leakage physics at a simpler level (fixed parameters,
  ideal-gas air).
- CoolSolve example `scroll_compressor.eescode` (`CSX-042`): simplified
  version of this model (stays in the CoolSolve repository as a test case);
  LaboThapPy has a Python implementation of the same model family.
- `CSL-0037` *scroll_expander_semi_empirical*: the expander counterpart of
  this model (same semi-empirical methodology: supply losses, leakage,
  mechanical losses, global isentropic effectiveness).
- `CSL-0078` *brine_to_water_heat_pump_refsim*: the same scroll machine inside a
  brine-to-water heat pump of the ULiège model bank, where it is described step
  by step (suction heating-up, isentropic compression to an adapted pressure,
  isochoric compression, exhaust cooling-down, leakage through the throat).
- `CSL-0156` *refrigeration_screw_compressor_r22*: the screw-compressor reference
  model of the same laboratory series (physical leakage model instead of the
  semi-empirical parameters), closed on an R22 cycle with sliding-valve part load.
- `CSL-0167` *reciprocating_polynomial_r22*: the reciprocating (piston)
  counterpart in the same JL080205 reference series (clearance-volume
  re-expansion and motor slip instead of leakage and adapted pressure).
- `CSL-0136` *polynomial_compressor_en12900*: a compressor map taken from
  catalogue data (EN 12900 polynomials for the isentropic and the volumetric
  efficiency) instead of a semi-empirical identification; the other way of
  getting the two efficiencies this model computes.
- `CSL-0260` *scroll_compressor_reed_valve*: the reference scroll model with a discharge reed valve (R407C), same ULiège model bank.
