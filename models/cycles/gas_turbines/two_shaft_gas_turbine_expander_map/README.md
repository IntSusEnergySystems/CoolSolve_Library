# Two-shaft gas turbine from compressor and expander data

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0293`

Steady exercise of a two-shaft gas turbine on air burning methane: a
gas-generator shaft (compressor, adiabatic combustor and turbine 1, closed by
a mechanical efficiency of 0.98) and a power turbine on a second shaft running
at a fixed reduced mass flow. The compressor reduced flow and isentropic
efficiency are interpolated from a **map versus the pressure ratio**; the
expander reduced flow and isentropic efficiency from a **second map versus its
pressure ratio**; the combustion products use the mean specific heats of the
ULiège combustion library (CSL-0005, copied in). The model is the library's
example of a **gas generator matched to a mapped power turbine**.

| | |
|---|---|
| **Category** | Cycles and machines › Gas turbines and gas cycles |
| **Fluids** | Air (compressor, power turbine side), CH4 (fuel); N₂, O₂, CO₂, H₂O (products, inside `cpbar`/`gamma`) |
| **Size** | 49 equations after analysis (largest block: 37, once the two copied library routines are inlined); the original equation window has 41 |
| **Source** | ULiège — course *Machines et systèmes thermiques* (MECA0006), repetition R9, exercise 3 (EES file `MSTH-SB-R9-EX3.EES`) |
| **Authors** | Stéphane Bertagnolio |
| **License** | MIT |
| **CoolSolve** | 0.4.0@9768373 — verified against the EES stored solution |

## Problem statement

A two-shaft gas turbine runs on air at **P₁ = 1.01 bar and T₁ = 15 °C**
(`MSTh - SB - R9 - Exercice 3`). The machine burns methane (CH₄, written
`m_f = 1`, `n_f = 4`, LHV = 50 MJ/kg). The exercise provides the
characteristic data of the compressor and of the expander as tables and asks
for the operating point of the machine ("exploitation of the given data"):

- the **compressor** reduced mass flow `M_R_c` and isentropic efficiency
  `epsilon_s_c` as functions of its pressure ratio `r_p_c`;
- the **expander** (turbine 1, driving the compressor on shaft 1) reduced mass
  flow `M_R_e` and isentropic efficiency `epsilon_s_e` as functions of its
  pressure ratio `r_p_e`;
- the **power turbine** (turbine 2, second shaft) runs at the **fixed reduced
  mass flow `M_R_t` = 188** and discharges at the inlet pressure (`P_5 = P_1`);
- the mechanical efficiency of shaft 1 is `eta_m` = 0.98.

The reduced mass flows are the ones written in the window (per bar, with the
textbook `+273`):

$$M_R=\dot m\,\frac{\sqrt{T+273}}{p/10^5}$$

Find the air and fuel mass flows, the compressor pressure ratio and discharge
temperature, the flame temperature, the expander pressure ratio and exit
temperature, and the power-turbine pressure ratio of this point.

## Model

The two 3×3 maps are the embedded lookup tables `Compresseur` and `Expanseur`
of the EES file, shipped as `…-compresseur.csv` and `…-expanseur.csv`:

| `r_p_c` | `M_R_c` | `epsilon_s_c` | | `r_p_e` | `M_R_e` | `epsilon_s_e` |
|---:|---:|---:|---|---:|---:|---:|
| 5.2 | 220 | 0.82 | | 2.5 | 90.2 | 0.84 |
| 5.0 | 236 | 0.83 | | 2.25 | 90.2 | 0.85 |
| 4.8 | 244 | 0.82 | | 2.0 | 88.2 | 0.84 |

They are read in the native keyword form of the window:

```
M_R_c = INTERPOLATE('compresseur','M_R_c','r_p_c',r_p_c=r_p_c)
epsilon_s_c = INTERPOLATE('compresseur','epsilon_s_c','r_p_c',r_p_c=r_p_c)
M_R_e = INTERPOLATE('expanseur','M_R_e','r_p_e',r_p_e=r_p_e)
epsilon_s_e = INTERPOLATE('expanseur','epsilon_s_e','r_p_e',r_p_e=r_p_e)
```

Compressor (isentropic relation with `gamma(m_f,n_f,0,T_1,T_2)`, `f = 0` is
pure air; `+273` as in the original):

$$(T_{2s}+273)/(T_1+273)=(P_2/P_1)^{(\gamma_c-1)/\gamma_c},\qquad
\epsilon_{s,c}(T_2-T_1)=T_{2s}-T_1,\qquad w_c=\bar c_{p,a}(T_2-T_1)$$

with `cp_a = CP(Air,T=T_2)` as written in the window. Adiabatic combustor, the
same five-term balance per kg of air as the other models of the course
(`q_1+q_2+q_3+q_4+q_5 = 0`, sensible enthalpies from a 25 °C reference, no
pressure loss: `P_3 = P_2`); `cp_p_23` and `cp_p_34` come from the `cpbar`
routine of the ULiège combustion library (CSL-0005), `cp_g = CP(CH4,T=T_1)`.
Turbine 1: isentropic expansion with `gamma(m_f,n_f,f,T_3,T_4)`,
`epsilon_s_e` from the map, `w_e = cp_p_34*(T_3-T_4)`. Shaft 1 closes with the
mechanical efficiency `eta_m = w_c/((1+f)*w_e)`, which fixes the flame
temperature. Power turbine: only its reduced flow closes the machine,
`M_R_t = M_dot_p*sqrt(273+T_4)/(P_4/1E5) = 188` — the exercise does not
compute its expansion work or exit temperature, so no state 5 beyond `P_5`
exists in the model.

| Inputs | Value | Outputs (operating point) | Value |
|---|---|---|---|
| `P_1`, `T_1` | 1.01 bar, 15 °C | `M_dot_a` air flow | 13.525 kg/s |
| `eta_m` | 0.98 | `M_dot_f` fuel flow | 0.2098 kg/s |
| `LHV_f` | 50 MJ/kg | `r_p_c`, `epsilon_s_c` (map) | 5.109, 0.8245 |
| `M_R_t` | 188 (kg/s)·√K/bar | `T_2` compressor exit | 219.2 °C |
| maps `compresseur`, `expanseur` | 3 × 3 each | `T_3` flame temperature | 875.5 °C |
| | | `T_4`, `P_4` (turbine 1 exit) | 700.9 °C, 228.0 kPa |
| | | `r_p_e`, `r_p_t` | 2.263, 2.257 |

## How to run

```bash
coolsolve ./two_shaft_gas_turbine_expander_map.eescode
```

Keep `two_shaft_gas_turbine_expander_map.initials` (the solution stored by
EES): **without it the 37-variable block does not converge** (MaxIterations).
The file also needs its two companion tables
(`two_shaft_gas_turbine_expander_map-compresseur.csv` and `…-expanseur.csv`),
since a CoolSolve model only reads the tables named after its own file name.

## Results

`two_shaft_gas_turbine_expander_map.sol` (EES stored values in parentheses):

| Quantity | Value | Quantity | Value |
|---|---:|---|---:|
| `M_dot_a` air flow | 13.5252 kg/s (13.5250) | `T_3` flame temperature | 875.48 °C (875.48) |
| `M_dot_f` fuel flow | 0.20977 kg/s (0.20994) | `T_4` / `T_4_s` | 700.88 / 669.93 °C (700.90 / 669.96) |
| `f` air–fuel ratio | 0.015509 (0.015522) | `P_2` = `P_3` | 516.04 kPa (516.04) |
| `r_p_c` | 5.1093 (5.1093) | `P_4` | 227.99 kPa (228.00) |
| `epsilon_s_c` (map) | 0.82454 (0.82453) | `P_5` | 101 kPa (101) |
| `w_c` | 209.97 kJ/kg (209.97) | `r_p_e` / `r_p_t` | 2.2634 / 2.2574 (2.2634 / 2.2574) |
| `w_e` | 210.98 kJ/kg (210.98) | `M_R_c` / `M_R_e` / `M_R_t` | 227.26 / 90.2 / 188 (227.26 / 90.2 / 188) |
| shaft 1 compressor side | 2.840 MW | shaft 1 turbine side `(1+f)·w_e` | 2.898 MW (ratio 0.98 = `eta_m`) |

The machine compresses 13.5 kg/s of air to 5.11:1, burns 1.55 % of methane in
it to reach 875 °C, and turbine 1 delivers exactly the compressor power
divided by `eta_m` (2.898 → 2.840 MW); the products then cross the power
turbine at the fixed reduced flow 188 down to 228 kPa and out at 101 kPa.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): the model runs on
     Air, so CoolSolve has no T-s/P-h diagram for it (CS-FEAT-DIAGRAM-IDEAL): a
     parametric-sweep plot is expected, e.g. T_3 / M_dot_a / r_p_c versus the
     fixed power-turbine reduced flow M_R_t, or the two maps read by the machine -->

## Verification

The EES file stores the solution of its last run (42 variable names, 41 numeric
values; the name `gamma` has no stored value). Reproduced with this model
(`tools/compare_solution.py`, CoolSolve 0.4.0@9768373):

```
| cp_a | 1026.45 | 1028.42 | 1.91e-03 | **DIFF** |
| cp_g | 2234.17 | 2209.98 | 1.08e-02 | **DIFF** |
| q_2 | 346.79 | 342.757 | 1.16e-02 | **DIFF** |
| T_2 | 219.562 | 219.163 | 1.82e-03 | **DIFF** |
| T_2_s | 183.668 | 183.34 | 1.79e-03 | **DIFF** |
41 common variables, 5 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 8
```

Explanations:

1. **`cp_g` and `q_2` (max 1.16·10⁻²)** — `cp_g = CP(CH4,T=T_1)` differs by
   ~1 % between EES and CoolProp; `q_2 = cp_g*(T_ref-T_1)` carries the same
   ratio (the largest deviations of the comparison). The same deviation was
   recorded for `CSL-0220`, the single-shaft sibling.
2. **`cp_a`, `T_2`, `T_2_s` (≤ 1.91·10⁻³)** — `CP(Air)` is ~0.2 % high in
   CoolProp at these temperatures; the two compressor temperatures inherit
   it. Everything else — flows, `f`, `w_c`, `w_e`, the flame temperature
   `T_3` (875.48 °C both), `T_4`, all pressures, the map reads and `eta_m` —
   agrees within 1·10⁻³, inside the 0.5 % tolerance of `ees_import.md` §11
   for a different equation of state.
3. The eight CoolSolve-only names are the unused outputs of the two `cpbar`
   CALLs (`Q_4_23`, `x_23`, `e_min_23`, `e_23`, `Q_4_34`, `x_34`,
   `e_min_34`, `e_34`); EES stored no values for them.

The lookup tables were checked against the stored solution: the solved
`r_p_c` = 5.109 lies between the nodes 5.0 and 5.2, and linear interpolation
of the table gives `M_R_c` = 227.3 and `epsilon_s_c` = 0.8245 against the
stored 227.255 and 0.824534; likewise `r_p_e` = 2.263 between 2.25 and 2.5
gives `M_R_e` = 90.2 and `epsilon_s_e` = 0.8495 against 90.2 and 0.849465.

## Niche

Nearest models of the library, compared by equations:

- **`CSL-0011`** (*two_shaft_gas_turbine_compressor_map*) — the same two-shaft
  concept of the same course (revision exercise of 2005-12-23), but the
  compressor map is keyed by the reduced speed, the expanders are closed by
  *given* reduced flows and the first-expander efficiency comes from a power
  balance (no mechanical efficiency), the exhaust pressure follows from the
  exhaust temperature, and there is no power-turbine map. Here both maps are
  keyed by pressure ratios, shaft 1 closes with `eta_m` = 0.98, and the power
  turbine is closed by its fixed reduced flow 188.
- **`CSL-0220`** (*gas_turbine_any_regime*) — the single-shaft sibling of the
  same R9 series (exercise 2): one shaft, expander data constant (no map),
  5 % combustor pressure loss, net shaft power. Here two shafts, a mapped
  expander, no pressure loss, and a mechanical efficiency.
- **`CSL-0050`** (*gas_turbine_two_shaft_intercooled_regenerative*) —
  two-shaft architecture with intercooling, regeneration and reheat at
  constant pressure ratio, no maps.

What this model adds: the design-point closure of the SB R9 series with an
**expander performance map** and a **power turbine at the fixed reduced flow
188** (the reduced-regime continuation of the same machine, inventory
`TM-0147`, describes this fixed reduced flow as the choked power turbine),
which no other library model combines.

## Source and attribution

Repetition exercise 3 of the ULiège course *Machines et systèmes thermiques*
(MECA0006), file `MSTH-SB-R9-EX3.EES` (EES X7.458, comments in French). The
author is identified from the file header `MSTh - SB - R9 - Exercice 3`
(`SB` = Stéphane Bertagnolio, same series as `CSL-0220` from exercise 2); the
EES licence stamp of the file is the ULiège Thermodynamics Laboratory one. The
`cpbar` and `gamma` routines are those of the ULiège combustion library
(P. Ngendakumana, 2003), published as the library model `CSL-0005` and copied
here from `CSL-0220`. The model was translated for the library by editing its
comments, never its equations.

Source file (collection of S. Quoilin):
`~/Nextcloud/thermo_models/machines et systemes thermiques/MSTh - Repetitions/TP 09/MSTH-SB-R9-EX3.EES`
(inventory candidate `TM-0146`).

## Conversion log

- **2026-10-24 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already `SI MASS DEG PA C J`, no conversion needed (the
  `$UnitSystem` line is dropped, as in every library model); the EES licence
  tag was removed; the embedded lookup tables `Compresseur` and `Expanseur`
  were renamed `compresseur` and `expanseur` (file-name safety) with their
  equation references updated by the tool; the stored solution carried in the
  binary (42 names, 41 values) was kept as `reference/ees_variables.csv` and
  as the `.initials` file. Comments translated to English, standard header
  added; the provisional-value comments of the original are kept as comments;
  **the 41 equations are unchanged** (checked equation by equation against
  the extraction). Table recovery was checked against the stored solution
  (see *Verification*).
- **2026-10-24 — `cpbar` calls and library routines**: the original calls
  `cpbar` in function position (`cp_p_23=cpbar(m_f,n_f,f,T_ref,T_3)`) while
  the ULiège `cpbar` is a five-output PROCEDURE; both calls are transcribed
  as `CALL cpbar(... : cp_p_23, Q_4_23, x_23, e_min_23, e_23)` — valid EES,
  no equation change, pattern `CSL-0034`/`CSL-0220`, so there is no separate
  `_coolsolve` variant. The `cpbar` PROCEDURE and `gamma` FUNCTION (loaded
  implicitly by EES from a user library, `CS-GAP-INCLUDE`) are copied in a
  marked block from `CSL-0220`, same origin `CSL-0005`, including the 0/0
  guard for coinciding temperatures.
- **Level** — score 5 on the `taxonomy.md` §3 grid (equations < 50: 0;
  largest block 37: 2; procedures/functions: 1; ≥ 3 coupled components: 1;
  curated guesses required: 1) → level 3, lowered by one point: the difficulty
  is pedagogical (a single design-point exercise of the MSTh family, as its
  siblings `CSL-0011` and `CSL-0220`, both level 2) → **level 2**.

## Limitations and CoolSolve gaps

Physical simplifications of the exercise: air and combustion products are
ideal gases with mean specific heats (no temperature dependence inside a
stage), the combustor has no pressure loss and no heat loss, the mechanical
losses of shaft 1 are summarised by the single `eta_m` = 0.98, and the power
turbine enters the closure only through its fixed reduced mass flow 188 —
its work, efficiency and exit temperature are not part of the model (no state
5 beyond `P_5`).

No CoolSolve gap blocks this file: the implicit EES user library is carried
in the file itself (copied routines, as in `CSL-0220`) and the `INTERPOLATE`
calls use the native keyword form (`CS-GAP-INTERP-EES` is closed). A
`.initials` file is required for convergence (see *How to run*).

## Related models

- `CSL-0005` (*cpbar_combustion_products*): the `cpbar` procedure and the
  `gamma` function used by this model, copied in its file.
- `CSL-0011` (*two_shaft_gas_turbine_compressor_map*): the other two-shaft
  gas turbine of the course, closed by expander reduced flows and the
  first-expander power balance instead of maps and a mechanical efficiency.
- `CSL-0220` (*gas_turbine_any_regime*): the single-shaft exercise 2 of the
  same R9 series, from whose file the library routines were copied.
- `CSL-0296` (*regenerative_two_shaft_gas_turbine*): two-shaft design-point
  exercise of the same family with a regenerator, isentropic efficiencies
  instead of expander data.
