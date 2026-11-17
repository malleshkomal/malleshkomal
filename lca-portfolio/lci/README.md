# Life cycle inventories of the LCA portfolio (LCIS2024)

Foreground inventories of the 11 portfolio case studies, published in the **LCIS2024** schema
(Nair, Chougule, Gomez Trillos & Brand-Daniels, 2025, *Journal of Cleaner Production* 520, 146120,
https://doi.org/10.1016/j.jclepro.2025.146120). Each folder has the same structure as the
`power-to-liquid` example in https://github.com/malleshkomal/ptl-lci-explorer:

| File | What it is |
|---|---|
| `<name>/dataset/<name>.csv` / `.xlsx` | Foreground inventory in the Brightway2 CSV/Excel layout |
| `<name>/dataset/<name>_properties.csv` | Schema version, counts, dependencies, unique identifier |
| `<name>/metadata/metadata.xlsx` | Filled LCIS2024 metadata template (scope, assumptions, authors, background, licence, sources) |
| `<name>/network/<name>.graphml` | Supply-chain network (activities, products, flows) |
| `<name>/environment.yml` | Environment used to generate the files |

| # | Folder | Activities | Exchanges | Data |
|---|---|---|---|---|
| 1 | lca-portfolio-cocoa-chocolate | 6 | 40 | illustrative |
| 2 | lca-portfolio-cotton-tshirt | 8 | 43 | illustrative |
| 3 | lca-portfolio-pet-water-bottle | 6 | 27 | illustrative |
| 4 | lca-portfolio-aluminium-can | 6 | 29 | illustrative |
| 5 | lca-portfolio-ecommerce-box | 6 | 26 | illustrative |
| 6 | lca-portfolio-flexible-coffee-pouch | 6 | 28 | illustrative |
| 7 | lca-portfolio-ev-battery | 8 | 47 | illustrative |
| 8 | lca-portfolio-smartphone | 7 | 30 | illustrative |
| 9 | lca-portfolio-plastic-recycling-system | 5 | 23 | illustrative |
| 10 | lca-portfolio-coffee-cup | 7 | 29 | illustrative (2 functional units) |
| 11 | imta-integrate-lci | 3 | 22 | published INTEGRATE PI05#3 data (3 functional units) |

Amounts are per 1 unit of each activity's reference product. Where an exchange comment quotes a
quantity "per functional unit", the amount in the table has been normalised to 1 unit of product.

## Validation

Every folder was read with `lcitools` from ptl-lci-explorer (`read_brightway_csv`, `read_properties`,
`read_metadata`, `run_all`): **0 errors**. Expected warnings: negative amounts for the system-expansion
credits in case 9 (3) and the net nitrogen uptake of SE-IMTA in case 11 (1). Each dataset was also
scaled to its functional unit with `lcitools.model.inventory`; key flows reproduce the LCI tables of
the portfolio website.

```python
import sys; sys.path.insert(0, "ptl-lci-explorer/src")
from lcitools.reader import dataset_paths, read_brightway_csv, read_properties, read_metadata
from lcitools.validate import run_all
from lcitools.model import inventory
p = dataset_paths("lca-portfolio-cocoa-chocolate")
db, acts, excs = read_brightway_csv(p["csv"])
print(run_all(db, acts, excs, read_properties(p["properties"]), read_metadata(p["metadata"])))
totals, _ = inventory(acts, excs, {"milk chocolate bar, consumption and end-of-life": 1.0})
```

## Before reuse

- **Cases 1–10 hold illustrative values** (literature-based estimates and stated assumptions), not primary data.
  Case 11 reproduces the foreground LCI of the IMTA repository (INTEGRATE deliverable PI05#3, IPMA & CTAQUA 2020).
- Background exchanges use ecoinvent 3.10 cut-off style names (`market for ...`) and have **not** been linked
  against a licensed ecoinvent database. Proxy names are marked in the exchange comment.
- Waste-treatment inputs are entered as positive amounts, as in the PtL example; ecoinvent expects negative
  amounts for waste, so flip the sign when linking.
- Case 9 uses system expansion: negative technosphere amounts are credits (avoided virgin polymer and energy).
- Metadata: author email and affiliation are left blank for the author to fill in.
- Licence: CC BY 4.0. For case 11 the report data remain with the INTEGRATE partners.
