import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT = Path(__file__).resolve().parent
load_dotenv(PROJECT / ".env")

CONN = f"postgresql+psycopg2://{os.environ['NEON_USER']}:{os.environ['NEON_PASSWORD']}@{os.environ['NEON_HOST']}/{os.environ['NEON_DB']}?sslmode={os.environ['NEON_SSLMODE']}"
engine = create_engine(CONN)

with engine.connect() as conn:
    # Filter out the nulls BEFORE calculating the sum
    query = text("""
        SELECT c.company, SUM(f.employees_affected) as total_laid_off
        FROM fact_layoffs f
        JOIN dim_company c ON f.company_id = c.company_id
        WHERE f.employees_affected IS NOT NULL
        GROUP BY c.company
        ORDER BY total_laid_off DESC
        LIMIT 3;
    """)
    results = conn.execute(query).fetchall()
    print("Top 3 Companies by Layoffs in Neon:")
    for row in results:
        # This time, we know for a fact it won't be None because of the WHERE clause
        print(f"{row[0]}: {row[1]:,.0f}")