# Week 3: Advanced Data Analysis and Visualization in Logistics

## Overview
This directory contains the exploratory data analysis (EDA), visual analytics, and operational root-cause diagnostics for the DataCo Global Supply Chain network (180,519 records). The analysis investigates why 54.83% of all orders incur delivery delay risk and provides actionable recommendations to optimize resource allocation.

## Key Visualizations & Findings
1. **Fulfillment Disparity (KDE Plot):** Actual shipping duration (mean 3.498 days) systematically outpaces scheduled commitments (mean 2.932 days).
2. **Carrier Tier Variance (Boxplot):** Standard Class exhibits wide transit variance (2–6 days), while Same Day shipping reliably caps lead times at 0–1 day.
3. **Dispatch Weekday Analysis (Bar Chart):** Delay probability remains uniformly high across all dispatch days (~54%–55%), indicating structural rather than weekend-only bottlenecks.
4. **Operational Correlation (Heatmap):** Customer order sales show zero correlation with late delivery risk ($r = -0.00$), confirming that high-value orders currently receive no dispatch prioritization.
5. **Regional Delay Corridors (Horizontal Bar Chart):** Southeast Asia and South Asia lead network delays with breach rates over 56%.

## Operational Recommendations
- **Dynamic SLA Recalibration:** Increase default scheduled standard delivery targets from 2.9 to 3.5 days to restore realistic expectations.
- **Value-Tiered Dispatching:** Implement automatic expedited queueing for orders with sales value exceeding $250.
- **Geographic Buffers:** Allocate +1 day transit buffers on high-latency international routes.

## Artifacts in this Directory
- `Week3_Advanced_Data_Analysis.ipynb`: Complete documented Python analysis and plotting scripts.
- `Week3_Advanced_Data_Analysis_Report.docx`: Comprehensive analytical report with embedded high-resolution figures.
- `charts/`: Exported high-resolution visualization figures.
