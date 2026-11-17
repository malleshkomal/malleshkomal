import sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
import os
HERE = Path(__file__).resolve().parent if "__file__" in dir() else Path(".")
sys.path.insert(0, os.environ.get("LCITOOLS_SRC", str(Path(__file__).resolve().parent.parent.parent / "ptl-lci-explorer/src")))
import networkx as nx
from lcitools.reader import dataset_paths, read_brightway_csv, read_metadata, read_properties
from lcitools.validate import run_all
from lcitools.model import inventory
from lci_specs import CASES
CHECK = {  # (FU index, flow name, expected per FU) -> must match portfolio LCI tables
 1: [(0, "market for irrigation", 0.018), (0, "market for electricity, medium voltage", 0.35), (0, "Occupation, permanent crop", 0.72), (0, "market for sugar, from sugar beet", 0.046)],
 2: [(0, "market for irrigation", 1.18), (0, "market for nitrogen fertiliser, as N", 0.028), (0, "market for tap water", 95 + 52)],
 3: [(0, "market for polyethylene terephthalate, granulate, bottle grade", 0.014), (0, LORRY := "market for transport, freight, lorry 16-32 metric ton, EURO6", 0.16 + 0.007 + 0.00075)],
 4: [(0, "market group for electricity, high voltage", 0.013 * 1.015 * 14), (0, "market for scrap aluminium", 0.00975)],
 5: [(0, "market for waste paper, sorted", 0.26), (0, "market for packaging film, low density polyethylene", 0.012)],
 6: [(0, "market for aluminium, wrought alloy", 0.0022), (0, "market for coffee, green bean", 0.003)],
 7: [(0, "market for nickel sulfate", 202), (0, "market for electricity, medium voltage", 1200 + 200 + 1500 + 80 + 300), (0, "market group for electricity, low voltage", 3400)],
 8: [(0, "market for electricity, low voltage", 4.0), (0, "market for gold", 0.000035 / 3)],
 9: [(0, "market for waste plastic, mixture", 440), (0, "market for polyethylene, high density, granulate", -448)],
 10: [(0, "market for liquid packaging board", 0.011), (1, "market for electricity, low voltage", 0.04), (1, "market for polypropylene, granulate", 0.0018)],
 11: [(0, "compound fish feed", 1788.3331), (1, "Nitrogen", 54.6786), (2, "Water, salt, ocean", 45188.6792)],
}
ok = True
for c in CASES:
    root = Path(__file__).resolve().parent.parent / "lci" / c["slug"]; p = dataset_paths(root)
    db, acts, excs = read_brightway_csv(p["csv"])
    props = read_properties(p["properties"]); meta = read_metadata(p["metadata"])
    f = run_all(db, acts, excs, props, meta)
    errors = [x for x in f if x.level == "error"]
    warns = [x for x in f if x.level == "warning"]
    g = nx.read_graphml(p["graphml"])
    print(f"\n{c['n']:>2} {c['slug']}: {len(acts)} activities, {len(excs)} exchanges | graph {g.number_of_nodes()} nodes / {g.number_of_edges()} edges | "
          f"licence {meta.get('License / SPDX Identifier')} | errors {len(errors)}, warnings {len(warns)}")
    for x in f: print(f"     [{x.level}] {x.check}: {x.message[:150]}")
    assert g.number_of_edges() == len(excs), "graph edges != exchanges"
    for fu_i, name, exp in CHECK[c["n"]]:
        fu_act = acts.loc[acts["reference product"] == c["fu"][fu_i][0], "name"].iloc[0]
        tot, _ = inventory(acts, excs, {fu_act: 1.0})
        got = tot.loc[tot["name"] == name, "scaled amount"].sum()
        good = abs(got - exp) <= 1e-4 * max(1, abs(exp))
        ok &= good
        print(f"     {'OK ' if good else 'BAD'} {name[:60]:<60} expected {exp:.6g} got {got:.6g}")
print("\nALL CHECKS PASS" if ok else "\nSOME CHECKS FAILED")
