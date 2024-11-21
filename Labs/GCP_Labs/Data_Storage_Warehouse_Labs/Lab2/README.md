# Intermediate Lab: Advanced Querying and Visualization in BigQuery


You can watch the toturial video at [Video](https://youtu.be/pAg5D4K3nkU)

## Objective

In this lab, you will learn how to:
- Write complex SQL queries to analyze data using BigQuery.
- Utilize BigQuery's built-in visualization tools for insights.
- Export and share your query results for further analysis or reporting.

## Prerequisites

Before you begin, ensure that you:
- Have a dataset loaded into BigQuery (from previous labs).
- Are familiar with basic SQL querying and data visualization concepts.

---

## Steps

### Step 1: Perform Data Analysis Using Intermediate SQL Queries

- Access your existing BigQuery dataset and table. (If you do not know how to create a bigquery table, refer to lab1)
- Write complex SQL queries to perform data analysis:
  - Use aggregate functions like `SUM`, `AVG`, `COUNT` to generate insights.
  - Apply `GROUP BY` and `ORDER BY` to structure your data effectively.

**Sample Query**:
```sql
SELECT 
    Species,
    AVG(SepalLengthCm) AS avg_sepal_length,
    AVG(SepalWidthCm) AS avg_sepal_width,
    AVG(PetalLengthCm) AS avg_petal_length,
    AVG(PetalWidthCm) AS avg_petal_width
FROM 
    `mlopslabsstorage001.iris.iris`
GROUP BY 
    Species
ORDER BY 
    avg_sepal_length DESC;
```

Experiment with different functions and combinations of SQL clauses to gain insights from your data.

---

### Step 2: Visualize Data Using BigQuery UI

After running your queries, visualize the results directly within BigQuery:
- In the BigQuery console, run your query.
- Click on **Explore Data** and choose a visualization type that best represents your data (e.g., bar chart, pie chart, line chart).
- Customize your chart with appropriate axis labels, colors, and other formatting options.

> **Task**: Create at least two different visualizations from your query results, such as:
> - A **bar chart** comparing the average Sepal Length of different species.
> - A **scatter plot** showing the relationship between average Petal Length and Sepal Width across species.

---

### Step 3: Export and Share Query Results

Once you've completed your analysis, export the query results for sharing with others or for further analysis:
- **Export to Google Sheets**: Run the query, click on the **Save Results** button, and select **Google Sheets**. The data will be exported directly to a new Google Sheets file.
- **Download as CSV**: Alternatively, download the query results as a CSV file for use in other tools like Excel or Google Data Studio.

#### Steps to Export to Google Sheets:

1. Run your query.
2. Click the **Save Results** button at the bottom of the BigQuery interface.
3. Choose **Google Sheets** from the dropdown.
4. Your data will be exported directly to Google Sheets, ready for sharing or further processing.

---

## Looker Studio Visualization Sample

To enhance your data visualization skills further, import your dataset into **Looker Studio** and create professional visualizations. Here's a guide on setting up a few common charts using the Iris dataset:

1. **Import Dataset**: In Looker Studio, connect to your BigQuery dataset (Iris dataset in this case).
2. **Create Visualizations**:
   - **Bar Chart**: Visualize the average sepal lengths for each species. 
   - **Scatter Plot**: Compare the relationship between sepal width and petal width.
3. **Customize the Dashboard**: Adjust colors, add filters, and modify the layout for a comprehensive dashboard.

---

## Conclusion

This lab guides you through more advanced querying techniques in BigQuery, using both SQL and built-in visualization tools to analyze and visualize the Iris dataset. You also learned how to export and share data for further use, building critical skills in data analysis and presentation.
