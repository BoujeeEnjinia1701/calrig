---
doc_id: CLR-DDR-003
title: CalRig design for construction
project: CalRig
doc_type: Design decision record
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target; cost wording only, no number changed
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Accepted by Amish on 2026-10-02, including the recommendations for A2 and A3; A1 stays proposed'
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Consequences updated after the approved follow-ups: appearance model brought in line with the constructable design and render scenes exported; A2 margin now 0.08 kg'
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations for A2 and A3 in Table 3, now decided as recommended and recorded in the design decisions register (CLR-DEC-001). A1 was not one of the open decisions in the register; it stays proposed, and its recommendation (keep the design and re-price at purchase) is carried in the register's value engineering section.

## Context

On 2026-09-30 Amish approved the build plan format and asked for it across all repos, writing: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of CLR-DDR-002 showed what CalRig does, but checking it part by part with build123d found twelve places where it could not be built as drawn: parts with no fixing, parts floating in the air, air loops with no way into the chamber, and a door with nothing to seal against.

The changes keep what the rig does: the same 36 L chamber, jacket, Peltier assembly, inner fin block, mixing fan, six bays, references, bubbler, dryer, HEPA loop, aerosol port, controller, supply and salt jars, in the same places. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now builds each component separately and runs 79 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must stay apart are apart by at least the stated clearance. All 79 pass.

## Options considered

For each problem the simplest change that a maker with a laser cutter, a saw, a drill and a 3D printer can build was chosen, keeping every part in its concept position where possible. The alternatives weighed are given in the "Why this way" column.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The door was a 412 x 312 mm sheet the size of the shell, sealing on the 6 mm front edges of the walls, too narrow for a D-section gasket. Its two latches were blocks on the door with nothing to catch on. | A 6 mm acrylic front frame, 450 x 350 mm with a 400 x 300 mm window, is solvent-welded to the shell's front edges and covers 19 mm of the jacket's front edges. The gasket sits on the frame 4 to 12 mm outside the opening. The door is 430 x 330 mm and overlaps the opening by 15 mm. Four draw latches (not two) sit on four 41 x 40 mm tabs on the frame, and hook keepers on the door. | Gives the gasket a 25 mm wide face and the latches something to pull against. Four latches squeeze a 430 mm long gasket evenly; two at mid-height would leave the corners loose. The frame is cut from the same sheet as the shell. |
| P2 | The removable door panel (462 x 362 mm) stood in front of the latches with no fixing. | The panel is 406 x 330 mm, covers the opening with 3 mm to spare each side, sits flat on the door between the latches and is held by four hook-and-loop pads. | No new hardware; it comes off by hand for the warm, dry points. The door's inside area that the condensation check uses (400 x 300 mm) is still covered. |
| P3 | The Peltier assembly passed through the wall with nothing clamping it to the wall, and its block floated in the opening. | The inner and outer sink bases (120 x 110 mm) clamp the right wall between them with four M4 stainless screws at 57 mm either side and 42 mm above and below the centre. The screws pass through rigid sleeves in the jacket so the foam is not crushed. The 80 x 80 mm module and spacer block sits in the 90 x 100 mm opening with 5 mm all round, filled with XPS offcuts and sealant. | This is how air-to-air thermoelectric assemblies are normally mounted through an insulated wall. Sink sizes, the fin block and the thermal path are unchanged. |
| P4 | The mixing fan floated 5 mm off the back wall with no fixing. | Four 12 x 12 x 15 mm acrylic spacers are welded to the inside of the back wall; the fan screws to them with M4 nylon screws, 15 mm off the wall. | No hole through the wall, so no leak; 15 mm lets the fan draw air from behind. |
| P5 | The tray stood on four 5 x 5 mm posts, and its perforation was not defined. | Four 10 x 10 x 50 mm welded legs, 10 mm in from each corner; 87 holes of 8 mm on a 24 mm grid (none over the legs). The tray stands loose and lifts out through the door. | 5 mm posts are too thin to weld square. The hole grid gives the "perforated" tray of the concept. |
| P6 | The reference mast stood behind the tray at tray-top height with nothing under it. | A printed 20 x 20 mm mast stands on the chamber floor against the back of the tray rail, held by two M4 nylon screws; the reference carrier screws onto its top. The references stay 120 mm above the tray. | Nothing is screwed into the shell, and the mast comes out with the tray. |
| P7 | The bubbler and dryer lines stopped at the jacket face with no fitting through the wall; the dryer line ended 10 mm short of the column; and the loop had no way out of the chamber, so the two pumps (in BOM lines 9 and 10, not modelled) had nothing to draw from. | Three 12 mm barbed bulkhead fittings in the right wall: the wet inlet, the dry inlet and a new suction port 20 mm above the floor. Two air pumps on the base draw through the suction port. The dryer line turns into the column. The dryer stands in a printed socket screwed to the base; the bubbler moved 10 mm back to clear the front frame. | A closed loop needs an outlet as well as inlets, as the precis describes ("draw air from the chamber and return it"). Bulkheads seal on the acrylic; the jacket holes are 4 mm clear. |
| P8 | The HEPA unit stood behind the chamber with no connection to it. | Two 12 mm bulkhead fittings in the back wall, 80 mm apart and 77 mm above the floor, run straight into the HEPA unit's ports. | The shortest air path; the unit pushes onto the fittings and is then screwed down. |
| P9 | The sensor and reference leads passed through one gland in the door, with no position given; opening the door would drag every lead. | Two M20 cable glands with multi-hole seal inserts in the back wall, 37 mm above the floor; the USB and I2C hub moves to the controller behind the chamber. | Leads stay put when the door opens; the gland is no longer in the clear door. |
| P10 | The precis keeps a drip tray and drain for cold points, but the model had none. | A 50 x 130 x 14 mm acrylic drip tray welded to the right wall 4 mm under the inner sink; a 6 mm drain bulkhead just above its floor; a line to a 250 mL bottle on the base. | Water from the inner sink at cold points leaves the chamber instead of pooling on the floor. |
| P11 | The aerosol port's 16 mm stub floated in a 20 mm hole. | The shell hole is 16 mm, the stub is a bulkhead with a nut inside, and the jacket hole is 32 mm. | Seals on the acrylic like the other bulkheads. |
| P12 | The salt jars stood loose on the base. | A printed rack with four pockets, screwed to the base. | Keeps the jars upright and labelled. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Base plate | 9 mm sealed birch plywood instead of 12 mm (plywood or HDPE), six rubber feet. Overall height 371 mm (was 374 mm). | The added acrylic, fittings and holders added about 0.7 kg; the thinner base saves 0.5 kg, so the rig is 13.83 kg against R13's 14 kg [A3]. The chamber and jacket stiffen the base where it carries load. |
| Mass | 13.8 kg (was 13.6 kg), R13 still met with 0.17 kg margin. | CLR-CAL-001 v0.4 [A3]. |
| Cost | $439 on 19 lines (was $412 on 18): lines 1, 2, 3, 5, 10 and 15 repriced and line 19 (bulkhead fittings, cable glands and drain, $14) added. R12 is now over the value-engineering target by $27; see A1. | Parts added for construction. `budget_usd` is unchanged at $412. |
| Wiring | The two bimetal cut-offs hold in a relay on the Peltier and heater supply (BOM line 13, no price change). | Small bimetal switches are often not rated to break about 5 A of direct current; a relay keeps the cut-off independent of the software, as R16 requires. |
| Thermal | Heat capacity 8.7 kJ/K (was 8.6); 40 to 20 °C in 78 min (was 77); 10 °C reached in 2.5 h (was 2.4 h). Every other result is unchanged. | The heat balance uses the inside areas, which did not change [B7, B8]. |
| Drawings | CLR-DWG-001 Rev P4; making sketches CLR-DWG-101 to 111 added. | Follow the model. |
| Documents | CLR-CAL-001 v0.4, CLR-REQ-001 v0.6, CLR-PRC-001 v0.6; build plan CLR-BLD-001 and register CLR-DEC-001 added. | Follow the model. |

*Table 3. Proposed; A2 and A3 accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The parts that make the design buildable bring the estimated cost to $439, $27 over the $412 value-engineering target (a hypothetical control target, not a limit). | Savings worth trying: (a) a core version without CO2 (about $372), which drops the SCD30 and soda lime and so changes what the rig does; (b) look for $27 of savings elsewhere, which no line obviously offers; (c) re-price at purchase. | No change to the target; keep the design and re-price at purchase. |
| A2 | The R13 mass margin is now 0.17 kg, on estimated masses. | (a) accept, and weigh the prototype at TRL 4; (b) look for more mass now (for example 5 mm acrylic for the top). | (a), with the 5 mm acrylic top as the first fallback if the finished rig weighs over 14 kg. Accepted 2026-10-02. |
| A3 | Base material. The appearance model proposes a dark HDPE base (REVIEW 2026-09-26, item 2); a 12 mm HDPE base would weigh about 3.4 kg and take the rig to about 15.8 kg, over R13. | (a) sealed 9 mm birch plywood, as modelled; (b) HDPE, with R13 relaxed again; (c) 6 mm HDPE (about 1.7 kg) on more feet. | (a), and keep HDPE for the renders only if Amish prefers its look. Accepted 2026-10-02 as (a), with the renders drawn in plywood too so they match what will be built. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CLR-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status (CLR-CAL-001 v0.4): met 12, at risk 3 (R4, R5, R6), not met 1 (R8), over the value-engineering target 1 (R12), not verifiable at TRL 3 1 (R14).
- The appearance model `cad/src/product_model.py` was brought in line with this design on 2026-10-02 (front frame, four latches, back-wall glands and bulkheads, drain, pumps, 9 mm plywood base) and its render scenes exported; the photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` are redrawn from them on Amish's Mac.
- With A2 and A3 accepted, the rig is weighed at TRL 4 (5 mm acrylic top as the first fallback over 14 kg) and the base stays 9 mm sealed birch plywood. After the front badge, door border and pull handle adopted on 2026-10-02 the estimated mass is 13.92 kg, a 0.08 kg margin (CLR-CAL-001 v0.7).
- Parts to check when they are bought (sink base size and clamp holes, latch footprint, bulkhead and gland sizes, HEPA port spacing) are listed in the design decisions register, CLR-DEC-001.
