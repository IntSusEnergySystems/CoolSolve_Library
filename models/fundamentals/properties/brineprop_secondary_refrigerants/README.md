# BrineProp: thermophysical properties of aqueous secondary refrigerants (function library)

🔵 **Level 2 · Intermediate** &nbsp;|&nbsp; 🧩 **Function library** &nbsp;|&nbsp; ⛔ **Blocked** &nbsp;|&nbsp; `CSL-0079`

The single procedure `BRINEPROP` of the **BrineProp** library of the ULiège
model bank: for a solution name (`EG`, `PG`, `EA`, `MA`, `GL`, `NH3`, `K2CO3`,
`CaCl2`, `MgCl2`, `NaCl`, `KAc`), a mass concentration in % and a temperature
in °C it returns the **freezing point, density, specific heat, thermal
conductivity or dynamic viscosity** of the aqueous solution, from an 18-term
polynomial in the deviations of the concentration and the temperature from the
mean values of the solution. It is the brine-property routine that the
glycol/water run-around loops, brine pumps, cooling and heating coils and
brine-to-water heat pumps of the collection call implicitly (seven candidate
rows of the inventory name it).

| | |
|---|---|
| **Category** | Fundamentals › Properties |
| **Fluids** | aqueous solutions EG, PG, EA, MA, GL, NH3, K2CO3, CaCl2, MgCl2, NaCl, KAc (secondary refrigerants; not CoolProp fluids) |
| **Size** | 440 equations after analysis (largest block: 1); the procedure itself is ~60 lines; two lookup tables (198 × 5 and 11 × 2 coefficients) |
| **Source** | ULiège Thermodynamics Laboratory — EES library `Brineprop.lib` (1997 edition according to its EES help file; compiled stamp EES 7.793) with the binary lookup tables `Brine1.lkt` and `Brine2.lkt` (EES 4.631) |
| **Authors** | TBD (ULiège Thermodynamics Laboratory; the EES help file of the library credits its 1997 edition and refers to IIR thermo-physical data, no personal name; the inventory attributes the library to the laboratory, J. Lebrun et al.) |
| **License** | MIT |
| **CoolSolve** | **blocked**: the native file does not parse (`CS-GAP-ELSEIF-CHAIN`, `CS-GAP-UPPERCASE`, `CS-GAP-STRING-ARRAY`); the runnable variant `brineprop_secondary_refrigerants_coolsolve.eescode` is **verified** against the EES stored solution (≤ 4.77e-10) |

## Problem statement

Give the thermophysical properties of an aqueous secondary refrigerant
(glycol, alcohol, brine) at a given mass concentration and temperature. Such
libraries replace a table lookup in the secondary-circuit models of HVAC and
heat-pump systems, where the brine side is treated as an incompressible fluid
whose ρ, c_p, k and μ are needed at each state.

## Model

| Routine | Signature | Returns |
|---|---|---|
| `BRINEPROP` (PROCEDURE) | `CALL BRINEPROP(Pr$, Fl$, Conc, Temp : output)` | `Pr$` = `'Freeze'` (°C), `'Density'` (kg/m³), `'SpecHeat'` (kJ/kg·K), `'ThermalC'` (W/m·K) or `'DynVisc'` (milliPa·s); `Fl$` = one of the 11 solution codes; `Conc` = mass concentration [%]; `Temp` = temperature [°C] |

Structure of the procedure (as in the original):

1. 22 `IF` statements check that `Conc` is inside the validity range of the
   named solution and `Call ERROR` otherwise (the message invites the user to
   set the limits of the variables in the *Variables Info* window, as in the
   original);
2. the property name is normalised (`Uppercase$`) and translated into an
   indicator `Pro` = 1…5 (Freeze, Density, SpecHeat, ThermalC, DynVisc); the
   solution name into `Flu` = 1…11 (EG, PG, EA, MA, GL, NH3, K2CO3, CaCl2,
   MgCl2, NaCl, KAc);
3. the 18 polynomial coefficients of the requested property and solution are
   read from table `Brine1` at the rows `Row[k] = k + (Flu-1)*18`, column
   `Pro`; the mean concentration `xm` and mean temperature `ym` of the solution
   are read from table `Brine2` at the row `Flu`;
4. with `x = Conc − xm` and `y = Temp − ym`, the property is
   `Funkt = c[1] + c[2]y + c[3]y² + c[4]y³ + c[5]x + c[6]xy + … + c[17]x⁴y + c[18]x⁵`,
   returned as `output = exp(Funkt)` for the dynamic viscosity,
   `output = Funkt/1000` for the specific heat and `output = Funkt` otherwise.

Validity ranges of `Conc` (mass %, as written in the procedure) and mean values
of table `Brine2`:

| Code | Solution | `Conc` [%] | xm [%] | ym [°C] |
|---|---|---|---|---|
| EG | ethylene glycol | 0 – 56.1 | 38.1615 | 6.3333 |
| PG | propylene glycol | 15.2 – 57.0 | 42.7686 | 5.3571 |
| EA | alcohol | 11.1 – 60.1 | 38.925 | −4.9038 |
| MA | methanol | 7.8 – 44.3 | 32.9283 | −6.25 |
| GL | glycerol | 19.5 – 63.0 | 47.8467 | 7.0 |
| NH3 | ammonia | 7.8 – 23.6 | 17.9664 | −7.1429 |
| K2CO3 | potassium carbonate | 13.3 – 39.0 | 27.6708 | 4.1667 |
| CaCl2 | calcium chloride | 9.0 – 29.4 | 22.918 | 0.2459 |
| MgCl2 | magnesium chloride | 7.2 – 20.5 | 13.7 | 5.875 |
| NaCl | soda | 7.9 – 22.6 | 12.3539 | 9.2581 |
| KAc | acetate | 11.0 – 41.0 | 30.9656 | 0.2459 |

The codes are those of the original and the product names are the usual
expansion of the code: the table of the EES help file shipped with the library
(`BRINEPROP.hlp`, table *Limits*) names them *Ethylene Glycol*, *Propylene
Glycol*, *Alcohol*, *Methanol*, *Glycerol*, *Ammonia*, *Potassium Carbonate*,
*Chloride*, *Magne…*, *Soda* and *Acetate*, but the three last ones are only
partly legible in that compiled help file, which is why the code comes first in
the table above. The concentration ranges are those tested by the procedure
itself, not those of the help file.

Units: the file is already SI-°C-Pa-J (EES unit system `SI MASS DEG PA C J`),
so **no unit conversion was needed**; the units of the outputs are the ones
declared by the original in its `U$` array: kg/m³, kJ/kg·K, W/m·K, milliPa·s
and °C.

## How to run

The native file `brineprop_secondary_refrigerants.eescode` **does not parse** in
CoolSolve (the `ELSE IF … ENDIF;ENDIF` ladders of the procedure,
`CS-GAP-ELSEIF-CHAIN`); it is kept in valid EES. The faithful runnable
transcription is

```bash
coolsolve ./brineprop_secondary_refrigerants_coolsolve.eescode
```

`solve` in 3 iterations; its baseline is
`brineprop_secondary_refrigerants_coolsolve.sol` (regression-tested as
`CSL-0079:coolsolve`). The variant changes only what the gaps force (selector
procedure + flattened property blocks, see *Conversion log*); it is valid EES,
with no CoolSolve-only syntax, and keeps the variable names of the native file.
Companion tables: `brineprop_secondary_refrigerants-Brine1.csv` /
`-Brine2.csv` for the native file, `…_coolsolve-Brine1.csv` / `-Brine2.csv`
for the variant, all four holding the same decoded values.

Models that call these routines copy their definitions
(`{--- Library procedure copied from CSL-0079 ---}`) until
`$INCLUDE library:brineprop_secondary_refrigerants` is available
(`CS-FEAT-IMPORT`).

## Results

Demonstration program (after the procedure definition), regression case of the
variant (`brineprop_secondary_refrigerants_coolsolve.sol`):

Case 1 — propylene glycol 50 % at 65 °C, the case of the commented example
block of the original library:

| Quantity | Value |
|---|---:|
| `T_freeze_1` [°C] | −33.0940254 |
| `rho_brine_1` [kg/m³] | 1006.87140 |
| `c_p_brine_1_kJ` [kJ/kg·K] | 3.70784870 |
| `k_brine_1` [W/m·K] | 0.380096893 |
| `mu_brine_1_mPa_s` [milliPa·s] | 1.35132125 |

Case 2 — ethylene glycol 25 % at 6.324036551 °C, the temperature stored by the
glycol run-around loop reference model of the same library (inventory
`TM-0476`), used for the verification below:

| Quantity | Value |
|---|---:|
| `T_freeze_2` [°C] | −10.9597832 |
| `rho_brine_2` [kg/m³] | 1036.22875 |
| `c_p_brine_2` [J/kg·K] (`c_p_brine_2_kJ` = 3.80535085) | 3805.35085 |
| `k_brine_2` [W/m·K] | 0.472382728 |
| `mu_brine_2` [Pa·s] (`mu_brine_2_mPa_s` = 2.94346083) | 0.00294346083 |

<!-- FIGURE (maintainer, docs/model_workflow.md §7): e.g. density and specific heat
     of EG 25 % and PG 50 % versus temperature (−20…80 °C) as a parametric sweep. -->
## Verification

Status **blocked** (the native file does not parse); the **runnable variant**
`brineprop_secondary_refrigerants_coolsolve.eescode` is **verified**: the three
properties that an independent EES reference holds agree to 4.77e-10, well
inside the tolerance.

1. **EES reference.** A `.lib` file stores no solution of its own, so the
   reference is the stored solution of the *glycol run-around loop* reference
   model of the same library, `GLYCOLRECOVERYLOOP_RefSim_EES_Model_SB080116.EES`
   (EES 7.888, inventory `TM-0476`), which calls `BRINEPROP` for ethylene
   glycol 25 % at `t_gw_m` = 6.324036551 °C and stores the three results
   (`rho_gw`, `c_p_gw`, `mu_gw`). Extracted with `tools/ees_extract.py`; the
   three values, converted to the units of the variant, form the reference
   CSV. Comparison with `tools/compare_solution.py` (default rtol = 0.001):

   | Variable | EES | CoolSolve | rel. diff |
   |---|---:|---:|---:|
   | `c_p_brine_2` [J/kg·K] | 3805.35 | 3805.35 | 7.88e-13 |
   | `mu_brine_2` [Pa·s] | 0.00294346 | 0.00294346 | 4.38e-11 |
   | `rho_brine_2` [kg/m³] | 1036.23 | 1036.23 | 4.77e-10 |

   `3 common variables, 0 differ (rtol=0.001); only in EES: 0; only in
   CoolSolve: 437`. The 437 CoolSolve-only variables are the internal
   variables of the ten flattened property blocks, the outputs of the selector
   procedure and the five case-1 properties; the reference file holds only the
   three properties the EES model stores, so the other seven properties of the
   demonstration program have **no** EES reference and are not part of the
   figure. No variable of the reference was excluded.
2. **Lookup tables.** `Brine1.lkt` and `Brine2.lkt` (EES 4.631 binary lookup
   files) were **decoded by hand** from the EES layout documented in
   `ees_import.md` §13 (per column: a short-string name in a 31-byte field,
   then *nrows* 10-byte values; the values are 80-bit extended floats written
   as a 64-bit little-endian significand followed by a 16-bit little-endian
   exponent whose bit 15 is the sign) and shipped as companion CSVs with the
   EES column names `Column1…5`. Both tables were then checked against the
   EES stored solution above: the decoded coefficients reproduce
   `rho_gw` = 1036.228755 kg/m³, `c_p_gw` = 3805.350851 J/kg·K and
   `mu_gw` = 0.002943460833 Pa·s of the glycol loop model to 4.8e-10 relative
   (`CS-GAP-LKT` worked around). The decode was also made independently of
   `CSL-0072`, which ships the same two tables for the same library: both
   decodes agree to the last printed digit (max. absolute difference 0.0).
3. **Independent computation** (work folder, deleted): a Python transcription
   of the procedure (same tables, same polynomial, no CoolSolve code) gives
   the same values as the variant for the two demonstration cases and for the
   5 properties of all 11 solutions, i.e. the transcription of the procedure is
   faithful over the whole table, not only at the verified point.

## Source and attribution

Function library of the **Thermodynamics Laboratory of the University of Liège**
(Faculté des Sciences Appliquées), distributed with the EES setups of the
laboratory as a compiled EES library loaded from the `USERLIB` folder
(`Brineprop.lib`, help file `BRINEPROP.hlp`, coefficient tables `Brine1.lkt` /
`Brine2.lkt`). No personal author is named in the library: the EES help file
credits the 1997 edition of the library and refers to IIR thermo-physical data,
and the inventory of S. Quoilin's collection attributes it to the laboratory
(J. Lebrun et al.); the author is therefore left `TBD` for the maintainer. The
lab disclaimer of the collection (freely distributed, may not be sold, cite the
origin) applies.

Source file (compiled EES library, Windows-1252, EES 7.793 stamp `$SB1`; the
equation text is plain text inside the binary), collection of S. Quoilin:
`~/Nextcloud/thermo_models/Model data bank/AHU_Components/Recovery_Systems/GLYCOLRECOVERYLOOP_REFSIM_EES_MODEL_SB080116.zip!/UserLib/BrineProp/Brineprop.lib`
(inventory candidate `TM-0479`). The sibling file `Brineprop2.LIB` of the same
folder (candidate `TM-0480`) holds the second-generation procedure
`BRINEPROP2` — see *Conversion log*.

## Conversion log

- **2026-10-05 — import** (`T-FUNC`, roadmap card C-84): the `.lib` is a
  *compiled* EES library, not plain text; its equation text was recovered from
  the binary (Windows-1252, NUL bytes and the compiled code section removed),
  the `{$DS.}`-like stamp `$SB1-X7.793` was dropped. Unit system already
  SI-°C-Pa-J on mass basis → **no unit conversion**. The procedure is copied
  unchanged (22 `Call ERROR` range checks, `Uppercase$` normalisation, the two
  `ELSE IF` ladders, the `U$` string array, the `REPEAT` loop, the polynomial
  and the output scaling); the only edits are the removal of the dead code that
  followed `END` in the library file (a stray `x=1` statement and the
  commented example block, which became the demonstration program) and of a
  commented-out duplicate of the unit ladder.
- **2026-10-05 — demonstration program**: written after the procedure
  definition (workflow §4), in the pattern of the example block of the
  library: case 1 is that example (PG, 50 %, `T_g_avg`), case 2 is the state
  stored by the glycol run-around loop model of the same library (EG, 25 %,
  6.324036551 °C) so that the verification has an EES reference. Two
  conversions are written explicitly for the comparison with that stored
  solution (`c_p_brine_2 = c_p_brine_2_kJ*1000`, `mu_brine_2 =
  mu_brine_2_mPa_s/1000`), which is how the glycol model itself calls the
  library (`… : c_p_gw/1000`, `… : mu_gw*1000`).
- **2026-10-05 — `T_g_avg` = 65**: the example block of the library writes
  `T_g_avg=65 [K]`, but the temperature argument of `BRINEPROP` is in degrees
  Celsius (the help file: *"temperature in °C"*; the coefficient tables are
  centred on °C, see `ym`). 65 K = −208.15 °C is below the freezing point of
  every one of the eleven solutions (the highest freezing point the correlation
  returns over the whole validity domain is 0.03 °C), so the demonstration uses
  `T_brine_1 = 65 [C]` and says so in a comment. This is the only reading
  decision taken in the import.
- **2026-10-05 — lookup tables**: decoded by hand from the binary `.lkt` files
  (see *Verification* item 2) and shipped as the four companion CSVs of the
  model; `CS-GAP-LKT` worked around. The CSV values are written with full
  round-trip precision (17 significant digits, Python `repr`) rather than the
  5 significant digits of an EES CSV export: the 18-term polynomial cancels, and
  the 5-digit rounding shifts the results by up to 1.4e-5 (viscosity), while the
  full precision keeps them at 5e-10.
- **2026-10-05 — runnable variant** `brineprop_secondary_refrigerants_coolsolve.eescode`
  (valid EES; no CoolSolve-only syntax). Changes forced by the gaps, logged in
  the variant header:
  1. `CS-GAP-ELSEIF-CHAIN`, `CS-GAP-UPPERCASE` and `CS-GAP-STRING-ARRAY` break
     `BRINEPROP`. The 22 range checks and the 11-branch solution ladder become a
     selector procedure `BRINEPROP_SELECT(Conc,Fl$ : Fl_brine)` of sequential
     single-line `IF` statements (conditions mutually exclusive, behaviour
     unchanged; kept in a procedure because `IF` statements are procedure-only
     in EES). The `Uppercase$` normalisation and the string array `U$` (unit
     labels only, feeding no equation) are dropped, and an explicit
     `Call ERROR` for an unrecognized solution name is added — the error the
     original raises only through its failed lookup.
  2. The property evaluation is flattened into the main program, one block per call of the demonstration program (library decision
     D10 style), the procedure-internal variables renamed per call
     (`<variable>_<tag>`, tags `_fz_1`, `_rho_1`, `_cp_1`, `_tc_1`, `_mu_1`
     and `_fz_2` … `_mu_2`), the `REPEAT` loop becoming a `DUPLICATE` loop. The
     polynomial, the tables, `Row[k]=k+(Fl-1)*18`, `xm`/`ym` and the output
     scaling are unchanged; the two outputs of case 2 are scaled to SI by the
     two explicit equations of the native file.
  3. `CS-GAP-LKT`: own companion tables (same decoded values).
- **Level 2** although the raw score is 4 (440 equations after the CoolSolve
  analysis, largest block 1, procedure present, semi-empirical correlation):
  the equation count comes entirely from the ten flattened repetitions of the
  same 18-term polynomial, not from model depth — the library routine itself is
  one polynomial and two table reads. Kept in line with the inventory guess and
  with the level-2 function library `CSL-0005` (`cpbar_combustion_products`).

## Limitations and CoolSolve gaps

The native file is **blocked**; `missing_features` lists every gap that blocks
it. The three gaps below are the first parse errors:

- `CS-GAP-ELSEIF-CHAIN` — the two `ELSE IF … ENDIF;ENDIF` ladders of
  `BRINEPROP` do not parse ("IF ... THEN without a matching ENDIF", 20 errors);
- `CS-GAP-UPPERCASE` — the intrinsic `Uppercase$` is unknown;
- `CS-GAP-STRING-ARRAY` — reading a string-array element (`UO$=U$[Pro]`) fails
  ("String variable not found"); the unit labels it carries feed no equation;
Worked around, not blocking the native file: `CS-GAP-INCLUDE` (the library is
implicit in EES, its definitions are copied into this file and into the models
that call them) and `CS-GAP-LKT` (binary `.lkt` tables decoded to CSV
companions). The runnable variant carries no gap of its own.

Physics and accuracy: the correlations are those of the laboratory (1997), with
IIR thermo-physical data; they are empirical polynomials valid only inside the
concentration ranges of the table above, and no uncertainty is given. The
property is a function of concentration and temperature only — pressure has no
influence (the brines are treated as incompressible by the calling models).
The 11 solutions are not CoolProp fluids: no EES property call is involved.
A second-generation procedure `BRINEPROP2` (candidate `TM-0480`, the sibling
`Brineprop2.LIB` of the same folder) computes the five properties in one call
and adds the Prandtl number; it uses the same `Brine1`/`Brine2` tables and the
same polynomial (the equation diff of the two files differs in the signature,
in the unit conversions of the outputs — viscosity in Pa·s instead of milliPa·s
— and in the extra `Pr` output), so it is recorded as `merged` in this model
rather than imported: it would be added to this folder, as a second procedure
of the same function library, by a follow-up card.

## Related models

- `CSL-0072` *centrifugal_brine_pump_refsim* — first user: its native and
  runnable files carry a copy of `BRINEPROP` (density and specific heat of EG
  25 %) and its own copies of the two coefficient tables; its EES reference
  values for EG 25 % at 25 °C (ρ = 1030.000008 kg/m³, c_p = 3852.099981
  J/kg·K) are reproduced by the tables of this model to 2.9e-09 and 6.2e-09
  relative (work folder, Python, deleted).
- `CSL-0074` *cooling_coil_refsim* — cooling coil of the same model bank that
  calls the library for the brine side (copy in its file).
- `CSL-0087` *internal_turbulent_nusselt*: the other translated function
  library (from `ht`), the third kind of function library of the library next to
  this one and `CSL-0005`.
- `CSL-0078` *brine_to_water_heat_pump_refsim* — brine evaporator of the same
  model bank; calls the library for the density and the specific heat of a 25 %
  propylene glycol solution (copy of the procedure in its file, tables shipped).
- `CSL-0113` *condenser_3_zones_plate_correlations*: plate condenser whose
  `prop_htf` procedure carries a glycol polynomial for the secondary fluid;
  this library is the more complete property source for the same fluids.
- `CSL-0091` *internal_laminar_and_curved_nu*: the laminar, entry-region and curved-duct (spiral, helical) internal-convection family of the same `ht` triage, same layout; it complements `CSL-0087` (turbulent pipe flow) at low Reynolds number and non-circular geometries.
- `CSL-0114` *evaporator_3_zones_plate_correlations*: three-zone plate evaporator whose `prop_htf` procedure carries the same glycol polynomial for the secondary fluid.
- `CSL-0121` *heat_transfer_fluid_properties*: companion function library for the pure
  heat-transfer fluids (monoethylene glycol, Therminol VP-1/66, thermal oil); the two
  libraries cover the secondary fluids of the library between them.
- `CSL-0161` *plate_hx_thermal_resistances*: single-phase plate heat exchanger
  (Martin) whose native file calls `BRINEPROP2` on its ethylene-glycol branch
  (candidate `TM-0480`, merged here); the runnable variant resolves the stored
  water run.
- `CSL-0162` *glycol_runaround_recovery_loop*: model of the same model bank
  calling `BRINEPROP` the same way ('SPECHEAT'/'DENSITY'/'DYNVISC' on EG 25 %);
  its runnable variant flattens the calls like this variant does.
- `CSL-0163` *cooling_coil_paramid*: calls this library's `BRINEPROP`
  procedure for the ethylene-glycol properties of the identified coil
  (card C-155; its runnable variant uses the stored brine values).
