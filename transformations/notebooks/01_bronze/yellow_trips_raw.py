# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from pyspark.sql.functions import current_timestamp
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# COMMAND ----------

# Obtains the year-month for 2 months prior to the current month in yyyy-MM format
two_months_ago = date.today() - relativedelta(months=5)
formatted_date = two_months_ago.strftime("%Y-%m")
print(f"formatted_date: {formatted_date}")
print(f'two_months_ago: {two_months_ago}')

# Read all Parquet files for the specified month from the landing directory into a DataFrame
df = spark.read.format("parquet").load(f"/Volumes/nyctaxi/00_landing/data_sources/nyctaxi_yellow/{formatted_date}")

# COMMAND ----------

# Add a column to capture when the data was processed
df = df.withColumn("processed_timestamp", current_timestamp())

# COMMAND ----------

# Write the DataFrame to a Unity Catalog managed Delta table in the bronze schema, appending the new data
df.write.mode("append").saveAsTable("nyctaxi.01_bronze.yellow_trips_raw")