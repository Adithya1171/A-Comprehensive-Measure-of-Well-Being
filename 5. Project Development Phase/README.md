# Human Development Index (HDI) Predictor

An end-to-end, machine-learning-driven web application to predict and analyze the Human Development Index (HDI) of countries based on major socio-economic development indicators.

---

## 1. Project Overview

The Human Development Index (HDI) Predictor is a Flask-based web application integrated with a Linear Regression machine learning model. It calculates the HDI score of a country and classifies it into one of four development tiers:

1. **Very High Human Development** ($\text{HDI} \ge 0.800$)
2. **High Human Development** ($0.700 \le \text{HDI} < 0.800$)
3. **Medium Human Development** ($0.550 \le \text{HDI} < 0.700$)
4. **Low Human Development** ($\text{HDI} < 0.550$)

---

## 2. Project Purpose

The Human Development Index is a composite statistic summarizing health, knowledge, and standards of living. This application serves as a policymaking simulator and educational tool, helping researchers, students, and analysts understand how shifts in individual developmental indicators influence a nation's overall classification.

---

## 3. Technology Stack

* **Backend Framework:** Python 3.x, Flask
* **Machine Learning & Data Science:** Scikit-learn, Pandas, NumPy, Joblib
* **Data Visualization:** Matplotlib, Seaborn
* **Database Management:** SQLite3 (parameterized SQL queries, password hashing via Werkzeug)
* **Frontend UI/UX:** HTML5, CSS3, JavaScript, Bootstrap 5 (dark mode theme with glassmorphic cards)

---

## 4. Project Directory Layout

```
HDI_Predictor/
├── app/
│   ├── __init__.py          # Flask Application Factory
│   ├── predict.py           # Model predictor helper
│   ├── routes.py            # Route controllers & Blueprint definitions
│   └── utils.py             # SQLite helper and authentication operations
├── dataset/
│   └── hdi_dataset.csv      # Unified tidy country indicators dataset
├── model/
│   ├── train_model.py       # ML Pipeline (EDA, training, evaluation, plot savings)
│   ├── model.pkl            # Serialized Linear Regression model
│   └── scaler.pkl           # Serialized StandardScaler
├── notebooks/
│   └── HDI_Analysis.ipynb   # Jupyter Notebook containing academic EDA
├── static/
│   ├── css/
│   │   └── style.css        # Premium custom Glassmorphism style sheet
│   ├── js/
│   │   └── script.js        # Client-side form validation and interactive JS
│   └── plots/               # Pre-computed visualization charts
│       ├── correlation_heatmap.png
│       ├── gni_vs_hdi.png
│       ├── hdi_category_distribution.png
│       ├── hdi_distribution.png
│       ├── life_expectancy_vs_hdi.png
│       └── schooling_vs_hdi.png
├── templates/
│   ├── base.html            # Parent responsive layout structure
│   ├── index.html           # Home landing page
│   ├── login.html           # Secure login card form
│   ├── register.html        # Registration card form
│   ├── dashboard.html       # Dynamic metrics dashboard
│   ├── predict.html         # Four-indicator prediction form
│   ├── result.html          # Glowing score index output page
│   ├── history.html         # User simulation logs table
│   └── about.html           # Scientific about details and EDA plots
├── tests/
│   └── test_app.py          # Automated unit test suite
├── app.py                   # Main application entry point runner
├── requirements.txt         # Project package dependencies
├── README.md                # System documentation
└── .gitignore               # Ignored versioning files
```

---

## 5. Machine Learning Pipeline

1. **Dataset Generation:** Sourced and expanded with realistic country records from the UNDP HDR database over 22 years (1000 rows).
2. **Exploratory Data Analysis (EDA):** Custom scripts output correlation matrices, histograms, and scatter plots to `static/plots/`.
3. **Data Splitting:** 80% Training set, 20% Test set.
4. **Feature Scaling:** `StandardScaler` fitted only on training data and stored as `model/scaler.pkl` to prevent data leakage.
5. **Model Training:** Linear Regression algorithm fit on the scaled parameters.
6. **Model Evaluation (Test Set Results):**
   * **$R^2$ Score (Coefficient of Determination):** $\approx 0.987$
   * **Mean Absolute Error (MAE):** $\approx 0.017$
   * **Root Mean Squared Error (RMSE):** $\approx 0.021$

---

## 6. How to Install and Run (Windows)

Follow these simple steps in your Command Prompt, PowerShell, or VS Code terminal:

### Step 1: Clone or Open the Project Folder
Ensure you are inside the `HDI_Predictor` root directory:
```powershell
cd HDI_Predictor
```

### Step 2: Initialize & Activate Virtual Environment (Recommended)
Create a clean virtual environment and activate it:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Train the Machine Learning Model
Run the pipeline to prepare serialized files and render static EDA graphs:
```powershell
python model/train_model.py
```

### Step 5: Start the Flask Application
```powershell
python app.py
```

### Step 6: Open the Browser
Once the server is running, navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 7. Development Indicators Ranges

When utilizing the **Predict HDI** interface, inputs must comply with the following boundaries:
* **Life Expectancy:** $20.0$ to $100.0$ years.
* **Mean Years of Schooling:** $0.0$ to $20.0$ years.
* **Expected Years of Schooling:** $0.0$ to $25.0$ years.
* **GNI per Capita:** Positive numerical value ($> \$0.00$).
