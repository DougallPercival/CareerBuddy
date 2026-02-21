import pandas as pd

def read_csv_as_str(table):
    """
    Load a provided csv entirely as strings
    """
    return pd.read_csv(table, dtype=str)