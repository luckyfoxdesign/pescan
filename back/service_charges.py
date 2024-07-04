import pandas as pd
import re
import db
import utils
import os


def condition(row):
    return row.isna().sum() > 3

def clean_rows_headers(df):
    mask = df.apply(condition, axis=1)
    df_cleaned = df[~mask]
    return df_cleaned

def update_org_code(df):
    col_1 = 'кодорганизации'

    df.reset_index(drop=True, inplace=True)
    for i in range(1, len(df)):
        if pd.isna(df.at[i, col_1]):
            df.at[i, col_1] = df.at[i-1, col_1]
    
    return df

def process(df_csv, db_columns_metadata, invoice_date):
    df_csv = utils.csv_normalize_columns_names(df_csv)
    df_csv = clean_rows_headers(df_csv)
    df_csv = update_org_code(df_csv)

    df_csv = df_csv.drop(columns=['едизм'])
    df_csv = df_csv.reset_index(drop=True)

    df_csv_export = df_csv[['кодорганизации', 'видуслуги', 'начисленозапериодруб']]
    
    return df_csv_export
