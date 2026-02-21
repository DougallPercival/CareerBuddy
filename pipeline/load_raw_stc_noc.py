import pandas as pd
import sys
import time

from util.df_func import read_csv_as_str
from util.db_func import write_table
from util.logger import get_logger

logger = get_logger(__name__)

# define variables for this run
PIPELINE_NAME="load_raw_stc_noc"
# database
SCHEMA_NAME="raw"
TABLE_NAME="src_ext_stc_noc"

# Mapping of old column names → new column names
rename_mapping = {
    'Level': 'level',
    'Hierarchical structure': 'hierarchy',
    'Code - NOC 2021 V1.0': 'code',
    'Class title': 'classTitle',
    'Class definition': 'classDefinition'
}

# rows to add
special_rows = [
    {
        "classTitle": "Total - Occupation - Minor group - National Occupational Classification (NOC) 2021",
        "code": "TM",
        "hierarchy": "Total",
        "level": 0,
        "classDefinition": ""
    },
    {
        "classTitle": "Occupation - not applicable",
        "code": "TN",
        "hierarchy": "Total",
        "level": 0,
        "classDefinition": ""
    },
    {
        "classTitle": "All occupations",
        "code": "TA",
        "hierarchy": "Total",
        "level": 0,
        "classDefinition": ""
    }
]

if __name__ == "__main__":
    logger.info(f"Starting {PIPELINE_NAME}")
    start = time.time()
    
    # datafile passed in as argument from external call
    if len(sys.argv) != 2:
            print("Usage: python raw_stc_income.py <datafile>")
            logger.error(f"No datafile passed in as argument to {PIPELINE_NAME}. Terminating.")
            sys.exit(1)

    table = sys.argv[1]
    logger.info(f"{table} passed in to {PIPELINE_NAME}")

    df = read_csv_as_str(table)

    # Apply the rename mapping
    df.rename(columns=rename_mapping, inplace=True)

    # Convert to DataFrame
    special_df = pd.DataFrame(special_rows)

    # Append to existing df
    df = pd.concat([df, special_df], ignore_index=True)
    
    logger.info(f"{PIPELINE_NAME}: Writing {len(df)} records to {SCHEMA_NAME}.{TABLE_NAME}")
    write_start = time.time()

    write_table(df, table_name=TABLE_NAME, schema=SCHEMA_NAME)

    write_end = time.time()
    end = time.time()

    logger.info(f"{PIPELINE_NAME}: Completed write to {SCHEMA_NAME}.{TABLE_NAME} in {round(write_end - write_start, 2)} seconds")
    logger.info(f"{PIPELINE_NAME}: Completed in {round(end - start, 2)} seconds")
