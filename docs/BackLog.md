# Development Backlog

**Last Updated:** 2024
**Status:** In Progress
**Total Tasks:** 16 | **Completed:** 0 | **In Progress:** 0 | **Pending:** 16

---

## Table of Contents
1. [Infrastructure & Setup (3 tasks)](#infrastructure--setup) ✅ DONE
2. [Code Quality & Refactoring (5 tasks)](#code-quality--refactoring)
3. [Code Cleanup (1 task)](#code-cleanup)
4. [Testing (5 tasks)](#testing)
5. [Documentation & CI/CD (2 tasks)](#documentation--cicd)
6. [Acceptance Criteria Summary](#acceptance-criteria-summary)

---

## Infrastructure & Setup

### Task 1: Create requirements.txt
**Status:** Pending  
**Priority:** High  
**Effort:** 0.5 hours  
**Assignee:** TBD

**Description:**
Generate a `requirements.txt` file that lists all Python package dependencies with pinned versions.

**Acceptance Criteria:**
- [ ] File `requirements.txt` exists in project root
- [ ] All imported packages are listed with version numbers:
  - pandas (version needed)
  - requests (version needed)
  - beautifulsoup4 (version needed)
  - pyodbc (version needed)
  - python-dotenv (for .env support)
- [ ] File can be used to install dependencies: `pip install -r requirements.txt`
- [ ] Virtual environment can be created and all packages installed without errors

**Commands to generate:**
```bash
pip freeze > requirements.txt
# Manual review to remove unnecessary packages
```

**Related Files:**
- `requirements.txt` (new)

---

### Task 2: Create .gitignore for Python project
**Status:** Pending  
**Priority:** High  
**Effort:** 0.5 hours  
**Assignee:** TBD

**Description:**
Create a `.gitignore` file to prevent committing sensitive files and directories.

**Acceptance Criteria:**
- [ ] File `.gitignore` exists in project root
- [ ] `.env` and `.env.local` files are ignored
- [ ] Virtual environment directory (`venv/`) is ignored
- [ ] Python cache directories (`__pycache__/`, `*.pyc`, `*.pyo`) are ignored
- [ ] IDE directories (`.vscode/`, `.idea/`) are ignored
- [ ] Test coverage reports (`.coverage`, `htmlcov/`) are ignored
- [ ] Logs directory is ignored (if applicable)
- [ ] Database backups or data files are ignored

**Content Template:**
```
# Environment variables
.env
.env.local
.env.*.local

# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs/
*.log
```

**Related Files:**
- `.gitignore` (new)

---

### Task 3: Create .env template file
**Status:** Pending  
**Priority:** High  
**Effort:** 0.5 hours  
**Assignee:** TBD

**Description:**
Create `.env.example` template file to document required environment variables without exposing secrets.

**Acceptance Criteria:**
- [ ] File `.env.example` exists in project root
- [ ] Contains all required environment variables with example/placeholder values
- [ ] Documentation comments explain each variable
- [ ] Database connection parameters are included
- [ ] File paths are included
- [ ] Logging configuration is included
- [ ] Clear instructions for users to copy and configure

**Content Template:**
```
# Database Configuration
DB_DRIVER=SQL Server
DB_SERVER=.\SQLEXPRESS
DB_DATABASE=ETFHoldings
DB_TRUSTED_CONNECTION=yes

# File Paths
CSV_DATA_PATH=C:\Users\YourUsername\Documents\DataSets\ETF_UDatasets\

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/etf_pipeline.log

# Scraping (optional rate limiting)
REQUEST_TIMEOUT=10
RETRY_ATTEMPTS=3
RETRY_DELAY=5
```

**Related Files:**
- `.env.example` (new)
- `README.md` (reference)

---

## Code Quality & Refactoring

### Task 4: Extract hardcoded paths and database connection string to environment variables
**Status:** Pending  
**Priority:** High  
**Effort:** 2 hours  
**Assignee:** TBD

**Description:**
Replace hardcoded paths and database connection strings with environment variable references throughout the codebase. This improves security and configurability.

**Files to Modify:**
- `ETLScript.py` - Hardcoded path in `read_file()`
- `SQLServerService.py` - Hardcoded connection string in `insert_into_table()` and `get_date()`

**Acceptance Criteria:**
- [ ] `ETLScript.py`:
  - [ ] Remove hardcoded path: `"C:\\Users\\smahe\\Documents\\DataSets\\ETF_UDatasets\\"`
  - [ ] Use `os.getenv("CSV_DATA_PATH")` instead
  - [ ] Add validation that path exists
- [ ] `SQLServerService.py`:
  - [ ] Extract connection string to function parameter or env variable
  - [ ] Create helper function `get_connection()` that builds connection string from env vars
  - [ ] Update both `insert_into_table()` and `get_date()` to use new function
  - [ ] Add connection error handling
- [ ] `main.py`:
  - [ ] Add `load_dotenv()` call from `python-dotenv` at startup
- [ ] All imports updated to include `os` and `dotenv`
- [ ] Code can run with `.env` file without modification

**Code Changes Example:**
```python
# Before
cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=ETFHoldings;Trusted_Connection=yes;')

# After
def get_connection():
    driver = os.getenv("DB_DRIVER", "SQL Server")
    server = os.getenv("DB_SERVER", ".\\SQLEXPRESS")
    database = os.getenv("DB_DATABASE", "ETFHoldings")
    trusted_conn = os.getenv("DB_TRUSTED_CONNECTION", "yes")
    
    connection_string = f'Driver={driver};Server={server};Database={database};Trusted_Connection={trusted_conn};'
    return pyodbc.connect(connection_string)
```

**Related Files:**
- `ETLScript.py`
- `SQLServerService.py`
- `main.py`
- `.env.example`
- `requirements.txt` (add python-dotenv)

---

### Task 5: Add logging module and replace print statements
**Status:** Pending  
**Priority:** High  
**Effort:** 2 hours  
**Assignee:** TBD

**Description:**
Implement Python's `logging` module to replace all `print()` statements. This provides better production observability and configurability.

**Current print statements to replace:**
- `DataScraperService.py` - None currently
- `ScrapeETF.py` - Lines with "INSERTED INTO DATABASE", "NO NEW DATA TO INSERT"
- `ETLScript.py` - Lines with "PLEASE SPECIFY A DIRECTORY", "COULD NOT INSERT INTO SERVER"
- `SQLServerService.py` - Lines with "Error converting Data", "UNABLE TO INSERT INTO DATABASE", "get_date failed"
- `PandaService.py` - Exception print statement

**Acceptance Criteria:**
- [ ] Create `logger_config.py` or add logging setup to `main.py`
- [ ] Configure logging to:
  - [ ] Output to console with level from `LOG_LEVEL` env var
  - [ ] Output to file `logs/etf_pipeline.log` (create logs directory if needed)
  - [ ] Use format: `[%(asctime)s] %(levelname)s [%(name)s] %(message)s`
- [ ] All modules import logger: `logger = logging.getLogger(__name__)`
- [ ] Replace all `print()` statements with appropriate log levels:
  - [ ] `logger.info()` for normal operations
  - [ ] `logger.warning()` for potentially problematic situations
  - [ ] `logger.error()` for errors
  - [ ] `logger.debug()` for detailed debugging info
- [ ] Exceptions logged with `logger.exception()` to include stack trace
- [ ] No `print()` statements remain in production code (except for main script entry if desired)
- [ ] Logs directory exists and is gitignored

**Code Changes Example:**
```python
# Before
print("INSERTED INTO DATABASE ", holdingsDate, etf)

# After
logger.info(f"Successfully inserted ETF holdings into database - Date: {holdingsDate}, ETF: {etf}")
```

**Related Files:**
- `main.py`
- `DataScraperService.py`
- `ScrapeETF.py`
- `ETLScript.py`
- `SQLServerService.py`
- `PandaService.py`
- `logger_config.py` (new - optional)
- `.env.example`
- `.gitignore`

---

### Task 6: Refactor exception handling - specific exceptions instead of bare except
**Status:** Pending  
**Priority:** High  
**Effort:** 2 hours  
**Assignee:** TBD

**Description:**
Replace bare `except:` clauses with specific exception types. This improves error handling clarity and prevents masking unexpected errors.

**Bare except clauses to fix:**
1. `ETLScript.py` line ~15: `except:` in directory listing
2. `ETLScript.py` line ~22: `except:` in file processing loop
3. `DataScraperService.py` (if any)
4. `PandaService.py` - Already has specific exception handling (good!)

**Acceptance Criteria:**
- [ ] No bare `except:` clauses remain in the codebase
- [ ] Each except clause catches specific exception type(s):
  - `FileNotFoundError` for missing files/directories
  - `IOError` for file I/O issues
  - `pyodbc.Error` for database errors
  - `RequestException` for HTTP request failures
  - `ValueError` for data conversion failures
  - Generic `Exception` only as absolute last resort with comment explaining why
- [ ] Error messages are descriptive and actionable
- [ ] Logging captures exception details with stack trace
- [ ] Code still recovers gracefully from expected errors

**Code Changes Example:**
```python
# Before
try:
    fileList = os.listdir(fileDirectory)
except:
    return print("PLEASE SPECIFY A DIRECTORY")

# After
try:
    fileList = os.listdir(fileDirectory)
except FileNotFoundError:
    logger.error(f"Directory not found: {fileDirectory}")
    return
except OSError as e:
    logger.error(f"Error accessing directory {fileDirectory}: {e}")
    return
```

**Related Files:**
- `ETLScript.py`
- `ScrapeETF.py`
- All service modules

---

### Task 7: Add docstrings to all functions
**Status:** Pending  
**Priority:** Medium  
**Effort:** 2 hours  
**Assignee:** TBD

**Description:**
Add comprehensive docstrings to all functions using Google-style format. This improves code documentation and IDE support.

**Functions to document:**

**DataScraperService.py:**
- `scrape_table(url, divClass)` - 3 lines
- `scrape_date(url, divClass)` - 3 lines
- `get_funds()` - 3 lines

**PandaService.py:**
- `get_table_headers(table)` - 3 lines
- `get_table_rows(table)` - 3 lines
- `create_pd(table)` - 3 lines
- `add_column(dataFrame, attributeName, value)` - 3 lines
- `change_data_type(df, column, kind)` - 5 lines
- `convert_data_types(df)` - 3 lines

**SQLServerService.py:**
- `insert_into_table(df)` - 5 lines
- `get_date(etf)` - 3 lines
- `get_connection()` - 3 lines (new helper)

**ScrapeETF.py:**
- `scrapeETF(url, etf)` - 5 lines

**ETLScript.py:**
- `read_file(filePath)` - 3 lines
- `remove_white_space(df)` - 3 lines
- `convert_data_types(df)` - 3 lines
- `insert_into_sql(df)` - 3 lines
- `main(fileDirectory)` - 5 lines

**Acceptance Criteria:**
- [ ] All functions have docstrings in Google style format
- [ ] Each docstring includes:
  - [ ] One-line summary of purpose
  - [ ] Extended description (if needed)
  - [ ] Args section with parameter types and descriptions
  - [ ] Returns section with return type and description
  - [ ] Raises section (if applicable)
  - [ ] Example usage (if helpful)
- [ ] Docstrings are above the function definition
- [ ] Parameter types are documented even if not using type hints
- [ ] All public functions are documented

**Docstring Template:**
```python
def function_name(param1, param2):
    """Short one-line description.
    
    Longer description if needed, explaining what the function does,
    any side effects, and important behaviors.
    
    Args:
        param1 (str): Description of param1.
        param2 (int): Description of param2.
    
    Returns:
        DataFrame: Description of return value.
    
    Raises:
        ValueError: When param1 is empty.
        ConnectionError: If database connection fails.
    
    Example:
        >>> result = function_name("test", 42)
        >>> print(result.shape)
        (100, 5)
    """
```

**Related Files:**
- All Python modules (7 files total)

---

### Task 8: Remove unused divClass parameter
**Status:** Pending  
**Priority:** Low  
**Effort:** 0.5 hours  
**Assignee:** TBD

**Description:**
Remove the unused `divClass` parameter from scraping functions since it's never used in the function body.

**Affected Functions:**
- `DataScraperService.py:scrape_table(url, divClass)` - divClass is not used
- `DataScraperService.py:scrape_date(url, divClass)` - divClass is not used

**Acceptance Criteria:**
- [ ] Function signatures updated to remove `divClass` parameter
- [ ] All calls to these functions updated:
  - [ ] `ScrapeETF.py` calls to `ds.scrape_table()` and `ds.scrape_date()`
- [ ] No changes to function behavior
- [ ] Code still passes all tests

**Code Changes Example:**
```python
# Before
def scrape_table(url, divClass):
    # divClass parameter never used
    data = requests.get(url).text
    ...

# After
def scrape_table(url):
    data = requests.get(url).text
    ...
```

**Related Files:**
- `DataScraperService.py`
- `ScrapeETF.py`

---

## Code Cleanup

### Task 9: Delete or repurpose empty scrapePhysicalETF.py
**Status:** Pending  
**Priority:** Low  
**Effort:** 0.25 hours  
**Assignee:** TBD

**Description:**
The file `scrapePhysicalETF.py` is empty and appears to be incomplete work. Decision needed on whether to delete or complete it.

**Acceptance Criteria:**
- [ ] Either:
  - [ ] File is deleted from repository
  - [ ] File is completed with implementation
  - [ ] File is converted to a stub/template for future work
- [ ] Git history reflects the change
- [ ] README updated if this module was referenced

**Related Files:**
- `scrapePhysicalETF.py`

---

## Testing

### Task 10: Add unit tests for PandaService.py
**Status:** Pending  
**Priority:** High  
**Effort:** 2 hours  
**Assignee:** TBD

**Description:**
Create comprehensive unit tests for the `PandaService.py` module, focusing on data type conversion and DataFrame manipulation.

**Test File:** `tests/test_panda_service.py`

**Functions to Test:**
- `get_table_headers()` - Test with sample HTML table
- `get_table_rows()` - Test with sample HTML table
- `create_pd()` - Test DataFrame creation
- `add_column()` - Test adding ETF and Date columns
- `change_data_type()` - Test each conversion type:
  - Currency conversion (handle $, commas, decimals)
  - Quantity conversion (handle decimals, negatives)
  - Percentage conversion (handle % symbol)
  - Date conversion (handle various date formats)

**Acceptance Criteria:**
- [ ] File `tests/test_panda_service.py` exists
- [ ] Uses `pytest` framework
- [ ] Uses `pytest-mock` for mocking
- [ ] Test coverage minimum 85% for module
- [ ] All test cases pass
- [ ] Tests include:
  - [ ] Happy path tests
  - [ ] Edge cases (empty data, null values, malformed data)
  - [ ] Error cases (invalid formats, type mismatches)
- [ ] Fixtures created for sample data
- [ ] Descriptive test names following pattern: `test_function_scenario()`

**Sample Test Structure:**
```python
import pytest
import pandas as pd
from PandaService import change_data_type

class TestChangeDataType:
    def test_currency_conversion_with_dollar_sign(self):
        df = pd.DataFrame({"Value": ["$1,234.56", "$999.99"]})
        result = change_data_type(df, "Value", "currency")
        assert result["Value"].dtype == float
        assert result["Value"].iloc[0] == 1234.56
    
    def test_percentage_conversion_removes_symbol(self):
        df = pd.DataFrame({"Pct": ["45.5%", "12.3%"]})
        result = change_data_type(df, "Pct", "percentage")
        assert result["Pct"].iloc[0] == 45.5
```

**Related Files:**
- `tests/test_panda_service.py` (new)
- `PandaService.py`
- `pytest.ini` (from Task 14)

---

### Task 11: Add unit tests for DataScraperService.py
**Status:** Pending  
**Priority:** High  
**Effort:** 2 hours  
**Assignee:** TBD

**Description:**
Create unit tests for `DataScraperService.py` with mocked HTTP requests to avoid external dependencies.

**Test File:** `tests/test_data_scraper_service.py`

**Functions to Test:**
- `scrape_table(url)` - Test with mocked HTML response
- `scrape_date(url)` - Test date extraction
- `get_funds()` - Test fund list parsing

**Acceptance Criteria:**
- [ ] File `tests/test_data_scraper_service.py` exists
- [ ] Uses `pytest` and `responses` library for HTTP mocking
- [ ] Uses fixtures for mock HTML responses
- [ ] Test coverage minimum 80% for module
- [ ] All test cases pass
- [ ] Tests include:
  - [ ] Successful scraping with valid HTML
  - [ ] Handling malformed HTML
  - [ ] Handling missing elements
  - [ ] Network error scenarios
- [ ] No actual HTTP requests are made during tests
- [ ] Mocked responses use realistic HTML from website

**Sample Test Structure:**
```python
import pytest
from unittest.mock import patch
import requests
from DataScraperService import scrape_table, get_funds

@pytest.fixture
def mock_html_response():
    return """
    <section id="secHoldings">
        <table>
            <tr><th>Security</th><th>Symbol</th></tr>
            <tr><td>Stock A</td><td>STKA</td></tr>
        </table>
    </section>
    """

def test_scrape_table_returns_table(mock_html_response):
    with patch('DataScraperService.requests.get') as mock_get:
        mock_get.return_value.text = mock_html_response
        result = scrape_table("http://example.com")
        assert result is not None
```

**Related Files:**
- `tests/test_data_scraper_service.py` (new)
- `DataScraperService.py`
- `requirements.txt` (add responses library)

---

### Task 12: Add unit tests for SQLServerService.py
**Status:** Pending  
**Priority:** High  
**Effort:** 2 hours  
**Assignee:** TBD

**Description:**
Create unit tests for `SQLServerService.py` with mocked database connections to avoid requiring a live database.

**Test File:** `tests/test_sql_server_service.py`

**Functions to Test:**
- `insert_into_table(df)` - Test insertion logic with mocked connection
- `get_date(etf)` - Test date retrieval
- `get_connection()` - Test connection string building (if created in Task 4)

**Acceptance Criteria:**
- [ ] File `tests/test_sql_server_service.py` exists
- [ ] Uses `pytest` and `unittest.mock` for connection mocking
- [ ] Mocks `pyodbc.connect()` to avoid requiring SQL Server
- [ ] Test coverage minimum 85%
- [ ] All test cases pass
- [ ] Tests include:
  - [ ] Successful insert with valid DataFrame
  - [ ] Rollback on error
  - [ ] Successful date retrieval
  - [ ] Null date handling
  - [ ] Connection error handling
  - [ ] Type conversion in DataFrame
- [ ] Fixtures for sample DataFrames and mock results

**Sample Test Structure:**
```python
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from SQLServerService import insert_into_table

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "Security": ["Stock A", "Stock B"],
        "MarketValue": [1000.0, 2000.0],
        "Symbol": ["STKA", "STKB"],
        "SEDOL": ["123456", "234567"],
        "Quantity": [10.0, 20.0],
        "Weight": [0.45, 0.55],
        "ETF": ["URNM", "URNM"],
        "Date": ["2024-01-15", "2024-01-15"]
    })

def test_insert_into_table_commits_on_success(sample_dataframe):
    with patch('SQLServerService.pyodbc.connect') as mock_connect:
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        
        insert_into_table(sample_dataframe)
        
        # Verify cursor methods were called
        assert mock_cursor.executemany.called
        mock_connect.return_value.commit.assert_called_once()
```

**Related Files:**
- `tests/test_sql_server_service.py` (new)
- `SQLServerService.py`

---

### Task 13: Add integration test for ScrapeETF.py workflow
**Status:** Pending  
**Priority:** Medium  
**Effort:** 2 hours  
**Assignee:** TBD

**Description:**
Create integration test that tests the complete workflow of the `scrapeETF()` function with mocked external services.

**Test File:** `tests/test_scrape_etf_integration.py`

**Test Scenarios:**
1. New data - Should insert when date differs from database
2. No new data - Should skip when date matches database
3. Database error - Should handle gracefully
4. Scraping error - Should handle gracefully

**Acceptance Criteria:**
- [ ] File `tests/test_scrape_etf_integration.py` exists
- [ ] Mocks both `DataScraperService` and `SQLServerService` modules
- [ ] Test cases cover:
  - [ ] Successful scrape and insert (new data)
  - [ ] Skip insert (data already exists)
  - [ ] Database connection error
  - [ ] Network error during scrape
- [ ] Uses fixtures for mock data
- [ ] Verifies correct functions are called with expected arguments
- [ ] Captures log output for assertions
- [ ] All tests pass

**Sample Test Structure:**
```python
import pytest
from unittest.mock import patch, MagicMock
from datetime import date
from ScrapeETF import scrapeETF

def test_scrape_etf_inserts_new_data():
    with patch('ScrapeETF.ds.scrape_table') as mock_scrape_table, \
         patch('ScrapeETF.ds.scrape_date') as mock_scrape_date, \
         patch('ScrapeETF.sql.get_date') as mock_get_date, \
         patch('ScrapeETF.sql.insert_into_table') as mock_insert, \
         patch('ScrapeETF.ps.create_pd') as mock_create_pd:
        
        mock_scrape_date.return_value = date(2024, 1, 15)
        mock_get_date.return_value = date(2024, 1, 10)  # Different date
        mock_create_pd.return_value = MagicMock()
        
        scrapeETF("http://example.com", "TEST")
        
        # Verify insert was called
        assert mock_insert.called
```

**Related Files:**
- `tests/test_scrape_etf_integration.py` (new)
- `ScrapeETF.py`

---

### Task 14: Create pytest configuration
**Status:** Pending  
**Priority:** Medium  
**Effort:** 1 hour  
**Assignee:** TBD

**Description:**
Create pytest configuration file to standardize test settings, coverage, and reporting.

**File Options:**
- `pytest.ini` (recommended) or
- `pyproject.toml` (if using poetry) or
- `setup.cfg` (if using setuptools)

**Acceptance Criteria:**
- [ ] Configuration file exists (`pytest.ini` preferred)
- [ ] Settings configured:
  - [ ] Test directory: `testpaths = tests`
  - [ ] Python files pattern: `python_files = test_*.py`
  - [ ] Test function pattern: `python_functions = test_*`
  - [ ] Minimum coverage threshold: `--cov-fail-under=80`
  - [ ] Coverage report: `--cov=. --cov-report=html --cov-report=term-missing`
  - [ ] Markers for test categorization (unit, integration, slow)
  - [ ] Asyncio mode configured (if async tests exist)
- [ ] Can run tests with: `pytest`
- [ ] Can run with coverage: `pytest --cov`
- [ ] HTML coverage report generates in `htmlcov/`
- [ ] `.gitignore` updated to ignore coverage files

**Sample pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

**Related Files:**
- `pytest.ini` (new) or `pyproject.toml`
- `.gitignore`

---

## Documentation & CI/CD

### Task 15: Document SQL Server schema and stored procedures
**Status:** Pending  
**Priority:** Medium  
**Effort:** 1 hour  
**Assignee:** TBD

**Description:**
Create documentation for the SQL Server database schema, including table structure and required stored procedures.

**File:** `docs/DATABASE_SCHEMA.md`

**Content to Include:**
- Tables schema (columns, types, constraints)
- Indexes
- Stored procedures:
  - `GetLastUpdateDate` - Parameters, returns, purpose
- Sample SQL scripts to create schema
- Data model diagram (text-based or link to external tool)

**Acceptance Criteria:**
- [ ] File `docs/DATABASE_SCHEMA.md` exists
- [ ] Documents `Holdings` table structure:
  - [ ] Column names and data types
  - [ ] Primary keys
  - [ ] Indexes
  - [ ] Constraints
- [ ] Documents `GetLastUpdateDate` stored procedure:
  - [ ] Input parameters
  - [ ] Return values
  - [ ] SQL script to create
- [ ] Includes CREATE TABLE script for easy setup
- [ ] Includes sample data insert scripts
- [ ] SQL Server version compatibility noted

**Sample Content:**
```markdown
# Database Schema

## Holdings Table

| Column | Type | Nullable | Description |
|--------|------|----------|-------------|
| holding_id | INT | NO | Primary Key, auto-increment |
| security_str | VARCHAR(255) | NO | Security name |
| market_val_int | DECIMAL(15,2) | YES | Market value |
| ...

## Stored Procedures

### GetLastUpdateDate
**Purpose:** Retrieve the most recent update date for a given ETF.

**Parameters:**
- @ETF VARCHAR(50) - ETF symbol

**Returns:** DATE - Last update date or NULL if no records exist
```

**Related Files:**
- `docs/DATABASE_SCHEMA.md` (new)
- `README.md`

---

### Task 16: Add GitHub Actions workflow for CI/CD
**Status:** Pending  
**Priority:** Low  
**Effort:** 1.5 hours  
**Assignee:** TBD

**Description:**
Create GitHub Actions workflow to automatically run tests and code quality checks on pull requests and pushes.

**File:** `.github/workflows/ci.yml`

**Acceptance Criteria:**
- [ ] Directory `.github/workflows/` exists
- [ ] File `ci.yml` created with workflow definition
- [ ] Workflow triggers on:
  - [ ] Push to main/master branch
  - [ ] Push to develop branch
  - [ ] Pull requests
- [ ] Workflow steps:
  - [ ] Checkout code
  - [ ] Set up Python (3.8+)
  - [ ] Install dependencies: `pip install -r requirements.txt`
  - [ ] Install test dependencies: `pip install pytest pytest-cov pytest-mock responses`
  - [ ] Run linting/formatting check (optional: pylint, black)
  - [ ] Run tests: `pytest --cov`
  - [ ] Generate coverage report
  - [ ] Fail on coverage below 80%
  - [ ] Upload coverage to codecov (optional)
- [ ] Matrix strategy for multiple Python versions (3.8, 3.9, 3.10, 3.11)
- [ ] Clear, descriptive step names
- [ ] README.md updated with CI badge

**Sample Workflow Structure:**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-mock responses
    
    - name: Run tests
      run: pytest --cov --cov-fail-under=80
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
```

**Related Files:**
- `.github/workflows/ci.yml` (new)
- `README.md`
- `requirements.txt`

---

## Acceptance Criteria Summary

### Must Have (Critical)
- [ ] All environment variables extracted (Task 4)
- [ ] Logging implemented throughout (Task 5)
- [ ] Exception handling refactored (Task 6)
- [ ] Unit tests for core modules (Tasks 10-12)
- [ ] Pytest configuration (Task 14)

### Should Have (Important)
- [ ] Requirements.txt created (Task 1)
- [ ] .gitignore created (Task 2)
- [ ] .env.example template (Task 3)
- [ ] Docstrings added (Task 7)
- [ ] Integration tests (Task 13)
- [ ] CI/CD workflow (Task 16)

### Nice to Have (Polish)
- [ ] Unused parameters removed (Task 8)
- [ ] Empty files cleaned up (Task 9)
- [ ] Database schema documented (Task 15)

---

## Implementation Order

**Recommended sequence based on dependencies:**

1. **Phase 1 - Foundation (Tasks 1-3):** Infrastructure setup
2. **Phase 2 - Code Quality (Tasks 4-7):** Refactoring for production readiness
3. **Phase 3 - Testing (Tasks 10-14):** Comprehensive test coverage
4. **Phase 4 - Polish (Tasks 8-9, 15-16):** Cleanup and CI/CD

**Estimated Total Time:** 16-20 hours

---

## Progress Tracking

| # | Task | Status | Start Date | End Date | Notes |
|----|------|--------|-----------|----------|-------|
| 1 | Create requirements.txt | Done | - | - | - |
| 2 | Create .gitignore | Done | - | - | - |
| 3 | Create .env template | Done | - | - | - |
| 4 | Extract hardcoded values | Done | - | - | - |
| 5 | Add logging | Pending | - | - | - |
| 6 | Refactor exceptions | Pending | - | - | - |
| 7 | Add docstrings | Pending | - | - | - |
| 8 | Remove unused params | Pending | - | - | - |
| 9 | Clean up empty files | Pending | - | - | - |
| 10 | Test PandaService | Pending | - | - | - |
| 11 | Test DataScraperService | Pending | - | - | - |
| 12 | Test SQLServerService | Pending | - | - | - |
| 13 | Test ScrapeETF integration | Pending | - | - | - |
| 14 | Create pytest config | Pending | - | - | - |
| 15 | Document DB schema | Pending | - | - | - |
| 16 | Add CI/CD workflow | Pending | - | - | - |

---

**Last Updated:** 2024  
**Next Review:** After Phase 1 completion
