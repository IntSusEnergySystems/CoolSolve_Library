# Single-effect ammonia-water absorption cycle (ideal generator)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0347`

Performance of the simple ammonia-water absorption refrigeration cycle of the EES
example `Absorp.ees` at one operating point. The generator produces a saturated
refrigerant vapour (state 2) and a saturated weak solution (state 3) at 115 °C; the
refrigerant is condensed at 13.5 bar, throttled to 1.7 bar and evaporated at −1 °C;
the weak solution is cooled in a solution heat exchanger, throttled and absorbs the
refrigerant vapour at 27 °C. As in the original: no rectifier, pump work neglected,
no refrigerant heat exchanger, and the effectiveness of the solution heat exchanger
is an output. It is the simpler companion of the library's richer chiller
(`CSL-0249`), built from a published EES example.

| | |
|---|---|
| **Category** | Refrigeration and heat pumps › Absorption chillers |
| **Fluids** | NH3H2O |
| **Size** | 108 equations (largest block: 2) |
| **Source** | EES example `Absorp.ees` ([fchartsoftware.com](https://fchartsoftware.com/ees/examples/absorp.ees)); copy in the ULiège collection |
| **Authors** | S. A. Klein (University of Wisconsin-Madison / F-Chart Software) |
| **License** | MIT |
| **CoolSolve** | 0.4.0@cc582a6 — verified (see [Verification](#verification)) |

## Niche

The library had a detailed single-effect NH3-H2O chiller (`CSL-0249`, written for the
library, rectifier, pump work, refrigerant heat exchanger, prescribed heat-exchanger
effectiveness). This model adds the published EES teaching example of the same cycle
in its simplest form: component outlet states fixed by temperature and saturation,
the solution heat exchanger effectiveness computed from the cycle instead of
prescribed, and the ammonia mass fractions of both generator streams as outputs. It
also documents the two `NH3H2O` property backends (EES external routine vs IAPWS
G4-01) on a worked example.

## Model

One operating point of a single-effect NH3-H2O absorption cycle (states numbered as
in the original):

- **Generator** (13.5 bar): strong solution `m_dot_1` (x = 0.38, 80 °C at the inlet,
  heated by the solution heat exchanger) splits into saturated vapour (state 2, 115 °C,
  Q = 1) and saturated weak solution (state 3, 115 °C, Q = 0); overall, ammonia and
  energy balances give `m_dot_2`, `m_dot_3` and `Q_gen`.
- **Condenser**: the refrigerant leaves at 27 °C as a sub-cooled liquid (state 4).
- **Refrigerant throttle**: isenthalpic to 1.7 bar (state 5, two-phase).
- **Evaporator**: the refrigerant leaves at −1 °C (state 6, two-phase); `T_min` is the
  dew temperature of the refrigerant at the low pressure (as in the original).
- **Absorber**: vapour `m_dot_2` (state 6) + weak solution `m_dot_3` (state 10, after
  its isenthalpic expansion) form the strong solution (state 7, x = 0.38, 27 °C);
  energy balance gives `Q_abs`.
- **Solution heat exchanger** ("generator heat exchanger" in the original): the strong
  solution is pumped with the work neglected (`h_7 = h_8`) and heated to state 1 by the
  weak solution, which leaves at `h_e` (state 9) and is then throttled to the absorber
  (state 10, `h_10 = h_9`); `T_m_9` (state 9 at `T_7`) is the lowest reachable weak-solution
  temperature, and `epsilon = (h_3 − h_e)/(h_3 − h_m_9)` is the computed effectiveness.
- **Overall**: `COP = Q_evap/Q_gen` and the balance check `CheckQ`.

The property calls are the EES built-in `NH3H2O` fluid (ammonia mass fraction `x`,
IAPWS G4-01 in CoolSolve): the original called the `NH3H2O` **external procedure**
(input codes 123 = (T, P, x), 128 = (T, P, Q), 234 = (P, x, h), 238 = (P, x, Q)),
replaced by the built-in property calls that the source itself documents as the
alternative interface. Inputs: `P_high`, `P_low`, `m_dot_1`, `T_1`, `x_1` and the fixed
component temperatures (80/115/27/−1 °C). Outputs: compositions, mass flows, state
points, the four heat rates [W], `COP` [-], `epsilon` [-], and the state-point arrays
`P[i]`, `T[i]`, `x[i]`, `h[i]`, `s[i]` (i = 1…10) for the diagrams.

## How to run

```bash
coolsolve ./nh3h2o_absorption_ideal.eescode
```

No `.initials` needed: the system is almost fully explicit (largest block: 2
equations). No variants.

## Results

Main results, EES stored solution vs CoolSolve (this build):

| Quantity | EES | CoolSolve |
|---|---:|---:|
| `x_2` refrigerant vapour [kg/kg] | 0.90854 | 0.90585 |
| `x_3` weak solution [kg/kg] | 0.30737 | 0.29998 |
| `m_dot_2` [kg/s] | 0.12082 | 0.13207 |
| `m_dot_3` [kg/s] | 0.87918 | 0.86793 |
| `T_5` after refrigerant throttle [°C] | −20.29 | −19.87 |
| `T_9` weak solution at `h_e` [°C] | 54.93 | 55.85 |
| `T_min` dew temperature at 1.7 bar [°C] | 60.10 | 60.48 |
| `epsilon` [-] | 0.68943 | 0.68145 |
| `Q_gen` [W] | 336 883 | 356 075 |
| `Q_cond` [W] | 187 369 | 205 821 |
| `Q_evap` [W] | 108 469 | 118 005 |
| `Q_abs` [W] | 257 983 | 268 259 |
| `COP` [-] | 0.32198 | 0.33141 |
| `CheckQ` [W] | −0.012 | 2.9e-11 |

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): diagram or plot made in CoolSolve,
     saved in figures/, e.g.  ![P-h diagram of the cycle](figures/nh3h2o_absorption_ideal_ph.png)  + one-line caption -->

## Verification

Reference: the solution stored in the original `Absorp.ees` (EES 8.821), compared with
`compare_solution.py nh3h2o_absorption_ideal.sol reference/ees_variables.csv
--ees-units`. Its printed summary:

> 58 common variables, 40 differ (rtol=0.001); only in EES: 37; only in CoolSolve: 50

The 40 flagged differences fall in four explained groups (all values above converted
by `--ees-units` from the stored units bar/kJ/K):

1. **Formulation difference, within tolerance for two property models** (typical of
   ees_import.md §11, older fluid model): `T_5` 2.07e-2, `T_9` 1.65e-2, `T_min` 6.42e-3,
   `x_2`/`x_4`/`x_5`/`x_6` 2.96e-3, `x_3`/`x_9` 2.40e-2, `epsilon` 1.16e-2, `COP` 2.84e-2,
   `m_dot_3` 1.28e-2.
2. **The same difference amplified by the circulation sensitivity**: `x_3` is 2.4 %
   lower, so `m_dot_2 = m_dot_1·(x_1 − x_3)/(x_2 − x_3)` rises 8.52e-2 and with it
   `Q_evap` 8.08e-2, `Q_cond` 8.97e-2, `Q_gen` 5.39e-2, `Q_abs` 3.83e-2.
3. **Absolute `h`, `s` are not comparable**: CoolSolve's `NH3H2O` is IAPWS G4-01
   (reference: `u = s = 0` for the pure saturated liquids at their triple points), the
   EES `NH3H2O` external routine is the Ibrahim & Klein (1993) model with its own
   references — CoolSolve `docs/nh3h2o_review.md` documents both the formulation and
   the reference-state difference (about 1 % between the formulations, plus another
   reference state for `h`, `s`, `u`). The offsets are state-dependent (liquid solutions
   +100 to +124 kJ/kg, vapour +310 kJ/kg), which is why only differences and derived
   results are compared here (ees_import.md §11).
4. **Four EES records carry mislabelled units** (the stored block `T_4`…`Qu4` says
   `C`, an author slip in the Variable Information dialog): `T_4` = 300.15 K = 27 °C,
   `P_4` = 13.5 bar, `s_4` = 0.4296 kJ/kg-K — the values agree with CoolSolve once
   converted (`T_4` = 27, `P_4` = 1.35e6). `CheckQ` is ≈ 0 on both sides (EES −0.012 W,
   its own convergence residual on a 750 kW throughput; CoolSolve 2.9e-11 W).

The maximum relative difference over the comparable variables (group 1+2) is
**8.97e-2** on `Q_cond` — the value quoted in `model.json`. During the import, the
call pair itself was checked: at state 6 every built-in input pair ((T, P, X),
(P, X, Q), and the saturation route of `CSL-0249`) returns the same state, and the
quality implied by the stored composition (0.7865) agrees with the stored quality
`Qu6` = 0.78299 within 0.45 % — the EES and CoolSolve states are the same; only the
enthalpy scale differs.

The whole-cycle energy balance closes (`CheckQ` ≈ 0) and the solution is physically
plausible (qualities of the two-phase states between 0 and 1, temperatures ordered
along each stream).

## Source and attribution

The EES example `Absorp.ees` ("Absorption cycle calculation using an external
Procedure") ships with EES and is published by F-Chart Software
(https://fchartsoftware.com/ees/examples/absorp.ees, MIT); the `{$ID$}` tag of the
ULiège copy names Professor S. A. Klein (University of Wisconsin-Madison) as the EES
licence holder. The current text of the example states that the ammonia-water data
"can be accessed using NH3H2O as the property name with the usual property
functions. Alternatively, the property data can be accessed using the NH3H2O
external procedure" — this model uses the first interface. Source:
`~/Nextcloud/thermo_models/EES_library/Absorp.ees` (EES 8.821).

## Conversion log

- **2026-11-14 — import**: `ees_extract.py` (EES 8.821, 95 variables, unit system
  `SI MASS DEG KPA C KJ`, bar annotations on the pressures, no tables). The stored
  solution is fresh (`CheckQ` ≈ 0 stored).
- **2026-11-14 — units**: converted by hand to SI-°C-Pa-J: `P_high = 13.5 [bar]` →
  1350000 Pa, `P_low = 1.7 [bar]` → 170000 Pa; the temperatures that the original
  passed in K through `tk()` (`TK(80)`, `TK(115)`, `TK(27)`, `TK(-1)`) are passed in °C;
  the heat rates and enthalpies are converted homogeneously (kJ, kJ/kg, kJ/s → J,
  J/kg, W); no hidden unit-dependent constant.
- **2026-11-14 — external procedure → built-in calls**: the nine `CALL NH3H2O(...)`
  calls to the external procedure are replaced by built-in `NH3H2O` property calls
  (`ENTHALPY`, `ENTROPY`, `MASSFRACTION`, `TEMPERATURE` with the (T, P, X), (T, P, Q),
  (P, X, H), (P, X, Q) pairs), the interface that the source itself documents; no
  equation of the cycle changes. External routines (DLLs) are not supported by
  CoolSolve; no gap is registered since the failure would only concern the external
  DLL (per task card, following the `CS-GAP-REFPROP` precedent: rewrite, not a gap).
- **2026-11-14 — dead code**: the `FUNCTION tk` (°C → K helper of the external calls)
  removed; the call outputs `u`, `v`, quality (`Qu…`) and the unused companions of
  `T_min`/`T_m_9` (`P_m_6`, `x_m_6`, `h_m_6`, `s_m_6`, `u_m_6`, `v_m_6`, `P_m_9`,
  `x_m_9`, `s_m_9`, `u_m_9`, `v_m_9`) were never used and are not computed.
- **2026-11-14 — state points**: the arrays `P[i]`, `T[i]`, `x[i]`, `h[i]`, `s[i]`
  (i = 1…10) added at the end for the diagrams (results unchanged).
- **Level**: equations 108 → 1; largest block 2 → 0; structure (arrays) → 1;
  ≥ 3 coupled components (generator, condenser, evaporator, absorber, solution heat
  exchanger) → 1; physics (no calibration/off-design) → 0; numerics (no curated
  guesses) → 0; score 3 → level 2.

## Limitations and CoolSolve gaps

None. The model runs in CoolSolve with the built-in `NH3H2O` calls; the original
external-procedure interface is not supported by CoolSolve (external routines), and
per the source's own documentation the built-in interface is the equivalent EES way
to call the same property data, so no gap is registered. Property results carry the
documented difference between the two `NH3H2O` formulations (see Verification,
group 1–3; CoolSolve `docs/nh3h2o_review.md`).

## Related models

- `CSL-0249` (*nh3h2o_absorption_chiller*): the same single-effect NH3-H2O cycle with
  the richer component models (rectifier, pump work, refrigerant heat exchanger,
  prescribed heat-exchanger effectiveness) — this model is its simpler published-example
  counterpart at the same pressure level (13.5/1.7 bar).
