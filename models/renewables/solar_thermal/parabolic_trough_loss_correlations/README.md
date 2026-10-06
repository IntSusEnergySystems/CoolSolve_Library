# Parabolic-trough receiver and collector heat-loss correlations (function library)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0083`

Empirical heat-loss and efficiency correlations of parabolic-trough solar
receivers and collectors, translated from the ThermoCycle Modelica library:
the Schott PTR70 receiver heat-loss correlation (NREL/TP-550-45633) with its
vacuum / lost-vacuum / hydrogen coefficient records and the Sopogy Soponova
receiver, the optical and thermal efficiency chain of the same receiver
model, and the Soltigua PTMx collector efficiency fit with its cubic
longitudinal incidence-angle modifier. A demonstration program calls every
function with typical values and checks the results against the published
references (NREL test data, Soltigua datasheet, and the independent Soponova
correlation of Quoilin et al.).

| | |
|---|---|
| **Category** | Renewable energy › Solar thermal |
| **Fluids** | none (the correlations are fluid-independent; the heat-transfer fluid enters only through the receiver temperature) |
| **Size** | 134 equations (largest block: 1), of which 6 function definitions; all explicit |
| **Source** | ThermoCycle Modelica library, `AbsSchottSopo.mo`, `AbsSoltigua.mo` and their geometry records, commit `b4f16c0b` — https://github.com/thermocycle/Thermocycle-library |
| **Authors** | Adriano Desideri and Sylvain Quoilin (ULiège Thermodynamics Laboratory); correlations of F. Burkholder and C. Kutscher (NREL, 2009) and of the Soltigua / Sopogy datasheets |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; verified against an independent Python re-evaluation and the published reference values (see *Verification*) |

## Problem statement

Parabolic-trough solar fields are simulated with empirical receiver heat-loss
correlations: fast curve fits of measured or modelled data, used in SAM and
Excelergy, that return the heat loss per metre of receiver as a function of
the receiver temperature, the ambient conditions, the wind and the
insolation. This library gathers the correlations of the ThermoCycle solar
absorber models as EES functions, with their coefficient records, so that
they can be evaluated and compared with the first-principles receiver model
`CSL-0082` and with the published data.

## Model

Six functions (all explicit, SI units, temperatures in °C — the unit the
correlations were fitted in; incidence angle in degrees, the original takes
it in radians):

| Function | Returns | Reference |
|---|---|---|
| `heat_loss_ptr70(T_fluid, T_amb, DNI, v_wind, Theta, A0…A6)` | heat loss [W/m] | Burkholder & Kutscher, NREL/TP-550-45633, Tables 6 and 8 |
| `eta_opt_ptr70(Theta, rho_cl, eps6)` | optical efficiency [-] | as in the original (`AbsSchottSopo.mo`) |
| `eta_opt_t_ptr70(Theta, rho_cl, Alpha_t, tau_g, eps6)` | optical efficiency of the tube [-] | as in the original |
| `eta_th_ptr70(HL, L, Q_tube_tot)` | thermal efficiency [-] | derived from the fluxes of the original |
| `iam_soltigua(Theta, A_0, A_1, A_2, A_3)` | longitudinal IAM `K_l` [-] | Soltigua PTMx datasheet REV03-04/2013 |
| `eta_soltigua(T_fluid, T_amb, DNI, K_l)` | collector efficiency [-] | Soltigua PTMx datasheet |

Schott/Sopogy coefficient records (passed as arguments, as in the replaceable
geometry records of the original); the values are those of NREL/TP-550-45633
except the Soponova record, which is the one of the ThermoCycle file:

| Record | A0 | A1 | A2 | A3 | A4 | A5 | A6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PTR70 vacuum (NREL Table 6) | 4.05 | 0.247 | −1.46·10⁻³ | 5.65·10⁻⁶ | 7.62·10⁻⁸ | −1.70 | 0.0125 |
| PTR70 lost vacuum (NREL Table 8) | 50.8 | 0.904 | 5.79·10⁻⁴ | 1.13·10⁻⁵ | 1.73·10⁻⁷ | −43.2 | 0.524 |
| PTR70 hydrogen (NREL Table 8) | 11.8 | 1.35 | 7.50·10⁻⁴ | 4.07·10⁻⁶ | 5.85·10⁻⁸ | −4.48 | 0.285 |
| Sopogy Soponova (ThermoCycle) | 11.8 | 1.35 | 7.50·10⁻⁴ | 4.07·10⁻⁶ | 5.85·10⁻⁸ | −4.48 | 0.285 |
| PTR70 broken glass (NREL Table 8, not in ThermoCycle) | −9.95 | 0.465 | −8.54·10⁻⁴ | 1.85·10⁻⁵ | 6.89·10⁻⁷ | 24.7 | 3.37 |

Soltigua PTMx geometry records (net collecting surface `S_net` [m²], aperture
`A_P` = 2.37 m, tube diameter 0.0424 m, and the `K_l` coefficients):

| Record | `S_net` [m²] | A_0 | A_1 | A_2 | A_3 |
|---|---:|---:|---:|---:|---:|
| PTMx-18 | 41 | 1 | 5.00396825·10⁻⁴ | −1.65·10⁻⁴ | −6.94444444·10⁻⁷ |
| PTMx-24 | 54 | 1.00057143 | 7.28571429·10⁻⁴ | −1.63214286·10⁻⁴ | −7.5·10⁻⁷ |
| PTMx-30 | 68 | 1.00078571 | 8.38888889·10⁻⁴ | −1.60595238·10⁻⁴ | −8.05555556·10⁻⁷ |
| PTMx-36 | 82 | 1 | 8.95634921·10⁻⁴ | −1.57380952·10⁻⁴ | −8.61111111·10⁻⁷ |
| PTMx-100 | 127.66 | 1 | 8.0·10⁻⁴ | −2.0·10⁻⁴ | −7.0·10⁻⁷ |

The demonstration program evaluates: (1) the PTR70 vacuum correlation at the
eleven measured points of the NREL heat-loss test (receiver #1 of Table 3,
test-stand ambient 23 °C, no solar input, still air); (2) the five coefficient
records at a typical operating point (350 °C, 30 °C, 950 W/m², 2 m/s, 20°);
(3) the optical/thermal efficiency chain of the PTR70 at a solar operating
point; (4) the Soponova record next to the independent 10-coefficient Soponova
correlation of Quoilin et al. (LaboThapPy `LTP-050`, not a library function —
evaluated inline for comparison); (5) the Soltigua `K_l` polynomial of the
PTMx-36 against the datasheet table, and the efficiency at the datasheet
reference condition.

## How to run

Open `parabolic_trough_loss_correlations.eescode` in the CoolSolve GUI and
press *Solve*, or from a terminal:

```bash
coolsolve ./parabolic_trough_loss_correlations.eescode
```

No guess values are needed (the system is fully explicit). To use the
functions in another model, copy the definitions (or `$INCLUDE
library:parabolic_trough_loss_correlations` once `CS-FEAT-IMPORT` is
available) and call them with the coefficient record of the receiver.

## Results

Baseline of the `.sol` (demonstration program):

| Quantity | Value | Reference |
|---|---:|---|
| PTR70 heat loss at the NREL test points | 14.1 … 481.5 W/m | measured 15 … 495 W/m (Table 3) |
| largest deviation from the measured values | −13.5 W/m at 506 °C (2.7 %) | within the ±10 W/m uncertainty elsewhere |
| PTR70 vacuum loss at 350 °C, 950 W/m², 2 m/s, 20° | 158.1 W/m | ≈ 150 W/m at 350 °C (report, Fig. 9) |
| PTR70 lost-vacuum / hydrogen loss at the same point | 1090 / 839 W/m | compromised HCEs lose much more (report, §21) |
| `eta_opt` / `eta_opt_t` at 5° | 0.887 / 0.783 | — |
| `eta_th` / `eta_TOT` at 350 °C, 900 W/m² | 0.955 / 0.747 | — |
| Soponova: ThermoCycle record vs Quoilin et al. | 661 vs 144 W/m | factor 4.6 — see *Conversion log* |
| Soltigua `K_l` vs the datasheet table (PTMx-36) | max deviation 0.003 | datasheet REV03-04/2013 |
| Soltigua efficiency at the datasheet reference condition | 0.633 (570 W/m²) | datasheet: 537 W/m² at `T_out` = 200 °C |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
      saved in figures/, e.g.  ![heat loss vs temperature](figures/<name>_png)  + one-line caption -->

## Verification

No reference results are stored in the ThermoCycle repository; the
verification reproduces the published values, cross-checked by an independent
Python re-evaluation of the same equations (throw-away script in the
conversion work folder, deleted after the import).

1. **Independent Python re-evaluation** (same equations, written from the
   Modelica source): 34 common variables, **0 differ** at the
   `compare_solution.py` tolerance (rtol = 1e-3); maximum relative difference
   **4.6·10⁻¹⁰** (`HL_calc[5]`).
2. **NREL PTR70 heat-loss test** (F. Burkholder and C. Kutscher,
   NREL/TP-550-45633, May 2009, Table 3): the vacuum correlation evaluated at
   the eleven measured absorber temperatures of receiver #1 (test-stand
   ambient 23 °C, DNI = 0, still air — the stand is indoors) reproduces the
   measured heat losses with deviations of −13.5 … +3.8 W/m. All points except
   the last are within the ±10 W/m uncertainty of the report; the 506 °C point
   (−13.5 W/m, 2.7 %) lies just above the 500 °C upper end of the parametric
   runs from which the correlation was derived (the correlation fits the
   *modelled* results, not the measurements). The correlation gives 158 W/m at
   350 °C, consistent with the ≈ 150 W/m read from Figure 9 of the report.
3. **Soltigua PTMx datasheet** (REV03-04/2013, cited in the original file):
   the corrected `K_l` polynomial reproduces the datasheet IAM table within
   0.003 at 0–60° for the PTMx-18/24/30/36 (checked for all four models in the
   Python re-evaluation; the demo shows the PTMx-36). The efficiency at the
   datasheet reference condition (`T_fluid` = 190 °C, mean of the 180–200 °C
   operating range, `T_amb` = 30 °C, DNI = 900 W/m², θ = 0°) is 0.633, i.e.
   570 W/m² — the same order as the datasheet's specific power of 537 W/m²
   (the datasheet does not state whether its ΔT is based on the inlet, mean
   or outlet temperature).
4. **Cross-check with `CSL-0082`** (the Forristal first-principles receiver
   model, card C-89): that model over-predicts the test-stand heat loss by a
   factor 1.9–5.8 (documented in its README), while the empirical PTR70
   correlation of this library reproduces the measured values — the two
   models bracket the stand data of the same test programme, and users
   needing measured-data predictions should use the empirical correlations.

## Source and attribution

This CoolSolve model is a translation (EES-compatible language,
equation-oriented) of the models `AbsSchottSopo` and `AbsSoltigua` and of
their geometry records from the ThermoCycle Modelica library, files
`ThermoCycle/Components/HeatFlow/Walls/SolarAbsorber/` (local clone
`~/git/Thermocycle-library`, commit `b4f16c0b`).
ThermoCycle — https://github.com/thermocycle/Thermocycle-library
Copyright (c) 2018 Thermodynamics Laboratory (University of Liège), MIT
License.
Original authors of the models: S. Quoilin and A. Desideri (see the git
history of the files and the package headers; the ThermoCycle maintainers are
B. Dechesne, J. Vega, S. Quoilin and J. Wronski). Scientific references: F.
Burkholder and C. Kutscher, *Heat Loss Testing of Schott's 2008 PTR70
Parabolic Trough Receiver*, NREL/TP-550-45633, May 2009 (correlation and
coefficient Tables 6 and 8, measured data Table 3); Soltigua PTMx datasheet
REV03-04/2013 (efficiency fit and `K_l` table); Sopogy Soponova datasheet
(cited in the original file). The independent Soponova correlation used for
comparison in the demo is that of Quoilin et al. (LaboThapPy
`correlations/solar/heat_losses.py`, inventory row `LTP-050`, not yet in the
library).

## Conversion log

- **2026-10-06 — translation** (`T-FUNC`/`T-TRANSLATE`): Modelica → EES. The
  correlations are steady explicit fits (no dynamic terms). The geometry
  records become function arguments, as in the replaceable `geometry`
  parameter of the original. The incidence angle is taken in degrees (the
  original is in radians; rad = deg·π/180); the receiver temperature enters
  in °C, the unit of the fits. Comments translated to English, standard
  header added. Verified as described above.
- **Source defects found and corrected** (each with its evidence):
  1. *Sign of the `A_2` term of the Soltigua `K_l` polynomial.* The original
     writes `K_l = A_3·Θ³ − A_2·Θ² + A_1·Θ + A_0`, which gives `K_l`(10°) =
     1.021 > 1 — unphysical for an incidence-angle modifier. With the
     standard all-plus form `A_3·Θ³ + A_2·Θ² + A_1·Θ + A_0` the polynomial
     reproduces the datasheet `K_l` table within 0.003 at 0–60° for the
     PTMx-18/24/30/36. Corrected; the demo checks the corrected form against
     the table.
  2. *Typo `A_3 = -2-6.94444444E-07`* of the Soltigua `BaseGeometry` record
     (already flagged in the source README §8). Corrected to
     `A_3 = -6.94444444E-07`: the other PTMx records have
     `A_3` ≈ −7.5…−8.6·10⁻⁷, and the corrected value reproduces the datasheet
     table (the typo value would give `K_l`(60°) ≈ −431). The PTMx-18 record,
     which does not override `A_3`, is the one concerned.
  3. *Soponova coefficient record identical to the PTR70 hydrogen record*
     (flagged as a probable copy in the source README §8; NREL Table 8
     confirms the hydrogen record). Kept as in the source — it is what the
     original file holds — and documented: at `T_fluid` = 300 °C,
     `T_amb` = 30 °C, DNI = 900 W/m², `v_wind` = 2 m/s it gives 661 W/m,
     while the independent Soponova correlation of Quoilin et al. (LTP-050)
     gives 144 W/m at the same point. The ThermoCycle record is therefore not
     the Soponova receiver's correlation; users should pass the LTP-050
     coefficients once that card is merged.
  4. *Double-counted 0.64 W/(m²·K) loss in `AbsSoltigua`* (flagged in the
     source README §8): the efficiency fit already contains the loss term
     `−0.64·(T−T_amb)/DNI`, and the model subtracts `Phi_amb` =
     `0.64·(T_amb−T)` again in the wall balance. The function library ships
     the datasheet efficiency fit only; the double-counting is a property of
     the original model's wall balance, not of the fit.
- **Level**: score of `docs/taxonomy.md` §3 — 134 equations (50–300) → 1;
  functions and `DUPLICATE` arrays → 1; semi-empirical calibration → 1;
  largest block 1 → 0; no multi-zone structure → 0; no curated guesses → 0.
  Score 3 → **level 2**.

## Limitations and CoolSolve gaps

- Validity range of the PTR70 correlation: receiver temperatures of
  100–500 °C (the parametric runs of the report); the demo's 506 °C test
  point is slightly outside.
- The `A4` term of the PTR70 correlation is written `DNI·cos(Θ)` following
  the ThermoCycle model (the report's `Ib·IAM·cosθ` with the collector IAM).
- The Soponova coefficient record of the original is suspect (see
  *Conversion log*); the broken-glass record of NREL Table 8 is not among the
  ThermoCycle geometry records and is shown for demonstration only.
- No CoolSolve gap was met; the file is valid EES and runs natively.

## Related models

- `CSL-0082` *parabolic_trough_receiver_forristal*: the first-principles
  1D radial receiver balance of the same collector family (Forristal/NREL);
  the cross-check between the two models is discussed in *Verification*.
- The Dickes–Lemort–Quoilin parabolic-trough collector models (LaboThapPy
  inventory rows `LTP-020`/`LTP-050`, including the independent Soponova
  correlation used in the demo) are not in the library yet; the function
  names and units of this library are chosen to be compatible with them.
