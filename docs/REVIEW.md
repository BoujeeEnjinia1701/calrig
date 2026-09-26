# Review note: CalRig

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (CLR-PRB-001 v0.2): the problem (humidity bias, temperature dependence and drift in low-cost sensors), users and operating environment, constraints, out of scope, prior work with sources (EPA targets, AQ-SPEC, Greenspan salt fixed points, Uganda calibration work), open questions. There was no co-design checklist to keep.
- `docs/03-requirements.md` (CLR-REQ-001 v0.2): 18 measurable requirements (R1 to R18) with targets, planned verification and a first-order status column; requirements not met listed plainly.
- `docs/02-concept.md` (CLR-PRC-001 v0.2): how it works, components table numbered to the BOM, first-order numbers with assumptions, heat balance at the temperature limits, condensation check, particle reference approach, design choices, links to AirStreet, HeatMap Node, DustBadge and FieldNode, safety section, open questions.
- `cad/src/concept_media.py`: massing model with 15 numbered parts (chamber shell, door, insulation jacket, base plate, Peltier heat pump, mixing fan, sensor tray, reference cluster, bubbler, dryer, HEPA loop, aerosol port, controller, power supply, salt jars), example sensors under test, and a lab bench with a 1.75 m person for scale in the hero only.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` and `viewer.html`, `exploded.png` with BOM callouts, `cutaway.png`, `flow.png` (calibration run; durations marked as estimates). Temporary `_views` folders removed.
- `bom/bom.csv`: 18 priced lines in the existing column format, lines 1 to 15 matching the exploded view.
- `README.md`: hero image and links line; Concept rationale, Burning platform, Where it could be used (6 industries, 5 regions), What sparked the idea, Problem, Concept, Key components and Safety expanded, headings and order unchanged.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem statements remain accurate.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Chamber volume and capacity | 36 L, six sensor bays | R10 met |
| Heat leak with jacket | about 1.0 W/K | Basis for R1 |
| Temperature range | 10 to 40 °C in a room at 25 °C or below; lowest about 15 °C in a 30 °C room | R1 **not met** in warm rooms |
| Humidity range | 20 to 85 % RH; 1.2 g of water for 20 to 85 % at 40 °C | R2 met, with door panel needed at 40 °C and 85 % RH |
| Four-point sweep plus particle run | about 6 h | R11 met |
| Smoke decay 300 to 5 µg/m³ | about 30 min | R7 met |
| Peak power | about 70 W from a 12 V external supply | R15 met |
| Size and mass | about 610 x 470 x 350 mm, about 10 kg | R13 **not met** on length by 10 mm |
| Parts cost | about $396 | R12 **not met** (budget $300) |

Requirements not met or at risk: R1 (cooling in warm rooms), R5 (temperature reference has no calibration certificate), R8 (particle traceability needs a collocation site), R12 (cost), R13 (footprint, by 10 mm). R3, R4 and R14 stay open until TRL 3.

### Proposed, awaiting Amish

1. **Budget.** Parts are about $396 against `budget_usd: 300`. Options: (a) raise to $400; (b) a core version without CO2 (drop the SCD30 and soda lime, about $329); (c) keep $300 by also dropping the second SHT45 and the insulation jacket, which weakens R4 and R1. Recommendation: (a). `project.yaml` is unchanged.
2. **Reference strategy.** Transfer references (SHT45, SCD30, collocated SPS30) checked against salt fixed points, an ice point and field collocation, rather than certified instruments. Recommendation: adopt, and state the uncertainty chain in every report.
3. **Cooling limit (R1).** Options: accept 10 °C only in rooms at 25 °C or below; add a second Peltier module (about $30, supply to 20 A); add an ice-water exchanger for cold runs. Recommendation: accept the limit for the first build.
4. **Test aerosol.** Incense smoke decay (recommended) versus a salt nebulizer or test dust. Reports would state the aerosol type.
5. **Gas scope.** AirStreet's README says it is "calibrated on CalRig" for PM2.5 and NO2. NO2 needs a certified gas cylinder, dilution and toxic gas handling. Options: a later add-on repo, a partner lab, or field collocation only for NO2. Recommendation: field collocation only for now, and align AirStreet's wording. Not changed in AirStreet.
6. **Door condensation.** Insulated door panel for hot, humid points (recommended), a double-glazed door or a heated film.
7. **Collocation partner** for the transfer SPS30: a regulatory monitoring station, a university site or an AQ-SPEC style program.

### Safety concerns

- Peltier hot side at 60 to 70 °C beside a combustible acrylic shell; independent thermal cut-offs and guarding are required.
- Water and electronics share the base: keep electronics outside and below the chamber, and use only a certified external 12 V supply.
- Smoke contains fine particles and some carbon monoxide; clear the chamber through the HEPA loop before opening, and ventilate the room.
- Soda lime (corrosive) and lithium chloride (harmful if swallowed) need gloves, eye protection and labeling.
- Exhaled-air CO2 checks need a single-user bag and filter.

### Gaps against the brief

- None known. The EPA numeric PM2.5 targets are cited through the EPA sensor loan program QAPP, which quotes the 2021 report, because the report PDF itself was not read in full.

### Recommended next step

Review this note and the media. If approved, run `/advance-trl3` to write the calculation note (heat balance with a real Peltier curve, moisture and condensation check, reference uncertainty budget, decay model with wall deposition), build the parametric model with STEP export and the drawing sheet, and complete the priced BOM.

## Session 2026-09-25: TRL 3

Amish's instruction for this batch (2026-09-25): "you know the drill, nothing gets past TRL 3". He did not review this repo's TRL 2 items one by one, so the recommendations were adopted for TRL 3 work, open for his review, and nothing here is recorded as decided by him.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CLR-DDR-001 v0.1): items A1 to A6 adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review; O1 (collocation partner) stays "Proposed, awaiting Amish".
- `docs/04-calcs/01-sizing.md` (CLR-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: geometry and mass, heat balance with a thermoelectric module model, moisture, condensation and conditioners, PI stability simulation, bay uniformity, reference uncertainty budgets, particle clean-down and decay, CO2, throughput, power and cost, with a results table for R1 to R18. The script imports the model's PARAMS and part solids and reads the BOM and `project.yaml`.
- `cad/src/model.py`: parametric build123d model (massing plus: chamber, full jacket and door panel, Peltier opening and sinks, six bays at the R10 head size, ports, conditioning column, base parts). Exports `cad/step/` and `cad/stl/` `calrig-assembly`, `chamber` and `conditioning`.
- `cad/src/sheets.py` and `cad/drawings/CLR-DWG-001.svg`, `.pdf`, `.png`: general arrangement, Rev P1, "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept blueprint stays CLR-DWG-010.
- `bom/bom.csv` (every line priced with a supplier type; total $404) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from `model.py`; all media refreshed (`hero`, `cutaway`, `exploded`, `flow`, `concept-blueprint`, `model.glb`, `viewer.html`) and checked by eye; temporary `_views` folders deleted.
- CLR-PRB-001, CLR-PRC-001 and CLR-REQ-001 bumped to v0.3 (R1 redefined per A3; statuses and numbers from CLR-CAL-001; design choices shown as adopted for TRL 3, open for review). `README.md` TRL badge, links and performance paragraph updated; the required sections are unchanged. `project.yaml`: `trl: 3`, `trl_target: 3`, evidence listed. Pitch, problem and `budget_usd` unchanged.

### Requirement status (CLR-CAL-001, Table 4)

Met 10, at risk 3, not met 4, not verifiable at TRL 3 1.

- **Not met:** R2 (85 % RH at 20 °C cannot be held in rooms above about 19 °C: the inner Peltier sink runs 1.2 K below the dew point and condenses about 8 g/h against 0.7 g/h from the bubbler); R8 (no collocation site yet); R12 ($404 against $300, and $4 over the proposed $400); R13 (mass 13.4 kg against 12 kg; 600 x 500 x 374 mm now fits).
- **At risk:** R4 (±0.18 °C at the EPA points with the 120 mm fan, ±0.42 °C at 10 °C); R5 (0.14 °C with the typical SHT45 tolerance, 0.24 °C if it is 0.2 °C); R6 (2.0 % RH, no margin).
- **Not verifiable at TRL 3:** R14 (software).
- **Met:** R1 (8.9 °C in a 25 °C room, 13.3 °C in a 30 °C room), R3 (idealized model), R7 (28 min decay), R9, R10, R11 (5.6 h), R15 (89 W, 7.4 A), R16, R17, R18.

Design changes made by the calculations: jacket on all faces but the door (conductance 0.82 W/K); 120 mm mixing fan; bubbler foam sleeve, 0.3 L fill and a trace-heated outlet line; base trimmed to 600 x 500 mm with the chamber moved so the aerosol valve stays on it. TRL 2 numbers corrected: gains 6.7 W (was 4 W), peak power 89 W (was 70 W), bus 7.4 A (was 6 A), mass 13.4 kg (was 10 kg), sweep 5.6 h (was 6 h), cost $404 (was $396).

### Decisions recorded (CLR-DDR-001)

Each adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: A1 budget rise to $400 (recorded only; `budget_usd` stays $300), A2 transfer references, A3 accept the cooling limit (R1 redefined), A4 incense smoke decay, A5 NO2 by field collocation only, A6 insulated door panel.

### Still awaiting Amish

1. **Budget figure.** $300 in `project.yaml`; $400 proposed; design now $404. Options: accept $404 or about $410; drop CO2 for a core version at about $337; or find $4 of savings.
2. **Collocation partner (O1)** for the transfer SPS30. No recommendation.
3. **Inner Peltier sink (R2).** Proposed: a larger inner fin block, about 0.20 K/W, so the 20 °C, 85 % RH point runs in rooms up to about 28 °C. Alternative: run that point only in a room below 19 °C. Recommendation: the larger sink, about $5 to $10 more.
4. **Mass (R13).** Options: carry the supply and salt jars separately (about 12.2 kg), use 5 mm acrylic, or relax R13 to 14 kg. Recommendation: relax to 14 kg; it is a bench rig.
5. **Reference temperature (R5).** Options: accept the risk, or add a certified thermistor probe or a second fixed point. Recommendation: a certified probe, if the budget allows.

### Cross-repo notes

- CalRig depends on no shared component. Siblings that use it: AirStreet (PM, T and RH; NO2 by field collocation, which matches A5; its pitch line still says "calibrated on CalRig" and is AirStreet's to change), DustBadge (low-level smoke checks only, consistent), HeatMap Node, SlopeWatch, TwinKit, FieldNode users.
- Possible conflict, not edited: HeatMap Node's 150 mm black globe and SlopeWatch's 34 x 130 mm capsule exceed the 90 x 70 x 50 mm bay size in R10. Both fit the chamber (244 mm clear above the tray) if they take two bays; R10 could add a "large item" case.
- H2Guard suggested a hydrogen span check on CalRig. That is outside A5 and is not adopted.

### Safety concerns

- Peltier outer sink up to about 50 °C and inner sink about 46 °C when heating; cut-offs at 70 °C hot side and 50 °C air stay required. Keep the sinks clear of the acrylic.
- Condensate on the inner sink at cold and humid points: a drip tray and drain are needed, and electronics stay below and outside the chamber.
- The new trace heater and bubbler pad each need a thermistor and must be switched off by the same cut-off.
- Smoke (fine particles and some CO), soda lime and lithium chloride precautions as at TRL 2.

### Gaps and notes

- The EPA PM2.5 target values are still cited through the EPA sensor loan program QAPP. WebFetch confirmed the EPA/600/R-20/280 record page but not the values in the PDF; the flag stays. WebSearch was not available. The SHT45 product page confirms ±0.1 °C and 1 % RH typical; the maximum tolerance and hysteresis used in CLR-CAL-001 are stated assumptions.
- No TRL 4 material exists in the repo (`firmware/` and `electronics/` are empty; `build-log/README.md` is the stock header only).
- The kit's cutaway cuts at the mean Y of the parts, which keeps the tray, mast, fan and Peltier in the section; the sensors under test fall mostly in the removed half. Left as is.
- `cad/drawings/.gitkeep` was removed now that the folder holds the drawing.

### Recommended next step

Review CLR-DDR-001 and the five items above. TRL 4 is on hold by Amish's instruction; nothing further should be done until he lifts it. For the record, TRL 4 would need a built chamber, a lab test report (TST, `environment: lab`) with logged temperature, humidity, uniformity and decay runs, salt and ice-point reference checks, and build log entries.
