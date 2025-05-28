import pandas as pd
from sklearn.preprocessing import LabelEncoder

# 讀取 CSV 檔案
file_path = r"D:\jeson-porject\Course_material_analysis\ending.csv"
df = pd.read_csv(file_path)

# 建立 LabelEncoder 實例
le_payment = LabelEncoder()
le_location = LabelEncoder()

# 執行編碼
payment_encoded = le_payment.fit_transform(df['Payment Method'])
location_encoded = le_location.fit_transform(df['Location'])

# 插入欄位：在原欄位後面插入編碼結果
payment_idx = df.columns.get_loc('Payment Method') + 1
location_idx = df.columns.get_loc('Location') + 1

df.insert(payment_idx, 'Payment Method Encoded', payment_encoded)
df.insert(location_idx + 1, 'Location Encoded', location_encoded)  # 注意：插入前已加了一欄，因此要再 +1

# 顯示對應關係
print("Payment Method 編碼對應：")
for i, label in enumerate(le_payment.classes_):
    print(f"{label} -> {i}")

print("\nLocation 編碼對應：")
for i, label in enumerate(le_location.classes_):
    print(f"{label} -> {i}")

# 顯示轉換後的前幾筆
print("\n轉換後預覽：")
print(df[['Payment Method', 'Payment Method Encoded', 'Location', 'Location Encoded']].head())

# 儲存新檔案
output_path = "encoded_data.csv"
df.to_csv(output_path, index=False)
print(f"\n轉換完成，已儲存至：{output_path}")
