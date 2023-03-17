import os
import asyncio
import aiohttp
import json
import config
from datetime import datetime, timedelta
from helper import get_scripts, get_transactions_for_address_v2_url, generate_path
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.dates import days_ago
from tempfile import NamedTemporaryFile

scripts = get_scripts(config.SQL_DIR)
pg_hook = PostgresHook(postgres_conn_id='postgres_blockchain')
conn = pg_hook.get_conn()

s3_hook = S3Hook(aws_conn_id='aws_s3')

default_args = {
    'owner': 'datakai',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


def get_transactions_save_psql():
    async def main():
        async with aiohttp.ClientSession() as session:
            page = 0
            has_more = True
            while has_more:
                url = get_transactions_for_address_v2_url(
                    chain='eth-mainnet',
                    address='0x76fca1adb104770b38581b64d55e67fa5a0f3966',
                    page_number=page,
                    page_size=2000
                )
                async with session.get(url) as response:
                    # print('Check to see if here is the error')
                    result = await response.json(content_type=None)
                    # print('Was it?')
                    data = result['data']['items']
                    pagination = result['data']['pagination']
                    query = (scripts['insert_results.sql'])
                    with conn as c:
                        cursor = c.cursor()
                        if not pagination['has_more']:
                            for row in data:
                                d = (json.dumps(row))
                                cursor.execute(
                                    query, (d, pagination['page_number'],))
                                c.commit()
                            has_more = False
                            print('End of the line')
                        elif pagination['has_more']:
                            for row in data:
                                d = (json.dumps(row))
                                cursor.execute(
                                    query, (d, pagination['page_number'],))
                                c.commit()
                            page += 1
                            print(f'More to go. Now passing to page {page}')
    asyncio.run(main())


def get_psql_send_s3():
    with conn as c:
        cursor = c.cursor()
        query = 'select data from staging.covalent_token_event'
        cursor.execute(query)
        loop = 1
        while True:
            results = cursor.fetchmany(100)
            if not results:
                break
            else:
                with NamedTemporaryFile(mode='w', suffix=str(loop)) as f:
                    # with open('dags/results.json', 'w') as f:
                    print(f'Loop number {loop}')
                    json.dump(results, f)
                    f.flush()
                    s3_hook.load_file(
                        # filename = 'dags/results.json',
                        filename=f.name,
                        key=f'events/{generate_path()}.json',
                        bucket_name='blockchain-token-holders',
                        replace=True
                    )
                    loop += 1
                    print(f'file {f.name} has been pushed to s3')


with DAG(
    dag_id='dag_get_transactions_save_s3',
    default_args=default_args,
    description='get historical contract transactions and save to psql and s3',
    start_date=days_ago(1),
    schedule_interval='@once'
) as dag:
    task1 = PythonOperator(
        task_id='get_transactions_save_psql',
        python_callable=get_transactions_save_psql
    )
    task2 = PythonOperator(
        task_id='get_psql_send_s3',
        python_callable=get_psql_send_s3
    )
    task1 >> [task2]
