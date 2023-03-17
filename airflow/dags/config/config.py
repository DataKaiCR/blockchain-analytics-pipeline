import os

CURR_DIR = os.getcwd()
SQL_DIR = os.path.join(CURR_DIR, 'dags','sql')

# SQL_DIR = '/airflow/dags/sql/'

MAX_LOG_DAYS = 3
LOG_DIR = '/efs/airflow/logs/'