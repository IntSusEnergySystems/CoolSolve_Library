# Engine cylinder count and operating parameters at rated power

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0331`

An H2 engine is sized from its bore, stroke, mean piston speed and rated shaft
power: displacement per cylinder, number of cylinders (the non-integer count
is rounded up to the next integer and the mean effective pressure is corrected
so that the rated power is kept), speed and efficiencies. The engine is then
run in submerged operation at 300 kW: its oxidiser is 30 % O2 plus 70 %
recirculated H2O (mass), the H2 combustion H2 + (0.5 O2 + alpha H2O) =
(1 + alpha) H2O is stoichiometric, and the volumetric efficiency follows from
the inlet mixture molar mass (ideal gas).

| | |
|---|---|
| **Category** | Cycles and machines › Engines |
| **Fluids** | H2, O2, H2O (ideal-gas species, molar masses and formation enthalpies) |
| **Size** | 43 equations (largest block: 1) — variant: 46 equations |
| **Source** | ULiège *Machines et combustion industrielle* (MCI), TP2 exercise 3 (EES file `Exercice_3_Param opératoires et combustion.EES`) |
| **Authors** | Ph. Ngendakumana; Rémi Dickes |
| **License** | MIT |
| **CoolSolve** | 0.4.0@2dc1367 — native file blocked by `CS-GAP-HEATING-VALUE`; runnable variant verified |

## Problem statement

Exercise 3 of the ULiège MCI TP2 (translated, paraphrased). (a) A four-stroke
engine must deliver a shaft power of 400 kW at rated speed. Given the bore
(110 mm), the stroke (150 mm), the mean piston speed (17.5 m/s) and the
intermittency factor of the four-stroke cycle (i = 0.5), compute the
displacement per cylinder and the number of cylinders. The count is not an
integer: round it up and correct the mean effective pressure, keeping the
rated shaft power. (b) In submerged operation the engine delivers 300 kW; the
speed follows a cube law W_dot_sh ∝ N³ and the throttling is recomputed. The
fuel is H2; the oxidiser carries 30 % O2 and 70 % recirculated gas (H2O) in
mass, the combustion is stoichiometric (phi = 1) and the thermal efficiency is
0.32 with LHV = 120 000 kJ/kg. At the inlet (180 kPa, 388 K) compute the
mixture molar mass, the density and the volumetric efficiency (about 0.8, OK
for a non-supercharged engine, as in the original).

## Model

- Displacement `V_s = pi*D^2/4*L`; speed from the mean piston speed
  `C_m_n = 2*L*(N_1/60)`; throttled volume flow
  `V_dot_th = i*V_s*(N_1/60)*n_c`; `n_c` from the rated power and the mean
  effective pressure `DELTAp_bar_e_n`; `N_cyl = CEIL(n_c)` and
  `DELTAp_bar_e_new` re-closes `W_dot_sh_n = -DELTAp_bar_e_new*V_dot_th_new`.
- Part load (index 2): `W_dot_sh_n/W_dot_sh_2 = (N_1/N_2)^3`, same
  `DELTAp_bar_e*V_dot_th` closure.
- Stoichiometry of `H2 + (0.5 O2 + alpha H2O) = (1 + alpha) H2O`: `alpha`
  from the O2 mass fraction of the oxidiser (0.3), stoichiometric fuel fraction
  `f_st` and equivalence ratio `phi`; fuel and oxidiser flows from
  `eta = -W_dot_sh/(M_dot_f*LHV_f)` and `f = M_dot_f/M_dot_oxydant`.
- Volumetric efficiency `epsilon_v = M_dot_oxydant/(rho_inlet*V_dot_th_2)`
  with `rho_inlet` from the ideal-gas law on the mole-fraction mixture molar
  mass `MM_inlet`.
- `LHV_f_EES = LowerHeatingValue(H2)` checks the LHV given in the statement;
  EES stored 119 946 kJ/kg.

## How to run

The native file `engine_cylinder_count.eescode` is **blocked**: CoolSolve does
not implement the EES built-in `LowerHeatingValue` (`CS-GAP-HEATING-VALUE`).
It is kept in valid EES and is not rewritten.

`engine_cylinder_count_coolsolve.eescode` is the runnable variant (tested as
`CSL-0331:coolsolve`); only the `LowerHeatingValue(H2)` call is replaced (see
the conversion log). Guess values in the `.initials` files (speeds, alpha,
V_dot_th…).

## Results

Values of the default operating point (variant CoolSolve / EES stored):

| Variable | CoolSolve (variant) | EES |
|---|---:|---:|
| V_s [m³] | 0.001425497667 | 0.001425497667 |
| n_c [-] | 7.400539 | 7.400539 |
| N_cyl [-] | 8 | 8 |
| N_1 [rev/min] | 3500 | 3500 |
| N_2 [rev/min] | 3179.96 | 3179.96 |
| DELTAp_bar_e_new [Pa] | 1 202 588 | 1 202 588 |
| DELTAp_bar_e_2 [Pa] | 992 714 | 992 714 |
| alpha [-] | 2.0722 | 2.0722 |
| M_dot_f [kg/s] | 0.0078125 | 0.0078125 |
| M_dot_oxydant [kg/s] | 0.206684 | 0.206673 |
| epsilon_v [-] | 0.79109 | 0.79102 |
| LHV_f_EES [J/kg] | 1.1996051e8 | 1.19946e8 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![Volumetric efficiency vs speed](figures/engine_cylinder_count_sweep.png)  + one-line caption -->

## Verification

`tools/compare_solution.py engine_cylinder_count_coolsolve.sol reference/ees_variables.csv
--ees-units` (the **variant** was verified; the native file does not solve):
"43 common variables, 1 differ (rtol=0.001); only in EES: 0; only in
CoolSolve: 4". The printed maximum 9.99e-01 is the single flagged row, `r`:
EES stores 0.53659 kJ/(kg-K) in a variable whose units cell is blank, so the
comparator cannot convert it; CoolSolve's 536.605 J/(kg-K) is the same value.
Excluding that row the maximum is 1.21e-04, on `LHV_f_EES`: the LHV built from
the CoolSolve formation enthalpies (119 960.5 kJ/kg) against the EES
`LowerHeatingValue(H2)` stored value (119 946 kJ/kg), 0.012 %. The 3 extra
CoolSolve-only variables are the species enthalpies `h_H2`, `h_O2`, `h_H2O_v`
of the variant. The speed laws, the cylinder count and the mass flows are
exact.

## Source and attribution

Source file (not copied into the library):
`~/Nextcloud/thermo_models/MCI_REMIDICKES/MCI/TP/MCI_TP2_Ex_1-3/Exercice_3_Param opératoires et combustion.EES`
(EES 10.589, RTF, SI-kPa-K-kJ, 43/44 stored values; EES ID stamp: P.
Ngendakumana licence, ULiège Thermotechnics). Authors from the inventory:
Ph. Ngendakumana; Rémi Dickes. Published under the library licence (MIT).

## Conversion log

- **2026-11-02 — import** (`tools/ees_extract.py`, then manual curation):
  unit system `SI MASS DEG KPA K KJ` converted by hand to SI-°C-Pa-J:
  `W_dot_sh_n = -400 kW → -4e5 W`, `W_dot_sh_2 = -300 kW → -3e5 W`,
  `DELTAp_bar_e_n = 1300 kPa → 1.3e6 Pa`, `p_inlet = 180 kPa → 1.8e5 Pa`,
  `LHV_f = 120000 kJ/kg → 1.2e8 J/kg`, `R_u = 8.314 kJ/(kmol-K) → 8314
  J/(kmol-K)`, `T_inlet = 388 K → 114.85 °C` and the ideal-gas law
  `p_inlet = rho_inlet*r*T_inlet` rewritten with the absolute temperature
  `(T_inlet + 273.15)`. French comments translated to English; EES tags
  (`{$ID$}`, `{$PX$}`, `{$ST$OFF}`) removed; the dead variable `N` (no
  equation, no stored value) is not carried over. No lookup or parametric
  table.
- **2026-11-02 — variant** `engine_cylinder_count_coolsolve.eescode`: the only
  change is `LHV_f_EES = LowerHeatingValue(H2)` replaced by the same LHV
  computed from the CoolSolve species enthalpies of formation,
  `LHV_f_EES = (h_H2*MM(H2) + 0.5*h_O2*MM(O2) - h_H2O_v*MM(H2O))/MM(H2)` at
  25 °C (water vapour, so the lower heating value). No CoolSolve-only syntax:
  valid EES in both files.
- **Level**: equations 43 → 0; largest block 1 → 0; functions/arrays 0;
  multi-component 0; semi-empirical 0; curated guesses 0 → score 0 → level 1,
  moved to level 2: one teaching exercise combining a sizing part and a
  combustion-stoichiometry part (inventory `level_guess` 2).

## Limitations and CoolSolve gaps

- Native file blocked by `CS-GAP-HEATING-VALUE`: the EES built-in property
  function `LowerHeatingValue(Fuel$)` is not implemented in CoolSolve
  (register row with reproducer and the EES stored value 119 946 kJ/kg for
  H2). The variant replaces only that call.

## Niche

Nearest library models: `CSL-0279` *engine_bsfc_bore_stroke_afr* (bore/stroke
and volumetric-efficiency sizing of a multi-cylinder engine, but the cylinder
count is an input and there is no combustion flow), `CSL-0185`
*diesel_injection_sizing* (displacement per cylinder, volumetric efficiency;
`n_c` an input) and `CSL-0244` *engine_dynamometer_test* (brake mean effective
pressure). This model is the only one that *solves for* the cylinder count
(non-integer count, CEIL rounding, mean-effective-pressure correction keeping
the rated power) and the only one with a combustion stoichiometry on an
O2 + recirculated-H2O oxidiser (submerged operation) with the volumetric
efficiency computed from the mixture molar mass.

## Related models

- CSL-0279 (*engine_bsfc_bore_stroke_afr*): nearest sizing exercise; here the
  cylinder count is an unknown instead of an input.
- CSL-0185 (*diesel_injection_sizing*): displacement per cylinder and
  volumetric efficiency, fixed cylinder count.
