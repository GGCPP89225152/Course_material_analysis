import pandas as pd
df = pd.read_csv("archive/dirty_cafe_sales.csv")
#.venv\Scripts\activate
#讀取CSV檔案為DataFrame
# 定義品項對應分類
item_map = {
    'cake': 'takeaway',
    'smoothie': 'takeaway',
    'coffee': 'takeaway',
    'tea': 'takeaway',
    'sandwich': 'takeaway',
    'cookie': 'takeaway',
    'juice': 'takeaway',
    'salad': 'instore'
}
def datacheck():
    #檢查是否成功讀入資料（資料不為空）
    if df.empty != True:
        
        return True
    else:
        return False
def dataclean(data_clean):
    values = df['Location'].unique()
    print("取得Location欄位中出現過的所有唯一值（不重複）")
    print(values)
    #將Location欄位中的所有值轉換為小寫
    data_clean['Location_Lower'] = data_clean['Location'].str.lower()
    data_clean['Location_Lower'] = data_clean['Location_Lower'].str.replace('[^a-z0-9]', '', regex=True)
    print("Location欄位中的所有值轉換為小寫並移除特殊字元")
    print(data_clean['Location_Lower'].value_counts())
    return data_clean
# 根據品項分類 location
def classify_location(row):
    loc = row['Location_Lower']
    item = str(row['Item']).lower() if pd.notnull(row['Item']) else ''

    if loc in ['instore', 'takeaway']:
        return loc
    elif loc in ['error', 'unknown']:
        return item_map.get(item, 'unknown')
    else:
        return 'unknown'



def main():
    df_clean = None
    #檢查資料是否正確讀取
    if datacheck() == True:
        print("資料讀取成功")
        #values = df['Item'].unique()
        #print("取得Item欄位中出現過的所有唯一值（不重複）")
        #print(values)
        
        
        #將Location欄位中的所有值轉換為小寫
        df_clean = dataclean(df.copy())

        # 套用分類邏輯
        df_clean['Location_Clean'] = df_clean.apply(classify_location, axis=1)

        # 顯示分類結果
        print("Location_Clean 分類結果：")
        print(df_clean['Location_Clean'].value_counts())
        # 顯示無法分類的品項
        print("無法分類的品項統計：")
        print(df_clean[df_clean['Location_Clean'] == 'unknown']['Item'].value_counts())

        # 匯出乾淨檔案
        df_clean.to_csv("cleaned_cafe_sale.csv", index=False)
        print("\n💾 已儲存清理後資料為 cleaned_cafe_sales.csv")

        
    else:
        print("資料讀取失敗")



if __name__ == "__main__":
    main()        