# BigQuery Spark-SQL Batch ETL

## Problem Statement
An Airline company called Spark Airways, recieves JSON flight data on daily basis in its GCS bucket. It contains fields such as id, flight_date, airline_code, flight_num, source_airport, destination_airport, departure_time, departure_delay, arrival_time, arrival_delay, airtime, and distance. Design an ETL pipeline for daily data ingestion of this flight data to produce average flight delays by flight number and distance as tables in BigQuery. 

## Technologies Used
- Spark SQL
- pyspark
- Airflow (Cloud Composer)
- GCS (Google Cloud Storage)
- BigQuery
- Shell

## ETL Pipeline
1. Create BigQuery tables avg_delays_by_flight_nums and avg_delays_by_distance using BQ command shell script. 
2. Create ephemeral Dataproc Cluster.
3. Load daily JSON file as a dataframe in pyspark script (flights-etl.py) and apply transformations to flight delays data using spark-sql to produre output tables.
4. Save the transformed data into GCS output bucket.
5. Load the transformed data from GCS output bucket into Bigquery partitioned tables.
6. Delete ephemeral Dataproc Cluster and transformed output data from GCS output bucket.
7. Use Apache Airflow to create DAGs and automate the Spark ETL batch processing job.