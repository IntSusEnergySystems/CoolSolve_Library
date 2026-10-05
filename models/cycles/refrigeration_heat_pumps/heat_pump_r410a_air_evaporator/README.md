# Air-source heat pump with R410A (evaporator air side)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0054`

An air-to-water heat pump running on R410A: the evaporator draws heat from the
outdoor air, the condenser heats a water circuit (e.g. floor heating). The
model determines the refrigerant flow rate from the condenser heat balance,
the evaporator air flow rate for a 15 K air cooling, the overall COP and the
compressor isentropic efficiency. The evaporator pressure drop is accounted
for and R410A is treated as the zeotropic fluid it is.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R410A |
| **Size** | 41 equations, all explicit (largest block: 1) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition 8, exercise 2, 2022-2023 (EES file `R08_E02_2022.EES`) |
| **Authors** | TBD (ULiège course MECA0002, *Thermodynamique appliquée* — repetition exercise, author not named in the source) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — verified against the EES stored solution and the companion CoolProp script (see *Verification*) |

## Problem statement

An air-to-water heat pump works with refrigerant R410A under the following
conditions: evaporator inlet pressure 8 bar, evaporator pressure drop 0.32 bar;
in the condenser (pressure drop neglected) the refrigerant enters at 105 °C and
30 bar and leaves at 45 °C; the water flow rate is 0.1 kg/s, heated by 25 K.
Compute the refrigerant flow rate and the overall COP of the heat pump. What is
the air flow rate through the evaporator if the air is cooled by 15 K? What is
the isentropic efficiency of the compressor?

## Model

Cycle states (1 = compressor inlet / evaporator outlet, 2 = condenser inlet,
3 = condenser outlet, 4 = evaporator inlet):

- condenser: state 2 superheated vapour $(p_2, T_2)$, state 3 subcooled liquid
  $(p_2, T_3)$, pressure drop neglected; the refrigerant heat duty balances the
  water duty $\dot Q_w = \dot m_w\, c_w\, \Delta T_w$, which fixes
  $\dot m_{R410A}$;
- expansion valve isenthalpic: $h_4 = h_3$;
- evaporator: pressure drop $p_1 = p_4 - \Delta P_{ev}$; no superheat being
  specified, state 1 is saturated vapour ($x_1 = 1$) — the compressor cannot
  admit liquid; the refrigerant duty balances the air duty
  $\dot Q_{air} = \dot m_{air}\, c_{air}\, \Delta T_{air}$, which fixes
  $\dot m_{air}$ (constant $c_p$ values for water and air, as in the original);
- compressor power $\dot W_{cmp} = \dot m\,(h_2 - h_1)$, $COP = -\dot Q_{cd} /
  \dot W_{cmp}$, isentropic efficiency $\eta_{is} = (h_{2,is} - h_1)/(h_2 - h_1)$
  with $h_{2,is}$ at $(p_2, s_1)$.

R410A is zeotropic: under the dome the temperature depends on pressure *and*
quality, so $T_1$ and $T_4$ are evaluated from $(p, x)$ and $(p, h)$; the
original notes that `T_sat` is not applicable there.

| Inputs | Value | Outputs | Value |
|---|---:|---|---:|
| `p_su_ev` / `DP_ev` | 8 bar / 0.32 bar | `m_dot_R410a` refrigerant flow | 0.0462 kg/s |
| `T_su_cd` / `p_su_cd` | 105 °C / 30 bar | `m_dot_air` air flow | 0.446 kg/s |
| `T_ex_cd` | 45 °C | `COP` | 2.799 |
| `m_dot_w_cool` / `DELTAT_w` | 0.1 kg/s / 25 K | `W_dot_cmp` compressor power | 3.740 kW |
| `DELTAT_air` | −15 K | `eta_is_cp` isentropic efficiency | 0.4628 |
| `c_w` / `c_air` | 4187 / 1005 J/kg-K | `T[1]` evaporator outlet | −1.199 °C |

## How to run

Open `heat_pump_r410a_air_evaporator.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./heat_pump_r410a_air_evaporator.eescode
```

No guess values are needed (all equations explicit).

## Results

| Quantity | Value | Quantity | Value |
|---|---:|---|---:|
| `p[1]` / `T[1]` | 7.68 bar / −1.20 °C | `Q_dot_cd` (condenser, negative) | −10.47 kW |
| `h[1]` | 421.02 kJ/kg | `Q_dot_ev` (evaporator) | 6.727 kW |
| `h[2]` | 502.00 kJ/kg | `Q_dot_w` (water heating) | 10.47 kW |
| `h[4]`, `x_4` | 275.37 kJ/kg, 0.341 | `W_dot_cmp` | 3.740 kW |
| `T[4]` | 0.007 °C | `COP` | 2.799 |
| `h_2_is` | 458.50 kJ/kg | `eta_is_cp` | 0.4628 |

The arrays `p[i]`, `T[i]`, `h[i]`, `s[i]` (i = 1..4, as defined by the original)
give the cycle on the P-h or T-s diagram (CoolSolve *Diagrams* tab, *Array
overlay*, *Close loop*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the cycle,
     figures/heat_pump_r410a_air_evaporator_ph.png -->

## Verification

1. **EES stored solution** (`compare_solution.py --ees-units`, work-folder
   reference `reference/ees_variables.csv`): `40 common variables, 3 differ
   (rtol=0.001); only in EES: 10; only in CoolSolve: 1`. The three differing
   variables are explained:
   - `T[4]` 1.71e-03 relative — an absolute deviation of 1.3e-5 °C on a
     near-zero temperature (EES vs CoolProp R410A properties); the companion
     CoolProp script gives 0.007398 °C, exactly the CoolSolve value;
   - `x_2`, `x_3`: EES `quality` returns 100 on a superheated state and −100 on
     a subcooled liquid, CoolSolve returns 0 (diagnostic outputs only, they
     feed no equation; gap `CS-GAP-QUALITY-DOME`, not blocking). The original's
     own comments annotate `x_2 = 100` / `x_3 = -100` in the same sense.
   The 10 variables only in the EES reference (`h[5]`, `h[6]`, `p[5]`, `p[6]`,
   `Pertes`, `s[5]`, `t[5]`, `T_SAT`, `Tsat_R410a`, `P`) are leftovers of
   earlier versions of the file, absent from its current equations.
2. **Companion CoolProp Python solution** of the same exercise
   (`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R8/old/ThAp20_R08E02.py`,
   N. Paulus): ṁ = 0.046187 kg/s, ṁ_air = 0.446254 kg/s, η_is = 0.462801,
   COP = 2.798635 — all within 4e-6 relative of the CoolSolve results (same
   property backend; its water cp of 4187 J/kg-K is the same value).

## Source and attribution

Repetition exercise solution file of the ULiège course *Thermodynamique
appliquée* (MECA0002), 2022-2023. No author is named in the EES file; the
collection metadata attributes the repetition material to the course team
(S. Quoilin, assistants). The companion CoolProp Python solution of the same
exercise (used as an additional verification reference) is signed by Nicolas
Paulus.

Source file (EES 10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R8/R08_E02_2022.EES`
(inventory candidate `TM-0449`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository): unit
  system `SI MASS DEG KPA C KJ` converted by hand to SI-°C-Pa-J
  ([ees_import.md §6](../../../docs/model_workflow.md)): `p_su_ev = 800E3 [Pa]`,
  `p_su_cd = 3000E3 [Pa]`, `DP_ev = 32000 [Pa]`, `c_w = 4187 [J/kg-K]`,
  `c_air = 1005 [J/kg-K]`; all property calls and balances become homogeneous
  in Pa/J with no other change. Decimal comma converted to dot by the
  extractor; EES licence/display tags removed. Comments translated to English
  (paraphrases of the original French comments); standard header added; no
  equation changed.
- The EES stored solution also contains variables of earlier file versions
  (`Pertes`, states 5–6, `Tsat_R410a`…); they are not part of the current
  equations and were not imported.
- **Level**: 41 equations (< 50 → 0), largest block 1 (≤ 5 → 0), arrays present
  (→ 1), cycle of 4 coupled components (→ 1), no semi-empirical/off-design
  physics (0), no curated guesses (0): score 2 → **level 2**.

## Limitations and CoolSolve gaps

- EES `quality` returns ±100 outside the saturation dome (100 superheated,
  −100 subcooled); CoolSolve returns 0 there (gap `CS-GAP-QUALITY-DOME`, not
  blocking: `x_2`/`x_3` are diagnostic outputs only).
- Constant specific heats for the water and air sides (values given in the
  course); condenser pressure drop neglected (as specified in the statement).

## Related models

- `CSL-0001` *refrigeration_cycle_simple_compressor*: refrigeration cycle
  (useful effect at the evaporator) with a simple compressor model.
- `CSL-0013` *heat_pump_basic_tespy*: air/water heat pump translated from TESPy.
- `CSL-0015` *refrigeration_cycle_basic_r134a*: basic vapour-compression cycle
  on R134a.
- `CSL-0061` *refrigerator_freezer_r134a*: same category; a two-evaporator
  refrigeration cycle (useful effect at two evaporators) rather than a heat
  pump.
