"""Foreground LCI specifications for the eleven portfolio case studies.

Amounts are per unit of each activity's reference product. Where it is easier to
think per functional unit, an activity is given with ``per`` = its output per FU and
the exporter divides every exchange by ``per``.

Values for cases 1-10 are the illustrative portfolio values (literature-based
estimates and stated assumptions). Case 11 reproduces the published foreground
LCI of the IMTA repository (INTEGRATE deliverable PI05#3).
"""

EI = "ecoinvent-3.10-cutoff"
BIO = "biosphere3"
UNITS = {"kg": "kilogram", "kWh": "kilowatt hour", "MJ": "megajoule", "tkm": "ton kilometer",
         "m3": "cubic meter", "m2a": "square meter-year", "m2": "square meter", "unit": "unit",
         "t": "metric ton"}
EWOCH = "Europe without Switzerland"
LORRY = "market for transport, freight, lorry 16-32 metric ton, EURO6"
LORRY4 = "market for transport, freight, lorry 16-32 metric ton, EURO4"
SHIP = "market for transport, freight, sea, container ship"
HEAT_NG = "market for heat, district or industrial, natural gas"
WASTE_NOTE = "waste-treatment input entered as a positive amount, as in the LCIS2024 PtL example; ecoinvent treats waste as negative - flip the sign when linking"


def T(name, amount, unit, loc, product, comment="", db=EI):
    return dict(type="technosphere", name=name, amount=amount, unit=UNITS[unit], location=loc,
                database=db, product=product, comment=comment)


def W(name, amount, loc, product, comment=""):
    return T(name, amount, "kg", loc, product, (comment + " | " if comment else "") + WASTE_NOTE)


def B(name, amount, unit, categories, comment=""):
    return dict(type="biosphere", name=name, amount=amount, unit=UNITS[unit], categories=categories,
                database=BIO, comment=comment)


def F(activity, amount, comment=""):
    return dict(type="foreground", name=activity, amount=amount, comment=comment)


def A(name, product, unit, loc, comment, exchanges, per=1.0):
    return dict(name=name, product=product, unit=UNITS[unit], location=loc, comment=comment,
                exchanges=exchanges, per=per)


CASES = []


def case(**kw):
    CASES.append(kw)


# ---------------------------------------------------------------- 1 cocoa
case(n=1, slug="lca-portfolio-cocoa-chocolate", short="Cocoa & chocolate",
     src="Portfolio case 1 (illustrative); Poore & Nemecek 2018; Konstantas et al. 2018",
     fu=[("milk chocolate bar, 100 g, eaten (functional unit)", "1 milk chocolate bar (100 g, 30% cocoa solids) eaten in Germany")],
     activities=[
    A("cocoa bean production, dried, West Africa", "cocoa beans, dried", "kg", "CI",
      "Smallholder cocoa, Cote d'Ivoire and Ghana. Yield 500 kg/ha/yr. 10% of supply from land converted in the last 20 years, amortised over 20 years.", [
        T("market for nitrogen fertiliser, as N", 0.0011, "kg", "GLO", "nitrogen fertiliser, as N", "regional surveys, low-input systems"),
        T("market for phosphate fertiliser, as P2O5", 0.0004, "kg", "GLO", "phosphate fertiliser, as P2O5", "illustrative assumption"),
        T("market for pesticide, unspecified", 0.00004, "kg", "GLO", "pesticide, unspecified", "illustrative assumption"),
        T("market for irrigation", 0.018, "m3", "RoW", "irrigation", "18 L supplementary irrigation per bar"),
        T("market for transport, freight, lorry 3.5-7.5 metric ton, EURO3", 0.0018, "tkm", "RoW", "transport, freight, lorry 3.5-7.5 metric ton, EURO3", "farm to collection point, 50 km"),
        B("Occupation, permanent crop", 0.72, "m2a", "natural resource::land", "0.036 kg / 500 kg per ha per year"),
        B("Transformation, from tropical rain forest", 0.0036, "m2", "natural resource::land", "10% of occupation converted, amortised over 20 years"),
        B("Transformation, to permanent crop", 0.0036, "m2", "natural resource::land", "mirror of forest transformation"),
        B("Carbon dioxide, from soil or biomass stock", 0.38, "kg", "air", "land-use change emissions, amortised; calibrated to portfolio result"),
        B("Dinitrogen monoxide", 0.00002, "kg", "air", "IPCC Tier 1 direct and indirect field N2O"),
     ], per=0.036),
    A("cocoa bean fermentation, drying and export to Europe", "cocoa beans, dried, at port of Amsterdam", "kg", "RER",
      "Heap fermentation and sun drying on farm, trucking to Abidjan/Tema and container shipping to Amsterdam.", [
        F("cocoa bean production, dried, West Africa", 0.036),
        T(LORRY4, 0.0108, "tkm", "RoW", "transport, freight, lorry 16-32 metric ton, EURO4", "300 km to port"),
        T(SHIP, 0.252, "tkm", "GLO", "transport, freight, sea, container ship", "7,000 km"),
     ], per=0.036),
    A("milk chocolate production", "milk chocolate, moulded", "kg", "DE",
      "Roasting, winnowing, grinding, mixing, refining, conching, tempering and moulding. Cocoa shells (0.005 kg per bar) leave as a co-product; burdens shown after economic allocation.", [
        F("cocoa bean fermentation, drying and export to Europe", 0.036),
        T("market for milk powder, whole", 0.028, "kg", "RER", "milk powder, whole", "proxy name: link to an available whole milk powder dataset (e.g. Agribalyse)"),
        T("market for sugar, from sugar beet", 0.046, "kg", "GLO", "sugar, from sugar beet"),
        T("market for electricity, medium voltage", 0.35, "kWh", "DE", "electricity, medium voltage", "industry benchmark 0.25-0.5 kWh"),
        T(HEAT_NG, 0.6, "MJ", EWOCH, "heat, district or industrial, natural gas", "roasting and conching"),
        T("market for tap water", 1.2, "kg", EWOCH, "tap water", "cleaning and cooling"),
        T(LORRY, 0.037, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "ingredients, 500 km"),
     ], per=0.105),
    A("chocolate bar packaging production", "chocolate bar packaging set (paper sleeve + Al-PE foil)", "unit", "RER",
      "4 g paperboard sleeve (50% recycled fibre) and 2 g aluminium-PE inner foil.", [
        T("market for folding boxboard carton", 0.004, "kg", "RER", "folding boxboard carton"),
        T("market for aluminium, wrought alloy", 0.0013, "kg", "GLO", "aluminium, wrought alloy", "foil share of laminate"),
        T("market for sheet rolling, aluminium", 0.0013, "kg", "GLO", "sheet rolling, aluminium"),
        T("market for packaging film, low density polyethylene", 0.0007, "kg", "GLO", "packaging film, low density polyethylene"),
        T(LORRY, 0.0018, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "300 km"),
     ]),
    A("distribution and retail of chocolate bars", "milk chocolate, packed, sold at retail", "kg", "DE",
      "Truck distribution (600 km) and ambient retail. 2 g retail losses per bar to biowaste.", [
        F("milk chocolate production", 0.105),
        F("chocolate bar packaging production", 1),
        T(LORRY, 0.07, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "600 km x 0.112 kg incl. secondary packaging"),
        T("market for electricity, low voltage", 0.02, "kWh", "DE", "electricity, low voltage", "store energy allocated by shelf space"),
        W("market for biowaste", 0.002, "RoW", "biowaste", "retail losses 2%"),
     ], per=0.103),
    A("milk chocolate bar, consumption and end-of-life", "milk chocolate bar, 100 g, eaten (functional unit)", "unit", "DE",
      "Functional unit. 3 g household food waste; paper sleeve 75% recycled (cut-off), foil laminate incinerated.", [
        F("distribution and retail of chocolate bars", 0.103),
        W("market for biowaste", 0.003, "RoW", "biowaste", "household food waste 3%"),
        W("market for waste paperboard", 0.0027, "DE", "waste paperboard", "to recycling (cut-off: burden-free for next user)"),
        W("market for municipal solid waste", 0.0033, "DE", "municipal solid waste", "foil laminate and remaining packaging, incinerated"),
     ]),
])

# ---------------------------------------------------------------- 2 T-shirt
case(n=2, slug="lca-portfolio-cotton-tshirt", short="Cotton T-shirt",
     src="Portfolio case 2 (illustrative); Textile Exchange; PEF apparel pilot",
     fu=[("cotton T-shirt, worn 50 times (functional unit)", "1 cotton T-shirt (180 g) worn 50 times and washed 25 times in Germany")],
     activities=[
    A("seed cotton production, conventional, irrigated, India", "seed cotton", "kg", "IN",
      "Conventional cotton, 50% irrigated; lint turnout about 37%.", [
        T("market for nitrogen fertiliser, as N", 0.028, "kg", "GLO", "nitrogen fertiliser, as N"),
        T("market for pesticide, unspecified", 0.0015, "kg", "GLO", "pesticide, unspecified", "active ingredient"),
        T("market for irrigation", 1.18, "m3", "RoW", "irrigation", "1,180 L blue water per T-shirt"),
        T("market for diesel, burned in agricultural machinery", 1.5, "MJ", "GLO", "diesel, burned in agricultural machinery"),
        B("Occupation, annual crop, irrigated", 1.8, "m2a", "natural resource::land"),
        B("Dinitrogen monoxide", 0.0006, "kg", "air", "IPCC Tier 1, direct + indirect"),
     ], per=0.62),
    A("cotton ginning and ring spinning", "cotton yarn, ring-spun, Ne 30", "kg", "IN",
      "Ginning (cottonseed co-product allocated economically, about 85% to lint) and ring spinning.", [
        F("seed cotton production, conventional, irrigated, India", 0.62),
        T("market for electricity, medium voltage", 2.3, "kWh", "IN", "electricity, medium voltage"),
        T(LORRY4, 0.184, "tkm", "RoW", "transport, freight, lorry 16-32 metric ton, EURO4", "gin to spinner, 800 km"),
     ], per=0.205),
    A("knitting of cotton single jersey", "cotton single jersey, greige", "kg", "BD", "Circular knitting.", [
        F("cotton ginning and ring spinning", 0.205),
        T("market for electricity, medium voltage", 0.9, "kWh", "BD", "electricity, medium voltage"),
        T(SHIP, 0.31, "tkm", "GLO", "transport, freight, sea, container ship", "India to Bangladesh, 1,500 km"),
     ], per=0.20),
    A("dyeing and finishing of cotton jersey", "cotton single jersey, dyed and finished", "kg", "BD",
      "Scouring, bleaching, reactive dyeing, washing, finishing. Steam from coal and gas boilers; effluent treatment assumed.", [
        F("knitting of cotton single jersey", 0.20),
        T("market for heat, district or industrial, other than natural gas", 9, "MJ", "RoW", "heat, district or industrial, other than natural gas", "coal boiler share"),
        T(HEAT_NG, 9, "MJ", "RoW", "heat, district or industrial, natural gas", "gas boiler share"),
        T("market for electricity, medium voltage", 0.8, "kWh", "BD", "electricity, medium voltage"),
        T("market for tap water", 95, "kg", "RoW", "tap water", "liquor ratio about 1:8 plus rinses"),
        T("market for chemical, organic", 0.015, "kg", "GLO", "chemical, organic", "proxy for dyes and auxiliaries"),
        T("market for sodium chloride, powder", 0.030, "kg", "GLO", "sodium chloride, powder", "dyeing salt"),
        T("market for wastewater, average", 0.095, "m3", "RoW", "wastewater, average", WASTE_NOTE),
     ], per=0.20),
    A("cut-make-trim of cotton T-shirt", "cotton T-shirt, 180 g", "unit", "BD", "Cutting (10% offcuts), sewing, labelling, polybag.", [
        F("dyeing and finishing of cotton jersey", 0.20),
        T("market for electricity, medium voltage", 0.6, "kWh", "BD", "electricity, medium voltage"),
        T("market for packaging film, low density polyethylene", 0.005, "kg", "GLO", "packaging film, low density polyethylene", "polybag"),
        W("market for waste textile, soiled", 0.020, "RoW", "waste textile, soiled", "cutting offcuts"),
     ]),
    A("distribution and retail of T-shirt", "cotton T-shirt, at retail", "unit", "DE", "Sea freight Chittagong-Hamburg, truck to stores.", [
        F("cut-make-trim of cotton T-shirt", 1),
        T(SHIP, 3.2, "tkm", "GLO", "transport, freight, sea, container ship", "16,000 km x 0.2 kg"),
        T(LORRY, 0.10, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "500 km"),
        T("market for electricity, low voltage", 0.15, "kWh", "DE", "electricity, low voltage", "store energy allocated by floor space"),
     ]),
    A("T-shirt laundry, 25 washes and 10 tumble-dry cycles", "T-shirt laundry service, 50 wears", "unit", "DE",
      "40 C washes in shared loads; vented dryer for 10 of 25 washes; no ironing.", [
        T("market for electricity, low voltage", 2.8, "kWh", "DE", "electricity, low voltage", "1.0 kWh washing + 1.8 kWh drying"),
        T("market for tap water", 52, "kg", EWOCH, "tap water"),
        T("market for soap", 0.10, "kg", "GLO", "soap", "proxy for laundry detergent"),
        T("market for wastewater, average", 0.052, "m3", EWOCH, "wastewater, average", WASTE_NOTE),
     ]),
    A("cotton T-shirt, use and end-of-life", "cotton T-shirt, worn 50 times (functional unit)", "unit", "DE",
      "Functional unit. 25% collected for reuse/downcycling (cut-off, leaves the system burden-free); remainder incinerated with residual waste.", [
        F("distribution and retail of T-shirt", 1),
        F("T-shirt laundry, 25 washes and 10 tumble-dry cycles", 1),
        W("market for municipal solid waste", 0.120, "DE", "municipal solid waste", "residual textiles, incinerated"),
     ]),
])

# ---------------------------------------------------------------- 3 PET
case(n=3, slug="lca-portfolio-pet-water-bottle", short="PET water bottle",
     src="Portfolio case 3 (illustrative); PlasticsEurope eco-profiles; ecoinvent",
     fu=[("bottled mineral water, 500 ml, consumed (functional unit)", "Packaging and delivery of 500 ml still mineral water, chilled and consumed once (virgin PET reference)")],
     activities=[
    A("PET bottle production, injection stretch blow moulding", "PET bottle, 500 ml, empty", "unit", "DE", "14 g virgin bottle-grade PET (reference case; EU SUPD requires 25% recycled content from 2025).", [
        T("market for polyethylene terephthalate, granulate, bottle grade", 0.014, "kg", "GLO", "polyethylene terephthalate, granulate, bottle grade"),
        T("market for electricity, medium voltage", 0.055, "kWh", "DE", "electricity, medium voltage", "preform and blow moulding"),
        T(LORRY, 0.007, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "resin, 500 km"),
     ]),
    A("closure and label production", "HDPE tethered cap and PP label", "unit", "DE", "2 g HDPE cap, 0.5 g PP label.", [
        T("market for polyethylene, high density, granulate", 0.002, "kg", "GLO", "polyethylene, high density, granulate"),
        T("market for injection moulding", 0.002, "kg", "GLO", "injection moulding"),
        T("market for polypropylene, granulate", 0.0005, "kg", "GLO", "polypropylene, granulate"),
        T(LORRY, 0.00075, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "300 km"),
     ]),
    A("mineral water treatment and bottling", "mineral water, 500 ml, bottled", "unit", "DE", "Filtration, filling, capping, labelling, shrink-wrapping.", [
        F("PET bottle production, injection stretch blow moulding", 1),
        F("closure and label production", 1),
        B("Water, well, in ground", 0.00075, "m3", "natural resource::in water", "0.5 L product + 0.25 L process water"),
        T("market for electricity, medium voltage", 0.01, "kWh", "DE", "electricity, medium voltage"),
        T("market for packaging film, low density polyethylene", 0.0004, "kg", "GLO", "packaging film, low density polyethylene", "shrink film share"),
     ]),
    A("distribution of bottled water to retail", "bottled water, 500 ml, at retail", "unit", "DE", "300 km one way, full truck loads.", [
        F("mineral water treatment and bottling", 1),
        T(LORRY, 0.16, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "300 km x 0.53 kg incl. secondary packaging"),
     ]),
    A("retail chilling of bottled water", "bottled water, 500 ml, chilled, at retail", "unit", "DE", "50% of bottles chilled for 2 days.", [
        F("distribution of bottled water to retail", 1),
        T("market for electricity, low voltage", 0.02, "kWh", "DE", "electricity, low voltage"),
        B("Ethane, 1,1,1,2-tetrafluoro-, HFC-134a", 0.000001, "kg", "air", "refrigerant leakage, illustrative"),
     ]),
    A("bottled water, consumption and end-of-life", "bottled mineral water, 500 ml, consumed (functional unit)", "unit", "DE",
      "Functional unit. 60% collected for recycling (cut-off), 25% incinerated, 15% landfilled or littered (litter not modelled as a flow).", [
        F("retail chilling of bottled water", 1),
        W("market for waste polyethylene terephthalate, for recycling, sorted", 0.0099, "GLO", "waste polyethylene terephthalate, for recycling, sorted", "60% collected"),
        W("market for municipal solid waste", 0.0041, "DE", "municipal solid waste", "incinerated share"),
        W("market for waste plastic, mixture", 0.0025, "RoW", "waste plastic, mixture", "landfill share"),
     ]),
])

# ---------------------------------------------------------------- 4 can
case(n=4, slug="lca-portfolio-aluminium-can", short="Aluminium can",
     src="Portfolio case 4 (illustrative); International Aluminium Institute; European Aluminium",
     fu=[("canned soft drink, 330 ml, consumed (functional unit)", "Packaging of 330 ml carbonated soft drink in one aluminium can (100% primary aluminium baseline)")],
     activities=[
    A("aluminium production, primary, ingot, global average", "aluminium, primary, ingot", "kg", "GLO",
      "Hall-Heroult smelting, about 14 kWh/kg on a global-average grid (about 0.8 kg CO2e/kWh). Bauxite residue is inside the alumina background dataset.", [
        T("market for aluminium oxide, metallurgical", 1.93, "kg", "GLO", "aluminium oxide, metallurgical"),
        T("market group for electricity, high voltage", 14, "kWh", "GLO", "electricity, high voltage"),
        T("market for anode, prebake, for aluminium electrolysis", 0.42, "kg", "GLO", "anode, prebake, for aluminium electrolysis"),
        B("Carbon dioxide, fossil", 1.55, "kg", "air", "anode oxidation"),
        B("Methane, tetrafluoro-, R-14", 0.00003, "kg", "air", "anode effects, IAI averages (order of magnitude)"),
     ]),
    A("casting and rolling of can-body sheet", "aluminium can-body sheet", "kg", "RER", "Casting, hot and cold rolling; process scrap remelted in-house.", [
        F("aluminium production, primary, ingot, global average", 1.015),
        T(HEAT_NG, 9.2, "MJ", EWOCH, "heat, district or industrial, natural gas"),
        T("market for electricity, medium voltage", 0.77, "kWh", "RER", "electricity, medium voltage"),
     ]),
    A("beverage can production, 330 ml", "aluminium beverage can, 330 ml, empty", "unit", "DE", "Cupping, drawing and ironing, washing, internal coating, printing, necking; 13 g can and end.", [
        F("casting and rolling of can-body sheet", 0.013),
        T("market for electricity, medium voltage", 0.02, "kWh", "DE", "electricity, medium voltage"),
        T(HEAT_NG, 0.08, "MJ", EWOCH, "heat, district or industrial, natural gas", "curing ovens"),
        T("market for epoxy resin, liquid", 0.0002, "kg", "RER", "epoxy resin, liquid", "proxy for internal coating and inks"),
        T(LORRY, 0.0026, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "200 km to filler"),
     ]),
    A("filling of beverage cans", "soft drink can, filled and seamed", "unit", "DE", "Beverage itself excluded.", [
        F("beverage can production, 330 ml", 1),
        T("market for electricity, medium voltage", 0.005, "kWh", "DE", "electricity, medium voltage"),
        T("market for tap water", 0.25, "kg", EWOCH, "tap water"),
        T("market for carbon dioxide, liquid", 0.002, "kg", "RER", "carbon dioxide, liquid", "carbonation share, illustrative"),
     ]),
    A("distribution and chilling of canned drinks", "soft drink can, chilled, at retail", "unit", "DE", "300 km truck; 50% chilled.", [
        F("filling of beverage cans", 1),
        T(LORRY, 0.11, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "300 km x 0.36 kg"),
        T("market for electricity, low voltage", 0.01, "kWh", "DE", "electricity, low voltage"),
     ]),
    A("canned soft drink, consumption and end-of-life", "canned soft drink, 330 ml, consumed (functional unit)", "unit", "DE",
      "Functional unit. 75% of cans collected for recycling (cut-off: remelting carried by the next product).", [
        F("distribution and chilling of canned drinks", 1),
        W("market for scrap aluminium", 0.00975, "Europe without Switzerland", "scrap aluminium", "75% collected"),
        W("market for municipal solid waste", 0.00325, "DE", "municipal solid waste", "25% not collected"),
     ]),
])

# ---------------------------------------------------------------- 5 box
case(n=5, slug="lca-portfolio-ecommerce-box", short="E-commerce cardboard box",
     src="Portfolio case 5 (illustrative); FEFCO/Cepi European database for corrugated board",
     fu=[("e-commerce order packaging, delivered and disposed (functional unit)", "Packaging to protect and deliver one 1 kg e-commerce order to a household in Germany (oversized box baseline)")],
     activities=[
    A("containerboard production, 50% recycled fibre", "containerboard, mixed furnish", "kg", "DE", "Kraftliner and recycled fluting; mill rejects about 6% of furnish.", [
        T("market for wood chips, wet, measured as dry mass", 0.24, "kg", "RER", "wood chips, wet, measured as dry mass", "virgin fibre"),
        T("market for waste paper, sorted", 0.26, "kg", "GLO", "waste paper, sorted", "recovered paper"),
        T(HEAT_NG, 2.6, "MJ", EWOCH, "heat, district or industrial, natural gas"),
        T("market for heat, district or industrial, other than natural gas", 2.6, "MJ", EWOCH, "heat, district or industrial, other than natural gas", "biomass boiler share"),
        T("market for electricity, medium voltage", 0.18, "kWh", "DE", "electricity, medium voltage"),
        B("Water, river", 0.009, "m3", "natural resource::in water", "evaporation losses"),
        B("Occupation, forest, intensive", 1.1, "m2a", "natural resource::land", "managed forest for virgin fibre"),
     ], per=0.47),
    A("corrugated box production, single wall, printed", "corrugated board box, single wall", "kg", "DE", "Corrugating, die-cutting, flexo printing; trim scrap (20 g) returned to recycling.", [
        F("containerboard production, 50% recycled fibre", 0.47),
        T("market for maize starch", 0.009, "kg", "GLO", "maize starch", "corrugating adhesive"),
        T("market for electricity, medium voltage", 0.08, "kWh", "DE", "electricity, medium voltage"),
        T(HEAT_NG, 0.6, "MJ", EWOCH, "heat, district or industrial, natural gas"),
     ], per=0.45),
    A("air-pillow void fill production", "LDPE air-pillow void fill", "kg", "RER", "Film inflated at the fulfilment centre.", [
        T("market for packaging film, low density polyethylene", 1.0, "kg", "GLO", "packaging film, low density polyethylene"),
     ]),
    A("transport of boxes to fulfilment centre", "corrugated board box, at fulfilment centre", "kg", "DE", "Flat-packed boxes, 250 km.", [
        F("corrugated box production, single wall, printed", 1.0),
        T(LORRY, 0.25, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "250 km per kg box"),
     ]),
    A("parcel packing and delivery to household", "parcel with 1 kg order, delivered", "unit", "DE",
      "Delivery by van allocated by parcel volume: an oversized parcel occupies 50% more van space. 0.2 tkm is the volume-allocated equivalent.", [
        F("transport of boxes to fulfilment centre", 0.45),
        F("air-pillow void fill production", 0.012),
        T("market for transport, freight, light commercial vehicle", 0.2, "tkm", EWOCH, "transport, freight, light commercial vehicle", "volume-allocated last mile and line haul (illustrative)"),
     ]),
    A("e-commerce packaging, end-of-life", "e-commerce order packaging, delivered and disposed (functional unit)", "unit", "DE",
      "Functional unit. 85% of the box recycled (cut-off); rest of box and all void fill incinerated with residual waste.", [
        F("parcel packing and delivery to household", 1),
        W("market for waste paperboard", 0.383, "DE", "waste paperboard", "to recycling"),
        W("market for municipal solid waste", 0.079, "DE", "municipal solid waste", "67 g box + 12 g void fill"),
     ]),
])

# ---------------------------------------------------------------- 6 flexible pouch
case(n=6, slug="lca-portfolio-flexible-coffee-pouch", short="Flexible food packaging",
     src="Portfolio case 6 (illustrative); PlasticsEurope; CEFLEX D4ACE",
     fu=[("ground coffee, 250 g, packed, delivered and pack disposed (functional unit)", "Packaging to protect and deliver 250 g ground coffee with a 12-month shelf life (multilayer PET/Al/PE baseline); coffee itself excluded except the share lost through packaging failure")],
     activities=[
    A("multilayer laminate production, PET/Al/PE", "printed multilayer laminate", "kg", "RER", "Reverse-printed PET, 9 micrometre aluminium foil and LDPE sealant, solvent-based lamination; includes 8% converting waste.", [
        T("market for polyethylene terephthalate, granulate, amorphous", 0.0033, "kg", "GLO", "polyethylene terephthalate, granulate, amorphous"),
        T("market for aluminium, wrought alloy", 0.0022, "kg", "GLO", "aluminium, wrought alloy"),
        T("market for sheet rolling, aluminium", 0.0022, "kg", "GLO", "sheet rolling, aluminium", "foil rolling"),
        T("market for packaging film, low density polyethylene", 0.006, "kg", "GLO", "packaging film, low density polyethylene"),
        T("market for extrusion, plastic film", 0.0033, "kg", "GLO", "extrusion, plastic film", "PET film"),
        T("market for chemical, organic", 0.0005, "kg", "GLO", "chemical, organic", "proxy for inks and adhesives"),
        T("market for electricity, medium voltage", 0.012, "kWh", "DE", "electricity, medium voltage"),
        T(HEAT_NG, 0.02, "MJ", EWOCH, "heat, district or industrial, natural gas", "drying and curing"),
     ], per=0.012),
    A("stand-up pouch making with degassing valve", "coffee pouch, 250 g, empty", "unit", "DE", "11 g pouch; 1 g converting waste.", [
        F("multilayer laminate production, PET/Al/PE", 0.012),
        T("market for polyethylene, low density, granulate", 0.0005, "kg", "GLO", "polyethylene, low density, granulate", "valve"),
        T("market for electricity, medium voltage", 0.003, "kWh", "DE", "electricity, medium voltage"),
        W("market for waste plastic, mixture", 0.001, "RoW", "waste plastic, mixture", "converting waste"),
     ]),
    A("coffee filling and sealing under nitrogen", "ground coffee, 250 g, packed", "unit", "DE", "Coffee production outside the boundary (only the share lost is included downstream).", [
        F("stand-up pouch making with degassing valve", 1),
        T("market for nitrogen, liquid", 0.0015, "kg", "RER", "nitrogen, liquid"),
        T("market for electricity, medium voltage", 0.005, "kWh", "DE", "electricity, medium voltage"),
     ]),
    A("distribution of packed coffee", "ground coffee, 250 g, packed, at retail", "unit", "DE", "400 km truck.", [
        F("coffee filling and sealing under nitrogen", 1),
        T(LORRY, 0.108, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "400 km x 0.27 kg"),
     ]),
    A("coffee lost through packaging performance", "coffee loss attributable to packaging, per pack", "unit", "DE", "1% of 250 g roasted coffee lost through barrier or seal failure (illustrative).", [
        T("market for coffee, green bean", 0.003, "kg", "GLO", "coffee, green bean", "2.5 g roasted coffee = about 3 g green bean; roasting excluded"),
        W("market for biowaste", 0.0025, "RoW", "biowaste"),
     ]),
    A("coffee pack, use and end-of-life", "ground coffee, 250 g, packed, delivered and pack disposed (functional unit)", "unit", "DE",
      "Functional unit. Multilayer pouch not recyclable in practice: incinerated with residual waste.", [
        F("distribution of packed coffee", 1),
        F("coffee lost through packaging performance", 1),
        W("market for municipal solid waste", 0.011, "DE", "municipal solid waste"),
     ]),
])

# ---------------------------------------------------------------- 7 EV battery
case(n=7, slug="lca-portfolio-ev-battery", short="EV battery",
     src="Portfolio case 7 (illustrative); Dai et al. 2019 (GREET); Batteries Regulation (EU) 2023/1542",
     fu=[("traction battery pack, 60 kWh, life cycle (functional unit)", "One 60 kWh NMC811 traction battery pack over a 200,000 km first vehicle life in Europe (virgin materials, East Asian cell production)")],
     activities=[
    A("NMC811 cathode active material production", "cathode active material, NMC811", "kg", "CN", "Co-precipitation of precursor and lithiation/calcination on a coal-heavy grid.", [
        T("market for lithium hydroxide, battery grade", 47, "kg", "GLO", "lithium hydroxide, battery grade", "about 7.8 kg Li"),
        T("market for nickel sulfate", 202, "kg", "GLO", "nickel sulfate", "45 kg Ni"),
        T("market for cobalt sulfate", 27, "kg", "GLO", "cobalt sulfate", "5.6 kg Co"),
        T("market for manganese sulfate", 16, "kg", "GLO", "manganese sulfate", "5.3 kg Mn"),
        T("market for sodium hydroxide, without water, in 50% solution state", 80, "kg", "GLO", "sodium hydroxide, without water, in 50% solution state"),
        T("market for ammonia, anhydrous, liquid", 4, "kg", "RoW", "ammonia, anhydrous, liquid"),
        T("market for electricity, medium voltage", 1200, "kWh", "CN", "electricity, medium voltage"),
        T(HEAT_NG, 6000, "MJ", "RoW", "heat, district or industrial, natural gas"),
     ], per=110),
    A("graphite anode material production", "anode active material, graphite", "kg", "CN", "50% synthetic graphite.", [
        T("market for graphite, battery grade", 77, "kg", "GLO", "graphite, battery grade", "incl. 10% losses"),
        T("market for electricity, medium voltage", 200, "kWh", "CN", "electricity, medium voltage"),
     ], per=70),
    A("lithium-ion cell manufacturing, NMC811", "lithium-ion cell, NMC811", "kg", "CN", "Electrode coating and drying, dry-room assembly, formation; about 25 kWh electricity per kWh cell capacity.", [
        F("NMC811 cathode active material production", 110),
        F("graphite anode material production", 70),
        T("market for lithium hexafluorophosphate", 4, "kg", "GLO", "lithium hexafluorophosphate", "electrolyte salt"),
        T("market for ethylene carbonate", 26, "kg", "GLO", "ethylene carbonate", "electrolyte solvent proxy"),
        T("market for polyethylene, high density, granulate", 6, "kg", "GLO", "polyethylene, high density, granulate", "separator"),
        T("market for extrusion, plastic film", 6, "kg", "GLO", "extrusion, plastic film", "separator"),
        T("market for aluminium, wrought alloy", 15, "kg", "GLO", "aluminium, wrought alloy", "cathode foil and cell cans"),
        T("market for copper, cathode", 20, "kg", "GLO", "copper, cathode", "anode foil"),
        T("market for N-methyl-2-pyrrolidone", 3, "kg", "GLO", "N-methyl-2-pyrrolidone", "solvent losses"),
        T("market for electricity, medium voltage", 1500, "kWh", "CN", "electricity, medium voltage"),
        T(HEAT_NG, 1000, "MJ", "RoW", "heat, district or industrial, natural gas"),
     ], per=260),
    A("battery pack assembly, 60 kWh", "battery pack, NMC811, 60 kWh", "unit", "CN", "Modules, cooling, battery management system and aluminium housing; pack mass 400 kg.", [
        F("lithium-ion cell manufacturing, NMC811", 260),
        T("market for aluminium, wrought alloy", 80, "kg", "GLO", "aluminium, wrought alloy", "housing"),
        T("market for copper, cathode", 10, "kg", "GLO", "copper, cathode", "busbars and wiring"),
        T("market for steel, low-alloyed", 30, "kg", "GLO", "steel, low-alloyed"),
        T("market for electronics, for control units", 2, "kg", "GLO", "electronics, for control units", "battery management system"),
        T("market for electricity, medium voltage", 80, "kWh", "CN", "electricity, medium voltage"),
     ]),
    A("shipping of battery pack to Europe", "battery pack, NMC811, 60 kWh, at vehicle plant", "unit", "RER", "Sea freight and trucking.", [
        F("battery pack assembly, 60 kWh", 1),
        T(SHIP, 8000, "tkm", "GLO", "transport, freight, sea, container ship", "20,000 km x 0.4 t"),
        T(LORRY, 200, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "500 km"),
     ]),
    A("battery-attributable charging losses, 200,000 km", "battery charging losses, first vehicle life", "unit", "RER", "About 10% of 34,000 kWh traction energy; EU grid.", [
        T("market group for electricity, low voltage", 3400, "kWh", "RER", "electricity, low voltage"),
     ]),
    A("battery pack collection and hydrometallurgical recycling", "spent battery pack recycling service", "unit", "RER", "Collection, discharge, dismantling, black mass and leaching; recovery in line with 2031 targets; no credits (cut-off).", [
        T(LORRY, 200, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "500 km"),
        T("market for electricity, medium voltage", 300, "kWh", "RER", "electricity, medium voltage"),
        T("market for sulfuric acid", 120, "kg", "RER", "sulfuric acid"),
        T("market for hydrogen peroxide, without water, in 50% solution state", 25, "kg", "RER", "hydrogen peroxide, without water, in 50% solution state"),
        T(HEAT_NG, 500, "MJ", EWOCH, "heat, district or industrial, natural gas"),
     ]),
    A("traction battery pack, life cycle", "traction battery pack, 60 kWh, life cycle (functional unit)", "unit", "RER", "Functional unit: production, use-phase losses and end-of-life of one pack.", [
        F("shipping of battery pack to Europe", 1),
        F("battery-attributable charging losses, 200,000 km", 1),
        F("battery pack collection and hydrometallurgical recycling", 1),
     ]),
])

# ---------------------------------------------------------------- 8 smartphone
case(n=8, slug="lca-portfolio-smartphone", short="Smartphone",
     src="Portfolio case 8 (illustrative); Clement et al. 2020; manufacturer environmental reports",
     fu=[("smartphone service, one user, one year (functional unit)", "Providing smartphone service to one user for one year in Germany (new phone used three years)")],
     activities=[
    A("smartphone mainboard and integrated circuits production", "smartphone mainboard, populated", "unit", "GLO", "Logic and memory ICs and printed wiring board per phone.", [
        T("market for integrated circuit, logic type", 0.003, "kg", "GLO", "integrated circuit, logic type"),
        T("market for integrated circuit, memory type", 0.002, "kg", "GLO", "integrated circuit, memory type"),
        T("market for printed wiring board, surface mounted, unspecified, Pb free", 0.012, "kg", "GLO", "printed wiring board, surface mounted, unspecified, Pb free"),
     ]),
    A("smartphone display and battery production", "smartphone display and battery set", "unit", "GLO", "6.1 inch display and 4,000 mAh cell.", [
        T("market for liquid crystal display, unmounted, mobile device", 0.030, "kg", "GLO", "liquid crystal display, unmounted, mobile device", "proxy for OLED module"),
        T("market for battery cell, Li-ion, NMC111", 0.045, "kg", "GLO", "battery cell, Li-ion, NMC111", "proxy for phone cell chemistry"),
     ]),
    A("smartphone final assembly", "smartphone, 180 g", "unit", "CN", "Assembly, test and software flashing.", [
        F("smartphone mainboard and integrated circuits production", 1),
        F("smartphone display and battery production", 1),
        T("market for aluminium, wrought alloy", 0.025, "kg", "GLO", "aluminium, wrought alloy", "frame"),
        T("market for flat glass, uncoated", 0.040, "kg", "RoW", "flat glass, uncoated", "cover glass proxy"),
        T("market for polycarbonate", 0.025, "kg", "GLO", "polycarbonate"),
        T("market for copper, cathode", 0.005, "kg", "GLO", "copper, cathode"),
        T("market for gold", 0.000035, "kg", "GLO", "gold", "35 mg"),
        T("market for tin", 0.0005, "kg", "GLO", "tin"),
        T("market for electricity, medium voltage", 10, "kWh", "CN", "electricity, medium voltage"),
     ]),
    A("smartphone retail packaging production", "smartphone retail box", "unit", "CN", "Fibre-based box, no charger.", [
        T("market for folding boxboard carton", 0.12, "kg", "RER", "folding boxboard carton"),
     ]),
    A("air freight and distribution of smartphone", "smartphone, packed, at retail, Germany", "unit", "DE", "Air freight 9,000 km; truck 500 km.", [
        F("smartphone final assembly", 1),
        F("smartphone retail packaging production", 1),
        T("market for transport, freight, aircraft, long haul", 3.0, "tkm", "GLO", "transport, freight, aircraft, long haul"),
        T(LORRY, 0.165, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6"),
     ]),
    A("smartphone charging, one year", "smartphone charging, 1 year", "unit", "DE", "Daily charging, 85% charger efficiency; network and data-centre energy excluded.", [
        T("market for electricity, low voltage", 4.0, "kWh", "DE", "electricity, low voltage"),
     ]),
    A("smartphone service, one year", "smartphone service, one user, one year (functional unit)", "unit", "DE",
      "Functional unit: one third of a phone used three years, one year of charging, one third of end-of-life.", [
        F("air freight and distribution of smartphone", 1 / 3),
        F("smartphone charging, one year", 1),
        W("market for used mobile phone", 0.06, "GLO", "used mobile phone", "one third of 180 g"),
     ]),
])

# ---------------------------------------------------------------- 9 municipal plastic recycling
case(n=9, slug="lca-portfolio-plastic-recycling-system", short="Plastic recycling system",
     src="Portfolio case 9 (illustrative); PlasticsEurope; Eurostat; waste-management LCAs",
     fu=[("household plastic packaging waste, 1 t, managed (functional unit)", "Management of 1 t household plastic packaging waste by kerbside collection, sorting and mechanical recycling, with system-expansion credits")],
     activities=[
    A("kerbside collection of plastic packaging waste", "plastic packaging waste, collected", "kg", "DE", "Separate collection, about 13 L diesel per tonne.", [
        T("market for transport, municipal waste collection, lorry 21 metric ton", 30, "tkm", "RoW", "transport, municipal waste collection, lorry 21 metric ton", "per tonne collected"),
     ], per=1000),
    A("sorting of plastic packaging waste at MRF", "sorted plastic bales", "kg", "DE", "NIR and ballistic sorting; 75% to polymer streams, 25% residues incinerated.", [
        F("kerbside collection of plastic packaging waste", 1000),
        T("market for electricity, medium voltage", 60, "kWh", "DE", "electricity, medium voltage"),
        T("market for steel, low-alloyed", 0.5, "kg", "GLO", "steel, low-alloyed", "baling wire"),
        W("market for waste plastic, mixture", 250, "DE", "waste plastic, mixture", "sorting residues to incineration"),
     ], per=750),
    A("transport of plastic bales to reprocessor", "sorted plastic bales, at reprocessor", "kg", "DE", "300 km.", [
        F("sorting of plastic packaging waste at MRF", 750),
        T(LORRY, 225, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6"),
     ], per=750),
    A("mechanical recycling of plastic bales", "plastic recyclate, pellets", "kg", "DE", "Shredding, washing, flotation, extrusion; 75% yield; residues incinerated.", [
        F("transport of plastic bales to reprocessor", 750),
        T("market for electricity, medium voltage", 600, "kWh", "DE", "electricity, medium voltage"),
        T(HEAT_NG, 2340, "MJ", EWOCH, "heat, district or industrial, natural gas"),
        T("market for tap water", 3500, "kg", EWOCH, "tap water", "washing"),
        T("market for sodium hydroxide, without water, in 50% solution state", 5, "kg", "GLO", "sodium hydroxide, without water, in 50% solution state"),
        T("market for wastewater, average", 3.5, "m3", EWOCH, "wastewater, average", WASTE_NOTE),
        W("market for waste plastic, mixture", 190, "DE", "waste plastic, mixture", "reprocessing losses to incineration"),
     ], per=560),
    A("plastic packaging waste management, 1 t", "household plastic packaging waste, 1 t, managed (functional unit)", "unit", "DE",
      "Functional unit. System expansion: 560 kg recyclate credited as avoided virgin polymer (substitution factor 0.8) and incineration energy credited as avoided grid electricity and heat. Negative amounts are credits.", [
        F("mechanical recycling of plastic bales", 560),
        T("market for polyethylene, high density, granulate", -448, "kg", "GLO", "polyethylene, high density, granulate", "avoided virgin polymer: 560 kg x 0.8; proxy for the PE/PP/PET mix"),
        T("market for electricity, medium voltage", -400, "kWh", "DE", "electricity, medium voltage", "avoided grid electricity from incinerating 440 kg residues"),
        T(HEAT_NG, -2700, "MJ", EWOCH, "heat, district or industrial, natural gas", "avoided heat from incineration"),
     ]),
])

# ---------------------------------------------------------------- 10 coffee cup
case(n=10, slug="lca-portfolio-coffee-cup", short="Coffee cup system",
     src="Portfolio case 10 (illustrative); UNEP 2021; Sinkko et al. 2024 (JRC)",
     fu=[("hot drink served in single-use paper cup (functional unit)", "Serving one 350 ml hot drink in a single-use PE-lined paper cup with PS lid"),
         ("hot drink served in reusable PP cup, 50 uses (functional unit)", "Serving one 350 ml hot drink in a reusable PP cup used 50 times and washed in a home dishwasher")],
     activities=[
    A("paper cup production, PE-lined, printed", "paper cup, 350 ml", "unit", "RER", "11 g cupstock board with 0.6 g PE extrusion coating.", [
        T("market for liquid packaging board", 0.011, "kg", "GLO", "liquid packaging board", "food-contact virgin board proxy"),
        T("market for polyethylene, low density, granulate", 0.0006, "kg", "GLO", "polyethylene, low density, granulate"),
        T("market for electricity, medium voltage", 0.003, "kWh", "RER", "electricity, medium voltage"),
        T(LORRY, 0.0088, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "board to converter, 800 km"),
     ]),
    A("polystyrene lid production", "polystyrene cup lid", "unit", "RER", "3 g thermoformed PS lid.", [
        T("market for polystyrene, high impact", 0.003, "kg", "GLO", "polystyrene, high impact"),
        T("market for thermoforming, with calendering", 0.003, "kg", "GLO", "thermoforming, with calendering"),
     ]),
    A("distribution of cups and lids to cafes", "single-use cup and lid, at cafe", "unit", "DE", "600 km.", [
        F("paper cup production, PE-lined, printed", 1),
        F("polystyrene lid production", 1),
        T(LORRY, 0.009, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6"),
     ]),
    A("hot drink served in single-use paper cup", "hot drink served in single-use paper cup (functional unit)", "unit", "DE",
      "Functional unit 1. Cup and lid 65% incinerated, 30% landfilled, 5% specialist recycling (not modelled).", [
        F("distribution of cups and lids to cafes", 1),
        W("market for municipal solid waste", 0.0095, "DE", "municipal solid waste", "incinerated share"),
        W("market for waste paperboard", 0.004, "DE", "waste paperboard", "landfilled share (proxy route)"),
     ]),
    A("reusable polypropylene cup production", "reusable PP cup with silicone lid", "unit", "RER", "100 g PP cup, injection moulded.", [
        T("market for polypropylene, granulate", 0.090, "kg", "GLO", "polypropylene, granulate"),
        T("market for injection moulding", 0.090, "kg", "GLO", "injection moulding"),
        T("market for silicone product", 0.010, "kg", "RER", "silicone product", "lid"),
        T(LORRY, 0.06, "tkm", "RER", "transport, freight, lorry 16-32 metric ton, EURO6", "600 km"),
     ]),
    A("dishwashing of reusable cup, per use", "reusable cup washed once", "unit", "DE", "Home dishwasher, shared load.", [
        T("market for electricity, low voltage", 0.04, "kWh", "DE", "electricity, low voltage", "incl. water heating"),
        T("market for tap water", 0.3, "kg", EWOCH, "tap water"),
        T("market for soap", 0.001, "kg", "GLO", "soap", "detergent proxy"),
     ]),
    A("hot drink served in reusable PP cup, 50 uses", "hot drink served in reusable PP cup, 50 uses (functional unit)", "unit", "DE",
      "Functional unit 2. One fiftieth of the cup and its end-of-life plus one wash.", [
        F("reusable polypropylene cup production", 0.02),
        F("dishwashing of reusable cup, per use", 1),
        W("market for municipal solid waste", 0.002, "DE", "municipal solid waste", "100 g cup / 50 uses"),
     ]),
])

# ---------------------------------------------------------------- 11 IMTA (published report data)
_IMTA_DB = "piscentool-simapro-background"
_imta_src = "INTEGRATE deliverable PI05#3 (IPMA & CTAQUA 2020), Table 4 and Table 5, scaled to 1 t"


def _imta(code, label, loc, comment, feed, feed_c, fry, spat, sea, land, n, p):
    ex = [
        T("compound fish feed", feed, "kg", loc, "compound fish feed", feed_c + "; " + _imta_src, db=_IMTA_DB),
        T("fish fry / fingerlings", fry, "kg", loc, "fish fry / fingerlings", "Piscentool used a carp-fry proxy; " + _imta_src, db=_IMTA_DB),
    ]
    if spat:
        ex.append(T("oyster spat (flesh)", spat, "kg", loc, "oyster spat", _imta_src, db=_IMTA_DB))
    ex += [B("Water, salt, ocean", sea, "m3", "natural resource::in water", "seawater pumped or tidal; matches Water consumption in Annex 1"),
           B("Occupation, water bodies, artificial", land, "m2a", "natural resource::land", "farm area x pond share x cycle length (report allocation rule)"),
           B("Nitrogen", n, "kg", "water::ocean", "net N to water from nutrient balance (Cho & Kaushik 1990); negative = net uptake")]
    if p:
        ex.append(B("Phosphorus", p, "kg", "water::ocean", "net P to water from nutrient balance; negative = net uptake"))
    return A(label, label + " (functional unit)", "t", loc, comment, ex)


case(n=11, slug="imta-integrate-lci", short="IMTA aquaculture",
     src="INTEGRATE deliverable PI05#3 (IPMA & CTAQUA 2020); repository malleshkomal/Life-cycle-assessment-of-Integrated-Multi-Trophical-Aquaculture-",
     fu=[("SI-POLY, 1 t aquatic product at farm gate (functional unit)", "Semi-intensive fishpond polyculture, 1 t fish at farm gate, one cycle (baseline)"),
         ("SI-IMTA, 1 t aquatic product at farm gate (functional unit)", "Semi-intensive pond IMTA, 1 t fish + oyster flesh at farm gate, one cycle"),
         ("SE-IMTA, 1 t aquatic product at farm gate (functional unit)", "Semi-extensive pond IMTA, 1 t fish + oyster flesh at farm gate, one cycle")],
     activities=[
    _imta("si-poly", "SI-POLY, 1 t aquatic product at farm gate", "PT",
          "Semi-intensive fishpond polyculture (meagre + gilthead seabream), IPMA Olhao, May 2017-Jul 2019. Reference flow 6,137 kg fish per pond; scaling 0.163. Fish only, no co-products.",
          1788.3331, "42% protein, 1.4% P", 14.8281, 0, 195822.7147, 2288.8399, 95.9263, 20.9712),
    _imta("si-imta", "SI-IMTA, 1 t aquatic product at farm gate", "PT",
          "Semi-intensive pond IMTA (meagre, white seabream, mullet + oysters + Ulva), IPMA Olhao, May-Oct 2017. Output 894.2 kg fish + 105.8 kg oyster flesh per t; 995.9 kg macroalgae is a co-product outside the functional unit (no allocation, no credit).",
          1536.2083, "42% protein, 1.4% P", 550.8544, 4.4752, 82270.1383, 959.3372, 54.6786, 14.6461),
    _imta("se-imta", "SE-IMTA, 1 t aquatic product at farm gate", "ES",
          "Semi-extensive pond IMTA (gilthead seabream + oysters, macroalgae pond), Estero Natural, Cadiz, Jan-Nov 2019, tidal exchange. Output 408.8 kg fish + 591.2 kg oyster flesh per t; 222,642 kg macroalgae co-product outside the functional unit. Net P to water is 0 and is omitted.",
          559.7484, "40% protein, 1.3% P", 283.0189, 90.566, 45188.6792, 4221.5998, -3.1447, 0),
])
