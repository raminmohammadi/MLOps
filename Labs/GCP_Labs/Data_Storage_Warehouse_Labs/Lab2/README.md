
BIGQUERY ADVANCED QUERYING & LOOKER STUDIO VISUALIZATION LAB

1. INTRODUCTION
---------------
In this lab, I performed an end-to-end data analytics workflow using
Google BigQuery and Looker Studio. I uploaded a dataset, explored its
schema, wrote advanced SQL queries, saved the results as new tables,
created visualizations in BigQuery, and built an interactive dashboard
in Looker Studio. This document summarizes the full process.

------------------------------------------------------------

2. DATASET INFORMATION
----------------------
Project: clean-equinox-472523-c4
Dataset: ecommerce_dw
Primary Table: orders_ext

The dataset contains e-commerce order-level data with fields including:

- order_id
- order_date
- customer_id
- state
- channel
- category
- quantity
- unit_price_usd
- line_amount_usd

------------------------------------------------------------

3. WORKFLOW OVERVIEW
--------------------
The steps I completed in this lab are:

1. Uploaded the dataset into BigQuery
2. Explored and validated the table schema
3. Wrote three SQL queries for analysis
4. Saved the query results as CSV, Sheets, and BigQuery tables
5. Built visualizations in BigQuery
6. Connected BigQuery tables to Looker Studio
7. Created a dashboard with multiple charts

------------------------------------------------------------

4. SQL ANALYSIS
---------------

4.1 Query 1 — Total Sales by Category
-------------------------------------
SQL:
SELECT
  category,
  SUM(line_amount_usd) AS total_sales_usd
FROM `clean-equinox-472523-c4.ecommerce_dw.orders_ext`
GROUP BY category
ORDER BY total_sales_usd DESC;

Purpose:
Identifies the highest revenue-generating categories.

4.2 Query 2 — Revenue by Channel (Using HAVING)
------------------------------------------------
SQL:
SELECT
  channel,
  SUM(line_amount_usd) AS total_revenue
FROM `clean-equinox-472523-c4.ecommerce_dw.orders_ext`
GROUP BY channel
HAVING SUM(line_amount_usd) > 5000
ORDER BY total_revenue DESC;

Purpose:
Filters channels that exceed a minimum revenue threshold.

4.3 Query 3 — Price Segmentation Using CASE
-------------------------------------------
SQL:
SELECT
  category,
  CASE
    WHEN unit_price_usd < 20 THEN 'Budget'
    WHEN unit_price_usd BETWEEN 20 AND 100 THEN 'Standard'
    ELSE 'Premium'
  END AS price_segment,
  COUNT(order_id) AS num_orders,
  SUM(line_amount_usd) AS segment_sales
FROM `clean-equinox-472523-c4.ecommerce_dw.orders_ext`
GROUP BY category, price_segment
ORDER BY category, price_segment;

Purpose:
Classifies each category into Budget, Standard, or Premium price segments
and summarizes performance.

------------------------------------------------------------

5. BIGQUERY VISUALIZATIONS
--------------------------
In BigQuery, I used the Visualization tab to create:

- Bar chart: Total sales by category
- Scatter plot: Unit price vs. quantity
- Table summaries: Category-level comparisons

These visualizations helped validate the query results.

------------------------------------------------------------

6. SAVING QUERY RESULTS
-----------------------
I saved my BigQuery results in multiple ways:

- CSV files (local)
- Google Sheets (cloud)
- New BigQuery tables, including:
  * cat_price_seg
  * sales_bucket
  * sales_channel_by_revenue

These tables were used directly in Looker Studio.

------------------------------------------------------------

7. LOOKER STUDIO DASHBOARD
--------------------------
Data sources added:

- orders_ext
- cat_price_seg
- sales_bucket
- sales_channel_by_revenue

Visualizations included:

- Table: Quantity by category
- Bar chart: Quantity by category
- Donut chart: Category share by avg unit price
- Bar charts: Sales by category and channel
- Segmentation charts: Budget, Standard, Premium

The dashboard was formatted with consistent colors, headings,
and layout.

------------------------------------------------------------

8. KEY INSIGHTS
---------------
- Some categories significantly outperform others in sales.
- Web is the strongest revenue channel.
- Most products fall in the Standard price segment.
- Premium items contribute meaningfully to revenue.
- Unit price and quantity show identifiable patterns.

------------------------------------------------------------

9. CONCLUSION
-------------
This lab helped me build practical skills in cloud-based data analysis.
I worked with BigQuery for SQL processing, performed segmentation and
aggregation, saved transformed data, and created a complete Looker Studio
dashboard. This workflow closely resembles real-world analytical tasks.
