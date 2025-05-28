import pandas as pd

# 讀取 CSV 檔案
file_path = r"D:\jeson-porject\Course_material_analysis\monthly_item_summary.csv"
df = pd.read_csv(file_path)

# 建立 pivot table：month 為列，item 為欄，quantity 為值
pivot_table = pd.pivot_table(df,
                             index='month',
                             columns='item',
                             values='quantity',
                             aggfunc='sum',
                             fill_value=0)

# 顯示前幾筆結果
print(pivot_table.head())

# 儲存結果為新 CSV 檔案
output_path = "new-monthly_item_sales_summary.csv"
pivot_table.to_csv(output_path)
print(f"\n已儲存轉換後的檔案至：{output_path}")
