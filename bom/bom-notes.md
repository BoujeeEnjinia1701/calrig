# BOM notes

- Every line in `bom.csv` carries an indicative unit price in USD and a supplier or supplier type. Prices are single-unit estimates for a garage build, not quotes.
- Total: $439 on 19 lines (checked by `docs/04-calcs/sizing.py`, CLR-CAL-001 v0.4 section K). This is $27 over the value-engineering target `budget_usd` of $412 in `project.yaml` (a hypothetical control target, not a limit; set by Amish on 2026-09-26 to cover the BOM as it then stood, CLR-DDR-002). `budget_usd` is unchanged.
- A core version without CO2 (no SCD30 in line 8 and no line 16) would be about $372.
- Change after CLR-DDR-002: line 5 now includes a larger inner fin block (about 0.20 K/W, about $8), so the 20 °C, 85 % RH point holds in rooms up to about 28 °C. A certified temperature probe (decided if the cost target allows) is not included, because the estimate is already above the $412 value-engineering target.
- Changes at TRL 3: line 3 now jackets every face except the door and includes the removable door panel; line 4 is trimmed to 600 x 500 mm; line 6 is a 120 mm fan; line 9 adds a foam sleeve and a trace-heated outlet line. Line numbers 1 to 15 match the exploded view and drawing CLR-DWG-001.
- Line 18 (software) is priced at zero and is not written at TRL 3.
- Changes for construction (CLR-DDR-003, 2026-10-01): line 1 adds the front frame, drip tray and fan spacers; line 2 has a 430 x 330 mm door and four latches; line 3 a smaller door panel on hook-and-loop pads; line 4 is 9 mm plywood with six feet (mass); line 5 adds clamp screws and sleeves; line 10 a printed socket; line 13 a cut-off relay (no price change); line 15 a printed rack; new line 19 holds the bulkhead fittings, cable glands and drain. Line numbers 1 to 15 and 19 match the exploded view.
