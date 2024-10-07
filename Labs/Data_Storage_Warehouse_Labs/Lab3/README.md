### Lab Title: **Advance BigQuery: Data Transformation and Query Optimization**

### Lab Objective:
In this lab, you will learn how to:
1. Perform advanced SQL transformations in BigQuery.
2. Optimize query performance using partitioning and clustering.
3. Work with user-defined functions (UDFs) for custom data processing.
4. Use window functions to aggregate data over partitions.
5. Create materialized views to improve query efficiency.

---

### Prerequisites:
- Basic knowledge of SQL and BigQuery.
- Access to Google Cloud Platform with BigQuery enabled.
- A dataset available in BigQuery or instructions to import a public dataset.

---

### Lab Setup:

1. **Create a Dataset in BigQuery:**
   - Open the [Google Cloud Console](https://console.cloud.google.com/).
   - Navigate to **BigQuery**.
   - Create a new dataset called `sales_data_analysis`.

2. **Use the Public Dataset (or Custom Data):**
   - We will be using a public dataset such as `bigquery-public-data.austin_bikeshare.bikeshare_trips`.
   - If you want to use custom data, upload a CSV file to a Google Cloud Storage bucket and load it into BigQuery.

---

### Step 1: **Advanced Data Transformation with SQL**

You will begin by writing SQL queries that perform complex transformations on the dataset. You’ll filter, aggregate, and join tables.

1. **Filter Data and Aggregate**
   - Query to filter data by date and group by specific conditions.

```sql
SELECT 
  start_station_name,
  COUNT(trip_id) AS total_rides,
  EXTRACT(MONTH FROM start_time) AS ride_month
FROM 
  `bigquery-public-data.austin_bikeshare.bikeshare_trips`
WHERE 
  start_time BETWEEN '2022-01-01' AND '2022-12-31'
GROUP BY 
  start_station_name, ride_month
ORDER BY 
  total_rides DESC;
```

2. **JOIN Example (Merging Data)**
   - Demonstrate how to join two tables (self-join in this case) to enrich data.

```sql
SELECT 
  a.start_station_name, 
  a.total_rides AS rides_2022, 
  b.total_rides AS rides_2023
FROM (
  SELECT start_station_name, COUNT(trip_id) AS total_rides
  FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
  WHERE EXTRACT(YEAR FROM start_time) = 2022
  GROUP BY start_station_name
) AS a
JOIN (
  SELECT start_station_name, COUNT(trip_id) AS total_rides
  FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`
  WHERE EXTRACT(YEAR FROM start_time) = 2023
  GROUP BY start_station_name
) AS b
ON a.start_station_name = b.start_station_name;
```

---

### Step 2: **Optimizing Query Performance**

1. **Partitioning Tables:**
   - Partition the dataset by the `start_time` column to improve query performance.

```sql
CREATE OR REPLACE TABLE `your_project.sales_data_analysis.partitioned_trips`
PARTITION BY DATE(start_time) AS
SELECT * FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`;
```

2. **Clustering:**
   - Cluster the table by `start_station_name` to enhance performance for queries filtering by station name.

```sql
CREATE OR REPLACE TABLE `your_project.sales_data_analysis.clustered_trips`
PARTITION BY DATE(start_time)
CLUSTER BY start_station_name AS
SELECT * FROM `bigquery-public-data.austin_bikeshare.bikeshare_trips`;
```

---

### Step 3: **Working with User-Defined Functions (UDFs)**

You will create and use a user-defined function to calculate distance between bike stations using latitude and longitude coordinates.

1. **Create the UDF:**

```sql
CREATE OR REPLACE FUNCTION `your_project.sales_data_analysis.calculate_distance`(
  lat1 FLOAT64, lon1 FLOAT64, lat2 FLOAT64, lon2 FLOAT64)
RETURNS FLOAT64
LANGUAGE js AS """
  function toRadians(deg) { return deg * (Math.PI / 180); }
  var R = 6371; // Radius of the Earth in km
  var dLat = toRadians(lat2 - lat1);
  var dLon = toRadians(lon2 - lon1);
  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
          Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
          Math.sin(dLon/2) * Math.sin(dLon/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  var distance = R * c;
  return distance;
""";
```

2. **Use the UDF in a Query:**

```sql
SELECT 
  start_station_name, 
  end_station_name, 
  `your_project.sales_data_analysis.calculate_distance`(
    start_station_latitude, start_station_longitude, 
    end_station_latitude, end_station_longitude) AS distance_km
FROM 
  `bigquery-public-data.austin_bikeshare.bikeshare_trips`
WHERE 
  distance_km IS NOT NULL
ORDER BY distance_km DESC
LIMIT 10;
```

---

### Step 4: **Using Window Functions**

Window functions allow you to perform calculations across a set of table rows related to the current row.

1. **Rank the Start Stations by Rides:**

```sql
SELECT 
  start_station_name,
  COUNT(trip_id) AS total_rides,
  RANK() OVER (ORDER BY COUNT(trip_id) DESC) AS rank
FROM 
  `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY 
  start_station_name
ORDER BY 
  rank;
```

---

### Step 5: **Creating Materialized Views**

Materialized views are used to store precomputed query results, improving query performance for frequently accessed data.

1. **Create a Materialized View:**

```sql
CREATE MATERIALIZED VIEW `your_project.sales_data_analysis.materialized_view`
AS 
SELECT 
  start_station_name, 
  COUNT(trip_id) AS total_rides
FROM 
  `bigquery-public-data.austin_bikeshare.bikeshare_trips`
GROUP BY 
  start_station_name;
```

2. **Querying the Materialized View:**

```sql
SELECT * FROM `your_project.sales_data_analysis.materialized_view`
ORDER BY total_rides DESC;
```

---

### Step 6: **Final Cleanup and Review**

1. **Review Table Partitions and Clustering:**

```sql
SELECT
  table_id, 
  creation_time, 
  partitioning_type, 
  clustering_fields
FROM 
  `your_project.your_dataset.INFORMATION_SCHEMA.TABLES`
WHERE 
  table_id = 'partitioned_trips' OR table_id = 'clustered_trips';
```

2. **Drop Tables and Views When Done:**

```sql
DROP TABLE IF EXISTS `your_project.sales_data_analysis.partitioned_trips`;
DROP TABLE IF EXISTS `your_project.sales_data_analysis.clustered_trips`;
DROP MATERIALIZED VIEW IF EXISTS `your_project.sales_data_analysis.materialized_view`;
```

---

### Conclusion:
In this lab, you've learned how to:
- Use advanced SQL queries in BigQuery.
- Implement optimizations using partitioning, clustering, and materialized views.
- Create and use User-Defined Functions.
- Apply window functions for analytics.

---

You can now upload this to GitHub as a structured lab. Make sure to include a `README.md` with clear instructions for users to follow along.
