import pandas as pd
import re
import utils
import os

def rename_columns(df):
    new_names = ['баланснаначалопериодазапени', 'оплаченозапени', 'начисленозапериодзапени', 'перерасчетзапени', 'исходящийбалансзапени']

    unnamed_indices = [i for i, col in enumerate(df.columns) if col is None or 'unnamed' in str(col).lower() or 'none' in str(col).lower()]
    for i, new_name in zip(unnamed_indices, new_names):
        df.columns.values[i] = new_name
    return df

def process(df_csv, invoice_date):
    df_csv = utils.csv_normalize_columns_names(df_csv)
    df_csv = df_csv.drop(index=0) # удаление строки которая второй уровень шапки
    df_csv = df_csv.iloc[:-1] # удаление последней суммируюшей строки "к оплате"
    df_csv = rename_columns(df_csv)

    df_csv['расчетныйпериод'] = df_csv['расчетныйпериод'].astype(str)
    df_csv['срокоплатыдо'] = df_csv['срокоплатыдо'].astype(str)

    df_csv_export = df_csv[['кодорганизации', 'наименованиеорганизации', 'начисленозапериодруб', 'перерасчетруб', 'расчетныйпериод']]

    return df_csv_export