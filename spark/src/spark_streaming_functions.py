from pyspark.sql.functions import from_json, col, month, hour, dayofmonth, col, year


def read_stream_kafka(spark, kafka_url, topic, startingOffsets="earliest"):
    read_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_url)\
        .option("subscribe", topic) \
        .option("failOnDataLoss", False) \
        .option("startingOffsets", startingOffsets) \
        .load()

    return read_stream


def process_stream(stream, stream_schema):
    """
    Process stream to fetch on value from the kafka message.
    convert ts to timestamp format and produce year, month, day,
    hour columns
    Parameters:
        stream : DataStreamReader
            The data stream reader for your stream
    Returns:
        stream: DataStreamReader
    """

    # read only value from the incoming message and convert the contents
    # inside to the passed schema
    stream = (stream
              .selectExpr("CAST(value AS STRING)")
              .select(
                  from_json(col("value"), stream_schema).alias(
                      "data")
              )
              .select("data.*")
              )

    # Add month, day, hour to split the data into separate directories
    stream = (stream
              .withColumn("ts", (col("ts")/1000).cast("timestamp"))
              .withColumn("year", year(col("ts")))
              .withColumn("month", month(col("ts")))
              .withColumn("hour", hour(col("ts")))
              .withColumn("day", dayofmonth(col("ts")))
              )

    return stream


def write_stream_file(stream, topic, file_format="parquet", time="2 minutes", mode="append"):
    write_stream = stream\
        .writeStream\
        .format(file_format)\
        .option("path", f"s3a://zingstreamp3/data/{topic}") \
        .partitionBy("month", "day") \
        .option("checkpointLocation", f's3a://zingstreamp3/data/checkpoint/{topic}')\
        .trigger(processingTime=time)\
        .outputMode(mode)

    return write_stream

#.option("path", f"s3a://zingstreamp3/data/{topic}.{file_format}") \
