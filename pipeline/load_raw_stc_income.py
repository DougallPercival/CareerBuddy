import pandas as pd
import sys
import time

from util.df_func import read_csv_as_str
from util.db_func import write_table_copy
from util.logger import get_logger

logger = get_logger(__name__)

# define variables for this run
PIPELINE_NAME="load_raw_stc_income"
# database
SCHEMA_NAME="raw"
TABLE_NAME="src_ext_stc_income"

CHUNK_SIZE = 500_000

# Mapping of old column names → new column names
rename_mapping = {
    'REF_DATE': 'refDate',
    'GEO': 'geo',
    'DGUID': 'DGUID',
    'Work activity during the reference year': 'workActivityRefYear',
    'Age': 'age',
    'Gender': 'gender',
    'Statistics': 'statistics',
    'Coordinate': 'coordinate',
    'Total - Employment income statistics': 'totEmpIncStat',
    'With employment income': 'withEmpInc',
    'Median employment income': 'medEmpInc',
    'Average employment income': 'avgEmpInc',
    'With wages, salaries and commissions': 'withWageSalaryComm',
    'Median wages, salaries and commissions': 'medWageSalaryComm',
    'Average wages, salaries and commissions': 'avgWageSalaryComm',
    'code': 'code'  # stays the same
}

# Special overrides
mapping = {
    "Total - Occupation - Minor group - National Occupational Classification (NOC) 2021": "TM",
    "Occupation - not applicable": "TN",
    "All occupations": "TA"
}

if __name__ == "__main__":
    logger.info(f"Starting {PIPELINE_NAME} - with chunked load")
    start = time.time()
    total_rows = 0

    # datafile passed in as argument from external call
    if len(sys.argv) != 2:
        print("Usage: python raw_stc_income.py <datafile>")
        logger.error(f"No datafile passed in as argument to {PIPELINE_NAME}. Terminating.")
        sys.exit(1)

    table = sys.argv[1]
    logger.info(f"{table} passed in to {PIPELINE_NAME}")

    #df = read_csv_as_str(table)
    for i, chunk in enumerate(pd.read_csv(table, chunksize=CHUNK_SIZE)):
        logger.info(f"Processing chunk {i+1}")

        df = chunk

        # remove columns that start with Symbol
        df = df.loc[:, ~df.columns.str.startswith("Symbol")]

        # update titles where substrings like (#) [#] are
        df.columns = df.columns.str.replace(r"\s*\([^)]*\)", "", regex=True)
        df.columns = df.columns.str.replace(r"\s*\[[^]]*\]", "", regex=True)

        # rename the long title occupation column
        df = df.rename(columns={
            "Occupation - Minor group - National Occupational Classification 2021":
                "occupation"
        })

        # rename income columns
        df.columns = [
            col.split(":", 1)[1].strip() if col.startswith("Employment income statistics")
            else col
            for col in df.columns
        ]


        # Ensure string (preserves leading zeros)
        occ = df["Occupation"].astype(str)

        # Split once on first space
        split = occ.str.split(" ", n=1, expand=True)
        first_part = split[0]
        second_part = split[1]

        # Code = first part only if it's fully numeric
        df["code"] = first_part.where(first_part.str.isdigit())

        # Description:
        # If first part was numeric → use remainder
        # Otherwise → use full original string
        df["description"] = second_part.where(first_part.str.isdigit(), occ)

        mask = df["Occupation"].isin(mapping)
        df.loc[mask, "code"] = df.loc[mask, "occupation"].map(mapping)

        df.drop(columns=["description", "occupation"])

        # Apply the rename
        df.rename(columns=rename_mapping, inplace=True)

        logger.info(f"{PIPELINE_NAME}: Writing {len(df)} records to {SCHEMA_NAME}.{TABLE_NAME}")
        write_start = time.time()

        write_table_copy(df, table_name="src_ext_stc_income", schema="raw")

        write_end = time.time()
        total_rows += len(chunk)
        logger.info(f"{PIPELINE_NAME}: Completed write of chunk {i} to {SCHEMA_NAME}.{TABLE_NAME} in {round(write_end - write_start, 2)} seconds")

    end = time.time()

    
    logger.info(f"{PIPELINE_NAME}: Completed in {round(end - start, 2)} seconds")