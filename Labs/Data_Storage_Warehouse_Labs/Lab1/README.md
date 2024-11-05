# Data Storage and Warehousing using Google Cloud (GCP)

You can watch the toturial video at [Kubernetes-lab2](https://youtu.be/8AzHqHQWTCw)

## Introduction

In today’s data-driven landscape, efficiently storing, managing, and analyzing large volumes of data is critical. Google Cloud Platform (GCP) offers powerful services to simplify these tasks. Two essential services in this space are **Google Cloud Storage (GCS)** and **Google BigQuery**.

**Google Cloud Storage (GCS)** provides scalable and secure storage for any type of data, acting as a foundation for cloud-based storage solutions. It integrates seamlessly with other Google services like BigQuery, making it ideal for building data pipelines.

**Google BigQuery** is a serverless data warehouse designed to process large datasets using SQL queries. Its fully-managed infrastructure enables you to analyze petabytes of data in seconds, making it a key tool for businesses seeking quick insights from their data.

This lab introduce you to how GCS and BigQuery work together to provide a full solution for cloud-based data storage and analysis.

---

##  Google Cloud Storage (GCS)

- **Scalable Data Storage**  
  GCS is designed to store data of any size, from small files to large datasets. It provides a centralized location for securely storing data that can be easily accessed from anywhere.
  
- **Bucket Creation and Management**  
  You will learn how to create and manage GCS buckets, which serve as containers for your data. You’ll set permissions, manage access with service accounts, and upload datasets.

- **Versioning and Lifecycle Policies**  
  GCS enables versioning to track changes and lifecycle management for automatic retention policies. These features help you manage data effectively over time.

---

##  Google BigQuery

- **Fast, Serverless Analytics**  
  BigQuery allows you to analyze massive datasets using SQL, without needing to manage any infrastructure. You’ll explore how to run queries and extract insights quickly and efficiently.

- **Dataset and Table Creation**  
  You will create datasets and tables in BigQuery, and load data from GCS. This data can then be queried using SQL to perform analysis and aggregations.

- **Seamless Integration with GCS**  
  BigQuery’s seamless integration with GCS allows you to load data directly from your storage bucket for analysis, making it easy to combine the two services for efficient data workflows.

---

## Conclusion

By completing these labs, you'll gain practical experience in setting up cloud storage with GCS and analyzing data with BigQuery. Together, they provide a robust solution for managing and processing large-scale datasets in the cloud.


