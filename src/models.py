"""
Model training and evaluation for NBA MVP prediction.

Implements two classifiers:
- Gaussian Naive Bayes
- Logistic Regression

Two evaluation modes:
- Pure MVP: binary classification of any finalist as MVP or not.
- Seasonal MVP: pick exactly one MVP per season from the three finalists.
"""

import os
import json
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_PATH = "data/processed/mvp_finalists_2001_2020.csv"
MODELS_DIR = "models"
RESULTS_DIR = "results"
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

FEATURES = [
    "g", "mp_per_g", "fg_pct", "fg3_pct", "ft_pct",
    "trb_per_g", "ast_per_g", "stl_per_g", "blk_per_g", "pts_per_g",
]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    train_df = df[df["season"] <= 2016].copy()
    test_df = df[df["season"] >= 2017].copy()
    return df, train_df, test_df


# ---------------------------------------------------------------------------
# Seasonal prediction helper
# ---------------------------------------------------------------------------
def seasonal_predictions(df, prob_column):
    """
    For each season, assign MVP=1 to the finalist with the highest predicted
    probability and 0 to the others.
    """
    preds = []
    for season, group in df.groupby("season"):
        group = group.copy()
        group["pred_seasonal"] = 0
        top_idx = group[prob_column].idxmax()
        group.loc[top_idx, "pred_seasonal"] = 1
        preds.append(group)
    return pd.concat(preds).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Model training & evaluation
# ---------------------------------------------------------------------------
def train_and_evaluate():
    df, train_df, test_df = load_data()

    X_train = train_df[FEATURES].values
    y_train = train_df["MVP"].values
    X_test = test_df[FEATURES].values
    y_test = test_df["MVP"].values

    # Scale features for Logistic Regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "naive_bayes": GaussianNB(),
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
    }

    results = {}
    trained_models = {}

    for name, model in models.items():
        print(f"\n=== {name.replace('_', ' ').title()} ===")

        # Naive Bayes does not need scaling; Logistic Regression does
        if name == "naive_bayes":
            model.fit(X_train, y_train)
            train_probs = model.predict_proba(X_train)[:, 1]
            test_probs = model.predict_proba(X_test)[:, 1]
        else:
            model.fit(X_train_scaled, y_train)
            train_probs = model.predict_proba(X_train_scaled)[:, 1]
            test_probs = model.predict_proba(X_test_scaled)[:, 1]

        # Pure predictions (threshold 0.5)
        train_pred_pure = (train_probs >= 0.5).astype(int)
        test_pred_pure = (test_probs >= 0.5).astype(int)

        # Seasonal predictions
        test_df_copy = test_df.copy()
        test_df_copy["prob"] = test_probs
        seasonal_df = seasonal_predictions(test_df_copy, "prob")
        test_pred_seasonal = seasonal_df["pred_seasonal"].values

        # Metrics
        train_acc_pure = accuracy_score(y_train, train_pred_pure)
        test_acc_pure = accuracy_score(y_test, test_pred_pure)
        test_acc_seasonal = accuracy_score(y_test, test_pred_seasonal)

        results[name] = {
            "train_accuracy_pure": round(train_acc_pure, 4),
            "test_accuracy_pure": round(test_acc_pure, 4),
            "test_accuracy_seasonal": round(test_acc_seasonal, 4),
            "confusion_matrix_pure": confusion_matrix(y_test, test_pred_pure).tolist(),
            "classification_report_pure": classification_report(
                y_test, test_pred_pure, output_dict=True, zero_division=0
            ),
        }

        trained_models[name] = {
            "model": model,
            "scaler": scaler if name != "naive_bayes" else None,
            "feature_names": FEATURES,
        }

        print(f"Train accuracy (pure):     {train_acc_pure:.2%}")
        print(f"Test accuracy (pure):      {test_acc_pure:.2%}")
        print(f"Test accuracy (seasonal):  {test_acc_seasonal:.2%}")
        print("Confusion matrix (pure):")
        print(confusion_matrix(y_test, test_pred_pure))

        # Save detailed predictions
        pred_df = test_df.copy()
        pred_df["probability"] = test_probs
        pred_df["pred_pure"] = test_pred_pure
        pred_df["pred_seasonal"] = test_pred_seasonal
        pred_df.to_csv(os.path.join(RESULTS_DIR, f"{name}_test_predictions.csv"), index=False)

    # Save models
    with open(os.path.join(MODELS_DIR, "trained_models.pkl"), "wb") as f:
        pickle.dump(trained_models, f)

    # Save metrics
    with open(os.path.join(RESULTS_DIR, "metrics.json"), "w") as f:
        json.dump(results, f, indent=2)

    # Feature importance for Logistic Regression
    lr_coef = trained_models["logistic_regression"]["model"].coef_[0]
    feat_importance = pd.DataFrame({
        "feature": FEATURES,
        "coefficient": lr_coef,
        "abs_coefficient": np.abs(lr_coef),
    }).sort_values("abs_coefficient", ascending=False)
    feat_importance.to_csv(os.path.join(RESULTS_DIR, "logistic_regression_feature_importance.csv"), index=False)
    print("\nLogistic Regression feature importance:")
    print(feat_importance.to_string(index=False))

    return results, trained_models


if __name__ == "__main__":
    train_and_evaluate()
