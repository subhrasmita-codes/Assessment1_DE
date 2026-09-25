import sys
sys.path.insert(0, "/opt/airflow")

from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator, get_current_context
from airflow.operators.bash import BashOperator
from pendulum import datetime

from ingestion.weather_api import fetch_daily
from ingestion.load import load_daily


def extract_and_load():
    context = get_current_context()
    date_str = context["data_interval_start"].strftime("%Y-%m-%d")

    rows = fetch_daily(date_str)
    load_daily(date_str, rows)


with DAG(
    dag_id="weather_daily",
    start_date=datetime(2026, 8, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
    },
    dagrun_timeout=timedelta(minutes=30),
    tags=["weather", "data-engineering"],
) as dag:

    extract_load = PythonOperator(
        task_id="extract_load",
        python_callable=extract_and_load,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt && dbt test",
    )

    extract_load >> dbt_run >> dbt_test