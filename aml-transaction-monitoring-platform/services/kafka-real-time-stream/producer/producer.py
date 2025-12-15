import pandas as pd
import json
import time
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=5
        )
        break
    except NoBrokersAvailable:
        print("Kafka not ready, retrying in 5 seconds...")
        time.sleep(5)

df = pd.read_csv("data/raw/saml-d/data.csv")

for _, row in df.iterrows():
    producer.send("transactions", row.to_dict())
    # print("Sent:", row.to_dict())
    time.sleep(1)

producer.flush()
