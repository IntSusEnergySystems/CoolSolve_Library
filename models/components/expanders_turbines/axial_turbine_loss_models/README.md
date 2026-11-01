# Axial-turbine loss models: Aungier, Balje-Binsley, Kacker-Okapuu

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0327`

Translation of the axial-turbine **loss coefficients** of LaboThapPy: the complete Aungier loss system of a blade row
(profile, secondary-flow, tip-clearance, trailing-edge, supersonic-expansion, shock and lashing-wire losses, one
`FUNCTION` each plus the `PROCEDURE` `Aungier_axial_loss` that assembles them), and the two correlations of the
sCO2 design method of Lee et al. (2012) kept in `pressure_loss_model.py`: the **Balje-Binsley** profile loss and the
**Kacker-Okapuu** secondary loss. The demonstration program re-runs the ORC example of the original (stator and
rotor, R245fa) and the sCO2 "Test" example (R744), and shows what the guards do.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | R245fa, R744 (the demonstration program only; the functions take numbers) |
| **Size** | 221 equations in the demonstration program (largest block 8) + 12 `FUNCTION` + 1 `PROCEDURE` |
| **Source** | [LaboThapPy](https://github.com/PyLaboThap/LaboThapPy) commit `f03f7f47`, files `labothappy/correlations/turbomachinery/aungier_axial_turbine.py` and `labothappy/correlations/turbomachinery/pressure_loss_model.py`; inventory row `LTP-051` (kept `todo` by C-373; rows `LTP-007`, `LTP-066` are duplicates of it) |
| **Authors** | Basile Chaudoir (the only author of the two files in the repository history) |
| **License** | Original: Apache-2.0 (`LICENSE.txt` of LaboThapPy); translation published under the library MIT licence |
| **CoolSolve** | 0.4.0 - **verified** against a re-run of the Python code (52 values compared, max relative deviation 4.1·10⁻¹³; flags checked separately) |

## Niche

No library model computes **blade-row loss coefficients** of an axial turbine from the blade geometry. The nearest
models are `CSL-0135` *turbine_stodola_offdesign* (Stodola cone law: pressure ratio versus flow and an efficiency
characteristic of the whole turbine, no geometry), `CSL-0318` *cordier_specific_speed* (0D pre-design: specific speed
and Cordier diameter from the duty, no blade rows) and the isentropic-efficiency turbines (`CSL-0174`, `CSL-0314`).
This model is the **next step down in detail**: given velocity triangles and blade geometry (chord, pitch, height,
thickness, tip clearance, Mach numbers), it gives the total-pressure loss `Y` of a stator or rotor and its seven
contributions, i.e. the building block of a mean-line turbine design. A search of `library.json` and of the model
folders for *Aungier*, *Kacker*, *Balje*, *Ainley* and *profile loss* finds no turbine model (the only hit is the
Balje name in the Cordier README). The radial-turbine loss models are another row (`LTP-052`).

## Problem statement

Function library. For a blade row the original returns `Y = (P01' - P02')/(P02' - P2)` (comment of the original) and
its components. The wrapper `Aungier_axial_loss` takes the same arguments as `aungier_loss_model` (angles in
degrees, no `rad_flag`) and returns the eight values; every loss function can also be called alone.

## Model

All lengths in m, angles in degrees, `mu2` in Pa·s, `rho2` in kg/m³, `w2` and `vm2` in m/s. Rotating-frame Mach numbers
`M1`, `M2`. The correlations are those of the code; the numeric constants are not repeated here.

| Block | Content (as in the original) |
|---|---|
| `Aungier_Kp(M1p, M2p)` | compressibility correction `Kp` of the profile and secondary losses |
| `Aungier_Kre(Re_c, c, e_r)` | Reynolds correction: laminar `sqrt(1e5/Re_c)`, transition 1, turbulent `(log10(5e5)/log10(Re))^2.58` with `Re_r = 100 c/e_r` (roughness-limited when `Re_c > Re_r`) |
| `Aungier_Km(M2p, s, R_c)` | Mach correction of the profile loss, 1 for `M2p <= 0.6` and `> 1` |
| `Aungier_Yp(...)` | profile loss: `Kmod·Kinc·Km·Kp·Kre·(fact_1·fact_2 - DY_TE)` with `Kmod = 0.67`, incidence factor `Kinc` from `i/i_s`, `Yp1` (nozzle) and `Yp2` (impulse) blends through `xi = (90 - beta1')/(90 - alpha2')`, thickness factor `tau^xi`, trailing-edge term of `t = 0.02 s` subtracted |
| `Aungier_Ys(...)` | secondary loss: lift coefficient, Ainley loading `Z`, aspect-ratio factor, `Ys = Ks·Kre·sqrt(Ys*²/(1 + 7.5 Ys*²))` |
| `Aungier_Ycl(...)` | tip clearance `0.47·Z·(c/h)·(delta/c)^0.78` |
| `Aungier_Yte(beta_g, s, t_TE)` | trailing edge `(s sin(beta_g)/(s sin(beta_g) - t_TE) - 1)²` |
| `Aungier_Yex(M2p)`, `Aungier_Ysh(M1p, M2p)` | supersonic expansion `((M2p - 1)/M2p)²`, shock loss |
| `Aungier_Ylw(...)` | lashing wires `N_lw·C_D·D_lw·vm2²/(h·w2²)` |
| `Aungier_axial_loss(alpha1, alpha2, beta_g, chi1, ... : Y_tot, Yp, Ys, Ycl, Yte, Yex, Ysh, Ylw)` | converts the angles from the axial to the tangent direction (`90 - angle`), calls the above, sums |
| `BaljeBinsley_Yp(Re, t_TE, chord, t_blade, chi1, chi2)` | `balje_binsley` of `pressure_loss_model.py` |
| `KackerOkapuu_Ys(AR, solidity, alpha1, alpha2, beta1)` | `kacker_okaapu` of `pressure_loss_model.py` |

The original takes the angles of `aungier_loss_model` from the axial direction and converts them with `90 - angle`
inside; `profile_losses` and `secondary_losses` work with angles from the tangent. The same split is kept
(`Aungier_Yp`, `Aungier_Ys`, `Aungier_Ycl` take tangent angles).

### Guards (what differs from the original)

The original returns any number, however non-physical, or raises an error. Every function here returns **-1** when

* an input is out of range (`0 < alpha2' < 90`, positive lengths, `mu2`, `rho2`, `w2`, `h`, `tan` or `sin` of an angle zero, throat blocked: `s·sin(beta_g) <= 0.02·s` in `Yp`, `<= t_TE` in `Yte`; `|xi| > 1.3` where the original raises `ValueError`);
* `0.6 < M2' <= 1` in `Aungier_Yp` (source defect 2 below);
* the result is outside `0 ... 1` (the plausibility bound is a library choice, not in the original) or, for `BaljeBinsley_Yp`, the original's `abs()` would hide a negative loss;
* a component of `Aungier_axial_loss` is -1: `Y_tot` is then -1.

`KackerOkapuu_Ys` keeps the `abs()` of the original (the sign of `alpha1 - alpha2` depends on the angle convention).

## Source defects found (documented, not shipped as results)

All checked by running the original (Python 3.12, CoolProp 8.0.0, commit `f03f7f47`).

1. **Unit of `beta_g`.** In `aungier_loss_model`, `beta_g` goes to `profile_losses`, which uses `sind(beta_g)` (degrees), and to the
   trailing-edge loss, which uses `np.sin(beta_g)` (radians) for the same variable. The only caller in the repository
   (`component/expander/turbine_mean_line_Aungier.py`) passes `beta_g` in degrees (`stage.beta_g_S*180/np.pi`), so its trailing-edge
   loss is the sine of a number of degrees read as radians. The translation uses degrees everywhere. Effect on the ORC example (reference values below are
   those printed by the original; their origin is not stated): `Yte` stator 0.007588 (original) / 0.007685 (degrees), rotor 0.003944 / 0.004817
   (printed reference 0.008 / 0.004). The reference values (one significant digit for `Yte`) do not decide between the two; the original agrees
   better with the rotor value, so the choice of degrees rests on the code, not on the example.
2. **Mach correction `Km`** `1 + (1.65(M2'-0.6) + 240(M2'-0.06)²)(s/R_c)^(3M2'-0.6)`: `(M2'-0.06)` looks like a typo for `(M2'-0.6)`,
   but this was **not checked against Aungier's book**, and the variant with `(M2'-0.6)` also gives large values (`Km` = 15.3 at `M2'` = 0.8 for the
   ORC stator geometry, computed once with the other constant: not shipped). The expression of the original gives `Km` = 191.4 at `M2'` = 0.8 and 111.2 at 0.65 and a profile loss of 2.51
   (Python, unmodified) at 0.8. `Aungier_Yp` therefore returns -1 for `0.6 < M2' <= 1`; `Aungier_Km` keeps the expression for the record. The ORC and "Test" examples never enter this range
   (their rotating Mach numbers are above 1 or below 0.6).
3. **Two definitions of the mean flow angle `alpha_m`.** `secondary_losses` uses `alpha_m = arctan((cot a1 + cot a2)/2)`, the tip-clearance block of
   `aungier_loss_model` uses `90 - arctan(...)` (the original carries a comment `# 90 -` showing it was toggled). Both are kept. With the ORC example: swapping the
   definition in `secondary_losses` gives `Ys` stator +160 % away from the printed reference (instead of +5.3 %), whereas the rotor changes by 4 points; swapping it in
   the clearance loss moves the rotor `Ycl` from -0.5 % to -4.8 % of the printed reference. The example thus supports the form of `secondary_losses` as written and does not
   settle the clearance form; which one is Aungier's was not checked.
4. **The example cases of `__main__`.** The default case `'Test'` passes radian angles to `cosd`/`sind` (solidity, pitch) and `beta_g` in radians: it returns `Yp` = -224.9 (stator) and
   +96.3 (rotor) with no warning (Python, unmodified). The case `'CO2'` returns `Yp` = -2.87 (not translated). The `'ORC'` case computes `R_c` with `np.sin` of degrees
   (irrelevant there since `M2' > 1`; the result is identical to 15 digits with `R_c` in degrees) and the rotor trailing-edge thickness from the **stator** pitch (`o_r = ss*sind(beta3)`); both kept as in the original in the demonstration.
5. Smaller points: the error message says `1.2` and the threshold is `1.3`; for `e = 0` the original evaluates `log10(-1)` (NaN, unused); `balje_binsley` and `kacker_okaapu` end with `abs()`;
   `kacker_okaapu` is the name of the function (the Kacker-Okapuu spelling is used here); the module `aungier_axial_turbine.py` cites no reference (the code comments mention a book and 2006 for `Kmod = 0.67`).

## How to run

```bash
coolsolve ./axial_turbine_loss_models.eescode
```

14 iterations with the default guesses (no `.initials`). The argument sets of section 6 are the tables
`axial_turbine_loss_models-bb_cases.csv` and `axial_turbine_loss_models-ko_cases.csv` (CoolSolve convention
`<model>-<table>.csv`; the EES user creates the Lookup tables `bb_cases` and `ko_cases` with the same content).

To use the functions in another model, copy the definitions (until `$INCLUDE library:` is supported) and call
`CALL Aungier_axial_loss(alpha1, alpha2, beta_g, chi1, c, delta, D_lw, e_r, h, mu2, M1, M2, N_lw, R_c, rho2, s, t_max, t_TE, vm2, w2 : Y_tot, Yp, Ys, Ycl, Yte, Yex, Ysh, Ylw)`;
test `Y_tot < 0` before using it.

## Results

Section 1, the ORC example of the original (R245fa, 12.6 bar, 100.55 °C, 50 kg/s, 1.52 MW, expansion ratio 6.4; stator `alpha1` = 3°,
`alpha2` = 71°, rotor `beta2` = -24°, `beta3` = 68°). Reference values: those printed in the original (origin not stated); "original" = the Python run unmodified, "degrees" = same with the
unit fix of defect 1 (this model).

| | Yp | Ys | Ycl | Yte | Yex | Ysh | Y_tot |
|---|---:|---:|---:|---:|---:|---:|---:|
| stator, this model | 0.01409 | 0.05791 | 0 | 0.00769 | 0.10223 | 0.01352 | 0.19542 |
| stator, reference of the original | 0.013 | 0.055 | 0 | 0.008 | 0.101 | 0.013 | 0.191 |
| stator, original (unmodified) | 0.01409 | 0.05791 | 0 | 0.00759 | 0.10223 | 0.01352 | 0.19533 |
| rotor, this model | 0.01695 | 0.04748 | 0.13836 | 0.00482 | 0.03497 | 0.01152 | 0.25409 |
| rotor, reference of the original | 0.016 | 0.05 | 0.139 | 0.004 | 0.034 | 0.011 | 0.253 |
| rotor, original (unmodified) | 0.01695 | 0.04748 | 0.13836 | 0.00394 | 0.03497 | 0.01152 | 0.25322 |

Against the printed reference values the components of this model are within +8.4 % / -5.3 % (`Yp` stator +8.4 %, `Yp` rotor +5.9 %, `Ys` stator +5.3 %, `Ys` rotor -5.0 %; the original prints the same
errors), except the rotor `Yte` (+20 %: 0.00482 against 0.004, a one-digit reference; -1.4 % with the unmodified original, defect 1); the totals differ by +2.3 % (stator) and +0.4 % (rotor). The reference values are rounded to one to three digits.

Section 2, the "Test" example (R744, 246.8 bar, 651 °C inlet) with consistent angles and a solidity computed in degrees (the original passes radians to `sind`; see defect 4):
stator `Yp` 0.1031, `Ys` 0.0687, `Yte` 0.00215, `Y_tot` 0.1739; rotor `Yp` 0.1293, `Ys` 0.0931, `Ycl` 0.0481, `Yte` 0.00347, `Y_tot` 0.2740. No reference value exists for this case. The rotor call uses `beta_g = -beta3` (positive) and the pitch from the rotor angles.

Section 3, the same example **with the inputs exactly as the original builds them** (pitch from radian angles, `beta_g` in radians): all of `Yp`, `Y_tot` are -1 (the original: -224.9 and +96.3); the rotor pitch is negative,
so `Ys`, `Ycl`, `Yte` are -1 as well; the stator `Ys` = 0.0687 is unchanged, `Yte` = 0.0303 (the original: 1.1·10⁻⁵ because of defect 1).

Section 4: `Km` of the original at `M2'` = 0.8 and 0.65 (ORC stator geometry): 191.4 and 111.2; `Aungier_Yp` returns -1.
Section 5: two lashing wires of 1 mm on the ORC stator: `Ylw` = 0.01086.

Section 6, argument sets of the table `bb_cases` (`Re`, `t_TE`, chord, `t_blade`, `chi1`, `chi2`) and `ko_cases` (`AR`, solidity, angles):

| | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| `BaljeBinsley_Yp` | 0.2861 | 0.6906 | 0.1089 | 0.2960 | -1 (`t_TE` > `t_blade`; original 0.532) | -1 (negative loss; original 1.839) |
| `KackerOkapuu_Ys` | 0.01122 | 0.06221 | 0.01049 | 0.04301 | 0.12438 | -1 (`AR` < 0; original 0.02244) |

The Balje-Binsley values are large for a trailing edge of 10 % of the thickness (0.29 at `Re` = 10⁶): the meaning of `t_blade` in the original ("blade thickness") and the correlation itself were **not checked
against Lee et al. (2012) or Balje and Binsley**; the model reproduces the code.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric plot of the seven stator or rotor loss
     contributions against the outlet Mach number, saved as figures/axial_turbine_loss_models_<type>.png -->

## Verification

LaboThapPy commit `f03f7f47` was cloned into `work/`, installed with `pip install --no-deps` in a throw-away virtual environment (Python 3.12.3, `numpy`, `CoolProp 8.0.0`) and its two
modules imported as they are. A driver script (`verify.py`, with `compare.py`, in `work/lt/`, deleted with the work folder) computed the inputs of every case independently
(CoolProp `PropsSI`: `(T,P)` for the ORC inlet, `T(H,P)` for the outlets, then density and viscosity at `(P,T)`), called `aungier_loss_model` (unmodified, and a copy in which only
`np.sin(beta_g)` of the trailing-edge loss is `sind(beta_g)`, defect 1), `balje_binsley` and `kacker_okaapu` for the 6 + 6 argument sets, and compared 52 values with the `.sol`:

* ORC stator and rotor, "Test" stator and rotor, lashing wires, `Km` (read from an instrumented copy of `profile_losses`, outputs unchanged): **52 values, max relative deviation 4.1·10⁻¹³** (all values `Yp, Ys, Ycl, Yex, Ysh, Ylw` against the unmodified original; `Yte` and `Y_tot` against the original with the unit fix; the "Test" cases against the fixed copy), `Balje-Binsley` and `Kacker-Okapuu` against the unmodified original.
* Flags: every `-1` has a Python value outside `0 ... 1` (-224.9, 96.3, 1.839, 2.51 for `Yp` at `M2'` = 0.8 ...) or an input the guards reject (negative pitch, negative aspect ratio, `t_TE` > `t_blade`, where the original returns the `abs()` of a meaningless number).
* The values with defect 1 (`Yte`, `Y_tot` of the demonstration cases 1, 2) are not a comparison with the unmodified original: the original gives 0.19533 / 0.25322 for `Y_tot` of the ORC stator / rotor (deviation of this model 5.0·10⁻⁴ and 3.5·10⁻³).
* Viscosity: the CoolProp of CoolSolve (8.1.0dev) gives 1.2388·10⁻⁵ Pa·s for R245fa at 1.969 bar and 81.66 °C, CoolProp 8.0.0 gives 1.4115·10⁻⁵ Pa·s (R744 agrees to 10⁻¹³). In the ORC case the Reynolds number (5.9·10⁶) is above the roughness Reynolds number (2.2·10⁶), so `Kre` does not depend on it: the original gives identical `Y_tot` with either viscosity.

Not compared with any publication: the printed reference values of the original (above) are the only independent numbers and their origin is not given; the Aungier book, Kacker and Okapuu (1982), Balje and Binsley and Lee et al. were not consulted.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language, equation-oriented) of the axial-turbine loss correlations of LaboThapPy, files
`labothappy/correlations/turbomachinery/aungier_axial_turbine.py` and `labothappy/correlations/turbomachinery/pressure_loss_model.py`, commit `f03f7f47`.
LaboThapPy - https://github.com/PyLaboThap/LaboThapPy - Copyright (C) 2025 Universite catholique de Louvain (UCLouvain), Universite de Liege (ULiege), Universite de Mons (UMONS), Apache License 2.0.
Original author of the two files (repository history): Basile Chaudoir (ULiège); other authors of the library are listed in its `AUTHORS.txt`.
Changes: translated from Python to the CoolSolve language; angles in degrees without `rad_flag`; `beta_g` in degrees in both places (defect 1); guards returning -1 and a plausibility bound
of 0 ... 1 on every loss coefficient; `Km` range 0.6-1 disabled (defect 2); NaN/exception paths replaced by -1; `PropsSI` calls replaced by property functions (`R245fa`, `CO2` -> `R744`; the `(T,H)` calls rewritten as `(P,h)`:
`T_out = temperature(fluid, P=p, h=h)`); examples flattened into the main program.
Scientific basis (not stated in the code, presumed from the names and comments, not checked): R. H. Aungier, *Turbine Aerodynamics: Axial-Flow and Radial-Inflow Turbine Design and Analysis*, ASME Press, 2006
(profile, secondary, clearance, trailing-edge, expansion, shock and lashing-wire losses; Kacker-Okapuu-type profile correlations); S. C. Kacker and U. Okapuu, "A mean line prediction method for axial flow turbine efficiency",
J. Eng. Power 104 (1982); `pressure_loss_model.py` cites J. Lee, J. I. Lee, Y. Ahn, H. Yoon, *Design methodology of supercritical CO2 Brayton cycle turbomachineries*, ASME Turbo Expo 2012 (the venue is not given in the code).

## Conversion log

- **2026-10-31 - translation (T-FUNC, card C-448)**: 12 functions + 1 procedure + demonstration program; temperatures K -> °C; `(T,H)` property calls rewritten with `(P,h)` (section 1: `T_out_s_o`, `T_out_r_o`, section 2: `T_out_s_t`, `T_out_r_t`);
  the inlet temperature of the "Test" case (CoolProp `T(H = 1159373 J/kg, P)` = 924.178 K) is a constant here because the enthalpy reference of EES differs from CoolProp's.
- Variable names that differ only in case are one variable in EES: coefficients of the original (`A`, `B`, `C`, `D`; `X`) are `A_1`, `cA`, ... in the functions, because the chord is `c`.
- **Workaround for a CoolSolve behaviour (unverified suggestion, not registered: no EES evidence at hand).** A `CALL` with two or more outputs whose body evaluates `SQRT(0)` or a negative number to the power 3 fails with
  *SingularJacobian* (NaN in the Jacobian), whereas the same code in the main program or in a one-output `CALL` solves. Reproducer: `PROCEDURE PP(a : x, y)` ⏎ `q = a - 0.75` ⏎ `x = q^3` ⏎ `y = 1` ⏎ `END` ⏎ `CALL PP(0.25 : x, y)`
  (the same with `x = SQRT(a)` and `CALL PP(0 : x, y)`). The functions therefore write integer powers of signed quantities as products (`xi*xi*xi`) and `Ysh_est/SQRT(1 + Ysh_est*Ysh_est)` for `SQRT(Ysh_est²/(1 + Ysh_est²))` (same value).
  May be related to the unreduced SingularJacobian row of section 8 of the register (2026-10-10, string output of a `CALL`).
- **Level** (taxonomy §3): equations 221 -> 1; largest block 8 -> 1; functions/procedures and arrays -> 1; no multi-zone structure, off-design or curated guesses -> 0 + 0 + 0; score 3 -> level 2.

## Limitations and CoolSolve gaps

* Only the algebraic loss coefficients are translated. Not translated: the mean-line stage assembly, deviation, map interpolation and PSO design loops (`LTP-007`, `LTP-066`, duplicates of this row), the Bezier blade construction, the `'CO2'` example case (non-physical in the original), and the radial-turbine losses (another inventory row).
* `Km` is unavailable for `0.6 < M2' <= 1` (defect 2); no number can be given there without the reference.
* The validity range of the correlations is not stated in the original; the guards above only exclude invalid or non-physical inputs and results.
* No registered CoolSolve gap is needed (`missing_features` empty); the `CALL` behaviour above is an unverified suggestion.

## Related models

- `CSL-0135` *turbine_stodola_offdesign*: whole-turbine off-design (cone law, efficiency characteristic) with no blade geometry; this model gives the row losses that would feed a mean-line efficiency.
- `CSL-0318` *cordier_specific_speed*: 0D pre-design of the machine (specific speed, diameter) before the blade rows are sized.
- `CSL-0174` *steam_turbine_isentropic_efficiency*, `CSL-0314` *steam_turbine_baumann*: turbine efficiency as a given number or a wetness correction.
- `CSL-0328` *radial_machine_loss_models*: the radial counterpart (centrifugal compressor and radial-inflow turbine losses as specific enthalpy losses).
