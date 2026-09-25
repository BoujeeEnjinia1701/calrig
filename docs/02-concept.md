---
doc_id: CLR-PRC-001
title: CalRig design precis
project: CalRig
doc_type: Design precis
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
  change: Populate to TRL 2 (how it works, components, first-order numbers, safety, open questions)
---

# CalRig design precis

## Summary

CalRig is a 36 L insulated acrylic chamber on a bench-top base. A Peltier heat pump sets the temperature, a heated bubbler and a silica gel dryer set the humidity, a HEPA loop gives clean air and a controlled smoke decay for particle tests, and a reference cluster (two Sensirion SHT45 temperature and humidity sensors, a Sensirion SCD30 CO2 sensor and a collocated Sensirion SPS30 particle sensor) sits among six sensors under test. A small controller steps through set points and logs everything; a laptop script fits a correction for each sensor and writes a dated record. First-order estimates suggest it meets most targets in CLR-REQ-001, but it misses the $300 budget (about $396), cannot cool to 10 °C in a 30 °C room, and depends on a collocation site for its particle reference.

![Figure 1. CalRig massing model on a lab bench with a 1.75 m person for scale.](../media/hero.png)

Figure 1. CalRig massing model on a lab bench, with a 1.75 m person for scale. Concept, not for fabrication.

## How it works

1. **Load.** Up to six sensor heads sit in the bays of a tray inside the chamber. Their leads pass through a sealed gland to a USB and I2C hub. The door is closed and latched.
2. **Check the references.** Before a campaign (monthly is proposed), the two SHT45 references are checked at four saturated salt fixed points (11, 33, 75 and 84 % RH at 25 °C; [Greenspan, 1977](https://nvlpubs.nist.gov/nistpubs/jres/81A/jresv81An1p89_A1b.pdf)) and in an ice bath at 0 °C. The SPS30 transfer sensor is collocated at a regulatory or research monitor for 30 days or more, and replaced in the chamber only if it meets the US EPA PM2.5 targets there.
3. **Temperature and humidity sweep.** The controller steps through set points, by default 20 °C and 40 °C at 40 % and 85 % RH, matching the EPA enhanced test conditions ([EPA FAQ](https://www.epa.gov/air-sensor-toolbox/frequently-asked-questions-reports-air-sensor-performance-testing-protocols)). The Peltier assembly heats or cools. Two small pumps push air through the bubbler (wet) and the dryer (dry) at a ratio set by PWM, with about 3 L/min in total. The internal fan mixes the chamber. Each point settles for about 45 min and is held for 30 min.
4. **Particle run.** With the HEPA loop at full speed the chamber is cleaned to below 2 µg/m³. A syringe draws a puff of smoke from an incense stick smoldering in a cup outside the chamber and injects it through the aerosol port. The HEPA loop then runs slowly and the concentration decays from about 300 to 5 µg/m³, giving a continuous comparison curve. The run can be repeated at a second humidity to fit the humidity term.
5. **CO2 check (optional).** Soda lime in the dryer path gives a near-zero point. One liter of exhaled breath from a bag raises the chamber by about 1,100 ppm for a span point.
6. **Fit and record.** The laptop script compares each sensor with the references, fits a slope, offset and humidity term, computes the EPA metrics (R², slope, intercept, RMSE, sensor-to-sensor precision) and writes a CSV and a one-page report per sensor serial number.

![Figure 2. Cutaway: sensor tray, reference cluster, mixing fan and Peltier assembly.](../media/cutaway.png)

Figure 2. Cutaway looking from the door side: sensor tray with six example sensors, reference cluster on its mast, mixing fan and the Peltier assembly through the right-hand wall.

## Main components

Table 1. Main components, numbered to match the BOM and the exploded view (Figure 3).

| No. | Component | Role | Key choice |
| --- | --- | --- | --- |
| 1 | Chamber shell | 36 L sealed volume (400 x 300 x 300 mm inside) | 6 mm cast acrylic, solvent-welded; small enough to condition fast, large enough for six heads |
| 2 | Front door | Access and viewing | Clear acrylic with silicone gasket and two latches |
| 3 | Insulation jacket | Cuts heat leak to about 1.0 W/K | Removable 25 mm XPS panels; an extra door panel for hot, humid points |
| 4 | Base plate | Carries the chamber and conditioners | 12 mm plywood or HDPE |
| 5 | Peltier heat pump | Heats and cools the chamber | 60 W air-to-air thermoelectric assembly with fins and fans on both sides |
| 6 | Internal mixing fan | Uniform air across the bays | 80 mm, 12 V, speed-controlled |
| 7 | Sensor tray | Holds six sensor heads, cable rail | Perforated sheet so air moves around the heads |
| 8 | Reference cluster | The known values | 2 x SHT45 (±0.1 °C, ±1.0 % RH typical, [Sensirion](https://sensirion.com/products/catalog/SHT45)), SCD30 (±(30 ppm + 3 %), [Sensirion](https://sensirion.com/products/catalog/SCD30)), SPS30 collocated transfer sensor (±10 % precision, [Sensirion](https://sensirion.com/products/catalog/SPS30)) |
| 9 | Humidifier bubbler | Wet air | Distilled water with a 10 W heater pad, held about 3 K above chamber air; no ultrasonic mist, which would add particles |
| 10 | Dryer column | Dry air | Indicating silica gel, about 500 g, regenerated in an oven |
| 11 | HEPA scrubber loop | Zero air and controlled smoke decay | H13 class filter cartridge with a variable-speed fan |
| 12 | Aerosol injection port | Smoke entry | Luer port with a ball valve; the smoke source stays outside |
| 13 | Controller and power board | Control, logging and protection | ESP32 class board, Peltier H-bridge, pump and fan MOSFETs, microSD, independent thermal cut-off |
| 14 | Power supply | 12 V, 10 A | Certified external brick; no mains wiring in the rig |
| 15 | Salt fixed-point jars | Humidity reference checks | LiCl, MgCl2, NaCl and KCl slurries in sealed jars |

![Figure 3. Exploded view with BOM numbers.](../media/exploded.png)

Figure 3. Exploded view. Callout numbers match Table 1 and `bom/bom.csv`.

## First-order numbers

All values are estimates for review at TRL 3.

Table 2. Chamber and process estimates.

| Quantity | Estimate | Assumption |
| --- | --- | --- |
| Internal volume | 36 L | 400 x 300 x 300 mm |
| Heat leak, jacket fitted | about 1.0 W/K | Jacketed walls 0.54 m² at U about 1.0 W/(m²·K); clear door 0.12 m² at U about 3.9 W/(m²·K); inside and outside film coefficients 10 and 8 W/(m²·K) |
| Internal heat gains | about 4 W | Mixing fan 1.5 W, references and six sensors about 2.5 W |
| Water to go from 20 to 85 % RH at 40 °C | about 1.2 g | Saturation vapor density 51.1 g/m³ at 40 °C |
| Settling per set point | about 45 min | 3 L/min conditioning flow (air change about 12 min), plus moisture held on walls and sensors |
| Four-point sweep plus particle run | about 6 h | 4 x (45 min settle + 30 min hold) + about 45 min particle run |
| Smoke mass for 300 µg/m³ | about 11 µg | 300 µg/m³ x 0.036 m³; one small syringe puff |
| Decay 300 to 5 µg/m³ | about 30 min | HEPA loop at 5 L/min gives a 7.2 min time constant; ln(60) = 4.1 time constants; wall deposition ignored |
| CO2 span from 1 L of breath | about +1,100 ppm | Exhaled air about 4 % CO2 (estimate) diluted into 36 L |
| Peak electrical power | about 70 W | Peltier 60 W, fans 4 W, pumps 4 W, controller 2 W |
| Overall size and mass | about 610 x 470 x 350 mm, about 10 kg | Massing model; acrylic 1,190 kg/m³ |

Table 3. Heat balance at the temperature limits (estimates).

| Case | Heat to move | Peltier coefficient of performance | Electrical input | Result |
| --- | --- | --- | --- | --- |
| Heat to 40 °C, room 22 °C | 18 W loss less 4 W gains = 14 W | above 1 in heating | about 10 W | Met |
| Cool to 10 °C, room 25 °C | 15 W leak + 4 W gains = 19 W | about 0.35 (about 30 K across the module) | about 55 W | Met, near the module limit |
| Cool to 10 °C, room 30 °C | 20 W leak + 4 W gains = 24 W | about 0.25 (about 35 K across) | about 95 W | **Not met**; about 15 °C is the lowest set point |

**Condensation at the hot, humid point.** At 40 °C and 85 % RH the dew point is about 37 °C. The inner face of the clear door in a 22 °C room is estimated at about 33 °C, so water will condense on it. With the door insulation panel fitted the inner face rises to about 38 °C, just above the dew point. The door panel is therefore required for that point, and the humidifier line must be kept warm or short. This is a design risk to check at TRL 3.

**Particle reference.** The chamber cannot create a traceable mass reference. It carries one from the field: a transfer SPS30 that has been collocated with a regulatory or research monitor. Chamber results then describe how each sensor compares with that transfer sensor in combustion smoke at known humidity. Reports must state the aerosol type, because optical sensors respond differently to dust, salt and smoke.

## Key design choices

All are proposed, awaiting Amish.

- **Transfer references instead of certified instruments.** Certified reference instruments cost thousands of dollars. CalRig uses good digital sensors, checked against physical fixed points (salts, ice) and field collocation. This keeps the rig near its budget and makes the uncertainty chain explicit.
- **Heated bubbler, not an ultrasonic mister.** Ultrasonic misters make mineral particles that would corrupt particle tests.
- **Smoke decay, not a nebulizer.** A decay curve covers the whole range in one run with no dilution hardware.
- **External 12 V supply.** Keeps mains voltage out of a box that holds water.
- **Temperature and humidity first, CO2 optional, no toxic gases.** NO2 for AirStreet would need a certified gas cylinder, a dilution system and toxic gas handling (see open questions).

## Links to other projects

- **AirStreet** describes itself as "calibrated on CalRig" for PM2.5 and NO2. CalRig covers PM2.5 and the temperature and humidity terms, but not NO2 in this version.
- **HeatMap Node** (heat and humidity), **DustBadge** (dust) and **FieldNode** sensor heads are intended users. DustBadge measures respirable dust, so a smoke-based chamber result will not transfer directly to mineral dust.

## Safety

> **Safety:** The Peltier hot-side heat sink can reach 60 to 70 °C; keep it guarded and away from the acrylic. An independent thermal cut-off opens the heater circuit at 50 °C chamber air or 70 °C hot side. The 12 V bus carries up to about 6 A: fuse it at the supply and use rated wire. Use only a certified external supply; never wire mains into the rig, which contains water.

> **Safety:** Test smoke contains fine particles and combustion gases, including carbon monoxide in small amounts. Light the incense in a cup outside the chamber, in a ventilated room, and run the HEPA loop until the reference reads below 5 µg/m³ before opening the door. No toxic calibration gases are used in this version.

> **Safety:** Soda lime is corrosive and lithium chloride is harmful if swallowed. Wear gloves and eye protection when filling cartridges and salt jars, label them, and keep them away from children. Cast acrylic is combustible: keep heaters and hot surfaces off the shell. Keep electronics below and outside the chamber so condensation cannot reach them. Fans have guards. Exhaled air for CO2 checks goes through a single-user bag and filter.

## Open questions

- [ ] Budget: raise to $400, or drop CO2 and soda lime for a core version at about $329 (both awaiting Amish).
- [ ] Cooling limit: accept 10 °C only in rooms at 25 °C or below, add a second Peltier module, or add an ice-water exchanger for cold runs.
- [ ] Particle reference: which collocation site (regulatory monitor, university, AQ-SPEC style program) will host the transfer SPS30, and how often it returns there.
- [ ] NO2 and other gases for AirStreet: separate add-on with certified gas and dilution, a partner lab, or field collocation only.
- [ ] Door condensation at 40 °C and 85 % RH: insulated door panel (proposed), double-glazed door, or a heated film.
- [ ] Report format: what a city or funder would accept as evidence.
