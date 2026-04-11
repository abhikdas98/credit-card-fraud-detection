import pickle
import pandas as pd

from src.preprocessing.preprocess import preprocess_data
from src.feature_engineering.features import create_features, encode_single


class InferencePipeline:
    def __init__(self):
        # Load artifacts
        self.model = pickle.load(open("models/model.pkl", "rb"))
        self.threshold = pickle.load(open("models/threshold.pkl", "rb"))
        self.encoding_maps = pickle.load(open("models/encoding_maps.pkl", "rb"))
        self.train_columns = pickle.load(open("models/train_columns.pkl", "rb"))

    def preprocess(self, data: dict):
        df = pd.DataFrame([data])

        # Convert datetime
        df['trans_date_trans_time'] = pd.to_datetime(
        df['trans_date_trans_time'], format="%d-%m-%Y %H:%M"
        )

        df['dob'] = pd.to_datetime(
            df['dob'], format="%d-%m-%Y"
        )

        # Feature engineering
        df['hour'] = df['trans_date_trans_time'].dt.hour
        df['day_of_week'] = df['trans_date_trans_time'].dt.dayofweek
        df['age'] = (df['trans_date_trans_time'] - df['dob']).dt.days // 365

        # Drop columns
        df = df.drop(columns=['first', 'last', 'street', 'trans_num'], errors='ignore')

        # ✅ CRITICAL FIX
        df = df.drop(columns=['trans_date_trans_time', 'dob'], errors='ignore')

        return df

    def encode(self, df):
        return encode_single(df, self.encoding_maps)

    def align_features(self, df):
        return df.reindex(columns=self.train_columns, fill_value=0)

    def predict(self, data: dict):
        df = self.preprocess(data)
        df = self.encode(df)
        df = self.align_features(df)

        prob = self.model.predict_proba(df)[:, 1][0]
        prediction = int(prob >= self.threshold)

        return {
            "fraud_probability": float(prob),
            "threshold": float(self.threshold),
            "prediction": "FRAUD" if prediction == 1 else "NOT FRAUD"
        }