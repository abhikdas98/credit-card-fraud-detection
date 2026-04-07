import numpy as np
from sklearn.metrics import confusion_matrix


def optimize_threshold(y_test, y_prob, cost_fn, cost_fp):
    thresholds = np.linspace(0, 0.2, 100)

    best_threshold = 0
    best_cost = float('inf')

    for t in thresholds:
        y_pred = (y_prob >= t).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

        cost = fn * cost_fn + fp * cost_fp

        if cost < best_cost:
            best_cost = cost
            best_threshold = t

    return best_threshold, best_cost