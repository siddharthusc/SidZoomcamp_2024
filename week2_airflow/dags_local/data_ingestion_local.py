import os
from airflow import DAG
from datetime import datetime

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
dataset_file = "green_tripdata_2019-09.csv.gz"
dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/{dataset_file}"

local_workflow = DAG(
    dag_id = "localIngestionDAG",
    schedule_interval = '0 6 2 * *',
    start_date = datetime(2021,1,1)
)

with local_workflow:
    wget_task = BashOperator(
        task_id = "wget",
        bash_command = f'curl -sSL {dataset_url} > {path_to_local_home}/green_taxi.csv.gz'
    )

    ingest_task = BashOperator(
        task_id = "ingest",
        bash_command = f'ls {path_to_local_home}'
    )

    wget_task >> ingest_task