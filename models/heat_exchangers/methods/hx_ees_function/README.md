# Heat exchangers: the EES HX function

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0332`

The **`HX` function of the EES heat exchanger library**, as an ordinary library function. EES
models compute the effectiveness or the number of transfer units of a heat exchanger with

```ees
epsilon = HX(TypeHX$, NTU, C_dot_1, C_dot_2, 'epsilon')
NTU     = HX(TypeHX$, epsilon, C_dot_1, C_dot_2, 'NTU')
```

where `NTU = UA/C_dot_min` and `C_dot_1`, `C_dot_2` `[W/K]` are the heat capacity rates of the two
streams. CoolSolve has no such built-in: a model that calls `HX` runs unchanged with one more line,

```ees
$INCLUDE hx_ees_function
```

which imports the functions of this file (its demonstration program is ignored). The code of the
function is therefore readable library code, not hidden in the solver.

| | |
|---|---|
| **Category** | Heat exchangers › Methods |
| **Fluids** | none (the relations are fluid-independent) |
| **Size** | 5 functions; the demonstration program has 38 equations, all explicit |
| **Source** | the interface, flow types and worked examples of the [EES HX function](https://fchartsoftware.com/ees/heat_transfer_library/heat_exchangers/hs1000.htm) (F-Chart Software); the relations of `CSL-0090` and `CSL-0102` (from `ht` 1.2.0), included, and the published relations cited in the code |
| **License** | MIT |
| **CoolSolve** | 0.4.0 with `$INCLUDE` — **verified** against the 33 worked examples of the EES help |

## Problem statement

The effectiveness-NTU method relates the effectiveness ε = Q̇ / (Ċ_min·(T_h,in − T_c,in)) of a heat
exchanger to `NTU = UA/Ċ_min` and `Cr = Ċ_min/Ċ_max`, through a relation that depends on the flow
arrangement. EES gathers the arrangements behind one function whose first argument names the
arrangement and whose last argument says whether ε or NTU is returned. The models of the EES
course material and of the ULiège toolkits call it directly, e.g. the cooling-tower identification
model `CSL-0286`:

```ees
epsilon_ct = HX('counterflow', NTU_ct, C_dot_af_ct, C_dot_fl_ct, 'epsilon')
```

## Model

`TypeHX$` (case ignored), as in EES:

| `TypeHX$` | Arrangement | `C_dot_1` | Relation |
|---|---|---|---|
| `parallelflow`, `counterflow` | double pipe | any | `eps_parallel`, `eps_counterflow` of `CSL-0090` |
| `crossflow_both_unmixed` | single-pass crossflow | any | approximate closed form `eps_crossflow_approx` (`CSL-0090`, as Nellis and Klein) |
| `crossflow_both_mixed` | single-pass crossflow | any | ε = [1/(1−e^−NTU) + Cr/(1−e^−Cr·NTU) − 1/NTU]^−1 |
| `crossflow_one_unmixed` | single-pass crossflow | the unmixed stream | `eps_crossflow_mixed_Cmax` (stream 1 is Ċ_min) or `eps_crossflow_mixed_Cmin` |
| `shell&tube_N`, N = 1…9 | N shell passes, 2N, 4N… tube passes | any | one 1-2 TEMA E shell (`temperature_effectiveness_TEMA_E` of `CSL-0102`) with NTU/N, combined in series |
| `12TEMAE_2shellsidestreams`, `13TEMAE`, `11TEMAG`, `12TEMAG`, `11TEMAH`, `12TEMAH`, `11TEMAJ`, `12TEMAJ`, `14TEMAJ` | TEMA shells | the shell side | the P-NTU relations of `CSL-0102` for stream 1: R1 = Ċ_1/Ċ_2, NTU1 = NTU·Ċ_min/Ċ_1, ε = P1·Ċ_1/Ċ_min |
| `regenerator` | balanced counterflow regenerator | the stream (`C_dot_2`: matrix heat capacity / blow period) | Lambertson, Kays and London: ε = NTU_o/(1+NTU_o)·(1 − 1/(9·Cr*^1.93)), NTU_o = NTU/2, Cr* = Ċ_2/Ċ_1 |

`Return$ = 'NTU'` uses the closed inverse where one exists (parallel flow, counterflow, crossflow with one
fluid unmixed, N shell passes) and otherwise a numerical inversion (`HX_NTU_numerical`): NTU is marched up
from 0.01 until ε is reached — so the lower NTU is returned when ε(NTU) is not monotonic, as EES does for
`crossflow_both_mixed` — the bracket is bisected, and a last Newton step gives the result the derivatives of
the implicit relation, so that `NTU = HX(…, 'NTU')` can sit in a simultaneous block of the calling model. As
in EES, `12TEMAJ`, `14TEMAJ` (ε is not monotonic in NTU) and `regenerator` cannot return NTU: the function
stops with an error that says so; write `epsilon = HX(…, 'epsilon')` and let the model solve for NTU.

The functions are `HX` (the dispatcher on `Return$`), `HX_epsilon`, `HX_NTU`, `HX_NTU_numerical` and
`HX_shell_passes`; the relations themselves come from `$INCLUDE hx_effectiveness_ntu` (`CSL-0090`) and
`$INCLUDE hx_temperature_effectiveness_pntu` (`CSL-0102`), so a model that includes this file also has the
functions of those two.

## How to run

In any model:

```ees
$INCLUDE hx_ees_function
C_dot_1 = 50 [W/K]
C_dot_2 = 30 [W/K]
UA = 75 [W/K]
epsilon = HX('counterflow', UA/MIN(C_dot_1, C_dot_2), C_dot_1, C_dot_2, 'epsilon')
```

The file itself runs as a model: its demonstration program evaluates the worked examples of the EES help, one
or two per type (`coolsolve hx_ees_function.eescode`, or *Open in CoolSolve*).

## Results

The demonstration program gives the values of the verification table below: e.g. ε = 0.8748 for the counterflow
exchanger of `UA` = 100 W/K, and NTU = 1.900 for ε = 0.74.

## Verification

Each page of the EES help on the heat exchanger library has two worked examples: ε for `UA` = 75 W/K,
`C_dot_1` = 50 W/K, `C_dot_2` = 30 W/K (NTU = 2.5), and NTU for ε = 0.61 with the same capacity rates; the
counterflow page uses `UA` = 100 W/K and ε = 0.74, the regenerator page `UA` = 600 W/K, `C_dot` = 50 W/K and a
matrix of 500 J/K over a 1 s blow. CoolSolve reproduces **all the printed digits of 32 of the 33 values**; the
deviations below are those of the 3 or 4 digits printed by EES.

| `TypeHX$` | Returns | CoolSolve | EES help | Rel. deviation |
|---|---|---|---|---|
| `parallelflow` | epsilon | 0.613553 | 0.6136 | 7.7e-05 |
| `parallelflow` | NTU | 2.331063 | 2.331 | 2.7e-05 |
| `crossflow_both_unmixed` | epsilon | 0.763225 | 0.7632 | 3.3e-05 |
| `crossflow_both_unmixed` | NTU | 1.340954 | 1.341 | 3.5e-05 |
| `crossflow_one_unmixed` | epsilon | 0.726043 | 0.726 | 5.9e-05 |
| `crossflow_one_unmixed` | NTU | 1.387215 | 1.387 | 1.6e-04 |
| `crossflow_both_mixed` | epsilon | 0.684109 | 0.6841 | 1.3e-05 |
| `crossflow_both_mixed` | NTU | 1.477771 | 1.478 | 1.6e-04 |
| `shell&tube_1` | epsilon | 0.689704 | 0.6897 | 6.4e-06 |
| `shell&tube_1` | NTU | 1.469725 | 1.470 | 1.9e-04 |
| `shell&tube_2` | epsilon | 0.775319 | 0.7753 | 2.4e-05 |
| `shell&tube_2` | NTU | 1.262959 | 1.263 | 3.3e-05 |
| `shell&tube_6` | epsilon | 0.806985 | 0.8070 | 1.8e-05 |
| `shell&tube_8` | NTU | 1.217569 | 1.218 | 3.5e-04 |
| `12TEMAE_2shellsidestreams` | epsilon | 0.727201 | 0.7272 | 2.0e-06 |
| `12TEMAE_2shellsidestreams` | NTU | 1.393322 | 1.393 | 2.3e-04 |
| `13TEMAE` | epsilon | 0.704127 | 0.7041 | 3.9e-05 |
| `13TEMAE` | NTU | 1.427012 | 1.427 | 8.3e-06 |
| `11TEMAG` | epsilon | 0.748204 | 0.7482 | 5.3e-06 |
| `11TEMAG` | NTU | 1.359589 | 1.360 | 3.0e-04 |
| `12TEMAG` | epsilon | 0.778356 | 0.7784 | 5.7e-05 |
| `12TEMAG` | NTU | 1.261402 | 1.261 | 3.2e-04 |
| `11TEMAH` | epsilon | 0.747914 | 0.7479 | 1.9e-05 |
| `11TEMAH` | NTU | 1.354194 | 1.354 | 1.4e-04 |
| `12TEMAH` | epsilon | 0.779270 | 0.7793 | 3.8e-05 |
| `12TEMAH` | NTU | 1.260698 | 1.261 | 2.4e-04 |
| `11TEMAJ` | epsilon | 0.727201 | 0.7272 | 2.0e-06 |
| `11TEMAJ` | NTU | 1.393322 | 1.393 | 2.3e-04 |
| `12TEMAJ` | epsilon | 0.682784 | 0.6828 | 2.4e-05 |
| `14TEMAJ` | epsilon | 0.684307 | 0.6843 | 9.8e-06 |
| `counterflow` | epsilon | 0.874752 | 0.8748 | 5.5e-05 |
| `counterflow` | NTU | 1.900217 | 1.9 | 1.1e-04 |
| `regenerator` | epsilon | 0.856024 | 0.8559 | 1.4e-04 |

The regenerator differs in the fourth digit: EES uses the relation of Dragutinović and Baclić, this file the
classical Lambertson / Kays and London correction (1.4·10⁻⁴). The numerical inversion is checked by the round trip
ε → NTU → ε: solving `2.5 = HX('crossflow_both_unmixed', e, 50, 30, 'NTU')` for `e` gives the ε of the table to
8·10⁻¹² (0 for `12TEMAG`). The native file of `CSL-0286` with `$INCLUDE hx_ees_function` gives the same solution
as its variant where the counterflow relation is written out (all 33 common variables equal).

## Source and attribution

- The interface (`TypeHX$` names, argument order, `C_dot_1` conventions), the list of flow types and the worked
  examples are those of the EES heat exchanger library documentation (F-Chart Software,
  <https://fchartsoftware.com/ees/heat_transfer_library/heat_exchangers/hs1000.htm> and the page of each type).
  The EES source code is not distributed and was not used: the relations are written from the publications.
- Relations of `CSL-0090` and `CSL-0102`: translated from `ht` 1.2.0 (Caleb Bell, MIT), see their READMEs.
- Both fluids mixed and N shell passes: Incropera, DeWitt, Bergman and Lavine, *Fundamentals of Heat and Mass
  Transfer*, 6th ed., Wiley, 2007, Tables 11.3 and 11.4; Nellis and Klein, *Heat Transfer*, Cambridge University
  Press, 2009, Tables 8-1 and 8-2.
- Regenerator: Kays and London, *Compact Heat Exchangers*, 3rd ed., McGraw-Hill, 1984.

## Conversion log

- 2026-11-04: written for the closure of the CoolSolve gap `CS-GAP-HX`: rather than a built-in of the solver,
  the EES function is library code that any model imports with `$INCLUDE` (CoolSolve `CS-FEAT-IMPORT`). The
  relations already in the library are included, not copied. The types are compared as strings (CoolSolve, like
  EES, ignores the case); `shell&tube_N` is matched for N = 1…9.

## Limitations and CoolSolve gaps

- `regenerator`: approximate relation (see Verification); no NTU from ε (as EES).
- `12TEMAJ`, `14TEMAJ`: no NTU from ε (as EES).
- `crossflow_both_unmixed` uses the approximate closed form, as the EES library (Nellis and Klein); the exact
  series is available as `crossflow_effectiveness_to_int` in `CSL-0090`.
- Needs a CoolSolve with `$INCLUDE` (0.4 and later development versions).

## Related models

- `CSL-0090` *hx_effectiveness_ntu* and `CSL-0102` *hx_temperature_effectiveness_pntu*: the relations used here.
- `CSL-0105` *lmtd_and_f_correction*: the LMTD method, the other way of rating a heat exchanger.
- `CSL-0286` *indirect_contact_tower_identification*: an EES model that calls `HX('counterflow', …)`.
