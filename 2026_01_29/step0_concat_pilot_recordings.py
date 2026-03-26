import warnings
warnings.filterwarnings("ignore")

import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "260129", "Pilots"))

FILE_1 = "Project1 Recording 1.xlsx"
FILE_2 = "Project1 Recording 2.xlsx"
OUTPUT_FILE = "Project1 Recording 1_2 concatenated.xlsx"


def find_column(df, candidates):
    existing = {c.lower(): c for c in df.columns}
    for name in candidates:
        if name.lower() in existing:
            return existing[name.lower()]
    return None


def require_column(df, candidates, description):
    col = find_column(df, candidates)
    if col is None:
        raise KeyError(f"{description} column not found. Tried: {candidates}")
    return col


def parse_start_time(value):
    ts = pd.to_datetime(value, dayfirst=True, errors="coerce")
    if pd.isna(ts):
        ts = pd.to_datetime(value, dayfirst=False, errors="coerce")
    if pd.isna(ts):
        raise ValueError(f"Could not parse start time value: {value}")
    return ts


def main():
    path_1 = os.path.join(DATA_DIR, FILE_1)
    path_2 = os.path.join(DATA_DIR, FILE_2)
    output_path = os.path.join(DATA_DIR, OUTPUT_FILE)

    df1 = pd.read_excel(path_1)
    df2 = pd.read_excel(path_2)

    start_col_1 = require_column(df1, ["Recording start time"], "Recording start time (file 1)")
    start_col_2 = require_column(df2, ["Recording start time"], "Recording start time (file 2)")
    rec_ts_col_2 = require_column(df2, ["Recording time stamp", "Recording timestamp"], "Recording timestamp (file 2)")

    comp_ts_col_1 = require_column(df1, ["Computer timestamp"], "Computer timestamp (file 1)")
    comp_ts_col_2 = require_column(df2, ["Computer timestamp"], "Computer timestamp (file 2)")

    start_1 = parse_start_time(df1[start_col_1].iloc[0])
    start_2 = parse_start_time(df2[start_col_2].iloc[0])
    offset_seconds = (start_2 - start_1).total_seconds()
    offset_us = offset_seconds * 1_000_000.0

    df2_adjusted = df2.copy()
    df2_adjusted[start_col_2] = start_1

    # ET timestamp columns are in microseconds in this pipeline.
    df2_adjusted[rec_ts_col_2] = pd.to_numeric(df2_adjusted[rec_ts_col_2], errors="coerce") + offset_us
    df2_adjusted[comp_ts_col_2] = pd.to_numeric(df2_adjusted[comp_ts_col_2], errors="coerce") + offset_us

    concatenated = pd.concat([df1, df2_adjusted], ignore_index=True)
    concatenated[comp_ts_col_1] = pd.to_numeric(concatenated[comp_ts_col_1], errors="coerce")
    concatenated = concatenated.sort_values(by=comp_ts_col_1, kind="stable").reset_index(drop=True)

    concatenated.to_excel(output_path, index=False)

    print(f"Input 1: {path_1}")
    print(f"Input 2: {path_2}")
    print(f"Output : {output_path}")
    print(f"Applied timestamp offset to file 2: {offset_us:.0f} microseconds")


if __name__ == "__main__":
    main()
