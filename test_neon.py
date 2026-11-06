import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT = Path(__file__).resolve().parent
load_dotenv(PROJECT / ".env")

required = ["NEON_HOST", "NEON_DB", "NEON_USER", "NEON_PASSWORD", "NEON_SSLMODE"]
missing = [k for k in required if not os.environ.get(k)]
if missing:
    raise SystemExit(f"Missing in .env: {missing}")

CONN = (
    f"postgresql+psycopg2://{os.environ['NEON_USER']}:{os.environ['NEON_PASSWORD']}"
    f"@{os.environ['NEON_HOST']}/{os.environ['NEON_DB']}"
    f"?sslmode={os.environ['NEON_SSLMODE']}"
)
engine = create_engine(CONN)

with engine.connect() as conn:
    print("Version:", conn.execute(text("SELECT version();")).scalar())
    print("DB/User:", conn.execute(text("SELECT current_database(), current_user;")).fetchone())

    conn.execute(text("CREATE TABLE IF NOT EXISTS _probe (id INT);"))
    conn.execute(text("DROP TABLE _probe;"))
    conn.commit()
    print("DDL works.")