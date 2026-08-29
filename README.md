# MetricMind: Agentic Semantic BI Engine

> **Axlero Solutions – Advanced Data Analytics (2026 Standards)**  
> *Governed, AI-Driven Conversational BI powered by Semantic Layers, Lakehouse Modeling, and Multi-Step Agentic Reasoning.*

---

## 📌 Executive Summary & Problem Solved

Traditional **"Text-to-SQL"** AI implementations directly expose raw enterprise data warehouses to LLMs. This almost always leads to disaster:
* **Hallucinated Joins & Schema Drift:** LLMs generate erroneous joins across complex dimensional models.
* **Metric Inconsistency:** Business logic (e.g. *Gross Margin*, *Churn*, *Recognized Revenue*) varies from prompt to prompt.
* **The "Deluge of Distrust":** Sales and Finance receive divergent numbers for the exact same quarter.

**MetricMind** solves this by establishing a **strict mathematical Semantic Layer (Cube.dev format)**. The AI agent (LangChain / Llama 3) does not write raw SQL; instead, it acts as an **orchestrator** querying governed metric APIs, performing autonomous multi-step root-cause diagnostics, and delivering verifiable analytics with 100% numerical consistency.

---

## 🏛️ System Architecture

```
[ Executive / Business User ]
           │
           ▼
[ Streamlit Conversational BI Platform ]
   • Interactive Chat Experience with Governed Responses
   • Multi-Metric Plotly Dynamic Visualizations (Line, Stacked Bar)
   • Audit Drawers: "View Compiled SQL" & "View Cube.dev API Call"
   • Live Semantic Layer Catalog Explorer & Interactive Query Playground
   • Real-Time Governance & Determinism Audit Suite
           │
           ▼
[ Agentic AI Orchestrator (LangChain / Llama 3) ]
   • Semantic Schema Discovery
   • Multi-Step Diagnostic Reasoning (Margin Drop -> Shipping Breakdown)
   • Cost Governance (Max Row Limits, Depth Constraints)
           │
           ▼ (Strict JSON REST Calls)
[ Enterprise Semantic Layer (Cube.dev Format) ]
   • Measures & Dimensions as Code (YAML)
   • Mathematical Metric Formulas (Gross Margin %, Churn Rate)
   • Deterministic ANSI SQL Compiler
           │
           ▼ (Compiled, Governed SQL)
[ Data Lakehouse & dbt Transformation Layer ]
   • Raw Bronze Staging Tables
   • Gold Analytical Marts (fct_orders, fct_cost_breakdown, dim_geography, dim_dates)
```

---

## 🧩 Key Modules & Directory Structure

```
c:\Users\jakar\Desktop\MetricMind\
├── app_streamlit.py               # Streamlit interactive Conversational BI & Governance Platform
├── data/
│   ├── seed_generator.py          # Enterprise multi-quarter corporate dataset generator
│   └── schema.sql                 # Snowflake / Lakehouse DDL specification
├── dbt_project/
│   ├── dbt_project.yml            # dbt configuration
│   ├── runner.py                  # dbt execution engine (staging -> gold marts)
│   └── models/
│       ├── staging/               # stg_orders.sql, stg_costs.sql, stg_geography.sql
│       ├── marts/                 # fct_orders.sql, fct_cost_breakdown.sql, dim_geography.sql
│       └── schema.yml             # Data quality tests & documentation
├── semantic_layer/
│   ├── engine.py                  # Semantic compiler & execution engine
│   ├── server.py                  # Cube.dev REST API (/cubejs-api/v1/meta, /load, /sql)
│   └── schema/
│       ├── orders.yml             # Measures: total_revenue, gross_margin_pct, total_cost
│       ├── costs.yml              # Measures: shipping_cost, material_cost, tariff_cost
│       ├── customers.yml          # Measures: churn_rate, active_customers
│       └── geography.yml          # Dimensions: region, country, country_code
├── agent/
│   ├── governance.py              # Cost governance guardrails (row caps, hop limits)
│   ├── schema_catalog.py          # Semantic schema extractor for LLM context
│   └── orchestrator.py            # Multi-step reasoning agent & Plotly visual generator
├── server/
│   └── app.py                     # FastAPI gateway & SSE streaming chat server
├── frontend/
│   ├── index.html                 # Web dashboard UI
│   ├── style.css                  # Dark mode styling
│   └── app.js                     # Dynamic ECharts renderer & audit modal controller
├── audit/
│   └── governance_audit.py        # 100% determinism & zero-hallucination verification suite
├── tests/
│   ├── test_semantic_engine.py    # Unit tests for Cube.dev compiler
│   ├── test_agent_reasoning.py    # Multi-step root cause diagnostic tests
│   └── test_e2e.py                # End-to-end REST API tests
├── run.py                         # Master one-click startup & verification script
└── README.md                      # Complete system documentation
```

---

## 🚀 Quick Start Guide

### Launch the Streamlit Platform:
```powershell
cd c:\Users\jakar\Desktop\MetricMind
python -m streamlit run app_streamlit.py
```
*Or simply run:*
```powershell
python run.py
```
Open **`http://localhost:8501`** in your browser.

---

## 🖥️ Streamlit Platform Features

1. **💬 Conversational BI & Multi-Step Diagnostics:**
   - Ask complex business questions with instant single-click prompt buttons.
   - Autonomous multi-step root-cause diagnostics (diagnosing the European Q4 margin drop and plotting interactive margin trajectories & operational cost breakdowns).
2. **🔍 Full Auditability & Single Source of Truth:**
   - Open the **Audit Transparency Drawer** under any response to view the exact **Cube.dev REST API JSON payload** and the **Compiled ANSI / Snowflake SQL** executed on the warehouse.
   - Inspect the raw governed data table returned by the Semantic Layer.
3. **🏛️ Semantic Layer Catalog Explorer & Playground:**
   - Browse the YAML definitions of all cubes, measures, and dimensions in real time.
   - Interactive Semantic Query Playground allowing custom multi-select measures, dimensions, and limits.
4. **💾 Lakehouse Gold Marts Browser:**
   - Inspect `fct_orders`, `fct_cost_breakdown`, `dim_geography`, and `dim_customers` with column schemas and summary statistics.
5. **🛡️ Live Governance & Determinism Audit:**
   - Click the **Run Full Governance Audit** button directly inside the UI to benchmark determinism (25 consecutive runs for "Q3 Revenue" returning $33,053,100.97 with 0% divergence).
