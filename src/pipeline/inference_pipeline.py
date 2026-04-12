import pandas as pd
import pickle

from src.preprocessing.preprocess import preprocess_data
from src.feature_engineering.features import create_features
from src.model.predict import ModelPredictor


class InferencePipeline:
    def __init__(self):
        with open("models/encoding_maps.pkl", "rb") as f:
            self.encoding_maps = pickle.load(f)

        with open("models/train_columns.pkl", "rb") as f:
            self.train_columns = pickle.load(f)

        self.model = ModelPredictor()

    def predict(self, data: dict):
        df = pd.DataFrame([data])

        df = preprocess_data(df)
        df = create_features(df)

        # encoding
        for col, mapping in self.encoding_maps.items():
            df[col] = df[col].map(mapping).fillna(0)

        df = df.reindex(columns=self.train_columns, fill_value=0)

        prob, pred = self.model.predict(df)

        return {
            "fraud_probability": float(prob),
            "prediction": "FRAUD" if pred == 1 else "NOT FRAUD"
        }