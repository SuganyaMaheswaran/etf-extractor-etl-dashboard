# ETF Extractor Dashboard

**ETF Extractor Dashboard** is a Python-based tool that scrapes ETF fund holdings from public websites, transforms the data, and loads it into a SQL Server database. It supports both live scraping and ETL from CSV datasets, with configurable options for scraping, data types, and database mappings.

---

## Features

- Scrape ETF fund holdings and update dates directly from fund websites.
- Convert scraped data into structured Pandas DataFrames.
- Clean and normalize financial data (currency, quantity, percentages, dates).
- Load ETF holdings data into SQL Server efficiently with bulk inserts.
- Avoid duplicate inserts by checking the latest holdings date.
- Fully configurable via `config.json` and `.env` for database connection and ETL options.

---

## File Structure
```
src/
├── config_loader.py # Loads configuration settings and SQL connection strings
├── config.json # JSON configuration for scraping, ETL, database, and type mappings
├── DataScraperService.py # Scrapes ETF fund tables, dates, and available fund links
├── ETLScript.py # ETL script to read CSVs and insert into SQL Server
├── main.py # Main script to scrape and update ETF data automatically
├── PandaService.py # Functions for DataFrame manipulation and type conversion
├── SQLServerService.py # Functions for interacting with SQL Server database
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/ETFExtractorDashboard.git
cd ETFExtractorDashboard
```

Install Python dependencies (recommended in a virtual environment):

```pip install pandas requests beautifulsoup4 pyodbc python-dotenv```

Ensure SQL Server is installed and running. Update your connection settings in .env if necessary.

---
## Configuration

### 1. `config.json`

Controls scraping, ETL, and database behavior:

**etl**

- `csv_dir`: Directory for CSV input files.
- `nan_to_null`: Convert NaN to SQL `NULL`.

**database**

- `table`: Main database table.
- `staging_table`: Optional staging table.
- `use_staging`: Use staging workflow or direct insert.

**mapping**

- `df_to_db`: Maps DataFrame columns to database columns.
- `required_columns`: Columns required in CSV or scraped data.

**types**

- Data type conversions (`currency`, `quantity`, `percentage`, `date`).

**regex**

- Patterns to clean data.

**scrape**

- `funds_start_url`: Starting URL for scraping ETF fund links.
- `fund_list_selector`: CSS selector to identify fund links.
- `holdings_table_selector`: CSS selector to identify holdings table.
- `date_selector`: CSS selector to extract last update date.
- `date_prefix`: Prefix in the string before the date (e.g., `"As of"`).
- `date_format`: Format to parse date strings (`%m/%d/%Y`).

## Usage

### 1. Scrape and Update ETF Data

Run `main.py` to scrape ETF holdings and insert new data into SQL Server:

```bash
python src/main.py
```

This will:

- Read fund URLs from config.json.
- Check if the latest holdings date already exists in SQL Server.
- Convert the holdings table into a DataFrame, clean the data, and insert new records.
- Skip insertion if no new data is available.

### 2. ETL from CSV Files

Load existing ETF datasets from CSV files into SQL Server:

```bash
python src/ETLScript.py <directory_path_with_csv_files>
```
Example:
```bash
python src/ETLScript.py "C:\Users\smahe\Documents\DataSets\ETF_UDatasets"
```

This will:

- Read all CSV files in the specified directory.
- Clean and normalize the data.
- Convert data types (currency, quantity, percentage, date).
- Insert the cleaned records into the SQL Server database.

## Database Structure
<table style="width:100%; text-align:left;">
  <thead>
    <tr>
      <th style="width:70%;">Column Name</th>
      <th style="width:30%;">Data Type</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>security_str</td><td>varchar</td></tr>
    <tr><td>market_val_int</td><td>float</td></tr>
    <tr><td>symbol_str</td><td>varchar</td></tr>
    <tr><td>sedol_str</td><td>varchar</td></tr>
    <tr><td>quantity_int</td><td>float</td></tr>
    <tr><td>weight_float</td><td>float</td></tr>
    <tr><td>etf_str</td><td>varchar</td></tr>
    <tr><td>update_dt</td><td>date</td></tr>
  </tbody>
</table>

The `get_date(etf)` function retrieves the most recent update date for a given ETF to prevent duplicate inserts.

## Dependencies
- Python 3.10+
- pandas
- requests
- beautifulsoup4
- pyodbc