FROM bitnami/spark:3.5.0

USER root

# Install Python deps
RUN pip install delta-spark kafka-python

# Create working directory
WORKDIR /app

COPY spark-jobs/bronze.py spark-jobs/silver.py spark-jobs/gold.py ./

USER 1001