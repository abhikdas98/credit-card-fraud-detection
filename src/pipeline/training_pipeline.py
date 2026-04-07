import pickle
import yaml
import os

from src.ingestion.data_loader import load_data
from src.preprocessing.preprocess import preprocess_data
from src.feature_engineering.features import create_features, encode_data
from src.model.train import train_model
from src.model.evaluate import optimize_threshold


class TrainingPipeline:
    def __init__(self, config_path="config/config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        os.makedirs("models", exist_ok=True)

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

    def save_artifacts(self, model, threshold, encoding_maps, train_columns):
        cfg = self.config["model"]

        pickle.dump(model, open(cfg["model_path"], "wb"))
        pickle.dump(threshold, open(cfg["threshold_path"], "wb"))
        pickle.dump(encoding_maps, open(cfg["encoding_map_path"], "wb"))
        pickle.dump(train_columns, open(cfg["columns_path"], "wb"))

    def run(self):
        df = load_data(self.config["data"]["raw"])

        df = preprocess_data(df)
        df = create_features(df)

        train, test = self.split_data(df)

        train, test, encoding_maps = encode_data(train, test)

        X_train = train.drop(columns=['is_fraud', 'trans_date_trans_time', 'dob'])
        y_train = train['is_fraud']

        X_test = test.drop(columns=['is_fraud', 'trans_date_trans_time', 'dob'])
        y_test = test['is_fraud']

        model = train_model(
            X_train,
            y_train,
            self.config["tuning"]["n_iter"]
        )

        y_prob = model.predict_proba(X_test)[:, 1]

        best_threshold, best_cost = optimize_threshold(
            y_test,
            y_prob,
            self.config["cost"]["false_negative"],
            self.config["cost"]["false_positive"]
        )

        self.save_artifacts(
            model,
            best_threshold,
            encoding_maps,
            X_train.columns.tolist()
        )

        print(f"Best Threshold: {best_threshold}")
        print(f"Minimum Cost: {best_cost}")


if __name__ == "__main__":
    TrainingPipeline().run()