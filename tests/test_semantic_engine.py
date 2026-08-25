"""
MetricMind - Semantic Engine Unit Tests
Tests schema parsing, metric calculations, and Cube REST API compliance.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from semantic_layer.engine import SemanticEngine

class TestSemanticEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = SemanticEngine()

    def test_meta_catalog(self):
        meta = self.engine.get_meta()
        self.assertIn("cubes", meta)
        cube_names = [c["name"] for c in meta["cubes"]]
        self.assertIn("orders", cube_names)
        self.assertIn("costs", cube_names)
        self.assertIn("customers", cube_names)
        self.assertIn("geography", cube_names)

    def test_orders_revenue_query(self):
        query = {
            "measures": ["orders.total_revenue", "orders.gross_margin_pct"],
            "dimensions": ["orders.quarter"],
            "limit": 10
        }
        res = self.engine.execute_query(query)
        self.assertIn("data", res)
        self.assertGreater(len(res["data"]), 0)
        first_row = res["data"][0]
        self.assertIn("orders.total_revenue", first_row)
        self.assertIn("orders.gross_margin_pct", first_row)
        self.assertIn("orders.quarter", first_row)

    def test_geography_filter(self):
        query = {
            "measures": ["orders.total_revenue"],
            "dimensions": ["geography.region"],
            "filters": [
                {
                    "member": "geography.region",
                    "operator": "equals",
                    "values": ["Europe"]
                }
            ]
        }
        res = self.engine.execute_query(query)
        self.assertEqual(len(res["data"]), 1)
        self.assertEqual(res["data"][0]["geography.region"], "Europe")

    def test_cost_breakdown_query(self):
        query = {
            "measures": ["costs.material_cost", "costs.shipping_cost", "costs.total_operational_cost"],
            "dimensions": ["costs.quarter"],
            "limit": 10
        }
        res = self.engine.execute_query(query)
        self.assertIn("data", res)
        self.assertGreater(len(res["data"]), 0)
        self.assertIn("costs.shipping_cost", res["data"][0])

if __name__ == "__main__":
    unittest.main()
