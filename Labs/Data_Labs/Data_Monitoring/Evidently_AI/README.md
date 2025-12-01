Data Monitoring with Evidently AI – README

Overview

In this lab, I used Evidently AI to perform data monitoring and evaluate how the distribution of incoming (production) data compares to a reference dataset. The goal was to detect data drift, analyze data quality, and generate a shareable HTML monitoring report that can be archived or sent to collaborators.

This exercise helped me understand how real-world MLOps systems track changes in data over time to maintain model reliability.

 What I Did in This Lab

1. Loaded the Adult Income dataset
2. Split it into:

2.1 Reference data (baseline/training-like)

2.2 Production data (simulated live data)

3. Defined a schema for Evidently:

3.1 Numerical columns

3.2 Categorical columns

4. Created an Evidently monitoring report using:

4.1 DataSummaryPreset → data quality + statistics

4.2 DataDriftPreset → feature-level and dataset-level drift detection

5. Ran the report comparing reference and production data
6. Saved the full report as an HTML file for explainability and versioning

Why This Matters: 

Machine learning systems depend on the assumption that new data looks like training data.
But in production: feature distributions drift, new categories appear
, missing values increase and schemas change unexpectedly.

These changes reduce model performance.

By using Evidently, I learned how to automatically detect these issues and generate reports that track data health over time. This is a core concept in MLOps, especially when models are deployed long-term.


What I Changed From the Original Lab

To extend the base lab and demonstrate my understanding, I made the following enhancements:

A) I added the DataSummaryPreset.

This allowed me to monitor: missing values, schema consistency, cardinality, and summary statistics

This gives a more complete picture of data health instead of drift alone.

Result : I saved the report as an HTML file.

Exporting the report to: adult_data_monitoring_report.html

This allowed me to: share the results, archive the report and keep historical monitoring logs

This is a standard MLOps best practice for explainability and version control.

