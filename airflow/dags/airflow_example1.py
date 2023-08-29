"""
Example DAG to work with Databricks and accept parameters per environment.
Useful references:
https://github.com/seanjw13/anomaly_detection/blob/main/airflow/dags/anomaly_detection_dag.py
"""
from airflow import DAG
from airflow.models.param import Param
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator, DatabricksRunNowOperator
# rom airflow.providers.databricks.operators.databricks_repos import DatabricksReposUpdateOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import json
import config
import os

user = "dustin.vannoy@databricks.com"
notebook_name1 = "databricks_with_poetry/example_notebook"

dl_settings = json.dumps({"delta_table": "hive_metastore.sewi_database.anomaly_detection"})

# Example of updating a Databricks Repo to the latest code
repo_path = f"/Repos/{user}/databricks_with_poetry"
# update_repo = DatabricksReposUpdateOperator(task_id='update_repo', repo_path=repo_path, branch="main")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

new_cluster = {
    'spark_version': "13.2.x-scala2.12",
    'node_type_id': 'i3.xlarge',
    'aws_attributes': {
        'availability': 'ON_DEMAND'
    },
    'num_workers': 1
}

with DAG('databricks_multihop_dag',
    start_date=days_ago(2),
    schedule_interval=None,
    default_args=default_args,
    params={
        "env": "dev",
        "x": Param(5, type="integer", minimum=3),
        "silver_job_id": Param(1, type="integer"),
        "gold_job_id": Param(695905173765504, type="integer")
        }
    ) as dag:

    notebook_task_params = {
        'existing_cluster_id': '0730-172948-runts698',
        'notebook_task': {
            'notebook_path': f'{repo_path}/{notebook_name1}',
            # 'base_parameters': {
            #     'n': 48,
            #     'delta_lake': dl_settings
            # },
        },
    }

    bronze = DatabricksSubmitRunOperator(
    task_id='bronze_task',
    do_xcom_push=True,
    json=notebook_task_params
)
    # new_cluster=new_cluster,


    silver = DatabricksRunNowOperator(
        task_id='silver_task',
        databricks_conn_id='databricks_default',
        job_id="{{params.silver_job_id}}"
    )

    gold = DatabricksRunNowOperator(
        task_id='gold_task',
        databricks_conn_id='databricks_default',
        job_id="{{params.gold_job_id}}"
    )

# bronze >>
silver >> gold