# Scroll-compressor heat pump on R407C — data consistency check

⛔ **Blocked** &nbsp;|&nbsp; 🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; `CSL-0068`

A manufacturer of scroll compressors for heat pumps announces the performance
of one operating point of its machine on R407C. The model rebuilds that
operating point from the announced capacities and powers and compares the
computed mass flow rate, swept volume and isentropic efficiency with the
announced ones: this is the *data consistency check* asked for by the original
exercise.

| | |
|---|---|
| **Category** | Cycles and machines › Refrigeration and heat pumps |
| **Fluids** | R407C (zeotropic blend, CoolProp mixture properties) |
| **Size** | 46 equations in the native file (47 in the `_coolsolve` variant), all explicit (largest block: 1) |
| **Source** | ULiège — *Machines et systèmes thermiques*, repetition session 8, exercise 5 (header `VL050415`) — CoolSolve example `refrigeration3` + original EES file |
| **Authors** | Vincent Lemort (ULiège Thermodynamics Laboratory, original exercise, 2005-04-15); S. Quoilin (CoolSolve example) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — native file **blocked** (`CS-GAP-PROP-TH`); the runnable `_coolsolve` variant is **verified** (see *Verification*) |

## Problem statement

A manufacturer of scroll compressors for heat pumps provides the performance of
one operating point of its compressor:

- evaporation temperature: 0 °C, superheat at the suction: 5 K;
- condensation temperature: 50 °C, subcooling: 4 K;
- heating capacity: 6.30 kW;
- electrical power input: 1.81 kW;
- refrigerating capacity: 4.60 kW;
- mass flow rate: 30.9 g/s and swept volume: 5.92 m³/h;
- refrigerant: R407C.

Check that these data are consistent and compute the **global isentropic
efficiency** of the compressor.

## Model

States, numbered as in the original: **1** compressor inlet, **2** condenser
inlet = compressor outlet, **3** condenser outlet, **4** evaporator inlet.

- **State 1**: saturation pressure at `T_ev` (`x = 1`) and the temperature
  `T_1 = T_ev + DELTA_T_oh`; the density `rho_1` and the entropy `s_1` follow.
- **State 2**: saturation pressure at `T_cd` (`x = 1`). The compressor is
  described by its isentropic efficiency
  $\varepsilon_{s,cp} = (h_{2,s}-h_1)/(h_2-h_1)$ with $h_{2,s} = h(P_2,s_1)$,
  so the exit enthalpy `h_2` is an **output**: it is fixed by the condenser
  balance $\dot Q_{cd} = \dot m (h_2-h_3)$ together with the announced heating
  capacity.
- **State 3**: saturation pressure at `T_cd` (`x = 0`) and the temperature
  `T_3 = T_cd - DELTA_T_sc`; `h_3` is the enthalpy of that compressed liquid.
- **State 4**: the enthalpy is unchanged from the condenser outlet (`h_4 = h_3`,
  as in the original) and the temperature is the evaporation temperature, so
  `P_4 = PRESSURE(R407C,T=T_ev,h=h_4)` gives the pressure of that state.
- **Flow rate and duties**: the refrigerating capacity closes the evaporator
  balance $\dot Q_{ev} = \dot m (h_1-h_4)$, which — with $\dot Q_{ev}$ given —
  gives the **mass flow rate** $\dot m$ the announced capacities imply; the
  compressor power delivered to the refrigerant is
  $\dot W = \dot m(h_2-h_1)$ and its isentropic counterpart
  $\dot W_s = \dot m(h_{2,s}-h_1)$. Two efficiencies are then available: the
  electrical one, `eta_el = W_dot/W_dot_el` (fluid power over electrical power)
  and the **global isentropic one**, `epsilon_s_cp_glob = W_dot_s/W_dot_el`.
- **Swept volume**: the compressor is a volumetric machine, so at a given speed
  it always draws the same volumetric flow $\dot V$:
  $\dot m = \dot V\rho_1$ and $\dot V_{m3h} = 3600\,\dot V$.

The three lines in braces are the values announced by the manufacturer. They
are **not** equations, in EES as well as in CoolSolve: the EES solution report
numbers 38 equations and does not include them, and its stored solution has
`M_dot` = 0.03195 kg/s and `V_dot_m3h` = 6.012 m³/h, not the announced 30.9 g/s
and 5.92 m³/h. In CoolSolve they are read as comments, so `M_dot` and
`V_dot_m3h` are **outputs** of the model — which is exactly what the exercise
asks.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `T_ev` / `DELTA_T_oh` evaporation, suction superheat | 0 °C / 5 K | `M_dot` mass flow rate | 0.031955 kg/s (31.95 g/s) |
| `T_cd` / `DELTA_T_sc` condensation, subcooling | 50 °C / 4 K | `V_dot_m3h` swept volume | 6.008 m³/h |
| `Q_dot_cd` heating capacity | 6.30 kW | `T_2` compressor outlet temperature | 82.86 °C |
| `Q_dot_ev` refrigerating capacity | 4.60 kW | `W_dot` / `W_dot_s` fluid / isentropic power | 1700 / 1172.5 W |
| `W_dot_el` electrical power | 1.81 kW | `eta_el` electrical efficiency | 0.9392 |
| | | `epsilon_s_cp` compressor isentropic efficiency | 0.6897 |
| | | `epsilon_s_cp_glob` **global isentropic efficiency** | **0.6478** |

## How to run

The native file `heat_pump_scroll_compressor_data_check.eescode` cannot run in
CoolSolve (`CS-GAP-PROP-TH`). The runnable transcription is
`heat_pump_scroll_compressor_data_check_coolsolve.eescode`:

```bash
coolsolve ./heat_pump_scroll_compressor_data_check_coolsolve.eescode
```

The system is fully explicit (47 blocks of 1 equation); no guess values are
needed.

## Results

CoolSolve (`_coolsolve` variant) and the solution stored by EES in the original
file:

| Quantity | CoolSolve (SI) | EES stored | rel. diff |
|---|---:|---:|---:|
| `COP` heating COP | 3.4807 | 3.481 | 9.7·10⁻⁵ |
| `M_dot` mass flow rate | 0.031 954 kg/s | 0.031 950 kg/s | 1.4·10⁻⁴ |
| `V_dot_m3h` swept volume | 6.0076 m³/h | 6.012 m³/h | 7.4·10⁻⁴ |
| `P_1` / `P_2` compressor inlet / outlet pressure | 460 724 / 1 987 620 Pa | 460 382 / 1 987 000 Pa | 7.4·10⁻⁴ / 3.1·10⁻⁴ |
| `T_2` compressor outlet temperature | 82.858 °C | 82.86 °C | 1.8·10⁻⁵ |
| `P_3` saturation pressure, liquid side | 2 215 879 Pa | 2 216 000 Pa | 5.5·10⁻⁵ |
| `P_4` pressure of state 4 | 529 964 Pa | 531 903 Pa | **3.6·10⁻³** |
| `W_dot` / `W_dot_s` fluid / isentropic power | 1700.0 / 1172.5 W | 1700 / 1173 W | ≤ 4.5·10⁻⁴ |
| `epsilon_s_cp` compressor isentropic efficiency | 0.68969 | 0.6899 | 3.0·10⁻⁴ |
| `epsilon_s_cp_glob` global isentropic efficiency | 0.64778 | 0.648 | 3.5·10⁻⁴ |
| `eta_el` electrical efficiency | 0.93923 | 0.9392 | 2.8·10⁻⁵ |

The consistency check itself (recomputed from the `.sol`):

- **COP**: `Q_dot_cd/W_dot_el` = 6300/1810 = 3.4807 — the announced 3.48 is
  recovered exactly, since it is the quotient of two announced data;
- **energy balance**: `Q_dot_cd` = `W_dot` + `Q_dot_ev` = 1700 + 4600 = 6300 W —
  the balance closes by construction of the exercise (all three powers are data);
- **mass flow rate**: 31.95 g/s against the announced 30.9 g/s, i.e. the
  announced capacities imply a flow rate **3.4 % higher** than announced;
- **swept volume**: 6.008 m³/h against the announced 5.92 m³/h (**+1.5 %**),
  consistent with the previous item since $\dot m = \dot V\rho_1$ and
  $\rho_1$ = 19.15 kg/m³ is fixed by the suction conditions — this is the
  physical content of the last comment of the original file;
- **efficiency**: 110 W of the 1810 W electrical input are lost outside the
  fluid (`eta_el` = 0.939), and of the 1700 W delivered to the refrigerant only
  1172.5 W would be needed isentropically (`epsilon_s_cp` = 0.690); the global
  isentropic efficiency of the machine is therefore 0.648 — the quantity the
  exercise asks for;
- **compression check**: `T_2` = 82.86 °C > `T_1` = 5 °C with a pressure ratio
  `P_2/P_1` = 4.31 — the compressor indeed compresses.

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` (i = 1…4, states 1‑2‑3‑4‑1) give the
cycle on the P‑h or T‑s diagram (CoolSolve *Diagram* tab, fluid R407C,
*Overlay array path*, *Close cycle*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the
     cycle, figures/heat_pump_scroll_compressor_data_check_ph.png -->

## Verification

`tools/compare_solution.py heat_pump_scroll_compressor_data_check_coolsolve.sol
<ees reference>` — the reference is the solution stored by EES in the original
file, read from its solution report `EES_ok/refrigeration3.tex`:

> 30 common variables, 1 differ (rtol=0.001); only in EES: 0; only in
> CoolSolve: 17

The 17 CoolSolve-only variables are the 17 outputs the import adds or the EES
report does not tabulate: the array elements `P[i]`, `h[i]`, `T[i]`, `s[i]`
(EES stores `P[i]` and `h[i]` but does not list them in the report; `T[i]` and
`s[i]` are added by the library, see *Conversion log*) and the auxiliary
temperature `T_4` of the `_coolsolve` variant.

One variable exceeds the 0.1 % tolerance: `P_4`, at **3.6·10⁻³**. It is
obtained in EES by inverting the property model on the **(T, H)** pair and in the
variant by inverting it on the **(P, H)** pair, and the state lies inside the
saturation dome of R407C at 0 °C (quality ≈ 0.335), where the two inversions and
the R407C data of EES 9.x and of CoolProp differ slightly. No other result
depends on `P_4`: it feeds only the array `P[4]`/`s[4]` (the diagram point).

**Maximum relative deviation over all the 30 variables: 3.6·10⁻³** (`P_4`);
over the 29 others: 9.7·10⁻⁴ (`rho_1`), inside the 0.5 % property tolerance of
`ees_import.md` §11 for a real-fluid blend with a different equation of state.

Note on the reference itself: `tools/ees_extract.py` decodes a *stale* stored
solution from the binary variable records of this EES file (the known
`CS-BUG-EXTRACT-STALE`): its `P_1` = 455 489 Pa, `h_1` = 270 638 J/kg and
`epsilon_s_cp` = 0.7057 are those of an older property database and are
inconsistent with the equations of the file (its `Q_dot_cd` balance gives
`M_dot` = 0.0320 but its `M_dot` record is that value while its
`M_dot=V_dot·rho_1` pair is not). The reference used above is the EES solution
report of the same file, `EES_ok/refrigeration3.tex` (all 38 equations listed,
solution table), which is the solution the CoolSolve example's own
`.initials` file also carries.

## Source and attribution

Exercise 5 of repetition session 8 of the ULiège course *Machines et systèmes
thermiques* (MSTP). The EES file carries the header `VL050415` (initials +
date, 2005-04-15) and its licence stamp (`{$ID$ #202: Laboratoire de
Thermodynamique, U. de Liege}`, the laboratory licence holder, not the author):
**Vincent Lemort** (ULiège Thermodynamics Laboratory) is the author of the
exercise. The model was rewritten in English as the CoolSolve example
`examples/refrigeration3.eescode` by S. Quoilin; the example remains in the
CoolSolve repository as a test case, and this library model follows the **EES
original**.

Sources (not copied into the library):

- CoolSolve example: `~/git/CoolSolve/examples/refrigeration3.eescode`
  (inventory candidate `CSX-040`);
- original EES file with its stored solution:
  `~/git/CoolSolve/misc/EES_ok.zip` → `EES_ok/refrigeration3.EES`
  (EES X7.210), with the solution report `EES_ok/refrigeration3.tex`.

No student data is included. The exercise is *not* a student solution: it is a
statement with the values of the manufacturer and the equations that check them.

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  EES X7.210, 38 variable records, no lookup table, no parametric table, no
  function called but not defined, no warning. The EES licence tag was removed,
  the `$UnitSystem SI MASS DEG PA C J` directive was deleted and the unit system
  is already SI‑°C‑Pa‑J, so **no conversion was needed** (all values are in °C,
  Pa, W, J/kg, kg/s and m³/h).
- **Faithful transcription** of the original equation window; comments
  translated from French to English (they paraphrase the original's own
  comments), standard header and section titles added. In particular the two
  unit annotations of the original (`M_dot=V_dot*rho_1 "[kg/s]"` and
  `V_dot_m3h=3600*V_dot "[m3/h]"`) are kept.
- **Difference with the CoolSolve example** (the library model follows the EES
  original): the example writes `h_4=PRESSURE(R407C,T=T_ev,p=p_4)` where the
  original writes `P_4=PRESSURE(R407C,T=T_ev,h=h_4)`. The example equates an
  **enthalpy with a pressure**; because EES and CoolSolve variable names are
  case-insensitive, `p_4` and `P_4` are the same variable there, and the
  example's line only fixes `P_4` to the numeric value of `h_4`
  (270 162 Pa in its solution instead of the 531 903 Pa of EES). The original
  line is restored here. Everything else in the example is identical to the
  original (checked equation by equation).
- **`Q_dot_ev{_bis}`** (Eqn 28 of the EES report is `Q_ev = M_dot*(h_1-h_4)`):
  the `{_bis}` marker of the original is kept verbatim; CoolSolve reads it as a
  comment, EES as its own "solve by bisection" marker. In both tools `Q_dot_ev`
  is fixed by its data line `Q_dot_ev=4.6E3` *and* used in the evaporator
  balance, which is consistent because the announced data are consistent
  (`M_dot*(h_1-h_4)` = 4600.0 W).
- **Braces** `{COP=3.48}`, `{M_dot=30.9E-3}`, `{V_dot_m3h=5.92}` kept as in the
  original: they are not equations in EES (see *Model*) and CoolSolve reads them
  as comments.
- **Diagram state points**: the original already fills the arrays `P[i]` and
  `h[i]`; `T[i]` and `s[i]` (i = 1…4) were **added** as pure outputs for the
  thermodynamic diagram (library convention, workflow §3 step 5), with
  `T[4] = T_ev` (the temperature of state 4 is an input of the original) and
  `s[i] = entropy(R407C,P=P[i],h=h[i])` for states 2 and 4 (the (P, H) pair) and
  `entropy(R407C,P=P_3,T=T_3)` for state 3. Re-solving with them changes no
  other result (identical values to the last digit).
- **Blocked native file** (`CS-GAP-PROP-TH`): CoolSolve, through CoolProp, does
  not support the **(T, H)** input pair, which the original uses for
  `P_4 = PRESSURE(R407C,T=T_ev,h=h_4)` — the state is known by its temperature
  and its enthalpy. The native file keeps the original line, in valid EES.
- **Runnable variant** `heat_pump_scroll_compressor_data_check_coolsolve.eescode`:
  the single change is the pressure of state 4, obtained with the **(P, H)**
  pair instead of (T, H):
  `T_4 = TEMPERATURE(R407C,P=P_4,h=h_4)` together with `T_4 = T_ev` (two
  equations, one new variable, whose value 0 °C is fixed by the second line).
  Every other equation, variable name and input value is unchanged, and the file
  is still **valid EES** (no CoolSolve-only syntax). It is verified against the
  same EES reference (see *Verification*).
- **Level**: score 1 on the scale of `taxonomy.md` §3 (46 equations → 0,
  largest block 1 → 0, arrays → 1) gives **level 1**; kept at level 1 (the card
  guessed L2): every equation is explicit, there is no implicit loop, no
  correlation and no iteration — an introductory exercise, like `CSL-0001` and
  `CSL-0015`.

## Limitations and CoolSolve gaps

- `CS-GAP-PROP-TH`: CoolSolve (through CoolProp) rejects the **(T, H)** input
  pair of a property call (*"CoolProp does not support T,H as input pair. Use
  P,H or T,S instead"*), while EES evaluates it (stored `P_4` = 531 903 Pa). It
  blocks the native file, in one line; the `_coolsolve` variant identifies the
  same state with the (P, H) pair. The native file is otherwise sound: run
  unmodified (`coolsolve -d`) it reports 46 equations, 46 variables and
  `System square: Yes` (the same count as the EES solution report, 38, plus the
  eight state-point entries added on import), and the only failing block is
  block 27, the one holding `P_4`.
- **No pressure drops, no heat transfer**: the model checks data, it does not
  predict the machine. The evaporator and condenser are isobaric by
  construction (saturation pressures from `T_ev` and `T_cd`), the compressor has
  no volumetric or mechanical loss model beyond the isentropic efficiency, and
  the swept volume is a pure volume balance.
- The original's `h_4 = h_3` (no subcooling along the liquid line) puts the
  state 4 **inside the saturation dome** at `T_ev` (quality ≈ 0.335,
  `P_4` = 530 kPa between the dew and bubble pressures of R407C at 0 °C,
  460.7 and 567.9 kPa): the evaporator inlet is a flashed mixture, not a
  subcooled liquid. This is the modelling assumption of the exercise, kept as
  it is; the effect on the announced capacities is small because `Q_dot_ev` is
  a data of the exercise.
- `M_dot` and `V_dot_m3h` are **outputs** here: the announced values are in
  braces and, in EES as in CoolSolve, are not equations. To impose them as data
  instead, `M_dot` must be set by an equation and `Q_dot_ev` freed (the comment
  of the original line `{M_dot=30.9E-3}` mentions this alternative).
- R407C is a zeotropic blend: its bubble and dew pressures differ (the "glide"),
  so `P_2`, `P_3` and `P_4` cannot be read as a single `P_sat`. EES 9.x and
  CoolProp agree on all of them to ≤ 0.1 % here, but the state 4 inversion is
  more sensitive (0.36 %).

## Related models

- `CSL-0015` *refrigeration_cycle_basic_r134a*: the companion exercise of the
  same ULiège session (basic R134a cycle, same `epsilon_s_cp = W_s/W` definition
  of the isentropic efficiency), from the CoolSolve example `refrigeration1`.
- `CSL-0025` *heat_pump_cycle_r22_30kw*: the other heat-pump exercise of that
  session (R22, 30 kW), from the CoolSolve example `refrigeration2`.
- `CSL-0061` *refrigerator_freezer_r134a*: a two-evaporator fridge-freezer
  blocked by the same gap `CS-GAP-PROP-TH`, with the same (P, H) workaround in
  its `_coolsolve` variant.
- `CSL-0001` *refrigeration_cycle_simple_compressor*: R134a / R22 / propane
  cycle with a reciprocating-compressor model (clearance volume).