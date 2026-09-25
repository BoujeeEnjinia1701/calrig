# CalRig

**Area:** Open Engineering · **Status:** Concept · **Prototype budget:** about $300 USD · **Difficulty:** 3 of 5

A calibration rig for low-cost sensors: a sealed chamber with controlled temperature, humidity and particle levels plus reference instruments, so every lab sensor can be checked against a known value before and after deployment.

## Concept rationale

Calibration is what turns a cheap sensor into a measurement; one shared rig raises the credibility of every sensing project in the lab.

## Burning platform

Cities and communities increasingly rely on low-cost sensor networks whose accuracy is rarely checked.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. Every smart city concept in this batch depends on sensors that must be trusted.

## Problem

Low-cost sensors drift and disagree, and without calibration their data is not trusted by cities, regulators or researchers.

## Concept

A calibration rig for low-cost sensors: a sealed chamber with controlled temperature, humidity and particle levels plus reference instruments, so every lab sensor can be checked against a known value before and after deployment.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Sealed acrylic chamber with fan
- Peltier heating and cooling module
- Humidifier and dryer
- Reference temperature, humidity and CO2 sensors
- Aerosol generator port
- Controller and logging software

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Mains wiring must be done or checked by a qualified electrician and follow local electrical code. Handle aerosol test materials in a ventilated space.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Gap-filling areas set.
