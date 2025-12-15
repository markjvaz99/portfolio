from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

spark = (
    SparkSession.builder
    .appName("spark-delta-job")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

bronze = spark.readStream.format("delta").load("/app/data/bronze/transactions") # Test

silver = (
    bronze
    .withColumn("amount", col("amount").cast("double"))
    .withColumn("event_time", to_timestamp("timestamp"))
    .dropDuplicates(["txn_id"])
    .filter(col("amount") > 0)
)

(
    silver.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/app/data/silver/_checkpoints")
    .start("/app/data/silver/transactions")
    .awaitTermination()
)
