# Pool nucleate boiling heat flux and critical heat flux

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0088`

Nine pool nucleate-boiling heat-transfer-coefficient correlations (Rohsenow,
McNelly, Forster-Zuber, Montinsky, Stephan-Abdelsalam and its five variants,
HEDH-Taborek, Bier, Cooper, Gorenflo) and three critical-heat-flux
correlations (Zuber, Serth-HEDH, HEDH-Montinsky), as twelve EES `FUNCTION`s.
The boiling functions return the wall heat-transfer coefficient `h`
[W/m²/K] of a pool-boiling surface (an evaporator tube wall) for a given excess
wall temperature `Te = T_wall − T_sat` [K], the wall heat flux follows from
`q = h*Te` and is left to the caller; the CHF functions return the upper limit
`q_crit` [W/m²] of that flux. The correlations take the liquid and vapour
properties as arguments (`rhol`, `rhog`, `mul`, `kl`, `Cpl`, `Hvap`, `sigma`,
`MW`, `P`, `Pc`, `Tsat`, `dPsat`); no property function is called inside a
`FUNCTION`, so the calling model passes them. This is the second of the 24 `ht`
families planned for the library (roadmap cards C-96…C-119) and follows the
layout of `CSL-0087`.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; the fluid properties are arguments) |
| **Size** | 78 equations after analysis (largest block: 1); 12 functions of 1–13 equations (the demonstration program accounts for the 46 input assignments and the 32 calls) |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/boiling_nucleic.py` (MIT); inventory row `HT-002` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (32 values, max deviation 4.1·10⁻¹¹) |

## Problem statement

An evaporator surface is heated above the saturation temperature of the
saturated liquid covering it. While the wall temperature stays small enough for
the vapour bubbles to leave freely — the *nucleate boiling* regime — the wall
heat flux rises steeply with the excess wall temperature; at the *critical heat
flux* the vapour layer can no longer remove the heat and the wall burns out.
Between the two limits the wall heat flux is predicted by a historical family of
correlations, each with its own input properties (all of them, or only the
reduced pressure, or nothing at all but the surface temperature), its own
validity and its own numerical result: for water at atmospheric pressure and an
excess wall temperature of 4.3 K, the five correlations of this library that
take that fluid's properties return `h` between 534 W/m²/K (`h_McNelly`) and
3520 W/m²/K (`h_Forster_Zuber`), i.e. wall fluxes of 2.3 to 15.1 kW/m² for the
same physical state (a factor 6.6), while the three correlations that only need
the reduced pressure `P/Pc` fall inside that range (1185 W/m²/K for
`h_Montinsky`, 1291 for `h_Bier`, 1558 for `h_Cooper`). The choice between them,
and the comparison with the CHF of the same fluid, is left to the user, who
knows the fluid, the surface and the geometry.

## Model

Nine boiling correlations (return `h` [W/m²/K]) and three CHF correlations
(return `q_crit` [W/m²]):

| EES `FUNCTION` | Arguments | Equation |
|---|---|---|
| `h_Rohsenow` | rhol, rhog, mul, kl, Cpl, Hvap, sigma, Te, Csf, n | h = µ_l·Hvap·[g(ρ_l−ρ_v)/σ]^0.5·[Cp_l·Te^(2/3)/(Csf·Hvap·Pr_lⁿ)]³ |
| `h_McNelly` | rhol, rhog, kl, Cpl, Hvap, sigma, P, Te | h = {0.225·(Te·Cp_l/Hvap)^0.69·(P·k_l/σ)^0.31·(ρ_l/ρ_v−1)^0.33}^(1/0.31) |
| `h_Forster_Zuber` | rhol, rhog, mul, kl, Cpl, Hvap, sigma, dPsat, Te | h = 0.00122·(k_l^0.79·Cp_l^0.45·ρ_l^0.49/(σ^0.5·µ_l^0.29·Hvap^0.24·ρ_v^0.24))·Te^0.24·ΔP_sat^0.75 |
| `h_Montinsky` | P, Pc, Te | h = {0.00417·Pc^0.69·Te^0.7·[1.8·p_r^0.17 + 4·p_r^1.2 + 10·p_r¹⁰]}^(1/0.3) |
| `h_Stephan_Abdelsalam` | rhol, rhog, mul, kl, Cpl, Hvap, sigma, Tsat, Te, form, kw, rhow, Cpw | five variants (`form` = 1 general, 2 water, 3 hydrocarbon, 4 cryogenic, 5 refrigerant), e.g. general: h = {0.23·X1^0.674·X2^0.35·X3^0.371·X5^0.297·X8⁻¹·⁷³·k_l/D_b}^(1/0.326), with D_b = 0.0146·angle·(2σ/(g(ρ_l−ρ_v)))^0.5 and X1…X8 as in the comment block |
| `h_HEDH_Taborek` | P, Pc, Te | h = {0.00417·Pc^0.69·Te^0.7·[2.1·p_r^0.27 + (9 + 1/(1−p_r²))·p_r²]}^(1/0.3) |
| `h_Bier` | P, Pc, Te | h = {0.00417·Pc^0.69·Te^0.7·[0.7 + 2·p_r·(4 + 1/(1−p_r))]}^(1/0.3) |
| `h_Cooper` | P, Pc, MW, Te, Rp | h = {55·Te^0.67·p_r^(0.12−0.2·log₁₀R_p)·(−log₁₀p_r)^−0.55·MW^−0.5}^(1/0.33) |
| `h_Gorenflo` | P, Pc, h0, Ra, Te, is_water | h = {h0·C_W·F(p_r)·(Te/q₀)ⁿ}^(−1/(n−1)), C_W = (Ra/Ra₀)^0.133, q₀ = 20 000 W/m², Ra₀ = 0.4 µm; water: n = 0.9 − 0.3·p_r^0.15, F(p_r) = 1.73·p_r^0.27 + (6.1 + 0.68/(1−p_r))·p_r²; other fluids: n = 0.9 − 0.3·p_r^0.3, F(p_r) = 1.2·p_r^0.27 + (2.5 + 1/(1−p_r))·p_r |
| `q_CHF_Zuber` | sigma, Hvap, rhol, rhog, K | q_crit = K·Hvap·ρ_v^0.5·[σ·g·(ρ_l−ρ_v)]^0.25 |
| `q_CHF_Serth_HEDH` | Di, sigma, Hvap, rhol, rhog | as `q_CHF_Zuber` with R\* = Di/2·[g(ρ_l−ρ_v)/σ]^0.5 and K = 0.125·R\*^−0.25 for 0.12 ≤ R\* ≤ 1.17, K = 0.118 otherwise |
| `q_CHF_HEDH_Montinsky` | P, Pc | q_crit = 367·Pc·p_r^0.35·(1−p_r)^0.9 |

Arguments: `rhol`, `rhog` (liquid and vapour density, `[kg/m³]`), `mul` (liquid
viscosity, `[Pa·s]`), `kl` (liquid thermal conductivity, `[W/m/K]`), `Cpl`
(liquid heat capacity, `[J/kg/K]`), `Hvap` (heat of vaporization at P, `[J/kg]`),
`sigma` (surface tension, `[N/m]`), `P` (saturation pressure, `[Pa]`), `Pc`
(critical pressure, `[Pa]`), `Tsat` (saturation temperature at P, `[K]`),
`dPsat` (rise of the saturation pressure between Te and Tsat, `[Pa]`), `Te`
(excess wall temperature, `[K]`), `MW` (molar mass, `[g/mol]`, as in `ht`),
`Di` (inside diameter of the tubes, `[m]`), `Rp` / `Ra` (surface roughness
parameters of Cooper and Gorenflo, `[m]`), `K` (constant of the Zuber CHF, `[−]`),
`h0` (reference heat-transfer coefficient of the Gorenflo method, `[W/m²/K]`),
`kw`, `rhow`, `Cpw` (wall conductivity, density and heat capacity, used by the
cryogenic variant of Stephan-Abdelsalam) and the two variant flags `form` and
`is_water` (1 or 0). `p_r = P/Pc` and `Pr_l = Cp_l·µ_l/k_l` are local variables of
the functions, as `ht` computes them internally.

Every function carries in its comment block (i) the equation, (ii) the validity
range **as quoted by `ht`** — none of these correlations quotes a numerical range,
so the note is the one of `ht` ("nucleate boiling regime", "diverges as p_r → 1",
…), (iii) the original paper or book and (iv) the `ht` module, function, version
and commit it was taken from. The correlations come from Forster & Zuber (1955)
to Schlünder's *VDI Heat Atlas* (1993); the original references are named
individually (Rohsenow 1951, McNelly 1953, Forster & Zuber 1955, Montinsky 1963,
Stephan & Abdelsalam 1980, Taborek 1986, Cooper 1984, Zuber 1958, Gorenflo 1993,
Serth 2014 as the secondary source of most of them).

Four members of the `ht` family are **not** translated: `h_nucleic`,
`h_nucleic_methods`, `qmax_boiling` and `qmax_boiling_methods` are dispatchers
that map a method name to a correlation; an EES caller calls the chosen
`FUNCTION` directly. The two data tables of `ht` (`h0_Gorenflow_1993` and
`h0_VDI_2e`, one reference coefficient per CAS number, 44 and 51 fluids) are
not translated either: `h0` is an **argument** of `h_Gorenflo` and the caller
reads the value of its fluid from the VDI Heat Atlas.

## How to run

Open `nucleate_boiling_and_chf.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./nucleate_boiling_and_chf.eescode
```

The demonstration program after the definitions calls each of the 12 functions
twice: once (case *A*) with the input set of the `ht` doctest of the
corresponding correlation — the `Stephan-Abdelsalam` function is called for its
five variants and `q_CHF_Zuber` for the two constants K = 0.149 and K = 0.18 —
and once (case *B*) with a single uniform input set: water at 1 atm
(ρ_l = 958 kg/m³, ρ_v = 0.597 kg/m³, µ_l = 2.75·10⁻⁴ Pa·s, k_l = 0.688 W/m/K,
Cp_l = 4180 J/kg/K, Hvap = 2.25·10⁶ J/kg, σ = 0.0588 N/m, P = 101 325 Pa,
Pc = 22 048 321 Pa, MW = 18.02 g/mol, Rp = 1 µm, h0 = 5600 W/m²/K, Ra = 0.4 µm,
T_sat = 373.15 K) at an excess wall temperature Te = 15 K, with ΔP_sat estimated
as 3906 K⁻¹·Te (the linear estimate used in the `ht` test suite) and a 5 mm
inside diameter for `q_CHF_Serth_HEDH`. It solves without any iteration
(`Solver: SUCCESS (0 iterations)`, every equation is explicit) and is the
regression baseline (`nucleate_boiling_and_chf.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0088 ---}` and
lists `CSL-0088` in its `related` field.

## Results

Values of the demonstration program (full precision in
`nucleate_boiling_and_chf.sol`):

| Quantity (case A) | h [W/m²/K] or q_crit [W/m²] | Quantity (case B) | h [W/m²/K] or q_crit [W/m²] |
|---|---:|---|---:|
| `h_Rohsenow` (water, Te = 4.9 K) | 3723.66 | (Te = 15 K) | 34810.19 |
| `h_McNelly` (water, Te = 4.3 K) | 533.81 | | 8613.04 |
| `h_Forster_Zuber` (water, Te = 4.3 K) | 3519.92 | | 12126.34 |
| `h_Montinsky` (water, Te = 4.3 K) | 1185.05 | | 21870.41 |
| `h_Stephan_Abdelsalam` (general) | 26722.44 | (general) | 13883.18 |
| `h_Stephan_Abdelsalam_water` | 30571.79 | | |
| `h_Stephan_Abdelsalam_hydrocarbon` | 21009.03 | | |
| `h_Stephan_Abdelsalam_cryogenic` | 3548.81 | | |
| `h_Stephan_Abdelsalam_refrigerant` | 84657.99 | | |
| `h_HEDH_Taborek` (P = 310.3 kPa, Pc = 2550 kPa, Te = 16.2 K) | 1397.27 | (water, Te = 15 K) | 5914.13 |
| `h_Bier` (water, Te = 4.3 K) | 1290.53 | | 23817.14 |
| `h_Cooper` (water, Te = 4.3 K) | 1558.14 | | 19692.29 |
| `h_Gorenflo` (water at 3 bar, Te = 6.57 K) | 3043.34 | (water, Te = 15 K) | 12878.56 |
| `q_CHF_Zuber` (K = 0.149) | 444307.22 | (water, K = 0.149) | 1255608.22 |
| `q_CHF_Zuber_K018` (K = 0.18) | 536746.98 | | |
| `q_CHF_Serth_HEDH` (Di = 12.7 mm, R\* = 5.14) | 351867.47 | (Di = 5 mm, R\* = 1.00) | 1053629.99 |
| `q_CHF_HEDH_Montinsky` (P = 310.3 kPa, Pc = 2550 kPa) | 398405.67 | (water) | 1224787.02 |
| `q_Rohsenow` = h·Te [W/m²] | 18245.91 | | 522152.88 |
| `q_Gorenflo` = h·Te [W/m²] | 20000.00 | | |

Sanity checks: the wall heat flux of case A (18 246 W/m² at Te = 4.9 K) is
1.45 % of the Zuber CHF of water at 1 atm (1.2556 MW/m²), i.e. the state is
clearly inside the nucleate boiling regime, and the same holds for case B
(522 153 W/m² at Te = 15 K, 41.6 % of that CHF). The three CHF correlations of
water at 1 atm stay within 16 % of each other (Serth-HEDH 1.0536, HEDH-Montinsky
1.2248 and Zuber 1.2556 MW/m², the last two with K = 0.149), and `q_Gorenflo_A`
= 20 000 W/m² is the flux of the state whose excess wall temperature was used as
input, by construction.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the nine boiling
     correlations h(Te) for water at 1 atm up to the Zuber CHF, e.g.
     figures/nucleate_boiling_and_chf_h_te.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/boiling_nucleic.py`, commit `85e0ee6`, installed from the local clone
`~/git/ht` in a throw-away virtual environment) for case *A* — where `ht` gives
no doctest for `Gorenflo` in its `Te` form, the input set of the case is the one
of its heat-flux doctest (`q = 20 000 W/m²` at 3 bar) converted to the excess
wall temperature Te = q/h = 6.5717 K, so the value reproduced is again the
published one (3043.3446) — plus values computed with the same Python functions
for case *B*. The 32 output values of the demonstration program were compared
with `CoolSolve/tools/compare_solution.py` (tolerance `rtol = 0.001`):

```
32 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 46
```

(the 46 "only in CoolSolve" variables are the 46 inputs of the demonstration
program — the three property sets `rhol_w1`…`MW_w1`, `rhol_w2`…`Hvap_w2` and
`rhol_r`…`Cpw_r`, the two Gorenflo references `h0_w`/`Ra_w` and their `_B`
counterparts —; the reference table holds only the 32 outputs). The largest
relative deviation over the 32 values is **4.1·10⁻¹¹** (`h_Cooper_A`), i.e.
round-off in the double-precision evaluation.

Per-function values, `ht` / CoolSolve:

| Function (case A) | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `h_Rohsenow_A` | 3723.655267067 | 3723.655267066 | 3.9e-13 |
| `h_McNelly_A` | 533.805697295 | 533.805697295 | 6.6e-14 |
| `h_Forster_Zuber_A` | 3519.923989746 | 3519.923989746 | 7.5e-14 |
| `h_Montinsky_A` | 1185.050977029 | 1185.050977029 | 2.2e-13 |
| `h_Stephan_Abdelsalam_A` (general) | 26722.441071108 | 26722.441071110 | 6.1e-14 |
| `h_Stephan_Abdelsalam_water_A` | 30571.788078886 | 30571.788078890 | 1.2e-13 |
| `h_Stephan_Abdelsalam_hydrocarbon_A` | 21009.034222030 | 21009.034222030 | 7.1e-15 |
| `h_Stephan_Abdelsalam_cryogenic_A` | 3548.805036091 | 3548.805036091 | 8.3e-14 |
| `h_Stephan_Abdelsalam_refrigerant_A` | 84657.985955520 | 84657.985955570 | 6.0e-13 |
| `h_HEDH_Taborek_A` | 1397.272486525 | 1397.272486525 | 3.5e-13 |
| `h_Bier_A` | 1290.534947150 | 1290.534947150 | 2.6e-13 |
| `h_Cooper_A` | 1558.143544215 | 1558.143544279 | 4.1e-11 |
| `h_Gorenflo_A` | 3043.344595525 | 3043.344595571 | 1.5e-11 |
| `q_CHF_Zuber_A` (K = 0.149) | 444307.223043423 | 444307.223043400 | 5.1e-14 |
| `q_CHF_Zuber_K018_A` (K = 0.18) | 536746.980857826 | 536746.980857800 | 4.9e-14 |
| `q_CHF_Serth_HEDH_A` | 351867.465229019 | 351867.465229000 | 5.5e-14 |
| `q_CHF_HEDH_Montinsky_A` | 398405.665451814 | 398405.665451800 | 3.6e-14 |
| `q_Rohsenow_A` = h·Te | 18245.910808631 | 18245.910808630 | 3.2e-14 |
| `q_Gorenflo_A` = h·Te | 20000.000000000 | 20000.000000300 | 1.5e-11 |

Case *B* (second input set, computed with the same Python functions):

| Function | `ht` | CoolSolve | Function | `ht` | CoolSolve |
|---|---:|---:|---|---:|---:|
| `h_Rohsenow_B` | 34810.1920 | 34810.1920 | `h_Gorenflo_B` | 12878.5645 | 12878.5645 |
| `h_McNelly_B` | 8613.0415 | 8613.0415 | `q_CHF_Zuber_B` | 1255608.2151 | 1255608.2151 |
| `h_Forster_Zuber_B` | 12126.3433 | 12126.3433 | `q_CHF_Serth_HEDH_B` | 1053629.9914 | 1053629.9914 |
| `h_Montinsky_B` | 21870.4091 | 21870.4091 | `q_CHF_HEDH_Montinsky_B` | 1224787.0163 | 1224787.0163 |
| `h_Stephan_Abdelsalam_B` | 13883.1837 | 13883.1837 | `q_Rohsenow_B` | 522152.8801 | 522152.8801 |
| `h_HEDH_Taborek_B` | 5914.1279 | 5914.1279 | | | |
| `h_Bier_B` | 23817.1419 | 23817.1419 | | | |
| `h_Cooper_B` | 19692.2884 | 19692.2884 | | | |

All 32 relative deviations are below 4.2·10⁻¹¹. Two cross-checks of the forms
that are **not** translated, computed with `ht` only: `Rohsenow(q = 18 245.91
W/m²)` returns the same `h` as `Rohsenow(Te = 4.9 K)` (3723.6552670674655 vs
3723.6552670674669), and `Gorenflo(P = 3 bar, Te = 6.5717 K)` returns the value of
the heat-flux doctest (3043.3445955254) — the heat-flux form is the implicit
inversion of the excess-temperature form, so `q = h*Te` is enough for the
caller.

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the pool nucleate boiling and critical heat flux
correlations of `ht`, the heat-transfer component of ChEDL, file
`ht/boiling_nucleic.py`, functions `Rohsenow`, `McNelly`, `Forster_Zuber`,
`Montinsky`, `Stephan_Abdelsalam`, `HEDH_Taborek`, `Bier`, `Cooper`, `Gorenflo`,
`Zuber`, `Serth_HEDH` and `HEDH_Montinsky`, version 1.2.0, commit `85e0ee6`
(2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one EES
`FUNCTION` named after the `ht` function (with the `h_` prefix of the library
convention for the nine boiling correlations and `q_CHF_` for the three CHF
ones), the string selector `correlation` of `Stephan_Abdelsalam` became an
integer flag `form` (1 general, 2 water, 3 hydrocarbon, 4 cryogenic, 5
refrigerant) and the string selector `CASRN` of `Gorenflo` (water or not) became
the flag `is_water`, the reference coefficient `h0` of `Gorenflo` became an
argument instead of a CAS-number lookup in a data table, the Python `log10`
became the EES `LOG10`, the optional arguments of the Python functions became
mandatory, and `g = 9.80665 m/s²` (the `fluids.constants.g` value used by `ht`)
is written out in the functions that need it. No equation was changed. Scientific
basis per function: the original paper or book quoted in its comment block.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`); the references most of them
come from in `ht` are Rohsenow, Hartnett & Cho, *Handbook of Heat Transfer*,
3E, McGraw-Hill 1998, Serth, *Process Heat Transfer*, 2E, 2014, and Schlünder,
*Heat Exchanger Design Handbook*, 1987.

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-97, family `HT-002`).** One EES
  `FUNCTION` per `ht` correlation (12 functions), named `h_<method>` and
  `q_CHF_<method>`, with the formula, the validity note of `ht`, the original
  reference and the `ht` module/function/version/commit in the comment block.
  Arguments are the Python arguments, in SI (`Pa`, `K`, `m`, `Pa·s`, `J/kg`,
  `N/m`), except `MW` which stays in `g/mol` as in `ht`; no property function is
  used inside a function, so the calling model passes the fluid properties itself
  (rule 5 of `sources/ht/README.md` §7).
- **The heat-flux form of the nine boiling correlations is not translated.** In
  `ht` each of them comes in two algebraic forms, one with the excess wall
  temperature `Te` and one with the heat flux `q`; the second is the implicit
  inversion of the first (checked against `ht`: `Rohsenow(q = h·Te)` and
  `Rohsenow(Te)` return the same `h`, and `ht`'s own test suite asserts it for
  `Rohsenow`, `McNelly`, `Forster_Zuber`, `Montinsky`, `HEDH_Taborek`, `Bier`,
  `Cooper`, `Stephan_Abdelsalam` and `Gorenflo`). The `Te` form is used here and
  the caller computes `q = h*Te`; this is stated in the file header.
- **String selectors became integer flags**: `Stephan_Abdelsalam.correlation`
  (`'general'`, `'water'`, `'hydrocarbon'`, `'cryogenic'`, `'refrigerant'`) is
  `form` = 1…5, and the water test of `Gorenflo` (`CASRN = '7732-18-5'`) is the
  flag `is_water`. The two `ht` data tables of reference coefficients
  (`h0_Gorenflow_1993`, `h0_VDI_2e`) are not translated — no data file is copied
  into the library — so `h0` is an argument; the demonstration program passes
  5600 W/m²/K, the value of that table for water.
- **Non-smooth regime switches use nested `IF` blocks** (the `form` and
  `is_water` selectors, and the R\* range of `q_CHF_Serth_HEDH`, written
  `IF R >= 0.12 AND R <= 1.17` as the CoolSolve Language Reference §6 allows).
  The one-word `ELSEIF` keyword is **not** used: CoolSolve 0.3.0 reads it as an
  unknown function, and a body written with it can return the wrong branch with
  a `SUCCESS` status (see *Limitations*).
- **Two discrepancies between the `ht` docstring and its code** were resolved in
  favour of the code, so that the values agree with `ht`, and both are noted in
  the comment block of the function: `Stephan_Abdelsalam` computes `X3` and `X4`
  identically (`Hvap·D_b²/α_l²`) where its docstring gives
  `X3 = Cp_l·T_sat·D_b²/α_l²`, and `Serth_HEDH` uses `K = 0.125·R*^−0.25` where
  its docstring writes 0.123 (the code value reproduces its doctest
  351867.465229019).
- **Argument names kept from `ht`**, including `Ra` in `Gorenflo`, which `ht`
  names like a Rayleigh number although it is a surface roughness; the comment
  block says so.
- **Selectors not translated**: `h_nucleic`, `h_nucleic_methods`,
  `qmax_boiling` and `qmax_boiling_methods` only map a method name to a
  correlation; the caller chooses the `FUNCTION` directly.
- **Level**: equations 78 → 1 point (50–300), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0 (the same
  reading as `CSL-0087`, these are steady closed-form fits of one operating
  point), curated guesses no → 0. Score 2 → **level 2**.

## Limitations and CoolSolve gaps

- **No validity range is quoted by `ht`** for any of these twelve correlations
  (the docstrings give the formula, the original reference and an example only).
  The comment block of each function repeats the qualification `ht` does give
  ("nucleate boiling regime", "diverges as the reduced pressure approaches 1",
  "ht notes that no example is known and that the results differ very much from
  the other correlations" for `Bier`) and nothing more. The *Results* and
  *Verification* numbers are a check of the **equations**, not recommended
  design values; `Bier` in particular is reproduced here only because it is part
  of the family.
- The spread between the correlations is large: a factor 6.6 between
  `h_McNelly` and `h_Forster_Zuber` on the same water state, and a factor 50
  between `h_McNelly` (water at 1 atm, Te = 4.3 K) and `h_Stephan_Abdelsalam`
  (general variant, the doctest fluid at Te = 16.2 K). They are fits of
  different data ranges, and the choice is the user's.
- No property call is available inside the functions, so the calling model must
  supply `rhol`, `rhog`, `mul`, `kl`, `Cpl`, `Hvap`, `sigma`, `P`, `Pc`, `Tsat`
  and `dPsat` at the boiling condition.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- **No gap registered for this card**: everything is plain EES
  (`FUNCTION`, nested `IF/THEN/ELSE`, `LOG10`) and runs in CoolSolve v0.3.0.
  The `ELSEIF` misbehaviour found while writing the file is *not* registered: no
  EES manual or EES file is available here to show that the one-word `ELSEIF` is
  valid EES (the EES idiom of `ELSE` + `IF` is the one already registered as
  `CS-GAP-ELSEIF-CHAIN`, and it is also the form used here).

## Related models

- `CSL-0096` *plate_hx_heat_transfer*: the flow-boiling counterpart of this
  file for a plate heat exchanger (five two-phase heat-transfer coefficients
  written for a given heat flux, and the plate single-phase Nusselt numbers),
  same `ht` triage and same layout.
- `CSL-0087` *internal_turbulent_nusselt*: the first `ht` family of the library
  (single-phase turbulent internal convection), same file layout, same comment
  blocks; its functions take the dimensionless numbers of a pipe flow, those of
  this file the properties of the boiling fluid.
- `CSL-0054` *heat_pump_r410a_air_evaporator* and `CSL-0061`
  *refrigerator_freezer_r134a*: two evaporator models of the library that size
  the refrigerant side from the duty; the heat-transfer side of their evaporators
  is where these correlations would enter.
- `sources/thermocycle` THC-004 (flow and nucleate boiling HTC, Shah 1979):
  quotes only the Shah correlation; this family is more complete and adds the
  CHF limit.
- `sources/labothappy` LTP-034 (in-tube HTC correlations): the `ht` family is
  more complete and is the reference for the equations.
- `CSL-0089` *condensation_film*: the condensation side of the same two-phase
  heat transfer (film condensation HTC), same file layout.
- `CSL-0092` *free_conv_cylinders*: free convection from vertical and horizontal
  cylinders (13 functions of the same `ht` module and layout); the natural
  convection that assists nucleate boiling on a horizontal tube is one of its
  arguments (Pr, Gr).
- `CSL-0094` *external_crossflow_cylinder*: crossflow over a single tube
  (8 functions of the same `ht` layout); a tube on which the nucleate boiling
  of this file takes place is in a crossflow of gas or air.
- `CSL-0097` *two_phase_nonboiling_in_tube*: the two-phase non-boiling
  in-tube heat-transfer coefficients of the same `ht` triage (9 functions),
  same layout; they rate the same tube when the two-phase flow is below the
  boiling onset treated by this file.
- `CSL-0098` *flow_boiling_in_tubes*: the flow-boiling coefficients of
  the same `ht` triage plus Shah 1982 and Gungor-Winterton 1987 from
  ThermoCycle (10 functions), same layout; its h_Chen_Edelstein,
  h_Chen_Bennett and h_Liu_Winterton write out h_Forster_Zuber and h_Cooper of
  this file, and the Shah 1982 chart correlation extends this pool-boiling
  family to flowing, boiling tubes.
- `CSL-0091` *internal_laminar_and_curved_nu*: the laminar, entry-region and curved-duct (spiral, helical) internal-convection family of the same `ht` triage, same layout; it complements `CSL-0087` (turbulent pipe flow) at low Reynolds number and non-circular geometries.
