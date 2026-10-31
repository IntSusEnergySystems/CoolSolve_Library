# Local pressure loss of curved bends: Idelchik coefficients (function library)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0316`

EES `FUNCTION` library of the local-loss coefficient of circular pipe bends
(elbows) of [LaboThapPy](https://github.com/PyLaboThap/LaboThapPy), itself a port
of the Idelchik-based `CurvedBend_LDP` of the Modelica Dissipation library: the
coefficient `zeta` depends on the bend angle `delta`, the radius ratio `R0/d_hyd`,
the Reynolds number (laminar, intermediate and high-Re branches blended with a
cubic step) and the wall roughness (correction factor `CF_fri` from the friction
of the bend arc). The pressure drop is `dP = zeta_tot·ρ·v²/2`, for a single-phase
flow or for a two-phase inlet through a mixture density. One `FUNCTION` per
element; the demonstration program calls them for three flows (water, water,
two-phase R410A), for the coefficient tables and for a Reynolds-number sweep.

| | |
|---|---|
| **Category** | Heat transfer › Pressure drop |
| **Fluids** | none in the functions; the demonstration uses Water and R410A |
| **Size** | 146 equations after analysis (largest block: 1); 14 functions |
| **Source** | [`LaboThapPy`](https://github.com/PyLaboThap/LaboThapPy), commit `f03f7f47`, file `labothappy/correlations/pressure_drop/local_losses/curved_elbow.py`; inventory row `LTP-029` of `sources/labothappy/inventory.csv` |
| **Authors** | Elise Neven (the `curved_elbow.py` module); the correlation is I. E. Idelchik's |
| **License** | MIT (original: Apache-2.0, `LICENSE.txt` of LaboThapPy) |
| **CoolSolve** | 0.4.0@9768373 — **verified** against a Python re-run of the source (95 values, max deviation 4.4·10⁻¹³) |

## Niche

The library had only *constant* fitting coefficients for elbows (`K` per fitting
type from a lookup table, independent of the flow, in `CSL-0158`) and the
straight-pipe friction and two-phase drops of `CSL-0130` / `CSL-0018`. This
model adds the **geometry- and Reynolds-dependent loss coefficient of a bend**
(angle, `R0/d`, roughness, laminar to turbulent) and a homogeneous two-phase
bend. Nearest models: `CSL-0130` (straight pipes, same source library, other
physics) and `CSL-0158` (fixed `K` of fittings): neither computes `zeta` of a
bend from its geometry.

## Problem statement

For a circular bend (inner diameter `d_hyd`, centre-line radius `R0`, deflection
angle `delta`, roughness `K`) carrying a mass flow `m_dot` of a fluid of density
`ρ` and viscosity `μ`, find the pressure drop. Adiabatic, constant diameter, no
elevation change (as in the original).

## Model

With `R0_d = R0/d_hyd`, `Re = |m_dot|/A·d_hyd/μ` (floor of 1), `A = π·d_hyd²/4`:

| EES `FUNCTION` | Content (as in the original) |
|---|---|
| `step_smoother(x0,x1,x)` | 0 for `x ≤ x0`, 1 for `x ≥ x1`, `t²(3−2t)` between, `t=(x−x0)/(x1−x0)` |
| `A1_elbow(delta)` | `A1 = 0.95·sin²(δ/2) + 2.05·sin⁴(δ/2)` |
| `A2_elbow(R0_d)` | 600 (`R0/d>2`), 1000 (`>1`), 3000 (`>0.7`), 6000 (`>0.55`), 4000 below |
| `B1_elbow(R0_d)` | `0.21·(R0/d)^−0.5` for `R0/d ≥ 1`, `0.21·(R0/d)^−2.5` below |
| `k_Re_elbow(Re,R0_d)` | `11.5/Re^0.19` (`R0/d>0.7`), `5.45/Re^0.131` (`0.55 ≤ R0/d ≤ 0.7`), `1+4400/Re` below |
| `Re_lam_limit_elbow(K,d)` | `min(6500, max(100, 754·exp(0.0065/max(K/d, 0.007))))` |
| `Re_elbow(m_dot,d,ρ,μ)` | Reynolds number as above |
| `f_Swamee_Jain_elbow(K,d,Re)` | `0.25/[log10(K/(3.7d)+5.74/Re^0.9)]²` (same formula as `f_Swamee_Jain` of `CSL-0130`, copied under another name because function names are unique in the library and `$INCLUDE` is not available) |
| `zeta_LOC_elbow(…,mode)` | `zeta_base = A1·B1`; `zeta_lam = A2/Re + zeta_base`; `zeta_inter = k_Re·zeta_base`; `zeta_mid = (1−s_lam)·zeta_lam + s_lam·zeta_inter`; `zeta_LOC = (1−s_turb)·zeta_mid + s_turb·zeta_base` |
| `CF_fri_elbow(zeta_LOC,…,mode)` | `CF_fri = 1 + s·min(1.4, f·L_arc/(d·zeta_LOC))`, `L_arc = |δ|·π/180·R0` |
| `zeta_tot_elbow(…,mode)` | `zeta_tot = max(10⁻¹², CF_fri)·zeta_LOC` |
| `dP_elbow(…,mode)` | `dP = zeta_tot·ρ·v²/2`, `v = |m_dot|/(ρA)` |
| `rho_mix_elbow(x,ρ_l,ρ_v)` | `α = 1/(1+(ρ_v/ρ_l)(1−x)/x)`, `ρ = 1/(α/ρ_v + (1−α)/ρ_l)` (formula of the original) |
| `dP_elbow_two_phase(…,x,ρ_l,ρ_v,μ_l,…)` | `dP_elbow` with `ρ = rho_mix_elbow`, `μ = μ_l` (saturated liquid), as the two-phase branch of the original |

Arguments (SI): `d_hyd`, `R0`, `K` `[m]`, `delta` `[deg]`, `rho`, `rho_l`, `rho_v`
`[kg/m³]`, `mu`, `mu_l` `[Pa·s]`, `m_dot` `[kg/s]`, `x` `[-]`, result `dP` `[Pa]`.
The Python dispatch (`EPS < x < 1−EPS` → two-phase branch, otherwise single-phase
properties of the `AbstractState`) is the caller's choice here: call `dP_elbow`
with the single-phase `ρ`, `μ`, or `dP_elbow_two_phase`.

### The `mode` argument (what differs from the source, and why)

The original calls the step helper as `stepsmoother(Re, a, b)`, while the helper
is defined as `stepsmoother(x0, x1, x)` (zero below `x0`, one above `x1`): the
Reynolds number is passed as `x0` instead of `x`. As written, the three calls
therefore behave as hard switches in the wrong places:

* the weights give `zeta_LOC = zeta_base` for every `Re < 3·10⁵`, i.e. the laminar
  branch `A2/Re + zeta_base` and the intermediate branch `k_Re·zeta_base` are
  **never used** below `Re = 3·10⁵` (above it `zeta_LOC = A2/Re + zeta_base`,
  a small term and a jump at `Re = 3·10⁵`);
* the roughness weight is 0 for `Re ≥ Re_lam` (1908 for `K/d ≤ 0.007`), i.e. the
  roughness correction acts only below that Reynolds number.

**`mode = 1`** reproduces the source exactly as written (verified numerically,
below). **`mode = 2`** is *this model's reading of the documented intent*
(docstring: laminar branch below `Re_transition`, intermediate branch up to
`4·10⁴`, high-Re branch above `3·10⁵`, roughness correction "0 in laminar, 1 in
turbulent"): the same weights with `x = Re` in the third position,
`step_smoother(Re_lam, 4E4, Re)`, `step_smoother(4E4, 3E5, Re)` and, for the
roughness, `step_smoother(Re_lam, 6500, Re)`. The roughness interval is a guess
(the call in the source, `(Re, 6500, Re_lam)`, would have its upper limit below
its lower one once reordered); mode 2 is **not** taken from the source and **not**
checked against the Modelica library or the handbook: it was only compared with
a copy of the source with the three calls reordered (`work/elbow/ce_fixed.py`).
Use `mode = 1` to reproduce LaboThapPy, `mode = 2` to see the behaviour the
documentation describes.

### Two-phase mixture density

`rho_mix_elbow` keeps the formula of the original, `1/(α/ρ_v + (1−α)/ρ_l)` with the
homogeneous void fraction `α`, which is not the homogeneous density
`1/(x/ρ_v + (1−x)/ρ_l)` (`α` is a volume fraction, so `α/ρ_v` has no direct
physical meaning). For R410A at 400 kPa, `x = 0.9` the original formula gives
15.46 kg/m³ against 17.13 kg/m³ for the homogeneous density (−9.8 %, recomputed
from the `.sol`: `rho_mix_C`, `rho_hom_C`). `CSL-0130` (`rho_two_phase_homogeneous`)
carries the same formula. It is reproduced for fidelity; `rho_hom_C` in the
demonstration gives the homogeneous value for comparison.

## How to run

```bash
coolsolve ./local_losses_idelchik_elbows.eescode
```

The demonstration program after the definitions solves without iteration
(`Solver: SUCCESS (0 iterations)`, 146 equations, all blocks of size 1). It is the
regression baseline `local_losses_idelchik_elbows.sol`. Until CoolSolve supports
`$INCLUDE library:…` (`CS-FEAT-IMPORT`), a model that needs the functions copies
the definitions in a block `{--- Library functions copied from CSL-0316 ---}`.

## Results

Demonstration cases (values from the `.sol`):

| Case | Quantity | mode 1 | mode 2 |
|---|---|---:|---:|
| A — water 26.85 °C, 3 bar, 10 mm, 90°, `R0/d = 1`, `K` = 45 µm, 0.1 kg/s (`Re` = 14 914) | `zeta_LOC` | 0.20738 | 0.40194 |
| | `CF_fri` | 1.000 | 1.1388 |
| | `zeta_tot` | 0.20738 | 0.45772 |
| | `dP` | 168.66 Pa | 372.26 Pa |
| B — water 101325 Pa, 10⁵ J/kg, 10 mm, 90°, `R0 = 0.5 m`, smooth, 0.5 kg/s (`Re` = 69 621) | `zeta_tot` | 0.029327 | 0.096320 |
| | `dP` | 595.88 Pa | 1957.06 Pa |
| C — R410A 400 kPa, `x` = 0.9, 10 mm, 90°, `R0 = 0.5 m`, 0.05 kg/s (`Re` = 30 191) | `dP` | 384.32 Pa | 1503.01 Pa |

Coefficients (case D): `A1` = 0.072837 / 0.183090 / 0.987500 / 3.0 for
δ = 30 / 45 / 90 / 180°; `A2` = 600 / 1000 / 3000 / 6000 / 4000 for
`R0/d` = 3 / 1.5 / 0.85 / 0.6 / 0.4; `B1` = 0.12124 (`R0/d` = 3), 2.0752 (0.4);
`Re_lam` = 1908.3 (`K/d` = 0 and 0.005) and 858.7 (`K/d` = 0.05).

Case E — `zeta_tot` (mode 1 / mode 2) at `Re` = 300 / 10³ / 3·10³ / 10⁴ / 10⁵ /
5·10⁵, 20 mm bend, 90°, `K` = 0.1 mm:

| `R0/d` | 300 | 10³ | 3·10³ | 10⁴ | 10⁵ | 5·10⁵ |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 0.148 / 2.120 | 0.132 / 0.720 | 0.120 / 0.353 | 0.120 / 0.367 | 0.120 / 0.299 | 0.121 / 0.264 |
| 1.5 | 0.209 / 3.503 | 0.181 / 1.169 | 0.169 / 0.519 | 0.169 / 0.368 | 0.169 / 0.286 | 0.171 / 0.242 |
| 0.85 | 0.338 / 10.31 | 0.318 / 3.311 | 0.311 / 1.319 | 0.311 / 0.664 | 0.311 / 0.432 | 0.317 / 0.352 |
| 0.6 | 0.762 / 20.74 | 0.749 / 6.744 | 0.744 / 2.747 | 0.744 / 1.365 | 0.744 / 0.906 | 0.756 / 0.773 |
| 0.4 | 2.062 / 15.38 | 2.053 / 6.049 | 2.049 / 3.391 | 2.049 / 2.532 | 2.049 / 2.147 | 2.057 / 2.069 |

Mode 1 is constant (`A1·B1`) from `Re` = 3·10³ to 10⁵ (the same value in three
columns) and rises by `A2/Re` only at 5·10⁵; the small excess at `Re` = 300 and
10³ is the roughness correction (`Re < Re_lam`). Mode 2 falls with `Re` (laminar
`A2/Re` term, `k_Re` intermediate regime) and is slightly non-monotonic for
`R0/d` = 3 between 3·10³ and 10⁴, where the roughness correction switches on.

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): zeta_tot versus Re for the five radius
     ratios, mode 1 and mode 2 (data of case E) -->

## Verification

**Reference.** The Python source itself, commit `f03f7f47` of the local clone,
re-run in a throw-away virtual environment under `work/elbow` (CoolProp 6.6.0,
the version pinned in the repository's `requirements.txt`; the clone was used
through `PYTHONPATH`, not installed). Script `work/elbow/ref_elbow.py` calls
`compute_zeta_LOC`, `compute_cf_fri`, `compute_zeta_tot`,
`compute_idelchik_coefficients`, `compute_re_lam_transition` and
`pressure_drop_curved_elbow` (the last one with `AbstractState` objects for cases
A, B, C, i.e. with CoolProp properties) for the same inputs as the demonstration
program (95 values; mode 2 values from the reordered copy `ce_fixed.py`).
Comparison with `CoolSolve/tools/compare_solution.py … --rtol 1e-6`:

```
95 common variables, 0 differ (rtol=1e-06); only in EES: 0; only in CoolSolve: 52
```

(the 52 values only in CoolSolve are inputs and intermediate quantities). The
largest relative deviation over the 95 values is **4.4·10⁻¹³** (`zt_g3_m2[1]`),
round-off. Mode-1 values of cases A, B, C: `dP_A1` 168.6575 Pa, `dP_B1`
595.8778 Pa, `dP_C1` 384.3203 Pa, identical to the Python in the printed digits.

The source has no `__main__`, example script or test: its own example is the
docstring of `pressure_drop_curved_elbow` (water at 300 K, 3 bar, `D = 0.01`,
`R0 = 0.01`, `δ = 90°`, `K = 45 µm`, 0.1 kg/s), which prints no value. **Executed
as written, it calls `AS.update(CP.PT_INPUTS, 300, 3e5)`, but CoolProp's
`PT_INPUTS` takes (P, T)**: the state is then P = 300 Pa, T = 3·10⁵ K,
ρ = 2.2·10⁻⁶ kg/m³, and the function returns 7.76·10¹⁰ Pa (run in this
environment, CoolProp 6.6.0 and 8.0.0 alike). Case A is that example with the
arguments in the right order (`dP_A1` = 168.66 Pa). Case B uses the parameters of
the elbow of `labothappy/component/Examples/pipe/pipe_example.py` (the function
called for the elbow alone: the `Pipe` component itself was not run), case C the
two-phase conditions of the same file (its `solve()` is commented out in the
source).

**Not checked.** The Idelchik handbook, the Modelica `CurvedBend_LDP` and the
VDI-Wärmeatlas were not consulted: coefficients are those of the Python source.
Mode 2 is checked only against the reordered copy of the Python, not against a
physical reference.

## Source and attribution

* **Original code**: Elise Neven, LaboThapPy (ULiège Thermodynamics Laboratory),
  <https://github.com/PyLaboThap/LaboThapPy>, commit `f03f7f47`, file
  `labothappy/correlations/pressure_drop/local_losses/curved_elbow.py` (history of
  the file: Elise Neven), Apache-2.0 (`LICENSE.txt`); the elbow component is
  `labothappy/component/pipe/curved_elbow.py`. Local clone `~/git/LaboThapPy`.
  The helper `stepsmoother` is `labothappy/toolbox/helper_function/step_smoother.py`
  and the Swamee-Jain factor `friction_factor_swamee_jain` of
  `labothappy/correlations/pressure_drop/pipe_DP.py` (same commit).
* **Scientific basis** (cited by the source, not consulted here): I. E. Idelchik,
  *Handbook of Hydraulic Resistance: Coefficients of Local Resistance and of
  Friction*, Hemisphere Publishing, 1986 (3rd ed. 2006); D. S. Miller, *Internal
  Flow Systems*, 2nd ed., 1984; VDI-Wärmeatlas, 9th ed., Springer, 2002, section
  Lac 6; Modelica Standard Library,
  `Modelica.Fluid.Dissipation.PressureLoss.Bend.CurvedBend_LDP`. Swamee, P. K. and
  A. K. Jain, J. Hydraulics Div. ASCE 102(HY5), 1976.
* The translation is published under the CoolSolve_Library MIT license
  (decision D3).

## Conversion log

- **2026-10-31 — translation (card C-364, inventory row `LTP-029`)**: the Python
  helpers become one `FUNCTION` each; `max(EPS, …)` guards and the Reynolds floor
  of 1 are kept; the dictionary of `compute_idelchik_coefficients` is split into
  `A1_elbow`, `A2_elbow`, `B1_elbow` (`C1 = 1` stays a factor in `zeta_LOC_elbow`);
  the `AbstractState` property lookup of `pressure_drop_curved_elbow` is left to
  the caller (`dP_elbow`: single-phase `ρ`, `μ`; `dP_elbow_two_phase`: saturated
  properties, `μ_l`).
- **`mode` argument added**: 1 = as the original, 2 = reordered `stepsmoother`
  arguments (described above); not in the source.
- **Duplicated names**: `f_Swamee_Jain_elbow` is `f_Swamee_Jain` of `CSL-0130`
  under another name (unique function names).
- **Level**: function library with 14 functions, regime blending, piecewise
  coefficients and a two-phase extension, verified against a source re-run; same
  level as the sibling function library `CSL-0130` → level 2.

## Limitations and CoolSolve gaps

No CoolSolve gap: the file solves as is (`System square: Yes`, 146 equations).
The correlation is limited to what the source states: circular bend, adiabatic,
constant diameter, no elevation; the homogeneous two-phase treatment and its
mixture-density formula are discussed above. The behaviour of mode 1 reflects an
apparent argument-order error of the source, not a CoolSolve limitation.
Reproducer of the source behaviour (LaboThapPy `f03f7f47`):

```python
import math
from labothappy.correlations.pressure_drop.local_losses.curved_elbow import compute_zeta_LOC as z
rho, mu, d = 1000, 1e-3, 0.02; m = lambda Re: Re*mu*math.pi*d*d/4/d
print(z(d, d, 90, 1e-4, rho, mu, m(1e3)), z(d, d, 90, 1e-4, rho, mu, m(1e5)))   # both 0.207375
```

## Related models

- `CSL-0130` (*pipe_pressure_drop_correlations*): same source library; friction
  factors and two-phase drops of straight pipes (the Swamee-Jain factor used for
  the roughness correction is the same formula).
- `CSL-0158` (*gas_pipe_insulated_pressure_drop*): fixed `K` coefficients of
  fittings (elbows included) from a table, independent of the flow.
- `CSL-0018` (*pipe_pressure_drop_colebrook*): Colebrook-White friction factor of
  a straight pipe.
