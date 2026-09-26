---
doc_id: CLR-DDR-002
title: CalRig recommendations accepted
project: CalRig
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the recommendations accepted by Amish on 2026-09-25, what changed in the repo, and the items still open
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below marked "Decided by Amish, 2026-09-25: go with recommendation" is accepted; items without a recommendation remain open.

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." This record lists every item in `docs/REVIEW.md` (TRL 2 and TRL 3 sessions) and in CLR-DDR-001 that carried a recommendation, now decided, and what changed in the repo. Items without a recommendation stay "Proposed, awaiting Amish". Where a recommendation offered several options, the recommended option is the decision. TRL 4 remains on hold by Amish's instruction, and `trl` and `trl_target` stay at 3.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (sessions 2026-09-25, /populate and TRL 3) and in CLR-DDR-001.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Budget (DDR-001 A1) | Raise `budget_usd` from $300 to $400 | `project.yaml` `budget_usd: 400`; R12 target restated as $400 in CLR-REQ-001 v0.4; README, CLR-PRB-001 v0.4, CLR-PRC-001 v0.4, BOM notes and CLR-CAL-001 v0.2 updated. The design is $412, so R12 is still not met |
| D2 | Reference strategy (DDR-001 A2) | Transfer references checked against salt fixed points, an ice point and field collocation; uncertainty chain in every report | Wording only: "decided" in CLR-PRC-001 v0.4 and CLR-DDR-001 v0.2 |
| D3 | Cooling limit (DDR-001 A3) | Accept 10 °C only in rooms at 25 °C or below; R1 as redefined in CLR-REQ-001 v0.3 | Wording only |
| D4 | Test aerosol (DDR-001 A4) | Incense smoke decay; aerosol type stated in every report | Wording only |
| D5 | Gas scope (DDR-001 A5) | NO2 by field collocation only; align AirStreet's wording | CLR-PRB-001 v0.4 wording. AirStreet's pitch line is listed as a cross-repo action in `docs/REVIEW.md`; AirStreet is not edited from this repo |
| D6 | Door condensation (DDR-001 A6) | Insulated removable door panel | Wording only (already in the model and BOM) |
| D7 | Inner Peltier sink (R2) | Larger inner fin block, about 0.20 K/W | `cad/src/model.py`: inner sink 30 x 80 x 90 mm to 45 x 120 x 110 mm and `sink_in_r` 0.20 K/W; STEP and STL re-exported; CLR-DWG-001 Rev P1 to P2; BOM line 5 $30 to $38; media regenerated. CLR-CAL-001 v0.2: inner sink at 20 °C, 85 % RH in a 22 °C room 16.2 °C to 18.3 °C (0.9 K above the dew point), dry up to about 28 °C (was 19 °C); R2 not met to met. Side effects: lowest chamber temperature in a 25 °C room 8.9 °C to 6.7 °C, in a 30 °C room 13.3 °C to 11.1 °C; cooling to 10 °C 3.7 h to 2.4 h; sweep plus particle run 5.6 h to 5.5 h; peak power 89 W to 90 W; mass 13.4 kg to 13.6 kg |
| D8 | Mass (R13) | Relax R13 from 12 kg to 14 kg; it is a bench rig | CLR-REQ-001 v0.4 R13 restated; CLR-CAL-001 v0.2 R13 not met to met (13.6 kg) |
| D9 | Reference temperature (R5) | Add a certified thermistor probe if the budget allows | The budget does not allow it ($412 against $400), so no probe is added to the BOM; R5 stays at risk. Recorded in CLR-PRC-001 v0.4, CLR-REQ-001 v0.4 and CLR-CAL-001 v0.2. Buying the probe would also be TRL 4 purchasing, which is on hold |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Collocation partner for the transfer SPS30. No recommendation was made. | Proposed, awaiting Amish |
| O2 | Budget figure above $400. The design is $412; options are to accept about $412, drop CO2 for a core version at about $345, or find $12 of savings. No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- Requirement status (CLR-CAL-001 v0.2): met 12 (was 10), at risk 3, not met 2 (was 4), not verifiable at TRL 3 1. Not met: R8 (collocation site, O1) and R12 ($412 against $400, O2).
- Documents bumped: CLR-PRB-001 v0.4, CLR-PRC-001 v0.4, CLR-REQ-001 v0.4, CLR-CAL-001 v0.2, CLR-DDR-001 v0.2; drawing CLR-DWG-001 Rev P2.
- Cross-repo action: AirStreet to align its "calibrated on CalRig" pitch line with NO2 by field collocation (D5). Not edited here.
- TRL 4 work (a built chamber, lab tests, buying parts, firmware beyond a sketch) remains on hold.
