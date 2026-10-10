# Vertical ground-loop heat exchanger (borefield) with heat pump: reference simulation model

🟠 **Level 3 · Advanced** &nbsp;|&nbsp; ⏱️ **Dynamic** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0081`

Time-dependent simulation of a vertical ground-coupled heat exchanger — a field
of `n_b` vertical U-tube boreholes of depth `L_bh` exchanging heat with a heat
pump — in which the borehole wall temperature follows the **cylindrical heat
source** theory (g-function of Cooper, 1976), the borehole thermal resistance
is the one of Remund (with the Sieder-Tate/Whitaker and Gnielinski Nusselt
correlations in a `PROCEDURE`), and the **Multiple Load Aggregation Algorithm**
(MLAA) of Pinel superposes the hour, day, week, month and remaining load
histories of the borefield. The model is integrated over the summer hours with
`INTEGRAL` and returns the borehole wall temperature, the borefield power, the
fluid temperatures of the loop and the energy extracted from the ground. It is
the library's reference model of a **geothermal (borefield) source**, from the
ULiège model data bank.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | none — the brine properties (`c_p_f`, `rho_f`, `mu_f`, `k_f`) are constant inputs, no property call |
| **Size** | 74 equations — 73 algebraic equations forming a **single** block of 73 (the whole model is mutually coupled through the two MLAA procedure calls), plus the 1 `INTEGRAL` state equation; 1 state variable, 999 integration steps of 3600 s. `coolsolve -d` prints `Total blocks: 0` (see *Limitations*, `CS-DOC-SQUARE-INTEGRAL`) |
| **Source** | ULiège model data bank — `VerticalGHES_RefSim_EES_Model_SB080213.EES` (EES X7.888), inside `VerticalGHES_EXE_Model_SB080213.zip` |
| **Authors** | Stéphane Bertagnolio (ULiège Thermodynamics Laboratory, from the header of the file) |
| **License** | MIT |
| **CoolSolve** | native file **blocked** by `CS-GAP-GOTO` and `CS-GAP-INTEGRALVALUE`; no runnable variant |

## Problem statement

A vertical ground-loop heat exchanger (a borefield of `n_b = 1` U-tube
boreholes, 100 m deep, 0.152 m in diameter, 5.5 m apart, in a ground of
conductivity 2.1 W/m·K and thermal diffusivity 0.082 m²/day) is coupled to a
heat pump of COP 3.5. The undisturbed ground temperature is 10 °C and the
brine of the loop circulates at 1 kg/s, entering the borefield at
−1.2173 °C and leaving at the temperature computed by the model. The heat pump
extracts a constant 4339 W, i.e. 3099 W are rejected to the ground
(`Q_dot_borefield = Q_dot_hp·(1 − 1/COP)`). Simulate the first 1000 summer
hours (1 h step) and give the borehole wall temperature `t_w`, the exhaust
temperature of the loop, and the energy extracted from the ground.

## Model

- **Borehole wall temperature (cylindrical heat source).** The mean ground
  temperature response to a continuous load `Q_dot_bf` distributed over the
  total borehole length is written with the g-function `G(Fo_p·t)` of Cooper
  (implemented as the `FUNCTION G`), and the sum of the load histories is
  accumulated by the MLAA:

  $$\frac{\mathrm{sum\_MLAA}}{k_s\,L_{bf}} = t_g - t_w + t_p$$

  with the Fourier number `Fo = 4·alpha_s/d_bh²` and the dimensionless time
  `Fo_p·time` (`time_day\step = 1/24·DELTAtau_summer`, i.e. the time step
  expressed in days). `t_p` is the **interference temperature penalty** of
  Bernier, set to 0 by the original ("the temperature penalty is neglected for
  short and middle-term simulations (less than 5 years)"); the correlation is
  implemented in the `PROCEDURE Penalty`, which the original does not call.
- **Multiple Load Aggregation Algorithm** (`PROCEDURE mean` and `PROCEDURE
  summation`, both driven by `GOTO` ladders and by `INTEGRALVALUE`): the mean
  borefield load over the last hour, day, week and month (`q_day`, `q_week`,
  `q_month`, `q_rest`) and the corresponding superposed response.
- **Borehole thermal resistance** `R_b = R_fluid + R_pp + R_g`:
  pipe wall `R_pp = ln(D_p_out/D_p_in)/(2π k_p)/2`, fluid `R_fluid =
  1/(π D_p_in h_in)` with `h_in = Nu#·k_f/D_p_in` from the Nusselt
  `PROCEDURE`, grout `R_g = 1/(S_bh k_grout)` with the Remund shape factor
  `S_bh = beta_0·(d_bh/D_p_out)^beta_1` (three borehole configurations A, B,
  C are proposed through the `$IF borehole_configuration$` directives).
- **Fluid side**: `Q_dot_borefield = L_bf/R_b·(t_w − t_f)` with
  `t_f = (t_f_su_loop + t_f_ex_loop)/2` and the loop temperature drop
  `t_f_su_loop = t_f − Q_dot_borefield/(2·m_dot_f_bf·c_p_f)`.

| Inputs | Value (regression case) | Main outputs |
|---|---|---|
| `n_b`, `L_bh`, `d_bh`, `B_sp`, `A_bf` | 1, 100 m, 0.152 m, 5.5 m, 1.25 | `t_w` = 1.388 °C at the end of the run |
| `k_s`, `alpha_s` | 2.1 W/m·K, 0.082 m²/day | `DELTAt_g` = 8.61 K |
| `D_p_in`, `D_p_out`, `k_p`, `k_grout` | 0.0274 m, 0.0335 m, 0.42 W/m·K, 2.6 W/m·K | `R_b` = 0.09667 K·m/W |
| `c_p_f`, `rho_f`, `mu_f`, `k_f`, `M_dot_f_bf` | 3960 J/kg·K, 1022 kg/m³, 0.003081 Pa·s, 0.49 W/m·K, 1 kg/s | `h_in` = 3307 W/m²·K, `Re` = 15 082, `Pr` = 24.9 |
| `t_g`, `t_f_ex_loop`, `COP_heatpump`, `Q_dot_hp` | 10 °C, −1.217341 °C, 3.5, 4339.06 W | `Q_dot_borefield` = 3099.3 W, `Q_bf_kWh` = 3450 kWh |
| `tau_summer_1`, `tau_summer_2`, `DELTAtau` | 1 h, 1000 h, 3600 s | `run_h` = 1000 h |

## How to run

The model **cannot be run in CoolSolve**: the native file keeps the
original syntax and is blocked (see *Limitations and CoolSolve gaps*). There is
**no runnable variant**, because the two gaps that block the physics of the
model (`INTEGRALVALUE`, `GOTO`) cannot be worked around without replacing the
Multiple Load Aggregation Algorithm by a different algorithm.

```bash
coolsolve ./vertical_ghes_refsim.eescode    # -> "Parse failed: Line 108: Could not parse line" … (GOTO ladders)
```

(the `$IF` directives are resolved — branch `'B'` is kept, the model is square — and the
first error is the parse error of the `GOTO` statements and labels of the two procedures,
lines 108–183.)

The file is otherwise complete: no missing library function, no lookup table,
no external data file, unit system already SI-°C-Pa-J.

## Results

The results below are the values **stored by EES** in the source file for the
regression operating point; they were checked against the equations of the
model (see *Verification*) and are what a correct solver must reproduce.

| Quantity | Value |
|---|---:|
| `Q_dot_borefield` = `Q_dot_bf` (final hour) | 3099.33 W |
| `t_w` (borehole wall, final hour) | 1.3876 °C |
| `DELTAt_g` = `t_g − t_w` | 8.6124 K |
| `t_f_su_loop` | −2.0000 °C |
| `t_f` (mean loop temperature) | −1.6087 °C |
| `sum_MLAA` | 1808.61 K |
| `R_b`, `R_fluid`, `R_pp`, `R_g` | 0.096674, 0.003512, 0.038084, 0.055078 K·m/W |
| `S_bh` (Remund shape factor) | 6.9832 |
| `h_in`, `Re`, `Pr` | 3307.4 W/m²·K, 15 082, 24.90 |
| `Q_bf_kWh` (energy extracted, 1 → 1000 h) | 3449.9 kWh |

Since the load is constant (4339 W at the heat pump, 3099 W to the ground),
the extracted energy divided by the simulated time gives the mean borefield
load: 3449.9 kWh over 999 h = 3453 W, i.e. the last-hour load of 3099 W is
9.6 % below the mean of the run (the wall temperature is still rising
monotonically towards the asymptotic value of the line-source solution, which
is why the stored mean is above the final value).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): t_w and
     Q_dot_borefield vs time from the Integral tab,
     figures/vertical_ghes_refsim_trajectory.png -->

## Verification

The source file stores the solution of its last EES run (86 variable records,
all decoded by `tools/ees_extract.py`, 86/86 — no −9999 and no parametric
table). Since the model cannot be solved in CoolSolve, the check made during
this import is an **algebraic one-liner per stored quantity**, all of them
agreeing to 10 significant digits with the file's own equations:

| Stored quantity | Recomputed from the equations | Agreement |
|---|---|---|
| `R_pipe` = 0.07616792758 K·m/W | `ln(0.0335/0.0274)/(2π·0.42)` = 0.0761679275756 | 10 digits |
| `Fo` = 14.1966759 | `4·0.082/0.152²` = 14.19667590 | 10 digits |
| `S_bh` = 6.983157838 | `17.44·(0.152/0.0335)^(−0.6052)` (configuration B) = 6.9831578384 | 10 digits |
| `R_g` = 0.05507757286 K·m/W | `1/(6.983157838·2.6)` = 0.05507757286 | 10 digits |
| `R_b` = 0.09667395984 K·m/W | `R_fluid + R_pp + R_g` = 0.096673959846 | 10 digits |
| `R_fluid` = 0.003512423196 K·m/W | `1/(π·0.0274·3307.445738)` = 0.0035124231963 | 10 digits |
| `Q_dot_hp` = 4339.061513 W | `3099.329652·3.5/2.5` = 4339.0615128 | 10 digits |
| `Q_dot_borefield` = 3099.329652 W | `100/0.09667395984·(1.387574205+1.608670498)` = 3099.3296519 | 10 digits |
| `DELTAt_g` = 8.612425795 K | `1808.609417/(2.1·100)` = 8.6124257952 | 10 digits |
| `tau` = `tau_2` = 3 600 000 s, `run_h` = 1000 | `1 + (3600000−3600)/3600`, `1000−1+1` | exact |
| `t_f_su_loop` = −2 °C | `t_f − Q/(2·m_dot_f_bf·c_p_f)` = −1.608670498 − 3099.329652/(2·1·3960) = −2.0000000 | 10 digits |

This also fixes the state of the control panel of the stored run, which the
source file leaves entirely commented out (every input is a display string
marked "!!control panel"): the stored values are used, **not** the displayed
defaults. They differ (`M_dot_f_bf` 1 vs 22 kg/s, `t_f_su_loop` −2 vs 0 °C,
`tau_summer_2` 1000 vs 8760 h, `n_b` 1 vs 20), so the file was last run with a
one-borehole, 1000-hour, 1 kg/s configuration.

The `t_f_ex_loop` = −1.217340997 °C input was reconstructed from the stored
solution: it is the only free variable of the loop pair (`t_f_su_loop` is
computed by §4.5 of the model), and it is the value for which the stored
`t_f` = −1.608670498 °C is recovered exactly (`(−2 − 1.217340997)/2`).

**The stored solution is partly stale** (`CS-BUG-EXTRACT-STALE`): thirteen of
its records are leftovers of equation sets that are commented out in the file
(`t_s` = 13 550.1 = `L_bh²/(9·alpha_s)`, `f_penalty`, `F_correlation_p`,
`A_heating` = −35 000, `B_heating` = 85 000, `Q_dot_cooling_max`,
`Q_dot_heating_max`, `Q_dot` = 1400, `q`, `t`, `time` = 1/24, `alpha`,
`L_b`, `m_dot_f_b`, `D_p_i`), while the records of the active model are
mutually consistent as shown above. The file also stores **no integral table**:
its `$IntegralTable` object and the plot objects of the file contain no
decodable time series (the largest Extended-float runs in the binary are
sequences of zero bytes), so the final state of the 1000-hour trajectory cannot
be checked point by point.

## Source and attribution

Stéphane Bertagnolio, *Vertical ground loop heat exchanger model*, ULiège
Thermodynamics Laboratory, Faculty of Applied Sciences, model data bank,
12 February 2008 (`SB` + date in the file name, "Authors: S.Bertagnolio" in
the header of the equations window). Reference simulation model of the model
bank (Laborelec toolkit lineage). The physics is taken from the six references
listed in the file: Bernier et al. (2007, Building Simulation), Bernier
(2006, ASHRAE Journal), Bernier, Labib, Pinel & Paillot (2004, *HVAC&R Research*
10(4) 471-487, the Multiple Load Aggregation Algorithm), Bernier (2001,
ASHRAE Transactions 107(1) 605-616), Bernier (2000, 4th International
Conference on Heat Pumps in Cold Climates) and Bernier, Chahla & Pinel (2005,
submitted to ASHRAE Transactions, the long-term penalty correlation), plus
Cooper (1976, *Int. J. Heat Mass Transfer* 19, 575-577) for the g-function.

Source file (EES X7.888, English comments, stored solution), collection of
S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/Heat_and_Cool_Production_Systems/Ground_Heat_Exchangers/VerticalGHES_EXE_Model_SB080213.zip!/VerticalGHES_RefSim_EES_Model_SB080213.EES`
(inventory candidate `TM-0490`; the archive also holds an EXE build of the
model and the `BrineProp` user library, neither of which is needed — the brine
properties are constant inputs here).

## Conversion log

- **2026-10-06 — import** (`tools/ees_extract.py`): unit system already
  `SI MASS DEG PA C J` (**no unit conversion needed**), no decimal comma, no
  lookup or parametric table, no implicit library function (the 5 `FUNCTION`/
  `PROCEDURE` definitions of the file are self-contained), EES licence tag
  removed, comments already in English, standard header added, `$UnitSystem`
  line deleted. **Author**: Stéphane Bertagnolio, from the header of the file
  (initials `SB` = Stéphane Bertagnolio, date 2008-02-12 in the file name).
- **2026-10-06 — inputs restored** (this is the only substantive change of
  the model). The source file delivers **all its inputs as display strings**
  marked "!!control panel" (`M_dot_f_bf=22 [kg/s]`, `t_f_su_loop=0 [C]`,
  `t_g=10 [C]`, `n_b=20`, `L_bh=100 [m]`, `alpha_s=0.082 [m^2/day]`,
  `k_s=2.1 [W/m-K]`, `k_p=0.42 [W/m-K]`, `D_p_in=0.0274 [m]`,
  `D_p_out=0.0335 [m]`, `k_grout=2.6 [W/m-K]`, `tau_summer_1=1 [h]`,
  `tau_summer_2=8760[h]`, `borehole_configuration$='B'`), so the model as
  delivered is under-determined (69 unmatched variables) and cannot run in EES
  either. The values of the **stored EES solution** were written as the input
  equations (`t_g` = 10 °C is the same in both), the display default being
  quoted in the comment where it differs; this operating point is the only one
  that can be verified and is the regression case of the card.
  Two inputs are not in the control panel and were restored the same way:
  `Q_dot_hp` = 4339.061513 W (the two load profiles of the original are
  commented out) and `t_f_ex_loop` = −1.217340997 °C (see *Verification*).
- **2026-10-06 — corrections**: the title of the equations window said
  *"Horizontal Ground Loop Heat Exchanger"* while the model, its description
  and its geometry are vertical (comment corrected); the dead equation
  `DELTAtau_summer=1 [-]`, immediately overwritten by
  `DELTAtau_summer=DELTAtau/3600` four lines below, was removed (it is a
  duplicate definition that makes the model over-determined in EES). No other
  equation was touched; the commented-out blocks (synthetic load profile,
  100 kW load, penalty correlation, Dittus-Boelter branch, alternate MLAA
  aggregation windows) are kept: they document the alternatives of the model.
- **2026-10-06 — level 3** (score 6 of `docs/taxonomy.md` §3: 74 equations → 1;
  largest algebraic block > 30 → 2; `PROCEDURE`/`FUNCTION` present → 1;
  discretised (5-zone load aggregation, hourly time step) → 1; dynamics →
  1; no curated guesses needed → 0), in line with the inventory guess.
- **2026-10-06 — category**: the task card places the model in
  `components/heat_exchangers` (where it now is), while
  `docs/taxonomy.md` §1 maps the inventory guess `solar_renewables` to
  `renewables/geothermal_biomass` ("borefields"). The card wins for this
  import; moving the model (or splitting the category) is a `T-TAXO`
  decision for the maintainer.
## Limitations and CoolSolve gaps

Physical limitations of the model as published by its author: constant
properties of the brine; the thermal response of the borefield is that of an
infinite medium with a *uniform* load along the whole borefield length (no
axial temperature profile, no shunt impedance, no thermal imbalance between
the legs of the U-tube); the interference penalty is switched off; the
Fourier number is taken constant over the simulation; the heat pump is
represented by a constant COP and a constant load. The model is a
semi-empirical design-stage model, not a design tool.

CoolSolve gaps blocking the native file (CoolSolve
`docs/model_library_support.md`; every ID is in `missing_features`):

- `CS-GAP-INTEGRALVALUE` — the MLAA
  reads the load history of the trajectory being integrated:
  `INTEGRALVALUE((t-1)*DELTAtau, q_day)`, and the `summation` procedure loops
  over it (`90: j:=j-1 … IF((j>t-h+1) AND (j>1)) THEN GOTO 90`). CoolSolve
  parses `INTEGRALVALUE` but has no evaluator for it: *"Unknown or unsupported
  function: INTEGRALVALUE with 2 arguments"* (both the quoted and the unquoted
  spelling of the variable name). It is a planned improvement in CoolSolve
  (`docs/integral_table.md` §7.2, item 4).
- `CS-GAP-GOTO` — the two MLAA
  procedures are written as `GOTO` ladders with numeric statement labels
  (`IF (t=1) THEN GOTO 1000`, `10:`, `20:`, `999:`). CoolSolve parses the
  labels and **silently ignores the jumps**, so every branch of a ladder is
  executed in turn: the values are wrong with a *SUCCESS* solver status. This
  is a silent wrong answer, not an error.
- `CS-DOC-SQUARE-INTEGRAL` — the `-d` analysis of a model with `INTEGRAL`
  calls reports `System square: No` and lists *all* variables as unmatched
  (`Equations: 74, Variables: 70`), which is why the real diagnosis comes from
  the `Algebraic subsystem is not square: N equations vs M unknowns` line of
  the debug folder (`integral.md`).

**No runnable variant is shipped.** `INTEGRALVALUE` and `GOTO` are what makes
the Multiple Load Aggregation Algorithm work: without them the five-zone
aggregation of the load history cannot be expressed at all, and replacing it
(keeping a `DUPLICATE` array of the whole trajectory, say) would be a
different model, not a transcription of this one. The `$IF` selection and the
`INTEGRAL` forms are handled by CoolSolve, but on their own they do not produce
a running model.

## Related models

- `CSL-0078` *brine-to-water heat pump reference model*: the heat-pump side
  (scroll compressor, glycol brine) of the same class of ground-source
  systems; also blocked, also from the ULiège model bank of 2008.