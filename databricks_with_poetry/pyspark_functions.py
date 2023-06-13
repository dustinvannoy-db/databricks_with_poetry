# from databricks.sdk.runtime import *
from pyspark.sql.functions import concat
import os


def create_sample_dataframe(spark):
    df = spark.createDataFrame([["test1", 1],["test2", 2]])
    df = df.withColumn("combined_val", concat("_1", "_2"))
    
    return df

def databricks_list_files(dbutils):
    files = dbutils.fs.ls("dbfs:/Users/dustin.vannoy@databricks.com/field_demos")
    for f in files:
        print(f)

def prepare_spark():
    try:
        from databricks.connect import DatabricksSession
        return DatabricksSession.builder.getOrCreate()
    except ModuleNotFoundError as e:
        try:
            from pyspark.sql import SparkSession
            return SparkSession.builder.getOrCreate()
        except ModuleNotFoundError as e:
            print("Databricks Connect not installed and pyspark not available.")
            raise e
