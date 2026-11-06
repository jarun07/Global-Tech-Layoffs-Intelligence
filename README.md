# Global Tech Layoffs & AI Impact Intelligence Platform (2020–2026)

## 📌 Project Overview
An end-to-end data engineering and analytics project investigating global technology layoffs and the relationship between AI adoption and workforce reductions. This project demonstrates the complete data lifecycle: from raw data ingestion to a cloud-based data warehouse and interactive business intelligence reporting.

## 📸 Dashboard Screenshots

### 1. Executive Summary
![Executive Summary](Executive%20Summary.png)

### 2. Geography & Industry
![Geography and Industry](Geography%20and%20Industry.png)

### 3. AI Impact Deep Dive
![AI Impact](AI%20Impact.png)

## 🏗️ Architecture & Pipeline
1. **Data Ingestion:** Combined 3 distinct raw datasets (OWID Layoffs, AI Layoffs Tracker, AI Layoffs Register).
2. **ETL (Python):** Cleaned, standardized, and deduplicated records using `pandas`.
3. **Data Warehousing:** Designed a **Star Schema** (Fact & Dimension tables) and deployed it to a cloud **PostgreSQL** database (Neon) using `SQLAlchemy`.
4. **Business Intelligence:** Connected Power BI to the cloud database to build a 3-page interactive dashboard.

## 🛠️ Technology Stack
- **Programming:** Python (Pandas, SQLAlchemy, Psycopg2)
- **Database:** PostgreSQL (Neon Cloud)
- **Analytics:** SQL
- **Visualization:** Power BI

## 📊 Dashboard Highlights
- **Executive Summary:** KPIs tracking 544K+ employees laid off, top 10 companies, and overall AI attribution rates.
- **Geography & Industry:** Treemaps and maps identifying which countries and industries were hit hardest.
- **AI Impact Deep Dive:** Analysis of AI-specific mechanisms, evidence tiers, and year-over-year trends.

## 📂 Repository Structure
- `.gitignore` - Prevents sensitive credentials and large datasets from being uploaded.
- `star_schema.py` - Python script to build the Fact and Dimension tables from consolidated data.
- `load_neon.py` - Python script to create tables in Neon PostgreSQL and load the data.
- `check_db.py` - SQL validation script proving the data is live in the cloud.
- `test_neon.py` - Database connection and DDL testing.

## 🔒 Data Quality & Governance
- Deduplication rules applied to prevent double-counting layoff events across multiple news sources.
- Explicit AI attribution tracked using a strict evidence tier system (Tier 1: Official filings, Tier 3: Soft reporting).
- Missing data preserved safely rather than artificially imputed.
