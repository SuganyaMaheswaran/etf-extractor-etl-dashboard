# ETFHoldings Database Data Dictionary

**Schema:** dbo

---

## Table: Holdings

| Column Name | Data Type | Nullable | Default | Primary Key | Foreign Key | Description |
|-------------|----------|---------|---------------|-------------|------------|-------------|
| HoldingID   | INT      | NO      | IDENTITY(1,1) | Yes       |            | Unique ID for each holding |
| ETF_ID      | INT      | NO      |               |           | ETFS.ETF_ID | ID of the ETF |
| Security_ID | INT      | NO      |               |           | Securities.Security_ID | ID of the security |
| Quantity    | DECIMAL  | YES     |               |           |            | Quantity of the security held |
| MarketValue | DECIMAL  | YES     |               |           |            | Market value of the holding |
| Weight      | FLOAT    | YES     |               |           |            | Weight of the holding in ETF |

---

## Table: ETFS

| Column Name | Data Type | Nullable | Default | Primary Key | Foreign Key | Description |
|-------------|----------|---------|--------|-------------|------------|-------------|
| ETF_ID      | INT      | NO      | IDENTITY(1,1) | Yes       |            | Unique ID for ETF |
| Name        | NVARCHAR(255) | NO |           |           |            | Name of the ETF |
| Symbol      | NVARCHAR(50)  | NO |           |           |            | ETF ticker symbol |
| FundManager | NVARCHAR(255) | YES|           |           |            | Name of the fund manager |
| InceptionDate | DATE   | YES     |           |           |            | Date ETF was created |

---

## Table: Securities

| Column Name | Data Type | Nullable | Default | Primary Key | Foreign Key | Description |
|-------------|----------|---------|--------|-------------|------------|-------------|
| Security_ID | INT      | NO      | IDENTITY(1,1) | Yes       |            | Unique ID for security |
| Name        | NVARCHAR(255) | NO |           |           |            | Name of the security |
| Symbol      | NVARCHAR(50)  | NO |           |           |            | Security ticker symbol |
| ISIN        | NVARCHAR(50)  | YES |           |           |            | International Securities ID |
| SEDOL       | NVARCHAR(50)  | YES |           |           |            | Stock Exchange Daily Official List code |
| AssetType   | NVARCHAR(50)  | YES |           |           |            | Type of asset (e.g., equity, bond) |

---

## Table: ETF_Securities

| Column Name | Data Type | Nullable | Default | Primary Key | Foreign Key | Description |
|-------------|----------|---------|--------|-------------|------------|-------------|
| ETF_ID      | INT      | NO      |           |           | ETFS.ETF_ID | ETF ID |
| Security_ID | INT      | NO      |           |           | Securities.Security_ID | Security ID |
| Quantity    | DECIMAL  | YES     |           |           |            | Quantity held (optional) |

---

### Notes
- `ETF_Securities` stores holdings of individual securities for each ETF. Each row references one ETF and one Security, with quantity information. This table ensures uniqueness of ETF + Security combinations.”
- Primary keys are indicated; foreign keys show relationships between tables.
- Fill in descriptions with additional business logic if needed.
