import os
import sys

from airflow.models import DagBag

# Assuming your DAG is in a file named populate_dag.py in the dags directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_dag_load():
    dagbag = DagBag(dag_folder="./src/airflow_workflow/dags", include_examples=False)
    dag = dagbag.get_dag("populate")

    assert dag is not None
    assert len(dagbag.import_errors) == 0


def test_dag_structure():
    """Test the structure and number of tasks in the DAG"""
    dagbag = DagBag(dag_folder="./src/airflow_workflow/dags", include_examples=False)
    dag = dagbag.get_dag("populate")

    # Check task count
    assert len(dag.tasks) == 5  # Scraping tasks + 2 cleaning tasks + 1 populate task

    # Check task names
    task_names = [task.task_id for task in dag.tasks]
    expected_tasks = [
        "scraping_avito",
        "scraping_yakeey",
        "clean_avito_dag",
        "clean_yakeey_dag",
        "populate_datawarehouse_dag",
    ]
    assert set(task_names) == set(expected_tasks)


def test_task_dependencies():
    """Test the task dependencies"""
    dagbag = DagBag(dag_folder="./src/airflow_workflow/dags", include_examples=False)
    dag = dagbag.get_dag("populate")

    # Get tasks
    scraping_avito = dag.get_task("scraping_avito")
    scraping_yakeey = dag.get_task("scraping_yakeey")
    clean_avito_task = dag.get_task("clean_avito_dag")
    clean_yakeey_task = dag.get_task("clean_yakeey_dag")

    # Check downstream dependencies
    assert scraping_avito.downstream_task_ids == {"clean_avito_dag"}
    assert scraping_yakeey.downstream_task_ids == {"clean_yakeey_dag"}
    assert set(clean_avito_task.downstream_task_ids) == {"populate_datawarehouse_dag"}
    assert set(clean_yakeey_task.downstream_task_ids) == {"populate_datawarehouse_dag"}


def test_default_args():
    """Test the default arguments of the DAG"""
    dagbag = DagBag(dag_folder="./src/airflow_workflow/dags", include_examples=False)
    dag = dagbag.get_dag("populate")

    assert dag.default_args["owner"] == "SMA"
    assert dag.default_args["retries"] == 0
    assert dag.schedule_interval == "@daily"
