# Pseudo-critical temperature and pseudo-boiling bounds of supercritical fluids (function library)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0317`

Three EES routines for the pseudo-critical point of a fluid above its critical pressure:
`T_pc_cpmax` finds the pseudo-critical temperature as the temperature of maximum isobaric
specific heat, `PseudoBoilingBounds` returns the temperatures `T_minus` and `T_plus` that
bound the pseudo-boiling transition in Banuti's linear model, and `T_pc_CO2_Yang` is the
empirical CO2 polynomial of `T_pc` against pressure. They supply the `T_pc` that the
near-supercritical Nusselt correlations of `CSL-0104` and the sCO2 / transcritical-CO2 cycle
models take as an input, and they are a small reusable utility for any model that crosses the
pseudo-critical line.

| | |
|---|---|
| **Category** | Fundamentals › Properties |
| **Fluids** | any CoolProp fluid (demonstrated: R744 (CO2), Water, R134a, Propane) |
| **Size** | 52 equations (largest block: 2) |
| **Source** | LaboThapPy `labothappy/correlations/properties/supercritical.py`, commit f03f7f47 |
| **Authors** | Elise Neven (LaboThapPy, ULiège Thermodynamics Laboratory) |
| **License** | MIT (translation); original Apache-2.0 |
| **CoolSolve** | 0.4.0@9768373 — verified against a re-run of the Python source (max abs 3.1e-06 K) |

## Niche

No library model computes a pseudo-critical temperature: `CSL-0104` takes `T_pc` as an
argument, and the sCO2 cycles (`CSL-0144`, `CSL-0038`) never need it. This model adds
(i) a fluid-general cp-maximum search, (ii) Banuti's pseudo-boiling bounds, which exist in no
other library model, and (iii) the Yang & Yang CO2 correlation. Nearest model: `CSL-0104`
(its consumer, not an overlap).

## Model

All temperatures are in °C and pressures in Pa; the original works in K and the translation
converts inside the routines (the bounds formulas need absolute temperatures).

**`T_pc_cpmax(fluid$, P)`** as in the original: the isobar at `P` is scanned on 500 equally spaced
temperatures from `0.9 T_crit` to `1.3 T_crit` (`numpy.linspace`), `cp` is evaluated at each point and the
temperature of the first maximum is returned. The result is therefore a grid value, with a resolution of
`0.4 T_crit/499` (0.24 K for CO2); the original has the same resolution. The scan is a `REPEAT ... UNTIL` loop in the function body.

**`PseudoBoilingBounds(fluid$, P, T_pc, T_max : T_minus, T_plus)`** follows the original
(reference Banuti, *The Latent Heat of Supercritical Fluids*, Period. Polytech. Chem. Eng. 63(2), 2019, 270-275; only taken from the source
docstring, the paper was not consulted). With `cp_pc`, `h_pc` the specific heat and enthalpy at `(P, T_pc)`,
`cp_L`, `h_L` the liquid values at `P_L` and `T_L - 0.01 K` (`T_L = T_sat(P_L)`, `P_L = 0.1 P_crit`, or `1.05 P_triple` when that
is lower) and `cp_IG` the specific heat at `(P, T_max)`, with absolute temperatures:

$$T_+ = \frac{h_{pc} - c_{p,pc}T_{pc}}{c_{p,IG}-c_{p,pc}},\qquad
T_- = \frac{h_{L,0} - h_{pc} + c_{p,pc}T_{pc}}{c_{p,pc}-c_{p,L}},\qquad h_{L,0}=h_L-c_{p,L}T_L$$

Differences with the original signature (logged below): `T_pc` and `T_max` are inputs and
the routine does not search or read them; the original has an optional `T_pc_func`
and reads `T_max` from CoolProp. `T_max` is not available as a CoolSolve function, so the demonstration passes the
CoolProp values.

**`T_pc_CO2_Yang(P)`**: $T_{pc} = -31.40 + 12.15p - 0.6927p^2 + 0.03160p^3 - 0.0007521p^4$ in °C with
`p` in MPa, stated valid for 7.5-14 MPa (Yang & Yang 2012, as cited by the original; the paper was not
consulted). The original returns K (adds 273.15).

## How to run

```
coolsolve pseudo_critical_properties.eescode
```
The demonstration program is at the end of the file: ten pressure/fluid cases (`T_pc_<i>`, `T_minus_<i>`, `T_plus_<i>`)
and the CO2 correlation at three pressures with the bounds computed from it (`T_pcc_<j>`, `T_minusc_<j>`, `T_plusc_<j>`).
The file solves in 24 iterations (about 2 s, 500 property calls per `T_pc_cpmax`). CoolSolve prints the cosmetic warning
`Unknown function 'P_triple'` while evaluating it correctly (see Limitations).
To use the functions from another model, include the file (`CS-FEAT-IMPORT`).

## Results

Selected demonstration results (°C):

| Case | P [MPa] | Fluid | T_minus | T_pc | T_plus |
|---|---:|---|---:|---:|---:|
| 1 | 7.5 | R744 | 31.020 | 31.771 | 32.342 |
| 2 | 8 | R744 | 32.236 | 34.696 | 37.077 |
| 3 | 10 | R744 | 33.948 | 44.935 | 58.274 |
| 4 | 14 | R744 | 35.849 | 61.269 | 101.860 |
| 5 | 20 | R744 | 39.260 | 75.897 | 168.840 |
| 6 | 25 | Water | 378.608 | 384.969 | 381.386 |
| 7 | 30 | Water | 383.006 | 402.086 | 391.353 |
| 8 | 5 | R134a | 102.328 | 111.936 | 134.539 |
| 9 | 6 | Propane | 96.273 | 117.273 | 255.651 |

For water `T_plus` is below `T_pc` (it is so in the original too: 654.54 K against 658.12 K at 25 MPa), so the three
temperatures are not always ordered `T_minus < T_pc < T_plus`; for the other cases they are. The
Yang correlation gives 31.712, 44.909 and 60.749 °C at 7.5, 10 and 14 MPa, below the cp-maximum values by 0.058,
0.026 and 0.521 K; the bounds computed from it differ from those of cases 1, 3 and 4 by 0.33 K (`T_minus`) and 0.27 K (`T_plus`) at
7.5 MPa, 0.002 K at 10 MPa and less than 0.03 K at 14 MPa.

## Verification

Reference: LaboThapPy commit f03f7f47 installed in a throw-away virtual environment (CoolProp 8.0.0), calling
`pseudo_critical_temperature`, `pseudo_boiling_bounds` (with and without `T_pc_func=pseudo_critical_temperature_CO2`) and
`pseudo_critical_temperature_CO2` on the demonstration cases; its values (K) converted to °C
were compared with `pseudo_critical_properties.sol` using `tools/compare_solution.py ... --rtol 1e-6`:
36 common variables, 0 differ at rtol=1e-06; at rtol=1e-09 two differ, `T_minus_2` (9.47e-08)
and `T_plus_2` (8.32e-08), the largest relative differences (3.05e-06 K and 3.08e-06 K absolute; not investigated, the case is at 8 MPa, near the critical pressure
where cp is steep). All other values agree within 1.5e-08 K (`T_pc` within 4.4e-11 K). The three
`T_pc_CO2_Yang` values agree to 1e-14 K.
A second set of ten cases outside the shipped file (Nitrogen 5 MPa, Ethane 8 MPa, CO2 12 and 30 MPa, R134a 8 MPa, Water 40 MPa, Methane 10 MPa, Propane 10 MPa, R245fa 6 MPa; CoolProp `T_max` passed)
gave a largest absolute difference of 1.2e-05 K (Nitrogen, `T_plus`); all temperatures agree to better than 1e-4 K.
The Python run used CoolProp 8.0.0, the CoolSolve build links CoolProp 8.1.0dev (revision 75af7816); the small differences were not traced to a cause. The comparison scripts lived in `work/` and were deleted. The bounds depend on absolute enthalpies and
agree, so the enthalpy reference state of CoolSolve and of the Python run is the same.

The original's own docstring gives no published values; nothing was compared with the Banuti or Yang papers.

## Source and attribution

Translated from LaboThapPy (PyLaboThap, ULiège), file `labothappy/correlations/properties/supercritical.py`,
commit `f03f7f473b190d0c0b5e296132b50565e89e4421`, https://github.com/PyLaboThap/LaboThapPy, Apache License 2.0 (`LICENSE.txt`).
The file history names one author, Elise Neven (2026-09-02). References cited by the original: D. Banuti, *The
Latent Heat of Supercritical Fluids*, Periodica Polytechnica Chemical Engineering 63(2), 2019, 270-275; Z. Yang and J. Yang,
*Investigation on the Properties of Supercritical CO2 Fluid and its Heat Transfer Characteristics* (2012). The translation
is published under the library licence (decision D3).

## Conversion log

- **2026-10-31 — translation (T-FUNC, card C-365)**: `pseudo_critical_temperature` -> `T_pc_cpmax` (the numpy grid and `argmax` become a
  `REPEAT` loop with a strict `>`, first maximum kept); `pseudo_boiling_bounds` -> `PseudoBoilingBounds`;
  `pseudo_critical_temperature_CO2` -> `T_pc_CO2_Yang`. Fluid `'CO2'` -> `'R744'` (bare `CO2` is the ideal-gas species in EES).
- Units: K -> °C at the routine interface; the formulas use `T + 273.15` internally.
- `T_pc_func` removed: the caller passes `T_pc`, which can come from either of the other routines. `PseudoBoilingBounds`
  is a PROCEDURE (two outputs).
- `T_max` (CoolProp `iT_max`) is an input of the procedure: no CoolSolve function returns it. Demonstration values
  (K) read with `CoolProp.PropsSI('Tmax', fluid)`: CO2 2000, Water 2000, R134a 455, Propane 650.
- `T_L` is the saturation temperature at `P_L` (`T_sat`), as `AS.update(PQ_INPUTS, P_L, 0)` then `AS.T()`.
- The Python case R1233zd(E) at 5 MPa was dropped from the demonstration: its CoolProp `T_max` (450 K) is below `T_pc` (460.76 K),
  and the original returns `T_plus` = 1145.58 K there.
- **Level**: function library, 3 routines, loop and property calls in the bodies, no coupled equations -> level 2.

## Limitations and CoolSolve gaps

- The cp-maximum search is a grid scan of the original (0.24 K resolution for CO2) and does not refine the maximum; far above the critical
  pressure the maximum of cp is broad and the pseudo-critical line less meaningful, which the original does not treat.
- `T_plus` depends on `cp_IG` read at `T_max`: for light or heavy fluids the value is far from the pseudo-critical
  region (propane at 10 MPa: 998.7 °C; the original returns 1271.9 K), and a `T_max` below `T_pc` gives nonsense.
- The Yang correlation is stated for 7.5-14 MPa only; the function does not check the range.
- CoolSolve prints `Unknown function 'P_triple'` at parse time but evaluates it (checked: `a = P_triple('R744')` gives 517 964 Pa).
  `T_triple` is documented in `docs/ees_vs_coolsolve.csv`, `P_triple` is not in the parser's list of built-ins. Cosmetic; not registered
  here because no EES evidence for the function name was found (unverified suggestion).
- No gap blocks the model (`missing_features` empty).

## Related models

- `CSL-0104` *supercritical_internal_nu*: Nusselt correlations that take `T_pc` as argument; this file provides it.
- `CSL-0144` *sco2_recompression_brayton*: an sCO2 cycle whose main compressor inlet (35 °C, 75 bar) is close to the pseudo-critical temperature computed here for 7.5 MPa (case 1: 31.77 °C).
