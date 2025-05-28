import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

try:
    df = pd.read_csv(r"D:\jeson-porject\Course_material_analysis\ending.csv", encoding='utf-8')
except Exception as e:
    print(f"讀取 CSV 檔案時發生錯誤：{e}")
    df = pd.DataFrame()  # 建立空資料避免後續噴錯

def datacheck():
    if not df.empty:
        print("資料讀取成功")
        print("欄位名稱：", df.columns.tolist())
        return True
    else:
        print("資料為空")
        return False
def Date_week():
    # 檢查是否有 'Transaction Date' 欄位
    if 'Transaction Date' in df.columns:
        try:
            # 將日期欄位轉為 Transaction Datetime 格式
            df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])

            # 新增 weekday 欄位（週一=1，週日=7）
            df['weekday'] = df['Transaction Date'].dt.weekday + 1

            print("成功轉換 'Transaction Date' 並新增 'weekday' 欄位")
            # 顯示前幾筆結果
            print(df[['Transaction Date', 'weekday']].head())

            # 儲存為新的 CSV 檔（避免覆蓋原始檔）
            df.to_csv(r"D:\jeson-porject\Course_material_analysis\ending.csv", index=False, encoding='utf-8-sig')
            print("成功加入 weekday 欄位並儲存新檔案")
        except Exception as e:
            print(f"轉換日期或儲存時發生錯誤：{e}")
    else:
        print("找不到 'Transaction Date' 欄位，請確認欄位名稱")
def main():
    if datacheck():
        # 顯示資料的唯一日期值
        # values = np.sort(df['Transaction Date'].unique())
        # print("唯一日期值：", values)
        Date_week()
        # 顯示資料的前幾筆
        print("資料的前幾筆：") 
        print(df.head())
    else:
        print("資料讀取失敗，請檢查檔案路徑或檔案內容")

if __name__ == "__main__":
    main()
