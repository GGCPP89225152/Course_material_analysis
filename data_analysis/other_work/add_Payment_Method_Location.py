import pandas as pd
import numpy as np

# 讀取資料
df = pd.read_csv(r"D:\jeson-porject\Course_material_analysis\data_analysis\ending.csv")  # 請將路徑替換成實際檔案位置

# 檢查缺值數量
missing_payment = df['Payment Method'].isna().sum()
missing_location = df['Location'].isna().sum()

# 計算現有類別分布
payment_counts = df['Payment Method'].value_counts()
location_counts = df['Location'].value_counts()

# 根據原比例生成補值數量
def generate_fill_values(missing_count, value_counts):
    ratios = value_counts / value_counts.sum()
    fill_counts = (ratios * missing_count).round().astype(int)
    # 誤差修正
    diff = missing_count - fill_counts.sum()
    if diff != 0:
        adjustment = np.sign(diff)
        for _ in range(abs(diff)):
            idx = fill_counts.idxmin() if adjustment > 0 else fill_counts.idxmax()
            fill_counts[idx] += adjustment
    return fill_counts

payment_fill_counts = generate_fill_values(missing_payment, payment_counts)
location_fill_counts = generate_fill_values(missing_location, location_counts)

# 建立補值清單並打亂順序
payment_fill_values = np.concatenate([[k] * v for k, v in payment_fill_counts.items()])
location_fill_values = np.concatenate([[k] * v for k, v in location_fill_counts.items()])
np.random.shuffle(payment_fill_values)
np.random.shuffle(location_fill_values)

# 填補缺值
df.loc[df['Payment Method'].isna(), 'Payment Method'] = payment_fill_values
df.loc[df['Location'].isna(), 'Location'] = location_fill_values

# 儲存結果（選擇性）
df.to_csv("filled_data.csv", index=False)

