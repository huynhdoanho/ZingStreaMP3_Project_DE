from pyspark.sql import SparkSession
from schema import schema
from spark_streaming_functions import *

spark = SparkSession.builder \
    .appName("Kafka") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.streams.resetTerminated()

kafka_url = "broker:29092"

listen_topic = "listen_events"
auth_topic = "auth_events"
page_view_topic = "page_view_events"


### listen events ###
# read stream from kafka
listen_events_stream = read_stream_kafka(spark, kafka_url=kafka_url, topic=listen_topic)

# process stream
listen_events_stream = process_stream(listen_events_stream, stream_schema=schema[listen_topic])

# write stream to file
listen_events_write_stream = write_stream_file(listen_events_stream, topic=listen_topic)


### auth events #### read stream from kafka
auth_events_stream = read_stream_kafka(spark, kafka_url=kafka_url, topic=auth_topic)

# process stream
auth_events_stream = process_stream(auth_events_stream, stream_schema=schema[auth_topic])
auth_events_stream.printSchema()
# write stream to file
auth_events_write_stream = write_stream_file(auth_events_stream, topic=auth_topic)


### page view events ###
# read stream from kafka
page_view_events_stream = read_stream_kafka(spark, kafka_url=kafka_url, topic=page_view_topic)

# process stream
page_view_events_stream = process_stream(page_view_events_stream, stream_schema=schema[page_view_topic])

# write stream to file
page_view_events_write_stream = write_stream_file(page_view_events_stream, topic=page_view_topic)


listen_events_write_stream.start()
auth_events_write_stream.start()
page_view_events_write_stream.start()

spark.streams.awaitAnyTermination()
