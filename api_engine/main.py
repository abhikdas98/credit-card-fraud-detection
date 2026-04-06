from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline.inference_pipeline import InferencePipeline

# Initialize app
app = FastAPI(
    title="Fraud Detection API",
    description="Real-time Credit Card Fraud Detection",
    version="1.0"
)

# Load pipeline once (VERY IMPORTANT)
pipeline = InferencePipeline()


# Define request schema
class Transaction(BaseModel):
    trans_date_trans_time: str
    cc_num: float
    merchant: str
    category: str
    amt: float
    gender: str
    city: str
    state: str
    job: str
    dob: str


# Root endpoint
@app.get("/")
def home():
    return {"message": "Fraud Detection API is running 🚀"}


# Prediction endpoint
@app.post("/predict")
def predict(transaction: Transaction):
    data = transaction.dict()

    result = pipeline.predict(data)

    return result