from pyspark.sql import SparkSession
from pyspark.sql.functions import window, sum, count

spark = (
    SparkSession.builder
    .appName("spark-delta-job")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)

silver = spark.readStream.format("delta").load("/app/data/silver/transactions")

gold = (
    silver
    .withWatermark("event_time", "10 minutes")
    .groupBy(
        window("event_time", "5 minutes"),
        "user_id"
    )
    .agg(
        sum("amount").alias("total_amount"),
        count("*").alias("txn_count")
    )
)

(
    gold.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/app/data/gold/_checkpoints")
    .start("/app/data/gold/user_activity")
    .awaitTermination()
)
