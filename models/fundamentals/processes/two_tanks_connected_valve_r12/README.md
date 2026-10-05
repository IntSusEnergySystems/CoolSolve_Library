# Two rigid tanks connected by a valve: change of quality of R12

🟢 **Level 1 · Introductory** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0048`

Two rigid tanks of 200 L each, connected by a valve, initially hold an R12
liquid–vapour mixture at 25 °C in tank A (10 % liquid and 90 % vapour *in
volume*) and nothing in tank B. Opening the valve lets saturated vapour flow from
A to B at constant temperature until the pressures are equal; part of the liquid
evaporates. The model computes how much the quality (vapour mass fraction) of
tank A has changed, and the distribution of the refrigerant between the two
tanks. It is a short, explicit mass/volume balance on a real fluid in the
two-phase dome — a good exercise on the difference between a *volume* fraction
and a *mass* quality.

| | |
|---|---|
| **Category** | Fundamentals › Processes |
| **Fluids** | R12 (real fluid: saturated liquid and saturated vapour at 25 °C) |
| **Size** | 27 equations, largest block 4 (one 2×2 implicit system for `Vol_l`, `Vol_v`) |
| **Source** | ULiège — course *Thermodynamique appliquée* (MECA0002), repetition session 1, exercise 4 (EES file `R1_E4_2022_method_bis.EES`, session 2022-2023) |
| **Authors** | TBD (ULiège, course *Thermodynamique appliquée*; the companion course files name S. Quoilin and the repetition assistants N. Paulus and B. Dechesne) |
| **License** | MIT |
| **CoolSolve** | v0.3.0 — runs; import verified against the EES stored solution (see *Verification*) |

## Problem statement

Two tanks A and B are connected by a valve. Each tank has a volume of 200 L.
Tank A contains R12 at 25 °C and, in volume, 10 % of liquid and 90 % of vapour.
Tank B is empty. The valve is then opened and saturated vapour escapes from A
until the pressure of B reaches that of A. The valve is then closed again. This
operation takes place slowly, so that the temperatures remain at 25 °C during
its whole duration. By how much has the quality in tank A changed as a result of
the process?

## Model

The whole operation is isothermal and slow, so as long as liquid is present the
pressure stays at the saturation pressure of 25 °C; only vapour crosses the
valve, and all the liquid stays in tank A. The unknowns of the problem are
therefore the liquid and vapour fractions of the **whole** volume
`Vol_A + Vol_B`:

- initial quality of tank A, from its initial liquid and vapour volumes:
  $m_{l,A} = V_{l,A}/v_l$, $m_{v,A} = V_{v,A}/v_v$,
  $x_{A,i} = m_{v,A}/m_{tot}$ with $v_l$ and $v_v$ the saturated specific volumes
  of R12 at $T_A$;
- distribution at the end of the operation: two equations for two unknowns,
  $V_{tot} = V_l + V_v$ and $m_{tot} = m_l + m_v$, closed by the definition of
  the specific volumes, $V_l = m_l v_l$ and $V_v = m_v v_v$ (a 2×2 implicit
  block);
- final state of tank A: the vapour left in A has volume $V_v - V_B$, so
  $m_{v,A,f} = (V_v - V_B)/v_v$, $m_{l,A,f} = V_l/v_l$ and
  $x_{A,f} = m_{v,A,f}/m_{A,f}$;
- change of quality $\Delta x_A = 100\,(x_{A,f} - x_{A,i})$, in percentage points.

Only two property calls are needed: the saturated liquid and saturated vapour
specific volumes at 25 °C.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `Vol_A`, `Vol_B` tank volumes | 0.2 m³ each | `x_A_i` initial quality of A | 0.2018 (20.2 %) |
| `T_A` process temperature | 25 °C | `x_A_f` final quality of A | 0.2685 (26.8 %) |
| `f_m_l_A`, `f_m_v_A` initial volume fractions | 0.1, 0.9 | **`Deltax_A` change of quality** | **+6.67 percentage points** |
| | | `m_B_f` mass transferred to B | 7.366 kg |
| | | `dVol_A`, `dm_tot` closure checks | 1.2·10⁻¹⁵ m³, −1.0·10⁻¹² kg |

## How to run

Open `two_tanks_connected_valve_r12.eescode` in the CoolSolve GUI and press
*Solve*, or from a terminal:

```bash
coolsolve ./two_tanks_connected_valve_r12.eescode
```

Every variable is fixed by an explicit equation apart from the single 2×2 block,
which converges in 2 iterations from a cold start: no guess values
(`.initials`), no solver settings and no runnable variant are needed.

## Results

| Variable | Value | Unit |
|---|---:|---|
| `v_l` specific volume of saturated liquid at 25 °C | 7.6276·10⁻⁴ | m³/kg |
| `v_v` specific volume of saturated vapour at 25 °C | 2.7153·10⁻² | m³/kg |
| `m_tot` initial total mass of R12 | 32.850 | kg |
| `x_A_i` initial quality in A | 0.20180 | – |
| `Vol_l`, `Vol_v` liquid / vapour volume at the end | 0.014219, 0.385781 | m³ |
| `m_l`, `m_v` liquid / vapour mass at the end | 18.642, 14.208 | kg |
| `Vol_v_A_f` vapour volume left in A | 0.185781 | m³ |
| `m_A_f` mass left in A | 25.484 | kg |
| `x_A_f` final quality in A | 0.26848 | – |
| **`Deltax_A` change of quality in A** | **+6.668** | percentage points |
| `dVol_A`, `dm_tot` closure checks | 1.2·10⁻¹⁵, −1.0·10⁻¹² | m³, kg |

The quality of tank A **increases by 6.67 percentage points** (from 20.2 % to
26.8 %): part of the liquid evaporates to fill tank B with vapour, so the mass
fraction of vapour in A rises even though the vapour *volume* of A barely
changes. The model closes on both conservation checks, `dVol_A` (volume of A) and
`dm_tot` (total mass of A + B), to round-off. The 10 % liquid fraction given *in
volume* corresponds to a mass quality of 20.2 % because saturated liquid R12 is
35.6 times denser than its saturated vapour (1311 kg/m³ against 36.83 kg/m³).

All the states of this process lie on the saturation line of R12 at 25 °C, so
there is no path to draw on a P-h or T-s diagram; the figure of the library is a
parametric sweep (CoolSolve *Parametric* tab), see the placeholder below.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): parametric sweep of
     Deltax_A vs T_A (or vs f_m_l_A), figures/two_tanks_connected_valve_r12_sweep.png -->

## Verification

Compared with the solution stored by EES in the source file
(`compare_solution.py … --ees-units`, the reference temperature converted from K
to °C): **27 common variables, 12 differ (rtol=0.001)**, largest relative
deviation **1.97·10⁻²** (`Deltax_A`).

| Variable | EES (converted) | CoolSolve | rel. diff |
|---|---:|---:|---:|
| `v_l` [m³/kg] | 7.6281972·10⁻⁴ | 7.6275905·10⁻⁴ | 8.0·10⁻⁵ |
| `v_v` [m³/kg] | 2.6866255·10⁻² | 2.7153183·10⁻² | 1.06·10⁻² |
| `m_tot` [kg] | 32.91837 | 32.84966 | 2.09·10⁻³ |
| `x_A_i` | 0.2035294 | 0.2017999 | 8.50·10⁻³ |
| `Vol_l` [m³] | 0.01415541 | 0.01421943 | 4.50·10⁻³ |
| `Vol_v` [m³] | 0.38584459 | 0.38578057 | 1.66·10⁻⁴ |
| `m_v` [kg] | 14.36168 | 14.20756 | 1.07·10⁻² |
| `x_A_f` | 0.2715465 | 0.2684796 | 1.13·10⁻² |
| `m_B_f` [kg] | 7.444283 | 7.365619 | 1.06·10⁻² |
| `Deltax_A` | 6.801712 | 6.667972 | 1.97·10⁻² |

**Origin of the deviation.** Every difference is driven by one property: the
saturated vapour specific volume of R12 at 25 °C (`v_v`, +1.06 % in CoolProp
with respect to EES); the saturated liquid side (`v_l`) agrees to 8·10⁻⁵. The
other deviations are that 1.06 % propagated through the mass and volume
balances (`Vol_l`, `m_l` 4.6·10⁻³; `Vol_v` only 1.66·10⁻⁴, because the liquid
carries 14 L of the 0.4 m³ and the vapour carries the rest) and amplified in the
results built on them (`x_A_i` 8.5·10⁻³) and above all in `Deltax_A`, a
*difference* of two qualities: 0.0667 against 0.0680, i.e. 1.97·10⁻² of a much
smaller number. Substituting the two EES values of `v_l` and `v_v` into the
model reproduces the stored EES solution exactly: **27 common variables, 6
differ at rtol=1e-12, largest relative deviation 2.09·10⁻¹⁰** — the
transcription of the equations is therefore exact and the whole deviation is an
equation-of-state difference between EES and CoolProp. 25 °C is 14 K below the
critical temperature of R12 (39.4 °C), where the saturated vapour density is at
its most sensitive to the formulation used; ees_import.md §11 allows *up to a
few %* for that case. The EES file stores `dVol_A` = 0 exactly; CoolSolve gives
1.2·10⁻¹⁵ m³.

**Additional reference.** The course folder holds a Python/CoolProp solution of
the same exercise of the same session (`Python/ThAp21_R01E04.py`), which solves
the problem in two different ways (a 4×4 linear system for the liquid/vapour
distribution, then a mean-density step to get the quality of tank A). Reproducing
that first method by hand with the specific volumes of the CoolSolve solution
gives `m_tot` = 32.849657 kg, `x_A_i` = 0.201800 and `x_A_f` = 0.268480, i.e.
the CoolSolve results to all printed digits, so the two models are
algebraically equivalent and use the same (CoolProp) R12 properties. The script
itself could not be run here (no CoolProp module in this environment) and no
number of it is used as a reference.

## Source and attribution

Solution of repetition exercise 4 (session 1) of the ULiège course
*Thermodynamique appliquée* (MECA0002), a session on properties and processes of
real fluids; the exercise asks by how much the quality in tank A changes when a
valve between two tanks is opened. The EES file names no author (its `{$ID$}`
tag is the laboratory's student/staff licence, and the folder `R1` carries no
initials); the companion course files attribute the session to the repetition
assistants N. Paulus and B. Dechesne (course by S. Quoilin) — to be confirmed by
the maintainer. The companion Python solution of the same exercise is signed
with initials only, which are not reproduced here.

Source file (EES X10.836, comments in French), collection of S. Quoilin:
`~/Nextcloud/thermo_models/thermodynamique appliquee/2022-2023/R1/R1_E4_2022_method_bis.EES`
(inventory candidate `TM-0382`, representative of the 5-file duplicate group
`DG-0091`; see *Decisions* below).

## Decisions on the duplicate group (inventory `DG-0091`)

The group is one exercise in five files. The equations were compared after
stripping the comments and the blank lines:

| Row | File | Equations | Decision |
|---|---|---|---|
| `TM-0382` | `2022-2023/R1/R1_E4_2022_method_bis.EES` | representative (27) | `added` → `CSL-0048` |
| `TM-0381` | `2022-2023/R1/R1_E4_2022.EES` | identical to `TM-0382` | `duplicate` of `CSL-0048` |
| `TM-0386` | `2022-2023/R1/save/R1_E4_2022.EES` | identical to `TM-0382` | `duplicate` of `CSL-0048` |
| `TM-0387` | `2022-2023/R1/save/R1_E4_2022_method_bis.EES` | identical to `TM-0382` | `duplicate` of `CSL-0048` |
| `TM-0509` | `2017-2018/THD10_R01.zip!/THD10_R01/SBorguet/R1_E4_2_borguet.EES` | same 27 equations, only `T_A = 25,0[K]+273,15 [K]` written `T_A = 25,0[°C]`; same stored results (25 °C) | `duplicate` of `CSL-0048` (an earlier session of the same exercise, no change of equations, assumptions or closure) |

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository): EES
  X10.836, 27 variable records (the stored solution), no lookup or parametric
  table, no external function (only `VOLUME(R12,T=…,x=…)`); `{$ID$}`, `{$PX$96}`
  and `{$ST$OFF}` tags removed, no NUL byte (the equations are stored as plain
  text, so `CS-BUG-EXTRACT-NUL` does not apply).
- **Unit system** `SI MASS DEG KPA K KJ` converted **by hand** to
  `SI MASS DEG PA C J`. The only quantity that changes is the process
  temperature: `T_A = 25.0 [C]` (298.15 K in the original, kept in the comment).
  The volumes were already in m³, the masses in kg and no pressure or energy
  appears in the equations, so no other conversion is needed; the `$UnitSystem`
  directive was deleted. The initial value of `T_A` in `<model>.initials`
  (298.15) would have been converted to 25; in the end no `.initials` file is
  shipped, the model converging in 2 iterations from a cold start.
- **Comments translated** to English, paraphrasing the French original (its note
  on the pressure staying at the saturation pressure of 25 °C, its note that only
  vapour crosses the valve, its two check equations). Section titles in the
  `"!…"` display form, standard header added. Equations otherwise unchanged.
- **Variable names kept**, including `f_m_l_A` / `f_m_v_A`, whose name suggests
  mass fractions while the original uses them (and its own comment, and the
  companion Python solution: `# titre en volume`) as *volume* fractions; the
  comment of each of the two lines says so. No variable was renamed.
- **No state-point arrays added**: all the states of the process lie on the
  saturation line of R12 at 25 °C, so there is no thermodynamic path to overlay
  on a P-h or T-s diagram (figure = parametric sweep, as for the other
  non-cycle models).
- **CoolSolve limitation met on the native line**: `T_A = 25,0[K]+273,15 [K]`
  (unit annotation on a *sub-expression*, valid EES, used by 35 EES files of the
  collection, 33 of them in *thermodynamique appliquée*) is a parse error in
  CoolSolve, registered as `CS-GAP-UNIT-SUBEXPR`.
  The allowed edit — the manual unit conversion of workflow §3 step 4 — removes
  it, so the native file of the library is not blocked and the gap is **not** in
  `missing_features`; the line is not valid CoolSolve as it stands in the
  original file, only the converted `T_A = 25.0 [C]`.
- **Level**: equations 27 (< 50 → 0), largest algebraic block 4 (≤ 5 → 0),
  structure: no function, procedure or array (0), no multi-zone or
  discretisation and fewer than three coupled components (0), no semi-empirical,
  off-design or dynamic physics (0), no curated guesses, simplified-model
  bootstrap, *Try Harder* or `coolsolve.conf` (0) → score 0 → level 1.

## Limitations and CoolSolve gaps

- The model assumes what the statement says: the process is slow enough to stay
  isothermal, tank B is adiabatic and contains nothing but saturated vapour when
  the valve is closed, tank A keeps all its liquid and the pressure stays at the
  saturation pressure of 25 °C. Real losses of the valve (pressure drop, heat
  transfer through the walls) are not modelled, as in the original.
- All the results scale with the saturated properties of R12 at 25 °C, 14 K
  below its critical point; the ~1 % difference between the EES and CoolProp
  saturated vapour densities is the accuracy limit of the model as imported (see
  *Verification*).
- No CoolSolve gap blocks this model (see `CS-GAP-UNIT-SUBEXPR` in the conversion
  log, removed here by the unit conversion).

## Related models

- `CSL-0044` (*rigid tank with a water–liquid mixture*): the same rigid-tank /
  saturation / quality physics on a single tank with water.
- `CSL-0003` (*evaporation of liquid methane in a tank*): evaporation in a tank
  of a real fluid, same course family and same import route.
- `CSL-0045` (*steam turbine exergy balance*): another model of the same course
  (*Thermodynamique appliquée*, MECA0002) and session series, imported the same
  way.
- `CSL-0057` *two_tanks_max_work_air*: two rigid vessels again, this time as
  an ideal-gas maximum-work (exergy) problem, same course and import route.
