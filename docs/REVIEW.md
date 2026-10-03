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

*Update 2026-09-25: items 1 to 6 are Decided by Amish, 2026-09-25: go with recommendation (CLR-DDR-002). Item 7 remains Proposed, awaiting Amish.*

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

*Update 2026-09-25: A1 to A6 are now Decided by Amish, 2026-09-25: go with recommendation (CLR-DDR-002).*

Each adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: A1 budget rise to $400 (recorded only; `budget_usd` stays $300), A2 transfer references, A3 accept the cooling limit (R1 redefined), A4 incense smoke decay, A5 NO2 by field collocation only, A6 insulated door panel.

### Still awaiting Amish

*Update 2026-09-25: items 3, 4 and 5 are Decided by Amish, 2026-09-25: go with recommendation (CLR-DDR-002). Items 1 (budget figure above $400) and 2 (O1) have no recommendation and remain Proposed, awaiting Amish.*

1. **Budget figure.** $300 in `project.yaml`; $400 proposed; design now $404. Options: accept $404 or about $410; drop CO2 for a core version at about $337; or find $4 of savings. **Decided by Amish, 2026-09-26: budget set to $412** (CLR-DDR-002).
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

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (CLR-DDR-002 v0.1). CLR-DDR-001 is bumped to v0.2 with A1 to A6 marked decided.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| Budget (A1) | Raise `budget_usd` to $400 | $300 | $400 in `project.yaml`; design $412, R12 still not met |
| Reference strategy (A2), cooling limit (A3), test aerosol (A4), door panel (A6) | As recommended | Adopted for TRL 3, open for review | Decided; wording only |
| Gas scope (A5) | NO2 by field collocation only; align AirStreet | Adopted, open for review | Decided; AirStreet wording is a cross-repo action |
| Inner Peltier sink (R2) | Larger inner fin block, about 0.20 K/W | 30 x 80 x 90 mm, 0.45 K/W; sink 16.2 °C at 20 °C, 85 % RH; dry below a 19 °C room; R2 not met | 45 x 120 x 110 mm, 0.20 K/W; sink 18.3 °C (0.9 K above dew point); dry up to a 28 °C room; R2 met |
| Mass (R13) | Relax to 14 kg | 12 kg limit, 13.4 kg, not met | 14 kg limit, 13.6 kg, met |
| Reference temperature (R5) | Certified probe if the budget allows | No probe | Budget does not allow ($412 against $400); no probe added; R5 at risk |

Knock-on numbers from CLR-CAL-001 v0.2: BOM line 5 $30 to $38, total $404 to $412; lowest chamber temperature 8.9 to 6.7 °C (25 °C room) and 13.3 to 11.1 °C (30 °C room); cooling to 10 °C 3.7 to 2.4 h; sweep plus particle run 5.6 to 5.5 h; peak power 89 to 90 W (7.5 A); core version without CO2 $337 to $345.

Files changed: `project.yaml` (budget, DDR-002 in evidence), `README.md` (budget, concept paragraph, key components, "What sparked the idea" rewritten), CLR-PRB-001 v0.4, CLR-PRC-001 v0.4, CLR-REQ-001 v0.4, CLR-CAL-001 v0.2 and `sizing.py`, CLR-DDR-001 v0.2, new CLR-DDR-002 v0.1, `cad/src/model.py` (STEP and STL re-exported), `cad/src/sheets.py` (CLR-DWG-001 Rev P2), `cad/src/concept_media.py` (key figures; all media regenerated and checked by eye), `bom/bom.csv`, `bom/bom-notes.md`. All PDFs, drawings and media re-rendered with the Design Molecule footer.

### Requirement status (CLR-CAL-001 v0.2)

Met 12, at risk 3, not met 2, not verifiable at TRL 3 1.

- **Not met:** R8 (no collocation site; O1 open), R12 ($412 against $400).
- **At risk:** R4 (±0.42 °C between bays at 10 °C), R5 (0.24 °C if the SHT45 tolerance is 0.2 °C; probe deferred), R6 (2.0 % RH, no margin).
- **Not verifiable at TRL 3:** R14 (software).
- **Met:** R1, R2 (now), R3, R7, R9, R10, R11, R13 (now), R15, R16, R17, R18.

### Still awaiting Amish

1. **Collocation partner (O1)** for the transfer SPS30. No recommendation.
2. **Budget figure above $400 (O2).** Design is $412. Accept about $412, drop CO2 for a core version at about $345, or find $12 of savings. No recommendation. **Decided by Amish, 2026-09-26: budget set to $412** (CLR-DDR-002).

### Cross-repo actions

- **AirStreet:** align the pitch line "calibrated on CalRig" with NO2 by field collocation only (decision A5). Not edited from this repo.
- Note, no decision: HeatMap Node's 150 mm globe and SlopeWatch's capsule exceed the R10 bay size; they fit the chamber if they take two bays.

### TRL

`trl: 3`, `trl_target: 3`. TRL 4 remains on hold by Amish's instruction: no build, test, purchasing, PCB or firmware work was done. The certified probe (D9) would be a purchase and is not bought.

## Session 2026-09-26: budget approved

Amish wrote on 2026-09-26: "i approve all the budget items." Budget set to $412 to cover the priced BOM: decided by Amish, 2026-09-26. This closes O2.

- `project.yaml` `budget_usd` $400 to **$412**. The priced BOM is unchanged at $412 (18 lines).
- R12 (cost): target $400 to $412; status **Not met to Met**. Requirement status is now met 13, at risk 3, not met 1 (R8, collocation site), not verifiable at TRL 3 1 (R14).
- The certified temperature probe (D9, "if the budget allows") is still not added: the new budget has no headroom for it, so R5 stays at risk.
- Files changed: `project.yaml`, `README.md`, CLR-PRB-001 v0.5, CLR-PRC-001 v0.5, CLR-REQ-001 v0.5, CLR-CAL-001 v0.3 (`sizing.py` rerun), CLR-DDR-002 v0.2, `bom/bom-notes.md`, `cad/src/concept_media.py` (blueprint key figure); media and PDFs regenerated, temporary `media/_views*` folders deleted.
- Still awaiting Amish: O1 (collocation partner). `trl: 3` and `trl_target: 3` are unchanged; TRL 4 remains on hold.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose CalRig for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal product shots. It does not change the design, `cad/src/model.py`, the BOM or any controlled document.

### What was added

- `cad/src/product_model.py`: `product_parts()` (99 parts: 65 shell, 31 internal, 2 accessory, 1 context), `TITLE` and `RENDER_VIEWS` (hero, exploded and a detail view without the bench). Every main dimension, position and interface is taken from `PARAMS`, `derived()` and `build_parts()` in `model.py`; the clear chamber shell is the `model.py` solid itself.
- Finished-product detail: the insulation jacket as five filleted panels with seams where they meet (bottom, top, back, left, right, as in `model.py`), a teal name plate and a lit status light on the top band; the clear door with a printed dark border, silicone gasket line, two draw latches with levers and rivets and the sensor lead gland; inside, the perforated six-bay tray with its cable rail and hub connectors, six example sensor heads in three styles with serial labels and lit status lights, the reference cluster on its printed mast with a teal vented front plate, the guarded 120 mm mixing fan and the finned inner Peltier block; outside, the finned outer sink and guarded 92 mm fan, the foam-sleeved bubbler with glass jar and knurled lid, the dryer column with indicating silica gel, the aerosol port with ball valve, lever and Luer port, the HEPA housing, controller, power supply and DC lead, four salt jars with coloured lids and labels, base plate screws and the removable door panel with a pull handle (accessory group, exploded view only).
- Context: a compact lab bench top (800 x 600 mm) under the 600 x 500 mm base plate.
- `README.md`: hero image now points to `media/render-hero.png`, and the links line starts with the exploded render. The render files are produced later by the orchestrator.

### Differences from model.py (appearance only)

Each item is **Proposed, awaiting Amish**.

1. **Faced, rounded jacket.** The XPS jacket is drawn with a smooth light-grey facing, 12 mm vertical and 10 mm top corner radii and visible panel seams; `model.py` has bare, square XPS panels. Recommendation: keep this look for renders only and decide on a facing (for example thin PVC sheet) at TRL 4, when its cost can be checked against the $412 budget.
2. **Base plate in dark HDPE** with 22 mm corner radii and four screw heads. The BOM allows plywood or HDPE. Recommendation: HDPE, since the rig holds water.
3. **Front status light and name plate** on the top band of the jacket, driven by the controller (BOM 13). Not in `model.py` or the BOM. Recommendation: adopt; a single LED and a label add little cost and show run state without opening the rig.
4. **Door details.** Printed border (22 mm), gasket line and a lead gland at the lower right of the door. BOM line 2 lists the gasket and gland but `model.py` gives no gland position. Recommendation: adopt the border (it hides the shell edges and wiring) and confirm the gland position at TRL 4.
5. **Door panel pull handle.** Not in `model.py` or the BOM. Recommendation: adopt; the panel is removed for every warm, dry point.
6. **Bubbler and dryer.** The foam sleeve stops 16 mm below the jar top so the glass and a knurled lid show; the overall height is unchanged. The wet and dry lines are drawn as round tubes (12 mm sleeved and 9 mm silicone) on the `model.py` routes instead of square bars. Recommendation: accept as drawn.
7. **Fan guards** on the outer 92 mm fan and the mixing fan, as the precis and BOM line 6 require; `model.py` shows plain boxes. Recommendation: accept.
8. **Example sensor heads** in three housing styles, each inside the `model.py` bay envelope, with lit status lights. They are example payload, not BOM items. Recommendation: accept.
9. **Aerosol valve lever** stands about 19 mm above the `model.py` valve envelope. Recommendation: accept; it is within the overall footprint.

### Checks

All parts are valid solids and tessellate; `python .kit/product_export.py` and `python .kit/render.py --check` pass. Matplotlib previews of the three views were checked by eye (clear parts left out of the previews).

### TRL

This is an appearance model only: no tolerances, no fabrication detail. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold. Still awaiting Amish: O1 (collocation partner) and items 1 to 9 above.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: design for construction and illustrated build plan (BLD-001)

Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with outstanding decisions kept out of the build plan and in a separate design decisions register. Kit 1.7.0 was installed (`.kit/`, `.claude/commands/`, `CLAUDE.md`). Instruction followed: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations."

### What was done

- `cad/src/model.py`: rebuilt as separate components (`build_components()`), with the BOM groups kept for the calculation note, drawing and media (`build_parts()`), and 79 build123d constructability checks (`python cad/src/model.py --check`): all pass. STEP and STL re-exported.
- `docs/decisions/0003-design-for-construction.md` (CLR-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `cad/src/build_plan_media.py`: overview, eleven making sketches (CLR-DWG-101 to 111), nine joint close-ups, thirteen step pictures, and four diagrams (wall hole positions, base layout, air loops, block-level wiring), in `docs/05-build-plan/` and `cad/drawings/`.
- `docs/05-build-plan.md` (CLR-BLD-001 v0.1) and `docs/06-design-decisions.md` (CLR-DEC-001 v0.1).
- `bom/bom.csv` (lines 1, 2, 3, 4, 5, 10, 13 and 15 revised; new line 19) and `bom/bom-notes.md`; CLR-CAL-001 v0.4 (`sizing.py` re-run), CLR-REQ-001 v0.6, CLR-PRC-001 v0.6; CLR-DWG-001 Rev P4; concept media regenerated (`hero`, `cutaway`, `exploded` with line 19, `flow`, `concept-blueprint`, `model.glb`, `viewer.html`).
- `project.yaml`: `design_state: constructable`; build plan, register, DDR-003 and overview picture added to `trl_evidence`. `budget_usd` unchanged at $412. README: build plan link, "Building the prototype" section, performance paragraph updated.

### Design changes made for construction (CLR-DDR-003)

1. **Door (P1):** a 450 x 350 mm acrylic front frame welded to the shell gives the gasket a 25 mm face; the door is 430 x 330 mm; four draw latches (was two) on frame tabs hook keepers on the door.
2. **Door panel (P2):** 406 x 330 mm on the door between the latches, on four hook-and-loop pads (was a loose full-front panel).
3. **Heat pump (P3):** both sink bases clamp the right wall with four M4 screws through rigid sleeves in the jacket.
4. **Mixing fan (P4):** on four welded 15 mm spacers on the back wall (was floating).
5. **Sensor tray (P5):** 10 mm legs (were 5 mm posts); 87-hole perforation defined.
6. **Reference mast (P6):** printed 20 mm mast standing on the floor, screwed to the tray rail (was floating behind the tray).
7. **Conditioning loop (P7):** three 12 mm bulkheads in the right wall, including a new suction port; two pumps on the base; dryer line now reaches the column; printed dryer socket; bubbler 10 mm further back.
8. **HEPA loop (P8):** two 12 mm bulkheads in the back wall into the HEPA unit (it had no connection).
9. **Leads (P9):** two M20 multi-hole cable glands in the back wall instead of one gland in the door; the hub moves to the controller.
10. **Drip tray and drain (P10):** welded tray under the inner sink, 6 mm drain bulkhead, line to a 250 mL bottle (in the precis but not in the model).
11. **Aerosol port (P11):** 16 mm bulkhead sealing in a 16 mm hole (was a stub floating in a 20 mm hole).
12. **Salt jars (P12):** printed rack.
13. **Knock-on:** base 9 mm sealed birch plywood (was 12 mm plywood or HDPE) to stay within 14 kg; overall height 371 mm; cut-offs hold in a relay on the Peltier and heater supply.

### Key results

- Mass 13.83 kg against 14 kg (R13 met, 0.17 kg margin). Value-engineering target $412 (a hypothetical control target, not a limit); estimated cost of the constructable design $439 on 19 lines ($27 over the target): **R12 over the value-engineering target**. Heat capacity 8.7 kJ/K; 10 °C reached in 2.5 h; every other result unchanged.
- Requirement status (CLR-CAL-001 v0.4): met 12, at risk 3 (R4, R5, R6), not met 1 (R8), over the value-engineering target 1 (R12), not verifiable at TRL 3 1 (R14).

### Proposed, awaiting Amish

All in the design decisions register (CLR-DEC-001): review of CLR-DDR-003 (recommend accept); mass margin (accept, weigh at TRL 4); base material (sealed plywood); plus the items carried over (savings worth trying against the value-engineering target are in the register's value engineering section): collocation partner (O1), appearance model items, report format, large sensor heads in R10.

### Stale images (made on Amish's Mac, not regenerated here)

`media/render-*.png`, `media/card.png`, `media/social-preview.png` and `cad/src/product_model.py` still show the concept door, two latches, the full-front door panel, the 12 mm base and no bulkheads, glands or drain. They need updating on Amish's Mac.

### Safety concerns

- The new drain and drip tray keep condensate inside the right wall away from the electronics; the electronics stand behind the chamber.
- Cut-offs now drive a relay so a small bimetal switch is not asked to break the Peltier current; to be checked in section 5 of the build plan.
- Solvent cement and laser-cut acrylic fumes added to the safety stops.

### Recommended next step

Amish reviews CLR-DDR-003 and the register, and the value engineering section. TRL 4 (building and testing to CLR-BLD-001) stays on hold.

## Session 2026-10-02: open-decision recommendations approved

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation for every open decision in the design decisions register. 7 decisions were recorded: each moved to Decisions made, dated 2026-10-02, with the approved recommendation and its record. trl stays 3; no build or test work was done, and the CAD model, BOM quantities and prices, and pictures were not changed.

### Documents changed

- `docs/06-design-decisions.md` (CLR-DEC-001 v0.3): the seven open decisions moved to Decisions made; Open decisions now reads none
- `docs/decisions/0003-design-for-construction.md` (CLR-DDR-003 v0.3): status accepted (Tables 1 and 2, A2 and A3) with Amish's words; A2 records the 5 mm acrylic top as the first fallback, A3 the plywood renders; A1 stays proposed
- `docs/decisions/0001-trl2-review-decisions.md` (CLR-DDR-001 v0.3): O1 (collocation partner) decided
- `docs/decisions/0002-recommendations-accepted.md` (CLR-DDR-002 v0.3): O1 (collocation partner) decided
- `docs/03-requirements.md` (CLR-REQ-001 v0.8): R8 names the first candidate site (status unchanged, not met); R10 adds the large item case; R14 states the EPA 2021 report basis and uncertainty chain
- `docs/04-calcs/01-sizing.md` (CLR-CAL-001 v0.6): requirement table wording for R8, R10 and R14; no result changed
- `docs/02-concept.md` (CLR-PRC-001 v0.8): open questions on the particle reference and report format answered; large heads take two or four bays
- `docs/01-problem.md` (CLR-PRB-001 v0.6): open questions on collocation and report format answered
- `README.md`: concept paragraph: larger heads take two or four of the six bays
- `bom/bom-notes.md`: base material and the adopted appearance items noted; no quantity or price changed
- PDFs regenerated with `python3 .kit/render.py`; superseded PDF versions removed by the render.

### Follow-up actions to carry approved decisions into the design

1. Decision 3 (pictures): Redraw the photoreal renders, `media/card.png` and `media/social-preview.png` from `cad/src/product_model.py` with the 9 mm sealed birch plywood base instead of dark HDPE (on Amish's Mac)
2. Decision 5 (model): Add the front status light and name plate, the printed door border and the door panel pull handle to `cad/src/model.py` and its constructability checks; draw no gland in the door
3. Decision 5 (drawings): Show the status light, name plate, door border and pull handle on CLR-DWG-001 and the door and door panel making sketches
4. Decision 5 (bom): Add BOM lines or line changes for the status light and its controller wiring, the name plate, the door border and the pull handle, and price them
5. Decision 5 (pictures): Regenerate the build plan pictures for the door, door panel and controller steps, and update the appearance model renders (four latches, glands in the back wall, jacket facing in renders only)
6. Decision 5 (docs): Add the status light wiring and pull handle to the build plan text (CLR-BLD-001) once they are in the model
7. Decision 7 (model): Add a model check that a 192 x 152 mm head fits a 2 x 2 block of bays and a 192 x 70 mm head two bays side by side, within the 244 mm clear height
8. Decision 7 (calcs): Add the large item case to `sizing.py` and CLR-CAL-001 section A, and confirm the R10 status
9. Decision 6 (docs): Define the per-sensor report template (R14) to the US EPA 2021 targets and protocol, with the uncertainty chain from the fixed points and the collocation record

### Points found in the review

- The cross-repo note says the large heads fit "if they take two bays"; the 150 mm HeatMap Node globe spans both 70 mm bay rows and two columns of the 318 x 176 mm tray, so it takes four bays, not two.
- The 2026-09-26 appearance note recommends an HDPE base (item 2) and a door gland (item 4); both are now superseded by DDR-003 (9 mm plywood for R13, glands in the back wall) and the appearance model still shows two latches, not four.
- R12 cost ($439 against the $412 target) is not an open register item; DDR-003 A1 recommended keeping the design and re-pricing at purchase. Confirm Amish is content to leave it in the value engineering section.

## 2026-10-02: Approved follow-ups carried out

Amish, 2026-10-02, approved carrying out every follow-up action from the open-decision sign-off ("APPROVED CHANGES, COMPLETE THESE") and preparing the render scenes. TRL stays 3; nothing was built or tested.

### Follow-ups

| # | Follow-up | Done | What changed |
| --- | --- | --- | --- |
| 1 | Decision 3: renders, card and social preview with the 9 mm plywood base | Scenes ready | `cad/src/product_model.py` draws the base as sealed birch plywood from the `model.py` solid; render scenes exported (below). The photoreal renders, `media/card.png` and `media/social-preview.png` are made next on Amish's Mac |
| 2 | Decision 5: status light, name plate, door border and pull handle in `model.py`; no gland in the door | Done | Front badge (printed, 200 x 30 mm, lip on the front frame's top edge) with a 12 V panel light and the name plate; status light lead along the jacket top and back panel to the controller; 22 mm printed border on the door, cut round the keepers; printed pull handle on the door panel. No gland in the door. 37 new checks; 116 of 116 pass |
| 3 | Decision 5: show them on CLR-DWG-001 and the door and door panel sketches | Done | CLR-DWG-001 Rev P5 (door panel fitted, callouts and notes); CLR-DWG-110 Rev P2 (border); CLR-DWG-111 Rev P2 (door panel and pull handle); new CLR-DWG-112 (front badge) |
| 4 | Decision 5: BOM lines for the status light and wiring, name plate, door border and pull handle | Done | Line 2 border ($17 to $20), line 3 pull handle ($17 to $18), line 13 status light output (no price change), new line 20 front badge, status light, name plate and lead ($5.50); basis for each price in the line notes and `bom/bom-notes.md` |
| 5 | Decision 5: build plan pictures for the door, door panel and controller steps; appearance model with four latches, back-wall glands, jacket facing in renders only | Done | New step 12 (badge and lead to the controller), steps 13 (door with border) and 14 (door panel with handle), joint 10, overview (26 components), wiring diagram; `product_model.py` rebuilt from the `model.py` solids (four latches and keepers, back-wall glands and bulkheads, no door gland, faced jacket) |
| 6 | Decision 5: status light wiring and pull handle in the build plan text | Done | CLR-BLD-001 v0.2: section 3.15 (front badge and status light), wiring item 8, pull handle in 3.14, border in 3.13, step 12 and renumbered steps, first checks for the status light and large heads |
| 7 | Decision 7: model check for 192 x 152 mm heads on 2 x 2 bays and 192 x 70 mm heads on two bays within the clear height | Done | `large_heads()` in `model.py`: every pair (4) and block (2) position at 234 mm tall (10 mm under the chamber top); 18 checks pass (on the tray, inside its outline, 5 mm or more from walls, fan, inner sink, drip tray, aerosol port and references) |
| 8 | Decision 7: large item case in `sizing.py` and CLR-CAL-001 section A; R10 status | Done | New result [A4]; **R10 moves from met for six heads to met including the large item case** |
| 9 | Decision 6: per-sensor report template (R14) to the US EPA 2021 targets, with the uncertainty chain | Done | CLR-PRC-001 v0.9, new section and Table 4: identification, run conditions, reference status, fitted correction, EPA metrics against their targets, enhanced conditions, uncertainty chain (ice point, salt fixed points, collocation record), limits of use. R14 stays not verifiable at TRL 3 (software not written) |

### Model and checks

- `python cad/src/model.py --check`: 116 of 116 pass (was 79). New: border on the door and clear of the gasket, keepers through the border cut-outs, pull handle on the panel and clear of door, latches and badge, badge on the jacket top and on the frame's top edge and clear of door, panel and latches, light bezel and name plate on the badge, lead from the light, clear of the badge hole, along the jacket, onto the controller and clear of glands, HEPA bulkheads, heat pump, dryer and supply, and the 18 large-head checks.
- STEP and STL regenerated. Overall 600 x 500 x 383 mm (the badge top is now the highest point; the jacket top is at 371 mm).

### Requirement status changes (CLR-CAL-001 v0.7, CLR-REQ-001 v0.9)

- R10: met for six heads to **met**, including the large item case.
- R12: over the value-engineering target by USD 27 to **over by USD 36.50**. Value-engineering target: USD 412. Estimated cost of the constructable design: USD 448.50 (USD 36.50 over the target). `budget_usd` unchanged.
- R13: still met; 600 x 500 x 383 mm, 13.92 kg, margin 0.08 kg (was 0.17 kg). The 5 mm acrylic top fallback (DDR-003, A2) would recover about 0.15 kg.
- R14: still not verifiable at TRL 3; the report template is now defined.
- Counts unchanged: met 12, at risk 3 (R4, R5, R6), not met 1 (R8), over the value-engineering target 1 (R12), not verifiable at TRL 3 1 (R14).

### Documents changed and new versions

- `cad/src/model.py`, `cad/src/sheets.py` (also corrected its view mapping to the kit layout, so the dimensions sit on the views), `cad/src/concept_media.py`, `cad/src/build_plan_media.py`, `cad/src/product_model.py`; `cad/step/`, `cad/stl/`
- `docs/04-calcs/sizing.py` and `docs/04-calcs/01-sizing.md` CLR-CAL-001 v0.7
- `docs/03-requirements.md` CLR-REQ-001 v0.9; `docs/02-concept.md` CLR-PRC-001 v0.9
- `docs/05-build-plan.md` CLR-BLD-001 v0.2; `docs/06-design-decisions.md` CLR-DEC-001 v0.4 (value engineering restated; items 8 and 9 to confirm); `docs/decisions/0003-design-for-construction.md` CLR-DDR-003 v0.4 (consequences)
- `bom/bom.csv` (lines 2, 3, 13, new 20) and `bom/bom-notes.md`; `README.md`

### Pictures regenerated (each looked at)

- `cad/drawings/CLR-DWG-001` Rev P5, CLR-DWG-110 Rev P2, CLR-DWG-111 Rev P2, CLR-DWG-112 P1 (new).
- `docs/05-build-plan/overview.png`, `joint-10.png` (new), `step-12.png` to `step-14.png`, `wiring.png`; the other joints, steps and the air loop diagram were redrawn by the same run with no change of content.
- `media/hero.png`, `exploded.png` (callout 20 added; HEPA unit and fittings moved so their callouts no longer touch others), `cutaway.png`, `flow.png`, `concept-blueprint.png`, `.pdf` and `.svg` (key figures: 383 mm, 13.9 kg, cost in the value-engineering wording), `model.glb`, `viewer.html`.
- `python3 .kit/drawing.py --check-text cad/drawings/*.svg media/concept-blueprint.svg`: no hits.

### Render scenes (appearance model)

- `cad/src/product_model.py` now takes most parts directly from `build_components()` in `model.py`: plywood base, faced jacket with the model's holes, front frame, drip tray and spacers, door with printed border, gasket, four latches and keepers, clamped Peltier sinks and screws, mixing fan on its spacers, perforated acrylic tray, printed mast, five bulkheads, two back-wall glands, drain line and bottle, two pumps and suction line, dryer socket, jar rack, front badge with name plate and lit status light, the light's lead, and the door panel with its pull handle (accessory). `RENDER_VIEWS` keeps hero, exploded and detail.
- Exported with `python3 .kit/export_views.py /home/claude/renders/calrig`: `calrig__hero`, `calrig__exploded` and `calrig__detail` (.npz and .json each) and `calrig__jobs.json`.
- Not rendered here: `media/render-*.png`, `media/card.png` and `media/social-preview.png` are made next on Amish's Mac.

### Appearance deviations (Proposed, awaiting Amish)

1. Jacket facing with rounded corners and seams, as decided for renders only; the base plate has 4 mm rounded corners. Recommendation: accept as appearance only.
2. The badge is drawn dark grey, the name plate teal with illustrative print, and the status light lit green; the model has no colour. Recommendation: accept.
3. The tray is drawn as white acrylic with a dark cable rail and six hub connectors; the cable glands are drawn with hex bodies. Recommendation: accept.
4. The lines from the pumps to the bubbler and dryer are not drawn (they are not in the model either); items 6 to 9 of 2026-09-26 (bubbler and dryer details, fan guards, example heads, valve lever) are kept as decided. Recommendation: accept.

### Design detail chosen while carrying out decision 5 (for Amish's information)

- The front of the rig has no free face for a name plate: the front frame covers the jacket's front edges up to 6 mm from the top. The name plate and light therefore sit on a printed badge on the top panel, its lip resting on the frame's top edge. This raises the overall height from 371 to 383 mm (R13 limit 400 mm) and adds about 0.07 kg. If Amish prefers no added height, the alternative is a badge recessed into a notch in the top panel's front edge, at the cost of a harder cut in the foam. Proposed, awaiting Amish, and listed as open decision 1 in the design decisions register; the build plan describes the badge as modelled.

### Cross-repo actions

- HeatMap Node: its R14 note says the assembled 150 mm globe does not fit a CalRig bay. Under CalRig R10 (2026-10-02) a head up to 192 x 152 mm in plan and 234 mm tall fits a 2 x 2 block of four bays, checked in the model, so the assembled globe can be calibrated in CalRig if it is no taller than 234 mm. HeatMap Node's R14 text and status should be reviewed there. Not edited.

### Safety concerns

- The status light runs at 12 V from a switched controller output on a 0.25 mm² lead with a built-in resistor; it adds no new hazard. The lead is clipped along the outside of the jacket, away from the outer sink (about 60 mm clear) and the dryer.
- The pull handle lets the door panel come off without prying at the door near the hot outer sink.

### Recommended next step

Render the product views on Amish's Mac from the exported scenes, then `python .kit/cards.py .`. Decide the badge placement point above and confirm items 8 and 9 in the register when parts are bought. TRL 4 remains on hold.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model (`cad/src/product_model.py`); captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
