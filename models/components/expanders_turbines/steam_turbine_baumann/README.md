# Steam turbine with Baumann wet-expansion efficiency correction

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ✅ **Verified** &nbsp;|&nbsp; `CSL-0314`

Isentropic efficiency of a steam turbine whose expansion ends in the vapour dome,
translated from the TESPy class `SteamTurbine`. The efficiency `eta_s_dry` of the
dry expansion is reduced, for the part of the expansion that is wet, by the Baumann
rule `eta_s = eta_s_dry*(1 - alpha*y_m)`, where `y_m` is the mean wetness of the
wet part. For a superheated inlet TESPy locates the point where the dry expansion
meets the saturated-vapour line with an inner root search (`brentq`); here that
point is two simultaneous equations. The file solves seven cases of the TESPy
documentation and tests.

| | |
|---|---|
| **Category** | Components › Expanders and turbines |
| **Fluids** | Water |
| **Size** | 140 equations (largest block: 4) |
| **Source** | TESPy `src/tespy/components/turbomachinery/steam_turbine.py` ([oemof/tespy](https://github.com/oemof/tespy), commit `19425523`) |
| **Authors** | Francesco Witte, tlmerbecks (GitHub handle, history of the file) |
| **License** | MIT |
| **CoolSolve** | v0.4.0 — runs; verified against a re-run of TESPy (see *Verification*) |

## Problem statement

A steam turbine expands steam from superheated conditions to a pressure at which
the steam is wet (docstring: 10 kg/s at 250 °C and 20 bar to 0.1 bar). The
isentropic efficiency of the same machine working dry is 0.9. What is the outlet
quality, the overall isentropic efficiency and the power when the efficiency of the
wet part is penalised by the Baumann rule?

## Model

Notation of the original (`eta_s_wet_func`). Inlet `(P_in, h_in)`, outlet `P_out`.

1. **Saturation crossing of the dry expansion** (TESPy `find_sat`): an expansion
   to pressure `P_x` with the dry efficiency ends on the saturated-vapour line:
   `h_x = h_in - eta_s_dry*(h_in - h(P_x, s_in))` and `h_x = h(P_x, x=1)`.
   Unknowns `P_x`, `h_x`, `h(P_x,s_in)`: three equations (TESPy: `brentq` on the
   pressure fraction).
2. **Wet part** from `(P_x, h_x)`, a saturated vapour, to `P_out`:
   `h_out,s = h(P_out, s(P_x, x=1))`, `y_m = 1 - (1 + x_out)/2`,
   `eta_wet = eta_s_dry*(1 - alpha*y_m)`, `h_out = h_x - eta_wet*(h_x - h_out,s)`,
   `x_out = quality(h_out, P_out)`. The mean wetness `y_m` depends on the outlet, so
   `h_out` and `x_out` are solved simultaneously (TESPy: Newton on the whole network).
3. **Overall results**: `eta_s = (h_in - h_out)/(h_in - h(P_out, s_in))`
   (TESPy `calc_eta_s`) and `W_dot = m_dot*(h_in - h_out)` (positive, produced).
4. **Wet inlet** (TESPy branch `state == "tp"`, case 7): no crossing; the rule is applied
   to the whole expansion with `y_m = ((1-x_in) + (1-x_out))/2`, `eta_s = eta_s_dry*(1 - alpha*y_m)`.

The three TESPy branches are: wet inlet (case 7), superheated inlet with a wet
outlet (cases 1–6, the one that is new), superheated inlet and outlet with the dry expansion staying
above saturation (`eta_s = eta_s_dry`, no equation to solve; not included). The
variable `margin = P_x - P_out` must be positive for the wet-outlet equations to
be valid.

Cases (`DUPLICATE` over cases 1–5, outlet pressure given; cases 6–7 outlet quality given,
outlet pressure unknown):

| Case | Inlet | Outlet | `alpha` | Origin |
|---|---|---|---:|---|
| 1 | 250 °C, 20 bar | 0.1 bar | 0.4 | docstring state, `alpha` at the lower limit of TESPy |
| 2 | 250 °C, 20 bar | 0.1 bar | 1.0 | docstring example, `P` = -7009682 W, `x` = 0.84 |
| 3 | 250 °C, 20 bar | 0.1 bar | 1.5 | docstring state, larger `alpha` |
| 4 | 191.5 °C, 8.763839 bar | 6.307527 bar | 1.0 | `test_SteamTurbine_outlet_near_saturation` (outlet marginally wet) |
| 5 | 191.55 °C, 8.763839 bar | 6.307527 bar | 1.0 | same test |
| 6 | 500 °C, 100 bar, 15 kg/s | `x_out` = 0.9 | 1.0 | `test_SteamTurbine`, "end in two phase" |
| 7 | `x_in` = 0.99, 100 bar, 15 kg/s | `x_out` = 0.9 | 1.0 | `test_SteamTurbine`, "start in two phase" |

## How to run

```bash
coolsolve ./steam_turbine_baumann.eescode
```

The file needs `steam_turbine_baumann.initials`: the crossing pressures `P_x`, the outlet
pressures of cases 6–7 and the outlet qualities/enthalpies of cases 1–3. Without it the solve ends
`SUCCESS` (63 iterations) but case 3 sits on a wrong root (`x_out[3]` = 2.2e-16, `eta_s[3]` = 0.339,
W_dot[3] = 2.8 MW), a state the physical equations accept because `quality` is clipped
at zero. Guard against this by looking at `x_out` after a solve. To study the effect of
`alpha` change `alpha[i]` (cases 1–3), or add a parametric table on `alpha[2]`.

## Results

| Case | `P_x` [bar] | `P_out` [bar] | `x_out` [-] | `eta_s` [-] | `W_dot` |
|---|---:|---:|---:|---:|---:|
| 1 | 10.200 | 0.1 | 0.8286 | 0.8787 | 7.294 MW |
| 2 | 10.200 | 0.1 | 0.8405 | 0.8444 | 7.010 MW |
| 3 | 10.200 | 0.1 | 0.8492 | 0.8193 | 6.801 MW |
| 4 | 6.355 | 6.308 | 0.99954 | 0.90006 | 57.90 kW |
| 5 | 6.349 | 6.308 | 0.99959 | 0.90005 | 57.90 kW |
| 6 | 6.011 | 0.545 (unknown) | 0.9 | 0.8935 | 14.344 MW |
| 7 | — | 57.335 (unknown) | 0.9 | 0.8505 | 1.257 MW |

In the docstring example (case 2) the dry expansion reaches saturated vapour at
`P_x` = 10.20 bar (180.74 °C, from CoolProp); the wet part from there to 0.1 bar
has `y_m` = 0.0798 and `eta_wet` = 0.8282, the overall `eta_s` = 0.8444 and the
power is 6.18 % below the constant-efficiency value (7.471 MW at `eta_s` = 0.9,
docstring, i.e. `7009682/7471296 - 1`). Case 7 is arithmetic: 0.9·(1 - 0.11/2) = 0.8505.

An overall `eta_s` slightly above `eta_s_dry` appears in cases 4 and 5 (0.90006, 0.90005):
the wet part is tiny (`y_m` = 2.3e-4 in case 4); the overall efficiency of the two-part expansion
(dry part, then wet part from the crossing point) is not the efficiency of either part (with `alpha` = 0.4,
case 1, the overall value is 0.8787, i.e. below 0.9 but above `eta_wet` = 0.8691). TESPy returns the same values (see below).

<!-- FIGURE (added by the maintainer, docs/model_workflow.md §7): eta_s and x_out versus alpha, or h-s diagram of the dry and wet parts -->

## Verification

Reference: TESPy re-run in a throw-away virtual environment (`work/baumann/`, deleted at the end):

```bash
python3 -m venv work/baumann/venv
work/baumann/venv/bin/pip install ~/git/tespy     # tespy 0.11.3.dev0, CoolProp 8.0.0
```

The script `ref2.py` rebuilds the networks of the docstring and of `test_SteamTurbine` and
`test_SteamTurbine_outlet_near_saturation` (`Source`, `SteamTurbine`, `Sink`; `eta_s_dry=0.9`, `alpha`, same
inlet/outlet specifications as in the table of cases) and writes `eta_s`, `x_out`, `W_dot` (sign changed),
`h_in`, `h_out`, `s_in` (and `P_out` for cases 6–7) to `tespy_reference.csv`, compared with the
CoolSolve `.sol` by `tools/compare_solution.py` (no unit conversion: both sides SI):

```
$ python3 tools/compare_solution.py steam_turbine_baumann.sol tespy_reference.csv
44 common variables, 0 differ (rtol=0.001); only in EES: 0; only in CoolSolve: 96
```

Maximum relative deviation **1.71e-09** over the 44 common variables (`--rtol 1e-12 --all` run;
largest `P_out_6` 1.71e-09, then `eta_s_6` 1.35e-10, `W_dot_6` 8.65e-11, all other
variables below 3.5e-11). The numbers stored in the docstring are reproduced: case 2 gives
`W_dot` = 7009682.2 W (TESPy `round(P, 0) = -7009682`) and `x_out` = 0.8405 (docstring: 0.84).
The same TESPy run with `eta_s=0.9` (docstring first example, not a case of the model) gives
P = -7471295.9 W and x = 0.821.

The third TESPy branch (superheated outlet) was run for information (`test_SteamTurbine`,
`td_dew=0.5`: 100 bar, 500 °C, outlet 6.07 bar): `eta_s` = 0.90000000, `x_out` = 1; it is not in the
model. A second check of the equations is analytical: case 7 equals the closed form
`eta_s_dry*(1 - alpha*y_m)` = 0.8505 (CoolSolve 0.85050000, TESPy 0.8505000).

## Source and attribution

Translation (equation-oriented, EES-compatible language) of the TESPy class `SteamTurbine`,
file `src/tespy/components/turbomachinery/steam_turbine.py`, commit `19425523`
(https://github.com/oemof/tespy/blob/19425523ff7ecd67b36e7b90efe04a9480a9ebe3/src/tespy/components/turbomachinery/steam_turbine.py).
Authors found in the history of the file: Francesco Witte (TESPy lead developer) and tlmerbecks
(who contributed the first version of the steam turbine component, 2025-01).
TESPy - Thermal Engineering Systems in Python - https://github.com/oemof/tespy,
Copyright (c) Francesco Witte and the TESPy contributors, MIT licence.
Changes: the network, the connections and the `design` solve mode replaced by simultaneous equations;
the `brentq` search of the saturation crossing replaced by equations (step 1); units SI-°C-Pa-J
(TESPy displays bar, °C, kJ/kg); power positive.
Please cite: F. Witte and I. Tuschy, "TESPy: Thermal Engineering Systems in Python", J. Open Source
Softw. 5(49), 2178 (2020), doi:10.21105/joss.02178.
Scientific reference named by TESPy for the Baumann rule: T. Tanuma (ed.), *Advances in Steam Turbines
for Modern Power Plants*, Elsevier (2017), doi:10.1016/C2014-0-03636-2; the rule is named after
K. Baumann (his paper was not consulted here). The mean-wetness definition is
as in the TESPy docstring.

Source file: `~/git/tespy/src/tespy/components/turbomachinery/steam_turbine.py`
(reference tests: `~/git/tespy/tests/test_components/test_turbomachinery.py`, `test_SteamTurbine`,
`test_SteamTurbine_outlet_near_saturation`; inventory candidate `TSP-004`).

## Niche

Nearest models: `CSL-0135` (*turbine_stodola_offdesign*, TESPy `Turbine`) and `CSL-0174`
(*steam_turbine_isentropic_efficiency*). They take the isentropic efficiency as given, or from a
characteristic line of the mass flow, and do not look at the state of the steam: nothing in them
changes `eta_s` when the expansion ends wet. This model adds the dependence of the efficiency on the
outlet wetness (Baumann rule), with the dry-to-wet transition located by equations; it is a stage-level
building block for steam turbines expanding into the vapour dome (low-pressure turbines, geothermal
steam, ORC with wet fluids). It is a different closure of the same energy balance, not another
property provider. `grep` for `Baumann` and `wetness` finds nothing else in the library.

## Conversion log

- **2026-10-31 — translation** (`T-TRANSLATE`): `SteamTurbine.eta_s_wet_func` as simultaneous
  equations; connections, `Source`/`Sink`, `Network` removed; two `Water` states plus the
  crossing point per case. Cases 1–5 are a `DUPLICATE` loop, 6 and 7 are written out because their
  specified quantity differs (`x_out` instead of `P_out`).
- **Wet-outlet assumption**: TESPy decides at run time between wet and dry outlet (`find_sat(1) >= 0`)
  and between a wet and a superheated inlet (`calc_phase`). The equations are written for the
  branches shown; the first by the sign of `margin`, the second by the choice of the section. No `IF`.
- **Initials**: stored values of unknowns only in `steam_turbine_baumann.initials`, none in equations.
- **Level**: 2 (taxonomy §3): property calls with two implicit pairs (crossing, wetness) and a
  largest block of 4, one regime-dependent closure.

## Limitations and CoolSolve gaps

- No CoolSolve gap: `missing_features` is empty. The model is valid EES (no CoolSolve-only syntax).
- The dry-outlet branch (`P_out >= P_x`) is not in the equations; use `eta_s = eta_s_dry` directly.
  TESPy limits `alpha` to 0.4–2.5 (parameter limits `min_val`/`max_val`), the model has no such limit.
- The Baumann rule is empirical (TESPy docstring: "influence factor"); the model does not check `alpha`.
- A solve without `.initials` can land on a wrong root (see *How to run*).

## Related models

- `CSL-0135` (*turbine_stodola_offdesign*): the TESPy `Turbine` class, parent of `SteamTurbine`; a dry
  efficiency characteristic and cone law instead of wetness.
- `CSL-0174` (*steam_turbine_isentropic_efficiency*): steam turbine with a given isentropic efficiency.
