import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

dag = DAG(
  dag_id="dbt",
  schedule_interval="@once",
  start_date=airflow.utils.dates.days_ago(0),
)

run = BashOperator(
    task_id='dbt_run',
    bash_command='cd /zingstreamp3_dbt && dbt deps && dbt run --profiles-dir . ',
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)



run >> end
