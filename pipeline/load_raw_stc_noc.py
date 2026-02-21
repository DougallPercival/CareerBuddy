import pandas as pd
import sys

from util.df_func import read_csv_as_str
from util.db_func import write_table

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

    # datafile passed in as argument from external call
    if len(sys.argv) != 2:
            print("Usage: python raw_stc_income.py <datafile>")
            sys.exit(1)

    table = sys.argv[1]

    df = read_csv_as_str(table)

    # Apply the rename mapping
    df.rename(columns=rename_mapping, inplace=True)

    # Convert to DataFrame
    special_df = pd.DataFrame(special_rows)

    # Append to existing df
    df = pd.concat([df, special_df], ignore_index=True)

    write_table(df, table_name="src_ext_stc_noc", schema="raw")
