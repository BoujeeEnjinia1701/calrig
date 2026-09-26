# BOM notes

- Every line in `bom.csv` carries an indicative unit price in USD and a supplier or supplier type. Prices are single-unit estimates for a garage build, not quotes.
- Total: $412 on 18 lines (checked by `docs/04-calcs/sizing.py`, CLR-CAL-001 v0.2 section K). This is $12 over `budget_usd` of $400 in `project.yaml` (raised from $300 by Amish on 2026-09-25, CLR-DDR-002). How to close the $12 is awaiting Amish.
- A core version without CO2 (no SCD30 in line 8 and no line 16) would be about $345.
- Change after CLR-DDR-002: line 5 now includes a larger inner fin block (about 0.20 K/W, about $8), so the 20 °C, 85 % RH point holds in rooms up to about 28 °C. A certified temperature probe (decided if the budget allows) is not included, because the budget does not yet allow it.
- Changes at TRL 3: line 3 now jackets every face except the door and includes the removable door panel; line 4 is trimmed to 600 x 500 mm; line 6 is a 120 mm fan; line 9 adds a foam sleeve and a trace-heated outlet line. Line numbers 1 to 15 match the exploded view and drawing CLR-DWG-001.
- Line 18 (software) is priced at zero and is not written at TRL 3.
