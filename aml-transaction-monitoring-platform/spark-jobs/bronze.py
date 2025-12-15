from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("spark-delta-job")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

schema = StructType([
    StructField("txn_id", StringType()),
    StructField("user_id", StringType()),
    StructField("amount", DoubleType()),
    StructField("currency", StringType()),
    StructField("timestamp", StringType()),
    StructField("merchant", StringType())
])

df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "transactions")
    .load()
)

bronze = (
    df.selectExpr("CAST(value AS STRING)")
      .select(from_json(col("value"), schema).alias("data"))
      .select("data.*")
)

(
    bronze.writeStream
    .queryName("bronze_transactions")
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/app/data/bronze/_checkpoints")
    .trigger(processingTime="5 minutes")
    .start("/app/data/bronze/transactions")
    .awaitTermination()
)
