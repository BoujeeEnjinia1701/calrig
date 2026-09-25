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
