from pyspark.sql import SparkSession
#from schema2 import schema
from pyspark.sql.types import (IntegerType,
                               StringType,
                               DoubleType,
                               StructField,
                               StructType,
                               LongType,
                               BooleanType,
                               TimestampType)
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
        StructField("registration", LongType(), True)
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
spark = SparkSession.builder.appName("read_file").master('spark://spark-master:7077').getOrCreate()

auth_events = spark.read.format("parquet").\
    schema(schema['auth_events']).\
    load("s3a://zingstreamp3/data/auth_events")
auth_events.createOrReplaceTempView("auth_events")
auth_events_data = spark.sql("SELECT * FROM auth_events")
auth_events_data.printSchema()
auth_events_data.show()

listen_events = spark.read.format("parquet").\
    schema(schema['listen_events']).\
    load("s3a://zingstreamp3/data/listen_events")
listen_events.printSchema()
listen_events.show()


page_view_events = spark.read.format("parquet").\
    schema(schema['page_view_events']).\
    load("s3a://zingstreamp3/data/page_view_events")
page_view_events.printSchema()
page_view_events.show()
