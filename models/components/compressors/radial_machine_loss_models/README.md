# Radial compressor and radial turbine loss models (rotor, stator, nozzle)

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0328`

Translation of the **loss models of centrifugal compressors and radial-inflow turbines** of LaboThapPy: seven rotor losses
(incidence, friction, blade loading, clearance, mixing, disc friction, recirculation) and two vaned-stator losses (friction,
incidence) of a centrifugal compressor, and the nozzle and four rotor losses (incidence, passage, clearance, trailing edge) of
a radial turbine. One `FUNCTION` per loss, one `PROCEDURE` per blade row that sums them. The losses are specific enthalpy
losses in J/kg. The demonstration program evaluates them on a consistent set of illustrative velocity triangles (the source has
no example).

| | |
|---|---|
| **Category** | Components › Compressors (the turbine part is the radial counterpart of `CSL-0327` in Expanders and turbines) |
| **Fluids** | R134a (compressor demonstration), R245fa (turbine demonstration); the functions take numbers only |
| **Size** | 126 equations in the demonstration program (largest block 8) + 14 `FUNCTION` + 3 `PROCEDURE` |
| **Source** | [LaboThapPy](https://github.com/PyLaboThap/LaboThapPy) commit `f03f7f47`, files `labothappy/correlations/turbomachinery/radial_compressor_losses.py` and `labothappy/correlations/turbomachinery/radial_turbine_losses.py`; inventory row `LTP-052` (rows `LTP-003`, `LTP-067`, `LTP-068` are duplicates of it) |
| **Authors** | Basile Chaudoir (the only author of the two files in the repository history, 2025-09 to 2026-05) |
| **License** | Original: Apache-2.0 (`LICENSE.txt` of LaboThapPy); translation published under the library MIT licence |
| **CoolSolve** | 0.4.0 - **verified** against a re-run of the Python code (demonstration: 18 values, max relative deviation 5.3·10⁻¹²; random sweep: 680 values, below 9·10⁻¹⁰ for values above 0.01 J/kg) |

## Niche

No library model gives the **loss mechanisms of a radial (centrifugal or radial-inflow) machine from its geometry and velocity
triangles**. The nearest models are `CSL-0327` *axial_turbine_loss_models* (same idea for the blade rows of an **axial** turbine:
total-pressure loss coefficients of Aungier, Balje-Binsley, Kacker-Okapuu; different geometry, different loss set, and
coefficients instead of enthalpy losses), `CSL-0318` *cordier_specific_speed* (0D pre-design: specific speed and diameter, no
losses) and `CSL-0069` / `CSL-0023` (centrifugal compressor exercises: similarity factors, constant isentropic efficiencies, no loss breakdown). This
model is the next step down in detail for radial machines: given the triangles and the impeller, vane and nozzle geometry, it
tells **how many J/kg each mechanism costs**, the building block of a mean-line design. A search of `library.json` for *Jansen*, *Meroni*, *Wasserbauer*, *Moustapha*, *Rodgers*, *impeller*, *incidence*, *disc friction*, *mixing loss* and of the model
folders for *disc friction*, *recirculation loss*, *clearance loss*, *Wasserbauer*, *Moustapha*, *Meroni* finds no radial-machine loss model (the hits are the axial `CSL-0327`, the centrifugal exercises `CSL-0023`, `CSL-0069`, the fan `CSL-0071`, `CSL-0318` and solar-geometry models for the word *incidence*).

## Problem statement

Function library. The losses of the original are those of a mean-line analysis: each is a specific enthalpy (J/kg) deduced from
radii, widths, angles, velocities, densities and viscosities at the stations of the rotor (and nozzle or vaned stator). The
wrappers `RadComp_rotor_loss`, `RadComp_stator_loss` and `RadTur_rotor_loss` return the sum and every term; `Dh_tot` is -1 when any term is -1.

## Model

All lengths in m, angles in degrees (the original works in radians), velocities in m/s, `rho` in kg/m³, `mu` in Pa·s, losses in J/kg.
The correlations are those of the code; the numeric constants are not repeated here. The reference direction of the angles is not stated in the
original; the demonstration takes the compressor inlet angles from the axial direction (`beta1 = arctan(u1/v1m)`) and the outlet and turbine
angles from the radial direction (`alpha2 = arctan(vu2/vm2)`), which only fixes the demonstration inputs.

| Function | Original (module `radial_compressor_losses.py` unless noted) | Source named in the original |
|---|---|---|
| `RadComp_Dh_inc_rotor` | `rotor_incidence_losses`: `0.5 (w1 sin(abs(beta1) - abs(beta1_opt)))^2`, `beta1_opt = arctan(A1/A1_th tan xhi1)` | Galvas, NASA technical report, 1973 |
| `RadComp_Dh_f_rotor` | `rotor_friction_losses`: `2 C_fi (L_b/D_hb) w_bar^2`, `w_bar = (2 w2 + w1s + w1h)/4`, blade length `L_b` and hydraulic diameter `D_hb` from the radii | Aungier 1995; Galvas 1973; Jansen 1967 |
| `RadComp_Dh_bl_rotor` | `rotor_blade_loading_losses`: `0.05 D_f^2 u2^2`, diffusion factor `D_f` with the fixed factor 0.75 | Coppage and Dallenbach 1956 |
| `RadComp_Dh_cl_rotor` | `rotor_clearance_losses`: `0.6 (eps/b2) abs(vu2) sqrt(...)` | Jansen 1967 |
| `RadComp_Dh_ml_rotor` | `rotor_mixing_losses`: `0.5 v2^2/(1 + tan^2 alpha2) ((1 - eps_w - b*)/(1 - eps_w))^2`, `b* = 1`, `eps_w` from 0.15 | Jansen 1967; Japikse 1996 |
| `RadComp_Dh_df_rotor` | `rotor_disc_friction_losses`: `0.25 rho_mean u2^3 r2^2 Kf/mdot`, `Kf` laminar-type (`Re2 < 3E5`) or turbulent-type | Jansen 1967 |
| `RadComp_Dh_rc_rotor` | `rotor_recirculation_losses`: `8E-5 sinh(3.5 abs(alpha2)^3) D_f^2 u2^2` (Coppage form left as a comment, not translated) | Oh, Yoon and Chung 1997 |
| `RadComp_Dh_inc_stator` | `stator_incidence_losses`: `0.6 w4^2/2 sin^2(beta4_opt - beta4)` | Conrad, Raif et al. 1980 (authors as printed in the source) |
| `RadComp_Dh_f_stator` | `stator_friction_losses`: `2 C_f vm^2 L_b/D_h` with an **added `D_h`** (defect 2) | same |
| `RadComp_rotor_loss`, `RadComp_stator_loss` | `radial_compressor_rotor_losses`, `radial_compressor_stator_losses` (sums) | Meroni, Zühlsdorf, Elmegaard, Haglind, *Design of centrifugal compressors for heat pump systems*, Applied Energy (2018) |
| `RadTur_Dh_nozzle` | `radial_turbine_losses.py` `nozzle_losses`: `(v3^2/2)(0.05/Re_3^0.2)(3 tan alpha3/(S3/c) + S3 cos alpha3/b3)` | Rodgers 1967 |
| `RadTur_Dh_inc_rotor` | `rotor_incidence_losses`: `(w4^2/2) sin^2(beta4 - beta4_opt)`, `beta4_opt = arctan(tan alpha4/(1 - n/1.98))` | Wasserbauer and Glassman 1975 |
| `RadTur_Dh_passage` | `rotor_passage_losses`: friction + secondary flow with `K_p = 0.11` and factor `mf` = 1 or 2, **`r4**b4` read as `r4*b4`** (defect 1) | Moustapha et al. 2003 |
| `RadTur_Dh_clearance` | `rotor_clearance_losses`: `K_a = 0.4`, `K_r = 0.75`, `K_ar = -0.3` | Moustapha et al. 2003 |
| `RadTur_Dh_TE` | `rotor_trailing_edge_losses` | Meroni 2018 |
| `RadTur_rotor_loss` | `rotor_losses` (sum of the four) | Aqel thesis 2023 |

Arguments that the original accepts but never uses are not inputs of the functions: `w1`, `w1_th`, `beta1` in the friction loss, `C_df` and `w1`
in the blade-loading and recirculation losses, `mu1`, `k_roughness`, `w1_th`, `C_df` of the compressor wrapper (the wrapper computes a friction factor from them,
`C_f_computed`, and never uses it), `r4` of the stator wrapper.

### Guards (what differs from the original)

The original returns any number, NaN, or raises a division error. Every function here returns **-1** when an input is out of range (non-positive lengths,
velocities or densities, `abs(angle) >= 90`, `r2 <= r1s`, `r1h >= r1s`, `r5s <= r5h`, `gamma5 <= 1`), when the original would return NaN or raise an error, or when the result is negative.
Library choices (not in the original): the range checks, the negativity test, `n_blade_R > 1.98` in `RadTur_Dh_inc_rotor` (see defect 4), and a
**-1 in place of the silent 0** that `rotor_clearance_losses` of the turbine returns when its square root is NaN. No upper bound is set: a loss in J/kg has no natural one.

## Source defects found (documented, not shipped as results)

All checked by running the original (Python 3.12.3, CoolProp 8.0.0, commit `f03f7f47`).

1. **Hydraulic diameter of the turbine rotor inlet.** `rotor_passage_losses` has `Dh4 = 4*np.pi*r4**b4/(2*np.pi*r4 + n_blade_R*b4)`: a length raised to the power of a length. In the demonstration (`r4` = 0.06 m, `b4` = 7 mm,
   12 blades) `r4**b4` = 0.980 and `Dh4` = 26.7 m against 0.01145 m with `r4*b4`. The product reads as `4A/P` with `A = 2 pi r4 b4` and `P = 2(2 pi r4 + n b4)`, and gives the same order of magnitude as the exit hydraulic diameter `Dh5` = 0.0228 m of the next line (my reading;
   the Aqel thesis and Moustapha et al. were **not checked**). This model uses `r4*b4`. Effect on the demonstration: passage loss 3445.8 J/kg (this model, and the original with the one-character fix) against **887.7 J/kg** from the unmodified original; rotor total 4889.5 against 2331.4 J/kg.
2. **Stator friction is not a ratio.** `stator_friction_losses` has `L_b_over_D_h = (r5 - r3)/cos((xhi3 + xhi5)/2)`, a length in metres: the hydraulic diameter `D_h` is missing, so the loss (`2 C_f vm^2 L_b/D_h` as the name and the cited form suggest) depends on the unit of length. `RadComp_Dh_f_stator`
   takes `D_h` as an **added input**; `D_h` = 1 m returns the original value exactly (demonstration: 2.927 J/kg with `D_h` = 1 m, 585.4 J/kg with an illustrative `D_h` = 5 mm: a factor 200). Which `D_h` the authors intend was not checked (the compressor friction function of the same file computes one for the rotor).
3. **Silent NaN, zero and exceptions.** `rotor_clearance_losses` (compressor) returns NaN for `r2 < r1s` (a negative number under the square root); the turbine `rotor_clearance_losses` returns **0** for the same condition (a
   deliberate `if np.isnan: return 0`), so a non-physical geometry gives zero clearance loss; `rotor_trailing_edge_losses` with `gamma5 = 1` and `rotor_recirculation_losses` with `u2 = 0` raise `ZeroDivisionError`; `rotor_mixing_losses` accepts `alpha2` = 95° (43.8 J/kg for the demonstration `v2`) and `rotor_incidence_losses` of the turbine accepts `n_blade_R = 1.5` (696.4 J/kg). All six are the `g1`...`g6` guard calls of the demonstration, which return -1.
4. **Not a defect, checked:** `beta4_opt = arctan(tan(alpha4)/(1 - n/1.98))` looks like an inverted ratio (it is negative for any `n > 1.98`), but with the relative inlet angle negative for a turbine it follows from a tangential velocity `vu4/u4 = 1 - 1.98/n`
   (my derivation: `tan(beta4_opt) = (vu4 - u4)/vm4 = tan(alpha4)/(1 - n/1.98)`; Wasserbauer and Glassman **not checked**). In the demonstration `beta4_opt` = -48.45° and `beta4` = -54.98°. It is kept; only `n <= 1.98` is excluded.
5. **Dead and unreferenced code.** The compressor wrapper computes `L_b`, `D_hb`, a Reynolds number and a friction factor `C_f_computed` that no loss uses (the friction loss takes `C_fi`); the blade-loading and the recirculation losses take the factor 0.75 as a constant and ignore `C_df`;
   `windage_losses` of the turbine module (Daily and Nece 1960) is an empty function (returns `None`): nothing to translate. The coefficient quoted with a question mark in the docstrings (`C_fi` = 0.004 ?) is kept as the demonstration value, unchecked.
6. **References not checked.** None of the cited papers, reports, books and the thesis was consulted; the correlations are reproduced from the code, and the constants (0.05, 0.6, 0.15, 8E-5, 3.7, 0.102, 0.11, 0.4, 0.75, -0.3, 1.98 ...) could not be confirmed against them. The source states that the models are unvalidated (no reference results in the repository).

## How to run

```bash
coolsolve ./radial_machine_loss_models.eescode
```

16 iterations. The two property-coupled loops of the demonstration (`h2_c`, `rho2_c`, `vm2_c` and `h5_t`, `rho5_t`, `vm5_t`) need the guesses of `radial_machine_loss_models.initials`.
To use the functions in another model, copy the definitions (until `$INCLUDE library:` is supported) and call
`CALL RadComp_rotor_loss(A1, A1_th, alpha2, beta1, beta1h, beta1s, beta2, b2, C_fi, Dh0, eps_a, eps_b, eps_r, L_z, mdot, mu2, n_bl_r, rho1, rho2, r1h, r1s, r2, u2, vu2, v1m, v2, w1, w1h, w1s, w2, xhi1, xhi2 : Dh_tot, Dh_inc, Dh_f, Dh_bl, Dh_cl, Dh_ml, Dh_df, Dh_rc)`
(and `RadComp_stator_loss`, `RadTur_rotor_loss` with `RadTur_Dh_nozzle`); test `Dh_tot < 0` before using a result.

## Results

The demonstration inputs are chosen for this library (**not** a published design): compressor R134a, 45 000 rpm, 1.2 kg/s, inlet 3 bar and 15 °C, outlet 5.2 bar, `r2` = 45 mm, `b2` = 2.5 mm, 14 blades, `vu2 = 0.8 u2`; turbine R245fa, 40 000 rpm, 3 kg/s, inlet 7 bar and 115 °C, outlet 2.5 bar, `r4` = 60 mm, `b4` = 7 mm,
12 blades, `vu4 = 0.8 u4`. Velocity triangles from simple relations (mass conservation, `vu2 = 0.8 u2`, no inlet swirl in the compressor, no exit swirl in the turbine) that are an assumption of the demonstration, not of the original; the vane inlet and the nozzle exit use the density of the preceding station (approximation).

| Compressor rotor, J/kg | inc | f | bl | cl | ml | df | rc | **total** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| this model | 465.7 | 774.9 | 405.5 | 1311.4 | 980.2 | 213.5 | 62.7 | **4214.0** |

The rotor total is 11.7 % of the Euler work `Dh0 = u2 vu2` = 35 975 J/kg (plain ratio `4214.0/35974.7`, not an efficiency of the original). Vaned stator (`D_h` = 5 mm, `r3` = 47.5 mm, `r5` = 75 mm): friction 585.4, incidence 314.5, total 899.96 J/kg.

| Turbine, J/kg | nozzle | rotor inc | passage | clearance | trailing edge | **rotor total** |
|---|---:|---:|---:|---:|---:|---:|
| this model | 1435.8 | 24.4 | 3445.8 | 1019.0 | 400.3 | **4889.5** |

Nozzle plus rotor are 12.5 % of the Euler work `u4 vu4` = 50 532 J/kg. The flagged guard calls `g1`...`g6` are all -1.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): stacked bar of the losses of the demonstration rotors, saved as figures/radial_machine_loss_models_<type>.png -->

## Verification

LaboThapPy commit `f03f7f47` was cloned into `work/` and installed with `pip install --no-deps` in a throw-away virtual environment (Python 3.12.3, `numpy` 2.5.4, `CoolProp` 8.0.0); its two modules were imported as they are
(`verify_demo.py`, `sweep.py` in `work/rl/`, deleted with the work folder).

* **Demonstration:** the inputs (geometry, velocities, densities, viscosities) were read from the `.sol` and passed to the unmodified `radial_compressor_rotor_losses`, `radial_compressor_stator_losses`, `nozzle_losses` and to `rotor_losses` of a copy of the turbine module in which only
  `r4**b4` is `r4*b4` (defect 1): **18 values** (8 compressor rotor, 4 stator, 5 turbine rotor, 1 nozzle), **max relative deviation 5.3·10⁻¹²**. The stator friction is compared as `original/D_h` (and as the original for `D_h` = 1 m).
* **Random sweep:** a CoolSolve file with the library functions and 40 random argument sets for each of `RadComp_rotor_loss` (8 outputs), `RadComp_stator_loss` (3), `RadTur_rotor_loss` (5) and `RadTur_Dh_nozzle` (1) in plausible ranges
  (680 values) against the same Python calls: **max relative deviation 8.6·10⁻¹⁰ for values above 0.01 J/kg** (largest absolute deviation 6.3·10⁻⁸ J/kg on a value of 17 881 J/kg); two values of 2.3·10⁻³ and 7.5·10⁻⁴ J/kg differ by 1.5·10⁻⁸ and 2.2·10⁻⁹ relative (3.4·10⁻¹¹ and 1.7·10⁻¹² J/kg absolute). No random set triggered a guard.
* **Guards:** the six `g` calls were run on the original: NaN (`g1`), `ZeroDivisionError` (`g2`, `g6`), 43.8 J/kg (`g3`), 696.4 J/kg (`g4`), 0 (`g5`); this model returns -1 for each.
* **Properties:** the CoolProp of CoolSolve (8.1.0dev) and CoolProp 8.0.0 agree to 10⁻¹² on the R134a and R245fa densities, enthalpy, `cp/cv` and speed of sound used, but not on the R245fa viscosity (1.3598·10⁻⁵ against 1.5562·10⁻⁵ Pa·s at 7 bar and 115 °C, +14.4 %);
  only `Re_3` of the nozzle depends on it (loss +2.7 % with the 8.0.0 value, `1.144^0.2`). The comparison above uses the CoolSolve inputs, so it is not affected.

**Not compared with any publication or measurement:** the source has no example or reference results, and no cited reference was consulted. The check shows that the translation reproduces the code (with the two documented changes), not that the code reproduces the literature.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language, equation-oriented) of the radial-machine loss correlations of LaboThapPy, files
`labothappy/correlations/turbomachinery/radial_compressor_losses.py` and `labothappy/correlations/turbomachinery/radial_turbine_losses.py`, commit `f03f7f47`.
LaboThapPy - https://github.com/PyLaboThap/LaboThapPy - Copyright (C) 2025 Universite catholique de Louvain (UCLouvain), Universite de Liege (ULiege), Universite de Mons (UMONS), Apache License 2.0.
Original author of the two files (repository history): Basile Chaudoir (ULiège); other authors of the library are listed in its `AUTHORS.txt`.
Changes: translated from Python to the CoolSolve language; angles in degrees; guards returning -1; unused arguments dropped; `r4**b4` read as `r4*b4` (defect 1); added `D_h` argument of the stator friction (defect 2);
silent 0 of the turbine clearance loss returned as -1; demonstration with new illustrative inputs (the source has none), `PropsSI` calls replaced by property functions (`R134a`, `R245fa`).
Scientific basis, **as cited by the original and not checked**: R. H. Aungier, *Mean streamline aerodynamic performance analysis of centrifugal compressors*, J. Turbomach. 117(3), 360 (1995); M. Galvas, *Fortran program for predicting off-design performance of centrifugal compressors*, NASA technical report (1973);
W. Jansen, *A method for calculating the flow in a centrifugal impeller when entropy gradients are present*, Royal Society conference on internal aerodynamics (turbomachinery), Cambridge, 1967;
J. Coppage and F. Dallenbach, *Study of supersonic radial compressors for refrigeration and pressurization systems*, Garrett Corp. report (1956); H. W. Oh, E. S. Yoon, M. K. Chung, *An optimum set of loss models for performance prediction of centrifugal compressors*, Proc. IMechE Part A 211(4), 331-338 (1997);
D. Japikse, *Centrifugal compressor design and performance*, Concepts ETI (1996); Conrad O., Raif K., Of M. W. (authors as printed in the source), *The calculation of performance maps for centrifugal compressors with vane-island diffusers*, ASME gas turbine conference 1980;
A. Meroni, B. Zühlsdorf, B. Elmegaard, F. Haglind, *Design of centrifugal compressors for heat pump systems*, Applied Energy (2018); Rodgers (1967) (nozzle loss), Wasserbauer and Glassman (1975) (turbine incidence), Moustapha et al. (2003) (passage and clearance), the Aqel thesis (2023) and Daily and Nece (1960) (windage, empty in the code), as named in the source, without bibliographic details.

## Conversion log

- **2026-10-31 - translation (T-FUNC, card C-449)**: 14 functions + 3 procedures + demonstration program; angles radians -> degrees; `PropsSI` calls replaced by property functions with `(T,P)` or `(P,h)` (no `(T,H)` call was needed);
  `np.sinh` -> `SINH`, `np.arctan` -> `ARCTAN`, `**` -> `^`; the `if/elif` of the original -> `IF/THEN/ELSE`; integer powers of signed quantities are written as products (`x*x`, as in `CSL-0327`, because of `CS-BUG-PROC-NEG-POW`; not tested here).
- Variable names that differ only in case are one variable in EES: the demonstration names the blade numbers `nbl_c`, `nbl_t` because `N_c`, `N_t` are the speeds.
- **Level** (taxonomy §3): equations 126 -> 1; largest block 8 -> 1; functions/procedures -> 1; no multi-zone structure, no off-design -> 0 + 0; curated guesses (`.initials`) for the two property loops -> 1; score 4 -> level 3.

## Limitations and CoolSolve gaps

* Only the algebraic losses are translated. Not translated: the mean-line station assembly, the optimisation loops (`LTP-003`, `LTP-067`, `LTP-068`, duplicates of this row), the unused friction factor of the compressor wrapper, the Coppage recirculation form (a comment in the original), and `windage_losses` (an empty function).
* The validity range of the correlations is not stated in the original; the guards only exclude invalid inputs and results, and an angle given in radians instead of degrees is accepted (a value of 1.2 passes as 1.2°).
* No registered CoolSolve gap is needed (`missing_features` empty).

## Related models

- `CSL-0327` *axial_turbine_loss_models*: the same building block for the blade rows of an axial turbine (loss coefficients instead of enthalpy losses).
- `CSL-0318` *cordier_specific_speed*: 0D pre-design (specific speed, diameter) before the geometry used here is fixed.
- `CSL-0069` *centrifugal_compressor_design_similarity*, `CSL-0023` *centrifugal_turbocompressor_performance*: centrifugal compressor exercises (similarity factors, constant isentropic efficiencies); this model gives a loss breakdown, which those models do not have.
