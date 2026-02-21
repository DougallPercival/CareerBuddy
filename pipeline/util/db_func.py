import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import io
from util.logger import get_logger

logger = get_logger(__name__)

# -------------------------------------------------------------------
# Load environment variables
# -------------------------------------------------------------------

load_dotenv()  # Loads variables from .env

DB_URI = os.getenv("DATABASE_URI")

if not DB_URI:
    logger.error("DATABASE_URI not found in environment variables")
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
        logger.info(f"[INFO] DataFrame is empty. Nothing written to {schema}.{table_name}")
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

        logger.info(f"[SUCCESS] Wrote {len(df)} rows to {schema}.{table_name}")

    except SQLAlchemyError as e:
        logger.error(f"[ERROR] Failed to write to {schema}.{table_name}")
        logger.error(str(e))
        raise

    finally:
        engine.dispose()



def write_table_copy(df: pd.DataFrame, table_name: str, schema: str = "public"):
    """
    Fast bulk load using Postgres COPY
    """
    engine = get_engine()
    conn = engine.raw_connection()
    cursor = conn.cursor()

    try:
        buffer = io.StringIO()
        df.to_csv(buffer, index=False, header=False)
        buffer.seek(0)

        # tell Postgres exactly which columns we’re writing
        columns = ", ".join([f'"{c}"' for c in df.columns])

        cursor.copy_expert(
            f"COPY {schema}.{table_name} ({columns}) FROM STDIN WITH CSV",
            buffer
        )

        conn.commit()
        logger.info(f"[SUCCESS] Loaded {len(df)} rows into {schema}.{table_name}")

    except Exception as e:
        conn.rollback()
        logger.error(e)
        raise e

    finally:
        cursor.close()
        conn.close()
