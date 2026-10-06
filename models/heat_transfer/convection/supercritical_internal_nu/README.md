# Near-supercritical internal convection: Nusselt-number correlations for vertical upward pipe flow

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0104`

Eighteen EES `FUNCTION`s returning the Nusselt number of turbulent **vertical
upward** flow in a pipe at near-supercritical pressure, from McAdams (1942) to
Petukhov-Kurganov-Ankudinov (1983). They are the correlations a designer needs
when the wall temperature crosses the pseudo-critical point of the fluid — the
regime of supercritical water in a once-through steam generator or of a
transcritical CO₂ evaporator/condenser — where the properties change steeply
between the wall and the bulk fluid and no ordinary single-phase correlation
holds. Each `FUNCTION` returns Nu; the wall heat-transfer coefficient follows
from `h = Nu*k/Di` and is left to the caller. Same layout and same comment
blocks as `CSL-0087`, the first of the `ht` families of the library.

| | |
|---|---|
| **Category** | Heat transfer › Convection |
| **Fluids** | none (the correlations are fluid-independent; Re, Pr and the wall/bulk property values are arguments) |
| **Size** | 119 equations after analysis (largest block: 1); 18 `FUNCTION`s |
| **Source** | [`ht`](https://github.com/CalebBell/ht) 1.2.0, commit `85e0ee6` (2025-12-07), file `ht/conv_supercritical.py` (MIT); inventory row `HT-018` of `sources/ht/inventory.csv` |
| **Authors** | the authors of the correlations (see the comment block of each function); the library itself: Caleb Bell and Contributors |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against `ht` 1.2.0 (71 values, max deviation 4.4·10⁻¹³) |

## Problem statement

Near the critical point of a fluid the specific heat peaks at the
pseudo-critical temperature T_pc, and the temperature of a heated wall crosses
it along the pipe. The resulting very large wall heat-transfer coefficient, and
the shapes of the density, viscosity and conductivity profiles between the wall
and the bulk, are accounted for by a family of correlations that take Re and Pr
**and** a set of property ratios or temperatures. The caller (a calling model
with real-fluid properties) computes those values and passes them to the chosen
correlation; the correlation returns Nu.

## Model

| EES `FUNCTION` | Arguments | Equation | Validity / data range (as quoted in `ht`) |
|---|---|---|---|
| `Nu_McAdams` | Re, Pr | Nu = 0.0243·Re^0.8·Pr^0.4 | no range quoted; high pressures, low heat fluxes |
| `Nu_Shitsman` | Re, Pr_b, Pr_w | Nu = 0.023·Re^0.8·min(Pr_b, Pr_w)^0.8 | D = 7.8 and 8.2 mm, Pr ≈ 1 |
| `Nu_Griem` | Re, Pr, H_b, corr | Nu = 0.0169·Re^0.8356·Pr^0.432·w, w from H_b (1540 / 1740 kJ/kg) | D = 10, 14, 20 mm; P = 22–27 MPa; G = 300–2500 kg/m²/s; q = 200–700 kW/m² |
| `Nu_Jackson` | Re, Pr, rho_w, rho_b, Cp_avg, Cp_b, T_b, T_w, T_pc, corr | Nu = 0.0183·Re^0.82·Pr^0.5·(rho_w/rho_b)^0.3·(Cp_avg/Cp_b)^n, n = 0.4 / 0.4+0.2(T_w/T_pc−1) / 0.4+0.2(T_w/T_pc−1)[1−5(T_b/T_pc−1)] | P = 23.4–29.3 MPa; G = 700–3600 kg/m²/s; q = 46–2600 kW/m²; Re = 8·10⁴–5·10⁵; D = 1.6–20 mm |
| `Nu_Gupta` | Re, Pr, rho_w, rho_b, mu_w, mu_b, corr | Nu_w = 0.004·Re^0.923·Pr̄_w^0.773·(rho_w/rho_b)^0.186·(mu_w/mu_b)^0.366 | P = 24 MPa; D = 10 mm; G = 200–1500 kg/m²/s; q = 0–1250 kW/m² |
| `Nu_Swenson` | Re, Pr, rho_w, rho_b, corr | Nu_w = 0.00459·Re^0.923·Pr̄_w^0.613·(rho_w/rho_b)^0.231 | P = 22.8–27.6 MPa; G = 542–2150 kg/m²/s; Re = 7.5·10⁴–3.16·10⁶; T_b = 75–576 °C; T_w = 93–649 °C |
| `Nu_Xu` | Re, Pr, rho_w, rho_b, mu_w, mu_b, corr | Nu_b = 0.02269·Re^0.8079·Pr̄_b^0.9213·(rho_w/rho_b)^0.6638·(mu_w/mu_b)^0.8687 | P = 23–30 MPa; D = 12 mm; G = 600–1200 kg/m²/s; q = 100–600 kW/m² |
| `Nu_Mokry` | Re, Pr, rho_w, rho_b, corr | Nu_b = 0.0061·Re^0.904·Pr̄_b^0.684·(rho_w/rho_b)^0.564 | P = 20 MPa; D = 10 mm; G = 200–1500 kg/m²/s; q = 0–1250 kW/m² |
| `Nu_Bringer_Smith` | Re, Pr | Nu_x = 0.0266·Re_x^0.77·Pr_w^0.55 | data distant from the critical region |
| `Nu_Ornatsky` | Re, Pr_b, Pr_w, rho_w, rho_b, corr | Nu_b = 0.023·Re^0.8·min(Pr_b, Pr_w)^0.8·(rho_w/rho_b)^0.3 | no range quoted |
| `Nu_Gorban` | Re, Pr | Nu_b = 0.0059·Re^0.90·Pr_b^(−0.12) | no range quoted; not recommended |
| `Nu_Zhu` | Re, Pr, rho_w, rho_b, k_w, k_b, corr | Nu_b = 0.0068·Re^0.9·Pr̄_b^0.63·(rho_w/rho_b)^0.17·(k_w/k_b)^0.29 | P = 22–30 MPa; D = 26 mm; G = 600–1200 kg/m²/s; q = 200–600 kW/m² |
| `Nu_Bishop` | Re, Pr, rho_w, rho_b, Di, x, corr | Nu_b = 0.0069·Re^0.9·Pr̄_b^0.66·(rho_w/rho_b)^0.43·(1+2.4·Di/x) | P = 22.8–27.6 MPa; x/D = 30–365; G = 651–3662 kg/m²/s; q = 310–3460 kW/m²; T_b = 282–527 °C |
| `Nu_Yamagata` | Re, Pr, Pr_pc, Cp_avg, Cp_b, T_b, T_w, T_pc, corr | Nu_b = 0.0138·Re^0.85·Pr_b^0.8·F, F from (T_pc−T_b)/(T_w−T_b) with n₁ = −0.77(1+1/Pr_pc)+1.49 and n₂ = 1.44(1+1/Pr_pc)−0.53 | P = 22.6–29.4 MPa; D = 7.5, 10 mm; G = 310–1830 kg/m²/s; q = 116–930 kW/m²; T_b = 230–540 °C |
| `Nu_Kitoh` | Re, Pr, H_b, G, q, corr | Nu_b = 0.015·Re^0.85·Pr^m, m = 0.69 − 81000/q_dht + f_c·q, q_dht = 200·G^1.2, f_c from H_b (1500 / 3300 kJ/kg) | G = 100–1750 kg/m²/s; q = 0–1800 kW/m²; T_b = 20–550 °C |
| `Nu_Krasnoshchekov_Protopopov` | Re, Pr, Cp_avg, Cp_b, k_w, k_b, mu_w, mu_b, corr | Nu = Nu₀·(mu_w/mu_b)^0.11·(k_w/k_b)^(−0.33)·(Cp_avg/Cp_b)^0.35, Nu₀ = (fd/8)Re·Pr̄/{1.07+12.7(fd/8)^0.5(Pr̄^(2/3)−1)}, fd = [1.82·LOG10(Re)−1.64]^(−2) | P = 22.3–32 MPa; Re = 2·10⁴–8.6·10⁶; Pr = 0.86–86; viscosity ratio 0.9–3.6; conductivity ratio 1–6; heat-capacity ratio 0.07–4.5 |
| `Nu_Petukhov` | Re, Pr, rho_w, rho_b, mu_w, mu_b, corr | Nu_b = (f/8)Re·Pr̄/{1+900/Re+12.7(f/8)^0.5(Pr̄^(2/3)−1)}, f = fd·(rho_w/rho_b)^0.4·(mu_w/mu_b)^0.2, fd = [1.82·LOG10(Re)−1.64]^(−2) | no range quoted |
| `Nu_Krasnoshchekov` | Re, Pr, rho_w, rho_b, Cp_avg, Cp_b, T_b, T_w, T_pc, corr | Nu = Nu₀·(rho_w/rho_b)^0.3·(Cp_avg/Cp_b)^n, n = 0.4 / n₁ = 0.22+0.18·T_w/T_pc / n₁+(5n₁−2)(1−T_b/T_pc) | P = 23.4–29.3 MPa; G = 700–3600 kg/m²/s; q = 46–2600 kW/m²; Re = 8·10⁴–5·10⁵; D = 1.6–20 mm |

Arguments: Re (Reynolds number, `[-]`, bulk or wall properties as the row of the
table above), Pr (Prandtl number, `[-]`), Pr_b / Pr_w / Pr_pc (bulk, wall and
pseudo-critical Prandtl numbers, `[-]`), rho_w / rho_b (wall and bulk
densities, `[kg/m³]`), mu_w / mu_b (wall and bulk viscosities, `[Pa·s]`), k_w /
k_b (wall and bulk conductivities, `[W/m·K⁻¹]`), Cp_avg (heat capacity
averaged between the wall and the bulk temperatures, `[J/kg·K⁻¹]`, which the
originals write (H_w−H_b)/(T_w−T_b)) and Cp_b (heat capacity at the bulk
temperature, `[J/kg·K⁻¹]`), T_b / T_w / T_pc (bulk, wall and pseudo-critical
temperatures, `[K]`), H_b (enthalpy of water, `[J/kg]`), G (mass flux,
`[kg/m²·s⁻¹]`), q (heat flux to the wall, `[W/m²]`), Di (tube diameter, `[m]`)
and x (axial distance along the tube, `[m]`), `corr` (flag: 1 or 0).

`corr` is the **decision taken** for the optional arguments of the Python
functions: EES has no optional arguments, so the corrections are applied when
`corr = 1` and the bare correlation is returned when `corr = 0` — the value
`ht` uses when the corresponding optional arguments are left out. Both forms
are exercised by the demonstration program.

Every function carries in its comment block (i) the equation, (ii) the data
range **as quoted by `ht`**, (iii) the original paper or book and (iv) the `ht`
module, function, version and commit it was taken from. All eighteen are quoted
by `ht` together with the assessment of Chen, W., X. Fang, Y. Xu and X. Su, "An
Assessment of Correlations of Forced Convection Heat Transfer to Water at
Supercritical Pressure", *Annals of Nuclear Energy* 76 (2015): 451-460, which
ranks them on three databases (normal, enhanced and deteriorated heat
transfer); the original papers are named individually (McAdams 1942,
Shitsman 1963, Griem 1996, Jackson 2002, Gupta 2010, Swenson-Carver-Kakarala
1965, Xu 2005, Mokry 2011, Bringer-Smith 1957, Ornatsky 1970, Gorban 1990,
Zhu 2009, Bishop 1965, Yamagata 1972, Kitoh 2001, Krasnoshchekov-Protopopov 1959,
Petukhov 1983, Krasnoshchekov 1967).

The module has **no selector** to translate: all 18 public functions of
`ht/conv_supercritical.py` are correlations (`ht/conv_supercritical.py` has no
`Nu_supercritical(_methods)` dispatcher, unlike the other `ht` families).

## How to run

Open `supercritical_internal_nu.eescode` in the CoolSolve GUI and press *Solve*,
or from a terminal:

```bash
coolsolve ./supercritical_internal_nu.eescode
```

The demonstration program after the definitions calls each of the 18 functions
twice per input set: case *A* with the input set of the `ht` doctest of the
correlation (the published values), case *B* with a single uniform input set
(Re = 3·10⁵, Pr = 2.5, Pr_w = 4, Pr_pc = 2.2, rho_w = 420 kg/m³,
rho_b = 280 kg/m³, mu_w = 5.5·10⁻⁵ Pa·s, mu_b = 7.5·10⁻⁵ Pa·s,
k_w = 0.095 W/m·K⁻¹, k_b = 0.078 W/m·K⁻¹, Cp_avg = 5200 J/kg·K⁻¹,
Cp_b = 4100 J/kg·K⁻¹, T_b = 390 K, T_w = 420 K, T_pc = 400 K, Di = 0.016 m,
x = 2 m, H_b = 1.6·10⁶ J/kg, G = 1400 kg/m²·s⁻¹, q = 650 kW/m²), once with
`corr = 0` and once with `corr = 1`. A third case *C* then calls the six branches
of the non-smooth switches that cases A and B do not take, with only the
temperature or the enthalpy that selects the branch changed (see the table
above the figure placeholder). The file solves without any iteration
(`Solver: SUCCESS (0 iterations)`, every equation is explicit) and is the
regression baseline (`supercritical_internal_nu.sol`).

Until CoolSolve supports `$INCLUDE library:…` for functions
(`CS-FEAT-IMPORT`), a model that needs these correlations copies their
definitions in a block `{--- Library functions copied from CSL-0104 ---}` and
lists `CSL-0104` in its `related` field.

## Results

Values of the demonstration program (full precision in
`supercritical_internal_nu.sol`), Nusselt numbers `[−]`:

| Correlation (`corr` = 1 applies the corrections) | A, `corr` = 0 | A, `corr` = 1 | B, `corr` = 0 | B, `corr` = 1 |
|---|---:|---:|---:|---:|
| `Nu_McAdams` | 261.38 | — | 844.27 | — |
| `Nu_Shitsman` | 266.12 | — | 1152.86 | — |
| `Nu_Griem` | 275.48 | 225.90 | 947.28 | 827.92 |
| `Nu_Jackson` | 252.37 | 264.07 | 896.73 | 1116.37 |
| `Nu_Gupta` | 189.79 | 186.20 | 922.68 | 888.19 |
| `Nu_Swenson` | 211.52 | 217.93 | 914.39 | 1004.18 |
| `Nu_Xu` | 293.96 | 289.13 | 1404.18 | 1403.78 |
| `Nu_Mokry` | 228.82 | 246.12 | 1020.56 | 1282.79 |
| `Nu_Bringer_Smith` | 208.18 | — | 726.33 | — |
| `Nu_Ornatsky` | 266.12 | 276.64 | 1152.86 | 1301.98 |
| `Nu_Gorban` | 182.54 | — | 449.27 | — |
| `Nu_Zhu` | 241.21 | 240.15 | 1029.49 | 1167.85 |
| `Nu_Bishop` | 246.10 | 265.36 | 1073.74 | 1302.80 |
| `Nu_Yamagata` | 283.94 | 292.35 | 1299.52 | 913.96 |
| `Nu_Kitoh` | 302.50 | 331.80 | 1277.09 | 823.51 |
| `Nu_Krasnoshchekov_Protopopov` | 234.83 | 228.85 | 886.91 | 960.13 |
| `Nu_Petukhov` | 248.01 | 254.83 | 927.69 | 1009.27 |
| `Nu_Krasnoshchekov` | 234.83 | 245.75 | 886.91 | 1103.88 |

Case *C* of the demonstration program calls the six branches of the non-smooth
switches that cases A and B do not take, with only the argument that selects the
branch changed (Nu `[−]`):

| Output | Branch exercised | Nu |
|---|---|---:|
| `Nu_Griem_w1_C` | w = 0.82, H_b < 1540 kJ/kg | 776.77 |
| `Nu_Jackson_n1_C` | n = 0.4 for T_b < T_w < T_pc (380 < 390 < 400 K) | 1113.72 |
| `Nu_Jackson_n2_C` | n = 0.4 for 1.2·T_pc < T_b < T_w (480 < 500 < 600 K) | 1113.72 |
| `Nu_Krasnoshchekov_n0p4_C` | n = 0.4 for T_b < T_w < T_pc | 1101.52 |
| `Nu_Krasnoshchekov_n3_C` | n = n₁ + (5n₁−2)·(1−T_b/T_pc) for T_w/T_pc > 2.5 | 1209.58 |
| `Nu_Yamagata_F1_C` | F = 1 for (T_pc−T_b)/(T_w−T_b) ≥ 1 | 1299.52 |
| `Nu_Kitoh_fc3_C` | f_c = −9.7·10⁻⁷ + 1.3/q_dht for H_b > 3300 kJ/kg | 1289.18 |

The regimes of the two first cases are, for the wall temperature, **above** the
pseudo-critical temperature (700 K > 600 K in A, 420 K > 400 K in B). Case A
therefore takes the last branch of `Nu_Jackson` (n = 0.4194) and of
`Nu_Krasnoshchekov` (n = n₁ = 0.43) and the E < 0 branch of `Nu_Yamagata`
(F from n₂), case B the `T_b < T_pc < T_w` branch of `Nu_Jackson` (n = 0.41),
the n₁ branch of `Nu_Krasnoshchekov` (n = 0.409) and the 0 ≤ E < 1 branch of
`Nu_Yamagata` (E = 0.333, F from n₁), whose factor is below 1 — that is why
`Nu_Yamagata_corr_B` (913.96) is smaller than its bare form (1299.52).
`Nu_Yamagata_F1_C` returns exactly the bare value, as it must: the branch it
takes sets F = 1. `Nu_Kitoh`'s enthalpy correction lowers Nu in case B
(H_b = 1.6 MJ/kg is in its middle branch, where f_c is negative) and raises it
in the two other branches (H_b = 1.3 and 3.6 MJ/kg), as `ht` gives.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the correlations
     over a bulk-temperature sweep at the pseudo-critical point, e.g. Nu vs T_b/T_pc
     at Re = 3E5 for the four wall-property ratios, figures/supercritical_internal_nu_nu_t.png -->

## Verification

Reference: the **doctest values published in the docstrings of `ht` 1.2.0**
(`ht/conv_supercritical.py`, commit `85e0ee6`, installed from the local clone in
a throw-away virtual environment) for case *A*, plus values computed with the
same Python functions for cases *B* and *C*. The 71 output values of the
demonstration program were compared with `CoolSolve/tools/compare_solution.py`
(tolerance `rtol = 0.001`):

```
71 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 48
```

(the 48 “only in CoolSolve” variables are the 48 inputs of the demonstration
program — `Re_A` … `Cp_b_P_B` and their `_B` counterparts —; the reference
table holds only the 71 outputs). The largest relative deviation over the 71
values is **4.4·10⁻¹³** (`Nu_Zhu_B`), i.e. round-off in the double-precision
evaluation.

| Output | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| Output | `ht` | CoolSolve | rel. dev. |
|---|---:|---:|---:|
| `Nu_McAdams_A` | 261.383863 | 261.383863 | 5.6e-14 |
| `Nu_Shitsman_A` | 266.117131 | 266.117131 | 9.5e-14 |
| `Nu_Griem_A` | 275.481858 | 275.481858 | 1.7e-13 |
| `Nu_Griem_corr_A` | 225.895123 | 225.895123 | 1.9e-13 |
| `Nu_Jackson_A` | 252.372316 | 252.372316 | 1.9e-13 |
| `Nu_Jackson_corr_A` | 264.070286 | 264.070286 | 1.9e-13 |
| `Nu_Gupta_A` | 189.787277 | 189.787277 | 1.2e-13 |
| `Nu_Gupta_corr_A` | 186.201355 | 186.201355 | 2.6e-13 |
| `Nu_Swenson_A` | 211.519684 | 211.519684 | 1.3e-13 |
| `Nu_Swenson_corr_A` | 217.928270 | 217.928270 | 1.7e-13 |
| `Nu_Xu_A` | 293.957251 | 293.957251 | 1.0e-13 |
| `Nu_Xu_corr_A` | 289.133054 | 289.133054 | 1.5e-13 |
| `Nu_Mokry_A` | 228.817801 | 228.817801 | 1.9e-13 |
| `Nu_Mokry_corr_A` | 246.115632 | 246.115632 | 3.1e-15 |
| `Nu_Bringer_Smith_A` | 208.176318 | 208.176318 | 4.3e-14 |
| `Nu_Ornatsky_A` | 266.117131 | 266.117131 | 9.5e-14 |
| `Nu_Ornatsky_corr_A` | 276.635312 | 276.635312 | 8.3e-14 |
| `Nu_Gorban_A` | 182.536728 | 182.536728 | 6.2e-16 |
| `Nu_Zhu_A` | 241.208772 | 241.208772 | 8.7e-15 |
| `Nu_Zhu_corr_A` | 240.145985 | 240.145985 | 1.2e-13 |
| `Nu_Bishop_A` | 246.098356 | 246.098356 | 9.8e-15 |
| `Nu_Bishop_corr_A` | 265.362005 | 265.362005 | 1.8e-13 |
| `Nu_Yamagata_A` | 283.938369 | 283.938369 | 1.2e-14 |
| `Nu_Yamagata_corr_A` | 292.347343 | 292.347343 | 1.1e-13 |
| `Nu_Kitoh_A` | 302.500655 | 302.500655 | 9.1e-14 |
| `Nu_Kitoh_corr_A` | 331.802341 | 331.802341 | 3.9e-14 |
| `Nu_Krasnoshchekov_Protopopov_A` | 234.828552 | 234.828552 | 1.5e-14 |
| `Nu_Krasnoshchekov_Protopopov_corr_A` | 228.852967 | 228.852967 | 9.7e-15 |
| `Nu_Petukhov_A` | 248.009141 | 248.009141 | 1.7e-13 |
| `Nu_Petukhov_corr_A` | 254.825860 | 254.825860 | 1.0e-13 |
| `Nu_Krasnoshchekov_A` | 234.828552 | 234.828552 | 1.5e-14 |
| `Nu_Krasnoshchekov_corr_A` | 245.753816 | 245.753816 | 1.0e-13 |
| `Nu_McAdams_B` | 844.265963 | 844.265963 | 4.0e-14 |
| `Nu_Shitsman_B` | 1152.860732 | 1152.860732 | 1.2e-14 |
| `Nu_Griem_B` | 947.282052 | 947.282052 | 3.0e-14 |
| `Nu_Griem_corr_B` | 827.924513 | 827.924513 | 2.3e-14 |
| `Nu_Jackson_B` | 896.727571 | 896.727571 | 4.3e-15 |
| `Nu_Jackson_corr_B` | 1116.369314 | 1116.369314 | 2.7e-13 |
| `Nu_Gupta_B` | 922.678787 | 922.678787 | 1.3e-14 |
| `Nu_Gupta_corr_B` | 888.185814 | 888.185814 | 4.5e-15 |
| `Nu_Swenson_B` | 914.392866 | 914.392866 | 5.2e-14 |
| `Nu_Swenson_corr_B` | 1004.176167 | 1004.176167 | 2.6e-13 |
| `Nu_Xu_B` | 1404.180338 | 1404.180338 | 5.5e-15 |
| `Nu_Xu_corr_B` | 1403.781822 | 1403.781822 | 1.3e-13 |
| `Nu_Mokry_B` | 1020.559701 | 1020.559701 | 1.2e-13 |
| `Nu_Mokry_corr_B` | 1282.785037 | 1282.785037 | 1.1e-13 |
| `Nu_Bringer_Smith_B` | 726.326697 | 726.326697 | 2.2e-14 |
| `Nu_Ornatsky_B` | 1152.860732 | 1152.860732 | 1.2e-14 |
| `Nu_Ornatsky_corr_B` | 1301.979735 | 1301.979735 | 1.3e-14 |
| `Nu_Gorban_B` | 449.270952 | 449.270952 | 2.2e-14 |
| `Nu_Zhu_B` | 1029.485532 | 1029.485532 | 4.4e-13 |
| `Nu_Zhu_corr_B` | 1167.852977 | 1167.852977 | 2.6e-13 |
| `Nu_Bishop_B` | 1073.738748 | 1073.738748 | 2.1e-13 |
| `Nu_Bishop_corr_B` | 1302.798597 | 1302.798597 | 2.1e-13 |
| `Nu_Yamagata_B` | 1299.523567 | 1299.523567 | 7.4e-14 |
| `Nu_Yamagata_corr_B` | 913.963893 | 913.963893 | 2.3e-14 |
| `Nu_Kitoh_B` | 1277.094197 | 1277.094197 | 1.5e-13 |
| `Nu_Kitoh_corr_B` | 823.514761 | 823.514761 | 4.1e-14 |
| `Nu_Krasnoshchekov_Protopopov_B` | 886.907062 | 886.907062 | 3.9e-14 |
| `Nu_Krasnoshchekov_Protopopov_corr_B` | 960.134714 | 960.134714 | 1.5e-14 |
| `Nu_Petukhov_B` | 927.692461 | 927.692461 | 5.3e-15 |
| `Nu_Petukhov_corr_B` | 1009.268903 | 1009.268903 | 3.1e-13 |
| `Nu_Krasnoshchekov_B` | 886.907062 | 886.907062 | 3.9e-14 |
| `Nu_Krasnoshchekov_corr_B` | 1103.881006 | 1103.881006 | 2.8e-13 |
| `Nu_Griem_w1_C` | 776.771283 | 776.771283 | 1.8e-15 |
| `Nu_Jackson_n1_C` | 1113.719171 | 1113.719171 | 8.7e-14 |
| `Nu_Jackson_n2_C` | 1113.719171 | 1113.719171 | 8.7e-14 |
| `Nu_Krasnoshchekov_n0p4_C` | 1101.522279 | 1101.522279 | 3.8e-13 |
| `Nu_Krasnoshchekov_n3_C` | 1209.583790 | 1209.583790 | 5.9e-14 |
| `Nu_Yamagata_F1_C` | 1299.523567 | 1299.523567 | 7.4e-14 |
| `Nu_Kitoh_fc3_C` | 1289.181926 | 1289.181926 | 2.4e-13 |

## Source and attribution

This CoolSolve model is a translation (into the EES-compatible language
CoolSolve reads) of the near-supercritical internal-convection correlations of
`ht`, the heat-transfer component of ChEDL, file `ht/conv_supercritical.py`,
functions `Nu_McAdams`, `Nu_Shitsman`, `Nu_Griem`, `Nu_Jackson`, `Nu_Gupta`,
`Nu_Swenson`, `Nu_Xu`, `Nu_Mokry`, `Nu_Bringer_Smith`, `Nu_Ornatsky`,
`Nu_Gorban`, `Nu_Zhu`, `Nu_Bishop`, `Nu_Yamagata`, `Nu_Kitoh`,
`Nu_Krasnoshchekov_Protopopov`, `Nu_Petukhov` and `Nu_Krasnoshchekov`,
version 1.2.0, commit 85e0ee6 (2025-12-07).

> ht - https://github.com/CalebBell/ht - "Copyright (C) 2016, Caleb Bell",
> MIT License.
> Please cite: Caleb Bell and Contributors (2016-2025). ht: Heat transfer
> component of Chemical Engineering Design Library (ChEDL),
> https://github.com/CalebBell/ht.

Changes: translated from Python to CoolSolve; every correlation became one EES
`FUNCTION` named after the `ht` function; the Python `log10` became the EES
`LOG10`, the Python `min` the EES `MIN`, the optional arguments became
mandatory plus the `corr` flag; the regime-dependent exponents of `Nu_Jackson`,
`Nu_Yamagata`, `Nu_Krasnoshchekov` and the enthalpy-dependent `w` of `Nu_Griem`
and `m` of `Nu_Kitoh` were written with nested block `IF` statements; the
product of the optional correction factors is a local variable `F` (or `f` for
the friction factor of `Nu_Petukhov`). No equation was changed. Scientific basis
per function: the original paper or book quoted in its comment block.

The scientific authors of the correlations are credited in the comment block of
each function and in `model.json` (`origin.authors`).

## Conversion log

- **2026-10-06 — translation (T-FUNC card C-113, family `HT-018`).** One EES
  `FUNCTION` per `ht` correlation (18 functions), named `Nu_<method>`, with the
  formula, the data range as quoted by `ht`, the original reference and the `ht`
  module/function/version/commit in the comment block. Arguments are the Python
  arguments in SI (`kg/m³`, `Pa·s`, `W/m·K⁻¹`, `J/kg·K⁻¹`, `K`, `J/kg`,
  `kg/m²·s⁻¹`, `W/m²`, `m`); **no property function is used inside a function**,
  so the calling model passes Re, Pr and the wall/bulk property values itself
  (rule 5 of `sources/ht/README.md` §7). No unit conversion was needed: `ht` is
  written in SI.
- The optional arguments of the Python functions (the property ratios, the
  temperatures, the enthalpy, the mass and heat fluxes) became mandatory
  arguments followed by the integer flag `corr`: `corr = 1` applies the
  corrections, `corr = 0` returns the bare correlation, i.e. the value `ht`
  returns when those arguments are `None`. This follows the pattern of `CSL-0087`
  (the 1/0 flags of `Nu_Dittus_Boelter`) and is logged as a decision of this
  card. Both calls are exercised in the demonstration program.
- The regime switches are **nested block** `IF/THEN/ELSE/ENDIF` statements (one
  `ENDIF` per `IF`), not `ELSE IF` ladders and not single-line `IF`s: the
  ladder form is `CS-GAP-ELSEIF-CHAIN` and the single-line form inside a
  function body is `CS-BUG-IF-SINGLELINE` in the CoolSolve register. The
  conditions of the Python code were translated one by one, including its
  boundary values (`E < 0` / `E < 1`, `H < 1.5E6` / `H <= 3.3E6`,
  `1 < T_w/T_pc < 2.5`), so each branch is taken exactly as in `ht`.
- `Nu_Petukhov`: the friction factor `f` is a local variable; `fd` is kept as
  the smooth-pipe friction factor of the formula `[1.82·LOG10(Re)−1.64]^(−2)`
  and `corr = 1` multiplies it by the density and viscosity ratios, as in `ht`.
- `Nu_Krasnoshchekov` and `Nu_Krasnoshchekov_Protopopov` keep `Nu_0` and `fd` as
  local variables, as `ht` computes them internally.
- **No selector** in this `ht` module: all 18 public functions are translated.
- **Level**: equations 112 → 1 point (50–300), largest block 1 → 0, functions
  present → 1, multi-zone no → 0, semi-empirical/off-design no → 0, curated
  guesses no → 0. Score 2 → **level 2** (same scoring as `CSL-0087`).

## Limitations and CoolSolve gaps

- All eighteen correlations are for **turbulent vertical upward** flow and were
  fitted on **water near its critical point** (P = 20–32 MPa); the transport
  property *ratios* and the heat-capacity ratio are what makes them applicable
  to another fluid (sCO₂), but the fitted coefficients were not re-fitted for
  it. `ht` notes in particular that `Nu_Kitoh` does not behave realistically
  outside the range of its own data and should not be used there, and that
  `Nu_Gorban` is not recommended (`ht` ranks it last of the fourteen
  correlations it assessed). Both are kept for completeness, with the note in
  their comment block.
- The two enthalpy arguments `H_b` of `Nu_Griem` (branches at 1540 and
  1740 kJ/kg, 1967 IFC reference point for water) and `Nu_Kitoh` (branches at
  1500 and 3300 kJ/kg, reference point not stated in the original) are
  **water-specific**; for another fluid their branches must be used with care.
- The demonstration input sets are realistic rather than staying inside every
  quoted data range (case A is the `ht` doctest set, which is outside the range
  of e.g. `Nu_Kitoh`, developed for G = 100–1750 kg/m²/s while its doctest uses
  G = 1500 kg/m²/s and q = 5 MW/m² against 0–1800 kW/m²; case B is a
  second-supercritical-like set with CO₂-like property values). The numbers of
  the *Results* and *Verification* tables check the **equations**, not
  recommended design values; the validity column of the table above is the one
  to use when choosing an input.
- CoolSolve cannot yet import the functions of a library file with
  `$INCLUDE library:…` (`CS-FEAT-IMPORT`, planned): a model that uses these
  correlations copies the definitions for now.
- No gap registered for this card: everything is plain EES (`FUNCTION`,
  nested `IF/THEN/ELSE/ENDIF`, `MIN`, `LOG10`) and runs in CoolSolve v0.3.0.

## Related models

- `CSL-0087` *internal_turbulent_nusselt*: the single-phase turbulent
  in-pipe Nusselt correlations of the same `ht` triage and the same layout;
  they apply to the part of the supercritical tube wall that stays below the
  pseudo-critical temperature and are written out in the bodies of several of
  the correlations of this file (Dittus-Boelter in `Nu_McAdams`, Gnielinski in
  `Nu_Krasnoshchekov`).
- `CSL-0038` *orc_co2_polynomial_maps*: a transcritical CO₂ power cycle whose
  evaporator and condenser cross the pseudo-critical point of R744; it is the
  kind of model that calls the functions of this file for the near-supercritical
  branches of its heat exchangers.