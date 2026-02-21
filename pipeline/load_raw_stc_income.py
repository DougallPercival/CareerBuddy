import pandas as pd
import sys

from util.df_func import read_csv_as_str
from util.db_func import write_table


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

    # datafile passed in as argument from external call
    if len(sys.argv) != 2:
        print("Usage: python raw_stc_income.py <datafile>")
        sys.exit(1)

    table = sys.argv[1]

    df = read_csv_as_str(table)
    print("read table")

    # remove columns that start with Symbol
    df = df.loc[:, ~df.columns.str.startswith("Symbol")]
    print("removed symbol columns")
    # update titles where substrings like (#) [#] are
    df.columns = df.columns.str.replace(r"\s*\([^)]*\)", "", regex=True)
    df.columns = df.columns.str.replace(r"\s*\[[^]]*\]", "", regex=True)

    # rename the long title occupation column
    df = df.rename(columns={
        "Occupation - Minor group - National Occupational Classification 2021":
            "Occupation"
    })

    # rename income columns
    df.columns = [
        col.split(":", 1)[1].strip() if col.startswith("Employment income statistics")
        else col
        for col in df.columns
    ]
    print("rename income columns")

    # Ensure string (preserves leading zeros)
    occ = df["Occupation"].astype(str)

    # Split once on first space
    split = occ.str.split(" ", n=1, expand=True)
    print("split")

    first_part = split[0]
    second_part = split[1]

    # Code = first part only if it's fully numeric
    df["code"] = first_part.where(first_part.str.isdigit())

    # Description:
    # If first part was numeric → use remainder
    # Otherwise → use full original string
    df["description"] = second_part.where(first_part.str.isdigit(), occ)
    print("finished description")

    mask = df["Occupation"].isin(mapping)
    df.loc[mask, "code"] = df.loc[mask, "Occupation"].map(mapping)

    print("mapped code")
    df.drop(columns=["description", "Occupation"])

    # Apply the rename
    df.rename(columns=rename_mapping, inplace=True)
    print("finished rename and writing to database")
    write_table(df, table_name="src_ext_stc_income", schema="raw")