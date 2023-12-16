from pyspark.sql import SparkSession
from pyspark.sql.types import (IntegerType,
                               StringType,
                               DoubleType,
                               StructField,
                               StructType,
                               LongType,
                               BooleanType)
from pyspark.sql.functions import from_json, col, year, month, hour, dayofmonth

schema = {
    'listen_events': StructType([
        StructField("artist", StringType(), True),
        StructField("song", StringType(), True),
        StructField("duration", DoubleType(), True),
        StructField("ts", LongType(), True),
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
        StructField("registration", LongType(), True)
    ]),
    'page_view_events': StructType([
        StructField("ts", LongType(), True),
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
        StructField("duration", DoubleType(), True)
    ]),
    'auth_events': StructType([
        StructField("ts", LongType(), True),
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
        StructField("success", BooleanType(), True)
    ])
}

# Khởi tạo SparkSession
spark = SparkSession.builder \
    .appName("Kafka") \
    .master("spark://spark-master:7077") \
    .getOrCreate()


spark.streams.resetTerminated()

# Đọc dữ liệu từ Kafka topic
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "broker:29092") \
  .option("subscribe", "listen_events") \
  .option("failOnDataLoss", False)\
  .option("startingOffsets", "earliest") \
  .load()


stream = df
stream = (stream
          .selectExpr("CAST(value AS STRING)")
          .select(
              from_json(col("value"), schema['listen_events']).alias(
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

write_stream = stream.writeStream\
                    .format("parquet")\
                    .option("path", 's3a://zingstreamp3/data')\
                    .option("checkpointLocation", 's3a://zingstreamp3/checkpoint')\
                    .trigger(processingTime="30 seconds")\
                    .outputMode("append")

write_stream.start().awaitTermination()

