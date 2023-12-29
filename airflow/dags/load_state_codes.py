import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import minio
from minio import Minio
import logging



def load_file_to_minio(file_name):

    client = Minio(
        endpoint="minio:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

    bucket = "zingstreamp3"

    found = client.bucket_exists(bucket)
    if not found:
        logging.error(f"bucket {bucket} is not exists")

    client.fput_object(
        bucket,
        f'data/{file_name}.csv',
        f"/zingstreamp3_dbt/seeds/{file_name}.csv"
    )


dag = DAG(
  dag_id="load_state_codes",
  schedule_interval="@once",
  start_date=airflow.utils.dates.days_ago(0),
)

download = BashOperator(
    task_id='download_state_codes_file',
    bash_command='curl -o /zingstreamp3_dbt/seeds/state_codes.csv --url https://raw.githubusercontent.com/huynhdoanho/zingstreamp3/main/state_codes.csv',
    dag=dag
)

seed = BashOperator(
    task_id='dbt_seed',
    bash_command='cd /zingstreamp3_dbt && dbt seed --select state_codes --profiles-dir . --target prod',
    dag=dag
)

upload_to_minio = PythonOperator(
    task_id='upload_to_minio',
    python_callable=load_file_to_minio,
    op_kwargs={'file_name': 'state_codes'},
    dag=dag
)


download >> [seed, upload_to_minio]
