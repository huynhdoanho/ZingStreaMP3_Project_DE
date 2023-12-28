import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from load_state_codes import load_file_to_minio
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://postgres:postgres@postgres_zingstreamp3:5432/zingstreamp3')


def load_file_to_postgres():
    songs = pd.read_csv("/zingstreamp3_dbt/seeds/songs.csv")
    songs.to_sql("songs", schema='staging', con=engine)


dag = DAG(
  dag_id="load_songs",
  schedule_interval="@once",
  start_date=airflow.utils.dates.days_ago(0),
)

download = BashOperator(
    task_id='download_songs_file',
    bash_command='curl -o /zingstreamp3_dbt/seeds/songs.csv --url https://raw.githubusercontent.com/ankurchavda/streamify/main/dbt/seeds/songs.csv',
    dag=dag
)

load_to_postgres = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_file_to_postgres,
    dag=dag
)

upload_to_minio = PythonOperator(
    task_id='Upload_to_minio',
    python_callable=load_file_to_minio,
    op_kwargs={'file_name': 'songs'},
    dag=dag
)

download >> [load_to_postgres, upload_to_minio]
