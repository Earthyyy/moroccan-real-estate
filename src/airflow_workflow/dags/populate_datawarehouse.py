import os
import sys
from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.python import get_current_context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.jobs.cleaning_avito import clean_avito
from src.jobs.cleaning_yakeey import clean_yakeey
from src.jobs.loading import populate_datawarehouse


def find_data_paths(data: str, execution_date: datetime) -> tuple[list[str], list[str]]:
    raw_dir = f"./data/raw/{data}"
    folder_name = f"{execution_date.strftime('%Y-%m-%d')}"
    raw_paths = [
        os.path.join(raw_dir, file)
        for file in os.listdir(raw_dir)
        if file.startswith(folder_name)
    ]

    clean_paths = [path.replace("raw", "clean", 1) for path in raw_paths]

    return (raw_paths, clean_paths)


default_args = {"owner": "SMA", "retries": 0}


@dag(
    dag_id="populate",
    default_args=default_args,
    start_date=datetime(2024, 12, 12),
    schedule_interval="@daily",
)
def populate():

    # Scraping operators
    scraping_avito = BashOperator(
        task_id="scraping_avito",
        bash_command="cd ${AIRFLOW_HOME} && scrapy crawl avito",
    )
    scraping_yakeey = BashOperator(
        task_id="scraping_yakeey",
        bash_command="cd ${AIRFLOW_HOME} && scrapy crawl yakeey",
    )

    dev_dw_path = "./data/dw/datawarehouse.db"

    @task()
    def clean_avito_dag():
        context = get_current_context()
        execution_date = context["execution_date"]

        avito_raw_paths, avito_clear_paths = find_data_paths("avito", execution_date)
        for i in range(len(avito_raw_paths)):
            clean_avito(avito_raw_paths[i], avito_clear_paths[i])

    @task()
    def clean_yakeey_dag():
        context = get_current_context()
        execution_date = context["execution_date"]

        yakeey_raw_paths, yakeey_clear_paths = find_data_paths("yakeey", execution_date)
        for i in range(len(yakeey_raw_paths)):
            clean_yakeey(yakeey_raw_paths[i], yakeey_clear_paths[i])

    @task()
    def populate_datawarehouse_dag():
        context = get_current_context()
        execution_date = context["execution_date"]

        _, avito_clean_paths = find_data_paths("avito", execution_date)
        _, yakeey_clean_paths = find_data_paths("yakeey", execution_date)
        populate_datawarehouse([*avito_clean_paths, *yakeey_clean_paths], dev_dw_path)

    # Execute TaskFlow tasks and assign results to variables
    clean_avito_task = clean_avito_dag()
    clean_yakeey_task = clean_yakeey_dag()
    populate_datawarehouse_task = populate_datawarehouse_dag()

    # Define task dependencies
    scraping_avito >> clean_avito_task
    scraping_yakeey >> clean_yakeey_task
    [clean_yakeey_task, clean_avito_task] >> populate_datawarehouse_task


populate()
