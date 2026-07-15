import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import joblib

# Setup directories
os.makedirs("model", exist_ok=True)
os.makedirs(os.path.join("static", "plots"), exist_ok=True)

# 1. Load Dataset
dataset_path = os.path.join("dataset", "hdi_dataset.csv")
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"Dataset not found at {dataset_path}. Run generate_dataset.py first.")

df = pd.read_csv(dataset_path)
print("Dataset Loaded Successfully!")
print(f"Dataset Shape: {df.shape}")

# 2. Data Understanding and Cleaning
# Display basic information
print("\n--- Dataset Info ---")
print(df.info())

print("\n--- Missing Values ---")
print(df.isnull().sum())

# Drop duplicates if any
initial_rows = len(df)
df = df.drop_duplicates()
print(f"\nRemoved {initial_rows - len(df)} duplicate rows.")

# Fill numerical missing values if any (using median)
for col in ["Life Expectancy", "Mean Years of Schooling", "Expected Years of Schooling", "GNI per Capita"]:
    if col in df.columns:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"Filled missing values in '{col}' with median: {median_val}")

# 3. Exploratory Data Analysis & Visualization
print("\nGenerating and saving plots to static/plots/...")

# Plot 1: HDI Score Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["HDI Score"], kde=True, color="teal")
plt.title("Distribution of Human Development Index (HDI) Score")
plt.xlabel("HDI Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join("static", "plots", "hdi_distribution.png"))
plt.close()

# Plot 2: Correlation Heatmap
plt.figure(figsize=(8, 6))
numerical_cols = ["Life Expectancy", "Mean Years of Schooling", "Expected Years of Schooling", "GNI per Capita", "HDI Score"]
corr_matrix = df[numerical_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".3f", linewidths=0.5)
plt.title("Correlation Matrix of HDI Indicators")
plt.tight_layout()
plt.savefig(os.path.join("static", "plots", "correlation_heatmap.png"))
plt.close()

# Plot 3: Feature Relationships (Life Expectancy vs HDI Score)
plt.figure(figsize=(8, 5))
sns.scatterplot(x="Life Expectancy", y="HDI Score", data=df, alpha=0.6, color="coral")
plt.title("Life Expectancy vs HDI Score")
plt.xlabel("Life Expectancy (Years)")
plt.ylabel("HDI Score")
plt.tight_layout()
plt.savefig(os.path.join("static", "plots", "life_expectancy_vs_hdi.png"))
plt.close()

# Plot 4: Schooling Indicators vs HDI Score
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.scatterplot(x="Mean Years of Schooling", y="HDI Score", data=df, alpha=0.6, color="purple", ax=axes[0])
axes[0].set_title("Mean Years of Schooling vs HDI Score")
axes[0].set_xlabel("Mean Years of Schooling (Years)")
axes[0].set_ylabel("HDI Score")

sns.scatterplot(x="Expected Years of Schooling", y="HDI Score", data=df, alpha=0.6, color="magenta", ax=axes[1])
axes[1].set_title("Expected Years of Schooling vs HDI Score")
axes[1].set_xlabel("Expected Years of Schooling (Years)")
axes[1].set_ylabel("HDI Score")
plt.tight_layout()
plt.savefig(os.path.join("static", "plots", "schooling_vs_hdi.png"))
plt.close()

# Plot 5: GNI per Capita vs HDI Score (Log scale on X is natural for GNI)
plt.figure(figsize=(8, 5))
sns.scatterplot(x="GNI per Capita", y="HDI Score", data=df, alpha=0.6, color="forestgreen")
plt.xscale("log")
plt.title("GNI per Capita (Log Scale) vs HDI Score")
plt.xlabel("GNI per Capita (constant 2017 PPP $)")
plt.ylabel("HDI Score")
plt.tight_layout()
plt.savefig(os.path.join("static", "plots", "gni_vs_hdi.png"))
plt.close()

# Plot 6: HDI Category Distribution
def classify_hdi(score):
    if score >= 0.800:
        return "Very High"
    elif score >= 0.700:
        return "High"
    elif score >= 0.550:
        return "Medium"
    else:
        return "Low"

df["HDI Category"] = df["HDI Score"].apply(classify_hdi)
plt.figure(figsize=(8, 5))
category_order = ["Very High", "High", "Medium", "Low"]
sns.countplot(x="HDI Category", data=df, order=category_order, hue="HDI Category", palette="viridis", legend=False)
plt.title("Distribution of Countries by HDI Category")
plt.xlabel("HDI Category")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig(os.path.join("static", "plots", "hdi_category_distribution.png"))
plt.close()

print("Plots generated and saved successfully!")

# 4. Feature and Target Selection
X = df[["Life Expectancy", "Mean Years of Schooling", "Expected Years of Schooling", "GNI per Capita"]]
y = df["HDI Score"]

# 5. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nTrain set size: {X_train.shape[0]} rows")
print(f"Test set size: {X_test.shape[0]} rows")

# 6. Apply Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
scaler_path = os.path.join("model", "scaler.pkl")
joblib.dump(scaler, scaler_path)
print(f"Scaler saved at: {scaler_path}")

# 7. Model Training
model = LinearRegression()
model.fit(X_train_scaled, y_train)
print("Linear Regression Model Trained successfully!")

# 8. Model Evaluation
y_pred = model.predict(X_test_scaled)

r2 = metrics.r2_score(y_test, y_pred)
mae = metrics.mean_absolute_error(y_test, y_pred)
mse = metrics.mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print("\n=== Model Evaluation Metrics (Test Set) ===")
print(f"R² Score (Coefficient of Determination): {r2:.6f}")
print(f"Mean Absolute Error (MAE):              {mae:.6f}")
print(f"Mean Squared Error (MSE):               {mse:.6f}")
print(f"Root Mean Squared Error (RMSE):         {rmse:.6f}")

print("\nModel Coefficients:")
for col, coef in zip(X.columns, model.coef_):
    print(f"  {col}: {coef:.6f}")
print(f"  Intercept: {model.intercept_:.6f}")

# 9. Save Model
model_path = os.path.join("model", "model.pkl")
joblib.dump(model, model_path)
print(f"Model saved at: {model_path}")
print("Machine learning pipeline completed successfully!")
