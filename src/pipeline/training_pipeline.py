import pickle
import yaml
import os
import pandas as pd
import numpy as np
import logging

from sklearn.metrics import precision_recall_curve, confusion_matrix
from sklearn.model_selection import train_test_split

from src.ingestion.data_loader import load_data
from src.preprocessing.preprocess import preprocess_data
from src.feature_engineering.features import create_features, encode_data
from src.model.train import train_model


# ✅ Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TrainingPipeline:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        os.makedirs("models", exist_ok=True)

    # ✅ Stratified split
    def split_data(self, df):
        train, test = train_test_split(
            df,
            test_size=0.2,
            stratify=df['is_fraud'],
            random_state=42
        )
        return train, test

    # ✅ F1-based threshold
    def optimize_threshold_f1(self, y_test, y_prob):
        precision, recall, thresholds = precision_recall_curve(y_test, y_prob)

        if len(thresholds) == 0:
            return 0.5

        precision = precision[:-1]
        recall = recall[:-1]

        f1_scores = 2 * (precision * recall) / (precision + recall + 1e-6)

        best_idx = np.argmax(f1_scores)
        best_threshold = thresholds[best_idx]

        logging.info(f"[F1] Threshold: {best_threshold:.4f}")
        logging.info(f"[F1] Precision: {precision[best_idx]:.4f}")
        logging.info(f"[F1] Recall: {recall[best_idx]:.4f}")

        return float(best_threshold)

    # 🔥 NEW: Cost-based threshold
    def optimize_threshold_cost(self, y_test, y_prob):
        COST_FN = self.config["cost"]["false_negative"]
        COST_FP = self.config["cost"]["false_positive"]

        thresholds = np.linspace(0.05, 0.8, 100)

        best_threshold = 0.5
        best_cost = float("inf")

        for t in thresholds:
            y_pred = (y_prob >= t).astype(int)

            tn = ((y_test == 0) & (y_pred == 0)).sum()
            fp = ((y_test == 0) & (y_pred == 1)).sum()
            fn = ((y_test == 1) & (y_pred == 0)).sum()
            tp = ((y_test == 1) & (y_pred == 1)).sum()

            cost = fn * COST_FN + fp * COST_FP

            if cost < best_cost:
                best_cost = cost
                best_threshold = t

        logging.info(f"[COST] Best Threshold: {best_threshold:.4f}")
        logging.info(f"[COST] Minimum Cost: {best_cost}")

        return float(best_threshold)

    # ✅ Save artifacts
    def save_artifacts(self, model, threshold, encoding_maps, train_columns):
        cfg = self.config["model"]

        with open(cfg["model_path"], "wb") as f:
            pickle.dump(model, f)

        with open(cfg["threshold_path"], "wb") as f:
            pickle.dump(threshold, f)

        with open(cfg["encoding_map_path"], "wb") as f:
            pickle.dump(encoding_maps, f)

        with open(cfg["columns_path"], "wb") as f:
            pickle.dump(train_columns, f)

        logging.info("✅ Artifacts saved successfully")

    def run(self):
        logging.info("🚀 Starting training pipeline...")

        # 🔹 Load data
        df = load_data(self.config["data"]["raw"])

        # 🔹 Preprocess
        df = preprocess_data(df)
        df = create_features(df)

        # 🔹 Split
        train, test = self.split_data(df)

        print("Train fraud ratio:", train['is_fraud'].mean())
        print("Test fraud ratio:", test['is_fraud'].mean())

        # 🔹 Encode
        train, test, encoding_maps = encode_data(train, test)

        # 🚨 Remove leakage features
        leakage_cols = [
            'is_fraud',
            'trans_date_trans_time',
            'dob',
            'cc_num',
            'unix_time',
            'lat', 'long', 'merch_lat', 'merch_long'
        ]

        X_train = train.drop(columns=leakage_cols, errors='ignore')
        y_train = train['is_fraud']

        X_test = test.drop(columns=leakage_cols, errors='ignore')
        y_test = test['is_fraud']

        logging.info(f"📊 Train shape: {X_train.shape}")
        logging.info(f"📊 Test shape: {X_test.shape}")

        # 🔹 Train model
        model = train_model(
            X_train,
            y_train,
            self.config["tuning"]["n_iter"]
        )

        # 🔹 Predict probabilities
        y_prob = model.predict_proba(X_test)[:, 1]

        # 🔥 BOTH thresholds
        threshold_f1 = self.optimize_threshold_f1(y_test, y_prob)
        threshold_cost = self.optimize_threshold_cost(y_test, y_prob)

        print("\n🔍 Threshold Comparison")
        print("----------------------")
        print(f"F1 Threshold   : {threshold_f1:.4f}")
        print(f"Cost Threshold : {threshold_cost:.4f}")

        # 👉 Choose final threshold (BUSINESS FIRST)
        final_threshold = threshold_cost

        # 🔹 Predictions
        y_pred = (y_prob >= final_threshold).astype(int)

        # 🔹 Evaluation
        cm = confusion_matrix(y_test, y_pred)

        print("\n📊 Evaluation Summary (FINAL)")
        print("----------------------------")
        print("Confusion Matrix:\n", cm)
        print("Fraud predicted:", y_pred.sum())
        print("Actual fraud:", y_test.sum())

        # 🔹 Save artifacts
        self.save_artifacts(
            model,
            final_threshold,
            encoding_maps,
            X_train.columns.tolist()
        )

        logging.info(f"🎯 Final Threshold Used: {final_threshold:.4f}")
        logging.info("✅ Training pipeline completed successfully!")


if __name__ == "__main__":
    TrainingPipeline().run()