"""Script to download and verify the Heart Disease dataset.

This script fetches the classic Heart Disease dataset (Cleveland / UCI format),
validates all required feature columns and target distribution, and writes
the clean dataset to data/heart.csv.
"""

import os
import sys
import urllib.request
import pandas as pd

# Expected columns according to project specification
EXPECTED_COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
]

DATASET_URLS = [
    # Cleaned, standardized 303-instance Cleveland Heart Disease dataset
    "https://raw.githubusercontent.com/mrdbourke/zero-to-mastery-ml/master/data/heart-disease.csv",
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/Heart%20Disease%20UCI.csv",
    "https://raw.githubusercontent.com/amankharwal/Website-data/master/heart.csv"
]


def download_and_verify_dataset(output_path: str = "data/heart.csv") -> pd.DataFrame:
    """Download and verify the heart disease dataset.
    
    Args:
        output_path: Destination path for the CSV file.
        
    Returns:
        pd.DataFrame: The verified DataFrame.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = None

    if os.path.exists(output_path):
        print(f"Dataset already exists at {output_path}. Validating...")
        try:
            df = pd.read_csv(output_path)
            if validate_dataframe(df):
                print(f"Dataset valid! Rows: {len(df)}, Columns: {list(df.columns)}")
                return df
            else:
                print("Existing dataset failed validation. Re-fetching...")
        except Exception as e:
            print(f"Error reading existing file: {e}. Re-fetching...")

    for url in DATASET_URLS:
        try:
            print(f"Attempting download from: {url}")
            temp_df = pd.read_csv(url)
            # Normalize column names (lowercase, strip whitespace)
            temp_df.columns = [c.strip().lower() for c in temp_df.columns]
            
            # Map condition / num to target if needed
            if "target" not in temp_df.columns:
                if "condition" in temp_df.columns:
                    temp_df = temp_df.rename(columns={"condition": "target"})
                elif "num" in temp_df.columns:
                    temp_df["target"] = (temp_df["num"] > 0).astype(int)

            if validate_dataframe(temp_df):
                df = temp_df[EXPECTED_COLUMNS].copy()
                df.to_csv(output_path, index=False)
                print(f"Successfully saved validated dataset to {output_path}")
                print(f"Dataset summary: {len(df)} rows, target distribution:\n{df['target'].value_counts()}")
                return df
        except Exception as e:
            print(f"Failed from {url}: {e}")

    # Fallback to fetching via OpenML if URLs fail
    try:
        print("Attempting to fetch dataset from OpenML (dataset id 43493 or heart-disease)...")
        from sklearn.datasets import fetch_openml
        heart_openml = fetch_openml("heart-disease", version=1, as_frame=True, parser="auto")
        df_openml = heart_openml.frame
        df_openml.columns = [c.strip().lower() for c in df_openml.columns]
        if "target" not in df_openml.columns and "num" in df_openml.columns:
            df_openml["target"] = (pd.to_numeric(df_openml["num"], errors="coerce") > 0).astype(int)
        
        # Verify and clean
        df_clean = df_openml.dropna().copy()
        for col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
        df_clean = df_clean.dropna()

        if validate_dataframe(df_clean):
            df_clean[EXPECTED_COLUMNS].to_csv(output_path, index=False)
            print(f"Successfully fetched and saved from OpenML to {output_path}")
            return df_clean[EXPECTED_COLUMNS]
    except Exception as e:
        print(f"OpenML fetch failed: {e}")

    raise RuntimeError(
        "Could not download or verify heart.csv from any source. "
        "Please place a valid heart.csv with columns: " + ", ".join(EXPECTED_COLUMNS)
    )


def validate_dataframe(df: pd.DataFrame) -> bool:
    """Check if the dataframe has required columns and valid target values."""
    if df is None or df.empty:
        return False
    missing_cols = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing_cols:
        print(f"Missing expected columns: {missing_cols}")
        return False
    if not set(df["target"].dropna().unique()).issubset({0, 1}):
        print(f"Invalid target values: {df['target'].unique()}")
        return False
    return True


if __name__ == "__main__":
    download_and_verify_dataset()
