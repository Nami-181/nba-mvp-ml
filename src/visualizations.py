"""
Generate visualizations for the NBA MVP prediction project.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)

RESULTS_DIR = "results"
PLOTS_DIR = "reports/figures"
os.makedirs(PLOTS_DIR, exist_ok=True)


def plot_accuracy_comparison():
    """Bar chart comparing model accuracies across evaluation modes."""
    with open(os.path.join(RESULTS_DIR, "metrics.json")) as f:
        metrics = json.load(f)

    models = ["Naive Bayes", "Logistic Regression"]
    train_pure = [metrics["naive_bayes"]["train_accuracy_pure"],
                  metrics["logistic_regression"]["train_accuracy_pure"]]
    test_pure = [metrics["naive_bayes"]["test_accuracy_pure"],
                 metrics["logistic_regression"]["test_accuracy_pure"]]
    test_seasonal = [metrics["naive_bayes"]["test_accuracy_seasonal"],
                     metrics["logistic_regression"]["test_accuracy_seasonal"]]

    x = np.arange(len(models))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8, 5))
    bars1 = ax.bar(x - width, train_pure, width, label="Train (pure)", color="#3498db")
    bars2 = ax.bar(x, test_pure, width, label="Test (pure)", color="#e74c3c")
    bars3 = ax.bar(x + width, test_seasonal, width, label="Test (seasonal)", color="#2ecc71")

    ax.set_ylabel("Accuracy")
    ax.set_title("Model Accuracy Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(models)
    ax.set_ylim(0, 1)
    ax.legend()

    # Add value labels on bars
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f"{height:.2f}",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "accuracy_comparison.png"), dpi=300)
    plt.close()
    print("Saved: accuracy_comparison.png")


def plot_confusion_matrices():
    """Confusion matrices for both models on the pure test set."""
    with open(os.path.join(RESULTS_DIR, "metrics.json")) as f:
        metrics = json.load(f)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for idx, (name, label) in enumerate([
        ("naive_bayes", "Naive Bayes"),
        ("logistic_regression", "Logistic Regression"),
    ]):
        cm = np.array(metrics[name]["confusion_matrix_pure"])
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=["Non-MVP", "MVP"],
                    yticklabels=["Non-MVP", "MVP"],
                    ax=axes[idx])
        axes[idx].set_title(f"{label} — Pure Mode")
        axes[idx].set_xlabel("Predicted")
        axes[idx].set_ylabel("Actual")

    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "confusion_matrices.png"), dpi=300)
    plt.close()
    print("Saved: confusion_matrices.png")


def plot_feature_importance():
    """Bar chart of Logistic Regression coefficients."""
    df = pd.read_csv(os.path.join(RESULTS_DIR,
                                  "logistic_regression_feature_importance.csv"))
    df = df.sort_values("coefficient", ascending=True)

    colors = ["#e74c3c" if c < 0 else "#2ecc71" for c in df["coefficient"]]

    plt.figure(figsize=(8, 5))
    plt.barh(df["feature"], df["coefficient"], color=colors)
    plt.axvline(0, color="black", linewidth=0.8)
    plt.xlabel("Logistic Regression Coefficient")
    plt.title("Feature Importance (Logistic Regression)")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "feature_importance.png"), dpi=300)
    plt.close()
    print("Saved: feature_importance.png")


def plot_prediction_table():
    """Visual table of test-set predictions for Logistic Regression."""
    df = pd.read_csv(os.path.join(RESULTS_DIR,
                                  "logistic_regression_test_predictions.csv"))
    df = df.sort_values(["season", "probability"], ascending=[True, False])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("tight")
    ax.axis("off")

    table_data = df[["season", "player", "team_id", "probability",
                     "MVP", "pred_seasonal"]].copy()
    table_data.columns = ["Season", "Player", "Team", "Prob.", "Actual", "Pred."]
    table_data["Prob."] = table_data["Prob."].round(3)

    table = ax.table(cellText=table_data.values,
                     colLabels=table_data.columns,
                     cellLoc="center",
                     loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)

    # Color correct predictions green, incorrect red
    for i in range(len(table_data)):
        actual = table_data.iloc[i]["Actual"]
        pred = table_data.iloc[i]["Pred."]
        if actual == pred:
            table[(i + 1, 4)].set_facecolor("#d5f5e3")
            table[(i + 1, 5)].set_facecolor("#d5f5e3")
        else:
            table[(i + 1, 4)].set_facecolor("#fadbd8")
            table[(i + 1, 5)].set_facecolor("#fadbd8")

    plt.title("Logistic Regression Predictions on Test Set (2017-2020)",
              fontsize=12, pad=20)
    plt.savefig(os.path.join(PLOTS_DIR, "prediction_table.png"), dpi=300)
    plt.close()
    print("Saved: prediction_table.png")


if __name__ == "__main__":
    plot_accuracy_comparison()
    plot_confusion_matrices()
    plot_feature_importance()
    # plot_prediction_table()  # Optional; can be large
