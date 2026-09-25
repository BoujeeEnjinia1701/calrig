---
doc_id: CLR-REQ-001
title: CalRig requirements
project: CalRig
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with first-order status
---

# CalRig requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3. Test conditions follow the enhanced lab conditions in the US EPA sensor testing reports (20 °C and 40 °C; 40 % and 85 % RH) so that CalRig results can be read against a known method ([EPA FAQ](https://www.epa.gov/air-sensor-toolbox/frequently-asked-questions-reports-air-sensor-performance-testing-protocols)).

The **reference room** is an indoor lab at 22 °C and 50 % RH unless a requirement states otherwise.

Table 1. Requirements with targets and first-order status (status values are estimates from CLR-PRC-001).

| ID | Requirement | Target | Verification (TRL 3 or later) | First-order status |
| --- | --- | --- | --- | --- |
| R1 | Chamber temperature range | 10 to 40 °C at the sensor tray, in a room at 15 to 30 °C | Heat balance calculation; later chamber log | **Not met** at the low end in a 30 °C room: about 15 °C reachable (estimate). Met in a room at 25 °C or below |
| R2 | Chamber humidity range | 20 to 85 % RH at any temperature from 20 to 40 °C | Moisture balance; later chamber log | Met by estimate; 20 % RH at 20 °C depends on dryer condition |
| R3 | Stability at a set point | ±0.3 °C and ±2 % RH over a 30 min hold | Controller simulation; later log | Open until TRL 3 control model |
| R4 | Uniformity across the six bays | ±0.3 °C and ±2 % RH between bays | Airflow check; later traverse with two references | Open; depends on mixing fan layout |
| R5 | Reference temperature uncertainty | 0.2 °C or better (expanded, k = 2) from 10 to 40 °C | Uncertainty budget; ice-point check | At risk: SHT45 datasheet is ±0.1 °C typical; no calibration certificate at this budget |
| R6 | Reference humidity uncertainty | 2 % RH or better (expanded) from 20 to 85 % RH, checked at four salt fixed points | Uncertainty budget; salt fixed-point checks ([Greenspan, 1977](https://nvlpubs.nist.gov/nistpubs/jres/81A/jresv81An1p89_A1b.pdf)) | Met by estimate if the salt checks pass |
| R7 | Particle test range | Zero below 2 µg/m³ PM2.5; controlled decay from 300 to 5 µg/m³ in 45 min or less | Decay calculation; later run | Met by estimate (about 30 min decay) |
| R8 | Particle reference traceability | Transfer PM sensor collocated with a regulatory or research monitor for 30 days or more, and meeting EPA PM2.5 targets there, before use as the chamber reference | Collocation record | **Not met by the rig alone.** Needs a collocation site; see CLR-PRC-001 |
| R9 | CO2 check | Zero check below 50 ppm with soda lime; span 400 to 2000 ppm against a reference of ±(30 ppm + 3 %) | Datasheet ([Sensirion SCD30](https://sensirion.com/products/catalog/SCD30)); later run | Met by estimate |
| R10 | Capacity | Six sensor heads per run, each up to 90 x 70 x 50 mm, with power and I2C, UART or USB leads through a sealed gland | Model check | Met in the massing model |
| R11 | Throughput | Four-point temperature and humidity sweep plus one particle decay run in 8 h or less, unattended | Timing estimate; later log | Met by estimate (about 6 h) |
| R12 | Cost | $300 or less in parts | Priced BOM (`bom/bom.csv`) | **Not met:** about $396 (indicative). Budget change proposed, awaiting Amish |
| R13 | Size and mass | Fits a 600 x 500 mm bench area, 400 mm high or less; 12 kg or less | Model; mass estimate | **Not met** on length by about 10 mm: about 610 x 470 x 350 mm, about 10 kg (estimate) |
| R14 | Records | Every run writes CSV (time, set points, references, each sensor) and a per-sensor report with fitted slope, offset and humidity term, EPA metrics and the reference check dates | Software review | Open (software not written at TRL 2) |
| R15 | Electrical safety | No mains wiring in the rig; certified external 12 V supply; fused 12 V bus; peak draw 100 W or less | Design review | Met in concept: about 70 W peak (estimate) |
| R16 | Thermal safety | Independent hardware cut-off opens the heater circuit at 50 °C air temperature or 70 °C Peltier hot side | Design review | Met in concept |
| R17 | Aerosol and gas safety | No toxic gases; test smoke vented through the HEPA loop before the door opens; smoke source outside the chamber | Design review | Met in concept |
| R18 | Garage-buildable | Built with a saw or laser cutter, a drill and a soldering iron; all active parts off the shelf | Design review | Met in concept |

## Requirements not met or at risk

- **R1**, cooling to 10 °C in a warm room. A single 60 W Peltier assembly cannot hold 20 K below a 30 °C room with the estimated heat leak (CLR-PRC-001, Table 3). Options are listed in CLR-PRC-001.
- **R5**, reference temperature uncertainty. Without a calibration certificate the claim rests on the datasheet and an ice-point check.
- **R8**, particle traceability. The chamber cannot make a mass reference; it transfers one from a collocation site.
- **R12**, cost. The estimate is about $396 against a $300 budget.
- **R13**, footprint, by about 10 mm on length; the base plate can be trimmed at TRL 3.

## Assumptions

- Chamber heat loss about 1.0 W/K with the insulation jacket fitted (CLR-PRC-001).
- Settling is limited by the mixing air flow (about 3 L/min through the conditioners) and by moisture held on the walls and sensors.
- Test aerosol is combustion smoke; results for other aerosols (dust, sea salt) will differ and must be stated in each report.
