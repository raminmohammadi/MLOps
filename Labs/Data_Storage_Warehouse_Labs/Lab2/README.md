# Intermediate Lab - Advanced Querying and Visualization in BigQuery

## Objective
In this lab, you will learn how to:
- Write more complex SQL queries to analyze data in BigQuery.
- Use BigQuery's built-in visualization tools.
- Export and share query results for further analysis or reporting.

## Prerequisites
- A dataset already loaded into BigQuery (from previous labs).
- Familiarity with basic SQL querying and data visualization concepts.

---

## Steps

### Step 1: Perform Data Analysis Using Intermediate SQL Queries
- Access your existing BigQuery dataset and table.
- Write more complex queries to analyze your data:
  - Use aggregate functions (`SUM`, `AVG`, `COUNT`) to generate insights.
  - Apply `GROUP BY` and `ORDER BY` clauses to structure the data.

**Example Query:**
```sql
SELECT product_category, AVG(sales) AS avg_sales
FROM `<PROJECT_ID>.<DATASET_NAME>.<TABLE_NAME>`
GROUP BY product_category
ORDER BY avg_sales DESC;
```
- Experiment with different functions and combinations to gain insights into your data.

---

### Step 2: Visualize Data Using BigQuery UI
- In the BigQuery console, run your query and select the **Explore data** option.
- Choose a visualization type, such as a bar chart, pie chart, or line chart, based on your query results.
- Customize the chart by adjusting the axes, labels, and colors to make your data more comprehensible.

> **Task:** Create at least two different visualizations using the results of your queries.

---

### Step 3: Export and Share Query Results
- Once you've completed your analysis, export the query results for use in other tools or for sharing with stakeholders.
- You can export the data to:
  - **Google Sheets**: Click on the **Export** option and choose **Google Sheets**.
  - **CSV File**: Download the results in CSV format for use in Excel or other applications.

#### How to Export to Google Sheets
1. Run your query and click on the **Save Results** button.
2. Select **Google Sheets**, and your data will be exported directly.

---

## Conclusion
This lab allows you to practice advanced data analysis and visualization techniques using BigQuery, reinforcing the importance of extracting and sharing insights from data.
