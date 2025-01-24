import pandas as pd

def main():
    pd.set_option('display.max_columns', None)
    
    df = pd.read_excel(EXCEL_FILE, 2)
    print(df)

if __name__ == "__main__":
    main()