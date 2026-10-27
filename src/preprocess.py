"""Data preprocessing module for Heart Disease classification.

Handles data loading, validation, missing value imputation, stratified
train/test splitting, and feature scaling using StandardScaler to avoid
data leakage.
"""

import os
from typing import List, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Standard 13 clinical features for Heart Disease dataset
FEATURE_NAMES: List[str] = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
]

TARGET_NAME: str = "target"


def validate_columns(df: pd.DataFrame) -> None:
    """Validate that required feature columns and target column are present.

    Args:
        df: Input pandas DataFrame.

    Raises:
        ValueError: If any expected column is missing.
    """
    all_required = FEATURE_NAMES + [TARGET_NAME]
    missing = [col for col in all_required if col not in df.columns]
    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {missing}. "
            f"Expected columns: {all_required}"
        )


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Check and handle missing or null values in the DataFrame.

    Replaces '?' or invalid entries with NaN, converts all feature columns to
    numeric, and imputes missing numeric values with column medians.

    Args:
        df: Input DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame without missing values.
    """
    df_clean = df.copy()

    # Replace common missing value indicators like '?'
    df_clean = df_clean.replace("?", np.nan)

    # Coerce columns to numeric
    for col in FEATURE_NAMES + [TARGET_NAME]:
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

    # Check for missing values
    missing_count = df_clean.isnull().sum().sum()
    if missing_count > 0:
        print(f"[INFO] Found {missing_count} missing values. Imputing with column medians...")
        for col in FEATURE_NAMES:
            if df_clean[col].isnull().any():
                median_val = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(median_val)
        # Drop rows where target is missing if any
        df_clean = df_clean.dropna(subset=[TARGET_NAME])

    # Ensure target is integer 0 or 1
    df_clean[TARGET_NAME] = df_clean[TARGET_NAME].astype(int)

    return df_clean


def load_raw_dataset(csv_path: str) -> pd.DataFrame:
    """Load and validate the raw heart disease CSV.

    Args:
        csv_path: Path to heart.csv.

    Returns:
        pd.DataFrame: Cleaned pandas DataFrame.

    Raises:
        FileNotFoundError: If the CSV path does not exist.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset file not found at: {csv_path}. Please run data/download_data.py first."
        )

    df = pd.read_csv(csv_path)
    # Normalize headers
    df.columns = [c.strip().lower() for c in df.columns]
    validate_columns(df)
    df = handle_missing_values(df)
    return df


def load_and_preprocess_data(
    csv_path: str,
    test_size: float = 0.20,
    random_state: int = 42,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler, List[str]]:
    """Reads CSV, validates columns, performs stratified train/test split,

    and fits StandardScaler strictly on the training set to prevent data leakage.

    Args:
        csv_path: Path to the heart disease dataset CSV.
        test_size: Proportion of the dataset to include in the test split (default: 0.20).
        random_state: Random state seed for reproducibility (default: 42).

    Returns:
        Tuple containing:
            - X_train_scaled (np.ndarray): Scaled training features.
            - X_test_scaled (np.ndarray): Scaled testing features.
            - y_train (np.ndarray): Training target labels.
            - y_test (np.ndarray): Testing target labels.
            - scaler (StandardScaler): Scaler fitted on X_train.
            - feature_names (List[str]): List of the 13 feature names.
    """
    df = load_raw_dataset(csv_path)

    X = df[FEATURE_NAMES].values
    y = df[TARGET_NAME].values

    # Stratified Train/Test Split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    # Feature Scaling: Fit strictly on X_train, transform X_test
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, FEATURE_NAMES


if __name__ == "__main__":
    import sys

    default_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "heart.csv"
    )
    target_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    if os.path.exists(target_path):
        X_tr, X_te, y_tr, y_te, sc, feats = load_and_preprocess_data(target_path)
        print(f"[SUCCESS] Preprocessed successfully!")
        print(f"X_train shape: {X_tr.shape}, X_test shape: {X_te.shape}")
        print(f"y_train distribution: {np.bincount(y_tr)}")
        print(f"y_test distribution: {np.bincount(y_te)}")
    else:
        print(f"[WARNING] Dataset not found at {target_path}. Run data/download_data.py first.")
