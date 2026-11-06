import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT = Path(__file__).resolve().parent
load_dotenv(PROJECT / ".env")

# Connect
CONN = (
    f"postgresql+psycopg2://{os.environ['NEON_USER']}:{os.environ['NEON_PASSWORD']}"
    f"@{os.environ['NEON_HOST']}/{os.environ['NEON_DB']}?sslmode={os.environ['NEON_SSLMODE']}"
)
engine = create_engine(CONN)
DATA_DIR = PROJECT / "data" / "warehouse"

print("Connecting to Neon and creating tables...")

with engine.begin() as conn:
    # Drop tables if they exist (to allow safe re-runs)
    conn.execute(text("DROP TABLE IF EXISTS fact_layoffs CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS dim_company CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS dim_location CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS dim_date CASCADE;"))

    # Create Dimensions
    conn.execute(text("""
        CREATE TABLE dim_company (
            company_id INT PRIMARY KEY,
            company VARCHAR(255),
            industry_category VARCHAR(255),
            industry_detail VARCHAR(255)
        );
    """))
    
    conn.execute(text("""
        CREATE TABLE dim_location (
            location_id INT PRIMARY KEY,
            country VARCHAR(255),
            location VARCHAR(255)
        );
    """))
    
    conn.execute(text("""
        CREATE TABLE dim_date (
            date_id INT PRIMARY KEY,
            full_date DATE,
            year INT,
            quarter INT,
            month INT,
            month_name VARCHAR(50),
            day_of_week VARCHAR(50)
        );
    """))

    # Create Fact Table with Foreign Keys
    conn.execute(text("""
        CREATE TABLE fact_layoffs (
            event_id VARCHAR(255) PRIMARY KEY,
            date_id INT REFERENCES dim_date(date_id),
            company_id INT REFERENCES dim_company(company_id),
            location_id INT REFERENCES dim_location(location_id),
            employees_affected NUMERIC,
            ai_attribution_level VARCHAR(50),
            evidence_tier VARCHAR(50),
            source_dataset VARCHAR(100)
        );
    """))

print("Tables created. Loading data...")

# Load CSVs
dim_company = pd.read_csv(DATA_DIR / "dim_company.csv")
dim_location = pd.read_csv(DATA_DIR / "dim_location.csv")
dim_date = pd.read_csv(DATA_DIR / "dim_date.csv")
fact_layoffs = pd.read_csv(DATA_DIR / "fact_layoffs.csv")

# Push to Neon
dim_company.to_sql("dim_company", engine, if_exists="append", index=False)
dim_location.to_sql("dim_location", engine, if_exists="append", index=False)
dim_date.to_sql("dim_date", engine, if_exists="append", index=False)
fact_layoffs.to_sql("fact_layoffs", engine, if_exists="append", index=False)

print("Data loaded successfully into Neon!")

# Validation
with engine.connect() as conn:
    print("\n--- Row Counts in Database ---")
    for table in ["dim_company", "dim_location", "dim_date", "fact_layoffs"]:
        res = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
        print(f"{table}: {res} rows")