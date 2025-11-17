📘 Data Monitoring with Evidently AI – README

🔍 Overview

In this lab, I used Evidently AI to perform data monitoring and evaluate how the distribution of incoming (production) data compares to a reference dataset. The goal was to detect data drift, analyze data quality, and generate a shareable HTML monitoring report that can be archived or sent to collaborators.

This exercise helped me understand how real-world MLOps systems track changes in data over time to maintain model reliability.

📁 What I Did in This Lab

✔ Loaded the Adult Income dataset
✔ Split it into:

Reference data (baseline/training-like)

Production data (simulated live data)

✔ Defined a schema for Evidently:

Numerical columns

Categorical columns

✔ Created an Evidently monitoring report using:

DataSummaryPreset → data quality + statistics

DataDriftPreset → feature-level and dataset-level drift detection

✔ Ran the report comparing reference and production data
✔ Saved the full report as an HTML file for explainability and versioning

🧠 Why This Matters

Machine learning systems depend on the assumption that new data looks like training data.
But in production: feature distributions drift, new categories appear
, missing values increase and schemas change unexpectedly.

These changes reduce model performance.

By using Evidently, I learned how to automatically detect these issues and generate reports that track data health over time. This is a core concept in MLOps, especially when models are deployed long-term.


🧩 What I Changed From the Original Lab

To extend the base lab and demonstrate my understanding, I made the following enhancements:

1️⃣ I added the DataSummaryPreset.

This allowed me to monitor:

missing values

schema consistency

cardinality

summary statistics

This gives a more complete picture of data health instead of drift alone.

2️⃣ I saved the report as an HTML file.

Exporting the report to:

adult_data_monitoring_report.html


allowed me to:

share the results

archive the report

keep historical monitoring logs

This is a standard MLOps best practice for explainability and version control.

📌 Output

After running the notebook, I generated:

adult_data_monitoring_report.html
