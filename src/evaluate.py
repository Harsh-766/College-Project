"""Evaluation module for Heart Disease classification models.

Computes accuracy, weighted precision, recall, and F1-score; extracts TN,
FP, FN, TP confusion matrix values; generates formatted classification
reports; and plots confusion matrices and comparative metrics using
matplotlib and seaborn.
"""

from typing import Any, Dict, Optional, Tuple, Union
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def compute_metrics(
    y_true: Union[np.ndarray, list],
    y_pred: Union[np.ndarray, list],
    model_name: str = "Model",
) -> Dict[str, Any]:
    """Calculate comprehensive evaluation metrics for a binary classification model.

    Args:
        y_true: Ground truth binary labels.
        y_pred: Predicted binary labels.
        model_name: Identifier name for the model.

    Returns:
        Dict[str, Any]: Dictionary containing metric values, confusion matrix,
        breakdown counts (TN, FP, FN, TP), and formatted classification report.
    """
    y_true_arr = np.asarray(y_true)
    y_pred_arr = np.asarray(y_pred)

    acc = accuracy_score(y_true_arr, y_pred_arr)
    prec = precision_score(y_true_arr, y_pred_arr, average="weighted", zero_division=0)
    rec = recall_score(y_true_arr, y_pred_arr, average="weighted", zero_division=0)
    f1 = f1_score(y_true_arr, y_pred_arr, average="weighted", zero_division=0)

    # Confusion matrix & breakdown
    cm = confusion_matrix(y_true_arr, y_pred_arr)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
    else:
        tn, fp, fn, tp = int(cm[0, 0]), 0, 0, 0

    clf_report_text = classification_report(
        y_true_arr,
        y_pred_arr,
        target_names=["No Disease (0)", "Disease (1)"],
        digits=4,
    )
    clf_report_dict = classification_report(
        y_true_arr,
        y_pred_arr,
        target_names=["No Disease (0)", "Disease (1)"],
        output_dict=True,
    )

    return {
        "model_name": model_name,
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "confusion_matrix": cm,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "classification_report_text": clf_report_text,
        "classification_report_dict": clf_report_dict,
    }


def generate_comparison_dataframe(
    eval_results: Dict[str, Dict[str, Any]]
) -> pd.DataFrame:
    """Generate a clean side-by-side performance comparison DataFrame.

    Args:
        eval_results: Dictionary mapping model names to their evaluation dicts.

    Returns:
        pd.DataFrame: Tabular comparison with formatted percentages.
    """
    rows = []
    for model_name, metrics in eval_results.items():
        rows.append(
            {
                "Model": model_name,
                "Accuracy": metrics["accuracy"],
                "Precision (Weighted)": metrics["precision"],
                "Recall (Weighted)": metrics["recall"],
                "F1-Score (Weighted)": metrics["f1_score"],
                "True Negatives (TN)": metrics["tn"],
                "False Positives (FP)": metrics["fp"],
                "False Negatives (FN)": metrics["fn"],
                "True Positives (TP)": metrics["tp"],
            }
        )
    return pd.DataFrame(rows)


def plot_confusion_matrix(
    cm: np.ndarray,
    model_name: str,
    ax: Optional[plt.Axes] = None,
    save_path: Optional[str] = None,
    cmap: str = "Blues",
) -> plt.Figure:
    """Plot a stylized confusion matrix heatmap with clear TN, FP, FN, TP annotations.

    Args:
        cm: 2x2 confusion matrix array.
        model_name: Title identifier for the model.
        ax: Optional matplotlib axes to draw on.
        save_path: Optional path to save the generated figure.
        cmap: Color map for the heatmap.

    Returns:
        plt.Figure: The created or updated matplotlib figure.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 5))
    else:
        fig = ax.get_figure()

    # Labels for annotations
    tn, fp, fn, tp = cm.ravel()
    total = np.sum(cm)
    group_counts = [f"{v:d}" for v in cm.flatten()]
    group_percentages = [f"{v/total:.1%}" for v in cm.flatten()]
    group_names = [
        "True Negative\n(Healthy)",
        "False Positive\n(False Alarm)",
        "False Negative\n(Missed Disease)",
        "True Positive\n(Diagnosed)",
    ]

    labels = [
        f"{name}\n\n{count}\n({pct})"
        for name, count, pct in zip(group_names, group_counts, group_percentages)
    ]
    labels = np.asarray(labels).reshape(2, 2)

    sns.heatmap(
        cm,
        annot=labels,
        fmt="",
        cmap=cmap,
        cbar=True,
        ax=ax,
        xticklabels=["Predicted No Disease", "Predicted Disease"],
        yticklabels=["Actual No Disease", "Actual Disease"],
        annot_kws={"size": 10, "weight": "bold"},
    )

    ax.set_title(f"Confusion Matrix — {model_name}", fontsize=13, pad=12, weight="bold")
    ax.set_ylabel("Actual Condition", fontsize=11, weight="semibold")
    ax.set_xlabel("Predicted Condition", fontsize=11, weight="semibold")

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_side_by_side_confusion_matrices(
    cm_gnb: np.ndarray,
    cm_svm: np.ndarray,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """Plot side-by-side confusion matrices for GaussianNB and SVM."""
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    plot_confusion_matrix(cm_gnb, "Gaussian Naïve Bayes", ax=axes[0], cmap="Blues")
    plot_confusion_matrix(cm_svm, "Support Vector Machine (RBF)", ax=axes[1], cmap="Purples")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig


def plot_metrics_comparison_barchart(
    comparison_df: pd.DataFrame,
    save_path: Optional[str] = None,
) -> plt.Figure:
    """Plot a grouped bar chart comparing Accuracy, Precision, Recall, and F1.

    Args:
        comparison_df: Output from generate_comparison_dataframe.
        save_path: Optional path to save the figure.

    Returns:
        plt.Figure: The generated bar chart figure.
    """
    metric_cols = [
        "Accuracy",
        "Precision (Weighted)",
        "Recall (Weighted)",
        "F1-Score (Weighted)",
    ]
    melted_df = comparison_df.melt(
        id_vars=["Model"],
        value_vars=metric_cols,
        var_name="Metric",
        value_name="Score",
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    palette = ["#2b5c8f", "#795290"] if len(comparison_df) == 2 else "viridis"

    sns.barplot(
        data=melted_df,
        x="Metric",
        y="Score",
        hue="Model",
        palette=palette,
        ax=ax,
        edgecolor="black",
        linewidth=0.8,
    )

    ax.set_ylim(0.0, 1.05)
    ax.set_title("Model Performance Benchmark: GaussianNB vs SVM (RBF)", fontsize=13, weight="bold")
    ax.set_ylabel("Score (0.0 - 1.0)", fontsize=11)
    ax.set_xlabel("Evaluation Metric", fontsize=11)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Annotate bar values
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", padding=3, fontsize=9, weight="bold")

    ax.legend(title="Algorithm", loc="lower right")
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
    return fig
