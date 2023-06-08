# from databricks_with_poetry.tasks.sample_etl_task import SampleETLTask
# from databricks_with_poetry.tasks.sample_ml_task import SampleMLTask
from pyspark.sql import SparkSession
# from pathlib import Path
# import mlflow
# import logging

# def test_jobs(spark: SparkSession, tmp_path: Path):
#     logging.info("Testing the ETL job")
#     common_config = {"database": "default", "table": "sklearn_housing"}
#     test_etl_config = {"output": common_config}
#     etl_job = SampleETLTask(spark, test_etl_config)
#     etl_job.launch()
#     table_name = f"{test_etl_config['output']['database']}.{test_etl_config['output']['table']}"
#     _count = spark.table(table_name).count()
#     assert _count > 0
#     logging.info("Testing the ETL job - done")

#     logging.info("Testing the ML job")
#     test_ml_config = {
#         "input": common_config,
#         "experiment": "/Shared/databricks_with_poetry/sample_experiment"
#     }
#     ml_job = SampleMLTask(spark, test_ml_config)
#     ml_job.launch()
#     experiment = mlflow.get_experiment_by_name(test_ml_config['experiment'])
#     assert experiment is not None
#     runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
#     assert runs.empty is False
#     logging.info("Testing the ML job - done")

import os
print( os.getenv("DATABRICKS_RUNTIME_VERSION"))
print(type(spark))

def spark_session():
    if os.getenv("DATABRICKS_RUNTIME_VERSION") is not None:
        # return spark
        return SparkSession.builder.getOrCreate()
#     else:
#         try:
#             # from databricks.connect import DatabricksSession
#             # from databricks.sdk.core import Config
#             # config = Config(profile=db_profile, cluster_id=db_cluster)
#             # return DatabricksSession.builder.sdkConfig(config).getOrCreate()
#             from databricks.connect import DatabricksSession
#             return DatabricksSession.builder.getOrCreate()
#         except (ModuleNotFoundError, ValueError):
#             from pyspark.sql import SparkSession
#             return SparkSession.builder.master("local[*]").getOrCreate()

print(type(spark_session()))

def prepare_spark():
    try:
        from databricks.connect import DatabricksSession
        return DatabricksSession.builder.getOrCreate()
    except ModuleNotFoundError as e:
        print("Databricks connect not installed")
        try:
            from pyspark.sql import SparkSession
            return SparkSession.builder.getOrCreate()
        except ModuleNotFoundError as e:
            print("Databricks Connect not installed and pyspark not available.")
            raise e
print(type(prepare_spark()))

from databricks.connect import DatabricksSession
spark2 = DatabricksSession.builder.getOrCreate()