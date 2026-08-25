"""
MetricMind - End-to-End API Gateway Integration Test
Tests FastAPI REST endpoints using TestClient.
"""

import os
import sys
import unittest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server.app import app

class TestE2EAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "healthy")

    def test_semantic_meta_endpoint(self):
        res = self.client.get("/api/semantic/meta")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("cubes", data)

    def test_chat_endpoint_root_cause(self):
        payload = {"query": "Why did our European margins drop last quarter?"}
        res = self.client.post("/api/chat", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["type"], "multi_step_diagnostic")
        self.assertIn("steps", data)
        self.assertIn("charts", data)

    def test_audit_stats_endpoint(self):
        res = self.client.get("/api/audit/stats")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("queries_processed", data)
        self.assertIn("sql_hallucinations_prevented", data)

if __name__ == "__main__":
    unittest.main()
