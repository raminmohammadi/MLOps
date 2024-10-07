### Lab Title: **Advanced BigQuery: Data Transformation and Query Optimization**

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
- A dataset available in BigQuery or instructions to import your CSV dataset (`Bikeshare_Trip_Dataset.csv`).

---

### Lab Setup:

We will use the `mlopslabsstorage001.bikeshare001.bikeshare` dataset.

---

### Step 1: **Advanced Data Transformation with SQL**

1. **Filter Data and Aggregate**

```sql
SELECT 
  start_station_name,
  COUNT(trip_id) AS total_rides,
  EXTRACT(MONTH FROM start_time) AS ride_month
FROM 
  `mlopslabsstorage001.bikeshare001.bikeshare`
WHERE 
  start_time BETWEEN '2023-10-01' AND '2024-10-01'
GROUP BY 
  start_station_name, ride_month
ORDER BY 
  total_rides DESC;
```

This query filters the dataset for trips that occurred between October 2023 and October 2024. It groups the trips by the start station and the month of the trip, counting the total number of rides for each station in each month and orders the result by the number of rides in descending order.

---

2. **JOIN Example (Merging Data)**

```sql
SELECT 
  a.start_station_name, 
  a.total_rides AS rides_2023, 
  b.total_rides AS rides_2024
FROM (
  SELECT start_station_name, COUNT(trip_id) AS total_rides
  FROM `mlopslabsstorage001.bikeshare001.bikeshare`
  WHERE EXTRACT(YEAR FROM start_time) = 2023
  GROUP BY start_station_name
) AS a
JOIN (
  SELECT start_station_name, COUNT(trip_id) AS total_rides
  FROM `mlopslabsstorage001.bikeshare001.bikeshare`
  WHERE EXTRACT(YEAR FROM start_time) = 2024
  GROUP BY start_station_name
) AS b
ON a.start_station_name = b.start_station_name;
```

This query compares the number of rides that started at each station between 2023 and 2024 by performing a self-join on the `start_station_name`.

---

### Step 2: **Optimizing Query Performance**

1. **Partitioning Tables:**

```sql
CREATE OR REPLACE TABLE `mlopslabsstorage001.bikeshare001.partitioned_trips`
PARTITION BY DATE(start_time) AS
SELECT * FROM `mlopslabsstorage001.bikeshare001.bikeshare`;
```

This query creates a partitioned table based on the `start_time` column, allowing for faster queries when filtering by date.

---

2. **Clustering:**

```sql
CREATE OR REPLACE TABLE `mlopslabsstorage001.bikeshare001.clustered_trips`
PARTITION BY DATE(start_time)
CLUSTER BY start_station_name AS
SELECT * FROM `mlopslabsstorage001.bikeshare001.bikeshare`;
```

This query creates a table that is partitioned by date and clustered by the `start_station_name`. Clustering allows for more efficient queries when filtering by station names.

---

### Step 3: **Working with User-Defined Functions (UDFs)**

1. **Create the UDF:**

```sql
CREATE OR REPLACE FUNCTION `mlopslabsstorage001.bikeshare001.calculate_distance`(
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

This creates a User-Defined Function (UDF) that calculates the distance between two points (start and end stations) based on their latitude and longitude coordinates using the haversine formula.

---

2. **Use the UDF in a Query:**

```sql
SELECT 
  start_station_name, 
  end_station_name, 
  `mlopslabsstorage001.bikeshare001.calculate_distance`(
    start_station_latitude, start_station_longitude, 
    end_station_latitude, end_station_longitude) AS distance_km
FROM 
  `mlopslabsstorage001.bikeshare001.bikeshare`
ORDER BY distance_km DESC
LIMIT 10;
```

This query uses the UDF to calculate the distance between the start and end stations for each trip and returns the 10 longest trips.

---

### Step 4: **Using Window Functions**

1. **Rank the Start Stations by Rides:**

```sql
SELECT 
  start_station_name,
  COUNT(trip_id) AS total_rides,
  RANK() OVER (ORDER BY COUNT(trip_id) DESC) AS rank
FROM 
  `mlopslabsstorage001.bikeshare001.bikeshare`
GROUP BY 
  start_station_name
ORDER BY 
  rank;
```

This query ranks each station based on the total number of rides starting from that station, providing a way to see the busiest stations.

---

### Step 5: **Creating Materialized Views**

1. **Create a Materialized View:**

```sql
CREATE MATERIALIZED VIEW `mlopslabsstorage001.bikeshare001.materialized_view`
AS 
SELECT 
  start_station_name, 
  COUNT(trip_id) AS total_rides
FROM 
  `mlopslabsstorage001.bikeshare001.bikeshare`
GROUP BY 
  start_station_name;
```

This creates a materialized view that precomputes and stores the total rides per station, improving performance for future queries.

---

2. **Querying the Materialized View:**

```sql
SELECT * FROM `mlopslabsstorage001.bikeshare001.materialized_view`
ORDER BY total_rides DESC;
```

This query retrieves the results from the materialized view, showing the stations ordered by the number of trips that started there.

---

### Conclusion:
In this lab, you've learned how to:
- Use advanced SQL queries in BigQuery.
- Implement optimizations using partitioning, clustering, and materialized views.
- Create and use User-Defined Functions.
- Apply window functions for analytics.

This lab now reflects the actual date range in your dataset and should work correctly. Let me know if you need further adjustments!
