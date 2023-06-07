from pyspark.sql import functions as fn
import pyspark_functions
import os

def get_spark_session():
    """Return spark variable if available (will be true when run on Databricks),
        otherwise create new one from local using databricks-connect (version 13.0 or greater)
    """
    try:
        return spark
    except NameError:
        from databricks.connect import DatabricksSession
        from databricks.sdk.core import Config
        db_profile = os.getenv("DB_PROFILE", "e2-field-eng")
        db_cluster = os.getenv("DB_CLUSTER")
        config = Config(profile=db_profile, cluster_id=db_cluster)
        return DatabricksSession.builder.sdkConfig(config).getOrCreate()

spark = pyspark_functions.prepare_spark()
df = pyspark_functions.create_sample_dataframe(spark)
updated_df = df.withColumn("created_date", fn.current_date())
updated_df.show()