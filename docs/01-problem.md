---
doc_id: CLR-PRB-001
title: CalRig problem statement
project: CalRig
doc_type: Problem statement
version: "0.4"
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
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Budget and gas scope lines updated for CLR-DDR-001 (A1, A5)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# CalRig problem statement

Low-cost sensors drift and disagree, and without calibration their data is not trusted by cities, regulators or researchers. Community groups, schools and small labs can buy a particle, humidity or CO2 sensor for tens of dollars, but they have no affordable way to check it against a known value before deployment, after a season in the field or after a repair. CalRig is a bench-top chamber that sets known temperature, humidity and particle conditions around a batch of sensors and compares them with reference instruments, so each sensor leaves with a dated calibration record.

## The problem

Low-cost sensors are now the main source of local air and climate data in many places, but their raw readings are biased in ways that depend on the environment:

- **Humidity bias in particle sensors.** Optical particle sensors count water-swollen particles as dry mass. A US-wide study of 53 PurpleAir sensors at 39 sites found that raw readings overestimated PM2.5 by about 40 % in most of the country, and that a correction with a humidity term cut the root mean square error from 8 to 3 µg/m³ ([Barkjohn et al., 2021](https://amt.copernicus.org/articles/14/4617/2021/)).
- **Temperature and humidity dependence of gas sensors.** Electrochemical and metal-oxide gas sensors respond to temperature and humidity as well as to the target gas, which is why the European sensor evaluation specification tests sensor systems across both ([CEN/TS 17660-1:2021](https://standards.iteh.ai/catalog/standards/cen/5bdb236e-95a3-4b5b-ba7f-62ab08cd21f8/cen-ts-17660-1-2021)).
- **Drift over time.** The UK Air Quality Expert Group warns that "without any ongoing quality control and calibration of these devices in the field their lifespan for producing useful data will always be limited" ([DEFRA AQEG](https://uk-air.defra.gov.uk/research/aqeg/pollution-sensors/how-could-I-use.php)).

The recognized fixes are collocation beside a regulatory monitor for weeks, and chamber tests at set temperature and humidity. The US EPA's performance targets for PM2.5 sensors ask for at least 30 days of field collocation with at least three identical sensors, plus enhanced lab tests at 20 °C and 40 °C and at 40 % and 85 % RH ([EPA FAQ on sensor testing reports](https://www.epa.gov/air-sensor-toolbox/frequently-asked-questions-reports-air-sensor-performance-testing-protocols)). Programs with a full chamber, such as South Coast AQMD's [AQ-SPEC](https://www.aqmd.gov/aq-spec), are few and expensive. Where regulatory monitors are absent, collocation is not possible at all: in 2020, OpenAQ found evidence that only 49 % of national governments produced any air quality data ([OpenAQ, 2020](https://documents.openaq.org/reports/Open+Air+Quality+Data+Global+State+of+Play+2020.pdf)).

A small group therefore either trusts factory calibration, which the studies above show is not enough, or does nothing. CalRig aims to make the chamber half of the process cheap, open and repeatable, and to make collocation more efficient by carrying a collocated "transfer" sensor back to the bench.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Lab and project builders (Design Molecule projects such as AirStreet, HeatMap Node and DustBadge) | Check every sensor before and after deployment and after repairs | Bench space, 12 V supply, batches of 1 to 6 sensor heads |
| Community air quality groups | Show that their network data is credible to a city or a newspaper | Volunteer-run, small budgets, sensors from mixed makers |
| Universities and schools in low-monitoring countries | Characterize sensors locally where no regulatory monitor exists nearby | Teaching labs, local suppliers, hot and humid climates |
| Municipal environment teams | Screen low-cost sensors before a procurement or a pilot | Small technical staff, need a documented method |
| Building and HVAC technicians | Check CO2 and humidity sensors used for ventilation control | Service vans and workshops |

### Operating environment

- **Room:** indoor lab or workshop at 15 to 30 °C, 20 to 80 % RH, on a bench about 0.9 m high.
- **Power:** a certified external 12 V supply from a normal socket; no mains wiring inside the rig.
- **Consumables:** distilled water, indicating silica gel, analytical-grade salts for fixed points, incense or a candle for test aerosol, soda lime for CO2 zero.
- **Operator:** one person with basic electronics skills; runs are unattended once started.

## Constraints

- Garage-buildable prototype, $400 USD in parts (`budget_usd`, raised from $300; decided by Amish on 2026-09-25, CLR-DDR-002). CLR-CAL-001 v0.2 prices the design at about $412 (REQ-001 R12, not met).
- Built from sheet acrylic, off-the-shelf thermoelectric, pump and sensor modules, and a small microcontroller; no machining beyond cutting and drilling.
- Uses only low-hazard test atmospheres: water vapor, room air, combustion smoke in small amounts, exhaled CO2. No toxic calibration gases in the first version.
- Open data: every run writes plain CSV and a readable report; software under MIT.
- Results must be described plainly: CalRig gives a characterized, documented comparison against transfer references. It does not by itself make a sensor a regulatory or equivalent method.

## Out of scope

- Regulatory certification or equivalence testing of sensors.
- Toxic reference gases (NO2, O3, CO, SO2) and gas dilution systems. NO2 sensors are calibrated by field collocation only (CLR-DDR-001 A5, decided by Amish on 2026-09-25).
- Noise, light, wind and water quality sensors.
- Particle size-resolved reference measurement; CalRig checks mass concentration against a collocated transfer sensor only.
- Field collocation hardware; CalRig relies on existing regulatory or research sites for that step.

## Prior work

- **AQ-SPEC** (South Coast AQMD) runs field and chamber evaluations of commercial sensors and publishes its [laboratory protocol](https://www.aqmd.gov/docs/default-source/aq-spec/protocols/sensors-lab-testing-protocol6087afefc2b66f27bf6fff00004a91a9.pdf). It sets the method CalRig follows in a much simpler form.
- **US EPA performance targets** for PM2.5 sensors set R² ≥ 0.70, slope 1.0 ± 0.35, intercept within ±5 µg/m³, RMSE ≤ 7 µg/m³ and precision SD ≤ 5 µg/m³ ([EPA/600/R-20/280](https://cfpub.epa.gov/si/si_public_record_report.cfm?Lab=CEMM&dirEntryID=350785), values as listed in the [EPA sensor loan program QAPP](https://www.epa.gov/system/files/documents/2024-06/particulate-matter-pm2.5-sensor-loan-program-qapp-aasb-qapp-004-r1.1.pdf)). CalRig reports its results against these metrics.
- **Saturated salt fixed points.** Greenspan's tables give equilibrium relative humidity over saturated salt solutions, for example 75.29 ± 0.12 % RH for sodium chloride at 25 °C ([Greenspan, 1977](https://nvlpubs.nist.gov/nistpubs/jres/81A/jresv81An1p89_A1b.pdf)). These are the cheapest traceable humidity references available.
- **Local calibration in Africa.** AirQo and university partners in Uganda calibrate low-cost PM2.5 sensors against reference instruments for urban and rural sites ([Calibration of low-cost sensor data in South Central Uganda](https://www.sciencedirect.com/science/article/pii/S1309104225001825); [World Economic Forum on AirQo](https://www.weforum.org/stories/2022/06/ugandan-researchers-low-cost-sensors-air-pollution/)). This shows the demand for local calibration capacity.
- **Commercial humidity generators and environmental chambers** exist but cost thousands of dollars and are not open.

## Open questions

- Which sensors do the first users most need to check: PM2.5, temperature and humidity, CO2, or NO2?
- Is there a regulatory or research monitor within reach of the first users for collocating the transfer PM sensor?
- What report format would a city or a funder accept as evidence of sensor quality?
