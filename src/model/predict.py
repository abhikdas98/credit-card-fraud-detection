import pickle
import os

class ModelPredictor:
    def __init__(self):
        with open("models/model.pkl", "rb") as f:
            self.model = pickle.load(f)

        with open("models/threshold.pkl", "rb") as f:
            self.threshold = pickle.load(f)

    def predict(self, X):
        prob = self.model.predict_proba(X)[:, 1][0]
        pred = int(prob >= self.threshold)

        return prob, pred