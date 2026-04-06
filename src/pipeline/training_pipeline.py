import pandas as pd
import numpy as np
import pickle
import yaml
import os

from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.metrics import confusion_matrix

import xgboost as xgb


class TrainingPipeline:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        # ✅ Ensure models directory exists
        os.makedirs("models", exist_ok=True)

    def load_data(self):
        path = self.config["data"]["raw"]
        df = pd.read_csv(path)
        return df

    def preprocess(self, df):
        # Convert datetime
        df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
        df['dob'] = pd.to_datetime(df['dob'])

        # Feature engineering
        df['hour'] = df['trans_date_trans_time'].dt.hour
        df['day_of_week'] = df['trans_date_trans_time'].dt.dayofweek
        df['age'] = (df['trans_date_trans_time'] - df['dob']).dt.days // 365

        # Drop columns
        df = df.drop(columns=['first', 'last', 'street', 'trans_num'])

        # Sort
        df = df.sort_values('trans_date_trans_time')

        return df

    def split_data(self, df):
        fraud_df = df[df['is_fraud'] == 1]
        non_fraud_df = df[df['is_fraud'] == 0]

        fraud_split = int(len(fraud_df) * 0.8)
        non_fraud_split = int(len(non_fraud_df) * 0.8)

        train = pd.concat([
            fraud_df.iloc[:fraud_split],
            non_fraud_df.iloc[:non_fraud_split]
        ])

        test = pd.concat([
            fraud_df.iloc[fraud_split:],
            non_fraud_df.iloc[non_fraud_split:]
        ])

        return train, test

    def encode(self, train, test):
        low_card_cols = ['category', 'gender', 'state']
        high_card_cols = ['merchant', 'city', 'job']

        # One-hot
        train = pd.get_dummies(train, columns=low_card_cols, drop_first=True)
        test = pd.get_dummies(test, columns=low_card_cols, drop_first=True)

        # Align columns
        train, test = train.align(test, join='left', axis=1, fill_value=0)

        # Frequency encoding
        self.encoding_maps = {}

        for col in high_card_cols:
            freq = train[col].value_counts(normalize=True)
            self.encoding_maps[col] = freq.to_dict()  # ✅ safer serialization

            train[col] = train[col].map(freq)
            test[col] = test[col].map(freq).fillna(0)

        print("✅ Encoding maps created")

        return train, test

    def train_model(self, X_train, y_train):
        scale_pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])

        model = xgb.XGBClassifier(
            scale_pos_weight=scale_pos_weight,
            eval_metric="aucpr",
            random_state=42
        )

        param_dist = {
            "n_estimators": [200, 400, 600],
            "max_depth": [4, 6, 8],
            "learning_rate": [0.01, 0.05, 0.1],
            "subsample": [0.8, 1.0],
            "colsample_bytree": [0.8, 1.0]
        }

        tscv = TimeSeriesSplit(n_splits=3)

        search = RandomizedSearchCV(
            model,
            param_dist,
            n_iter=self.config["tuning"]["n_iter"],
            scoring="average_precision",
            cv=tscv,
            n_jobs=-1
        )

        search.fit(X_train, y_train)

        return search.best_estimator_

    def optimize_threshold(self, y_test, y_prob):
        COST_FN = self.config["cost"]["false_negative"]
        COST_FP = self.config["cost"]["false_positive"]

        thresholds = np.linspace(0, 0.2, 100)

        best_threshold = 0
        best_cost = float('inf')

        for t in thresholds:
            y_pred = (y_prob >= t).astype(int)
            tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

            cost = fn * COST_FN + fp * COST_FP

            if cost < best_cost:
                best_cost = cost
                best_threshold = t

        return best_threshold, best_cost

    def save_artifacts(self, model, threshold):
        model_path = self.config["model"]["model_path"]
        threshold_path = self.config["model"]["threshold_path"]
        encoding_path = self.config["model"]["encoding_map_path"]
        columns_path = self.config["model"]["columns_path"]

        # Save model
        with open(model_path, "wb") as f:
            pickle.dump(model, f)

        # Save threshold
        with open(threshold_path, "wb") as f:
            pickle.dump(threshold, f)

        # ✅ Save encoding maps safely
        if not hasattr(self, "encoding_maps"):
            raise ValueError("Encoding maps not found. Encode step may have failed.")

        with open(encoding_path, "wb") as f:
            pickle.dump(self.encoding_maps, f)

        print(f"✅ Encoding maps saved at {encoding_path}")

        with open(columns_path, "wb") as f:
            pickle.dump(self.train_columns, f)

    def run(self):
        df = self.load_data()
        df = self.preprocess(df)

        train, test = self.split_data(df)
        train, test = self.encode(train, test)

        X_train = train.drop(columns=['is_fraud', 'trans_date_trans_time', 'dob'])
        y_train = train['is_fraud']

        X_test = test.drop(columns=['is_fraud', 'trans_date_trans_time', 'dob'])
        y_test = test['is_fraud']

        self.train_columns = X_train.columns.tolist()

        model = self.train_model(X_train, y_train)

        y_prob = model.predict_proba(X_test)[:, 1]

        best_threshold, best_cost = self.optimize_threshold(y_test, y_prob)

        self.save_artifacts(model, best_threshold)

        print(f"Best Threshold: {best_threshold}")
        print(f"Minimum Cost: {best_cost}")


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run()