"""
MetricMind - Agent Reasoning & Multi-Step Diagnostic Tests
Tests agent orchestration, schema-aware query planning, dimensional entity extraction, and root-cause analysis.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.orchestrator import MetricMindAgent

class TestAgentReasoning(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.agent = MetricMindAgent()

    def test_european_margin_root_cause(self):
        query = "Why did our European margins drop last quarter?"
        result = self.agent.orchestrate(query)

        self.assertEqual(result["type"], "multi_step_diagnostic")
        self.assertEqual(len(result["steps"]), 2)
        self.assertIn("Shipping", result["text"])
        self.assertEqual(len(result["charts"]), 2)
        
        # Verify charts structure
        chart1 = result["charts"][0]
        self.assertEqual(chart1["type"], "line")
        chart2 = result["charts"][1]
        self.assertEqual(chart2["type"], "bar")

    def test_standard_revenue_query(self):
        query = "Show me European sales"
        result = self.agent.orchestrate(query)
        self.assertEqual(result["type"], "standard_query")
        self.assertGreater(len(result["steps"]), 0)
        self.assertEqual(len(result["charts"]), 1)

    def test_churn_analysis_segment_query(self):
        query = "What is our Churn Rate by Segment?"
        result = self.agent.orchestrate(query)
        self.assertEqual(result["type"], "standard_query")
        self.assertIn("dim_customers", result["steps"][0]["compiled_sql"])

    def test_churn_analysis_tier_query(self):
        query = "Show active customer count by account tier"
        result = self.agent.orchestrate(query)
        self.assertEqual(result["type"], "standard_query")
        self.assertIn("customers.tier", result["steps"][0]["cube_query"]["dimensions"])

    def test_product_category_revenue(self):
        query = "Show revenue by product category"
        result = self.agent.orchestrate(query)
        self.assertEqual(result["type"], "standard_query")
        self.assertIn("orders.product_category", result["steps"][0]["cube_query"]["dimensions"])

    def test_regional_scope_override(self):
        query = "What was our total revenue?"
        result = self.agent.orchestrate(query, region_override="North America")
        self.assertEqual(result["type"], "standard_query")
        filters = result["steps"][0]["cube_query"]["filters"]
        self.assertTrue(any(f["values"] == ["North America"] for f in filters))

    def test_cost_breakdown_query(self):
        query = "Compare 2025 Shipping Costs vs Material Costs"
        result = self.agent.orchestrate(query)
        self.assertEqual(result["type"], "standard_query")
        self.assertIn("fct_cost_breakdown", result["steps"][0]["compiled_sql"])

if __name__ == "__main__":
    unittest.main()
