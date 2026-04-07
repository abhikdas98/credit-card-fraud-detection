import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit


def train_model(X_train, y_train, n_iter):
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
        n_iter=n_iter,
        scoring="average_precision",
        cv=tscv,
        n_jobs=-1
    )

    search.fit(X_train, y_train)

    return search.best_estimator_