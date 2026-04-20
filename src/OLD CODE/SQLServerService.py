import os
import pandas as pd
import pyodbc
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables once
load_dotenv()


# -----------------------------
# Reusable DB connection
# -----------------------------
def get_connection():
    driver = os.getenv("DB_DRIVER")
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    trusted = os.getenv("DB_TRUSTED_CONNECTION")

    conn_str = (
        f"Driver={driver};"
        f"Server={server};"
        f"Database={database};"
        f"Trusted_Connection={trusted};"
    )

    return pyodbc.connect(conn_str)


# -----------------------------
# Bulk insert function
# -----------------------------
def insert_into_table(df: pd.DataFrame):
    cnxn = get_connection()

    try:
        tuples = list(df[[
            "Security", "MarketValue", "Symbol", "SEDOL",
            "Quantity", "Weight", "ETF", "Date"
        ]].itertuples(index=False, name=None))

        with cnxn.cursor() as cur:
            cur.fast_executemany = True
            cur.executemany("""
                INSERT INTO Holdings(
                    security_str,
                    market_val_int,
                    symbol_str,
                    sedol_str,
                    quantity_int,
                    weight_float,
                    etf_str,
                    update_dt
                ) VALUES (?,?,?,?,?,?,?,?)
            """, tuples)

        cnxn.commit()

    except Exception as e:
        cnxn.rollback()
        print("UNABLE TO INSERT INTO DATABASE:", e)
        raise

    finally:
        cnxn.close()


# -----------------------------
# Get latest update date
# -----------------------------
def get_date(etf):
    cnxn = get_connection()

    try:
        with cnxn.cursor() as cur:
            cur.execute("EXEC GetLastUpdateDate @ETF=?", etf)
            row = cur.fetchone()

        if not row or row[0] is None:
            return None

        val = row[0]

        if isinstance(val, datetime):
            return val.date()

        return datetime.strptime(str(val), "%Y-%m-%d").date()

    except Exception as e:
        print("get_date failed:", e)
        return None

    finally:
        cnxn.close()