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
        return spark
    except NameError:
        try:
            from databricks.connect import DatabricksSession
            return DatabricksSession.builder.getOrCreate()
        except ModuleNotFoundError as e:
            print("Not running on Databricks cluster and Databricks Connect not installed.")
            raise e

# def get_spark_session():
#     if os.getenv("DATABRICKS_RUNTIME_VERSION") is not None:
#         from pyspark.sql import SparkSession
#         return SparkSession.builder.getOrCreate()
#     else:
#         try:
#             from databricks.connect import DatabricksSession
#             from databricks.sdk.core import Config
#             db_profile = os.getenv("DB_PROFILE", "field-eng")
#             db_cluster = os.getenv("DB_CLUSTER")
#             config = Config(profile=db_profile, cluster_id=db_cluster)
#             return DatabricksSession.builder.sdkConfig(config).getOrCreate()
#         except ModuleNotFoundError:
#             from pyspark.sql import SparkSession
#             return SparkSession.builder.getOrCreate()