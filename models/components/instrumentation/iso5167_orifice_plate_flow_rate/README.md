# ISO 5167 orifice plate (diaphragm) flow-rate calculation

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; ⚙️ **Steady-state** &nbsp;|&nbsp; ⛔ **Blocked** (runnable variant ✅ verified) &nbsp;|&nbsp; `CSL-0075`

Flow-rate calculation of the ISO 5167-1980 standard for a **diaphragm** (orifice
plate with **corner pressure tappings**), from the ULiège model bank
(Laborelec toolkit lineage). The fluid — here saturated humid air — is
characterised at the upstream state (density, viscosity, cp/cv ratio); the mass
flow rate follows from the measured pressure drop through the Stolz discharge
coefficient and the expansibility factor. The stored operating point is
written **inversely**: the mass flow rate is imposed and the model solves the
bore diameter `Di_dph` of the diaphragm. The file also flags out-of-range
inputs (bore, pipe diameter, diameter ratio, Reynolds) with `CALL WARNING`
branches.

| | |
|---|---|
| **Category** | Components › Instrumentation |
| **Fluids** | AirH2O (saturated humid air at the default point); the `fluidprop` procedure accepts any CoolSolve fluid |
| **Size** | 34 equations, largest block 6: 2 procedures + 1 flattened module (25 equations) + main program |
| **Source** | ULiège model bank — `Model data bank/EES_Functions/iso5167/` (EES file `ISO5167 flow rate calculation - diaphragm.EES`) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory model bank, Laborelec toolkit lineage; EES licence stamp of the J. Lebrun lab) |
| **License** | MIT |
| **CoolSolve** | native file **blocked** (`CS-GAP-ISIDEALGAS`, `CS-BUG-HUMIDAIR-PROPS`); runnable variant `iso5167_orifice_plate_flow_rate_coolsolve.eescode` verified (see *Verification*) |

## Problem statement

A diaphragm of bore `Di_dph` in a pipe of diameter `De_dph` = 50 mm carries
saturated humid air at 50 °C and 8 bar. With corner tappings, a measured
pressure drop of 0.5 bar and an imposed mass flow rate of 0.125 kg/s, find the
bore diameter and the flow characteristics (Reynolds number, discharge
coefficient, expansibility factor). In the original design version the bore
was given (`Di_dph` = 0.018 m, kept commented out) and the mass flow rate was
the result.

## Model

Upstream state (`fluidprop` procedure): humidity ratio, density, viscosity and
`Gamma` = cp/cv of the fluid; for `AirH2O` the properties are per kg of dry
air and the density is converted per kg of mixture with (1+w), as in the
original.

ISO 5167-1980 procedure (module `flowrate` of the original, flattened into the
main program):

- pipe and bore sections; mass flux `G_dph` and pipe Reynolds number
  `Re_D_dph = G_dph*De_dph/mu_dph`;
- velocity of approach factor `E_dph = (1 - beta_dph^4)^(-0.5)` with
  `beta_dph = Di_dph/De_dph`;
- discharge coefficient, Stolz equation:
  `C_D_dph = 0.5959 + 0.0312*beta^2.1 - 0.184*beta^8 + 0.0029*beta^2.5*(10^6/Re)^0.75 + coef*L1*beta^4/(1-beta^4) - 0.03371*L2*beta^3`
  with `L1`, `L2` the tapping distance ratios (0 for corner tappings) and
  `coef` the 0.039/0.09 coefficient selected by the 5-argument `if` of the
  original;
- expansibility factor
  `epsilon_dph = 1 - (0.41 + 0.35*beta^4)*DELTAP/(Gamma*P_su)`;
- mass flow rate
  `M_dot_a_dph = E_dph*C_D_dph*epsilon_dph*A_di_dph*sqrt(2*DELTAP_dph*rho_a_su_dph)`.

The `warning_error` procedure checks the ISO validity ranges (bore > 12.5 mm,
pipe diameter 0.05–1 m, beta 0.23–0.8, Reynolds 5000/10⁴/2·10⁴–10⁸ depending
on beta) and reports violations with `CALL WARNING`.

| Inputs | Value | Outputs | Value |
|---|---|---|---|
| `t_a_su_dph` upstream temperature | 50 °C | `Di_dph` bore diameter | 0.017025 m |
| `P_a_su_dph` upstream pressure | 8·10⁵ Pa | `rho_a_su_dph` upstream density | 8.583 kg/m³ |
| `RH_su_dph` relative humidity | 1 | `w` humidity ratio (property value) | 0.009975 kg/kg |
| `DELTAP_dph` pressure drop | 5·10⁴ Pa | `beta_dph` diameter ratio | 0.3405 |
| `De_dph` pipe diameter | 0.050 m | `Re_D_dph` Reynolds number | 1.619·10⁵ |
| `l1_dph`, `l2_dph` tapping distances | 0, 0 m | `C_D_dph` discharge coefficient | 0.5999 |
| `M_dot_a_dph` mass flow rate | 0.125 kg/s | `epsilon_dph` expansibility factor | 0.9813 |
| `fluid$` | 'AirH2O' | `Gamma_dph` cp/cv ratio | 1.3863 |

## How to run

```bash
coolsolve ./iso5167_orifice_plate_flow_rate_coolsolve.eescode
```

The native file `iso5167_orifice_plate_flow_rate.eescode` is valid EES and is
kept unchanged (module flattened, comments translated). In CoolSolve it takes the
`AirH2O` branch and stops in block 16 (6 unknowns of the ISO 5167 iteration) with
*SingularJacobian*, because of the wrong humid-air `density` and `cv` of
`CS-BUG-HUMIDAIR-PROPS` (`isidealgas` is still unknown, but only the other-fluid
branch uses it). The runnable variant is documented in its header; each of its
changes is listed in the conversion log below.

## Results

At the default operating point the variant gives `Di_dph` = 17.025 mm,
`Re_D_dph` = 1.619·10⁵, `C_D_dph` = 0.5999, `epsilon_dph` = 0.9813. The
expansibility factor differs from 1 by 1.9 % (0.5 bar drop on 8 bar), and the
discharge coefficient is close to its low-Reynolds asymptote 0.5959 plus the
Reynolds term.

<!-- FIGURE (maintainer, docs/model_workflow.md §7): no diagram applies (single state point);
      a parametric sweep of beta_dph over the C_D_dph equation could serve. -->

## Verification

The EES **stored solution of the source file is stale** (known tool behaviour,
`CS-BUG-EXTRACT-STALE`): it mixes at least two
older runs with the current inputs. Evidence in the stored values themselves:

- `var3_out` = 0.36 while `beta_dph` = 0.3714285714, although
  `warning_error` assigns `var3_out := beta_dph` — impossible in one solution;
- `A_De_dph` = 0.0038485 = π·0.07²/4 while `De_dph` = 0.05 (an older run with
  a 70 mm pipe, `beta_dph` = 0.3714 = 0.026/0.07, `d1_dph` = 0.011, `d2_dph` = 0.006);
- `rho_a_su_dph` = 1.231 kg/m³, impossible at 50 °C / 8 bar (saturated humid
  air ≈ 8.58 kg/m³) — an older, near-atmospheric state point.

The only stored values consistent with the current operating point are the
inputs and the solved bore diameter `Di_dph` = **0.01702816341** (the last
design inversion run). The variant was verified against it:

```text
python3 tools/compare_solution.py iso5167_orifice_plate_flow_rate_coolsolve.sol <consistent rows of reference/ees_variables.csv>
→ 7 common variables (inputs and Di_dph), 0 differ (rtol=0.001)
```

| Variable | EES stored | CoolSolve variant | rel. diff |
|---|---:|---:|---:|
| `Di_dph` [m] | 0.01702816341 | 0.01702515 | 1.8·10⁻⁴ |

(the 6 other common variables are the inputs, identical by construction)

Independent sanity checks of the humid-air state (hand calculation with
standard psychrometrics, EES-equivalent mixture rules): density 8.583 vs
8.575 kg/m³ (+0.10 %), humidity ratio 0.009975 vs 0.009750 (+2.3 %, CoolProp
vs ASHRAE saturation pressure), viscosity 1.967·10⁻⁵ Pa·s, `Gamma` 1.3863 vs
≈1.398 (CoolProp cp of humid air vs the EES ideal-mixture cp, ≈0.8 %; effect
on `Di_dph` ≈0.03 %). All within the real-fluid/property-backend tolerance of
`docs/ees_import.md` §11.

## Source and attribution

File of the ULiège **model data bank** (`EES_Functions/iso5167/`), Laborelec
toolkit lineage, comments in French; no author named in the file (the
`{$ID$}` stamp is the EES licence of the J. Lebrun laboratory, not the
author). Sibling files of the same family: `ISO5167 flow rate calculation -
long radius.EES` (TM-0256) and `ISO5167_air_flow_rate_calculation-isa1932.EES`
(TM-0257) implement the same procedure for a long-radius nozzle and an ISA
1932 nozzle (different discharge-coefficient equation and validity ranges);
they are described only (inventory decision `merged`) and were not imported
with this card.

Source file (EES 7.793), collection of S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/EES_Functions/iso5167/ISO5167 flow rate calculation - diaphragm.EES`
(inventory candidate `TM-0255`).

## Conversion log

- **2026-10-05 — import** (`tools/ees_extract.py`, CoolSolve repository):
  unit system already `SI MASS DEG PA C J` (no unit conversion). The EES
  licence tag was removed. The inventory's FluidProp hint is a false lead: the
  `fluidprop` *procedure* of the file calls the EES built-ins
  (`density`, `viscosity`, `cp`, `cv`, `HumRat`), no external tool — the model
  has no FluidProp dependency. Comments translated to English, standard header
  added, no equation changed.
- **2026-10-05 — MODULE flattened (decision D10).** The `MODULE flowrate` is
  replaced by its equations in the main program (one call): formal arguments
  replaced by the actual ones (`d1_dph` → `l1_dph`, `d2_dph` → `l2_dph`);
  internal variables keep their `_dph` tag except `coef` → `coef_dph` and the
  internal `L1_dph`, `L2_dph` → `L1_ratio_dph`, `L2_ratio_dph`, which would
  collide with the caller's `l1_dph`, `l2_dph` (EES names are
  case-insensitive). The file stays valid EES; `CS-GAP-MODULE` (not planned)
  is not a blocker after flattening and is not listed in `missing_features`.
- **2026-10-05 — stale stored solution.** See *Verification*: only the inputs
  and `Di_dph` are used as reference.
- **2026-10-05 — runnable variant** `iso5167_orifice_plate_flow_rate_coolsolve.eescode`
  (native file kept in valid EES). Changes, each forced by a gap:
  1. `coef_dph = if(0.039/0.09 - L1_ratio_dph, 0.09, 0.039)`: the 5-argument
     intrinsic `if(A,B,X,Y,Z)` (X if A<B, Y if A=B, Z if A>B) rewritten with
     the 3-argument CoolSolve form; exactly equivalent here because the A=B
     and A>B branches of the original both return 0.039. The 5-argument form is
     accepted by CoolSolve now, so this rewrite is not required.
  2. `isidealgas(Fluid$)` unsupported (`CS-GAP-ISIDEALGAS`): the
     ideal-gas special case of `fluidprop` is dropped and
     `viscosity`/`cp`/`cv` are always called with (T=, P=), which CoolProp
     accepts for ideal gases too. For the default fluid the branch used was
     already the humid-air one: no effect on the verified operating point.
  3. `fluid$ = 'airh2o'` written `'AirH2O'`: CoolSolve compared strings
     case-sensitively, so the lowercase spelling of the original missed the
     `AirH2O` branch of `fluidprop` and silently returned the fallback density
     10⁴ kg/m³; the comparison is case-insensitive now, so this rewrite is not
     required. Same fluid in EES.
  4. `Rho = (1+w)/volume(AirH2O, T, P, R)`: `density(AirH2O, ..., R=)` returns
     the fallback value 1E4 in CoolSolve (`CS-BUG-HUMIDAIR-PROPS`);
     EES `density` = 1/`volume` for AirH2O (per kg of dry air), times (1+w)
     as in the original.
  5. `Gamma = cp/(cp - R_mix)` with `R_mix = (287.055 + w*461.495)/(1+w)`:
     `cv(AirH2O, ...)` returns cp in CoolSolve (`CS-BUG-HUMIDAIR-PROPS`);
     cv = cp − R_mix is the EES relation for the ideal-gas humid-air mixture.
  6. The six `CALL WARNING` statements of `warning_error` are replaced by
     comments with the same validity ranges: with the broken humid-air
     properties (points 4–5) or any iterate far from the solution a range check fires
     and CoolSolve raises *"Unknown procedure: warning"*
     (`CS-GAP-CALL-WARNING`); with correct properties and the shipped guesses
     none of the ranges is violated at the solution.
- **Level justification** (taxonomy §3): 34 equations (0) + largest block 6
  (1) + procedures present (1) + no discretisation (0) + no calibration
  (0) + curated guesses needed (1) = score 3 → **level 2**.
## Limitations and CoolSolve gaps

- Native file blocked; `missing_features` (model.json) lists every gap that
  blocks a faithful CoolSolve run: `CS-GAP-ISIDEALGAS` (hard error, only for a
  fluid other than `AirH2O`) and `CS-BUG-HUMIDAIR-PROPS` (silent wrong results,
  then *SingularJacobian* in block 16).
- `CS-GAP-CALL-WARNING` concerns the native file too but does not block it: at
  the stored operating point no warning branch is taken; with the wrong
  humid-air properties of `CS-BUG-HUMIDAIR-PROPS` a range check can fire and
  raise *"Unknown procedure: warning"*.
- The variant inherits the CoolProp humid-air backend (see *Verification*):
  `w` +2.3 %, `Gamma` −0.8 % vs EES mixture rules, `Di_dph` within 2·10⁻⁴.
- The `warning_error` procedure checks are documentation-only in the variant.
- The ISO 5167-1980 Stolz equation is the 1980 edition of the standard (the
  current edition is ISO 5167-2:2003 with slightly different coefficients);
  the model reproduces the 1980 text, as in the original.

## Related models

- none yet in the library (first model of `components/instrumentation`);
  the nozzle variants TM-0256/TM-0257 of the same source family are natural
  follow-ups (see *Source and attribution*).
- `CSL-0122` *nozzle_discharge_coefficients*: the long-radius member of the
  same ISO 5167 source family (TM-0256) plus the ASHRAE 41.2 / ISO R859
  nozzle bank, as a function library; its ISO 5167 part is
  character-identical to the TM-0256 equations described above.
