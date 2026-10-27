"""Streamlit Web Dashboard for Heart Disease Prediction & Model Comparison.

Compares Gaussian Naïve Bayes and Support Vector Machine (RBF Kernel)
with EDA, benchmark comparisons, and real-time clinical diagnosis.
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# Configure sys.path so modules can be imported
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from src.evaluate import (
    compute_metrics,
    generate_comparison_dataframe,
    plot_confusion_matrix,
    plot_metrics_comparison_barchart,
    plot_side_by_side_confusion_matrices,
)
from src.preprocess import FEATURE_NAMES, TARGET_NAME, load_and_preprocess_data, load_raw_dataset
from src.train import train_models

# Page Configuration
st.set_page_config(
    page_title="CardioPredict ML | GaussianNB vs SVM",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished, clinical UI
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .badge-positive {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-negative {
        background-color: #DCFCE7;
        color: #166534;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_PATH = os.path.join(APP_DIR, "data", "heart.csv")
MODELS_DIR = os.path.join(APP_DIR, "saved_models")
SCALER_PATH = os.path.join(MODELS_DIR, "scaler.joblib")
GNB_PATH = os.path.join(MODELS_DIR, "gaussian_nb.joblib")
SVM_PATH = os.path.join(MODELS_DIR, "svm_rbf.joblib")
METRICS_PATH = os.path.join(MODELS_DIR, "metrics_summary.json")


# Clinical descriptions and reference ranges
FEATURE_METADATA = {
    "age": {"name": "Age", "desc": "Patient age in years", "min": 25, "max": 85, "default": 54},
    "sex": {
        "name": "Sex",
        "desc": "Biological sex",
        "options": {1: "Male (1)", 0: "Female (0)"},
        "default": 1,
    },
    "cp": {
        "name": "Chest Pain Type (cp)",
        "desc": "Chest pain classification",
        "options": {
            0: "0: Typical Angina",
            1: "1: Atypical Angina",
            2: "2: Non-anginal Pain",
            3: "3: Asymptomatic",
        },
        "default": 0,
    },
    "trestbps": {
        "name": "Resting Blood Pressure (trestbps)",
        "desc": "Resting BP in mm Hg on admission (Normal: < 120 mm Hg)",
        "min": 90,
        "max": 200,
        "default": 130,
    },
    "chol": {
        "name": "Serum Cholesterol (chol)",
        "desc": "Serum cholesterol in mg/dl (Desirable: < 200 mg/dl)",
        "min": 100,
        "max": 580,
        "default": 240,
    },
    "fbs": {
        "name": "Fasting Blood Sugar (fbs)",
        "desc": "Fasting blood sugar > 120 mg/dl (Diabetic indicator)",
        "options": {0: "False: <= 120 mg/dl (0)", 1: "True: > 120 mg/dl (1)"},
        "default": 0,
    },
    "restecg": {
        "name": "Resting ECG (restecg)",
        "desc": "Resting electrocardiographic results",
        "options": {
            0: "0: Normal",
            1: "1: ST-T Wave Abnormality",
            2: "2: Probable/Definite Left Ventricular Hypertrophy",
        },
        "default": 0,
    },
    "thalach": {
        "name": "Maximum Heart Rate (thalach)",
        "desc": "Maximum heart rate achieved during exercise stress test",
        "min": 60,
        "max": 220,
        "default": 150,
    },
    "exang": {
        "name": "Exercise Induced Angina (exang)",
        "desc": "Angina episode triggered by exercise",
        "options": {0: "No (0)", 1: "Yes (1)"},
        "default": 0,
    },
    "oldpeak": {
        "name": "ST Depression (oldpeak)",
        "desc": "ST depression induced by exercise relative to rest",
        "min": 0.0,
        "max": 6.5,
        "step": 0.1,
        "default": 1.0,
    },
    "slope": {
        "name": "ST Slope (slope)",
        "desc": "Slope of the peak exercise ST segment",
        "options": {0: "0: Upsloping", 1: "1: Flat", 2: "2: Downsloping"},
        "default": 1,
    },
    "ca": {
        "name": "Major Vessels Colored (ca)",
        "desc": "Number of major vessels (0-3) colored by fluoroscopy",
        "options": {0: "0 Vessels", 1: "1 Vessel", 2: "2 Vessels", 3: "3 Vessels"},
        "default": 0,
    },
    "thal": {
        "name": "Thalassemia (thal)",
        "desc": "Thallium heart scan result",
        "options": {
            1: "1: Normal blood flow",
            2: "2: Fixed defect",
            3: "3: Reversible defect",
        },
        "default": 2,
    },
}


@st.cache_data
def get_cached_raw_data() -> pd.DataFrame:
    """Load and cache the raw dataset."""
    if not os.path.exists(DATA_PATH):
        from data.download_data import download_and_verify_dataset
        download_and_verify_dataset(DATA_PATH)
    return load_raw_dataset(DATA_PATH)


@st.cache_resource
def load_or_train_pipeline() -> Tuple[Any, Any, Any, Dict[str, Any], pd.DataFrame]:
    """Load trained models and scaler, or trigger training if not present."""
    if (
        not os.path.exists(SCALER_PATH)
        or not os.path.exists(GNB_PATH)
        or not os.path.exists(SVM_PATH)
    ):
        with st.spinner("Initializing models and running training pipeline..."):
            train_models(DATA_PATH, MODELS_DIR)

    scaler = joblib.load(SCALER_PATH)
    gnb = joblib.load(GNB_PATH)
    svm = joblib.load(SVM_PATH)

    # Load test split for metrics
    X_train, X_test, y_train, y_test, _, _ = load_and_preprocess_data(DATA_PATH)

    # Compute metrics fresh
    y_pred_gnb = gnb.predict(X_test)
    y_pred_svm = svm.predict(X_test)

    eval_results = {
        "Gaussian Naïve Bayes": compute_metrics(y_test, y_pred_gnb, "Gaussian Naïve Bayes"),
        "Support Vector Machine": compute_metrics(y_test, y_pred_svm, "Support Vector Machine"),
    }
    comparison_df = generate_comparison_dataframe(eval_results)

    return scaler, gnb, svm, eval_results, comparison_df


def main():
    st.markdown('<div class="main-header">❤️ CardioPredict ML: Heart Disease Classification</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Production-grade benchmark comparing <b>Gaussian Naïve Bayes</b> vs. <b>Support Vector Machine (RBF Kernel)</b> on clinical data</div>',
        unsafe_allow_html=True,
    )

    # Ensure dataset and models are available
    try:
        raw_df = get_cached_raw_data()
        scaler, gnb, svm, eval_results, comparison_df = load_or_train_pipeline()
    except Exception as e:
        st.error(f"Error initializing application pipeline: {e}")
        st.info("Ensure the dataset is available in `data/heart.csv` or internet access is enabled to fetch it.")
        st.stop()

    # ==========================================
    # SIDEBAR CONTROLS
    # ==========================================
    with st.sidebar:
        st.header("⚙️ Model Configuration")
        selected_model_name = st.selectbox(
            "Primary Evaluation Model:",
            ("Gaussian Naïve Bayes", "Support Vector Machine"),
            index=0,
            help="Select model to inspect hyperparameters and use for individual focus.",
        )

        selected_model = gnb if selected_model_name == "Gaussian Naïve Bayes" else svm

        st.markdown("---")
        st.subheader("🔍 Parameter Inspector")
        with st.expander("View Algorithm Hyperparameters", expanded=True):
            if selected_model_name == "Gaussian Naïve Bayes":
                st.code(
                    f"Algorithm: GaussianNB\n"
                    f"var_smoothing: {selected_model.var_smoothing}\n"
                    f"Classes: {selected_model.classes_.tolist()}\n"
                    f"Priors: {selected_model.class_prior_ if hasattr(selected_model, 'class_prior_') else 'Empirical'}",
                    language="yaml",
                )
            else:
                st.code(
                    f"Algorithm: SVC (Support Vector Classifier)\n"
                    f"Kernel: {selected_model.kernel}\n"
                    f"C (Regularization): {selected_model.C}\n"
                    f"Gamma: {selected_model.gamma}\n"
                    f"Probability Estimation: {selected_model.probability}\n"
                    f"Support Vectors: {selected_model.n_support_.tolist()}\n"
                    f"Random State: {selected_model.random_state}",
                    language="yaml",
                )

        st.markdown("---")
        st.subheader("🔁 Pipeline Retraining")
        if st.button("Force Retrain Models", use_container_width=True):
            with st.spinner("Retraining both models..."):
                train_models(DATA_PATH, MODELS_DIR)
                st.cache_resource.clear()
                st.success("Retrained and refreshed cache!")
                st.rerun()

        st.caption("Heart Disease UCI Cleveland Dataset • Standardized Split 80/20")

    # ==========================================
    # MAIN PANEL TABS
    # ==========================================
    tab1, tab2, tab3 = st.tabs([
        "📊 Tab 1: Dataset Overview & EDA",
        "📈 Tab 2: Model Performance & Comparison",
        "🩺 Tab 3: Live Patient Diagnosis Tool",
    ])

    # ------------------------------------------
    # TAB 1: EDA & DATASET OVERVIEW
    # ------------------------------------------
    with tab1:
        st.subheader("📋 Dataset Overview")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Total Patients", f"{len(raw_df)}")
        col_m2.metric("Total Clinical Features", f"{len(FEATURE_NAMES)}")
        disease_count = (raw_df["target"] == 1).sum()
        disease_pct = (disease_count / len(raw_df)) * 100
        col_m3.metric("Patients with Disease", f"{disease_count} ({disease_pct:.1f}%)")
        healthy_count = (raw_df["target"] == 0).sum()
        healthy_pct = (healthy_count / len(raw_df)) * 100
        col_m4.metric("Healthy Patients", f"{healthy_count} ({healthy_pct:.1f}%)")

        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("##### First 5 Sample Records")
            st.dataframe(raw_df.head(), use_container_width=True)

        with col_right:
            st.markdown("##### Missing Values & Column Types")
            summary_info = pd.DataFrame({
                "Data Type": raw_df.dtypes.astype(str),
                "Missing Values": raw_df.isnull().sum(),
                "Unique Values": raw_df.nunique(),
            })
            st.dataframe(summary_info, use_container_width=True)

        st.markdown("---")
        st.subheader("🔥 Clinical Features Correlation Heatmap")
        fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
        corr_matrix = raw_df[FEATURE_NAMES + [TARGET_NAME]].corr()
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt=".2f",
            cmap="vlag",
            center=0,
            linewidths=0.5,
            ax=ax_corr,
            cbar_kws={"shrink": 0.8},
        )
        ax_corr.set_title("Pearson Correlation Matrix (Features vs. Disease Target)", fontsize=12, weight="bold")
        st.pyplot(fig_corr)
        plt.close(fig_corr)

        st.markdown("---")
        st.subheader("📈 Feature Distributions by Disease Diagnosis")
        dist_feature = st.selectbox(
            "Select Continuous Feature to Analyze:",
            ["age", "trestbps", "chol", "thalach", "oldpeak"],
            index=3,
        )

        fig_dist, axes_dist = plt.subplots(1, 2, figsize=(12, 4.5))

        # Create explicit categorical condition column for clean plotting
        plot_df = raw_df.copy()
        plot_df["Condition"] = plot_df["target"].map({0: "No Disease (0)", 1: "Disease (1)"})

        # Histogram with KDE
        sns.histplot(
            data=plot_df,
            x=dist_feature,
            hue="Condition",
            kde=True,
            palette={"No Disease (0)": "#22c55e", "Disease (1)": "#ef4444"},
            element="step",
            ax=axes_dist[0],
        )
        axes_dist[0].set_title(f"Distribution of {dist_feature.upper()}", weight="bold")

        # Boxplot with explicit hue to avoid Seaborn palette deprecation & ValueError
        sns.boxplot(
            data=plot_df,
            x="Condition",
            y=dist_feature,
            hue="Condition",
            palette={"No Disease (0)": "#86efac", "Disease (1)": "#fca5a5"},
            legend=False,
            ax=axes_dist[1],
        )
        axes_dist[1].set_xlabel("Cardiac Diagnosis", weight="semibold")
        axes_dist[1].set_title(f"{dist_feature.upper()} Boxplot by Target", weight="bold")

        st.pyplot(fig_dist)
        plt.close(fig_dist)

    # ------------------------------------------
    # TAB 2: MODEL PERFORMANCE & COMPARISON
    # ------------------------------------------
    with tab2:
        st.subheader("⚖️ Side-by-Side Model Benchmark")
        st.markdown(
            "Evaluation on 20% stratified test set. Both models were trained strictly on standardized training data."
        )

        # Comparative dataframe with highlight
        st.dataframe(
            comparison_df.style.format({
                "Accuracy": "{:.4f}",
                "Precision (Weighted)": "{:.4f}",
                "Recall (Weighted)": "{:.4f}",
                "F1-Score (Weighted)": "{:.4f}",
            }).highlight_max(
                subset=["Accuracy", "Precision (Weighted)", "Recall (Weighted)", "F1-Score (Weighted)"],
                color="#C6F6D5",
            ),
            use_container_width=True,
        )

        # Performance metric bar chart
        st.markdown("##### 📊 Metric Comparison Visualization")
        fig_bar = plot_metrics_comparison_barchart(comparison_df)
        st.pyplot(fig_bar)
        plt.close(fig_bar)

        st.markdown("---")
        st.subheader("🧩 Confusion Matrix Breakdown")
        col_cm1, col_cm2 = st.columns(2)

        with col_cm1:
            st.markdown("#### Gaussian Naïve Bayes")
            gnb_m = eval_results["Gaussian Naïve Bayes"]
            fig_gnb = plot_confusion_matrix(gnb_m["confusion_matrix"], "Gaussian Naïve Bayes", cmap="Blues")
            st.pyplot(fig_gnb)
            plt.close(fig_gnb)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("TN", gnb_m["tn"])
            c2.metric("FP", gnb_m["fp"])
            c3.metric("FN", gnb_m["fn"])
            c4.metric("TP", gnb_m["tp"])

            with st.expander("View Full Classification Report (GaussianNB)"):
                st.text(gnb_m["classification_report_text"])

        with col_cm2:
            st.markdown("#### Support Vector Machine (RBF)")
            svm_m = eval_results["Support Vector Machine"]
            fig_svm = plot_confusion_matrix(svm_m["confusion_matrix"], "SVM (RBF Kernel)", cmap="Purples")
            st.pyplot(fig_svm)
            plt.close(fig_svm)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("TN", svm_m["tn"])
            c2.metric("FP", svm_m["fp"])
            c3.metric("FN", svm_m["fn"])
            c4.metric("TP", svm_m["tp"])

            with st.expander("View Full Classification Report (SVM)"):
                st.text(svm_m["classification_report_text"])

        st.markdown("---")
        st.info(
            "💡 **Clinical Interpretation Note**: In heart disease screening, **False Negatives (FN)** are high-risk "
            "as they represent patients with heart disease erroneously diagnosed as healthy. A model with high **Recall (Sensitivity)** "
            "minimizes missed diagnoses."
        )

    # ------------------------------------------
    # TAB 3: LIVE PATIENT DIAGNOSIS TOOL
    # ------------------------------------------
    with tab3:
        st.subheader("🩺 Real-Time Patient Risk Assessment")
        st.markdown("Enter patient clinical attributes to perform real-time disease classification.")

        # Preset profiles
        preset_choice = st.radio(
            "Load Clinical Preset Profile:",
            ("Custom Patient Input", "Preset 1: Healthy Profile (Low Risk)", "Preset 2: Cardiac Patient (High Risk)"),
            horizontal=True,
        )

        preset_data = {}
        if preset_choice == "Preset 1: Healthy Profile (Low Risk)":
            preset_data = {
                "age": 42, "sex": 0, "cp": 2, "trestbps": 115, "chol": 180,
                "fbs": 0, "restecg": 0, "thalach": 172, "exang": 0, "oldpeak": 0.0,
                "slope": 2, "ca": 0, "thal": 2,
            }
        elif preset_choice == "Preset 2: Cardiac Patient (High Risk)":
            preset_data = {
                "age": 63, "sex": 1, "cp": 0, "trestbps": 160, "chol": 290,
                "fbs": 1, "restecg": 2, "thalach": 110, "exang": 1, "oldpeak": 3.2,
                "slope": 1, "ca": 2, "thal": 3,
            }

        st.markdown("##### Clinical Attributes Form")
        with st.form("patient_diagnosis_form"):
            col1, col2, col3 = st.columns(3)

            with col1:
                age_val = st.slider(
                    "Age (years)",
                    min_value=FEATURE_METADATA["age"]["min"],
                    max_value=FEATURE_METADATA["age"]["max"],
                    value=preset_data.get("age", FEATURE_METADATA["age"]["default"]),
                )
                sex_val = st.selectbox(
                    "Sex",
                    options=list(FEATURE_METADATA["sex"]["options"].keys()),
                    format_func=lambda x: FEATURE_METADATA["sex"]["options"][x],
                    index=list(FEATURE_METADATA["sex"]["options"].keys()).index(preset_data.get("sex", 1)),
                )
                cp_val = st.selectbox(
                    "Chest Pain Type (cp)",
                    options=list(FEATURE_METADATA["cp"]["options"].keys()),
                    format_func=lambda x: FEATURE_METADATA["cp"]["options"][x],
                    index=list(FEATURE_METADATA["cp"]["options"].keys()).index(preset_data.get("cp", 0)),
                )
                trestbps_val = st.number_input(
                    "Resting Blood Pressure (mm Hg)",
                    min_value=FEATURE_METADATA["trestbps"]["min"],
                    max_value=FEATURE_METADATA["trestbps"]["max"],
                    value=preset_data.get("trestbps", 130),
                )
                chol_val = st.number_input(
                    "Serum Cholesterol (mg/dl)",
                    min_value=FEATURE_METADATA["chol"]["min"],
                    max_value=FEATURE_METADATA["chol"]["max"],
                    value=preset_data.get("chol", 240),
                )

            with col2:
                fbs_val = st.selectbox(
                    "Fasting Blood Sugar > 120 mg/dl",
                    options=list(FEATURE_METADATA["fbs"]["options"].keys()),
                    format_func=lambda x: FEATURE_METADATA["fbs"]["options"][x],
                    index=list(FEATURE_METADATA["fbs"]["options"].keys()).index(preset_data.get("fbs", 0)),
                )
                restecg_val = st.selectbox(
                    "Resting ECG (restecg)",
                    options=list(FEATURE_METADATA["restecg"]["options"].keys()),
                    format_func=lambda x: FEATURE_METADATA["restecg"]["options"][x],
                    index=list(FEATURE_METADATA["restecg"]["options"].keys()).index(preset_data.get("restecg", 0)),
                )
                thalach_val = st.slider(
                    "Max Heart Rate Achieved (thalach)",
                    min_value=FEATURE_METADATA["thalach"]["min"],
                    max_value=FEATURE_METADATA["thalach"]["max"],
                    value=preset_data.get("thalach", 150),
                )
                exang_val = st.selectbox(
                    "Exercise Induced Angina (exang)",
                    options=list(FEATURE_METADATA["exang"]["options"].keys()),
                    format_func=lambda x: FEATURE_METADATA["exang"]["options"][x],
                    index=list(FEATURE_METADATA["exang"]["options"].keys()).index(preset_data.get("exang", 0)),
                )

            with col3:
                oldpeak_val = st.slider(
                    "ST Depression (oldpeak)",
                    min_value=float(FEATURE_METADATA["oldpeak"]["min"]),
                    max_value=float(FEATURE_METADATA["oldpeak"]["max"]),
                    value=float(preset_data.get("oldpeak", 1.0)),
                    step=FEATURE_METADATA["oldpeak"]["step"],
                )
                slope_val = st.selectbox(
                    "ST Slope (slope)",
                    options=list(FEATURE_METADATA["slope"]["options"].keys()),
                    format_func=lambda x: FEATURE_METADATA["slope"]["options"][x],
                    index=list(FEATURE_METADATA["slope"]["options"].keys()).index(preset_data.get("slope", 1)),
                )
                ca_val = st.selectbox(
                    "Major Vessels Colored (ca)",
                    options=list(FEATURE_METADATA["ca"]["options"].keys()),
                    format_func=lambda x: FEATURE_METADATA["ca"]["options"][x],
                    index=list(FEATURE_METADATA["ca"]["options"].keys()).index(preset_data.get("ca", 0)),
                )
                thal_val = st.selectbox(
                    "Thalassemia (thal)",
                    options=list(FEATURE_METADATA["thal"]["options"].keys()),
                    format_func=lambda x: FEATURE_METADATA["thal"]["options"][x],
                    index=list(FEATURE_METADATA["thal"]["options"].keys()).index(preset_data.get("thal", 2)),
                )

            submitted = st.form_submit_button("⚡ Run Real-Time Cardiac Diagnosis", use_container_width=True)

        if submitted:
            # Construct patient record
            patient_record = np.array([
                [
                    age_val,
                    sex_val,
                    cp_val,
                    trestbps_val,
                    chol_val,
                    fbs_val,
                    restecg_val,
                    thalach_val,
                    exang_val,
                    oldpeak_val,
                    slope_val,
                    ca_val,
                    thal_val,
                ]
            ])

            # Transform with saved StandardScaler
            scaled_input = scaler.transform(patient_record)

            # Predictions
            pred_gnb = gnb.predict(scaled_input)[0]
            prob_gnb = gnb.predict_proba(scaled_input)[0]

            pred_svm = svm.predict(scaled_input)[0]
            prob_svm = svm.predict_proba(scaled_input)[0]

            st.markdown("---")
            st.subheader("📋 Diagnostic Predictions & Confidence Breakdown")

            res_col1, res_col2 = st.columns(2)

            with res_col1:
                st.markdown("### Gaussian Naïve Bayes")
                if pred_gnb == 1:
                    st.error("🚨 **Heart Disease Detected** (Class 1)")
                else:
                    st.success("✅ **No Heart Disease Detected** (Class 0)")

                p_disease_gnb = float(np.clip(prob_gnb[1], 0.0, 1.0)) * 100
                st.write(f"**Confidence Probability of Disease:** `{p_disease_gnb:.1f}%`")
                st.progress(float(np.clip(prob_gnb[1], 0.0, 1.0)))

                st.markdown(
                    f"- Healthy (No Disease): **{prob_gnb[0]*100:.1f}%**\n"
                    f"- Disease Detected: **{prob_gnb[1]*100:.1f}%**"
                )

            with res_col2:
                st.markdown("### Support Vector Machine (RBF)")
                if pred_svm == 1:
                    st.error("🚨 **Heart Disease Detected** (Class 1)")
                else:
                    st.success("✅ **No Heart Disease Detected** (Class 0)")

                p_disease_svm = float(np.clip(prob_svm[1], 0.0, 1.0)) * 100
                st.write(f"**Confidence Probability of Disease:** `{p_disease_svm:.1f}%`")
                st.progress(float(np.clip(prob_svm[1], 0.0, 1.0)))

                st.markdown(
                    f"- Healthy (No Disease): **{prob_svm[0]*100:.1f}%**\n"
                    f"- Disease Detected: **{prob_svm[1]*100:.1f}%**"
                )

            # Clinical Insights & Observations
            st.markdown("#### 🔍 Clinical Factor Observations")
            observations = []
            if trestbps_val >= 140:
                observations.append(f"⚠️ **Hypertension**: Resting BP ({trestbps_val} mmHg) is elevated (Stage 2 Hypertension).")
            if chol_val >= 240:
                observations.append(f"⚠️ **High Cholesterol**: Serum cholesterol ({chol_val} mg/dl) is in the high-risk range (>= 240 mg/dl).")
            if fbs_val == 1:
                observations.append("⚠️ **Elevated Fasting Blood Sugar**: > 120 mg/dl indicates potential impaired fasting glucose or diabetes.")
            if exang_val == 1:
                observations.append("⚠️ **Exercise Induced Angina**: Presence of chest discomfort under physical exertion.")
            if oldpeak_val >= 2.0:
                observations.append(f"⚠️ **Marked ST Depression**: oldpeak = {oldpeak_val} suggests significant myocardial ischemia.")
            if ca_val > 0:
                observations.append(f"⚠️ **Coronary Calcification**: {ca_val} major blood vessel(s) colored by fluoroscopy.")

            if observations:
                for obs in observations:
                    st.markdown(obs)
            else:
                st.success("🌟 All monitored physical markers are within standard normal baseline ranges.")


if __name__ == "__main__":
    main()
