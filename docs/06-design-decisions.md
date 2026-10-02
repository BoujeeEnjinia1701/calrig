---
doc_id: CLR-DEC-001
title: CalRig design decisions register
project: CalRig
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; open items gathered from the review note, the decision records and the build work
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: 'Amish approved the recommendations for all seven open decisions on 2026-10-02 (CLR-DDR-003 accepted); moved to decisions made'
---

# CalRig design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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

## Value engineering

Value-engineering target: USD 412 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 439 (USD 27 over the target).

Main cost drivers (CLR-CAL-001, K): the reference cluster (line 8, $132), the chamber shell (line 1, $51), the Peltier heat pump (line 5, $40) and the parts added for construction ($27, of which new line 19, bulkhead fittings, cable glands and drain, is $14). The CO2 path (SCD30 in the reference cluster and soda lime, line 16, $8) is the largest block that is not core to the temperature, humidity and particle functions.

Savings worth trying:

- A core version without CO2 (no SCD30, no soda lime), about USD 372; this changes what the rig does and would be proposed, not made (CLR-DDR-003, A1).
- Re-pricing the fittings, glands and drain (line 19) and the front frame, drip tray and spacers ($6) at purchase.
- Looking for savings in the reference cluster and shell; no single line obviously offers $27.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items A1 to A6: budget raised to $400, transfer references checked at salt and ice fixed points, accept the cooling limit (R1 redefined), incense smoke decay, carbon dioxide optional and nitrogen dioxide by field collocation only, insulated door panel | Amish: "i accept all your recommendations, go with them across all repos." | CLR-DDR-001, CLR-DDR-002 |
| 2026-09-25 | Larger inner fin block (about 0.20 K/W); R13 relaxed to 14 kg; certified temperature probe only if the budget allows | Amish, same instruction | CLR-DDR-002, D7 to D9 |
| 2026-09-26 | Budget set to $412 to cover the priced BOM as it then stood | Amish: "i approve all the budget items." | CLR-DDR-002, O2 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12 and their knock-on changes, including the 9 mm sealed birch plywood base, as made | Amish: "i approve your recommendations for all 555 open decisions." | CLR-DDR-003, Tables 1 and 2 |
| 2026-10-02 | Mass margin of 0.17 kg accepted on paper; the finished rig is weighed at TRL 4, and a 5 mm acrylic top is the first fallback if it weighs over 14 kg | Amish: "i approve your recommendations for all 555 open decisions." | CLR-DDR-003, A2 |
| 2026-10-02 | Base plate: sealed 9 mm birch plywood, as modelled; the renders are to show plywood too, so they match what will be built | Amish: "i approve your recommendations for all 555 open decisions." | CLR-DDR-003, A3; REVIEW 2026-09-26, item 2 |
| 2026-10-02 | Collocation partner for the transfer SPS30: a state or local regulatory monitoring site with a federal equivalent PM2.5 monitor. First candidate to approach: a Texas Commission on Environmental Quality site in Dallas-Fort Worth; fallback: South Coast AQMD's AQ-SPEC program | Amish: "i approve your recommendations for all 555 open decisions." | CLR-DDR-001, O1 |
| 2026-10-02 | Appearance model items: jacket facing (1) in renders only, decided at TRL 4; status light and name plate (3), printed door border (4, with no gland in the door, since P9 put the glands in the back wall) and door panel pull handle (5) adopted in the design; bubbler and dryer details, fan guards, example heads and valve lever (6 to 9) accepted as drawn | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, items 1 and 3 to 9 |
| 2026-10-02 | Calibration report based on the US EPA 2021 performance targets and testing protocol for PM2.5 air sensors, with a stated uncertainty chain from the salt and ice fixed points and the collocation record | Amish: "i approve your recommendations for all 555 open decisions." | CLR-PRC-001, open questions |
| 2026-10-02 | R10 gains a large item case: a head up to 192 x 152 mm in plan takes a 2 x 2 block of four bays, and a head up to 192 x 70 mm takes two bays side by side, within the 244 mm clear height | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-25, cross-repo notes |
