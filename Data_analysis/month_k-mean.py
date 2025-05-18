import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# 讀取資料
df = pd.read_csv(r"D:\jeson-porject\Course_material_analysis\ending.csv")

# 建立「月份 × 品項 × 銷量」的 pivot table
pivot = df.groupby(['Month', 'Item'])['Quantity'].sum().reset_index()
pivot_pivoted = pivot.pivot(index='Item', columns='Month', values='Quantity').fillna(0)

# 執行 KMeans 分群
kmeans = KMeans(n_clusters=3, random_state=42)
pivot_pivoted['Cluster'] = kmeans.fit_predict(pivot_pivoted)

# 儲存結果
clustered = pivot_pivoted.reset_index()
clustered.to_csv("clustered_items_by_month.csv", index=False)
print("✅ 聚類結果已儲存為 clustered_items_by_month.csv")

# === 可視化：依群集分類畫每個品項的月銷售趨勢圖 ===
plt.figure(figsize=(14, 8))
month_cols = [col for col in clustered.columns if isinstance(col, (int, float))]

# 設定色彩樣式
palette = sns.color_palette("Set2", n_colors=clustered['Cluster'].nunique())

# 畫每條品項線
for _, row in clustered.iterrows():
    item = row['Item']
    cluster = row['Cluster']
    sales = row[month_cols]
    plt.plot(month_cols, sales, label=item, alpha=0.7, color=palette[cluster])

# 圖表細節
plt.title("Monthly Sales Trends by Item (Cluster Colored)")
plt.xlabel("Month")
plt.ylabel("Total Quantity")
plt.xticks(month_cols)
plt.grid(True, linestyle='--', alpha=0.5)

# 顯示圖例（在右上角）
plt.legend(title="Item", loc='upper right', fontsize='small', frameon=True)
plt.tight_layout()
plt.show()
