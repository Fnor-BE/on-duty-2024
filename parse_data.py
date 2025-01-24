import pandas as pd
import numpy as np
from calendar import monthrange

HEADER_COLUMNS = 5

def load_month(xls, sheet_name, skiprows=0):
    df = pd.read_excel(xls, sheet_name=sheet_name, skiprows=skiprows)
    df.rename(columns={
        df.columns[2]: 'ID',
        df.columns[3]: 'Name',
        df.columns[4]: 'AMPM'
    }, inplace=True)
    return df

def days_in_month(year:int, month:int) -> int:
    _, days_in_month = monthrange(year, month)
    return days_in_month

def drop_columns_after_last_day(df: pd.DataFrame, year:int, month:int) -> pd.DataFrame:
    last_day_number = days_in_month(year, month)
    last_column_index = HEADER_COLUMNS + last_day_number
    
    return df.iloc[:, 0:last_column_index]

def ffill_header_columns(df):
    df[df.columns[0]] = df[df.columns[0]].ffill()
    df[df.columns[1]] = df[df.columns[1]].ffill()
    return df

def drop_rows_without_data(df):
    return df.dropna(subset=['AMPM']).reset_index(drop=True)

def rename_columns_to_datekey(df: pd.DataFrame, year:int, month:int) -> pd.DataFrame:
    for i in range(0, 32):
        datekey = f'{year}{month:02}{i:02}'
        df.rename(columns={i: datekey}, inplace=True)
    return df

def fill_pm_info(df):
    columns = ['ID', 'Name']
    df.loc[ df['AMPM'] == 'PM', columns ] = np.nan
    for column in columns:
        df[column] = df[column].ffill()
    return df

def unpivot_month(df):
    
    df = fill_pm_info(df)
    
    unpivoted = pd.melt(
        df,
        id_vars=['S/Dept', 'Atelier', 'ID', 'Name', 'AMPM'],
        var_name='DateKey',
        value_name='Code'
    )
    return unpivoted
    

def load_and_parse_data(excel_file_path:str, year=2020, skip_sheets:int=0, skiprows:int=0) -> pd.DataFrame:
    excel = pd.ExcelFile(excel_file_path)
    month_sheets = excel.sheet_names[skip_sheets:]
    
    for i, sheet in enumerate(month_sheets):
        month_number = i + skip_sheets
        month_data = load_month(excel_file_path, sheet, skiprows=skiprows)
        month_data = drop_columns_after_last_day(month_data, year, month_number)
        month_data = ffill_header_columns(month_data)
        month_data = drop_rows_without_data(month_data)
        month_data = rename_columns_to_datekey(month_data, year, month_number)
        month_data = unpivot_month(month_data)
        
        if i == 0:
            year_data = month_data
        else:
            year_data = pd.concat([year_data, month_data], ignore_index=True)
            
    return year_data

        