import os
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Directory setup
os.makedirs("dataset", exist_ok=True)
output_path = os.path.join("dataset", "hdi_dataset.csv")

# Base countries with realistic indicators (approximate recent data)
countries_base = {
    # Very High Development (HDI >= 0.800)
    "Norway": {"LE": 83.2, "MYS": 13.0, "EYS": 18.2, "GNI": 66000},
    "Switzerland": {"LE": 84.0, "MYS": 13.9, "EYS": 16.5, "GNI": 69000},
    "Germany": {"LE": 81.2, "MYS": 14.1, "EYS": 17.0, "GNI": 55000},
    "USA": {"LE": 77.2, "MYS": 13.7, "EYS": 16.3, "GNI": 64000},
    "Japan": {"LE": 84.8, "MYS": 13.4, "EYS": 15.2, "GNI": 42000},
    "United Kingdom": {"LE": 80.7, "MYS": 13.4, "EYS": 17.2, "GNI": 46000},
    "Australia": {"LE": 83.2, "MYS": 12.7, "EYS": 21.0, "GNI": 49000},
    "Singapore": {"LE": 82.8, "MYS": 11.9, "EYS": 16.5, "GNI": 90000},
    
    # High Development (0.700 <= HDI < 0.800)
    "Russia": {"LE": 71.3, "MYS": 12.2, "EYS": 15.8, "GNI": 27000},
    "Brazil": {"LE": 72.8, "MYS": 8.1, "EYS": 15.6, "GNI": 14300},
    "China": {"LE": 78.2, "MYS": 8.1, "EYS": 14.2, "GNI": 17500},
    "Mexico": {"LE": 70.2, "MYS": 9.2, "EYS": 14.9, "GNI": 17800},
    "Turkey": {"LE": 76.0, "MYS": 8.6, "EYS": 18.3, "GNI": 31000},
    "Colombia": {"LE": 72.8, "MYS": 8.9, "EYS": 14.4, "GNI": 14500},
    
    # Medium Development (0.550 <= HDI < 0.700)
    "India": {"LE": 67.2, "MYS": 6.7, "EYS": 11.9, "GNI": 66000/9.5}, # ~6900
    "Egypt": {"LE": 70.2, "MYS": 7.4, "EYS": 13.8, "GNI": 11700},
    "Indonesia": {"LE": 67.6, "MYS": 8.6, "EYS": 13.7, "GNI": 11400},
    "South Africa": {"LE": 62.3, "MYS": 10.2, "EYS": 13.6, "GNI": 12900},
    "Bangladesh": {"LE": 72.4, "MYS": 6.2, "EYS": 12.4, "GNI": 5500},
    "Morocco": {"LE": 74.0, "MYS": 5.9, "EYS": 14.2, "GNI": 7300},
    
    # Low Development (HDI < 0.550)
    "Pakistan": {"LE": 66.1, "MYS": 4.5, "EYS": 8.7, "GNI": 4600},
    "Nigeria": {"LE": 52.7, "MYS": 5.2, "EYS": 9.8, "GNI": 4900},
    "Kenya": {"LE": 61.4, "MYS": 6.7, "EYS": 10.7, "GNI": 4400},
    "Ethiopia": {"LE": 65.0, "MYS": 3.2, "EYS": 9.7, "GNI": 2300},
    "Congo (Dem. Rep.)": {"LE": 59.2, "MYS": 7.0, "EYS": 9.7, "GNI": 1100},
    "Yemen": {"LE": 63.8, "MYS": 3.2, "EYS": 9.1, "GNI": 1500},
    "Niger": {"LE": 61.6, "MYS": 2.1, "EYS": 6.5, "GNI": 1200},
    "Central African Republic": {"LE": 53.9, "MYS": 4.3, "EYS": 8.0, "GNI": 960},
    "Chad": {"LE": 52.5, "MYS": 2.5, "EYS": 7.3, "GNI": 1300},
    "Burundi": {"LE": 61.7, "MYS": 3.1, "EYS": 10.7, "GNI": 700}
}

# Add India correctly
countries_base["India"]["GNI"] = 6900

data_rows = []

# Generate time series for base countries (2000 to 2022) -> 30 countries * 23 years = 690 rows
for country, stats in countries_base.items():
    for year in range(2000, 2023):
        # Calculate year factor to simulate growth over time (2000 has lower values, 2022 has higher)
        year_diff = year - 2022
        growth_factor = 1.0 + (year_diff * 0.005) # ~0.5% growth/decay per year
        
        # Add slight country-year specific random variation
        random_var = np.random.uniform(0.97, 1.03)
        
        le = max(20.0, min(85.0, stats["LE"] * growth_factor * np.random.uniform(0.99, 1.01)))
        mys = max(0.0, min(15.0, stats["MYS"] * growth_factor * random_var))
        eys = max(0.0, min(21.0, stats["EYS"] * growth_factor * random_var))
        gni = max(100.0, min(95000.0, stats["GNI"] * (1.0 + (year_diff * 0.015)) * random_var)) # Income grows slightly faster
        
        # Calculate official UN HDI
        le_index = (le - 20.0) / 65.0
        mys_index = mys / 15.0
        eys_index = eys / 18.0
        education_index = (mys_index + eys_index) / 2.0
        
        # Avoid log(gni <= 100) issues
        gni_clipped = max(101.0, gni)
        income_index = (np.log(gni_clipped) - np.log(100.0)) / (np.log(75000.0) - np.log(100.0))
        
        # Compute geometric mean
        hdi = (le_index * education_index * income_index) ** (1.0 / 3.0)
        hdi = max(0.0, min(1.0, hdi))
        
        # Add a tiny bit of random noise to target to make it realistic for Linear Regression
        hdi_noisy = max(0.0, min(1.0, hdi + np.random.normal(0, 0.005)))
        
        data_rows.append({
            "Country": country,
            "Year": year,
            "Life Expectancy": round(le, 2),
            "Mean Years of Schooling": round(mys, 2),
            "Expected Years of Schooling": round(eys, 2),
            "GNI per Capita": round(gni, 2),
            "HDI Score": round(hdi_noisy, 4)
        })

# Generate 310 additional fully synthetic countries to make it a total of 1000 rows
for i in range(310):
    # Randomly select a developmental tier
    tier = np.random.choice(["Very High", "High", "Medium", "Low"])
    
    if tier == "Very High":
        le = np.random.uniform(76.0, 85.0)
        mys = np.random.uniform(11.0, 14.5)
        eys = np.random.uniform(15.0, 20.0)
        gni = np.random.uniform(30000.0, 85000.0)
    elif tier == "High":
        le = np.random.uniform(70.0, 77.0)
        mys = np.random.uniform(8.0, 11.5)
        eys = np.random.uniform(13.0, 16.5)
        gni = np.random.uniform(12000.0, 31000.0)
    elif tier == "Medium":
        le = np.random.uniform(62.0, 72.0)
        mys = np.random.uniform(5.5, 8.5)
        eys = np.random.uniform(10.5, 13.5)
        gni = np.random.uniform(4000.0, 13000.0)
    else: # Low
        le = np.random.uniform(50.0, 62.0)
        mys = np.random.uniform(1.5, 5.5)
        eys = np.random.uniform(5.0, 10.0)
        gni = np.random.uniform(500.0, 4500.0)
        
    year = np.random.randint(2010, 2023)
    country = f"Country_Sim_{i+1}"
    
    # Calculate UN HDI
    le_index = (le - 20.0) / 65.0
    mys_index = mys / 15.0
    eys_index = eys / 18.0
    education_index = (mys_index + eys_index) / 2.0
    
    gni_clipped = max(101.0, gni)
    income_index = (np.log(gni_clipped) - np.log(100.0)) / (np.log(75000.0) - np.log(100.0))
    
    hdi = (le_index * education_index * income_index) ** (1.0 / 3.0)
    hdi = max(0.0, min(1.0, hdi))
    hdi_noisy = max(0.0, min(1.0, hdi + np.random.normal(0, 0.005)))
    
    data_rows.append({
        "Country": country,
        "Year": year,
        "Life Expectancy": round(le, 2),
        "Mean Years of Schooling": round(mys, 2),
        "Expected Years of Schooling": round(eys, 2),
        "GNI per Capita": round(gni, 2),
        "HDI Score": round(hdi_noisy, 4)
    })

# Convert to DataFrame
df = pd.DataFrame(data_rows)

# Shuffle the dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to CSV
df.to_csv(output_path, index=False)
print(f"Dataset generated successfully at '{output_path}'. Total rows: {len(df)}")
print(df.head())
