import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# -------------------------------------------------------------------
# Load environment variables
# -------------------------------------------------------------------

load_dotenv()  # Loads variables from .env

DB_URI = os.getenv("DATABASE_URI")

if not DB_URI:
    raise ValueError("DATABASE_URI not found in environment variables")


# -------------------------------------------------------------------
# Engine Factory
# -------------------------------------------------------------------

def get_engine():
    """
    Create and return a SQLAlchemy engine.
    """
    return create_engine(DB_URI)


# -------------------------------------------------------------------
# Write Function
# -------------------------------------------------------------------

def write_table(
    df: pd.DataFrame,
    table_name: str,
    schema: str = "public",
    if_exists: str = "append",
    chunksize: int = 10000
):
    """
    Write a pandas DataFrame to a PostgreSQL table.
    """

    if df.empty:
        print(f"[INFO] DataFrame is empty. Nothing written to {schema}.{table_name}")
        return

    engine = get_engine()

    try:
        with engine.begin() as connection:
            df.to_sql(
                name=table_name,
                con=connection,
                schema=schema,
                if_exists=if_exists,
                index=False,
                chunksize=chunksize,
                method="multi"
            )

        print(f"[SUCCESS] Wrote {len(df)} rows to {schema}.{table_name}")

    except SQLAlchemyError as e:
        print(f"[ERROR] Failed to write to {schema}.{table_name}")
        print(str(e))
        raise

    finally:
        engine.dispose()
