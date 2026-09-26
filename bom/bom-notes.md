# BOM notes

- Every line in `bom.csv` carries an indicative unit price in USD and a supplier or supplier type. Prices are single-unit estimates for a garage build, not quotes.
- Total: $404 on 18 lines (checked by `docs/04-calcs/sizing.py`, CLR-CAL-001 section K). This is $104 over `budget_usd` of $300 in `project.yaml` and $4 over the $400 proposed at TRL 2, which is awaiting Amish.
- A core version without CO2 (no SCD30 in line 8 and no line 16) would be about $337.
- Changes at TRL 3: line 3 now jackets every face except the door and includes the removable door panel; line 4 is trimmed to 600 x 500 mm; line 6 is a 120 mm fan; line 9 adds a foam sleeve and a trace-heated outlet line. Line numbers 1 to 15 match the exploded view and drawing CLR-DWG-001.
- Line 18 (software) is priced at zero and is not written at TRL 3.
