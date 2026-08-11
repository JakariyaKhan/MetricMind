"""
MetricMind - Data Lakehouse Ingestion & Seed Generator
Generates realistic multi-quarter enterprise corporate data:
- Orders and line items with revenue
- Detailed cost breakdowns (shipping, material, tariffs, overhead)
- Regional dimensions (Europe, North America, APAC, LATAM)
- Designed to replicate the enterprise scenario: European Gross Margin drop in 2025 Q4 due to shipping cost surge.
"""

import os
import json
import random
import sqlite3
from datetime import datetime, timedelta

def generate_enterprise_data(db_path: str = "metricmind_lakehouse.db"):
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(db_path)) if os.path.dirname(db_path) else ".", exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop existing tables
    cursor.executescript("""
    DROP TABLE IF EXISTS raw_orders;
    DROP TABLE IF EXISTS raw_costs;
    DROP TABLE IF EXISTS raw_geography;
    DROP TABLE IF EXISTS raw_customers;

    CREATE TABLE raw_geography (
        geography_id INTEGER PRIMARY KEY,
        region TEXT NOT NULL,
        country TEXT NOT NULL,
        country_code TEXT NOT NULL,
        currency TEXT NOT NULL
    );

    CREATE TABLE raw_customers (
        customer_id INTEGER PRIMARY KEY,
        customer_name TEXT NOT NULL,
        segment TEXT NOT NULL,
        tier TEXT NOT NULL,
        signup_date TEXT NOT NULL,
        is_active INTEGER NOT NULL
    );

    CREATE TABLE raw_orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        geography_id INTEGER NOT NULL,
        order_timestamp TEXT NOT NULL,
        product_category TEXT NOT NULL,
        gross_revenue_usd REAL NOT NULL,
        discount_amount_usd REAL NOT NULL,
        net_revenue_usd REAL NOT NULL,
        units_sold INTEGER NOT NULL,
        status TEXT NOT NULL
    );

    CREATE TABLE raw_costs (
        cost_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        material_cost_usd REAL NOT NULL,
        shipping_cost_usd REAL NOT NULL,
        tariff_cost_usd REAL NOT NULL,
        overhead_cost_usd REAL NOT NULL,
        carrier TEXT NOT NULL,
        cost_center TEXT NOT NULL
    );
    """)

    # 1. Populate Geography
    geographies = [
        (1, 'Europe', 'Germany', 'DEU', 'EUR'),
        (2, 'Europe', 'France', 'FRA', 'EUR'),
        (3, 'Europe', 'United Kingdom', 'GBR', 'GBP'),
        (4, 'Europe', 'Netherlands', 'NLD', 'EUR'),
        (5, 'North America', 'United States', 'USA', 'USD'),
        (6, 'North America', 'Canada', 'CAN', 'CAD'),
        (7, 'APAC', 'Japan', 'JPN', 'JPY'),
        (8, 'APAC', 'Singapore', 'SGP', 'SGD'),
        (9, 'APAC', 'Australia', 'AUS', 'AUD'),
        (10, 'LATAM', 'Brazil', 'BRA', 'BRL'),
    ]
    cursor.executemany("INSERT INTO raw_geography VALUES (?, ?, ?, ?, ?)", geographies)

    # 2. Populate Customers
    segments = ['Enterprise', 'Mid-Market', 'SMB']
    tiers = ['Tier 1', 'Tier 2', 'Tier 3']
    customers = []
    for c_id in range(1, 201):
        c_name = f"Customer Corp {c_id:03d}"
        segment = random.choice(segments)
        tier = random.choice(tiers)
        signup_date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        is_active = 1 if random.random() > 0.12 else 0
        customers.append((c_id, c_name, segment, tier, signup_date, is_active))
    cursor.executemany("INSERT INTO raw_customers VALUES (?, ?, ?, ?, ?, ?)", customers)

    # 3. Populate Orders & Cost Breakdown across 2025 Q1 - Q4
    # Replicate exact scenario: European Gross Margin drops in Q4 due to freight/shipping surge
    random.seed(42) # Deterministic data generation
    
    categories = ['Cloud Hardware', 'Network Switches', 'Edge Gateways', 'Enterprise Storage']
    carriers_eu = ['DHL Global', 'Maersk Freight', 'Hapag-Lloyd', 'DB Schenker']
    carriers_other = ['FedEx Express', 'UPS Supply Chain', 'DHL Global']
    
    orders = []
    costs = []
    
    start_date = datetime(2025, 1, 1)
    total_days = 365
    
    order_counter = 1
    cost_counter = 1
    
    for day_offset in range(total_days):
        current_date = start_date + timedelta(days=day_offset)
        quarter = f"Q{(current_date.month - 1) // 3 + 1}"
        year = current_date.year
        
        # 10 to 20 orders per day
        daily_orders_count = random.randint(12, 22)
        
        for _ in range(daily_orders_count):
            c_id = random.randint(1, 200)
            geo = random.choice(geographies)
            geo_id = geo[0]
            region = geo[1]
            
            category = random.choice(categories)
            units = random.randint(2, 25)
            unit_price = random.uniform(800, 2500)
            
            gross_rev = round(units * unit_price, 2)
            discount = round(gross_rev * random.uniform(0.02, 0.08), 2)
            net_rev = round(gross_rev - discount, 2)
            
            # Base cost components
            base_material = round(net_rev * random.uniform(0.40, 0.46), 2)
            base_overhead = round(net_rev * random.uniform(0.05, 0.08), 2)
            base_tariff = round(net_rev * random.uniform(0.02, 0.04), 2)
            
            # Shipping Cost Logic:
            # In Q1-Q3 Europe: shipping is ~6-8% of revenue (healthy ~38-42% gross margin)
            # In Q4 Europe (Oct-Dec): European maritime shipping / fuel surcharge surges to 20-25% of revenue!
            # This causes European gross margin % to drop from ~40% to ~23% in Q4!
            if region == 'Europe':
                carrier = random.choice(carriers_eu)
                if quarter == 'Q4':
                    # Shipping surge anomaly
                    shipping_pct = random.uniform(0.20, 0.26)
                else:
                    shipping_pct = random.uniform(0.06, 0.09)
            elif region == 'North America':
                carrier = random.choice(carriers_other)
                shipping_pct = random.uniform(0.07, 0.10)
            else: # APAC & LATAM
                carrier = random.choice(carriers_other)
                shipping_pct = random.uniform(0.08, 0.11)
                
            shipping_cost = round(net_rev * shipping_pct, 2)
            
            # Order timestamp
            time_hour = random.randint(8, 20)
            time_min = random.randint(0, 59)
            time_sec = random.randint(0, 59)
            order_ts = current_date.strftime(f"%Y-%m-%d {time_hour:02d}:{time_min:02d}:{time_sec:02d}")
            
            orders.append((
                order_counter,
                c_id,
                geo_id,
                order_ts,
                category,
                gross_rev,
                discount,
                net_rev,
                units,
                'COMPLETED'
            ))
            
            costs.append((
                cost_counter,
                order_counter,
                base_material,
                shipping_cost,
                base_tariff,
                base_overhead,
                carrier,
                'Logistics & Operations'
            ))
            
            order_counter += 1
            cost_counter += 1

    cursor.executemany("INSERT INTO raw_orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", orders)
    cursor.executemany("INSERT INTO raw_costs VALUES (?, ?, ?, ?, ?, ?, ?, ?)", costs)

    conn.commit()
    conn.close()
    print(f"[+] Successfully generated enterprise lakehouse data: {len(orders)} orders, {len(costs)} cost records in '{db_path}'")

if __name__ == "__main__":
    generate_enterprise_data("metricmind_lakehouse.db")
