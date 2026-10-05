# Scroll expander semi-empirical model

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0037`

Semi-empirical model of a scroll (positive-displacement) expander, originally
written as an EES `MODULE expander(...)` called once from the main program.
The library version flattens the module equations into the main program
(library decision D10, CoolSolve does not implement `MODULE`/`SUBPROGRAM`,
`CS-GAP-MODULE`). From the machine geometry, the loss parameters and the
supply state it computes the mass flow rate, the shaft power, the calculated
exhaust state and the global isentropic effectiveness. The module was designed
to be reused inside ORC cycle models (see the merged source TM-0272 below).

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | R123 (default run) |
| **Size** | 82 equations, one implicit block of 40 variables |
| **Source** | S. Quoilin (ULiège), EES file `expander_module.EES` (2008), transcribed as CoolSolve example `expander_module.eescode` |
| **Authors** | Sylvain Quoilin (ULiège Thermodynamics Laboratory) |
| **License** | MIT |
| **CoolSolve** | v0.3.0@536d427 — runs from the shipped `.initials` with the shipped `coolsolve.conf` (Newton fails on the 40-variable block, TrustRegion converges); import verified against the EES solution report (see *Verification*) |

## Model

Given the supply state (`p_r_su_exp`, `t_r_su_exp`), the exhaust pressure and
the rotational speed, the model computes (variable names as in the original):

- **Supply**: throttling through an equivalent cross-section `A_thr_su`
  (diameter `d_su`) with an incompressible-flow pressure drop, and an
  effectiveness–NTU wall heat transfer with a part-load conductance law
  `AU_su_exp_n*(M_dot_r_exp/M_dot_r_exp_n)^0.6`, down to the state
  (`P_r_su1_exp`, `t_r_su1_exp`);
- **Expansion**: isentropic from `v_r_su1_exp` up to the built-in volume
  `v_r_in_exp = r_v_in * v_r_su1_exp` (adapted pressure `P_r_in_exp`), then
  isochoric to the exhaust pressure; the two specific works add up to
  `w_in_exp` (also equal to `h_r_su1_exp − h_r_ex2_exp`);
- **Leakage**: flow through the area `A_leak` at the critical (choking)
  pressure `P_r_thr`, with the isentropic exponent `gamma_r` derived from the
  isentropic relation between the supply and throat states; the leakage mixes
  back with the main flow at the exhaust;
- **Exhaust**: effectiveness–NTU wall heat transfer (part-load law with
  `AU_ex_exp_n`), giving the calculated exhaust state `h_r_ex_exp`,
  `t_r_ex_exp`;
- **Mechanical losses** `W_dot_loss_exp = 2*PI*N_rot_exp/60*T_m` and an
  ambient heat balance fixing the wall temperature `t_wall_exp`;
- **Global isentropic effectiveness**
  `epsilon_s_exp = W_dot_sh_exp / W_dot_sh_exp_s`.

## How to run

```bash
coolsolve ./scroll_expander_semi_empirical.eescode
```

The shipped `.initials` hold the converged solution; `coolsolve.conf` adds
TrustRegion to the solver pipeline because Newton alone fails on the
40-variable algebraic block (`SingularJacobian`).

## Results (default run, R123)

| Inputs | Value | Outputs | CoolSolve | EES report |
|---|---:|---|---:|---:|
| `p_r_su_exp` / `t_r_su_exp` | 9.6 bar / 170 °C | `M_dot_r_exp` mass flow [kg/s] | 0.07850 | 0.07841 |
| `p_r_ex_exp` | 1.3 bar | `W_dot_sh_exp` shaft power [W] | 2172 | 2202 |
| `N_rot_exp` | 2500 1/min | `t_r_ex_exp` exhaust temperature [°C] | 114.1 | 116.3 |
| `r_v_in` / `V_s_cp` | 4.05 / 148 cm³ | `epsilon_s_exp` isentropic effectiveness [-] | 0.657 | 0.656 |
| `A_leak` / `d_su` | 4.525e-6 m² / 5.749e-3 m | `w_in_exp` specific work [J/kg] | 37 156 | – |
| `T_m` / `M_dot_r_exp_n` | 0.5323 / 0.12 | `W_dot_loss_exp` losses [W] | 139.4 | – |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): e.g. a parametric sweep
     of epsilon_s_exp or W_dot_sh_exp vs N_rot_exp, figures/scroll_expander_semi_empirical_sweep.png -->

## Verification

Reference: the LaTeX **solution report** (`EES_ok/expander_module.tex`) and
residuals window dump (`EES_ok/expander_module.residuals`) shipped in CoolSolve
`misc/EES_ok.zip` next to the original `.EES` — all 103 equation residuals are
below 1.1·10⁻¹² (relative) at that solution. The **variable records decoded from the binary `.EES` by
`ees_extract.py` are stale** for this file (they mix at least two older runs:
`r_p_exp = 3.33` instead of 7.38, `C_dot_su_exp = inf`) and were **not** used;
reported as tool bug `CS-BUG-EXTRACT-STALE`.

`compare_solution.py` against the 21 main-program variables of the solution
report (`rtol=0.001`): `21 common variables, 4 differ`. The 17 fixed inputs
agree exactly; the computed outputs differ by:

| Variable | EES report | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `epsilon_s_exp` | 0.656 | 0.657325 | 2.02e-03 |
| `M_dot_r_exp` | 0.07841 | 0.0785037 | 1.19e-03 |
| `t_r_ex_exp` | 116.3 | 114.081 | 1.91e-02 |
| `W_dot_sh_exp` | 2202 | 2172.15 | 1.36e-02 |

These deviations are attributed to the R123 property differences between EES
9.920 and CoolProp (the reference values are also rounded to 4–5 significant
digits in the report); the largest one (1.9 % on the exhaust temperature,
i.e. 2.2 K) is within the "up to a few %" expected for older EES fluid models
(CoolSolve `docs/ees_import.md` §11). The solution is the same physical branch
(all effectivenesses in [0, 1], `w_exp_2 > 0`, ambient heat balance closed) and
satisfies the equations to 1e-9. Module-internal variables have no reference
values (the solution report lists main-program variables only).

## Source and attribution

Component model written by **Sylvain Quoilin** (ULiège Thermodynamics
Laboratory, 2008-03-18 per the thermo_models copy), reused in ORC cycle models.
Source files (MIT, collection of S. Quoilin):

- CoolSolve example (equation-identical transcription of the original):
  `~/git/CoolSolve/examples/expander_module.eescode` (inventory `CSX-019`),
- original EES file with stored solution, residuals and solution report:
  `~/git/CoolSolve/misc/EES_ok.zip`, `EES_ok/expander_module.EES` (EES 9.920),
- module-only variant (same module equations, the main-program inputs
  commented out for reuse inside a calling program):
  `~/Nextcloud/thermo_models/modeles/ExpanderSimpleModelSQ080318.EES`
  (inventory `TM-0272`) and its copy `ExpanderSimpleModelSQ110701.EES`
  (inventory `TM-0273`).

## Conversion log

- **2026-10-05 — import and MODULE flattening (decision D10).** The EES
  original is a `MODULE expander(...)` with a single `CALL`. Its 65 equations
  were copied into the main program with the formal arguments replaced by the
  actual arguments of the call: `M_dot_r_nom → M_dot_r_exp_n` (2 equations),
  `d_thr_su → d_su` (1 equation); the formal argument `t_amb` is not used in
  the module body and disappears. The module-internal variables already carry
  the `_exp` suffix, which serves as the per-call tag; they were kept
  unchanged and collide with no main-program variable. The first module
  equation `V_s_exp = V_s_cp/r_v_in` is textually identical to a main-program
  equation (in EES they act on two distinct variables, module-local and main);
  it is kept once. `$bookmark expander_model` (an EES GUI navigation tag) and
  the `module`/`call`/`end` lines were removed. The flattened file is valid
  EES. *C-46 check:* a normalised line comparison of the file with the
  extraction of the original (formals replaced, `$` directives and
  module/call/end lines ignored) shows no other difference; the 20
  formal-actual link equations that EES generates (`expander\1.M_dot_r_nom=
  M_dot_r_exp_n`, … in `EES_ok/expander_module.residuals`) are absorbed by the
  replacement of the formals. Unit system already SI-C-Pa-J; comments translated to English; standard
  header added.
- **Level justification** (taxonomy §3): equations 82 (50–300 → 1), largest
  algebraic block 40 (> 30 → 2), semi-empirical physics → 1, needs curated
  guesses and a solver-pipeline setting → 1; total 5 → level 3.
- **Solver**: from the shipped `.initials` (converged solution), the default
  Newton pipeline fails on the 40-variable block with `SingularJacobian`;
  `coolsolve.conf` adds TrustRegion (8 iterations). Deep-search
  (multi-start) also recovers the solution from rough guesses, giving the
  same point.

## Related models

- `CSL-0007` *scroll_compressor_semi_empirical*: same semi-empirical
  methodology for the compressor of the same family.
- `CSL-0036` *orc_extraction_r134a*: ORC with two-stage scroll expanders —
  the application the module was written for.
- See also the CoolSolve example `expander_module.eescode` (kept in CoolSolve
  as a test case).
