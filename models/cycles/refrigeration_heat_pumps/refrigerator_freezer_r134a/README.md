# Domestic refrigerator-freezer on R134a (two evaporators)

✅ **Verified** &nbsp;|&nbsp; 🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; `CSL-0061`

Sizing of a domestic fridge-freezer running on R134a: 1.5 kW of refrigeration
delivered at **two** evaporation temperatures (+3 °C for the fridge compartment
and −20 °C for the freezer), the useful effect split 1/3 – 2/3 between the two
compartments, with condensation at 35 °C. The cycle has one high pressure and
**two low pressures**, hence two expansion valves, two evaporators and an
intermediate pressure level.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R134a |
| **Size** | 56 equations (55 unknowns — one equation of the original is the definition of the input `eta_is_cp`, see *Conversion log*), all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition session 8, exercise 3 (EES file `R08_E03_2022.EES`) |
| **Authors** | N. Paulus, B. Dechesne (repetition assistants) and S. Quoilin (course) — see *Source and attribution* |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — **verified** against the stored EES solution (see *Verification*) |

## Problem statement

A domestic refrigerator-freezer working with R134a has to be sized. It must
deliver 1.5 kW of refrigeration at evaporation temperatures of +3 °C and
−20 °C; the power is split 2/3 for the freezer and 1/3 for the refrigerator.
The condensation temperature is 35 °C. Determine:

- the temperature of the gas leaving the compressor for an isentropic
  efficiency of 75 %;
- the refrigerant flow rate;
- the compressor power;
- the heat to be rejected at the condenser;
- the volumetric flow rate entering the two expansion valves.

The schematic (see the original comments) describes a cycle of six steps: 1‑2
compression in the compressor, 2‑3 condensation in the condenser, 3‑4 first
expansion through a throttling valve, 4‑5 evaporation in the first evaporator
(first useful effect, cools the refrigerator), 5‑6 second expansion through a
throttling valve, 6‑1 second evaporation in the second evaporator (second
useful effect, cools the freezer). One high pressure but two low pressures give
two phase-change temperatures and therefore two different useful effects.

## Model

States (as numbered in the original): 1 compressor inlet, 2 condenser inlet,
3 condenser outlet, 4 first evaporator inlet, 5 first evaporator outlet,
6 second evaporator inlet.

- **State 1**: saturated vapour at the freezer evaporation temperature
  (`x[1] = 1`, assumption of the original, the statement gives no superheat).
- **State 2**: condensing pressure from `P_sat` at `T_cd`; the compressor exit
  enthalpy follows from the isentropic efficiency,
  $\eta_{is} = (h_{2,is} - h_1)/(h_2 - h_1)$ with
  $h_{2,is} = h(p_2, s_1)$.
- **State 3**: saturated liquid at `T_cd` (`x[3] = 0`, assumption of the
  original), no pressure drop in the condenser.
- **State 4**: isenthalpic first expansion; the evaporator is isobaric, so
  `p[4] = P_sat(T_fridge)` and the temperature is `T_fridge`.
- **State 5**: the split of the useful effect fixes the state,
  $h_5 = h_4 + (h_1 - h_4)/3$ (the first evaporator provides one third of the
  required capacity).
- **State 6**: isenthalpic second expansion, isobaric at `p[1]`.
- **Flow rate and powers**: $\dot m_r = \dot Q_{cool}/(h_1 - h_4)$ (both
  evaporators lie between states 1 and 4; the only other elements are the
  isenthalpic valves), $\dot W_{cp} = \dot m_r (h_2 - h_1)$ (positive: received
  by the system) and $\dot Q_{cd} = \dot m_r (h_3 - h_2)$ (negative: rejected
  by the system), following the sign convention of the original.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `Q_dot_cool` required capacity | 1500 W | `T_ex_cp` compressor outlet temperature | 55.90 °C |
| `T_fridge` / `T_freezer` evaporation | 3 / −20 °C | `m_dot_r` refrigerant flow rate | 0.010905 kg/s (10.9 g/s) |
| `T_cd` condensation | 35 °C | `W_dot_cp` compressor power | 575 W |
| `eta_is_cp` isentropic efficiency | 0.75 | `Q_dot_cd` condenser duty | −2075 W (2.075 kW rejected) |
| `fluid$` | R134a | `V_dot_3` / `V_dot_5` valve inlet flows | 9.34 / 319.8 L/s |

## How to run

```bash
coolsolve ./refrigerator_freezer_r134a.eescode
```

## Results

CoolSolve (main file) and the solution stored by EES in the source
file:

| Quantity | CoolSolve (SI) | EES stored | Agreement |
|---|---:|---:|---:|
| `p[1]` freezer evaporator pressure | 132 735 Pa (1.327 bar) | 132 820 Pa | 6.4·10⁻⁴ |
| `p[2]` condensing pressure | 886 981 Pa (8.870 bar) | 887 473 Pa | 5.6·10⁻⁴ |
| `p[4]` fridge evaporator pressure | 325 985 Pa (3.260 bar) | 326 212 Pa | 7.0·10⁻⁴ |
| `T_ex_cp` compressor outlet | 55.8986 °C | 55.8987 °C | 2.9·10⁻⁶ |
| `m_dot_r` refrigerant flow | 0.0109053 kg/s | 0.0109056 kg/s | 3.0·10⁻⁵ |
| `W_dot_cp` compressor power | 574.99 W | 574.93 W | 8.9·10⁻⁵ |
| `Q_dot_cd` condenser duty | −2074.99 W | −2074.93 W | 2.5·10⁻⁵ |
| `V_dot_3` first valve inlet | 9.3407·10⁻⁶ m³/s (9.34 L/s) | 0.0093410 L/s | 2.7·10⁻⁵ |
| `V_dot_5` second valve inlet | 3.1978·10⁻⁴ m³/s (319.8 L/s) | 0.319544 L/s | 7.2·10⁻⁴ |
| `x[4]`, `x[5]`, `x[6]` qualities | 0.22906, 0.46262, 0.56933 | 0.22906, 0.46263, 0.56933 | ≤ 3.3·10⁻⁵ |

Sanity checks on the results (recomputed from the `.sol` file):

- evaporator duties: `m_dot_r*(h[5]-h[4])` = 500.0 W (fridge, 1/3 of 1.5 kW) and
  `m_dot_r*(h[1]-h[6])` = 1000.0 W (freezer, 2/3), as prescribed;
- energy balance of the cycle: 1500.0 W of refrigeration + 575.0 W of compressor
  power = 2075.0 W, which is exactly the condenser duty — the balance closes;
- `COP = Q_dot_cool/W_dot_cp` = 2.61, against a Carnot COP of 5.45 for the
  two-compartment machine (reversible work 275.2 W =
  `Q_dot_fridge*(T_cd_K/T_fridge_K - 1) + Q_dot_freezer*(T_cd_K/T_freezer_K - 1)`),
  the loss coming from the 0.75 isentropic efficiency of the compressor.

The arrays `p[i]`, `h[i]`, `T[i]`, `s[i]`, `v[i]`, `x[i]` (i = 1…6, state 7 =
state 1 closes the loop) give the cycle on the P‑h or T‑s diagram (CoolSolve
*Diagram* tab, *Overlay array path*, *Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the
     two-evaporator cycle, figures/refrigerator_freezer_r134a_ph.png -->

## Verification

`tools/compare_solution.py refrigerator_freezer_r134a.sol
reference/ees_variables.csv --ees-units` (reference: solution stored by EES in
the source file, converted from its kPa/kJ unit system):

> 55 common variables, 17 differ (rtol=0.001); only in EES: 2; only in
> CoolSolve: 1

The 17 differences are explained:

- **15 absolute enthalpies and entropies** (`h[1]`…`h[7]`, `h_2_is`, `s[1]`…`s[7]`):
  EES and CoolProp use different reference states for R134a. The offsets are
  constant over the whole cycle: +148 145…148 155 J/kg on `h`
  (+148.15 kJ/kg, the value already documented for R134a in `CSL-0015`) and
  +795.62…795.69 J/kg·K on `s`. All differences and all derived results agree.
- **2 volumetric flow rates** `V_dot_3`, `V_dot_5`: reported in m³/s here and in
  L/s by EES (the factor 1000 is the only difference). The L/s values quoted
  above are the same numbers.
- Excluded from the agreement statement above: the two variables only EES
  reports, `P` and `Pertes`. They appear in the EES variable records but in
  **none** of the equations of the file (leftovers of an earlier version of the
  exercise); they were not imported. The single variable only CoolSolve reports
  is the string variable `fluid$`.

Maximum relative deviation over all the other variables: **7.5·10⁻⁴** (`v[5]`),
i.e. well inside the 0.5 % tolerance for real-fluid properties with a different
equation of state (`ees_import.md` §11).

Second, independent reference: the course also provides a Python/CoolProp
solution of the same exercise (2020 session,
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R8/old/ThAp20_R08E03.py`,
same statement and same equations). Run as is it prints 55.9 °C, 11 g/s,
575 W, 2.07 kW and 0.01 / 0.32 L/s — the same results as the table above (it was
used as a check only, nothing was copied from it).

## Source and attribution

Solution of exercise 3 of repetition session 8 of the ULiège course
*Thermodynamique appliquée* (MECA0002). The EES file itself names no author: it
carries only the licence stamp of the laboratory
(`{$ID$ #0202: For use only by students and staff at the Laboratoire de
Thermodynamique, University of Liege …}`, removed by the extraction). The
`authors` column of the source inventory and the metadata of the companion files
of the same session (the Python solution of the 2020 edition of this exercise,
which names its author, and the Word statement) attribute the exercise solutions
of the session to the repetition assistants N. Paulus and B. Dechesne, in a
course given by S. Quoilin; they are listed as authors here on that basis. No
student data is included.

Source file (EES 10.836, comments in French, decimal comma), collection of
S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R8/R08_E03_2022.EES`
(inventory candidate `TM-0450`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES 10.836, 57 variable records, no lookup or parametric table, no function
  called but not defined. The EES licence tag, `{$PX$96}` and `{$ST$OFF}` were
  removed; the decimal comma was converted by the tool; the extraction report
  warns that the EES unit system is `SI MASS DEG KPA C KJ`. Comments translated
  to English, standard header added, and the model converted **by hand** to
  SI‑°C‑Pa‑J (below).
- **Unit conversion** (`ees_import.md` §6). Temperatures were already in °C and
  the specific volumes in m³/kg, so:
  - `Q_dot_cool = 1500` (1.5 kW in the original); `Q_dot_freezer` and
    `Q_dot_fridge` follow unchanged (1000 W and 500 W);
  - `p[2] = P_sat(fluid$,T=T_cd)` and `p[4] = P_sat(fluid$,T=T[4])`: **no**
    factor is added, because a property-function result is already in
    CoolSolve units (Pa). The original values are 887.5 kPa and 326.2 kPa;
  - `W_dot_cp` and `Q_dot_cd` are therefore in W (`m_dot_r*(h[2]-h[1])` with
    `h` in J/kg), and `m_dot_r = Q_dot_cool/(h[1]-h[4])` in kg/s;
  - `V_dot_3` and `V_dot_5` are reported in **m³/s** (`m_dot_r*v[3]`,
    `m_dot_r*v[5]`); the original multiplies by 1000 to answer in L/s. The L/s
    values are kept in the comments of the two lines and in the results table.
- **Guess values (`.initials`)**: the stored EES values converted to SI, except
  the **absolute enthalpies and entropies** (`h[1]`…`h[7]`, `h_2_is`,
  `s[1]`…`s[7]`), which are left out: they are expressed in the EES reference
  state (148.15 kJ/kg and 795.65 J/kg·K below CoolProp's) and, fed to CoolProp
  as initial guesses, they lead it into a physically meaningless state
  (`enthalpy(R134a,p=p[2],s=s[1])` then returns a wrong value **without** an
  error message). The remaining guesses (pressures, temperatures, specific
  volumes, qualities, powers, flow rates) are all consistent between the two
  tools. The two orphan records `P` and `Pertes` of the EES file were not
  imported (they are in no equation).
- **`eta_is_cp`**: kept exactly as in the original — an input value
  (`eta_is_cp = 0.75`) *and* a definition equation
  (`eta_is_cp = (h_2_is-h[1])/(h[2]-h[1])`). EES keeps the first assignment as
  the fixed value and solves the second equation for `h[2]`; the same idiom is
  used in `CoolSolve misc/EES_ok.zip: EES_ok/refrigeration1.EES` (`epsilon_s_cp`
  = 0.75, then `epsilon_s_cp = w_s/w`), whose stored solution satisfies both
  equations (`w_s`/`w` = 0.75). CoolSolve also treats the first assignment as the
  fixed value and solves the block for `h[2]`, and the model converges.
- **(T, H) property calls, decision D11** (2026-10-05, roadmap card C-88): the
  original evaluates the three properties of state 4 (first evaporator inlet)
  with the **(T, H)** input pair — `x[4]`, `s[4]`, `v[4]` — the temperature being
  known from the isobaric evaporator and the enthalpy from the isenthalpic valve.
  CoolProp does not support that pair (`CS-GAP-PROP-TH`, not planned), so in the
  **model itself** the three calls now use the **(P, H)** pair,
  `x[4] = quality(fluid$,P=p[4],H=h[4])`, `s[4] = entropy(fluid$,P=p[4],H=h[4])`,
  `v[4] = volume(fluid$,P=p[4],H=h[4])`: state 4 lies in the saturation dome at
  `T_fridge`, so the saturation pressure at the same temperature,
  `p[4] = P_sat(fluid$,T=T[4])` (already computed on the previous line), fixes the
  same state. This is the rewrite prescribed by workflow §6 ("Property calls with
  the (T, H) input pair", decision D11): no native/variant split for this reason
  alone, so the runnable variant `refrigerator_freezer_r134a_coolsolve.eescode`
  (and its `.sol`, `.initials`) has been deleted and this file is the single model
  file. Every variable name, input value and other equation is unchanged, the file
  is still valid EES (no CoolSolve-only syntax), and the values are bit-identical
  to those of the deleted variant. `CS-GAP-PROP-TH` is no longer a blocking gap
  and is not listed in `missing_features`. Not needed either: any change to the
  `eta_is_cp` line (an earlier attempt inverted it for `h[2]`), which was
  reverted.
- **Diagram support**: none needed. The original already computes every state as
  an array (`p[i]`, `h[i]`, `T[i]`, `s[i]`, `v[i]`, `x[i]`, i = 1…6) and repeats
  state 1 as state 7 to close the loop, which is the state-point block of the
  library convention (workflow §3, step 5); the results are unchanged.
- **Level**: score 2 on the scale of `taxonomy.md` §3 (56 equations → 1,
  arrays → 1) would give level 2; kept at **level 1** because every equation is
  explicit (largest block 1), no iteration, no correlation and no property loop
  has to be resolved — the same pedagogical intent as `CSL-0001` and
  `CSL-0015`.

## Limitations and CoolSolve gaps

- `CS-GAP-PROP-TH` (not blocking): CoolSolve, through CoolProp, rejects the
  **(T, H)** input pair of a property call (*"CoolProp does not support T,H as
  input pair. Use P,H or T,S instead"*). The original uses it for the three
  properties of state 4 (first evaporator inlet) and EES computes them (stored
  `x[4]` = 0.22906, `s[4]` = 381.82 J/kg·K, `v[4]` = 0.0149007 m³/kg). The model
  rewrites those three calls with the (P, H) pair, which identifies the same
  state (decision D11, see the conversion log), so the gap does not block the
  file; it would still be needed by anyone wanting the original (T, H) form.
- The compressor inlet is assumed to be **saturated vapour** and the condenser
  outlet **saturated liquid** (assumptions of the original; the statement gives
  no superheat and no subcooling). Real appliances have 2–5 K of superheat at
  the compressor inlet, so the density, the flow rate and the COP of the real
  machine differ from these values.
- The evaporator of the fridge compartment is modelled as isobaric **and**
  isothermal at `T_fridge`, and the second evaporator is isobaric at `p[1]`:
  no pressure drop, no heat transfer coefficient, no finite approach
  temperature. The model sizes the machine, it does not predict off-design
  behaviour.
- The compressor is described by its isentropic efficiency only (no mechanical
  or electrical losses): `W_dot_cp` is the *isentropic* shaft power of the ideal
  cycle times 1/0.75.
- No volumetric bounds: the `.initials` file holds guesses only, and the model
  relies on the qualities staying in [0, 1] (`CS-GAP-BOUNDS`, not blocking).

## Related models

- `CSL-0001` *refrigeration_cycle_simple_compressor*: R134a (also R22,
  propane) vapour-compression cycle of the same exercise family, with a
  reciprocating-compressor model and a clearance volume.
- `CSL-0015` *refrigeration_cycle_basic_r134a*: basic R134a cycle with a
  constant isentropic efficiency and a motor efficiency; it uses the same
  `epsilon_s_cp = w_s/w` definition of the isentropic efficiency.
- `CSL-0054` *heat_pump_r410a_air_evaporator*: same category, heat pump on the
  zeotropic R410A with an air-side evaporator balance.