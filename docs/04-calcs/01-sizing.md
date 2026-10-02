---
doc_id: CLR-CAL-001
title: CalRig sizing calculations
project: CalRig
doc_type: Calculation
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (geometry and mass, heat balance with a thermoelectric model, moisture and condensation, control stability, bay uniformity, reference uncertainty, particle decay, CO2, throughput, power, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Larger inner Peltier sink (0.20 K/W), budget $400, R13 relaxed to 14 kg; all results re-run
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish; budget $412 covers the priced BOM, so R12 is met (CLR-DDR-002 v0.2)
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Re-run for the constructable design (CLR-DDR-003); 9 mm base, mass 13.8 kg, heat capacity 8.7 kJ/K, BOM $439 on 19 lines, so R12 is not met pending a budget decision
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target; cost wording only, no number changed
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Requirement table wording follows the decisions of 2026-10-02 (R8 candidate site, R10 large item case, R14 report basis); no result changed'
---

# CalRig sizing calculations

On paper, CalRig meets twelve of its eighteen requirements, has three at risk, misses one, is over the value-engineering target on cost and has one that cannot be checked at TRL 3. The miss is R8 (particle traceability needs a collocation site that is still to be named). R12 is over the target: making the design buildable (CLR-DDR-003) added a front frame, bulkhead fittings, cable glands, a drain and printed holders, so the estimated cost of the constructable design is about $439 against the $412 value-engineering target set by Amish on 2026-09-26 (CLR-DDR-002), $27 over the target. The three at risk are R4 (bay uniformity at cold set points), R5 (reference temperature uncertainty, which depends on an uncertified sensor tolerance) and R6 (reference humidity uncertainty, 2.0 % RH against a 2 % RH target). R1 is met against the relaxed target of DDR-001: 6.7 °C is reachable in a 25 °C room and 11.1 °C in a 30 °C room. R2 is now met because the inner Peltier sink was enlarged under DDR-002 (0.45 to 0.20 K/W), which keeps it above the dew point at 20 °C and 85 % RH in rooms up to about 28 °C. R13 is met against the relaxed 14 kg limit of DDR-002 (13.8 kg, with a 9 mm base).

The calculations in v0.1 changed four parts of the TRL 2 concept: the jacket now covers the bottom and the right-hand wall as well; the mixing fan grows from 80 mm to 120 mm; the bubbler jar gets a foam sleeve, a smaller fill and a trace-heated outlet line; and the base plate is trimmed to 600 x 500 mm with the chamber moved so the aerosol valve stays on it. Version 0.2 adds the larger inner fin block (about 45 x 120 x 110 mm) decided by Amish on 2026-09-25. Version 0.4 re-runs every result for the constructable design of CLR-DDR-003; only the mass, heat capacity, ramp times and cost move. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace checks of the thermal cut-offs, the fuse rating or the smoke clearance on a built rig. See CLR-PRC-001, Safety.

## Scope and method

The note checks every requirement in CLR-REQ-001 v0.6 against the design in CLR-PRC-001 v0.6 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS`, derived dimensions and part solids, so the chamber size, jacket, bay layout, footprint and mass are those of the STEP files and drawing CLR-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is the reference room of CLR-REQ-001 (22 °C, 50 % RH) with the R1 room range of 15 to 30 °C, the four US EPA enhanced set points (20 °C and 40 °C at 40 % and 85 % RH), six sensor heads at the largest size in R10 and the insulated door panel fitted.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Films | Inside 10 W/(m²·K) (fan-stirred); outside 8 W/(m²·K) (still room, with radiation) | Typical values |
| Materials | Acrylic k 0.19 W/(m·K), 1,190 kg/m³, 1,470 J/(kg·K); XPS k 0.034 W/(m·K), 35 kg/m³; foam sleeve k 0.035 W/(m·K); plywood 550 kg/m³ | Handbook values |
| Thermal bridges | Edges, gasket, cable gland and fixings add 20 % to the jacketed wall conductance | Allowance |
| Air paths | Conditioning loop 3 L/min, closed from and back to the chamber, returning at room temperature; HEPA loop 20 L/min full, 5 L/min slow, H13 (99.95 %); gasket leak 0.1 air changes per hour | Design values |
| Internal gains | Mixing fan 2.4 W, inner Peltier fan 1.5 W, six heads at 0.4 W, references 0.4 W: 6.7 W [B3] | Typical fan and sensor draw; up from 4 W at TRL 2 |
| Thermoelectric module | One 12706-class module: Vmax 15.2 V, Imax 6.0 A, ΔTmax 66 K at 300 K; derived Seebeck 50.7 mV/K, resistance 1.98 Ω, conductance 0.54 W/K [A0] | Typical datasheet values, to confirm for the chosen assembly |
| Heat sinks | Outer sink with 92 mm fan 0.25 K/W; inner sink with fan 0.20 K/W (larger fin block, DDR-002; 0.45 K/W for the stock inner sink) | Typical air-to-air assembly; the 0.20 K/W figure is a target for the fin block to confirm |
| Supply | 12 V; the module voltage is limited to 12 V | Certified external supply |
| Moisture | Water diffusivity in PMMA 1 x 10⁻¹² m²/s, uptake 2 % by mass at 100 % RH, linear in RH; bubbler air leaves at 90 % saturation; silica gel holds 5 % by mass at low RH and delivers about 5 % RH air | Literature order of magnitude; to confirm |
| Aerosol | Incense smoke, deposition 0.2 per hour in a stirred chamber | Order of magnitude for sub-micron smoke |
| Reference sensors | SHT45 ±0.1 °C and ±1.0 % RH typical ([Sensirion](https://sensirion.com/products/catalog/SHT45)); a 0.2 °C tolerance is also checked because no certificate is bought; hysteresis 0.8 % RH | Datasheet typical values; the maximum figures and hysteresis are assumptions until the full datasheet is read |

## A. Geometry, capacity, size and mass (R10, R13)

The chamber is 400 x 300 x 300 mm inside (36.0 L) in a 412 x 312 x 312 mm acrylic shell [A1]. The tray is 318 x 176 mm with six 90 x 70 mm bays and 244 mm of clear height above it, so six heads at the R10 maximum of 90 x 70 x 50 mm fit, with the reference cluster behind and above them [A2]. R10 is met.

With the chamber moved toward +X and the base trimmed, the whole rig, including the aerosol valve, the Peltier fan, the conditioning column and the salt jars, fits 600 x 500 mm and is 371 mm high [A3]. Adding the bottom jacket panel raised the chamber by 25 mm, which is still within the 400 mm limit. The mass is about 13.8 kg: 5.3 kg of acrylic (shell, front frame, drip tray and door), 1.5 kg of 9 mm plywood base, 0.7 kg of XPS and about 6.4 kg of bought-in and printed parts, including 0.2 kg for the larger inner fin block and 0.3 kg for the fittings, drain and printed holders added under CLR-DDR-003. R13 was relaxed from 12 kg to 14 kg under DDR-002 because CalRig is a bench rig, so R13 is **met**, with 0.17 kg of margin; the base went from 12 to 9 mm plywood to keep that margin.

## B. Heat balance and temperature range (R1, R16)

With every face except the door jacketed, the wall conductance is 1.01 W/(m²·K); the clear door is 3.90 W/(m²·K) and the door with its panel 1.01 W/(m²·K) [B1]. The total chamber conductance with the panel fitted is 0.82 W/K, of which 0.06 W/K is the conditioning loop; with the panel off it is 1.17 W/K [B2]. The TRL 2 estimate of about 1.0 W/K is therefore about right, but internal gains are larger than assumed (6.7 W against 4 W) [B3].

The Peltier module is modeled with its Seebeck, Joule and conduction terms, both sink resistances and the 12 V limit, and solved for the lowest chamber temperature it can hold at full drive.

*Table 2. Lowest chamber temperature at full drive, door panel fitted [B4].*

| Room | Lowest chamber temperature | Module | Outer sink |
| --- | --- | --- | --- |
| 15 °C | -2.0 °C | 5.01 A, 12.0 V, 60 W | 35 °C |
| 22 °C | 4.1 °C | 4.98 A, 12.0 V, 60 W | 42 °C |
| 25 °C | 6.7 °C | 4.97 A, 12.0 V, 60 W | 45 °C |
| 30 °C | 11.1 °C | 4.95 A, 12.0 V, 59 W | 50 °C |

Holding 10 °C in a 25 °C room takes 19.1 W of cooling at 3.20 A, 7.8 V and 25 W, with the inner sink near 6.2 °C [B5]. Heating is easy: 40 °C in a 15 °C room needs 13.9 W at about 8 W electrical, against a heating capacity of about 80 W at 12 V [B6]. The revised R1 (10 to 40 °C in rooms of 15 to 25 °C, with the lowest point stated for warmer rooms) is therefore **met**, with a 3.3 K margin at 25 °C (1.1 K with the stock inner sink). In a 30 °C room the lowest set point is about 11 °C.

The lumped heat capacity is about 8.7 kJ/K, mostly the acrylic, and the passive time constant is 2.9 h [B7]. At full drive the chamber goes from 20 to 40 °C in about 31 min, but from 40 to 20 °C in about 78 min, and reaching 10 °C in a 25 °C room takes about 2.5 h because the margin is small [B8]. Sweeps should run from cold to hot, and 10 °C points are a separate, slower run.

The outer sink stays at or below 50 °C in normal use, 20 K under the 70 °C hot-side cut-off; the inner sink reaches about 43 °C when heating to 40 °C in a 15 °C room, and the 50 °C air cut-off is 10 K above the top set point [J2]. R16 is met.

## C. Moisture, condensation and the conditioners (R2)

Going from 20 to 85 % RH at 40 °C needs 1.19 g of water in the air and about 0.59 g taken up by the acrylic surface in 45 min, 1.8 g in all [C1]. With the loop time constant of 12 min and bubbler air at 43 °C and 90 % saturation, the chamber reaches 85 % RH in about 26 min [C2]. Drying to 20 % RH at 20 °C from room air takes about 22 min [C3]. The 500 g of silica gel holds about 25 g at low RH, enough for about 12 sweeps between regenerations [C4].

The bubbler needs two changes. A bare 500 mL jar at 43 °C loses 7.7 W in a 22 °C room, and evaporation takes another 2.7 W, which is more than the 10 W pad can give; a 10 mm foam sleeve cuts the loss to 2.4 W, and with a 0.3 L fill the pad warms the water in about 50 min, so it is preheated during the 20 °C points [C5]. Air from the bubbler also condenses in a room-temperature line: a foam-lagged 200 mm line would deliver it at about 28 °C, well below its 41 °C dew point, so the line needs a small trace heater, about 1.1 W to hold 45 °C (3 W is allowed in the BOM) [C6].

**Door condensation.** At 40 °C and 85 % RH the dew point is 37.0 °C. In a 22 °C room the clear door face runs at 33.0 °C and condenses; with the door panel it runs at 38.2 °C, a 1.2 K margin. In a 15 °C room the margin falls to 0.5 K [C7]. The door panel (adopted under DDR-001) is required, and the hot, humid point is at risk in cold rooms.

**Peltier sink condensation (R2).** At 20 °C and 85 % RH the dew point is 17.4 °C. Holding 20 °C in a 22 °C room still needs 8.3 W of cooling, mostly to remove the internal gains. With the stock 0.45 K/W inner sink of v0.1 that put the sink at about 16.2 °C, 1.2 K below the dew point: it condensed about 7.7 g/h against about 0.7 g/h from the bubbler and stayed dry only in rooms below about 19 °C, so R2 was not met [C9]. With the larger fin block decided under DDR-002 (0.20 K/W, same fan) the sink runs at about 18.3 °C, 0.9 K above the dew point, and stays dry in rooms up to about 28 °C [C8, C9]. R2 is **met** across the R1 room range of 15 to 25 °C. The 0.9 K margin is small, and the 0.20 K/W figure is a target for the chosen fin block. Cold points below the dew point will still wet the sink, so a drip tray and drain are needed in any case.

## D. Stability at a set point (R3)

A lumped plant with a PI controller, a 20 s transport delay, a 4 s sensor lag, an 8-bit drive and a room swinging ±1 K over 30 min holds the chamber within ±0.02 K [D1]. At 40 °C and 85 % RH that temperature term is worth 0.10 % RH; with an assumed ±1 % RH from the wet and dry mixing control, the humidity stability is about ±1.0 % RH [D2]. R3 is met on this idealized model, which does not include mixing inside the chamber or the sink's own lag; the chamber log planned for TRL 4 is the real check.

## E. Uniformity across the bays (R4)

The bay-to-bay temperature span is estimated as half the chamber load divided by the heat capacity rate of the mixing air, with the fan delivering 40 % of its free-air flow through the tray region. With the 80 mm fan of the TRL 2 concept the span is 0.61 K at 40 °C, 0.62 K at 20 °C and 1.42 K at 10 °C in a 25 °C room; with a 120 mm fan it falls to 0.36, 0.37 and 0.84 K [E1]. The 120 mm fan is therefore adopted in the model and BOM. That gives ±0.18 °C at the EPA set points, within the ±0.3 °C target, but ±0.42 °C at 10 °C. The humidity spread from temperature at 40 °C and 85 % RH is ±0.8 % RH [E2]. R4 is **at risk**: met at the EPA set points on a coarse estimate, not met at the cold end.

## F. Reference uncertainty (R5, R6)

*Table 3. Reference temperature uncertainty budget (standard uncertainties, °C) [F1].*

| Component | Value |
| --- | --- |
| Ice point realization (crushed ice and water) | 0.02 |
| SHT45 tolerance after the ice-point offset, 0 to 40 °C (0.1 °C, rectangular) | 0.058 |
| Drift between monthly checks (0.03 °C, rectangular) | 0.017 |
| Resolution and noise | 0.01 |
| Gradient from the reference mast to a bay (0.05 °C, rectangular) | 0.029 |
| **Expanded, k = 2** | **0.14** |

With the typical 0.1 °C tolerance the expanded uncertainty is 0.14 °C, inside the 0.2 °C target; if the tolerance is 0.2 °C, as a maximum specification would allow, it is 0.24 °C [F1]. R5 is **at risk** until a second fixed point or a certified probe pins down the slope. Under DDR-002 a certified probe is to be added if the cost target allows; the estimated cost is already above the $412 value-engineering target, so the probe is not in the BOM.

For humidity, the components are the salt fixed point itself (0.14 % RH), a 0.2 K gradient in the jar at 85 % RH (0.59), hysteresis (0.46), interpolation between fixed points (0.29) and use away from 25 °C (0.58) [F2]. The expanded uncertainty is 2.0 % RH [F3], at the 2 % RH target with no margin. R6 is **at risk**. The jar gradient and temperature terms dominate, so thermally lagged jars and fixed points taken at the chamber temperature would help most.

## G. Particles (R7, R8)

With the HEPA loop at 20 L/min, the chamber cleans from 35 to 2 µg/m³ in about 5 min, and the gasket leak holds a floor of about 0.17 µg/m³ in a 15 µg/m³ room [G1]. At 5 L/min the decay from 300 to 5 µg/m³ takes about 28 min, 29 min without deposition, so wall losses barely matter. The 300 µg/m³ start needs about 10.8 µg of smoke, which a 60 mL syringe delivers if the plume in the cup is above 0.18 mg/m³ [G2]. R7 is met. R8 is **not met** by the rig alone: the transfer SPS30 still needs a collocation site, which remains open for Amish.

## H. CO2 (R9)

Recirculating the chamber through soda lime at 3 L/min brings it to 50 ppm in about 25 min, with a leak floor of about 8 ppm; one liter of breath at 4 % CO2 then adds about 1,081 ppm, and the SCD30 reference is good to about ±60 ppm at 1,000 ppm [H1]. R9 is met by calculation and datasheet.

## I. Throughput (R11)

For the four EPA points, run cold to hot, each point settles for the longer of its temperature ramp and humidity change, then allows 15 min for the heads to equilibrate and holds for 30 min: 20 °C and 40 % RH 22 + 15 + 30 min; 20 °C and 85 % RH 26 + 15 + 30 min; 40 °C and 85 % RH 31 + 15 + 30 min; 40 °C and 40 % RH 22 + 15 + 30 min [I1]. The sweep takes about 4.7 h and the particle run about 49 min, 5.5 h in all [I2]. R11 is met.

## J. Power (R15)

The peak load is about 90 W: the Peltier at 59 W, bubbler heater 10 W, line trace 3 W, pumps 4 W, fans 6 W, HEPA blower 3 W, controller 2 W and sensors 3 W, or 7.5 A at 12 V [J1]. This is within the 100 W limit, the 10 A supply and the 10 A fuse. R15 is met. The TRL 2 figure of about 70 W and 6 A left out the heaters.

## K. Cost (R12)

The BOM totals $439 on 19 lines, $27 over the value-engineering target `budget_usd` of $412 (a hypothetical control target, not a limit; set by Amish on 2026-09-26 to cover the then priced BOM, DDR-002; it was $400, and $300 before 2026-09-25) [K1]. The increase from $396 at TRL 2 comes from the extra jacket panels, the 120 mm fan, the bubbler sleeve and trace heat ($404 in v0.1), about $8 for the larger inner fin block, and $27 for the parts that make the design buildable (CLR-DDR-003): the front frame, drip tray and spacers ($6), two more latches and a larger door ($2), hook-and-loop pads ($1), clamp screws and sleeves ($2), the dryer socket and jar rack ($2) and new line 19, bulkhead fittings, cable glands and the drain ($14). A core version without CO2 (no SCD30 and no soda lime) would cost about $372. R12 is **over the value-engineering target** by $27; savings worth trying are in the value engineering section of CLR-DEC-001.

## L. Results against every requirement

*Table 4. Results against CLR-REQ-001 v0.4 (tags point to the script output).*

| ID | Target | Value | Status |
| --- | --- | --- | --- |
| R1 | 10 to 40 °C in a room at 15 to 25 °C; lowest point stated up to 30 °C | 6.7 °C lowest in a 25 °C room; 11.1 °C in a 30 °C room; 40 °C held [B4, B6] | Met |
| R2 | 20 to 85 % RH at 20 to 40 °C | Reached in 26 min or less; 20 °C and 85 % RH held in rooms up to about 28 °C [C2, C3, C8, C9] | Met |
| R3 | ±0.3 °C, ±2 % RH over 30 min | ±0.02 °C, ±1.0 % RH (idealized model) [D1, D2] | Met |
| R4 | ±0.3 °C, ±2 % RH between bays | ±0.18 °C at the EPA points, ±0.42 °C at 10 °C; ±0.8 % RH [E1, E2] | At risk |
| R5 | 0.2 °C, k = 2 | 0.14 °C (0.1 °C tolerance); 0.24 °C (0.2 °C tolerance) [F1] | At risk |
| R6 | 2 % RH, k = 2 | 2.0 % RH [F3] | At risk |
| R7 | Zero below 2 µg/m³; 300 to 5 µg/m³ in 45 min | 5 min clean-down, 0.17 µg/m³ floor; 28 min decay [G1, G2] | Met |
| R8 | Transfer PM sensor collocated 30 days | First candidate site named (CLR-DEC-001); not yet collocated | **Not met** |
| R9 | Zero below 50 ppm; span 400 to 2,000 ppm | 8 ppm floor; about 1,100 ppm added per liter of breath, to about 1,500 ppm from room air [H1] | Met |
| R10 | Six heads 90 x 70 x 50 mm; large items in two or four bays | Six bays, 244 mm clear [A2]; large item case not yet checked | Met (six heads) |
| R11 | Sweep plus particle run in 8 h | 5.5 h [I2] | Met |
| R12 | $412 in parts | $439 [K1] | Over the value-engineering target by $27 |
| R13 | 600 x 500 mm, 400 mm high, 14 kg | 600 x 500 x 371 mm, 13.8 kg [A3] | Met |
| R14 | CSV and per-sensor report to the US EPA 2021 targets, with uncertainty chain | Software not written (beyond TRL 3) | Not verifiable at TRL 3 |
| R15 | No mains; fused 12 V; 100 W peak | 90 W, 7.5 A [J1] | Met |
| R16 | Cut-offs at 50 °C air and 70 °C hot side | Outer sink 50 °C at most in use [J2] | Met |
| R17 | No toxic gases; smoke cleared through HEPA | By design; 5 min clean-down [G1] | Met |
| R18 | Saw or laser cutter, drill, soldering iron | By design; no machined parts in the model | Met |

Counts: met 12, at risk 3, not met 1 (R8), over the value-engineering target 1 (R12), not verifiable at TRL 3 1 [L1].

## Checks against the TRL 2 figures

*Table 5. TRL 2 claims checked and corrected.*

| TRL 2 claim (CLR-PRC-001 v0.2, README) | TRL 3 value | Change |
| --- | --- | --- |
| Heat leak about 1.0 W/K | 0.82 W/K with door panel and full jacket; 1.17 W/K panel off | Jacket extended to all faces |
| Internal gains about 4 W | 6.7 W | Corrected |
| 10 °C not reachable in a 30 °C room; about 15 °C lowest | 11.1 °C lowest in a 30 °C room; 6.7 °C in a 25 °C room (larger inner sink) | Corrected |
| Settling about 45 min per point; sweep plus particle run about 6 h | 22 to 31 min to settle plus 15 min equilibration; 5.5 h | Corrected |
| Decay 300 to 5 µg/m³ about 30 min | 28 min | Confirmed |
| Peak power about 70 W; bus about 6 A | 90 W; 7.5 A | Corrected (heaters added) |
| Size about 610 x 470 x 350 mm; mass about 10 kg | 600 x 500 x 371 mm; 13.8 kg | Corrected |
| Parts about $396 | $439 (larger inner sink; parts for construction) | Corrected |
| Door with panel just above dew point at 40 °C, 85 % RH | 1.2 K margin at 22 °C, 0.5 K at 15 °C | Confirmed |
| Humidity range met by estimate | Not met at 20 °C, 85 % RH above a 19 °C room with the stock sink; met up to 28 °C with the larger sink (DDR-002) | New finding, resolved |
