import pickle
import pandas as pd
import numpy as np


class InferencePipeline:
    def __init__(self):
        # Load artifacts
        with open("models/model.pkl", "rb") as f:
            self.model = pickle.load(f)

        with open("models/threshold.pkl", "rb") as f:
            self.threshold = pickle.load(f)

        with open("models/encoding_maps.pkl", "rb") as f:
            self.encoding_maps = pickle.load(f)

    def preprocess(self, data: dict):
        df = pd.DataFrame([data])

        # Convert datetime
        df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
        df['dob'] = pd.to_datetime(df['dob'])

        # Feature engineering
        df['hour'] = df['trans_date_trans_time'].dt.hour
        df['day_of_week'] = df['trans_date_trans_time'].dt.dayofweek
        df['age'] = (df['trans_date_trans_time'] - df['dob']).dt.days // 365

        # Drop columns
        df = df.drop(columns=['first', 'last', 'street', 'trans_num'], errors='ignore')

        return df

    def encode(self, df):
        low_card_cols = ['category', 'gender', 'state']
        high_card_cols = ['merchant', 'city', 'job']

        # One-hot encoding
        df = pd.get_dummies(df, columns=low_card_cols, drop_first=True)

        # Frequency encoding (use saved maps)
        for col in high_card_cols:
            freq_map = self.encoding_maps.get(col, {})
            df[col] = df[col].map(freq_map).fillna(0)

        return df

    def align_features(self, df):
        # Load training columns
        with open("models/train_columns.pkl", "rb") as f:
            train_cols = pickle.load(f)

        # Align columns
        df = df.reindex(columns=train_cols, fill_value=0)

        return df

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