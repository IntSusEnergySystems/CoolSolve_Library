# Scroll compressor with discharge (reed) valve - reference model

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0260`

Semi-empirical reference model of a hermetic scroll compressor equipped with a discharge
(reed) valve, extending the model of Winandy, Saavedra & Lebrun (2002) implemented in
[`CSL-0007`](#related-models): supply heating-up against a fictitious wall, mixing with the
internal leakage (choked isentropic throat flow), isentropic compression to the adapted
pressure, isochoric compression to the exhaust pressure (with the "star" correction when the
adapted pressure is lower), exhaust cooling-down, then **choked flow through the discharge
valve, which fixes the mass flow rate**. Electromechanical losses and a fictitious-wall heat
balance with the ambient close the energy budget. The parameters (few and physically
meaningful) were identified from the Copeland ZH15K4E-TFD catalogue; a reduced evaporator and
condenser at imposed saturation temperatures close the refrigerant cycle (R407C).

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | R407C |
| **Size** | 162 equations (largest block: 66) |
| **Source** | `~/Nextcloud/thermo_models/Model data bank/Compressors/SCROLLCOMPRESSORWITHREEDVALVE_REFSIM_MODEL_VL080229.zip!/scrollCompressorWithReedValve_RefSim_EES_Model_VL080229.EES` (EES 7.888) |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory), 2008-02-19; model of Winandy, Saavedra & Lebrun (2002) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution (see Verification) |

## Problem statement

The model predicts the mass flow rate, the electrical power, the exhaust temperature and the
energies of a scroll compressor at given cycle boundary conditions (evaporating/condensing
temperatures, superheat, subcooling), from a small set of physically meaningful parameters
identified on catalogue data. It is the discharge-valve companion of the Winandy scroll
compressor model: the exhaust (reed) valve makes the mass flow rate a *result* of the valve
flow capacity instead of an input, and the exhaust pressure drop appears as a computed
pressure ratio `r_p_ex = p_ex_cp/p_ex1_cp` ≈ 0.88 at the default point.

## Model

Compression path (states 1-7 in the state-point block of the `.eescode`):

1. **su**: suction state, `t_sat_su_cp + DELTAt_oh_ev` (superheat imposed by the cycle);
2. **su → su1**: heating-up against the fictitious wall (`NTU` effectiveness, `AU` scaling
   with `M_dot^0.8`, wall temperature `t_w_cp`);
3. **su1 → su2**: mixing with the internal leakage coming back from the exhaust plenum
   (isentropic choked throat flow through `A_leak_cp`, critical pressure
   `P_thr_crit = P_ex1_cp*(2/(gamma+1))^(gamma/(gamma-1))`, polytropic expansion `ex2 → thr`);
4. **su2 → in**: isentropic compression to the adapted pressure (built-in volume ratio
   `r_v_in_cp`);
5. **in → ex2**: isochoric compression to the exhaust pressure; when the adapted pressure is
   lower than the exhaust pressure, the "star" correction of the original applies
   (clearance volume `C` in the volume balance, `IF(A,B,X,Y,Z)` on
   `p_in_cp` vs `p_ex2_cp`);
6. **ex2 → ex1**: exhaust cooling-down against the fictitious wall;
7. **ex1 → ex**: pressure drop through the discharge (reed) valve of diameter `d_ex`:
   isentropic choked flow, `M_dot_r = C_thr_ex_cp*A_ex/v_thr_ex_cp`, which **fixes the mass
   flow rate**; `p_ex_cp` at the dew point of the condensing pressure.

Energy: `W_dot_cp = W_dot_in_cp + W_dot_loss0_cp + alpha_cp*W_dot_in_cp`; wall heat balance
`W_dot_loss_cp = Q_dot_su_cp + Q_dot_ex_cp + Q_dot_amb_cp` determines the wall temperature
`t_w_cp`. Efficiencies: volumetric `epsilon_v_cp = v_su_cp/v_su1_cp`, global isentropic
`epsilon_s_cp = w_s_cp/w_cp`. The reduced evaporator/condenser compute `Q_dot_ev`, `Q_dot_cd`
at imposed `t_ev`, `t_cd` (mid-quality saturation pressures, manufacturer convention).

| Inputs | Outputs |
|---|---|
| `fluid$`, `t_ev`, `t_cd`, `DELTAt_oh_ev`, `DELTAt_sc_cd`, `t_amb` | `M_dot_r`, `W_dot_cp`, `t_ex_cp` |
| `AU_amb_cp`, `AU_su_cp_n`, `AU_ex_cp_n`, `A_leak_cp`, `W_dot_loss0_cp`, `alpha_cp` | `Q_dot_ev`, `Q_dot_cd`, `t_w_cp`, `M_dot_leak_cp` |
| `d_ex`, `C`, `corr`, `r_v_in_cp`, `M_dot_r_cp_n`, `N_rot` | `epsilon_v_cp`, `epsilon_s_cp`, `r_p_cp`, `r_p_ex`, `V_s_cp`, `V_dot_s_cp_m3h`, state points `P[i]`, `h[i]`, `T[i]`, `s[i]` |

## How to run

```bash
coolsolve ./scroll_compressor_reed_valve.eescode
```

The `.initials` file holds the solution of the default operating point and the good guesses of
the "star" correction block (`w_in2_cp|star` family), which EES does not store; without them
the 66-variable block does not converge. The default operating point is the last EES run of
the source file: `t_ev = 10 °C`, `t_cd = 50 °C`, R407C, `N_rot = 3000 1/min`.

## Results (default operating point)

| Quantity | EES (stored) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `M_dot_r` [kg/s] | 0.13402 | 0.13829 | 3.1e-2 |
| `W_dot_cp` [W] | 5578.9 | 5625.8 | 8.3e-3 |
| `Q_dot_ev` [W] | 20403 | 21539 | 5.3e-2 |
| `Q_dot_cd` [W] | 25779 | 26969 | 4.4e-2 |
| `t_ex_cp` [°C] | 79.96 | 77.83 | 2.7e-2 |
| `t_w_cp` [°C] | 62.87 | 61.31 | 2.5e-2 |
| `epsilon_s_cp` [-] | 0.66111 | 0.66039 | 1.1e-3 |
| `epsilon_v_cp` [-] | 0.94953 | 0.94875 | 8.2e-4 |
| `r_p_cp` [-] | 2.95903 | 2.96410 | 1.7e-3 |
| `P_ev` [Pa] | 704184 | 709191 | 7.1e-3 |
| `P_cd` [Pa] | 2.0837e6 | 2.10211e6 | 8.8e-3 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the compression path](figures/scroll_compressor_reed_valve_ph.png)
     + one-line caption -->

## Verification

Reference: the **EES stored solution** of the source file (its last run, 1227 stored values,
121 common with this model), compared with `tools/compare_solution.py`:

- absolute `h`/`s`/`u`: **reference-state offset** between the two R407C property backends
  (EES mixture model vs CoolProp): `h` +138.9 to +142.9 kJ/kg (liquid/vapour), `s` +762.8
  J/kg-K on the vapour - the model chains its own property calls, so this offset does not
  affect the physics, only the comparison of absolute values (maximum rel. diff of the
  comparison: 5.25e-1, on `h_ex_cd`/`h_su_ev`);
- derived results: isentropic efficiency 1.1e-3, pressure ratio 1.7e-3, adapted pressure
  1.8e-3, exhaust-valve pressure ratio 2.2e-3, electromechanical losses 7.6e-3, electrical
  power 8.3e-3, condensing/evaporating pressure 8.8e-3/7.1e-3, mass flow rate 3.1e-2,
  condensing capacity 4.4e-2, refrigerating capacity 5.3e-2;
- the largest deviations sit on the mixture `c_p` (10-13 %) and on the small heating-up
  temperature difference `DELTAt_su_cp` (12 %): R407C mixture properties of EES and CoolProp
  differ by more than for pure fluids (same finding as `CSL-0078`, same model family).

The source file also contains a parametric table `Table 1` (80 runs x 41 columns: `t_cd`
20-50 °C, `t_ev` -25-10 °C, model results and Copeland catalogue data). Its row 70
(`t_ev = 10 °C`, `t_cd = 50 °C`) differs from the stored solution by 0.9-8 % on the thermal
quantities (e.g. `M_dot_r` 0.1288 vs 0.1340 kg/s): the table was apparently computed with
slightly different identified parameters than the last single run; the stored solution is the
reference used here.

## Source and attribution

- Source: `~/Nextcloud/thermo_models/Model data bank/Compressors/SCROLLCOMPRESSORWITHREEDVALVE_REFSIM_MODEL_VL080229.zip!/scrollCompressorWithReedValve_RefSim_EES_Model_VL080229.EES`
  (inventory row TM-0482, duplicate group DG-0116 with TM-0481 = `CSL-0007`).
- Authors: Vincent Lemort (ULiège Thermodynamics Laboratory), file dated 2008-02-19; the
  underlying model is Winandy, E., C. Saavedra O., J. Lebrun (2002), *Experimental analysis
  and simplified modelling of a hermetic scroll refrigeration compressor*, Applied Thermal
  Engineering 22, 107-120.
- Original disclaimer (paraphrased): freely distributed, may not be sold, the user is asked
  to cite the origin; accuracy not guaranteed.
- Licence of this import: MIT.

## Conversion log

- **2026-10-22 - import**: `tools/ees_extract.py` (EES 7.888); unit system already
  `SI MASS DEG PA C J`, no conversion needed. The 13 diagram-window inputs of the original
  (commented equations with `!! in diagram`) are restored as assignments with the values of
  the last EES run (`t_ev = 10` - the commented defaults were -25/20 °C; all identified
  parameters equal their commented values). French/English comments kept, nomenclature and
  header moved to this README, licence `{$ID$}` tag removed, dead commented block "4.4.
  Manufacturer data for validation" dropped (its catalogue values live in the parametric
  table of the source).
- **2026-10-22 - property-call rewrites (R407C CoolProp limitations, decisions D11/D12 style;
  the file stays valid EES)**:
  - `p_ev = pressure(fluid$,t=t_ev,x=0.5)` and `p_cd = pressure(fluid$,t=t_cd,x=0.5)`: the
    (T, x) pair returns NaN in CoolProp for the zeotropic R407C at mid-quality (dew x=1 and
    bubble x=0 work). Rewritten through the supported (P, x) pair, written implicitly in the
    pressure with the auxiliary unknowns `t_ev_x`, `t_cd_x` (`t_ev_x = TEMPERATURE(fluid$,
    P=P_ev, x=0.5)`, `t_ev_x = t_ev`); the solved `P_ev`/`P_cd` differ from EES by 0.7-0.9 %
    (dome of a different mixture EOS).
  - the three (v, u) property calls of the "star" block (`pressure/entropy/enthalpy(fluid$,
    v=v_in_cp|star, u=u_in_cp|star)`): CoolProp cannot invert the (U, V) pair for R407C (NaN,
    single-phase included). Rewritten: the auxiliary unknown `t_in_cp|star` gives `(p, t)` by
    inversion of the known `u|star` and `v|star` through `intenergy`/`volume` with the
    (P, T) pair, `h|star` follows from the identity `h = u + p*v` and `s|star` from the
    (P, H) pair. Valid where the star state is single-phase (the case at the operating
    point); EES evaluated the original calls also inside the dome.
  - state point `T[3] = temperature(fluid$,s=s_in_cp,v=v_in_cp)`: the (s, v) pair is not
    evaluated by CoolProp for R407C (`CS-GAP-PROP-SV`); state 3 is at the adapted pressure,
    so `temperature(fluid$,P=p_in_cp,s=s_in_cp)` is used.
  - `W_dot_loss_cp = Q_dot_su_cp + Q_dot_ex_cp + Q_dot_amb_cp`: the original writes the same
    equation as `0 = W_dot_loss_cp - ...`, which CoolSolve classifies as a check equation
    that does not join the solved system; same equation, standard form.
- **2026-10-22 - structural equation of the import**: `t_sat_ex_cp = t_sat_su_cd`. In the
  original, `t_sat_ex_cp` is determined through the composition
  `p_ex_cp = pressure(fluid$,t=t_sat_ex_cp,x=1)` with `P_ex_cp = P_cd`, i.e. both saturation
  temperatures are the dew temperature at the condensing pressure. Both equations are kept;
  the identity (exact within one property backend) keeps CoolSolve's system square - without
  it the structural analysis counts one equation short. The condenser-side glide of R407C
  remains visible through `t_sat_su_cd - t_sat_ex_cd` ≈ 4.6 K.
- **2026-10-22 - inputs of the solver**: `.initials` = solution of the default operating
  point plus hand-computed guesses for the "star" block (EES does not store the `|star`
  variables); without them the 66-variable block does not converge.
- **Level**: equations 162 (1) + largest block 66 (2) + arrays present (1) + no multi-zone (0)
  + semi-empirical identification (1) + curated guesses needed (1) = score 6 -> level 3.

## Limitations and CoolSolve gaps

- The (T, x) mid-quality inversion and the (U, V) pair are CoolProp limitations for
  pseudo-pure/zeotropic fluids (documented in the CoolSolve register,
  `CS-GAP-PROP-TQ-PSEUDOPURE` and `CS-GAP-PROP-UV`): they force the rewrites above, but the
  native file stays valid EES and runs, so `missing_features` is empty.
- Validity of the rewrites: the (P, x) inversion of the saturation pressures is exact for the
  manufacturer convention (quality 0.5 at the given temperature); the (P, T) rewrite of the
  "star" block is valid where that state is single-phase (the case at the operating point and
  along the parametric domain of the source table, where the adapted pressure stays below the
  exhaust pressure).
- The mass flow rate is a result of the discharge-valve flow capacity: sweeping `d_ex`
  changes `M_dot_r` at fixed cycle boundaries.

## Related models

- `CSL-0007` (*scroll_compressor_semi_empirical*): the same Winandy model without discharge
  valve and clearance (R22, Copeland ZR72KC-TFD); this model extends it with the discharge
  (reed) valve and the "star" correction (duplicate group DG-0116).
- `CSL-0078` (*brine_to_water_heat_pump_refsim*): same RefSim model family on R407C; documents
  the same property-backend deviations (reference states, 0.4-3.3 % on derived results) and
  the (s, v) rewrite used for state point 3.
- `CSL-0068` (*heat_pump_scroll_compressor_data_check*): R407C scroll-compressor data
  consistency check; documents the zeotropic behaviour of R407C saturation pressures in
  CoolProp (dew/bubble vs mid-quality).
