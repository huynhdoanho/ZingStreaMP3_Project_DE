import airflow
from pyspark.sql import SparkSession
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import logging
import datetime
from datetime import timedelta
from airflow.operators.dummy_operator import DummyOperator
from pyspark.sql.types import (IntegerType,
                               StringType,
                               DoubleType,
                               StructField,
                               StructType,
                               LongType,
                               BooleanType,
                               TimestampType)

# time
now = datetime.datetime.now()
month = now.month
day = now.day - 1

# postgres config
postgres_url = "jdbc:postgresql://postgres_zingstreamp3:5432/zingstreamp3"
postgres_properties = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}

# Topic list
topic_list = ['listen_events', 'auth_events', 'page_view_events']

# schema
schema = {
    'listen_events': StructType([
        StructField("artist", StringType(), True),
        StructField("song", StringType(), True),
        StructField("duration", DoubleType(), True),
        StructField("ts", TimestampType(), True),
        StructField("sessionid", IntegerType(), True),
        StructField("auth", StringType(), True),
        StructField("level", StringType(), True),
        StructField("itemInSession", IntegerType(), True),
        StructField("city", StringType(), True),
        StructField("zip", IntegerType(), True),
        StructField("state", StringType(), True),
        StructField("userAgent", StringType(), True),
        StructField("lon", DoubleType(), True),
        StructField("lat", DoubleType(), True),
        StructField("userId", LongType(), True),
        StructField("lastName", StringType(), True),
        StructField("firstName", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("registration", LongType(), True),
        StructField("month", IntegerType(), True),
        StructField("day", IntegerType(), True),
        StructField("hour", IntegerType(), True)
    ]),
    'page_view_events': StructType([
        StructField("ts", TimestampType(), True),
        StructField("sessionId", IntegerType(), True),
        StructField("page", StringType(), True),
        StructField("auth", StringType(), True),
        StructField("method", StringType(), True),
        StructField("status", IntegerType(), True),
        StructField("level", StringType(), True),
        StructField("itemInSession", IntegerType(), True),
        StructField("city", StringType(), True),
        StructField("zip", IntegerType(), True),
        StructField("state", StringType(), True),
        StructField("userAgent", StringType(), True),
        StructField("lon", DoubleType(), True),
        StructField("lat", DoubleType(), True),
        StructField("userId", IntegerType(), True),
        StructField("lastName", StringType(), True),
        StructField("firstName", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("registration", LongType(), True),
        StructField("artist", StringType(), True),
        StructField("song", StringType(), True),
        StructField("duration", DoubleType(), True),
        StructField("month", IntegerType(), True),
        StructField("day", IntegerType(), True),
        StructField("hour", IntegerType(), True)
    ]),
    'auth_events': StructType([
        StructField("ts", TimestampType(), True),
        StructField("sessionId", IntegerType(), True),
        StructField("level", StringType(), True),
        StructField("itemInSession", IntegerType(), True),
        StructField("city", StringType(), True),
        StructField("zip", IntegerType(), True),
        StructField("state", StringType(), True),
        StructField("userAgent", StringType(), True),
        StructField("lon", DoubleType(), True),
        StructField("lat", DoubleType(), True),
        StructField("userId", IntegerType(), True),
        StructField("lastName", StringType(), True),
        StructField("firstName", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("registration", LongType(), True),
        StructField("success", BooleanType(), True),
        StructField("month", IntegerType(), True),
        StructField("day", IntegerType(), True),
        StructField("hour", IntegerType(), True)
    ])
}

spark = SparkSession.builder.appName("example") \
    .master('spark://spark-master:7077') \
    .getOrCreate()


def write_to_postgres(topic):
    logging.info(f"Topic: {topic}")
    logging.info(f"Time: {now}")

    data = spark.read.format("parquet"). \
        schema(schema[topic]). \
        load(f"s3a://zingstreamp3/data/{topic}/month={month}/day={day}")
    logging.info(data.printSchema())

    data.write.jdbc(
        postgres_url,
        f"staging.{topic}",
        mode="append",
        properties=postgres_properties
        )


dag = DAG(
  dag_id="ZingStreaMP3",
  schedule_interval="0 1 * * *",    # 00:01:00
  start_date=airflow.utils.dates.days_ago(0),
)

start = DummyOperator(
    task_id="Start",
    dag=dag
)

end = DummyOperator(
    task_id="End",
    dag=dag
)

create_postgres_schema = PostgresOperator(
    task_id='create_schema',
    postgres_conn_id="postgres_zingstreamp3",
    sql="CREATE SCHEMA IF NOT EXISTS staging",
    dag=dag
)

for topic in topic_list:

    create_table = PostgresOperator(
        task_id=f'Create_{topic}_Table',
        postgres_conn_id="postgres_zingstreamp3",
        sql=f"sql/create_{topic}_table.sql",
        dag=dag
    )

    insert = PythonOperator(
        task_id=f"Insert_{topic}",
        python_callable=write_to_postgres,
        op_kwargs={'topic': topic},
        dag=dag
    )


    start >> create_postgres_schema >> create_table >> insert >> end
