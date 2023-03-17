from datetime import datetime
import logging
import shutil
import config
from helper import get_scripts
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "datakai",
    'depends_on_past': False,
    'email': "hstecher@datakai.net",
    'email_on_failure': False
}

scripts = get_scripts(config.SQL_DIR)
pg_hook = PostgresHook(postgres_conn_id='postgres_airflow')
conn = pg_hook.get_conn()


def find_old_logs():
    # Query old dag runs and build the log file paths to be deleted
    # Example log directory looks like this:
    # '/path/to/logs/dag_name/task_name/2021-01-11T12:25:00+00:00'
    sql = scripts['cleanup_logs.sql'].format(
        config.LOG_DIR, config.MAX_LOG_DAYS)
    return sql


def delete_log_dir(log_dir):
    try:
        # Recursively delete the log directory and its log contents (e.g, 1.log, 2.log, etc)
        shutil.rmtree(log_dir)
        logging.info(f"Deleted directory and log contents: {log_dir}")
    except OSError as e:
        logging.info(f"Unable to delete: {e.filename} - {e.strerror}")


def execute():
    logging.info("Fetching old logs to purge...")
    with conn.cursor() as cursor:
        cursor.execute(find_old_logs())
        rows = cursor.fetchall()
        logging.info(f"Found {len(rows)} log directories to delete...")
    for row in rows:
        delete_log_dir(row[0])


with DAG(
        dag_id="airflow_log_cleanup",
        start_date=days_ago(1),
        schedule_interval="00 00 * * *",
        default_args=default_args,
        max_active_runs=1,
        catchup=False,
) as dag:
    log_cleanup_op = PythonOperator(
        task_id="delete_old_logs",
        python_callable=execute
    )
