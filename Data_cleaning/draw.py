import pandas as pd
import matplotlib.pyplot as plt

# 讀取資料
file_path = r"D:\jeson-porject\Course_material_analysis\new-monthly_item_sales_summary.csv"
df_summary = pd.read_csv(file_path, index_col=0)

# 繪圖
fig, ax = plt.subplots(figsize=(12, 6))
df_summary.plot(kind='line', ax=ax, colormap='tab20', marker='o')  # 加上 marker 讓每個點明顯

# 標題與軸標籤
plt.title("Monthly sales of each product", fontsize=14)
plt.xlabel("month", fontsize=12)
plt.ylabel("quantity", fontsize=12)
plt.xticks(rotation=45)

# 顯示圖例在圖外右側
plt.legend(
    title="Product",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    borderaxespad=0
)

# 調整整體排版避免被擠壓
plt.tight_layout(rect=[0, 0, 0.85, 1])

# 儲存圖檔
plt.savefig("monthly_item_sales_line_with_legend_outside.png", dpi=300, bbox_inches="tight")

# 顯示圖表
plt.show()

