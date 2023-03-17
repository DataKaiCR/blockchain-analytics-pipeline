import os
from datetime import timedelta
from helper import get_scripts
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.dates import days_ago
from psycopg2 import sql

CURR_DIR = os.getcwd()
SQL_PATH = os.path.join(CURR_DIR, 'dags','sql')

default_args = {
    'owner': 'datakai',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def deploy_script():
    scripts = get_scripts(SQL_PATH)
    return scripts

def create_user_admin():
    hook = PostgresHook(
        postgres_conn_id = 'postgres_airflow'
    )
    conn = hook.get_conn()
    with conn as c:
        cursor = c.cursor()
        cursor.execute(deploy_script()['create_user_admin.sql'])
        c.commit()

def create_database_blockchain():
    hook = PostgresHook(
        postgres_conn_id = 'postgres_airflow'
    )
    conn = hook.get_conn()
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute((deploy_script()['drop_db.sql']))
    cursor.execute((deploy_script()['create_db.sql']))
    cursor.close()
    conn.close()

def create_schemas():
    hook = PostgresHook(
        postgres_conn_id = 'postgres_blockchain'
    )
    conn = hook.get_conn()
    with conn as c:
        cursor = c.cursor()
        cursor.execute(deploy_script()['create_schemas.sql'])
        c.commit()

def create_tables():
    hook = PostgresHook(
        postgres_conn_id = 'postgres_blockchain'
    )
    conn = hook.get_conn()
    with conn as c:
        cursor = c.cursor()
        cursor.execute(deploy_script()['create_tables.sql'])
        c.commit()

with DAG(
    dag_id = 'dag_set_blockchain_db',
    default_args=default_args,
    description = 'create new blockchain db and user admin',
    start_date = days_ago(1),
    schedule_interval = '@once'
) as dag:
    task1 = PythonOperator(
        task_id = 'create_user_admin',
        python_callable=create_user_admin
    )
    task2 = PythonOperator(
        task_id = 'create_database_blockchain',
        python_callable=create_database_blockchain
    )
    task3 = PythonOperator(
        task_id = 'create_schemas',
        python_callable=create_schemas
    )
    task4 = PythonOperator(
        task_id = 'create_tables',
        python_callable=create_tables
    )
    trigger_dag = TriggerDagRunOperator(
        task_id = 'trigger_dag_get_transactions_save_s3',
        trigger_dag_id='dag_get_transactions_save_s3'
    )
    task1 >> task2 >> task3 >> task4 >> trigger_dag