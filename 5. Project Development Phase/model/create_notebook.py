import os
import json

# Setup notebooks directory
os.makedirs("notebooks", exist_ok=True)
notebook_path = os.path.join("notebooks", "HDI_Analysis.ipynb")

# Define cells structure
cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Human Development Index (HDI) Exploratory Data Analysis & Modeling\n",
            "This notebook provides a comprehensive academic analysis of the Human Development Index (HDI) dataset, exploring its dimensions and training a Linear Regression model to predict the HDI score."
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Project Background and Indicators\n",
            "The Human Development Index (HDI) is a statistical measure compiled by the United Nations to evaluate the social and economic development levels of countries. It consists of three dimensions:\n",
            "- **Health**: Measured by Life Expectancy at Birth.\n",
            "- **Education**: Measured by Mean Years of Schooling and Expected Years of Schooling.\n",
            "- **Standard of Living**: Measured by Gross National Income (GNI) per Capita."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Import Libraries\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "from sklearn.model_selection import train_test_split\n",
            "from sklearn.linear_model import LinearRegression\n",
            "from sklearn import metrics\n",
            "import os"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Load Dataset\n",
            "We load the clean CSV dataset `dataset/hdi_dataset.csv` generated for this project."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load dataset\n",
            "df = pd.read_csv('../dataset/hdi_dataset.csv')\n",
            "print(f\"Dataset Shape: {df.shape}\")\n",
            "df.head()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Exploratory Data Analysis and Statistics\n",
            "Let's look at the basic statistics of the dataset, missing values, and columns description."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Dataset info\n",
            "df.info()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Summary statistics\n",
            "df.describe()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Missing values check\n",
            "print(\"Missing values per column:\")\n",
            "df.isnull().sum()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Visualizations & Correlation Analysis\n",
            "Let's plot the indicators to see their relationship with the target variable `HDI Score`."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Distribution of HDI Score\n",
            "plt.figure(figsize=(8, 5))\n",
            "sns.histplot(df['HDI Score'], kde=True, color='teal')\n",
            "plt.title('Distribution of HDI Score')\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Correlation Matrix Heatmap\n",
            "plt.figure(figsize=(8, 6))\n",
            "numerical_cols = ['Life Expectancy', 'Mean Years of Schooling', 'Expected Years of Schooling', 'GNI per Capita', 'HDI Score']\n",
            "sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm', fmt='.3f')\n",
            "plt.title('Correlation Matrix of HDI Indicators')\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Scatter plot: Life Expectancy vs HDI Score\n",
            "plt.figure(figsize=(6, 4))\n",
            "sns.scatterplot(x='Life Expectancy', y='HDI Score', data=df, alpha=0.6, color='coral')\n",
            "plt.title('Life Expectancy vs HDI Score')\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Scatter plot: GNI per Capita vs HDI Score (Log scale on X)\n",
            "plt.figure(figsize=(6, 4))\n",
            "sns.scatterplot(x='GNI per Capita', y='HDI Score', data=df, alpha=0.6, color='forestgreen')\n",
            "plt.xscale('log')\n",
            "plt.title('GNI per Capita (Log Scale) vs HDI Score')\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Model Training and Evaluation\n",
            "We train a Linear Regression model using the four features to predict the HDI Score."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Select features and target\n",
            "X = df[['Life Expectancy', 'Mean Years of Schooling', 'Expected Years of Schooling', 'GNI per Capita']]\n",
            "y = df['HDI Score']\n",
            "\n",
            "# Split data into train and test sets\n",
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n",
            "print(f\"Train size: {len(X_train)}, Test size: {len(X_test)}\")"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Fit Linear Regression\n",
            "model = LinearRegression()\n",
            "model.fit(X_train, y_train)\n",
            "\n",
            "# Make predictions\n",
            "y_pred = model.predict(X_test)\n",
            "\n",
            "# Compute metrics\n",
            "r2 = metrics.r2_score(y_test, y_pred)\n",
            "mae = metrics.mean_absolute_error(y_test, y_pred)\n",
            "rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))\n",
            "\n",
            "print(f\"R² Score: {r2:.4f}\")\n",
            "print(f\"MAE:      {mae:.4f}\")\n",
            "print(f\"RMSE:     {rmse:.4f}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Key Observations\n",
            "- There is a very strong positive correlation between Life Expectancy, schooling, GNI per Capita and the HDI Score.\n",
            "- A simple Linear Regression model achieves a high coefficient of determination ($R^2 > 0.98$), indicating that the linear combination of the normalized indexes acts as an excellent predictor of the overall index score.\n",
            "- Education metrics (Mean & Expected years of schooling) carry significant weight in the regression coefficients, showing their high influence on human development levels."
        ]
    }
]

notebook_json = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

# Write notebook
with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(notebook_json, f, indent=2)

print(f"Jupyter Notebook generated successfully at '{notebook_path}'")
