from datetime import datetime , timedelta
from airflow import DAG
from docker.types import Mount
from airflow.providers.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
import subprocess

CONN_ID=''
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
  'elt_and_dbt',
  default_args=default_args,
  description='ETL and DBT pipeline',
  start_date=days_ago(1),
  catchup=False
)

t1 = AirbyteTriggerSyncOperator(
  task_id='airbyte_postgres-bigquery',
  airbyte_conn_id='airbyte',
  connection_id=CONN_ID,
  asynchronous=False,
  timeout=3600,
  wait_seconds=3,
  dag=dag
)

t2 = DockerOperator(
    task_id='dbt-run',
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
        "run",
        "--profiles-dir",
        "/root",
        "--project-dir",
        "/opt/dbt"
      ],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    mounts=[
      Mount(source="E:/project_for_fun/datathon",target='/opt/dbt',type='bind'),
      Mount(source="C:/Users/John/.dbt",target='/root',type='bind')
    ] ,
    dag=dag
)

t1>>t2