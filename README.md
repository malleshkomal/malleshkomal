# Hi, I'm Komal Chougule 👋

**Life cycle assessment & sustainability data analyst** · Berlin, Germany · **Open to new opportunities**

I love to work with messy data, collecting LCI inventory, organise the LCI in well structured manner for reuseability and transperancy. Co-author of a peer-reviewed paper on publishing life cycle inventories so others can reuse them.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Komal%20Chougule-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/komal-mallesh-chougule-72b63a150/)
![Location](https://img.shields.io/badge/Based%20in-Berlin-555555)
![Status](https://img.shields.io/badge/Status-Open%20to%20work-2ea44f)

---

## 📄 Publication

**A generalized schema to publish and share life cycle inventories (LCI): Exemplary case of an aviation fuel supply chain**
R. R. Nair, **K. M. Chougule**, J. C. Gomez Trillos, U. Brand-Daniels · *Journal of Cleaner Production* · [Read the paper](https://www.sciencedirect.com/science/article/pii/S0959652625014702)

The paper proposes a common structure for publishing LCI data so it can be found, checked and reused. It's demonstrated on a power-to-liquid jet fuel supply chain: wind power, electrolysis, direct air capture and Fischer-Tropsch synthesis.

**Life cycle assessment of integrated multi-trophic aquaculture: A review on methodology and challenges for its sustainability evaluation**
A. F. Hala, **K. Chougule**, M. E. Cunha, M. Caria Mendes, I. Oliveira, T. Bradley, J. Forbes, L. Galileu Speranza · *Aquaculture* 590, 741035 (2024)

The review looks at how LCA is applied to integrated multi-trophic aquaculture (IMTA) and why defining the functional unit and choosing the method are hard for multi-product systems.

---

## 🚀 Featured projects

### 🐟 [LCA of fish monoculture and IMTA aquaculture: KPI decision tool](https://github.com/malleshkomal/Life-cycle-assessment-of-Integrated-Multi-Trophical-Aquaculture-)
Built on the pond LCA of the EU INTEGRATE project (Interreg Atlantic Area): semi-intensive and semi-extensive pond IMTA (fish + oysters + macroalgae) against a conventional fish-only pond, per tonne of fish + oyster.
- Inventory, nitrogen and phosphorus balance and impact results per process transcribed and shared in the LCIS2024 structure from my paper
- **13 KPIs** on environment and circularity with targets, as an **offline Excel tool** and as Python with 35 tests
- Semi-intensive IMTA keeps **47%** of the feed nitrogen in products (fish pond: 20%) and cuts eutrophication by **57%**; the semi-extensive IMTA cuts global warming by **56%**. Both need more land
- 39 cross-checks between the report's tables, with two inconsistencies documented
- `LCA` `Piscentool` `Excel` `Python` `pandas` `matplotlib` `pytest`

<a href="https://github.com/malleshkomal/Life-cycle-assessment-of-Integrated-Multi-Trophical-Aquaculture-"><img src="https://raw.githubusercontent.com/malleshkomal/Life-cycle-assessment-of-Integrated-Multi-Trophical-Aquaculture-/main/results/charts/06_flow_si_imta.svg" alt="Animated flow diagram: how fish waste is used in a pond IMTA" width="720"></a>

### 🎓 [Master thesis: biocrude from livestock manure via hydrothermal liquefaction](https://github.com/malleshkomal/htl-manure-lca) · [interactive findings](https://malleshkomal.github.io/htl-manure-lca/)
*Life cycle assessment of biocrude production from livestock manure in Germany via hydrothermal liquefaction*, MSc, TU Bergakademie Freiberg, 2022.
- Three Aspen Plus process models: HTL alone, HTL + catalytic hydrothermal gasification, and HTL + fractional distillation
- 2,000 t/day of wet cattle manure makes **117 t/day of biocrude** (27.6% yield, 39.1 MJ/kg)
- Cradle-to-gate LCA in GaBi (CML 2001): **1.26 kg CO₂ eq per kg bio-oil** with wind power, 1.67 kg on the German grid
- Inventory for 6 scenarios, 12 charts, a Python model that reproduces the mass balance, and automatic data checks
- `Aspen Plus` `GaBi` `LCA` `Python` `pandas` `d3.js`

<a href="https://github.com/malleshkomal/htl-manure-lca"><img src="https://raw.githubusercontent.com/malleshkomal/htl-manure-lca/main/results/charts/06_gwp_by_contributor.png" alt="Global warming potential per kg of bio-oil by contributor, six scenarios" width="720"></a>

### [Life cycle assessment of sustainable aviation fuel : Structured LCI schema for Transparency and reusability ](https://github.com/malleshkomal/ptl-lci-explorer) · [live findings page](https://malleshkomal.github.io/ptl-lci-explorer/)
Python tools that read, validate and scale the paper's published inventory without needing the original LCA software.
- Scales the supply chain to **1 kg of jet fuel** (25.6 kWh, 3.16 kg CO₂ from air) and **1 kg of liquid hydrogen** (65.2 kWh)
- Six automatic quality checks on the published files
- Links circularity KPIs (carbon loop, end-of-life coverage, Material Circularity Indicator) to a screening carbon footprint through shared scenario parameters: the most circular scenario is also the lowest-carbon one, and electricity sets **85%** of the footprint ([methods](https://github.com/malleshkomal/ptl-lci-explorer/blob/main/METHODS.md))
- Seven charts, an interactive findings page and an [animated flow diagram](https://malleshkomal.github.io/ptl-lci-explorer/flow.html) of the supply chain
- `Python` `pandas` `NumPy` `matplotlib` `d3.js` `pytest`

<a href="https://malleshkomal.github.io/ptl-lci-explorer/flow.html"><img src="https://raw.githubusercontent.com/malleshkomal/ptl-lci-explorer/main/results/charts/08_flow_animated.svg" alt="Animated flow diagram: wind power, water and CO₂ from air become 1 kg of PtL jet fuel" width="720"></a>

### [Circular Design Advisor](https://github.com/malleshkomal/circular-design-advisor)
An animated decision dashboard for the end of life of a modular aluminium exhibition-booth panel: reuse, repair, reprocessing, recycling or disposal.
- Per-use LCA, circularity KPIs and cost for five strategies, with literature sources tracked for every input
- 2,538-scenario simulation, 1,500-draw Monte Carlo, Pareto optimisation and a Random Forest surrogate (R² 0.99)
- Reuse beats recycling from two planned uses: **5.7 vs 21.1 kg CO₂e per use** (illustrative baseline)
- Streamlit dashboard with animated Plotly charts and a chatbot that explains the calculated results
- `Python` `Streamlit` `Plotly` `scikit-learn` `pandas` `pytest`

<a href="https://github.com/malleshkomal/circular-design-advisor"><img src="https://raw.githubusercontent.com/malleshkomal/circular-design-advisor/main/docs/screenshots/01_overview.png" alt="Circular Design Advisor dashboard overview" width="720"></a>

### [Circular-booth-KPI](https://github.com/malleshkomal/Circular-booth-KPI)
Compares single-use and reusable exhibition booth designs on carbon footprint per use, cost and circularity.
- Shows reuse cutting GWP per booth use by **88–91%** (illustrative data)
- Reuse-cycle simulation and a transparent, explainable multi-criteria ranking
- A guard against double-counting recycling benefits
- `Python` `pandas` `matplotlib` `pytest`

### [Garment LCA Pipeline](https://github.com/malleshkomal/Simple-T-shirt-example)
An end-to-end LCA data pipeline for a T-shirt, jeans and sneakers, from raw supplier data to animated charts.
- Collects four sources (bill of materials, factory meters, shipments, use and end-of-life assumptions)
- Validates, converts units and loads results into a SQLite star schema
- Footprints of **4.68 to 10.91 kg CO₂e per unit**, with raw materials the largest source (simulated data)
- Animated matplotlib GIFs and an interactive page with hover values
- `Python` `pandas` `SQLite` `matplotlib` `JavaScript`

<a href="https://github.com/malleshkomal/Simple-T-shirt-example"><img src="https://raw.githubusercontent.com/malleshkomal/Simple-T-shirt-example/main/output/1_stacked_build.gif" alt="Animated stacked bar chart of carbon footprint per garment by life cycle stage" width="720"></a>

---

## 🧰 What I work with

| Area | Skills and tools |
|---|---|
| **Life cycle assessment** | LCA modelling (ISO 14040/44), carbon footprint (GWP), life cycle inventories, openLCA, GaBi, Brightway, ecoinvent, EF 3.1, CML 2001 |
| **Process modelling** | Aspen Plus (RYield, RGibbs, RadFrac, Fortran calculators), mass and energy balances, hydrothermal liquefaction |
| **Circular economy** | Circularity KPIs, KPI frameworks, nutrient recovery (IMTA), reuse and end-of-life scenarios, recycled content |
| **Energy systems** | Power-to-X, hydrogen, sustainable aviation fuels, prospective energy scenarios |
| **Data & analysis** | Python, pandas, NumPy, SQLite, scikit-learn, Jupyter, data pipelines and validation |
| **Visualisation** | matplotlib, Plotly, d3.js, Streamlit, animated and interactive dashboards |
| **Decision support** | Transparent multi-criteria comparison of design options |

---

## 📫 Get in touch

I'm looking for roles in **LCA, sustainability analytics and circular economy**. Message me on [LinkedIn](https://www.linkedin.com/in/komal-mallesh-chougule-72b63a150/).
