import pandas as pd
import numpy as np

def create_dimdate(start: str, end:str) -> pd.DataFrame:
    dimdate = pd.DataFrame({
        'Date': pd.date_range(start=start, end=end, freq="D")
    })
    
    dimdate['DateKey'] = dimdate['Date'].dt.strftime('%Y%m%d')
    
    dimdate['DayOfWeek'] = dimdate['Date'].dt.weekday + 1
    dimdate['DayOfWeekText'] = dimdate['Date'].dt.day_name()
    dimdate['DayOfWeekShort'] = dimdate['Date'].dt.strftime('%a')
    
    dimdate['IsWeekend'] = np.where( dimdate['DayOfWeek'] > 5, 1, 0 )
    
    
    return dimdate

def add_holidays(dimdate: pd.DataFrame, holidays:list) -> pd.DataFrame:
    
    dimdate['IsHoliday'] = 0    
    for day in holidays:
        dimdate.loc[dimdate['Date'] == day, 'IsHoliday'] = 1
        
    
    dimdate['DaysToHoliday'] = dimdate['Date'].apply(
        lambda date: min(
            abs(np.busday_count(date.date(), pd.to_datetime(holiday).date())) 
            for holiday in holidays
        )
    )
    
    return dimdate



if __name__ == '__main__':
    print(create_dimdate('2024-01-01', '2024-12-31'))