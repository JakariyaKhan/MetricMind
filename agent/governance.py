"""
MetricMind - Cost & Query Governance Guardrails
Enforces strict warehouse and semantic layer query constraints to prevent
unbounded compute, runaway queries, and infinite agentic loops.
"""

from typing import Dict, Any, Tuple, Optional
import datetime

class CostGovernance:
    def __init__(
        self,
        max_row_limit: int = 200,
        default_row_limit: int = 50,
        max_reasoning_hops: int = 3,
        max_time_range_years: int = 3
    ):
        self.max_row_limit = max_row_limit
        self.default_row_limit = default_row_limit
        self.max_reasoning_hops = max_reasoning_hops
        self.max_time_range_years = max_time_range_years

    def sanitize_query(self, query: Dict[str, Any], hop_count: int = 0) -> Tuple[Dict[str, Any], Optional[str]]:
        """
        Validates and enforces governance rules on a semantic query payload.
        Returns: (sanitized_query, governance_warning_message)
        """
        warnings = []
        sanitized = dict(query)

        # 1. Enforce Hop Limit
        if hop_count > self.max_reasoning_hops:
            raise PermissionError(
                f"[Cost Governance] Agent exceeded maximum reasoning depth of {self.max_reasoning_hops} hops."
            )

        # 2. Enforce Row Limits
        limit = sanitized.get("limit")
        if limit is None:
            sanitized["limit"] = self.default_row_limit
            warnings.append(f"Applied default row limit of {self.default_row_limit}.")
        elif limit > self.max_row_limit:
            sanitized["limit"] = self.max_row_limit
            warnings.append(f"Clamped requested limit {limit} to maximum permitted limit of {self.max_row_limit}.")

        # 3. Ensure at least one metric/measure or dimension is requested
        if not sanitized.get("measures") and not sanitized.get("dimensions"):
            raise ValueError("[Cost Governance] Query must include valid measures or dimensions.")

        # 4. Check date bounds in filters
        filters = sanitized.get("filters", [])
        for f in filters:
            if f.get("operator") == "inDateRange":
                vals = f.get("values", [])
                if len(vals) == 2:
                    try:
                        d1 = datetime.datetime.strptime(vals[0][:10], "%Y-%m-%d")
                        d2 = datetime.datetime.strptime(vals[1][:10], "%Y-%m-%d")
                        diff_days = abs((d2 - d1).days)
                        if diff_days > (self.max_time_range_years * 365):
                            raise ValueError(
                                f"[Cost Governance] Date range spans {diff_days} days, exceeding max lookback limit ({self.max_time_range_years} years)."
                            )
                    except ValueError as ve:
                        if "exceeding max lookback" in str(ve):
                            raise ve

        warning_str = " | ".join(warnings) if warnings else None
        return sanitized, warning_str
