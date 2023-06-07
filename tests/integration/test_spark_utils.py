import pytest
import os

from databricks_with_poetry import pyspark_functions

db_profile = os.getenv("DB_PROFILE", "field-eng")
db_cluster = os.getenv("DB_CLUSTER")

@pytest.fixture(scope="session")
def spark_session():

    if os.getenv("DATABRICKS_RUNTIME_VERSION") is not None:
        return spark
    else:
        try:
            # from databricks.connect import DatabricksSession
            # from databricks.sdk.core import Config
            # config = Config(profile=db_profile, cluster_id=db_cluster)
            # return DatabricksSession.builder.sdkConfig(config).getOrCreate()
            from databricks.connect import DatabricksSession
            return DatabricksSession.builder.getOrCreate()
        except (ModuleNotFoundError, ValueError):
            from pyspark.sql import SparkSession
            return SparkSession.builder.master("local[*]").getOrCreate()

@pytest.mark.integration()
def test_create_sample_dataframe_valid_df(spark_session):
    return_df = pyspark_functions.create_sample_dataframe(spark_session)
    assert return_df.count() == 2
    # assert isinstance(return_df, DataFrame)
    print("Completed test for create_sample_dataframe")

@pytest.mark.integration()
def test_prepare_spark():
    lcl_spark = pyspark_functions.prepare_spark()
    print(type(lcl_spark))
    assert str(type(lcl_spark)).find('SparkSession') > -1

if __name__ == "__main__":
    # test_create_sample_dataframe_valid_df()
    print(pytest.main(["-p", "no:cacheprovider"]))
