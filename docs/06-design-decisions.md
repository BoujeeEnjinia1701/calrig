---
doc_id: CLR-DEC-001
title: CalRig design decisions register
project: CalRig
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open items gathered from the review note, the decision records and the build work
---

# CalRig design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Review the design-for-construction changes P1 to P12 (front frame and four latches, door panel fixing, heat pump clamping, fan spacers, tray legs, mast, air-loop bulkheads and pumps, HEPA bulkheads, back-wall glands, drip tray and drain, aerosol bulkhead, jar rack) and the 9 mm base, made under Amish's 2026-09-30 instruction to make the design physically buildable | Accept; or change any item | Accept | The whole build plan | CLR-DDR-003, Tables 1 and 2 |
| 2 | Budget: the parts that make the design buildable bring the BOM to $439, $27 over `budget_usd` of $412 (R12 not met) | (a) raise the budget to $439; (b) a core version without carbon dioxide (about $372), which changes what the rig does; (c) find $27 of savings | (a) | Bill of materials; none of the build steps | CLR-DDR-003, A1 |
| 3 | Mass margin: 13.8 kg against the 14 kg of R13, a 0.17 kg margin on estimated masses | (a) accept and weigh the prototype at TRL 4; (b) save more mass now, for example a 5 mm acrylic top | (a) | Section 5 mass check | CLR-DDR-003, A2 |
| 4 | Base plate material: the appearance model shows dark HDPE, which at 12 mm would take the rig to about 15.8 kg | (a) sealed 9 mm birch plywood, as modelled; (b) HDPE with R13 relaxed again; (c) 6 mm HDPE on more feet | (a); HDPE for renders only if preferred | Base plate (section 3.1) | CLR-DDR-003, A3; REVIEW 2026-09-26, item 2 |
| 5 | Collocation partner for the transfer SPS30 particle sensor (R8 not met until one is named) | A regulatory monitoring station, a university site or an AQ-SPEC style program | None yet | Not part of the build; needed before the SPS30 is used as the reference | CLR-DDR-001, O1 |
| 6 | Appearance model items 1 and 3 to 9: faced, rounded jacket; front status light and name plate; printed door border; door panel pull handle; bubbler and dryer details; fan guards; example sensor heads; aerosol valve lever | Adopt for renders, adopt in the design, or drop, item by item | As recorded in the review note (mostly adopt for renders; decide on facing and status light at TRL 4) | Renders only, except the status light (controller wiring) and the pull handle (door panel) | REVIEW 2026-09-26, items 1 and 3 to 9 |
| 7 | Report format that a city or funder would accept as calibration evidence | Open | None yet | Not part of the build; affects the fitting software (R14) | CLR-PRC-001, open questions |
| 8 | Larger sensor heads (HeatMap Node's 150 mm globe, SlopeWatch's capsule) that exceed the 90 x 70 x 50 mm bay size of R10 | Add a "large item" case to R10 that takes two bays; or leave them to other rigs | None yet | Sensor tray bay layout (section 3.9) | REVIEW 2026-09-25, cross-repo notes |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The heat pump's sink bases are at least 120 x 110 mm and take four M4 clamp screws at 57 mm either side and 42 mm above and below centre | The bases clamp the wall over the 90 x 100 mm opening; the shell's clamp holes are cut to match | CLR-DDR-003, P3 |
| 2 | An inner fin block and fan that reach about 0.20 K/W | R2 at 20 °C and 85 % RH depends on it | CLR-DDR-002, D7; CLR-PRC-001, open questions |
| 3 | The draw latches fit a 41 x 40 mm tab and reach a keeper 15 mm in from the tab edge | Sets the frame tab size and the keeper position | CLR-DDR-003, P1 |
| 4 | The thread sizes of the bulkhead fittings (12 and 6 mm), cable glands (M20) and aerosol bulkhead (16 mm), and that the multi-hole gland inserts suit the sensor leads | The shell holes are laser cut to these sizes before anything is fitted | CLR-DDR-003, P7 to P11 |
| 5 | The HEPA unit's ports are 12 mm and 80 mm apart at 117 mm above the bench, or can be drilled to that | The back-wall fittings run straight into them | CLR-DDR-003, P8 |
| 6 | The SHT45 tolerance the supplier states (0.1 or 0.2 °C) | R5 is at risk if it is 0.2 °C | CLR-CAL-001, [F1] |
| 7 | The bimetal switches and relay: opening temperatures of 50 and 70 °C and a relay rated 10 A at 12 V direct current | R16 rests on them | CLR-DDR-003, Table 2 |

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items A1 to A6: budget raised to $400, transfer references checked at salt and ice fixed points, accept the cooling limit (R1 redefined), incense smoke decay, carbon dioxide optional and nitrogen dioxide by field collocation only, insulated door panel | Amish: "i accept all your recommendations, go with them across all repos." | CLR-DDR-001, CLR-DDR-002 |
| 2026-09-25 | Larger inner fin block (about 0.20 K/W); R13 relaxed to 14 kg; certified temperature probe only if the budget allows | Amish, same instruction | CLR-DDR-002, D7 to D9 |
| 2026-09-26 | Budget set to $412 to cover the priced BOM as it then stood | Amish: "i approve all the budget items." | CLR-DDR-002, O2 |
