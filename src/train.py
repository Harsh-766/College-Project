"""Model training and artifact serialization module.

Trains Gaussian Naïve Bayes and Support Vector Machine (RBF kernel)
on preprocessed heart disease data, evaluates performance on hold-out
test data, and serializes trained models and the fitted scaler into saved_models/.
"""

import json
import os
import sys
from typing import Any, Dict, Tuple
import joblib
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Add project root to sys.path if invoked directly
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.evaluate import (
    compute_metrics,
    generate_comparison_dataframe,
    plot_side_by_side_confusion_matrices,
    plot_metrics_comparison_barchart,
)
from src.preprocess import FEATURE_NAMES, load_and_preprocess_data


def train_models(
    data_path: str,
    models_dir: str = "saved_models",
) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Train GaussianNB and SVC, evaluate on test split, and save artifacts.

    Args:
        data_path: Path to dataset CSV.
        models_dir: Destination directory for serialized model artifacts.

    Returns:
        Tuple containing:
            - results (Dict[str, Any]): Dictionary of trained models, scaler, and metrics.
            - comparison_df (pd.DataFrame): Comparison table of both models.
    """
    os.makedirs(models_dir, exist_ok=True)

    print(f"[INFO] Loading and preprocessing dataset from: {data_path}")
    X_train, X_test, y_train, y_test, scaler, feature_names = load_and_preprocess_data(
        data_path, test_size=0.20, random_state=42
    )
    print(f"[INFO] Dataset split: {X_train.shape[0]} train rows, {X_test.shape[0]} test rows.")

    # 1. Instantiate models
    # Note: probability=True enables predict_proba for live diagnosis confidence scores
    models = {
        "Gaussian Naïve Bayes": GaussianNB(),
        "Support Vector Machine": SVC(kernel="rbf", probability=True, random_state=42),
    }

    eval_results: Dict[str, Dict[str, Any]] = {}
    trained_models: Dict[str, Any] = {}

    print("\n" + "=" * 60)
    print("STARTING MODEL TRAINING & EVALUATION")
    print("=" * 60)

    for name, model in models.items():
        print(f"\n[TRAINING] {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        metrics = compute_metrics(y_test, y_pred, model_name=name)
        eval_results[name] = metrics
        trained_models[name] = model

        print(f"[EVALUATION] {name}:")
        print(f"  • Accuracy:           {metrics['accuracy']:.4f}")
        print(f"  • Precision (wt):     {metrics['precision']:.4f}")
        print(f"  • Recall (wt):        {metrics['recall']:.4f}")
        print(f"  • F1-Score (wt):      {metrics['f1_score']:.4f}")
        print(f"  • Confusion Matrix:   TN={metrics['tn']}, FP={metrics['fp']}, FN={metrics['fn']}, TP={metrics['tp']}")
        print("\nClassification Report:")
        print(metrics["classification_report_text"])

    # Build comparison dataframe
    comparison_df = generate_comparison_dataframe(eval_results)
    print("=" * 60)
    print("SIDE-BY-SIDE MODEL BENCHMARK")
    print("=" * 60)
    print(comparison_df.to_string(index=False))

    # 2. Serialize artifacts
    print(f"\n[INFO] Saving model artifacts to '{models_dir}'...")
    scaler_path = os.path.join(models_dir, "scaler.joblib")
    gnb_path = os.path.join(models_dir, "gaussian_nb.joblib")
    svm_path = os.path.join(models_dir, "svm_rbf.joblib")
    metadata_path = os.path.join(models_dir, "metrics_summary.json")

    joblib.dump(scaler, scaler_path)
    joblib.dump(trained_models["Gaussian Naïve Bayes"], gnb_path)
    joblib.dump(trained_models["Support Vector Machine"], svm_path)

    # Save summary metadata in JSON (excluding numpy objects)
    serializable_summary = {
        "features": feature_names,
        "models": {
            k: {
                "accuracy": v["accuracy"],
                "precision": v["precision"],
                "recall": v["recall"],
                "f1_score": v["f1_score"],
                "tn": v["tn"],
                "fp": v["fp"],
                "fn": v["fn"],
                "tp": v["tp"],
                "classification_report": v["classification_report_dict"],
            }
            for k, v in eval_results.items()
        },
    }
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(serializable_summary, f, indent=2)

    # Save visual benchmark charts
    try:
        cm_gnb = eval_results["Gaussian Naïve Bayes"]["confusion_matrix"]
        cm_svm = eval_results["Support Vector Machine"]["confusion_matrix"]
        plot_side_by_side_confusion_matrices(
            cm_gnb, cm_svm, save_path=os.path.join(models_dir, "confusion_matrices.png")
        )
        plot_metrics_comparison_barchart(
            comparison_df, save_path=os.path.join(models_dir, "metrics_comparison.png")
        )
        print(f"[INFO] Saved comparison charts in '{models_dir}'")
    except Exception as e:
        print(f"[WARNING] Could not save visualization figures: {e}")

    print(f"[SUCCESS] All artifacts successfully saved:")
    print(f"  • Scaler:       {scaler_path}")
    print(f"  • GaussianNB:   {gnb_path}")
    print(f"  • SVM (RBF):    {svm_path}")
    print(f"  • Metrics:      {metadata_path}")

    return {
        "models": trained_models,
        "scaler": scaler,
        "eval_results": eval_results,
        "test_data": (X_test, y_test),
    }, comparison_df


if __name__ == "__main__":
    default_csv = os.path.join(PROJECT_ROOT, "data", "heart.csv")
    models_target_dir = os.path.join(PROJECT_ROOT, "saved_models")

    # If data does not exist, run downloader first
    if not os.path.exists(default_csv):
        print(f"[INFO] '{default_csv}' not found. Attempting download...")
        from data.download_data import download_and_verify_dataset
        download_and_verify_dataset(default_csv)

    train_models(default_csv, models_target_dir)
