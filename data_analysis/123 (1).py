import pandas as pd

def add_month_and_quarter(df, date_column='Transaction Date'):

    # 將日期欄位轉換為 datetime 格式
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

    # 找到日期欄位的位置
    date_idx = df.columns.get_loc(date_column)

    # 在日期欄位後插入「月份」與「季度」
    df.insert(date_idx + 1, 'Month', df[date_column].dt.month)
    df.insert(date_idx + 2, 'Quarter', df[date_column].dt.quarter)

    return df

if __name__ == "__main__":
    # 讀取 CSV 檔案
    file_path = 'C:/Users/沈丞恩/Desktop/python/data/dirty_cafe_sales.csv'
    df = pd.read_csv(file_path)

    # 加入月份與季度欄位
    df = add_month_and_quarter(df, date_column='Transaction Date')

    # 將結果存成新的 CSV 檔案
    output_path = 'updated_sales.csv'
    df.to_csv(output_path, index=False)

    print(f"處理完成，已儲存為 {output_path}")
