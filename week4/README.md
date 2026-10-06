# Week 4: Predictive Modeling and Optimization in Logistics Systems

## Overview
This directory contains the machine learning and optimization pipeline designed to forecast transit lead times and mitigate the 54.83% delivery delay risk observed in the DataCo Global Supply Chain dataset (180,519 records).

## Model Evaluation Benchmark (Holdout Test Set)
| Model Architecture | MAE (Days) | RMSE (Days) | R² Score |
| :--- | :--- | :--- | :--- |
| **Linear Regression (Baseline)** | 1.0924 | 1.3061 | 0.3541 |
| **Decision Tree Regressor** | 0.8412 | 1.0825 | 0.5562 |
| **Random Forest Regressor (Ensemble)** | **0.7816** | **1.0142** | **0.6108** |

## Key Insights & Optimization Strategies
1. **Model Performance:** Random Forest achieved an MAE of ~18.7 hours, explaining over 61% of total transit variance.
2. **Top Delay Drivers:** Carrier shipping mode, scheduled SLA targets, and destination geographic corridors dominate feature importance.
3. **Interactive Inference:** Implemented `predict_shipment_performance()` to take new shipment inputs and output predicted transit days alongside an automated delay risk flag.
4. **Prescriptive Optimization:**
   - **Dynamic SLA Calibration:** Replaces rigid promises with model-backed ETA calculations (`Predicted_Days + 1.0 * RMSE`).
   - **Carrier Tier Escalation:** Automatically upgrades shipments projected to miss scheduled deadlines to expedited tiers prior to dispatch.
   - **Forward Deployment:** Reallocates fast-moving inventory to high-latency regional hubs.

## Artifacts in this Directory
- `Week4_Predictive_Modeling.ipynb`: Complete training, validation, and interactive inference code.
- `Week4_Predictive_Modeling_and_Optimization_Report.docx`: Comprehensive final deliverable report with embedded evaluation charts and optimization recommendations.
