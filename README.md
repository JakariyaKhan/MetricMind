<div align="center">

# 🧠 MetricMind: Agentic Semantic BI Engine
### Governed Enterprise Conversational Analytics via Semantic Layers & AI Orchestration

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://jakariyakhan-metricmind-app-streamlit-xqoydr.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?logo=python&logoColor=white)](https://python.org)
[![Cube.dev](https://img.shields.io/badge/Semantic_Layer-Cube.dev_Standard-7c3aed?logo=cube&logoColor=white)](https://cube.dev)
[![dbt](https://img.shields.io/badge/Data_Transformations-dbt_Gold_Marts-FF694B?logo=dbt&logoColor=white)](https://getdbt.com)
[![LangChain](https://img.shields.io/badge/Orchestration-LangChain_/_LLM-00A67E?logo=langchain&logoColor=white)](https://langchain.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Jakariya_Khan-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jakariyakhan/)

<br/>

### 🌐 **[🚀 Click Here to Launch the Live Interactive App](https://jakariyakhan-metricmind-app-streamlit-xqoydr.streamlit.app/)**

</div>

---

## 📌 Executive Summary & The Problem Solved

As enterprise data architectures evolve, traditional **"Text-to-SQL"** AI bots are failing in production:
* ❌ **Hallucinated Joins & Broken Keys:** LLMs write rogue joins across complex star schemas.
* ❌ **Business Logic Drift:** Financial metrics (*Gross Margin %*, *Recognized Revenue*, *Customer Churn*) require strict corporate accounting formulas that LLMs cannot guess.
* ❌ **The "Deluge of Distrust":** Finance, Sales, and Ops receive divergent numbers for the exact same quarter, destroying institutional trust.

**MetricMind** solves this crisis by introducing a **strict mathematical Semantic Layer (Cube.dev format)**. The AI agent acts as an **orchestrator**—it does not generate raw SQL, but instead queries governed semantic APIs, executes autonomous multi-step root-cause diagnostics, and enforces 100% metric determinism.

---

## 🏛️ End-to-End System Architecture

```
                    ┌─────────────────────────────────────────────────────────────┐
                    │                      EXECUTIVE USER                         │
                    │       "Why did our European margins drop last quarter?"     │
                    └──────────────────────────────┬──────────────────────────────┘
                                                   │
                                                   ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │         INTERACTIVE STREAMLIT CONVERSATIONAL BI             │
                    │  • Executive Question Dropdowns & Regional Scope Filters    │
                    │  • Dynamic Multi-Metric Plotly Charts (Line, Stacked Bar)   │
                    │  • Audit Transparency Drawers ("View SQL" / "View API Call")│
                    └──────────────────────────────┬──────────────────────────────┘
                                                   │
                                                   ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │          AGENTIC ORCHESTRATOR (LangChain / Llama 3)         │
                    │  • Semantic Schema Discovery & Entity Extraction            │
                    │  • Multi-Step Diagnostic Engine (Root-Cause Isolation)      │
                    │  • Cost Governance Guardrails (Max 200 Rows, 3-Hop Limit)   │
                    └──────────────────────────────┬──────────────────────────────┘
                                                   │ (Strict JSON API Payloads)
                                                   ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │            ENTERPRISE SEMANTIC LAYER (Cube.dev Format)      │
                    │  • Governed Metrics as Code: gross_margin_pct, total_revenue│
                    │  • Canonical Dimensions: orders.quarter, geography.region   │
                    │  • Deterministic ANSI / Snowflake SQL Compiler              │
                    └──────────────────────────────┬──────────────────────────────┘
                                                   │ (Compiled, Governed SQL)
                                                   ▼
                    ┌─────────────────────────────────────────────────────────────┐
                    │           DATA LAKEHOUSE (Snowflake / Gold Marts)           │
                    │  • dbt Staging Views (stg_orders, stg_costs, stg_geography) │
                    │  • dbt Gold Marts (fct_orders, fct_cost_breakdown, dim_*)   │
                    └─────────────────────────────────────────────────────────────┘
```

---

## 🌟 Key Features & Innovations

### 1. 📐 Metrics as Code (Decoupled Semantic Layer)
All business metrics are codified in version-controlled YAML files (`orders.yml`, `costs.yml`, `customers.yml`, `geography.yml`):
$$\text{Gross Margin \%} = \frac{\text{Net Revenue} - \text{Total COGS}}{\text{Net Revenue}} \times 100$$
$$\text{Customer Churn Rate \%} = \left(1 - \frac{\text{Active Customers}}{\text{Total Customers}}\right) \times 100$$

### 2. 🔍 Autonomous Multi-Step Root Cause Diagnostics
When an executive asks *"Why did our European margins drop last quarter?"*:
1. **Primary Query:** Retrieves quarterly European margins, identifying a drop from **40.5% in Q3** to **22.8% in Q4**.
2. **Autonomous Secondary Hop:** Without human intervention, queries the operational expense breakdown (`shipping_cost`, `material_cost`, `tariff_cost`).
3. **Root Cause Isolated:** Identifies that **Shipping Costs surged by +240.5%** in Q4 due to regional maritime freight inflation, while material costs remained stable.
4. **Interactive Visualization:** Renders a margin trajectory line chart + operational cost breakdown stacked bar chart.

### 3. 🔒 100% Single Source of Truth & Auditability
* **"View SQL" Drawer:** Inspect the exact compiled, optimized ANSI SQL executed on the lakehouse.
* **"View API Call" Drawer:** Inspect the strict Cube.dev JSON payload sent to the Semantic Layer.
* **Governance Audit Benchmark:** Proven **0.00% numerical variance** across 25+ rephrased prompt runs.

### 4. 🛡️ Warehouse Cost Governance
* Max row limit clamping (capped at 200 rows to prevent unbounded warehouse scans).
* Reasoning hop ceiling (maximum 3 exploratory hops to prevent infinite agent loops).

---

## 📁 Repository Structure

```
MetricMind/
├── app_streamlit.py               # Streamlit Conversational BI & Governance Platform
├── .streamlit/
│   └── config.toml                # Dark Executive Theme configuration
├── requirements.txt               # Production Python dependencies
├── Dockerfile                     # Container deployment specification
├── docker-compose.yml             # Docker compose orchestration
├── run.py                         # One-click master setup & runner script
├── data/
│   ├── seed_generator.py          # Enterprise multi-quarter dataset generator (6,300+ records)
│   └── schema.sql                 # Snowflake / Lakehouse DDL specification
├── dbt_project/
│   ├── dbt_project.yml            # dbt configuration
│   ├── runner.py                  # dbt staging & gold dimensional mart builder
│   └── models/
│       ├── staging/               # stg_orders.sql, stg_costs.sql, stg_geography.sql
│       ├── marts/                 # fct_orders.sql, fct_cost_breakdown.sql, dim_geography.sql
│       └── schema.yml             # Column tests & documentation
├── semantic_layer/
│   ├── engine.py                  # Cube.dev semantic compiler & execution engine
│   ├── server.py                  # Cube.dev REST API (/cubejs-api/v1/meta, /load, /sql)
│   └── schema/
│       ├── orders.yml             # Measures: total_revenue, gross_margin_pct, total_cost
│       ├── costs.yml              # Measures: shipping_cost, material_cost, tariff_cost
│       ├── customers.yml          # Measures: churn_rate, active_customers
│       └── geography.yml          # Dimensions: region, country, country_code
├── agent/
│   ├── governance.py              # Cost governance guardrails & row limiters
│   ├── schema_catalog.py          # Semantic schema extractor for LLM context
│   └── orchestrator.py            # Multi-step reasoning agent & Plotly generator
├── audit/
│   └── governance_audit.py        # 100% determinism verification benchmark suite
└── tests/
    ├── test_semantic_engine.py    # Unit tests for Cube compiler
    ├── test_agent_reasoning.py    # Unit tests for multi-step diagnostics
    └── test_e2e.py                # End-to-end integration tests
```

---

## 🚀 Quick Start Guide (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/JakariyaKhan/MetricMind.git
cd MetricMind
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch with One Command
```bash
python run.py
```
*Or run Streamlit directly:*
```bash
streamlit run app_streamlit.py
```

Open **`http://localhost:8501`** in your browser.

---

## 🧪 Governance Benchmark & Automated Testing

Run the automated verification suite:
```bash
python audit/governance_audit.py
python -m unittest discover tests
```

### ✅ Verification Benchmark Results:
| Audit Test | MetricMind Benchmark | Result | Status |
| :--- | :--- | :--- | :--- |
| **Metric Determinism (Q3 Revenue)** | 0% numerical divergence | **$33,053,100.97** (25/25 runs identical) | ✅ **PASS** |
| **SQL Hallucination Prevention** | 0 unconstrained queries | **100% compiled via Semantic Layer** | ✅ **PASS** |
| **Multi-Step Diagnostics** | Autonomous secondary hop | **Isolated +240.5% European Shipping Surge** | ✅ **PASS** |
| **Cost Governance Guardrails** | Max row limit clamping | **Clamped 50,000 -> 200 rows** | ✅ **PASS** |
| **Unit & Integration Tests** | 15 test cases | **15/15 passed in 0.08s** | ✅ **PASS** |

---

## 👨‍💻 Author & Contact

**Jakariya Khan**  
*Final Year B.Tech in Computer Science & Engineering (Artificial Intelligence & Machine Learning)*  

* 🌐 **Live Application:** [MetricMind on Streamlit Cloud](https://jakariyakhan-metricmind-app-streamlit-xqoydr.streamlit.app/)
* 💼 **LinkedIn:** [linkedin.com/in/jakariyakhan](https://www.linkedin.com/in/jakariyakhan/)
* 🐙 **GitHub:** [@JakariyaKhan](https://github.com/JakariyaKhan)

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
