
import pandas as pd
from sqlalchemy import create_engine

# 1. INGESTION - Read raw CSV data
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"

print("Starting Data Pipeline...")

df = pd.read_csv(url)

print("\nRaw Data:")
print(df.head())

# 2. INTEGRATION - Clean and transform data

# Add a date column for demonstration
df["order_date"] = pd.date_range(
    start="2026-01-01", periods=len(df), freq="D"
)

# Introduce missing values for cleaning demonstration
df.loc[0, "total_bill"] = None
df.loc[1, "tip"] = None

# Fill missing numeric values with column averages
df["total_bill"] = df["total_bill"].fillna(df["total_bill"].mean())
df["tip"] = df["tip"].fillna(df["tip"].mean())

# Standardize date format
df["order_date"] = pd.to_datetime(
    df["order_date"]
).dt.strftime("%Y-%m-%d")

print("\nCleaned Data:")
print(df.head())

# 3. PRESENTATION - Load data into SQLite
engine = create_engine("sqlite:///pipeline_data.db")

df.to_sql(
    "cleaned_orders",
    con=engine,
    if_exists="replace",
    index=False
)

print("\nData successfully loaded into SQLite database!")
print("Total rows inserted:", len(df))
print("Pipeline completed successfully!")
