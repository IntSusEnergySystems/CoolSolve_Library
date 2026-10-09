# Hermetic reciprocating compressor reference model with polynomial laws (R22)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0167`

Semi-empirical "reference" model of a hermetic reciprocating (piston)
refrigeration compressor, closed on a simple R22 vapour-compression cycle. As
in the scroll reference of the same laboratory series (`CSL-0007`), the
refrigerant path is decomposed into six steps — supply pressure drop
(fixed-area obstacle), heating-up against a fictitious wall of uniform
temperature, isentropic compression, cooling-down to the wall, exhaust
pressure drop — but the flow rate follows the classical clearance-volume
re-expansion law and the motor slip grows linearly with the electrical power.
The identified parameters are imposed through scaled comparison variables
(AUD = AU per V_s^(2/3), FMEP_0); the polynomial laws identified from the
simulation results are listed in the header comment of the file.

| | |
|---|---|
| **Category** | Components › Compressors |
| **Fluids** | R22 |
| **Size** | 133 equations (largest block: 34) |
| **Source** | ULiège Thermodynamics Laboratory — file 3_2_3 of the reciprocating compressor series (JL080205) |
| **Authors** | TBD (J. Lebrun, ULiège Thermodynamics Laboratory, per the file series) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@7addbbc — verified against the EES stored solution (see *Verification*) |

## Problem statement

Reference model of the ULiège laboratory series: a hermetic piston compressor
(swept volume 2.08 L, 1250 rpm nominal, R22) is simulated in a cycle with
evaporation at 0 °C, condensation at 40 °C, 5 K superheat and 5 K subcooling.
Its parameters (flow-rate characteristic, heat-transfer conductances, power
losses) were identified "manually" from test data, as described in the file
header; the file also lists the parabolic polynomial laws identified for
Q_dot_ev, W_dot, M_dot and epsilon_v_cp as functions of t_ev (and t_cd), which
file 3_2_4 of the same series then uses to simulate the compressor without the
detailed model. The default run is the operating point stored in the EES file.

## Model

Six steps along the refrigerant path (as in the original):

1. **su → su1, supply pressure drop**: fixed-area obstacle (isentropic nozzle
   + isobaric diffusion), `DELTAp = C²/(2·v)`, area from the scaled diameter
   `delta_su_cp = d/(V_s)^(1/3)`;
2. **su1 → su2, heating-up**: fictitious wall of uniform temperature `t_w_cp`,
   ε-NTU exchanger, `AU_su1 = AUDsu·V_s^(2/3)`; the wall balance
   `W_dot - W_dot_in - Q_su1 - Q_ex2 + Q_amb = 0` closes the model;
3. **suction**: `M_dot = V_tr·N/v_su2` with the true swept volume
   `V_tr = V_s + V_c·(1 - v_su2/v_ex2)` (clearance gas re-expansion,
   `C_f = V_c/V_s` = 3.25 %); motor slip `N = N_nom·(1 - C_sd·W_dot)`;
4. **su2 → ex2, isentropic compression**; electrical power
   `W_dot = M_dot·w_s/epsilon_s` = `W_dot_in·(1 + alpha) + W_dot_loss0`;
5. **ex2 → ex1, cooling-down** to the same fictitious wall (ε-NTU,
   `AU_ex2 = AUDex·V_s^(2/3)`);
6. **ex1 → ex, exhaust pressure drop**: constant correlation
   `DELTAp = 2E5·M_dot²` Pa (fitted in bar in the original).

Cycle closure: saturation pressures at 0/40 °C, 5 K superheat, 5 K subcooling,
isenthalpic expansion; Carnot COP and second-law efficiency computed for
comparison.

| Inputs | Value | Outputs (default run) | Value |
|---|---|---|---|
| `t_ev` / `t_cd` | 0 / 40 °C | `M_dot` mass flow | 0.759 kg/s |
| `DELTAt_sh_ev` / `DELTAt_sc_cd` | 5 / 5 K | `W_dot` electrical power | 32.46 kW |
| `N_nom_cp` | 1250 rpm | `Q_dot_ev` / `Q_dot_cd` | 125.7 / 157.6 kW |
| `t_amb_cp` | 20 °C | `COP_c` / `COP_h` | 3.87 / 4.86 |
| `fluid$` | R22 | `t_ex_cp` discharge temperature | 78.4 °C |
| 10 identified parameters | see the `.eescode` file | `t_w_cp` fictitious wall | 63.6 °C |
| | | `epsilon_v_cp` / `epsilon_s_cp` | 0.870 / 0.673 |

## How to run

```bash
coolsolve ./reciprocating_polynomial_r22.eescode
```

The 34-equation compressor block **requires the guess values** of
`reciprocating_polynomial_r22.initials` (the EES solution): without them the
solve fails (SingularJacobian). With them it converges in 35 iterations. The
state points are available as the arrays `P[i]`, `h[i]`, `T[i]`, `s[i]`
(1 su, 2 su1, 3 su2, 4 ex2, 5 ex1, 6 ex, 7 condenser outlet, 8 evaporator
inlet) for the CoolSolve diagrams (*Overlay array path*).

## Results

Default run, CoolSolve (EES reference in parentheses): `M_dot` 0.7590 kg/s
(0.7578), `W_dot` 32.46 kW (32.48), `Q_dot_ev` 125.7 kW (125.6), `Q_dot_cd`
157.6 kW (157.5), `COP_c` 3.873 (3.866), `COP_h` 4.856 (4.849), `t_ex_cp`
78.41 °C (78.89), `t_ex2_cp` 82.80 °C (83.31), `t_w_cp` 63.57 °C (63.85),
`epsilon_v_cp` 0.8697 (0.8691), `epsilon_s_cp` 0.6728 (0.6726), `FMEP_0_cp`
63.46 kPa (63.46).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the R22 cycle
     through the compressor (states 1-8), figures/reciprocating_polynomial_r22_ph.png -->

## Verification

Vs the EES stored solution of the source file (extracted by `ees_extract.py`;
97 variables in common after the hand conversion of the reference values from
bar/kJ to Pa/J). With `compare_solution.py` (rtol 0.02): 14 variables differ,
of which **13 are absolute enthalpies/entropies carrying the R22
reference-state offset between EES 6.395 and CoolProp** (h: +155.2 kJ/kg, s:
+824 J/kg, both nearly constant across states; the isentropic relation uses
`s_su_cp` on both sides, so the offset cancels — `w_s` agrees to 1.7e-3), and
`C_sd_cp` differs by exactly the intentional unit conversion (8e-4 per kW →
8e-7 per W; the converted variable `N_cp` agrees to 1e-4). The remaining 83
variables all agree within **1.81e-02** (worst: `C_dot_su1_cp` 545.9/555.8
W/K, driven by `c_p_su1_cp` 720.4/732.3 J/kg-K, +1.65 %), median 7.9e-04 —
within the "older EES fluid model" tolerance (the R22 formulation of EES
6.395 differs from CoolProp, as documented at 1.4 % on the R22 cycle
`CSL-0001`). `M_dot`, `W_dot` and `W_dot_loss` are absent from the extracted
variable table (EES 6 record decoding, a known `ees_extract.py` limitation,
ees_import.md §13): hand-checked against the solution listing stored in the
file header — 0.75895/0.7578 (1.5e-03), 32463/32480 W (5.2e-04),
7282.5/7285 W (3.4e-04).

## Source and attribution

File `3_2_3_Polynomial_modelling.EES` of the reciprocating compressor series
"reciprocating JL080205" (J. Lebrun, ULiège Thermodynamics Laboratory; the
archive contains the identification file 3_2_1, the simulation file 3_2_2 and
the polynomial use file 3_2_4). Source:
`~/Nextcloud/thermo_models/modeles/JL/new/reciprocating JL080205.zip!/reciprocating JL080205/3_2_3_Polynomial_modelling.EES`
(EES 6.395). The compressor equations are the same as in file 3_2_2 of the
series, in the family of the Winandy et al. (2002) scroll reference model
(`CSL-0007`, which cites the scientific references).

## Conversion log

- **2026-10-09 — import (task C-159).** `ees_extract.py` on the source file:
  EES 6.395, unit system SI MASS DEG **BAR C KJ** → converted by hand to
  SI-°C-Pa-J (ees_import.md §6): all property calls now return Pa/J; the
  explicit bar factors were removed (`p_su1_cp = p_su_cp - C²/(2·v)`, the
  original divides by 1e+5); the empirical correlations keep their fitted
  coefficients with the unit converted (`DELTAp_ex1_cp = 2E5·M_dot²` for
  `2·M_dot²` bar; `C_sd_cp = 8E-7` 1/W and `C_sd_cp = C_rsd_cp/50000` for
  0.8e-3 per kW and `C_rsd_cp/50`; `FMEP_0_cp = 63.46E3` Pa for 63.46 kPa;
  `AUDsu/ex/amb = 10.32E3/6.137E3/0.7978E3` W/(K·m^(4/3)) for the kW/K-based
  values); parameter values and guess values (`.initials`) converted
  accordingly (pressures ×1e5, energies/powers/conductances ×1e3).
  Comments translated to English; the commented-out alternative parameter
  lines (`AU_*` direct values, `W_dot_loss0 = 3.3`, `C_sd_cp = 8e-4`,
  `Sp_cp = 2.854`) were removed: the identified parameters are imposed through
  the scaled comparison variables AUD/FMEP_0 kept active in the original; the
  ~100-line listing of the stored solution duplicated in a comment was removed
  (it matches the extracted reference; used for the hand-checks above). The
  polynomial-law comment block of the original is kept (values in kW, as in
  the original). Diagram-ready state arrays `P/h/T/s[1..8]` added as
  post-processing (results unchanged). No change to any equation of the
  original physics.
- **Level**: equations 133 → 1 (50–300); largest block 34 → 2 (> 30);
  arrays present → 1; single component → 0; semi-empirical calibration → 1;
  curated guesses needed (fails without `.initials`) → 1. Score 6 → **level 3**,
  same rating as the scroll reference `CSL-0007`.

## Limitations and CoolSolve gaps

- The parameters are identified on one machine (2.08 L hermetic piston
  compressor, R22 test data); the model structure is machine-independent once
  the parameters are re-identified.
- No lubricant model, no valve dynamics, constant exhaust pressure-drop
  correlation (as in the original).
- No new CoolSolve gap met: all functions used (`enthalpy`, `entropy`,
  `pressure`, `specheat`, `temperature`, `volume`, `exp`, `pi`) are supported.
- Known tool limitation (not re-reported): `ees_extract.py` decodes EES 6
  variable records on a best-effort basis — four spurious variables (`C`, `i`,
  `M`, `s`, `W_dot_cp` with placeholder values) and three missing ones
  (`M_dot`, `W_dot`, `W_dot_loss`), hand-checked here (ees_import.md §13).

## Related models

- `CSL-0007` *scroll_compressor_semi_empirical*: the scroll reference of the
  same laboratory series and methodology (leakage and adapted-pressure
  isochoric compression instead of the clearance re-expansion).
- `CSL-0022` *refrigeration_compressor_identification*: the same component at
  level 2, identified from two operating points with a four-parameter
  clearance/loss model.
- `CSL-0001` *refrigeration_cycle_simple_compressor*: the same cycle closure
  with a simple volumetric-efficiency compressor.
- `CSL-0156` *refrigeration_screw_compressor_r22*: the screw-compressor
  reference of the same series, closed on an R22 cycle.
- Files 3_2_1 (identification), 3_2_2 (simulation) and 3_2_4 (use of the
  polynomial model) of the same zip archive are not imported (see the
  inventory, TM-0497/TM-0498).
