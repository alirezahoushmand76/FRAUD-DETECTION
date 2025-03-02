from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, LongType, ArrayType
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

after_schema = StructType([
    StructField("age", LongType(), True),
    StructField("email", StringType(), True),
    StructField("id", LongType(), True),
    StructField("name", StringType(), True),
    StructField("purchase", LongType(), True),
    StructField("store", StringType(), True),
    StructField("timestamp", LongType(), True),
    StructField("clerk", StringType(), True)
])

source_schema = StructType([
    StructField("connector", StringType(), True),
    StructField("db", StringType(), True),
    StructField("lsn", LongType(), True),
    StructField("name", StringType(), True),
    StructField("schema", StringType(), True),
    StructField("sequence", StringType(), True),
    StructField("snapshot", StringType(), True),
    StructField("table", StringType(), True),
    StructField("ts_ms", LongType(), True),
    StructField("ts_ns", LongType(), True),
    StructField("ts_us", LongType(), True),
    StructField("txId", LongType(), True),
    StructField("version", StringType(), True),
    StructField("xmin", StringType(), True)
])

field_schema = StructType([
    StructField("field", StringType(), True),
    StructField("fields", ArrayType(StructType([
        StructField("default", StringType(), True),
        StructField("field", StringType(), True),
        StructField("name", StringType(), True),
        StructField("optional", StringType(), True),
        StructField("parameters", StructType([
            StructField("allowed", StringType(), True)
        ]), True),
        StructField("type", StringType(), True),
        StructField("version", LongType(), True)
    ])), True),
    StructField("name", StringType(), True),
    StructField("optional", StringType(), True),
    StructField("type", StringType(), True),
    StructField("version", LongType(), True)
])

schema_schema = StructType([
    StructField("fields", ArrayType(field_schema), True),
    StructField("name", StringType(), True),
    StructField("optional", StringType(), True),
    StructField("type", StringType(), True),
    StructField("version", LongType(), True)
])

payload_schema = StructType([
    StructField("after", after_schema, True),
    StructField("before", StringType(), True),
    StructField("op", StringType(), True),
    StructField("source", source_schema, True),
    StructField("transaction", StringType(), True),
    StructField("ts_ms", LongType(), True),
    StructField("ts_ns", LongType(), True),
    StructField("ts_us", LongType(), True)
])

complete_schema = StructType([
    StructField("payload", payload_schema, True),
    StructField("schema", schema_schema, True)
])

spark = SparkSession.builder \
    .appName("Process-Kafka-Topics-by-Spark") \
    .getOrCreate()

# If you want to debug, comment the following line. This line 
# results in command line only show us the result of Bathces
spark.sparkContext.setLogLevel("WARN")

df_stream_postgres = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "postgrestopic.public.customer") \
    .load()

df_stream_mysql = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "mysqltopic.mariadb.customer") \
    .load()    

parsed_stream_postgres = df_stream_postgres.select(from_json(col("value").cast("string"), complete_schema) \
     .alias("data")) \
     .select("data.payload.after") \
     .selectExpr("after.purchase AS postgres_purchase",
    "after.clerk AS postgres_clerk",
    "after.store AS postgres_store",
    "after.name AS postgres_customer"
    )   


parsed_stream_mysql = df_stream_mysql.select(from_json(col("value").cast("string"), complete_schema) \
     .alias("mysql_data")) \
     .select("mysql_data.payload.after") \
     .selectExpr("after.purchase AS mysql_purchase",
    "after.clerk AS mysql_clerk",
    "after.store AS mysql_store",
    "after.name AS mysql_customer"
    )    

aggregated_stream_postgres = parsed_stream_postgres.groupBy("postgres_clerk").agg(
    F.count("postgres_purchase").alias("postgres_purchase_count")
)

aggregated_stream_mysql = parsed_stream_mysql.groupBy("mysql_clerk").agg(
    F.count("mysql_purchase").alias("mysql_purchase_count")
)

aggregated_query_postgres = aggregated_stream_postgres.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime='45 second') \
    .start()

aggregated_query_mysql = aggregated_stream_mysql.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime='45 second') \
    .start()

query_postgres = parsed_stream_postgres.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime='30 second') \
    .start()     

query_mysql = parsed_stream_mysql.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime='30 second') \
    .start() 


query_postgres.awaitTermination()
query_mysql.awaitTermination()
aggregated_query_postgres.awaitTermination()
aggregated_query_mysql.awaitTermination()
