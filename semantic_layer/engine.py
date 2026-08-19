"""
MetricMind - Enterprise Semantic Layer Engine
A Python-powered Cube.dev compatible semantic compiler and execution engine.
- Decouples metric definitions as code (YAML) from LLM and BI layers.
- Compiles natural semantic requests into deterministic ANSI SQL.
- Guarantees 100% mathematical consistency across all enterprise metrics.
"""

import os
import re
import glob
import yaml
import sqlite3
from typing import Dict, List, Any, Optional, Tuple

class SemanticEngine:
    def __init__(self, schema_dir: str = "semantic_layer/schema", db_path: str = "metricmind_lakehouse.db"):
        self.schema_dir = os.path.abspath(schema_dir)
        self.db_path = os.path.abspath(db_path)
        self.cubes: Dict[str, Dict[str, Any]] = {}
        self.load_schemas()

    def load_schemas(self):
        """Loads all Cube.dev YAML schema files from the schema directory."""
        self.cubes.clear()
        yaml_files = glob.glob(os.path.join(self.schema_dir, "*.yml")) + glob.glob(os.path.join(self.schema_dir, "*.yaml"))
        for yf in yaml_files:
            try:
                with open(yf, "r", encoding="utf-8") as f:
                    content = yaml.safe_load(f)
                    if content and "cubes" in content:
                        for cube in content["cubes"]:
                            cube_name = cube["name"]
                            self.cubes[cube_name] = cube
            except Exception as e:
                print(f"[!] Error loading semantic schema {yf}: {e}")

    def get_meta(self) -> Dict[str, Any]:
        """Returns metadata catalog matching the Cube.dev /cubejs-api/v1/meta specification."""
        cube_list = []
        for name, cube in self.cubes.items():
            measures = []
            for m in cube.get("measures", []):
                measures.append({
                    "name": f"{name}.{m['name']}",
                    "title": m.get("title", m["name"].replace("_", " ").title()),
                    "type": m.get("type", "number"),
                    "format": m.get("format"),
                    "description": m.get("description", "")
                })
            dimensions = []
            for d in cube.get("dimensions", []):
                dimensions.append({
                    "name": f"{name}.{d['name']}",
                    "title": d.get("title", d["name"].replace("_", " ").title()),
                    "type": d.get("type", "string"),
                    "description": d.get("description", ""),
                    "primaryKey": d.get("primary_key", False)
                })
            cube_list.append({
                "name": name,
                "title": cube.get("title", name.title()),
                "description": cube.get("description", ""),
                "measures": measures,
                "dimensions": dimensions
            })
        return {"cubes": cube_list}

    def compile_sql(self, query: Dict[str, Any]) -> Tuple[str, List[Any], Dict[str, str]]:
        """
        Compiles a Cube REST API query payload into deterministic ANSI SQL.
        Returns: (sql_string, params, alias_mapping)
        """
        measures = query.get("measures", [])
        dimensions = query.get("dimensions", [])
        filters = query.get("filters", [])
        time_dimensions = query.get("timeDimensions", [])
        order_spec = query.get("order", {})
        limit = query.get("limit", 100)

        if not measures and not dimensions and not time_dimensions:
            raise ValueError("Query must specify at least one measure, dimension, or timeDimension.")

        # Identify primary cube
        all_members = measures + dimensions
        for td in time_dimensions:
            all_members.append(td.get("dimension"))
        for f in filters:
            all_members.append(f.get("member"))

        cube_names = list({m.split(".")[0] for m in all_members if m and "." in m})
        if not cube_names:
            cube_names = ["orders"]
        
        # Primary cube is the first measure's cube, or the first referenced cube
        primary_cube_name = cube_names[0]
        if measures and "." in measures[0]:
            primary_cube_name = measures[0].split(".")[0]
        elif "orders" in cube_names:
            primary_cube_name = "orders"

        primary_cube = self.cubes.get(primary_cube_name)
        if not primary_cube:
            raise ValueError(f"Cube '{primary_cube_name}' not found in semantic schema.")

        table_alias = primary_cube_name
        from_clause = f"{primary_cube['sql_table']} AS {table_alias}"

        # Determine joins needed
        joins_needed = [c for c in cube_names if c != primary_cube_name]
        join_clauses = []
        defined_joins = {j["name"]: j for j in primary_cube.get("joins", [])}

        for jc in joins_needed:
            if jc in defined_joins:
                join_def = defined_joins[jc]
                target_cube = self.cubes.get(jc)
                if target_cube:
                    raw_join_sql = join_def["sql"]
                    # Replace {CUBE} with primary table alias and {target.field} with target_alias.field
                    formatted_join_sql = raw_join_sql.replace("{CUBE}", table_alias)
                    formatted_join_sql = re.sub(rf"\{{{jc}\.([^}}]+)\}}", rf"{jc}.\1", formatted_join_sql)
                    join_clauses.append(f"LEFT JOIN {target_cube['sql_table']} AS {jc} ON {formatted_join_sql}")

        # Build Select expressions
        select_exprs = []
        alias_mapping = {}
        group_by_indices = []
        idx = 1

        # 1. Dimensions
        for dim_name in dimensions:
            if "." not in dim_name:
                continue
            c_name, d_name = dim_name.split(".", 1)
            cube_obj = self.cubes.get(c_name, {})
            dim_def = next((d for d in cube_obj.get("dimensions", []) if d["name"] == d_name), None)
            if dim_def:
                raw_sql = dim_def["sql"]
                sql_expr = f"{c_name}.{raw_sql}" if not "(" in raw_sql else raw_sql.replace("{CUBE}", c_name)
                alias = dim_name.replace(".", "__")
                select_exprs.append(f"{sql_expr} AS \"{alias}\"")
                alias_mapping[alias] = dim_name
                group_by_indices.append(str(idx))
                idx += 1

        # 2. Time Dimensions
        for td in time_dimensions:
            td_name = td.get("dimension")
            granularity = td.get("granularity", "day")
            if "." not in td_name:
                continue
            c_name, d_name = td_name.split(".", 1)
            cube_obj = self.cubes.get(c_name, {})
            dim_def = next((d for d in cube_obj.get("dimensions", []) if d["name"] == d_name), None)
            if dim_def:
                raw_sql = dim_def["sql"]
                col_ref = f"{c_name}.{raw_sql}"
                if granularity == "quarter":
                    sql_expr = f"'Q' || ((CAST(SUBSTR({col_ref}, 6, 2) AS INTEGER) - 1) / 3 + 1)"
                elif granularity == "month":
                    sql_expr = f"SUBSTR({col_ref}, 1, 7)"
                elif granularity == "year":
                    sql_expr = f"SUBSTR({col_ref}, 1, 4)"
                else: # day / date
                    sql_expr = f"DATE({col_ref})"
                
                alias = f"{td_name}__{granularity}".replace(".", "__")
                select_exprs.append(f"{sql_expr} AS \"{alias}\"")
                alias_mapping[alias] = f"{td_name}.{granularity}"
                group_by_indices.append(str(idx))
                idx += 1

        # 3. Measures
        for m_name in measures:
            if "." not in m_name:
                continue
            c_name, meas_name = m_name.split(".", 1)
            cube_obj = self.cubes.get(c_name, {})
            meas_def = next((m for m in cube_obj.get("measures", []) if m["name"] == meas_name), None)
            if meas_def:
                m_type = meas_def.get("type", "number")
                raw_sql = meas_def["sql"]
                
                if m_type == "count":
                    sql_expr = f"COUNT({c_name}.{raw_sql})"
                elif m_type == "sum":
                    sql_expr = f"SUM({c_name}.{raw_sql})"
                elif m_type == "avg":
                    sql_expr = f"AVG({c_name}.{raw_sql})"
                elif m_type == "min":
                    sql_expr = f"MIN({c_name}.{raw_sql})"
                elif m_type == "max":
                    sql_expr = f"MAX({c_name}.{raw_sql})"
                else: # custom formula / number
                    # Substitute any direct column references with proper table prefixes
                    # Example: net_revenue_usd -> c_name.net_revenue_usd
                    formatted = raw_sql
                    for col in ["net_revenue_usd", "total_cost_usd", "gross_revenue_usd", "discount_amount_usd",
                                "material_cost_usd", "shipping_cost_usd", "tariff_cost_usd", "overhead_cost_usd", "is_active"]:
                        formatted = re.sub(rf"\b{col}\b", f"{c_name}.{col}", formatted)
                    sql_expr = formatted
                
                alias = m_name.replace(".", "__")
                select_exprs.append(f"{sql_expr} AS \"{alias}\"")
                alias_mapping[alias] = m_name
                idx += 1

        # Build WHERE filters
        where_clauses = []
        params = []
        for f in filters:
            member = f.get("member")
            op = f.get("operator", "equals")
            vals = f.get("values", [])
            
            if "." in member:
                c_name, field_name = member.split(".", 1)
                cube_obj = self.cubes.get(c_name, {})
                # check dimensions
                field_def = next((d for d in cube_obj.get("dimensions", []) if d["name"] == field_name), None)
                if field_def:
                    col_sql = f"{c_name}.{field_def['sql']}"
                    if op == "equals":
                        where_clauses.append(f"{col_sql} = ?")
                        params.append(vals[0] if vals else "")
                    elif op == "notEquals":
                        where_clauses.append(f"{col_sql} != ?")
                        params.append(vals[0] if vals else "")
                    elif op == "contains":
                        where_clauses.append(f"{col_sql} LIKE ?")
                        params.append(f"%{vals[0]}%" if vals else "%")
                    elif op == "inDateRange" and len(vals) == 2:
                        where_clauses.append(f"DATE({col_sql}) BETWEEN ? AND ?")
                        params.extend(vals)
                    elif op == "gte":
                        where_clauses.append(f"{col_sql} >= ?")
                        params.append(vals[0])
                    elif op == "lte":
                        where_clauses.append(f"{col_sql} <= ?")
                        params.append(vals[0])
                    elif op == "in":
                        placeholders = ", ".join(["?"] * len(vals))
                        where_clauses.append(f"{col_sql} IN ({placeholders})")
                        params.extend(vals)

        # Build SQL statement
        select_str = ",\n    ".join(select_exprs)
        joins_str = "\n".join(join_clauses)
        where_str = f"\nWHERE {' AND '.join(where_clauses)}" if where_clauses else ""
        group_by_str = f"\nGROUP BY {', '.join(group_by_indices)}" if group_by_indices else ""
        
        # Order clause
        order_clauses = []
        if isinstance(order_spec, dict):
            for k, v in order_spec.items():
                alias = k.replace(".", "__")
                direction = "DESC" if str(v).lower() == "desc" else "ASC"
                order_clauses.append(f"\"{alias}\" {direction}")
        elif isinstance(order_spec, list):
            for item in order_spec:
                if isinstance(item, list) and len(item) == 2:
                    alias = item[0].replace(".", "__")
                    direction = "DESC" if str(item[1]).lower() == "desc" else "ASC"
                    order_clauses.append(f"\"{alias}\" {direction}")

        order_by_str = f"\nORDER BY {', '.join(order_clauses)}" if order_clauses else ""
        limit_str = f"\nLIMIT {int(limit)}"

        compiled_sql = f"SELECT\n    {select_str}\nFROM {from_clause}\n{joins_str}{where_str}{group_by_str}{order_by_str}{limit_str};".strip()
        # Clean up empty lines
        compiled_sql = re.sub(r'\n+', '\n', compiled_sql)
        
        return compiled_sql, params, alias_mapping

    def execute_query(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Executes a semantic query and returns Cube.dev compliant structured JSON results."""
        sql_query, params, alias_mapping = self.compile_sql(query)
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(sql_query, params)
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            record = {}
            for col_alias, val in dict(row).items():
                member_name = alias_mapping.get(col_alias, col_alias)
                # Ensure float rounding for clean JSON presentation
                if isinstance(val, float):
                    val = round(val, 2)
                record[member_name] = val
            data.append(record)
            
        conn.close()

        # Build response payload
        return {
            "query": query,
            "data": data,
            "sql": sql_query,
            "params": params,
            "total": len(data),
            "annotation": {
                "measures": {m: {"title": m.split(".")[1].replace("_", " ").title()} for m in query.get("measures", [])},
                "dimensions": {d: {"title": d.split(".")[1].replace("_", " ").title()} for d in query.get("dimensions", [])}
            }
        }
