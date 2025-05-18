import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# 讀取資料
df = pd.read_csv(r"D:\jeson-porject\Course_material_analysis\ending.csv")

# 建立「季度 × 品項 × 銷量」的 pivot table
pivot = df.groupby(['Quarter', 'Item'])['Quantity'].sum().reset_index()
pivot_pivoted = pivot.pivot(index='Item', columns='Quarter', values='Quantity').fillna(0)

# K-Means 聚類（你可調整 n_clusters 數量）
kmeans = KMeans(n_clusters=3, random_state=42)
pivot_pivoted['Cluster'] = kmeans.fit_predict(pivot_pivoted)

# 轉回 DataFrame 並存檔
clustered = pivot_pivoted.reset_index()
clustered.to_csv("clustered_items_by_quarter.csv", index=False)
print("✅ 聚類結果已儲存至 clustered_items_by_quarter.csv")

# === 可視化：品項季度銷量折線圖（依群集分色） ===
plt.figure(figsize=(12, 8))
quarter_cols = [1, 2, 3, 4]

for _, row in clustered.iterrows():
    item = row['Item']
    cluster = row['Cluster']
    sales = row[quarter_cols]
    plt.plot(quarter_cols, sales, label=item, alpha=0.6)

# 標示色彩
plt.title("Sales trends of each product by season")
plt.xlabel("Quarter")
plt.ylabel("total_sales")
plt.xticks([1, 2, 3, 4])
plt.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1, fontsize='small')
plt.tight_layout()
plt.show()
