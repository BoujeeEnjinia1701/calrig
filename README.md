# CalRig

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Open Engineering · **TRL:** 3 of 9 (analytical proof of concept) · **Prototype budget:** about $300 USD · **Difficulty:** 3 of 5

A calibration rig for low-cost sensors: a sealed chamber with controlled temperature, humidity and particle levels plus reference instruments, so every lab sensor can be checked against a known value before and after deployment.

![CalRig concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement CLR-DWG-001 (PDF)](cad/drawings/CLR-DWG-001.pdf) · [Calculations CLR-CAL-001](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Calibration is what turns a cheap sensor into a measurement. Most of the error in a low-cost particle, humidity or CO2 sensor comes from temperature, humidity and drift, and those can be set and checked in a small sealed box. CalRig does the chamber half of the recognized method (known conditions, reference instruments, a dated record) and carries a field-collocated reference sensor back to the bench for the particle half, so one shared rig raises the credibility of every sensing project in the lab.

It is open and garage-buildable because the people who most need calibration, community networks and labs in places without regulatory monitors, cannot buy a commercial environmental chamber. Sheet acrylic, a Peltier module, two aquarium-class pumps, silica gel, laboratory salts for humidity fixed points and a microcontroller are available almost everywhere, and an open method lets others check the results.

## Burning platform

Air pollution is a very large health burden, and much of the world measures it with low-cost sensors or not at all. In 2019, 99 % of the world's population lived where WHO air quality guideline levels were not met, and ambient air pollution caused an estimated 4.2 million premature deaths, about 89 % of them in low- and middle-income countries ([WHO fact sheet](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)). In 2020 OpenAQ found evidence that only 49 % of national governments produced any air quality data ([OpenAQ, 2020](https://documents.openaq.org/reports/Open+Air+Quality+Data+Global+State+of+Play+2020.pdf)).

Low-cost sensors fill that gap only if they are corrected. Raw PurpleAir particle sensors overestimated PM2.5 by about 40 % across most of the United States until a humidity-aware correction cut the error from 8 to 3 µg/m³ ([Barkjohn et al., 2021](https://amt.copernicus.org/articles/14/4617/2021/)), and the UK Air Quality Expert Group warns that without ongoing calibration their useful life "will always be limited" ([DEFRA AQEG](https://uk-air.defra.gov.uk/research/aqeg/pollution-sensors/how-could-I-use.php)).

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Municipal air quality programs | Screen and recheck community PM2.5 sensors before and after each season |
| Universities and schools | Teaching lab for measurement uncertainty; local characterization of sensors for research networks |
| Building services and HVAC | Check CO2 and humidity sensors that drive ventilation control |
| Occupational health | Check the humidity response of wearable particle monitors before field use |
| Agriculture and cold chain | Check temperature and humidity loggers used in grain stores and cold rooms |
| Open hardware and citizen science | Publish a calibration record with every open sensor design |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| United States | The EPA publishes PM2.5 sensor performance targets and enhanced chamber test conditions ([EPA](https://www.epa.gov/air-sensor-toolbox/frequently-asked-questions-reports-air-sensor-performance-testing-protocols)); CalRig lets community groups report against them without a commercial chamber |
| United Kingdom and European Union | DEFRA's expert group calls for ongoing calibration of sensors ([DEFRA AQEG](https://uk-air.defra.gov.uk/research/aqeg/pollution-sensors/how-could-I-use.php)), and CEN/TS 17660-1 tests sensor systems across temperature and humidity ([CEN/TS 17660-1:2021](https://standards.iteh.ai/catalog/standards/cen/5bdb236e-95a3-4b5b-ba7f-62ab08cd21f8/cen-ts-17660-1-2021)) |
| Uganda and Kenya | Listed by OpenAQ in 2020 among populous countries with no national government air quality monitoring program ([OpenAQ, 2020](https://documents.openaq.org/reports/Open+Air+Quality+Data+Global+State+of+Play+2020.pdf)); local groups already calibrate low-cost sensor networks ([Uganda study](https://www.sciencedirect.com/science/article/pii/S1309104225001825)) |
| Nigeria and West Africa | Nigeria, with about 206 million people, was also on OpenAQ's 2020 list of countries without a national monitoring program ([OpenAQ, 2020](https://documents.openaq.org/reports/Open+Air+Quality+Data+Global+State+of+Play+2020.pdf)); low-cost networks there need local checks in heat and high humidity |
| South and Southeast Asia | WHO reports the greatest burden of ambient air pollution deaths in its South-East Asia and Western Pacific regions ([WHO](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)); dense sensor networks in humid climates depend on humidity correction |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. Every smart city concept in this batch depends on sensors that must be trusted. The practical trigger is the humidity bias documented in widely used particle sensors ([Barkjohn et al., 2021](https://amt.copernicus.org/articles/14/4617/2021/)): a network that is not checked in humid air can overstate pollution by tens of percent.

## Problem

Low-cost sensors drift and disagree, and without calibration their data is not trusted by cities, regulators or researchers. Full problem statement: [docs/01-problem.md](docs/01-problem.md).

## Concept

A bench-top, 36 L insulated acrylic chamber sets known temperature (10 to 40 °C in rooms up to 25 °C), humidity (20 to 85 % RH) and particle levels (clean air, then a controlled smoke decay from about 300 µg/m³) around up to six sensors. Reference sensors, checked against salt humidity fixed points, an ice point and a 30-day field collocation for the particle reference, give the known values. A controller steps through set points and a laptop script writes a calibration record for each sensor, reported against the US EPA PM2.5 sensor targets.

Calculated performance (TRL 3, [CLR-CAL-001](docs/04-calcs/01-sizing.md)): a four-point sweep plus a particle run takes about 5.6 h unattended; about 89 W peak from an external 12 V supply; 600 x 500 x 374 mm and about 13.4 kg. Ten of eighteen requirements are met on paper. Not met: the $300 budget (about $404 in parts; a rise to $400 is proposed, awaiting Amish), the 12 kg mass limit, holding 85 % RH at 20 °C in a room warmer than about 19 °C (the Peltier sink condenses water), and particle traceability without a collocation site. NO2 is calibrated by field collocation, not on CalRig.

Full design precis: [docs/02-concept.md](docs/02-concept.md). Requirements: [docs/03-requirements.md](docs/03-requirements.md).

## Key components

1. Sealed 6 mm acrylic chamber (36 L) with front door and removable insulation jacket
2. 60 W Peltier heat pump and internal mixing fan
3. Heated bubbler (wet air) and silica gel dryer (dry air), mixed by two pumps
4. HEPA scrubber loop and aerosol injection port for zero air and smoke decay
5. Reference cluster: two Sensirion SHT45, a Sensirion SCD30 (CO2) and a collocated Sensirion SPS30 (PM)
6. Six-bay sensor tray, controller with independent thermal cut-off, certified external 12 V supply
7. Saturated salt fixed-point jars for checking the humidity references

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> **Safety:** No mains wiring inside the rig; use only a certified external 12 V supply. The Peltier hot side reaches 60 to 70 °C and is guarded, with an independent thermal cut-off. Test smoke contains fine particles and some carbon monoxide: light it outside the chamber in a ventilated room and clear the chamber through the HEPA loop before opening. Soda lime is corrosive and lithium chloride is harmful if swallowed; wear gloves and eye protection. No toxic calibration gases are used.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (CLR-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `CLR-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Gap-filling areas set.
