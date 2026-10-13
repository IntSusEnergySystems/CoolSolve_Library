# Counterflow heat exchanger and condenser rated by UA and a smoothed LMTD

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0137`

Translation of the two TESPy heat-exchanger component classes: the generic
counterflow exchanger `HeatExchanger` (`hx_lmtd_ua.eescode`, inventory row
`TSP-008`) and its condensing variant `Condenser`
(`hx_lmtd_ua_condenser.eescode`, row `TSP-009`). Both files carry the
**design** and the **off-design** run of the corresponding TESPy class
doctest, so that the duty closed by a terminal temperature difference, the
duty closed by the heat-transfer coefficient `UA`, the smoothed logarithmic
mean temperature difference, the pinch (`ttd_min`), the two effectivenesses
and the off-design `UA` characteristic lines are all exercised.

| | |
|---|---|
| **Category** | Components › Heat exchangers |
| **Fluids** | Air (hot side of the main file), Water (cold side of the main file; condensing hot side of the condenser file), Air (cold side of the condenser file) |
| **Size** | main file: 70 equations after analysis (largest block 8) + 1 `FUNCTION`; condenser: 68 equations (largest block 8) |
| **Source** | [`TESPy`](https://github.com/oemof/tespy) commit `19425523`, files `src/tespy/components/heat_exchangers/base.py`, `.../condenser.py`, `src/tespy/data/char_lines.json`; inventory rows `TSP-008` and `TSP-009` of `sources/tespy/inventory.csv` |
| **Authors** | Francesco Witte, Malte Fritz and the TESPy contributors; the LMTD smoothing is from S. Quoilin, PhD thesis, University of Liège, 2011 |
| **License** | MIT |
| **CoolSolve** | 0.3.0 — **verified** against the two TESPy class doctests (43 compared values, max deviation 4.3·10⁻⁵) |

## Problem statement

**Main file (`hx_lmtd_ua.eescode`).** A water-cooled exhaust-air heat
exchanger (the example of the TESPy `HeatExchanger` docstring): 0.100 m³/s of
air at 35 °C enters the hot side and is cooled to 17.5 °C, 0.1 bar; cooling
water enters the cold side at 10 °C, 3 bar. The component is **designed** for
an upper terminal temperature difference `ttd_u` = 5 K, which fixes the water
outlet temperature (30 °C) and the duty; the heat-transfer coefficient `UA`
then follows from the duty and the LMTD. In the **off-design** run the air
flow drops to 0.075 m³/s, the water flow is held at its design value and
`UA` follows the characteristic line `f_UA(m/m_design)`.

**Condenser file (`hx_lmtd_ua_condenser.eescode`).** 1 kg/s of waste steam at
2 700 kJ/kg (superheated, 15.76 bar) is condensed with ambient air entering at
20 °C, 1.001 bar; the component is **designed** for `ttd_u` = 15 K referred to
the **dew-line** temperature and for an air outlet temperature of 40 °C,
which fixes the air mass flow. The steam leaves as **saturated liquid**. In
the **off-design** run the steam flow drops to 0.7 kg/s, the air inlet
temperature rises to 30 °C and the air volumetric flow is held at its design
value; the condensing pressure is the unknown closed by the `UA` equation.

## Model

| TESPy | Equation (EES) | Comment |
|---|---|---|
| `energy_balance_hot_func` | `M_dot_h*(h_h_ex - h_h_su) = Q_dot` | heat transfer from the hot side, `Q_dot` **negative** when the hot side is cooled (TESPy sign convention, kept) |
| `energy_balance_func` | `M_dot_c*(h_c_ex - h_c_su) = -Q_dot` | cold-side energy balance |
| `UA_func` | `Q_dot + UA*lmtd = 0` with `lmtd = LMTD_smoothed(ttd_u, ttd_l)` | duty closed by the heat-transfer coefficient |
| `ttd_u_func`, `ttd_l_func` | `ttd_u = T_h_su - T_c_ex`, `ttd_l = T_h_ex - T_c_su` | terminal temperature differences |
| `ttd_min_func` | `ttd_min = MIN(ttd_u, ttd_l)` | pinch |
| `eff_hot_func`, `eff_cold_func`, `eff_max_func` | `eff_hot = (h_h_ex - h_h_su)/(h(P_h_ex, T_c_su) - h_h_su)`, `eff_cold = (h_c_ex - h_c_su)/(h(P_c_ex, T_h_su) - h_c_su)`, `eff_max = MAX(eff_hot, eff_cold)` | effectiveness against the theoretical maximum enthalpy change |
| `smoothed_lmtd` (module function) | `FUNCTION LMTD_smoothed(td_a, td_b)` | four-branch smoothed LMTD, ε = 0.001 K, ξ = 5 1/K |
| `UA_char_func` | `UA = UA_design*f_UA`, `f_UA = 2/(1/f_1 + 1/f_2)`, `f_1 = INTERPOLATE('uachar', …, M_dot_h_2/M_dot_h_design)`, `f_2 = INTERPOLATE('uachar', …, M_dot_c_2/M_dot_c_design)` | off-design UA from the characteristic lines of `char_lines.json` |
| `Condenser.subcooling_func` | `h_h_ex = ENTHALPY(fluid, P=P_h_ex, x=0)` | hot outlet is saturated liquid (subcooling deactivated, as in the doctest) |
| `Condenser.ttd_u_func`, `Condenser.calculate_lmtd` | `ttd_u = T_dew - T_c_ex`, `lmtd = LMTD_smoothed(T_dew - T_c_ex, ttd_l)` with `T_dew = TEMPERATURE(fluid, P=P_h_su, x=1)` | the ttd's of a condenser refer to the dew line, not to the hot inlet state |
| `dp1`, `dp2` | `P_h_su = P_h_ex + dp_1`, `P_c_ex = P_c_su - dp_2` | pressure drop per side, as an input (see *Conversion log*) |

Two *specification sets* are shipped side by side in each file (suffixes `_1`
and `_2`), because TESPy runs a component in a `design` phase (the design
parameters `pr1`, `pr2`, `ttd_u` and the connection design values become
unknowns) and in an `offdesign` phase (the design state is read back from
`design_path`). In EES the two phases are two sets of equations in one file:

* **case 1 — design**: the duty is closed by the ttd specification
  (`ttd_u = 5 K`, `T_c_ex = 40 °C`), `UA` is an output
  (`UA = -Q_dot/lmtd`);
* **case 2 — off design**: the duty is closed by the `UA` equation,
  `UA = UA_design·f_UA` from the characteristic lines, and the ttd's are
  outputs (the pinch of an off-design point).

## Results

`hx_lmtd_ua.eescode` vs the TESPy `HeatExchanger` doctest (case 1 = design,
case 2 = off design), all values in SI:

| Quantity | TESPy | CoolSolve | rel. diff |
|---|---:|---:|---|
| `Q_dot_1` [W] | −2 031.598 | −2 031.598 | 1.4e−09 |
| `UA_1` [W/K] | 329.497 | 329.497 | 0 |
| `lmtd_1` [K] | 6.1658 | 6.1658 | 5.8e−08 |
| `ttd_u_1` / `ttd_l_1` / `ttd_min_1` [K] | 5.0 / 7.5 / 5.0 | 5.0 / 7.5 / 5.0 | ≤ 3.7e−09 |
| `eff_hot_1` / `eff_cold_1` / `eff_max_1` [−] | 0.700031 / 0.800203 / 0.800203 | idem | ≤ 6.0e−09 |
| `M_dot_h_1` / `M_dot_c_1` [kg/s] | 0.115388 / 0.0242766 | idem | ≤ 2.4e−08 |
| `T_h_ex_1` / `T_c_ex_1` [°C] | 17.5 / 30.0 | idem | ≤ 1.6e−09 |
| `Q_dot_2` [W] | −1 778.054 | −1 778.054 | 6.7e−09 |
| `UA_2` [W/K] | 306.044 | 306.044 | 2.0e−09 |
| `lmtd_2` [K] | 5.8098 | 5.8098 | 8.6e−08 |
| `ttd_u_2` / `ttd_l_2` / `ttd_min_2` [K] | 7.4988 / 4.3957 / 4.3957 | idem | ≤ 8.6e−08 |
| `M_dot_h_2` [kg/s] | 0.0857659 | idem | 1.6e−08 |
| `T_h_ex_2` / `T_c_ex_2` [°C] | 14.4 / 27.5 | 14.396 / 27.501 | ≤ 3.3e−07 |

The doctest itself prints `round(ex_he.T − he_cw.T, 0) = 5.0` (design),
`round(he_cw.T, 1) = 27.5` and `round(he_ex.T, 1) = 14.4` (off design), all
reproduced.

`hx_lmtd_ua_condenser.eescode` vs the TESPy `Condenser` doctest:

| Quantity | TESPy | CoolSolve | rel. diff |
|---|---:|---:|---|
| `Q_dot_1` [W] | −2 471 505.34 | −2 471 505.34 | 1.1e−09 |
| `UA_1` [W/K] | 105 429.00 | 105 429.00 | 4.7e−08 |
| `lmtd_1` [K] | 23.4424 | 23.4424 | 6.3e−08 |
| `ttd_l_1` / `ttd_min_1` [K] | 34.5789 / 15.0 | idem | ≤ 2.8e−08 |
| `eff_hot_1` / `eff_cold_1` [−] | 0.944738 / 0.229637 | idem | ≤ 1.3e−08 |
| `M_dot_c_1` [kg/s] | 122.7776 | 122.7776 | 1.1e−09 |
| `T_dew_1` / `T_h_ex_1` [°C] | 55.0 / 54.5789 | idem | ≤ 3.8e−08 |
| `Q_dot_2` [W] | −1 727 731.46 | −1 727 731.44 | 1.0e−08 |
| `UA_2` [W/K] | 99 158.20 | 99 159.31 | 1.1e−05 |
| `lmtd_2` [K] | 17.4240 | 17.4238 | 1.1e−05 |
| `ttd_u_2` / `ttd_l_2` / `ttd_min_2` [K] | 11.3395 / 25.3719 / 11.3395 | 11.3392 / 25.3719 / 11.3392 | ≤ 2.6e−05 |
| `M_dot_c_2` [kg/s] | 118.7117 | 118.7168 | 4.3e−05 |

The doctest prints `round(amb_he.v, 2) = 103.17`, `round(ws_he.T − he_amb.T, 1)
= 66.9`, `T_sat − he_amb.T = 15.0` (design) and 62.5 / 11.3 (off design).

The arrays `P[i]`, `h[i]`, `T[i]`, `s[i]` give the cold stream (main file) and
the condensing stream (condenser file) of both cases on the P-h or T-s
diagram (CoolSolve *Diagram* tab, *Array overlay*).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): P-h diagram of the
      condensing stream, figures/hx_lmtd_ua_ph.png -->

## Verification

Both TESPy class doctests were re-run from the local clone
(`~/git/tespy`, commit `19425523`) in a throw-away virtual environment
(`python3 -m venv` + `pip install -e ~/git/tespy`, Python 3 + CoolProp
8.1.0dev) that is **deleted at the end of the card** (workflow §9), together
with the scratch script `tespy_reference.py` that printed every quantity
compared here; the same values were written as a reference CSV in the format
of `tools/compare_solution.py` and compared with

```bash
python3 ../CoolSolve/tools/compare_solution.py hx_lmtd_ua.sol reference_hx.csv --all
python3 ../CoolSolve/tools/compare_solution.py hx_lmtd_ua_condenser.sol reference_cd.csv --all
```

* main file: *22 common variables, 0 differ (rtol=0.001)*, largest relative
  deviation **3.30e−07** (`T_h_ex_2`);
* condenser: *21 common variables, 0 differ (rtol=0.001)*, largest relative
  deviation **4.28e−05** (`M_dot_c_2`).

Absolute enthalpies and entropies are **not** compared: EES `Air` is an
ideal-gas substance and TESPy calls the CoolProp `air` mixture, so the two
reference states differ by an additive constant (the same convention as
`CSL-0052`); all enthalpy *differences*, hence the duties and the
effectivenesses, agree (the effectiveness denominators are built from the same
fluid and the offset cancels).

The two residual deviations of the condenser off-design case come from the
same source: the air density of the EES ideal-gas substance `Air` differs from
the CoolProp `air` mixture by 4·10⁻⁵ at 30 °C, 1.001 bar, which moves the air
mass flow deduced from the fixed volumetric flow; the condensing pressure
(an unknown closed by the `UA` equation) moves with it by 5·10⁻⁵.

## Source and attribution

TESPy — *Thermal Engineering Systems in Python*, Francesco Witte, Malte
Fritz, F. T. Germany and the contributors, <https://github.com/oemof/tespy>,
commit `19425523`, MIT licence. The physics translated here is the
`HeatExchanger` component (`base.py`) and its condensing subclass
(`condenser.py`), with the default `UA` characteristic lines of
`src/tespy/data/char_lines.json` (shipped as the lookup tables
`hx_lmtd_ua-uachar.csv` and `hx_lmtd_ua_condenser-uachar.csv`) and the
`smoothed_lmtd` function.

The smoothing of the logarithmic mean temperature difference is
`tespy.components.heat_exchangers.base.smoothed_lmtd`, cited by TESPy as
S. Quoilin, *Study of cooling and heat pump systems*, PhD thesis, University
of Liège, 2011 (ε = 1 K and ξ = 1e4 there; TESPy lowers both to 0.001 K and
5 1/K for lower pinches and lower stiffness). The library already ships the
unsmoothed relation as the `LMTD` `FUNCTION` of `CSL-0105`.

Translated and published under the CoolSolve_Library MIT licence (decision
D3), with credit to the authors of the original model.

## Conversion log

1. **Python solver plumbing → simultaneous equations.** The network, the
   connections, the Newton iterations and the `design`/`offdesign` switch of
   TESPy become equations: one set for the design phase, one set for the
   off-design phase (suffixes `_1` and `_2`).
2. **Design state.** In TESPy the off-design phase reads the frozen design
   state from `design_path`; the three design quantities the characteristic
   lines need (`UA_design`, `M_dot_h_design`, `M_dot_c_design`) are therefore
   **inputs** of the off-design case, with the values of the design run of the
   same file (identical to the values case 1 computes; they are written as
   constants because the off-design case must not depend on case 1).
3. **Pressure drops are inputs.** TESPy's `dp1`/`dp2` are computed from
   `zeta1_d4`/`zeta2_d4`, the design geometry (diameter, length) and the
   Reynolds and mass flux of the run — a pipe-friction model outside the scope
   of this card (UA/LMTD/ttd/pinch). Each case therefore takes `dp_1` and
   `dp_2` as inputs with the values of the corresponding TESPy run; the
   pressures they generate are the `P_h_su`, `P_h_ex`, `P_c_su`, `P_c_ex`
   values listed in the input block. (`pr1`/`pr2` are thus not separate
   inputs: they are the ratio of the two pressures.)
4. **`v` is a volumetric flow.** In this TESPy version `Connection.v` is the
   volumetric flow in m³/s (checked against `calc_vol()`: 0.1 m³/s at
   0.115 388 kg/s and 0.8668 m³/kg), so the hot/cold flows are imposed as
   `V_dot = M_dot*VOLUME(fluid, T, P)`.
5. **Characteristic lines → lookup tables.** `CharLine` is a linear
   interpolation *clamped* to the first and last node (`extrapolate=False`);
   the EES `INTERPOLATE` of CoolSolve is linear and **extrapolates** beyond
   the table (`CS-GAP-INTERP-EXTRAP`), which is the same value on the whole
   range of the shipped tables (`m/m_design` between 0 and 3). The
   `DEFAULT` lines of `HeatExchanger` are in `hx_lmtd_ua-uachar.csv`, the
   `DEFAULT` line of `Condenser` (hot side: the *CONDENSING FLUID* line of
   `HeatExchanger`) in `hx_lmtd_ua_condenser-uachar.csv`; both variants ship
   their own companion table, as the workflow prescribes.
6. **`smoothed_lmtd` → `FUNCTION LMTD_smoothed`.** One `FUNCTION` per
   correlation, called from the main program (`lmtd_1 = LMTD_smoothed(ttd_u_1,
   ttd_l_1)`). The nested `IF`/`ELSE`/`ENDIF` blocks are the block form of
   the conditional (the single-line form in a body is wrong in CoolSolve,
   `CS-BUG-IF-SINGLELINE`); ε and ξ are local assignments, never `$COMMON`
   (decision D13). The condenser file repeats the body: a CoolSolve model
   cannot have two bodies of the same name and `$INCLUDE library:<name>`
   (`CS-FEAT-IMPORT`) does not exist yet; the copy is marked in its comment
   block.
7. **Sign convention kept.** `Q_dot` is the heat transfer *from the hot side*
   (`M_dot_h*(h_h_ex - h_h_su)`), as in TESPy: it is negative when the hot
   side is cooled. The cold-side balance is written
   `M_dot_c*(h_c_ex - h_c_su) = -Q_dot`.
8. **Fluids.** `Water` for the steam and the cooling water (real fluid in EES
   and CoolProp); `Air` for the air streams. EES `Air` is the ideal-gas
   substance (chemical formula) while TESPy uses the CoolProp `air` mixture —
   see *Verification*.
9. **Two occurrences of a variable on the left-hand side** (TESPy writes
   `Q = m*(h_out - h_in)` on both sides) are written as
   `M_dot*(h_ex - h_h_su) = Q_dot`, which the structural analysis of CoolSolve
   accepts (one equation per variable).
10. **`.initials` for the main file.** The off-design block (8 variables) does
    not converge from the default guesses (all 1); `hx_lmtd_ua.initials`
    carries the values of the TESPy run, as the debugging guide prescribes.
    The condenser file converges from the default guesses (71 iterations,
    no `.initials`).
11. **Level.** Score of `docs/taxonomy.md` §3: 70 equations (1), largest block
    8 (1), one `FUNCTION` and the diagram arrays (1), off-design physics
    (1), curated guesses (1) = 5 → level 3, lowered by one to **level 2**:
    the physics is a single explicit set of correlations of one component,
    the pedagogical audience is the applied-thermodynamics course.
12. **State arrays.** `P[i]`, `h[i]`, `T[i]`, `s[i]` are pure post-processing
    (the results are unchanged); the file ends with a newline, without it
    CoolSolve drops the last equation (see the register row).

## Related models

* `CSL-0105` *lmtd_and_f_correction* — the `LMTD` `FUNCTION` and the
  shell-and-tube / air-cooler correction factors `F`.
* `CSL-0014` *hx_constant_pinch* — a heat exchanger sized by an imposed pinch
  (LaboThapPy).
* `CSL-0013` *heat_pump_basic_tespy* — the TESPy tutorial cycle (same source
  library).

## How to run

```bash
coolsolve ./hx_lmtd_ua.eescode              # main file
coolsolve ./hx_lmtd_ua_condenser.eescode   # condensing variant
```