"""
MetricMind - Semantic Schema Catalog Provider
Extracts verified metadata from the Semantic Layer and formats it for LLM orchestration.
"""

from typing import Dict, Any, List
from semantic_layer.engine import SemanticEngine

class SchemaCatalog:
    def __init__(self, engine: SemanticEngine):
        self.engine = engine

    def get_catalog_summary(self) -> str:
        """Formats the semantic layer schema into an optimized system prompt context."""
        meta = self.engine.get_meta()
        lines = [
            "### ENTERPRISE SEMANTIC LAYER CATALOG (Cube.dev Format)",
            "You must query metrics ONLY using this catalog. DO NOT generate raw SQL queries.",
            "Use the exact member names (cube.measure or cube.dimension) specified below:\n"
        ]

        for cube in meta.get("cubes", []):
            lines.append(f"Cube: `{cube['name']}` ({cube.get('title', '')}) - {cube.get('description', '')}")
            lines.append("  Measures (Aggregated Metrics):")
            for m in cube.get("measures", []):
                lines.append(f"    - `{m['name']}`: {m.get('description', '')} [Type: {m.get('type')}, Format: {m.get('format', 'numeric')}]")
            lines.append("  Dimensions (Attributes / Grouping):")
            for d in cube.get("dimensions", []):
                lines.append(f"    - `{d['name']}`: {d.get('description', '')} [Type: {d.get('type')}]")
            lines.append("")

        return "\n".join(lines)

    def get_all_measure_names(self) -> List[str]:
        meta = self.engine.get_meta()
        names = []
        for cube in meta.get("cubes", []):
            for m in cube.get("measures", []):
                names.append(m["name"])
        return names

    def get_all_dimension_names(self) -> List[str]:
        meta = self.engine.get_meta()
        names = []
        for cube in meta.get("cubes", []):
            for d in cube.get("dimensions", []):
                names.append(d["name"])
        return names
