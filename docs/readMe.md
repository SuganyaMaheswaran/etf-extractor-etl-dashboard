# ETF Holdings Data Pipeline

A Python-based data pipeline that scrapes ETF fund holdings from the Sprott website, transforms the data, and loads it into SQL Server.

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Development Backlog](#development-backlog)
- [Testing](#testing)

## Project Overview

This project automates the collection and storage of ETF holdings data. It scrapes real-time holdings information from the Sprott ETF website, performs data transformation, and stores the results in a SQL Server database. The pipeline includes intelligent date-checking to avoid duplicate data insertions.

**Tech Stack:**
- Python 3.x
- Pandas (data transformation)
- BeautifulSoup (web scraping)
- Requests (HTTP client)
- PyODBC (SQL Server connectivity)

## Architecture

### Data Flow

```
get_funds() 
    ↓
[List of ETF URLs]
    ↓
scrapeETF() for each ETF
    ↓
scrape_table() + scrape_date()
    ↓
Data Transformation (PandaService)
    ↓
Date Check (Is this newer than DB?)
    ↓
insert_into_table() 
    ↓
SQL Server
```

### Module Breakdown

| Module | Responsibility |
|--------|-----------------|
| `main.py` | Entry point - orchestrates the scraping pipeline |
| `DataScraperService.py` | Web scraping layer - extracts data from HTML |
| `ScrapeETF.py` | Business logic - orchestrates scraping and date checking |
| `PandaService.py` | Data transformation - converts HTML to DataFrames, type conversions |
| `SQLServerService.py` | Database layer - bulk inserts and queries |
| `ETLScript.py` | Batch processing utility - loads CSV files to SQL Server |

## Features

- **Automated Web Scraping**: Extracts ETF holdings tables and dates from Sprott website
- **Smart Date Checking**: Only inserts new data if update date differs from database
- **Bulk Insert Optimization**: Uses `fast_executemany` for efficient database writes
- **Type Conversion**: Automatically converts currency, quantities, percentages, and dates
- **Error Handling**: Database transactions with rollback on failure
- **CSV Batch Processing**: Separate ETL script for loading historical CSV data

## Setup

### Prerequisites
- Python 3.7+
- SQL Server (Express or higher)
- Access to SQL Server database named `ETFHoldings`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd etf-pipeline
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up SQL Server database**
   - Create database `ETFHoldings`
   - Create `Holdings` table with schema matching `SQLServerService.py`
   - Create stored procedure `GetLastUpdateDate`

### Environment Variables

Create a `.env` file:
```
DB_DRIVER=SQL Server
DB_SERVER=.\SQLEXPRESS
DB_DATABASE=ETFHoldings
DB_TRUSTED_CONNECTION=yes
CSV_DATA_PATH=C:\Users\YourUsername\Documents\DataSets\ETF_UDatasets\
LOG_LEVEL=INFO
```

## Usage

### Run ETF Scraping Pipeline

```bash
python main.py
```

This will:
1. Fetch list of ETFs from Sprott website
2. Scrape holdings for each ETF
3. Check if data is newer than what's in the database
4. Insert only new records into SQL Server

### Run Batch CSV Processing

```bash
python ETLScript.py /path/to/csv/directory
```

### Run Specific ETF Scrape

```python
from ScrapeETF import scrapeETF
scrapeETF("https://sprottetfs.com/urnm-sprott-uranium-miners-etf", "URNM")
```

## Development Backlog

### Infrastructure & Setup
- [ ] Create `requirements.txt` with all project dependencies
- [ ] Create `.gitignore` for Python project
- [ ] Create `.env.example` template file for configuration variables

### Code Quality & Refactoring
- [ ] Extract hardcoded paths and database connection string to environment variables
- [ ] Add logging module setup and replace all `print()` statements with proper logging
- [ ] Refactor exception handling - replace bare `except:` clauses with specific exceptions
- [ ] Add docstrings to all functions (Google or NumPy style)
- [ ] Remove unused `divClass` parameter from scraping functions

### Code Cleanup
- [ ] Delete or repurpose the empty `scrapePhysicalETF.py` file

### Testing
- [ ] Add unit tests for `PandaService.py` (data type conversion, column addition)
- [ ] Add unit tests for `DataScraperService.py` (mocking HTTP requests)
- [ ] Add unit tests for `SQLServerService.py` (mocking database connections)
- [ ] Add integration test for `ScrapeETF.py` workflow
- [ ] Create pytest configuration (`pytest.ini` or `pyproject.toml`)

### Documentation & CI/CD
- [ ] Document SQL Server schema and stored procedures
- [ ] Add GitHub Actions workflow for CI/CD
- [ ] Create deployment guide

## Testing

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=.
```

### Run Specific Test File

```bash
pytest tests/test_panda_service.py
```

### Test Categories

| Module | Tests |
|--------|-------|
| `test_panda_service.py` | Data type conversions, DataFrame operations |
| `test_data_scraper_service.py` | Web scraping (mocked requests) |
| `test_sql_server_service.py` | Database operations (mocked connections) |
| `test_scrape_etf.py` | Integration tests for full workflow |

## Known Issues

- Hardcoded file paths in `ETLScript.py`
- Bare exception handlers need specific error types
- No logging in place yet (using `print()`)
- Missing docstrings on functions
- Unused parameter in scraping functions

## Future Improvements

- Add retry logic for failed scrapes (exponential backoff)
- Implement data validation before database insertion
- Add monitoring/alerting for pipeline failures
- Create dashboard for viewing ETF holdings
- Add support for other ETF providers
- Implement incremental scraping (only changed holdings)

## Contributing

Before contributing, please:
1. Create a feature branch
2. Add tests for new functionality
3. Run `pytest` to ensure tests pass
4. Follow PEP 8 style guidelines
5. Add docstrings to all functions

<!-- ## License -->


## Contact

Created by: Suganya Maheswaran
