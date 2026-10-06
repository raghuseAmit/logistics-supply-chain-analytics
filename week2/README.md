# Week 2: Data Collection, Cleaning, and Preprocessing for Logistics Analysis

## Overview
This directory contains the data preparation pipeline executed on the DataCo Global Smart Supply Chain dataset (180,519 records). The objective was to audit, clean, normalize, and engineer logistics features for downstream predictive modeling.

## Key Pipeline Steps Implemented
1. **Quality Audit & Pruning:** 
   - Pruned `Product Description` (100% missing) and `Order Zipcode` (86.24% missing).
   - Removed unencrypted PII (`Customer Email`, `Customer Password`) and redundant image URLs.
   - Preserved destination spatial integrity via City, State, and Country features.
2. **Temporal Validation:** 
   - Standardized order and shipping timestamps to native `datetime64`.
   - Verified 0 chronological inversions (`shipping date >= order date`).
3. **Outlier Mitigation (IQR Winsorization):** 
   - Detected and capped 1,943 `Sales per customer` outliers at $461.93.
   - Capped 2,048 `Order Item Product Price` extreme leverage points.
4. **Feature Engineering:** 
   - Derived `Dispatch_Lead_Days` (fractional fulfillment duration).
   - Flagged `Is_Weekend_Dispatch` (carrier handoffs on Saturday/Sunday).
   - Computed `Delivery_SLA_Variance` (Actual vs. Scheduled transit duration).
5. **Standardization & Encoding:**
   - Applied Z-score standardization (`Sales per customer`, `Dispatch_Lead_Days`, `Days for shipping (real)`).
   - One-hot encoded `Shipping Mode` with `drop_first=True`.

## Verified Post-Cleaning Metrics (180,519 Records)
- **Null Values Remaining:** 0 across all analytical features.
- **Mean Actual Transit Time:** 3.498 days.
- **Mean Scheduled Transit Time:** 2.932 days.
- **Orders at Delay Risk:** 54.83% (`Late_delivery_risk` = 1).

## Artifacts in this Directory
- `Week2_Data_Preprocessing.ipynb`: Complete documented Python pipeline.
- `Week2_Data_Preprocessing_Report.docx`: Detailed strategic and technical report for Week 2 evaluation.
