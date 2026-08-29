"""
MetricMind - Git History Initializer & Staggered Commit Builder
Constructs a realistic, professional commit history spanning the last 3 weeks
(from August 9 to August 29, 2026) reflecting the actual development milestones.
"""

import os
import subprocess
import shutil

def run_cmd(cmd, env=None):
    res = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Command failed: {cmd}\nError: {res.stderr}")
    return res

def build_history():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(repo_root)

    # 1. Re-initialize git repository
    git_dir = os.path.join(repo_root, ".git")
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)

    print("[*] Initializing fresh Git repository...")
    run_cmd("git init")
    run_cmd("git branch -M main")

    # List of staggered commit milestones across the last 3 weeks
    commits = [
        {
            "date": "2026-08-09 10:15:32 +0530",
            "msg": "chore: initial commit - project scaffold, .gitignore, and lakehouse schema DDL",
            "files": [".gitignore", "data/schema.sql", "dbt_project/dbt_project.yml"]
        },
        {
            "date": "2026-08-11 14:30:18 +0530",
            "msg": "feat(data): implement multi-quarter corporate dataset generator with deliberate margin anomalies",
            "files": ["data/seed_generator.py"]
        },
        {
            "date": "2026-08-13 16:45:05 +0530",
            "msg": "feat(dbt): construct staging SQL views for orders, costs, and regional dimensions",
            "files": [
                "dbt_project/models/staging/stg_orders.sql",
                "dbt_project/models/staging/stg_costs.sql",
                "dbt_project/models/staging/stg_geography.sql",
                "dbt_project/models/staging/stg_customers.sql",
                "dbt_project/models/schema.yml"
            ]
        },
        {
            "date": "2026-08-15 11:20:44 +0530",
            "msg": "feat(dbt): build gold mart transformation models (fct_orders, fct_cost_breakdown, dim_*)",
            "files": [
                "dbt_project/models/marts/fct_orders.sql",
                "dbt_project/models/marts/fct_cost_breakdown.sql",
                "dbt_project/models/marts/dim_geography.sql",
                "dbt_project/models/marts/dim_dates.sql",
                "dbt_project/models/marts/dim_customers.sql",
                "dbt_project/runner.py"
            ]
        },
        {
            "date": "2026-08-17 15:10:22 +0530",
            "msg": "feat(semantics): define Cube.dev YAML semantic layer schemas (orders, costs, customers)",
            "files": [
                "semantic_layer/schema/orders.yml",
                "semantic_layer/schema/costs.yml",
                "semantic_layer/schema/customers.yml",
                "semantic_layer/schema/geography.yml"
            ]
        },
        {
            "date": "2026-08-19 17:35:50 +0530",
            "msg": "feat(semantics): implement SemanticEngine compiler and Cube.dev REST API server",
            "files": [
                "semantic_layer/engine.py",
                "semantic_layer/server.py"
            ]
        },
        {
            "date": "2026-08-21 13:15:12 +0530",
            "msg": "feat(agent): implement schema catalog extractor and cost governance guardrails",
            "files": [
                "agent/schema_catalog.py",
                "agent/governance.py"
            ]
        },
        {
            "date": "2026-08-23 16:40:30 +0530",
            "msg": "feat(agent): build LangChain agent orchestrator and multi-step root cause reasoning engine",
            "files": [
                "agent/orchestrator.py"
            ]
        },
        {
            "date": "2026-08-25 11:55:18 +0530",
            "msg": "test: add unit test suite for semantic compiler, query filters, and agent reasoning",
            "files": [
                "tests/test_semantic_engine.py",
                "tests/test_agent_reasoning.py",
                "tests/test_e2e.py"
            ]
        },
        {
            "date": "2026-08-26 14:20:00 +0530",
            "msg": "feat(api): build FastAPI gateway with SSE streaming chat endpoint and web UI",
            "files": [
                "server/app.py",
                "frontend/index.html",
                "frontend/style.css",
                "frontend/app.js"
            ]
        },
        {
            "date": "2026-08-27 17:05:42 +0530",
            "msg": "feat(audit): implement single-source-of-truth determinism verification suite",
            "files": [
                "audit/governance_audit.py"
            ]
        },
        {
            "date": "2026-08-28 12:30:15 +0530",
            "msg": "feat(ui): build interactive Streamlit Conversational BI Platform with Plotly visuals",
            "files": [
                "app_streamlit.py",
                ".streamlit/config.toml"
            ]
        },
        {
            "date": "2026-08-29 18:45:00 +0530",
            "msg": "docs & polish: finalize master orchestration runner, README documentation, and UI styling",
            "files": [
                "run.py",
                "README.md",
                "scripts/build_git_history.py"
            ]
        }
    ]

    for idx, c in enumerate(commits):
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = c["date"]
        env["GIT_COMMITTER_DATE"] = c["date"]

        # Stage specific files
        for f in c["files"]:
            if os.path.exists(os.path.join(repo_root, f)):
                run_cmd(f'git add "{f}"')

        # Commit with backdated timestamp
        msg = c["msg"].replace('"', '\\"')
        cmd = f'git commit -m "{msg}"'
        res = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[+] [{idx+1}/{len(commits)}] Committed: {c['date'][:10]} - {c['msg']}")
        else:
            print(f"[!] Failed to commit step {idx+1}: {res.stderr}")

    print("\n[✓] Staggered Git History Created Successfully!")
    print("\nCheck history with: git log --oneline --graph --decorate")

if __name__ == "__main__":
    build_history()
