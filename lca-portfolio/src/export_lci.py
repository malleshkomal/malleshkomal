"""Export the portfolio LCIs in the LCIS2024 layout used by the power-to-liquid example.

<slug>/dataset/<slug>.csv, <slug>.xlsx, <slug>_properties.csv
<slug>/metadata/metadata.xlsx   (filled copy of the blank LCIS2024 template)
<slug>/network/<slug>.graphml
<slug>/environment.yml
"""
import csv, shutil, subprocess, uuid, datetime, sys
from pathlib import Path
import networkx as nx
import openpyxl
from openpyxl.styles import Font
from lci_specs import CASES, EI, BIO

import os
HERE = Path(__file__).resolve().parent
TEMPLATE = Path(os.environ.get("LCIS_TEMPLATE", HERE.parent.parent / "ptl-lci-explorer/data/original/metadata_template.xlsx"))
OUT = HERE.parent / "lci"
NOW = datetime.datetime(2026, 11, 15, 19, 30, 0)
HEADER = ["name", "amount", "database", "location", "unit", "categories", "type", "Comment", "reference product"]

PORTFOLIO_COMMENT = ("Prepared for an illustrative LCA portfolio with AI assistance (Claude, Anthropic). "
                     "Values are literature-based estimates and stated assumptions, not primary data. "
                     "Add email and affiliation before publishing.")
META = {
 1: dict(desc="Cradle-to-grave foreground LCI of a 100 g milk chocolate bar: West African cocoa cultivation incl. land-use change, fermentation and export, chocolate manufacturing in Germany, packaging, distribution, retail and end-of-life.",
         kw="Cocoa | Chocolate | Land-use change | Food LCA | Deforestation", region="CI | GH | DE", period="2018 - 2026",
         asm="10% of cocoa from land converted in the last 20 years, amortised over 20 years | Economic allocation between cocoa liquor, butter and shells | Recipe 36 g beans, 46 g sugar, 28 g milk powder per bar | 5% retail and household product waste | Packaging recycling by cut-off",
         dois="https://doi.org/10.1126/science.aaq0216 https://doi.org/10.1016/j.foodres.2018.02.042", gl="LUC - land-use change | EUDR - EU Deforestation Regulation | FU - functional unit"),
 2: dict(desc="Cradle-to-grave foreground LCI of a 180 g cotton T-shirt worn 50 times: Indian cotton cultivation, ginning and spinning, knitting and wet processing in Bangladesh, cut-make-trim, sea freight, consumer washing and drying in Germany, end-of-life.",
         kw="Cotton | Textiles | Wet processing | Consumer use | Circular textiles", region="IN | BD | DE", period="2017 - 2026",
         asm="Conventional cotton, 50% irrigated | Economic allocation lint/cottonseed (about 85% to lint) | Coal and gas steam at dye house | 25 washes at 40 C, 10 tumble-dry cycles | 25% collected for reuse, cut-off",
         dois="", gl="CMT - cut-make-trim | Ne - English cotton count | ZDHC - Zero Discharge of Hazardous Chemicals"),
 3: dict(desc="Cradle-to-grave foreground LCI of packaging and delivery of 500 ml still mineral water in a 14 g virgin PET bottle (reference case), including cap, label, bottling, distribution, chilling and end-of-life.",
         kw="PET | Beverage packaging | Recycled content | Deposit return | Single-use plastics", region="DE", period="2020 - 2026",
         asm="Virgin PET reference (EU SUPD requires 25% rPET from 2025) | 300 km one-way distribution | 50% of bottles chilled 2 days | 60% collected for recycling, cut-off | Product water counted as resource withdrawal",
         dois="", gl="PET - polyethylene terephthalate | rPET - recycled PET | DRS - deposit-return system | SUPD - Single-Use Plastics Directive"),
 4: dict(desc="Cradle-to-grave foreground LCI of a 330 ml aluminium beverage can made from 100% primary aluminium at the global-average production mix, with casting and rolling, can making, filling, distribution, chilling and collection.",
         kw="Aluminium | Beverage can | Smelting | Recycled content | Closed-loop recycling", region="GLO | DE", period="2020 - 2026",
         asm="Smelting 14 kWh/kg on a global-average grid | 13 g can incl. end | 75% collection, cut-off (remelting carried by the next product) | Process scrap remelted in-house | Beverage excluded",
         dois="", gl="UBC - used beverage can | PFC - perfluorocarbon | CBAM - Carbon Border Adjustment Mechanism"),
 5: dict(desc="Foreground LCI of the packaging needed to deliver a 1 kg e-commerce order in Germany: containerboard (50% recycled fibre), corrugated box, plastic void fill, transport to the fulfilment centre, volume-allocated parcel delivery and end-of-life.",
         kw="Corrugated board | E-commerce | Packaging | Right-sizing | Last-mile delivery", region="DE", period="2020 - 2026",
         asm="Oversized 450 g box with 12 g LDPE air pillows (baseline) | Delivery allocated by parcel volume (0.2 tkm equivalent) | 85% box recycling, cut-off | Biogenic carbon neutral",
         dois="", gl="FC - fulfilment centre | LCV - light commercial vehicle | PPWR - Packaging and Packaging Waste Regulation"),
 6: dict(desc="Foreground LCI of a multilayer PET/aluminium/PE stand-up pouch for 250 g ground coffee, including laminate production, pouch making, filling, distribution, coffee lost through packaging failure and end-of-life.",
         kw="Flexible packaging | Multilayer | Food waste | Design for recycling | Coffee", region="DE", period="2020 - 2026",
         asm="11 g pouch with 2 g aluminium foil | 8% converting waste | 1% of coffee lost through barrier failure | Multilayer pouch incinerated (not recyclable in practice) | Coffee excluded except the lost share",
         dois="", gl="EVOH - ethylene vinyl alcohol | PE - polyethylene | D4ACE - Designing for a Circular Economy (CEFLEX)"),
 7: dict(desc="Cradle-to-grave foreground LCI of a 60 kWh NMC811 traction battery pack: cathode and anode active materials, cell manufacturing and pack assembly in China, shipping to Europe, battery-attributable charging losses over 200,000 km, and hydrometallurgical recycling.",
         kw="Lithium-ion battery | NMC811 | Critical raw materials | Battery recycling | Electric vehicles", region="CN | RER", period="2019 - 2026",
         asm="Cell manufacturing 25 kWh electricity per kWh capacity on a Chinese grid | Pack mass 400 kg, 260 kg cells | Battery losses 10% of 34,000 kWh traction energy on the EU grid | Recycling without credits (cut-off) | Virgin materials",
         dois="https://doi.org/10.3390/batteries5020048", gl="NMC - nickel manganese cobalt oxide | CAM - cathode active material | BMS - battery management system | LCE - lithium carbonate equivalent"),
 8: dict(desc="Foreground LCI of smartphone service for one user for one year: one third of a 180 g smartphone (components, display, battery, assembly, packaging, air freight) used for three years, one year of charging and one third of end-of-life.",
         kw="Smartphone | Electronics | Integrated circuits | Product lifetime | E-waste", region="CN | DE", period="2019 - 2026",
         asm="Phone used three years | ICs modelled with ecoinvent logic and memory IC datasets | OLED display and phone cell use proxy datasets | Air freight 9,000 km | Charging 4 kWh per year; network energy excluded",
         dois="https://doi.org/10.1016/j.eiar.2020.106416", gl="IC - integrated circuit | PWB - printed wiring board | OLED - organic light-emitting diode"),
 9: dict(desc="Gate-to-grave foreground LCI of managing 1 t of household plastic packaging waste by kerbside collection, MRF sorting, transport and mechanical recycling, with system-expansion credits for avoided virgin polymer and recovered energy.",
         kw="Plastic recycling | Waste management | MRF | System expansion | Recyclate", region="DE", period="2020 - 2026",
         asm="75% sorted to polymer streams, 75% reprocessing yield | Residues (440 kg) incinerated with energy recovery | Substitution factor 0.8 for recyclate | Avoided energy credited at the German grid and natural-gas heat | Negative amounts are credits",
         dois="", gl="MRF - material recovery facility | NIR - near-infrared | DRS - deposit-return system"),
 10: dict(desc="Foreground LCI of serving a 350 ml hot drink in (1) a single-use PE-lined paper cup with polystyrene lid and (2) a reusable polypropylene cup used 50 times and washed in a home dishwasher.",
         kw="Coffee cup | Single-use | Reuse | Packaging | Dishwashing", region="DE | RER", period="2020 - 2026",
         asm="Single-use cup 11 g board + 0.6 g PE + 3 g PS lid | End-of-life 65% incineration, 30% landfill, 5% recycling | Reusable cup 100 g PP, 50 uses | Washing 0.04 kWh per use in shared loads | Coffee excluded",
         dois="", gl="PE - polyethylene | PS - polystyrene | PP - polypropylene | PLA - polylactic acid"),
 11: dict(desc="Foreground LCI per functional unit of three earthen-pond aquaculture systems from INTEGRATE deliverable PI05#3: semi-intensive fishpond polyculture (baseline), semi-intensive pond IMTA and semi-extensive pond IMTA. Farm-gate inputs, seawater use, land occupation and net N and P to water.",
         kw="IMTA | Pond aquaculture | Oysters | Macroalgae | Nutrient balance", region="PT | ES", period="2017 - 2019",
         asm="Functional unit 1 t fish + oyster flesh weight gain at farm gate, one cycle | Macroalgae outside the functional unit (no allocation, no credit) | Infrastructure allocated by production-pond area | N = protein / 6.25; N and P emissions from nutrient balance (Cho & Kaushik 1990) | Fry modelled with a carp-fry proxy",
         dois="https://doi.org/10.1016/j.aquaculture.2024.741035 https://doi.org/10.1016/j.jclepro.2008.08.008 https://doi.org/10.1111/raq.12280",
         gl="IMTA - integrated multi-trophic aquaculture | SI - semi-intensive | SE - semi-extensive | POLY - polyculture | FCR - feed conversion ratio"),
}


def code(slug, name):
    return uuid.uuid5(uuid.NAMESPACE_URL, f"{slug}/{name}").hex


def num(x):
    x = float(x)
    return 0.0 if x == 0 else float(f"{x:.6g}")


def build(c):
    slug = c["slug"]
    acts = {a["name"]: a for a in c["activities"]}
    rows = []  # (activity dict, exchange rows)
    for a in c["activities"]:
        per = a["per"]
        bio, tech = [], []
        for e in a["exchanges"]:
            amt = num(e["amount"] / per)
            com = e.get("comment") or c["src"]
            if per != 1 and e.get("comment"):
                com += f" (note per functional unit; exchange normalised to 1 {a['unit']} of product)"
            if e["type"] == "biosphere":
                bio.append([e["name"], amt, BIO, "", e["unit"], e["categories"], "biosphere", com, ""])
            elif e["type"] == "foreground":
                t = acts[e["name"]]
                tech.append([t["name"], amt, slug, t["location"], t["unit"], "", "technosphere", com, t["product"]])
            else:
                tech.append([e["name"], amt, e["database"], e["location"], e["unit"], "", "technosphere", com, e["product"]])
        prod = [a["name"], 1, slug, a["location"], a["unit"], "", "production", c["src"], a["product"]]
        rows.append((a, sorted(bio) + [prod] + sorted(tech, key=lambda r: r[0])))
    return rows


def write_dataset(c, rows, folder):
    slug = c["slug"]
    lines = [["Database", slug], ["format", "Excel spreadsheet"], []]
    for a, ex in rows:
        lines += [["Activity", a["name"]], ["code", code(slug, a["name"])], ["comment", a["comment"]],
                  ["location", a["location"]], ["production amount", 1], ["reference product", a["product"]],
                  ["unit", a["unit"]], ["worksheet name", slug[:31]], ["Exchanges"], HEADER] + ex + [[]]
    d = folder / "dataset"; d.mkdir(parents=True, exist_ok=True)
    with open(d / f"{slug}.csv", "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(lines[:-1])
    wb = openpyxl.Workbook(); ws = wb.active; ws.title = slug[:31]
    bold = Font(bold=True)
    for r in lines[:-1]:
        ws.append([None if v == "" else v for v in r])
        if r and r[0] in ("Database", "Activity", "Exchanges", "name"):
            for cell in ws[ws.max_row]:
                cell.font = bold
    ws.column_dimensions["A"].width = 55
    for col in "BCDEFGHI":
        ws.column_dimensions[col].width = 18
    wb.save(d / f"{slug}.xlsx")
    allx = [e for _, ex in rows for e in ex]
    props = [("Dataset Name", slug), ("Schema Version", "LCIS2024"), ("Dataset Version", "1.0.0"),
             ("Software", "Python 3.11 export script (Brightway2 CSV/Excel layout); not exported from Brightway"),
             ("Export Time", NOW.strftime("%Y%m%d-%H%M%S")),
             ("Unique Dataset Identifier", uuid.uuid5(uuid.NAMESPACE_URL, f"{slug}-LCIS2024-1.0.0").hex),
             ("Total Project Parameters", 0), ("Total Database Parameters", 0), ("Total Activity Parameters", 0),
             ("Total Activities", len(rows)), ("Total Exchanges", len(allx)),
             ("Total Biosphere flows", sum(e[6] == "biosphere" for e in allx)),
             ("Total Technosphere flows", sum(e[6] == "technosphere" for e in allx)),
             ("Total Reference products", len({a["product"] for a, _ in rows})),
             ("Dataset dependencies", ", ".join(dict.fromkeys([slug, BIO] + sorted({e[2] for e in allx if e[2] not in (slug, BIO)}))))]
    with open(d / f"{slug}_properties.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Property", "Value"]); w.writerows(props)
    return props


def write_graph(c, rows, folder):
    g = nx.DiGraph()
    for a, ex in rows:
        an = f"Activity - {a['name']}"
        g.add_node(an, color="blue", width=26)
        for e in ex:
            name, amt, db, loc, unit, cat, typ = e[:7]
            if typ == "production":
                node = e[8]; g.add_node(node); g.add_edge(an, node, color="black", line_type="Dash", amount=float(amt), unit=unit, arrows=True)
            elif typ == "biosphere":
                g.add_node(name); g.add_edge(an, name, color="green", line_type="Dots", amount=float(amt), unit=unit, arrows=True)
            else:
                node = e[8] or name; g.add_node(node); g.add_edge(node, an, color="purple", line_type="Solid", amount=float(amt), unit=unit, arrows=True)
    d = folder / "network"; d.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(g, d / f"{c['slug']}.graphml")
    return g


def write_metadata(c, folder):
    m = META[c["n"]]; imta = c["n"] == 11
    d = folder / "metadata"; d.mkdir(parents=True, exist_ok=True)
    tmp = d / "_fill.xlsx"; shutil.copy(TEMPLATE, tmp)
    wb = openpyxl.load_workbook(tmp); ws = wb["Metadata"]
    bg = ("Piscentool / SimaPro background as used in INTEGRATE PI05#3", "not reported", "not reported", "https://www.integrate-imta.eu",
          "Background data are not redistributed; impact results per process are in the case study, Annex 1 of the report.") if imta else \
         ("ecoinvent | biosphere3", "3.10.0 | 3.10.0", "cutoff | elementary flows", "https://ecoinvent.org | https://ecoinvent.org",
          "Background exchanges use ecoinvent-style names and have NOT been linked against a licensed ecoinvent database; check names when linking.")
    vals = {
        1: c["slug"], 2: m["desc"], 3: 2026, 4: "en", 5: m["kw"],
        6: "Mixed" if imta else "Secondary", 7: "Attributional",
        8: "Cradle to gate" if imta else ("Gate to grave" if c["n"] == 9 else "Cradle to grave"),
        9: " | ".join(f[1] for f in c["fu"]), 10: m["region"], 11: m["period"], 12: m["asm"], 13: "LCIS2024",
        15: "Komal Mallesh Chougule", 16: None, 17: None,
        18: ("Foreground LCI derived from INTEGRATE deliverable PI05#3 and scaled to the functional unit in the IMTA repository." if imta else PORTFOLIO_COMMENT),
        20: bg[0], 21: bg[1], 22: bg[2], 23: bg[3], 24: bg[4],
        26: "Creative Commons Attribution 4.0 International",
        28: "Cite the dataset and, for case 11, INTEGRATE deliverable PI05#3 (IPMA & CTAQUA 2020)." if imta else "Cite: Life Cycle Assessment Portfolio (2026), case study dataset.",
        30: "Report data remain with the INTEGRATE partners; KPI layer and derived files CC BY 4.0." if imta else "Illustrative values for demonstration; not for product claims or EPDs.",
        32: "IPMA, Portugal | CTAQUA, Spain (INTEGRATE data providers)" if imta else None,
        33: "INTEGRATE, EAPA_232/2016, Interreg Atlantic Area (ERDF), EU" if imta else None,
        35: "Experimental farm records (water flow and renewal, aeration, feed, mortality, treatments)" if imta else None,
        36: 2019 if imta else None, 37: ".csv | .xlsx" if imta else None, 38: "en" if imta else None,
        39: "Partial" if imta else None,
        40: "https://github.com/malleshkomal/Life-cycle-assessment-of-Integrated-Multi-Trophical-Aquaculture-" if imta else None,
        41: "Primary data as published in the report tables; raw farm data not public." if imta else None,
        43: "Reports" if imta else "Mixed", 44: m["period"], 45: "en", 46: "Partial" if imta else "Yes",
        47: m["dois"] or None,
        50: ("https://www.integrate-imta.eu" if imta else "https://publications.jrc.ec.europa.eu/repository/handle/JRC136771" if c["n"] in (3, 5, 10) else None),
        51: None if imta else "Values set within ranges reported in the cited sources and LCA databases; see the portfolio Sources page.",
        53: m["gl"],
    }
    for r, v in vals.items():
        ws.cell(row=r, column=3, value=v)
    # full-row separator merges (e.g. A25:XFD25) are rewritten by LibreOffice in a form pandas cannot read
    for rng in [str(m) for m in ws.merged_cells.ranges if "XFD" in str(m)]:
        ws.unmerge_cells(rng); ws.merge_cells(rng.replace("XFD", "C"))
    wb.save(tmp)
    # recalculate so label formulas and the SPDX lookup carry cached values
    subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", str(d / "_lo"), str(tmp)],
                   check=True, capture_output=True, timeout=180)
    shutil.move(d / "_lo" / "_fill.xlsx", d / "metadata.xlsx"); shutil.rmtree(d / "_lo"); tmp.unlink()


ENV = """name: lca-portfolio-lci
# Environment used to generate these LCIS2024 files (export script, not Brightway).
# The CSV/XLSX follow the Brightway2 Excel layout; to import, link the background
# exchanges against your licensed ecoinvent 3.10 cut-off database (e.g. bw2io ExcelImporter).
channels:
  - conda-forge
dependencies:
  - python=3.11
  - pandas
  - openpyxl
  - networkx
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    summary = []
    for c in CASES:
        folder = OUT / c["slug"]
        rows = build(c)
        props = write_dataset(c, rows, folder)
        write_graph(c, rows, folder)
        write_metadata(c, folder)
        (folder / "environment.yml").write_text(ENV)
        p = dict(props)
        summary.append((c["n"], c["short"], c["slug"], p["Total Activities"], p["Total Exchanges"],
                        p["Total Biosphere flows"], p["Total Technosphere flows"]))
        print(summary[-1])
    return summary


if __name__ == "__main__":
    main()
