---
doc_id: CLR-REQ-001
title: CalRig requirements
project: CalRig
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with first-order status
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: R1 redefined per CLR-DDR-001 A3; status column replaced by the CLR-CAL-001 results; budget note per A1
---

# CalRig requirements

These requirements have been checked by calculation in CLR-CAL-001 v0.1. Targets are still proposals, not yet validated with users. R1 was redefined in this version under CLR-DDR-001 (item A3, adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review). Test conditions follow the enhanced lab conditions in the US EPA sensor testing reports (20 °C and 40 °C; 40 % and 85 % RH) so that CalRig results can be read against a known method ([EPA FAQ](https://www.epa.gov/air-sensor-toolbox/frequently-asked-questions-reports-air-sensor-performance-testing-protocols)).

The **reference room** is an indoor lab at 22 °C and 50 % RH unless a requirement states otherwise.

Table 1. Requirements with targets and status from CLR-CAL-001 (Table 4 there gives the values and script tags).

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (CLR-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Chamber temperature range | 10 to 40 °C at the sensor tray in a room at 15 to 25 °C; in rooms from 25 to 30 °C, the lowest reachable set point is stated in each calibration record | Heat balance with a thermoelectric model; later chamber log | Met: 8.9 °C reachable in a 25 °C room; 13.3 °C lowest in a 30 °C room |
| R2 | Chamber humidity range | 20 to 85 % RH at any temperature from 20 to 40 °C | Moisture balance; later chamber log | **Not met** at 20 °C and 85 % RH in rooms above about 19 °C: the inner Peltier sink condenses faster than the bubbler supplies water. Other corners reached in 26 min or less |
| R3 | Stability at a set point | ±0.3 °C and ±2 % RH over a 30 min hold | Controller simulation; later log | Met on an idealized model: ±0.02 °C, ±1.0 % RH |
| R4 | Uniformity across the six bays | ±0.3 °C and ±2 % RH between bays | Airflow estimate; later traverse with two references | At risk: ±0.18 °C at the EPA points with the 120 mm fan, ±0.42 °C at 10 °C; ±0.8 % RH |
| R5 | Reference temperature uncertainty | 0.2 °C or better (expanded, k = 2) from 10 to 40 °C | Uncertainty budget; ice-point check | At risk: 0.14 °C with the typical sensor tolerance, 0.24 °C if it is 0.2 °C; no calibration certificate |
| R6 | Reference humidity uncertainty | 2 % RH or better (expanded) from 20 to 85 % RH, checked at four salt fixed points | Uncertainty budget; salt fixed-point checks ([Greenspan, 1977](https://nvlpubs.nist.gov/nistpubs/jres/81A/jresv81An1p89_A1b.pdf)) | At risk: 2.0 % RH, no margin |
| R7 | Particle test range | Zero below 2 µg/m³ PM2.5; controlled decay from 300 to 5 µg/m³ in 45 min or less | Decay calculation; later run | Met: 5 min clean-down; 28 min decay |
| R8 | Particle reference traceability | Transfer PM sensor collocated with a regulatory or research monitor for 30 days or more, and meeting EPA PM2.5 targets there, before use as the chamber reference | Collocation record | **Not met by the rig alone.** The collocation site is still open (CLR-DDR-001 O1) |
| R9 | CO2 check | Zero check below 50 ppm with soda lime; span 400 to 2000 ppm against a reference of ±(30 ppm + 3 %) | Calculation and datasheet ([Sensirion SCD30](https://sensirion.com/products/catalog/SCD30)); later run | Met: 8 ppm floor; about 1,100 ppm added per liter of breath |
| R10 | Capacity | Six sensor heads per run, each up to 90 x 70 x 50 mm, with power and I2C, UART or USB leads through a sealed gland | Model check | Met: six bays, 244 mm clear above the tray |
| R11 | Throughput | Four-point temperature and humidity sweep plus one particle decay run in 8 h or less, unattended | Timing estimate; later log | Met: about 5.6 h |
| R12 | Cost | $300 or less in parts (`budget_usd`; a rise to $400 is proposed, awaiting Amish) | Priced BOM (`bom/bom.csv`) | **Not met:** $404, over both $300 and the proposed $400 |
| R13 | Size and mass | Fits a 600 x 500 mm bench area, 400 mm high or less; 12 kg or less | Model; mass estimate | **Not met** on mass: 600 x 500 x 374 mm fits; about 13.4 kg |
| R14 | Records | Every run writes CSV (time, set points, references, each sensor) and a per-sensor report with fitted slope, offset and humidity term, EPA metrics and the reference check dates | Software review | Not verifiable at TRL 3 (software not written) |
| R15 | Electrical safety | No mains wiring in the rig; certified external 12 V supply; fused 12 V bus; peak draw 100 W or less | Design review; power budget | Met: about 89 W, 7.4 A peak |
| R16 | Thermal safety | Independent hardware cut-off opens the heater circuit at 50 °C air temperature or 70 °C Peltier hot side | Design review; heat balance | Met: outer sink 50 °C at most in normal use |
| R17 | Aerosol and gas safety | No toxic gases; test smoke vented through the HEPA loop before the door opens; smoke source outside the chamber | Design review | Met by design |
| R18 | Garage-buildable | Built with a saw or laser cutter, a drill and a soldering iron; all active parts off the shelf | Design review | Met by design |

## Requirements not met or at risk

- **R2**, humidity at 20 °C and 85 % RH. The inner Peltier sink runs about 1.2 K below the dew point in the reference room (CLR-CAL-001, section C). A larger inner sink is proposed in `docs/REVIEW.md`.
- **R8**, particle traceability. The chamber cannot make a mass reference; it transfers one from a collocation site that is still to be chosen.
- **R12**, cost. $404 against $300; the proposed $400 is also exceeded.
- **R13**, mass. About 13.4 kg against 12 kg; the footprint and height now fit.
- **R4**, **R5** and **R6** are at risk (uniformity at cold points, sensor tolerance and humidity budget without margin).

## Assumptions

- Chamber conductance about 0.82 W/K with the full jacket and door panel fitted, and 6.7 W of internal gains (CLR-CAL-001).
- Settling is limited by the 3 L/min conditioning flow, moisture held on the walls and a 15 min equilibration allowance for the heads.
- Test aerosol is incense smoke (CLR-DDR-001 A4); results for other aerosols (dust, sea salt) will differ and must be stated in each report.
