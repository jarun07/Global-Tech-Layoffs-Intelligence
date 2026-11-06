import os
import pandas as pd

PROJECT = r"C:\Users\hotsp\OneDrive\Desktop\GLOBAL_WORKFORCE_INTELLIGENCE"
INPUT_FILE = os.path.join(PROJECT, "data", "consolidated", "parquet", "consolidated_layoffs.parquet")
OUT_DIR = os.path.join(PROJECT, "data", "warehouse")
os.makedirs(OUT_DIR, exist_ok=True)

print("Loading consolidated data...")
df = pd.read_parquet(INPUT_FILE)

# 1. DIM DATE
print("Building dim_date...")
# Get min and max dates, drop missing dates
dates = pd.to_datetime(df["event_date"]).dropna()
min_date, max_date = dates.min(), dates.max()
date_range = pd.date_range(start=min_date, end=max_date, freq='D')

dim_date = pd.DataFrame({"full_date": date_range})
dim_date["date_id"] = dim_date["full_date"].dt.strftime("%Y%m%d").astype(int)
dim_date["year"] = dim_date["full_date"].dt.year
dim_date["quarter"] = dim_date["full_date"].dt.quarter
dim_date["month"] = dim_date["full_date"].dt.month
dim_date["month_name"] = dim_date["full_date"].dt.strftime("%B")
dim_date["day_of_week"] = dim_date["full_date"].dt.strftime("%A")

# 2. DIM COMPANY
print("Building dim_company...")
companies = df[["company", "industry_category", "industry_detail"]].drop_duplicates(subset=["company"]).reset_index(drop=True)
companies["company_id"] = companies.index + 1
dim_company = companies[["company_id", "company", "industry_category", "industry_detail"]]

# 3. DIM LOCATION
print("Building dim_location...")
locations = df[["country", "location"]].drop_duplicates().reset_index(drop=True)
locations["location_id"] = locations.index + 1
dim_location = locations[["location_id", "country", "location"]]

# 4. FACT LAYOFFS
print("Building fact_layoffs...")
fact = df.copy()

# --- THE FIX: Drop rows with missing dates before processing ---
fact = fact.dropna(subset=["event_date"]).copy()

# Convert dates to the integer ID (No more fillna(0) needed)
fact["date_id"] = pd.to_datetime(fact["event_date"]).dt.strftime("%Y%m%d").astype(int)

# Map IDs
fact = fact.merge(companies[["company", "company_id"]], on="company", how="left")
fact = fact.merge(locations[["country", "location", "location_id"]], on=["country", "location"], how="left")

# Select final fact columns
fact_layoffs = fact[[
    "event_id", "date_id", "company_id", "location_id",
    "employees_affected", "ai_attribution_level", "evidence_tier", "source_dataset"
]]

# Save all to CSV for the DB loader
dim_date.to_csv(os.path.join(OUT_DIR, "dim_date.csv"), index=False)
dim_company.to_csv(os.path.join(OUT_DIR, "dim_company.csv"), index=False)
dim_location.to_csv(os.path.join(OUT_DIR, "dim_location.csv"), index=False)
fact_layoffs.to_csv(os.path.join(OUT_DIR, "fact_layoffs.csv"), index=False)

print(f"Star Schema built successfully!")
print(f"dim_company: {len(dim_company)} rows")
print(f"dim_location: {len(dim_location)} rows")
print(f"dim_date: {len(dim_date)} rows")
print(f"fact_layoffs: {len(fact_layoffs)} rows")