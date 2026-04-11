from kafka import KafkaProducer
import pandas as pd
import json
import time

# ✅ Retry logic
def create_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                linger_ms=10,
                retries=5,
                acks='all'
            )
            print("✅ Connected to Kafka (Producer)")
            return producer
        except Exception:
            print("❌ Kafka not ready (producer), retrying in 5 sec...")
            time.sleep(5)


producer = create_producer()

# Load data
df = pd.read_csv("data/raw/fraudTest.csv")

print(f"🚀 Streaming {len(df)} records...")

for i, row in df.iterrows():
    try:
        data = row.to_dict()
        producer.send("fraud_topic", value=data)

        if i % 100 == 0:
            print(f"📤 Sent {i} records")

        time.sleep(0.01)

    except Exception as e:
        print(f"⚠️ Error: {e}")

producer.flush()
producer.close()

print("✅ Producer finished")