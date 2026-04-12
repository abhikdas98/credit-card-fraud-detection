from kafka import KafkaConsumer
import json
import time
import pandas as pd
import sys

from src.pipeline.inference_pipeline import InferencePipeline
from src.utils.logger import get_logger
from src.utils.exception import CustomException

logger = get_logger()


# ✅ Retry logic for Kafka
def create_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                "fraud_topic",
                bootstrap_servers='kafka:9092',
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id="fraud-group"
            )
            print("✅ Connected to Kafka (Consumer)")
            return consumer
        except Exception:
            print("❌ Kafka not ready (consumer), retrying...")
            time.sleep(5)


consumer = create_consumer()

pipeline = InferencePipeline()

print("🚀 Consumer started...")

for message in consumer:
    try:
        data = message.value

        result = pipeline.predict(data)

        logger.info(f"Processed: {result}")

        # ✅ Save to CSV (BI layer)
        output = {
            **data,
            **result
        }

        df = pd.DataFrame([output])

        df.to_csv(
            "data/bi/predictions.csv",
            mode="a",
            header=not pd.io.common.file_exists("data/bi/predictions.csv"),
            index=False
        )

    except Exception as e:
        logger.error(CustomException(e, sys))