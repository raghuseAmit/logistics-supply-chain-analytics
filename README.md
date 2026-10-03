# logistics-supply-chain-analytics
Logistics Data Analytics: From Strategic Planning to Visualization, Predictive Modeling &amp; Optimization
---

## 🗓️ Week 1: Strategic Planning, Research & Analytical Architecture

### 1. Objective & Operational Scenario
* **Context**: Simulation of a regional e-commerce fulfillment network comprising 1 Central Distribution Center (CDC) and 5 Regional Fulfillment Hubs (RFHs)[cite: 2].
* **Core Challenges**: Demand volatility-induced regional stockouts, non-optimal vehicle dispatching with idle driver dwell times, and skewed safety-stock holding expenditures[cite: 2].
* **Goal**: Establish a strategic blueprint mapping data science methodologies directly to logistics efficiency and resource allocation targets[cite: 2].

### 2. Key Performance Indicators (KPIs)
* **On-Time In-Full (OTIF) Delivery Rate** ($\ge 96.5\%$): Measures SLA fulfillment and dispatch reliability[cite: 2].
* **Days of Supply of Inventory (DSI)** (14–18 Days): Tracks working capital efficiency and inventory turnover velocity[cite: 2].
* **Cost Per Ton-Kilometer (CPTK)** ($\ge 12\%$ reduction): Evaluates freight transportation operational expenditure per payload-distance unit[cite: 2].
* **Order Lead Time Variance ($\sigma_{\text{LT}}$)** ($\le 1.5$ Hours): Assesses consistency from order ingestion to physical gate dispatch[cite: 2].

### 3. Applied Data Science Methodology & Research
* **Time-Series Demand Forecasting (Predictive)**: Utilizing LightGBM and Prophet on historical order volume and temporal indicators to substitute static buffer baselines with demand-aware safety limits[cite: 2].
* **Spatial Clustering (Unsupervised)**: Applying DBSCAN on customer coordinates to partition dynamic urban micro-delivery zones[cite: 2].
* **Capacitated Vehicle Routing (Prescriptive)**: Formulating mixed-integer constraints using Google OR-Tools to solve the Capacitated Vehicle Routing Problem (CVRP), respecting payload capacities and distance matrices[cite: 2].

### 4. Implementation Snippets (`week1/logistics_strategy.py`)
Week 1 includes a proof-of-concept Python script validating algorithmic feasibility[cite: 2]:
* **Ingestion & Cleaning**: Converts raw timestamps, derives lead times, isolates spatial anomalies, and imputes payload weights using localized category medians[cite: 2].
* **Stochastic Safety Stock Calculation**: Evaluates combined demand and supplier lead-time variances via analytical Gaussian $Z$-score formulations[cite: 2].
* **CVRP Solver**: Generates deterministic routing paths under strict vehicle payload boundaries using Google OR-Tools[cite: 2].

### 5. Running the Week 1 Validation Script
```bash
pip install pandas numpy scipy ortools
python week1/logistics_strategy.py
