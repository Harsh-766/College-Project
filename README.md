# ❤️ CardioPredict ML: Heart Disease Classification Benchmark

A production-grade Machine Learning classification system and clinical decision support dashboard comparing **Gaussian Naïve Bayes** and **Support Vector Machine (RBF Kernel)** on the classic Heart Disease dataset.

---

## 📌 Project Overview

Cardiovascular disease is the leading cause of morbidity globally. Early, reliable risk stratification allows physicians to intervene proactively. This project delivers an end-to-end, production-ready machine learning pipeline featuring:

- **Strict Data Preprocessing**: Missing value imputation, stratified 80/20 train/test splitting, and `StandardScaler` fitted strictly on training data to prevent data leakage.
- **Model Comparison**: Rigorous head-to-head benchmark between a probabilistic generative classifier (**Gaussian Naïve Bayes**) and a maximum-margin discriminative classifier (**Support Vector Machine** with Radial Basis Function kernel).
- **Comprehensive Evaluation**: Metrics including Accuracy, Weighted Precision, Recall, F1-Score, detailed confusion matrices with TN, FP, FN, TP breakdowns, and full classification reports.
- **Interactive Streamlit Web Dashboard**: 3-tier clinical interface with EDA visualizations, side-by-side metric charts, and an interactive real-time patient risk diagnosis engine.

---

## 🏗️ Architecture & Directory Structure

```text
heart-disease-ml/
├── data/
│   ├── heart.csv               # 13 clinical features + binary target
│   └── download_data.py        # Automated dataset retrieval & verification
├── src/
│   ├── __init__.py
│   ├── preprocess.py           # Clean data loading, stratified split, leakage-free scaling
│   ├── train.py                # Model training, test evaluation, artifact persistence
│   └── evaluate.py             # Metrics calculation, confusion matrix & comparative charts
├── saved_models/               # Serialized artifacts (joblib & json)
│   ├── scaler.joblib           # Fitted StandardScaler
│   ├── gaussian_nb.joblib      # Trained GaussianNB model
│   ├── svm_rbf.joblib          # Trained SVC(kernel='rbf', probability=True)
│   └── metrics_summary.json    # JSON report of benchmark metrics
├── app.py                      # Multi-tab Streamlit web application
├── requirements.txt            # Project dependencies
└── README.md                   # Complete documentation
```

---

## 🔬 Dataset Description

The dataset incorporates 13 clinical attributes used to classify cardiac risk (`target`: `1` = Heart Disease, `0` = Healthy):

| Attribute | Name | Clinical Description | Range / Units |
| :--- | :--- | :--- | :--- |
| `age` | Age | Patient age | 29 – 77 years |
| `sex` | Sex | Biological sex | `1` = Male, `0` = Female |
| `cp` | Chest Pain Type | Classification of chest discomfort | `0`: Typical Angina, `1`: Atypical Angina, `2`: Non-anginal, `3`: Asymptomatic |
| `trestbps` | Resting BP | Resting blood pressure on admission | 94 – 200 mm Hg |
| `chol` | Cholesterol | Serum cholesterol | 126 – 564 mg/dl |
| `fbs` | Fasting Blood Sugar | Blood sugar > 120 mg/dl | `1` = True, `0` = False |
| `restecg` | Resting ECG | Electrocardiogram results | `0`: Normal, `1`: ST-T Abnormality, `2`: LVH |
| `thalach` | Max Heart Rate | Peak heart rate achieved | 71 – 202 bpm |
| `exang` | Exercise Angina | Exercise-induced angina | `1` = Yes, `0` = No |
| `oldpeak` | ST Depression | ST depression induced by exercise vs rest | 0.0 – 6.2 |
| `slope` | ST Slope | Slope of the peak exercise ST segment | `0`: Upsloping, `1`: Flat, `2`: Downsloping |
| `ca` | Major Vessels | Major vessels (0–3) colored by fluoroscopy | 0 – 3 |
| `thal` | Thalassemia | Thallium scintigraphy defect scan | `1`: Normal, `2`: Fixed defect, `3`: Reversible defect |
| **`target`** | **Diagnosis** | **Target Condition** | **`1`: Disease Present, `0`: Disease Absent** |

---

## 🧠 Algorithmic Comparison: GaussianNB vs. SVM

| Property | Gaussian Naïve Bayes (GaussianNB) | Support Vector Machine (SVM RBF) |
| :--- | :--- | :--- |
| **Model Paradigm** | Generative, Probabilistic | Discriminative, Geometric Maximum-Margin |
| **Core Assumption** | Features are conditionally independent given class: $P(X \mid y) = \prod P(x_i \mid y)$ | Finds optimal separating hyperplane maximizing distance to nearest support vectors |
| **Feature Correlation** | Sensitive to highly correlated features (may overweigh redundant signals) | Handles non-linear feature interactions seamlessly via RBF kernel mapping |
| **Data Scaling** | Does not strictly require scaling (estimates feature means & variances) | **Crucially requires scaling**; unscaled features distort Euclidean/RBF distances |
| **Training Complexity** | $O(N \cdot d)$ — Extremely fast linear pass | $O(N^2 \cdot d)$ to $O(N^3)$ — Quadratic in sample size |
| **Clinical Suitability** | Fast baseline with direct Bayesian posterior probability estimation | High predictive precision and resistance to overfitting in non-linear clinical boundaries |

---

## 🚀 Quickstart & Installation

### 1. Clone or Navigate to Directory
```bash
cd heart-disease-ml
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. Fetch the Dataset & Train Models
```bash
# Verify or fetch data
python data/download_data.py

# Train both algorithms and save artifacts
python src/train.py
```

### 5. Launch the Streamlit Interactive Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📊 Evaluation & Clinical Considerations

- **Leakage Prevention**: All transformations (`StandardScaler`) are computed strictly using `scaler.fit_transform(X_train)` and applied via `scaler.transform(X_test)`.
- **Stratified Validation**: The 80/20 train/test split preserves class distributions across subsets (`stratify=y`).
- **Clinical Trade-offs (False Negatives vs False Positives)**:
  - In cardiology screening, a **False Negative (FN)** means a patient with coronary artery disease is discharged without necessary intervention, posing life-threatening risks.
  - A **False Positive (FP)** results in secondary follow-up testing (angiogram/stress ECG), causing mild anxiety but preventing mortality.
  - Therefore, **Recall (Sensitivity)** for Class 1 is prioritized alongside overall F1-Score.

---

## 👥 Authors & License
Built with ❤️ for production-grade Machine Learning and clinical decision support. Open-source under the MIT License.
