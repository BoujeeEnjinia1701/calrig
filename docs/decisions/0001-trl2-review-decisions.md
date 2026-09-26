---
doc_id: CLR-DDR-001
title: CalRig TRL 2 review decisions
project: CalRig
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review recommendations adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** items A1 to A6 decided by Amish, 2026-09-25: go with recommendation (see CLR-DDR-002). Item O1 remains open.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed seven items as "Proposed, awaiting Amish". On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He did not review this batch item by item. Every item that carried a recommendation is therefore adopted as recommended for TRL 3 work, open for his review. Items without a recommendation stay open. On 2026-09-25 Amish then accepted all the recommendations ("i accept all your recommendations, go with them across all repos"), so A1 to A6 are now decided; see CLR-DDR-002.

## Options considered

The options for each item are those listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in CLR-PRC-001 v0.2, Open questions.

## Decision

*Table 1. Items decided.*

| # | Item | Recommendation adopted | Status |
| --- | --- | --- | --- |
| A1 | Budget | Option (a): raise `budget_usd` from $300 to $400. Set in `project.yaml` on 2026-09-25 (CLR-DDR-002). | Decided by Amish, 2026-09-25: go with recommendation. |
| A2 | Reference strategy | Transfer references (two SHT45, SCD30, collocated SPS30) checked against salt fixed points, an ice point and field collocation, with the uncertainty chain stated in every report. | Decided by Amish, 2026-09-25: go with recommendation. |
| A3 | Cooling limit (R1) | Accept 10 °C only in rooms at 25 °C or below for the first build; no second module or ice-water exchanger. R1 is redefined accordingly in CLR-REQ-001 v0.3. | Decided by Amish, 2026-09-25: go with recommendation. |
| A4 | Test aerosol | Incense smoke decay; every report states the aerosol type. | Decided by Amish, 2026-09-25: go with recommendation. |
| A5 | Gas scope | NO2 by field collocation only for now; no gas cylinder, dilution or toxic gas handling in CalRig. AirStreet's README already states that NO2 is calibrated by field collocation; its pitch line still says "calibrated on CalRig" and is AirStreet's to change. AirStreet is not edited from this repo. | Decided by Amish, 2026-09-25: go with recommendation. |
| A6 | Door condensation | Insulated removable door panel for hot, humid points (and for cold points). | Decided by Amish, 2026-09-25: go with recommendation. |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Collocation partner for the transfer SPS30 (regulatory monitoring station, university site or an AQ-SPEC style program). No recommendation was made. | Proposed, awaiting Amish |

The pitch and problem lines in `project.yaml` were not flagged for rewording in the review and are unchanged.

## Consequences

- CLR-REQ-001 v0.3: R1 redefined to 10 to 40 °C in rooms of 15 to 25 °C, with the lowest reachable set point stated in each record for rooms up to 30 °C (A3). R12 keeps the $300 target from `project.yaml` and notes the proposed $400.
- CLR-PRC-001 v0.3: the key design choices above are no longer shown as "proposed"; they are adopted for TRL 3 work, open for review. The door panel becomes part of the jacket (A6).
- CLR-PRB-001 v0.3: the constraint and out-of-scope lines reflect A1 and A5.
- CLR-CAL-001 v0.1 checks every requirement against the adopted design. It found that R2 (20 °C at 85 % RH in the reference room), R8 (O1 still open), R12 (cost) and R13 (mass) are not met. The design changes it made (full jacket, 120 mm mixing fan, sleeved bubbler with a trace-heated line, 600 x 500 mm base) are engineering changes within the adopted concept. The larger inner sink and the other TRL 3 review items were decided on 2026-09-25 and are recorded in CLR-DDR-002, which also brings R2 and R13 to met.
