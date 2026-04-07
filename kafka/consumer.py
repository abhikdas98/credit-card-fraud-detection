from kafka import KafkaConsumer
import json
import pandas as pd

from src.pipeline.inference_pipeline import InferencePipeline

consumer = KafkaConsumer(
    "fraud_topic",
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

pipeline = InferencePipeline()

output_file = "data/bi/predictions.csv"

for message in consumer:
    data = message.value

    result = pipeline.predict(data)

    record = {**data, **result}

    df = pd.DataFrame([record])

    df.to_csv(output_file, mode='a', header=not pd.io.common.file_exists(output_file), index=False)

    print("Processed:", result)