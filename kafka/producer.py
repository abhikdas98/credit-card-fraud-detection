from kafka import KafkaProducer
import pandas as pd
import json
import time

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

df = pd.read_csv("data/raw/fraudTest.csv")

for _, row in df.iterrows():
    data = row.to_dict()

    producer.send("fraud_topic", value=data)

    print("Sent:", data['trans_num'])

    time.sleep(0.01)  # simulate streaming