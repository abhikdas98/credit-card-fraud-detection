from src.pipeline.inference_pipeline import InferencePipeline

pipeline = InferencePipeline()

sample = {
    "trans_date_trans_time": "2020-06-21 12:14:00",
    "cc_num": 2291160000000000,
    "merchant": "fraud_Kirlin and Sons",
    "category": "personal_care",
    "amt": 2.86,
    "gender": "M",
    "city": "Columbia",
    "state": "SC",
    "job": "Mechanical engineer",
    "dob": "1968-03-19"
}

result = pipeline.predict(sample)

print(result)