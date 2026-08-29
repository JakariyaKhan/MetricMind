"""
MetricMind - Master Orchestration & Startup Script
Initializes the lakehouse, runs dbt transformations, performs governance audits,
and launches the interactive Streamlit Conversational BI Platform.
"""

import os
import sys
import subprocess

def main():
    print("=" * 75)
    print("  METRICMIND: AGENTIC SEMANTIC BI ENGINE (STREAMLIT PLATFORM)")
    print("  Governed Enterprise Analytics via Semantic Layers & AI Orchestration")
    print("=" * 75)

    db_file = "metricmind_lakehouse.db"

    # Step 1: Data Ingestion & Seeding
    print("\n[Step 1/3] Ingesting multi-quarter enterprise corporate data...")
    from data.seed_generator import generate_enterprise_data
    generate_enterprise_data(db_file)

    # Step 2: dbt Transformation Pipeline
    print("\n[Step 2/3] Executing dbt staging & gold dimensional transformations...")
    from dbt_project.runner import run_transformations
    run_transformations(db_file)

    # Step 3: Launch Streamlit Application
    print("\n[Step 3/3] Launching MetricMind Interactive Streamlit Interface...")
    print("  -> Starting Streamlit Dashboard on http://localhost:8501")
    print("  -> Press CTRL+C to stop.\n")

    # Launch streamlit via subprocess
    cmd = [sys.executable, "-m", "streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.headless=true"]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
