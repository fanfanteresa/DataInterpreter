# -*- encoding: utf-8 -*-
# -*- encoding: utf-8 -*-

import pandas as pd
from tools.tool_registry import register_tool


TAGS = ["report interpreting"]


# Define a converter function that will parse percentage strings to floats
def parse_percentage(value):
    try:
        # Remove the percentage sign and convert to float
        return float(value.strip().strip('%')) / 100
    except AttributeError:
        # If value is not a string, return it as it is
        return value


@register_tool(tags=TAGS)
def read_excel(filepath: str) -> pd.DataFrame:
    """
    Load the Excel file into a pandas dataframe

    Args:
        filepath: The file path

    """
    df = pd.read_excel(filepath, thousands=',')
    # check for percentage sign
    percentage_cols = []
    for col in df.columns:
        if type(df[col][0]) is str:
            if "%" in df[col][0]:
                percentage_cols.append(col)
    # print(f"percentage columns: {' '.join(percentage_cols)}")
    for col in percentage_cols:
        df[col] = df[col].apply(parse_percentage)
    return df
