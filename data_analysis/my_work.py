import pandas as pd
import numpy as np
import re
import os
from dirty_cafe_sales import CafeSalesCleaner
 

class Data_collation:
    #資料整理
    
    def __init__(self, file_path , output_path):
        #初始化函式
        self.file_path = file_path
        self.df = pd.read_csv(file_path,dtype=str)
        self.output_path = output_path
        self.now_date = self.df
        self.errorkey = []
        self.all_value_count = {}
        self.Product_price = {}


    def datac_heck(self):
        #檢查是否成功讀入資料（資料不為空）
        if self.df.empty != True:
            return True
        else:
            return False
        
    def check_data_label_and_first_five_data(self):
        #檢查資料標籤
        print("資料前五筆：")
        print(self.now_date.head())
        return True
    
    def sort_data(self, date_column='Transaction Date', UP = False):
        #排序資料
        #檢查date_column標籤是否存在於資料中
        if date_column not in self.df.columns:
            print(f"資料中不存在標籤 {date_column}，請重新輸入:")
            return False
        else:
            if UP == True:
                self.now_date.sort_values(by=date_column, ascending=True, inplace=True)
            else:
                self.now_date.sort_values(by=date_column, ascending=False, inplace=True)
            

    '''
    清空錯誤值
    '''        
    def data_value_count(self):
        #檢查資料中所有值的計數
        self.all_value_count = {}

        for row in self.df.iterrows():
            for col in self.df.columns:
                val = str(row[1][col]).strip()
                val_lower = val.lower()

                if col not in self.all_value_count:
                    self.all_value_count[col] = {}

                if val_lower not in self.all_value_count[col]:
                    self.all_value_count[col][val_lower] = 0

                self.all_value_count[col][val_lower] += 1

        # 排序並印出結果
        for col, value_counts in self.all_value_count.items():
            print(f"--- 欄位：{col} ---")
            sorted_values = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
            for val, count in sorted_values:
                print(f"{val}: {count}")
            print()
        
        return self.all_value_count

    def input_error_key(self, key):
        #輸入使用者想要的錯誤關鍵字
        self.errorkey.append(key)

    def print_error_key(self):
        #回傳使用者輸入的錯誤關鍵字
        print("使用者輸入的錯誤關鍵字：")
        for key in self.errorkey:
            print(key)
        return self.errorkey

        
        
    def data_clean(self):
        #將資料中包含錯誤關鍵字的資料刪除
        for idx, row in self.df.iterrows():
            for col in self.df.columns:
                val = str(row[col]).strip()
                val_lower = val.lower()

                # 檢查是否有錯誤關鍵字並刪除
                if any(key in val_lower for key in self.errorkey):
                    # 刪除該欄位的資料
                    self.df.at[idx, col] = np.nan

    '''
    插入月份與季度
    '''
    def Fill_in_the_blanks_with_upward_values(self, date_column='Transaction Date'):
        # 檢查欄位是否存在
        if date_column not in self.now_date.columns:
            print(f"資料中不存在標籤「{date_column}」，請重新輸入")
            return False

        # 複製 DataFrame，以免直接修改原始資料（可選）
        self.now_date[date_column] = self.now_date[date_column].fillna(method='ffill')

        return self.df

    def add_month_and_quarter(self, date_column='Transaction Date'):
        #檢查date_column標籤是否存在於資料中
        if date_column not in self.df.columns:
            print(f"資料中不存在標籤 {date_column}，請重新輸入:")
            return False
        
        else:
            # 將日期欄位轉換為 datetime 格式
            self.now_date[date_column] = pd.to_datetime(self.df[date_column], errors='coerce')

            # 找到日期欄位的位置
            date_idx = self.now_date.columns.get_loc(date_column)

            # 在日期欄位後插入「月份」與「季度」
            self.now_date.insert(date_idx + 1, 'Month', self.df[date_column].dt.month)
            self.now_date.insert(date_idx + 2, 'Quarter', self.df[date_column].dt.quarter)

            return True
        

        
    '''
    用數學填補空白
    '''

    '''   
    def Record_product_unit_price(self,item_column='Item',quantlty_column='Quantity' ,price_column='Price Per Unit', total_column='Total Spent'):
        #檢查item_column標籤是否存在於資料中
        if item_column not in self.df.columns:
            print(f"資料中不存在標籤 {item_column}，請重新輸入:")
            return False
        
        if price_column not in self.df.columns:
            print(f"資料中不存在標籤 {price_column}，請重新輸入:")
            return False
        
        if total_column not in self.df.columns:
            print(f"資料中不存在標籤 {total_column}，請重新輸入:")
            return False        
        
        for row in self.now_date.iterrows():
            price = row[1][price_column]
            qty = row[1][quantlty_column]
            total = row[1][total_column]
            item = row[1][item_column]
            # 將數值轉換為浮點數
            price = float(price) if pd.notna(price) else np.nan
            qty = float(qty) if pd.notna(qty) else np.nan
            total = float(total) if pd.notna(total) else np.nan
            item = str(item).strip() if pd.notna(item) else np.nan

            if pd.notnull(price) and pd.notnull(item):
                if self.Product_price.get(item) == None:
                    self.Product_price[item] = price

            elif pd.isnull(price) and pd.notnull(qty) and pd.notnull(total) and pd.notnull(item):
                if self.Product_price.get(item) == None:
                    new_price = total / qty
                    self.Product_price[item] = new_price
            

        #print self.Product_price
        print("品項平均單價：")
        for item, price in self.Product_price.items():
            print(f"{item}: {price}")    

    def Fill_in_the_number_infomation(self, item_column='Item',quantlty_column='Quantity' ,price_column='Price Per Unit', total_column='Total Spent'):
        #檢查item_column標籤是否存在於資料中
        if item_column not in self.df.columns:
            print(f"資料中不存在標籤 {item_column}，請重新輸入:")
            return False
        
        if price_column not in self.df.columns:
            print(f"資料中不存在標籤 {price_column}，請重新輸入:")
            return False
        
        if total_column not in self.df.columns:
            print(f"資料中不存在標籤 {total_column}，請重新輸入:")
            return False
        
        self.Record_product_unit_price(item_column,quantlty_column ,price_column, total_column)
        
        for idx, row in self.now_date.iterrows():
            price = row[price_column]
            qty = row[quantlty_column]
            total = row[total_column]
            item = row[item_column]

            # 清洗數值
            price = float(price) if pd.notna(price) else np.nan
            qty = float(qty) if pd.notna(qty) else np.nan
            total = float(total) if pd.notna(total) else np.nan
            item = str(item).strip() if pd.notna(item) else np.nan

            # 補上價格欄位
            if pd.isnull(price) and pd.notnull(item):
                if item in self.Product_price:
                    self.now_date.at[idx, price_column] = self.Product_price[item]

            if pd.isnull(price) and pd.notnull(qty) and pd.notnull(total):
                new_price = total / qty
                self.now_date.at[idx, price_column] = new_price
'''
            



    '''
    匯出資料
    '''
    def export_data(self):
        #將結果存成新的 CSV 檔案
        self.now_date.to_csv(self.output_path, index=False)
        print(f"處理完成，已儲存為 {self.output_path}")
        return True
    


def main():
    #檢查資料是否正確讀取
    data = Data_collation("archive/dirty_cafe_sales.csv", "dirty_cafe_sales_cleaned.csv")
    if data.datac_heck() == True:
        print("資料讀取成功")
        #values = df['Item'].unique()
        #print("取得Item欄位中出現過的所有唯一值（不重複）")
        #print(values)
        
        data.check_data_label_and_first_five_data()
        #檢查資料中所有值的計數
        #data.data_value_count()
        #排序資料
        data.sort_data(date_column='Transaction Date', UP = True)
        data.check_data_label_and_first_five_data()
        #輸入錯誤關鍵字
        data.input_error_key('error')
        data.input_error_key('unknown')
        data.input_error_key('ERROR')
        data.input_error_key('UNKNOWN')

        #回傳使用者輸入的錯誤關鍵字
        data.print_error_key()

        #將資料中包含錯誤關鍵字的資料刪除
        data.data_clean()

        data.Fill_in_the_blanks_with_upward_values(date_column='Transaction Date')
        #檢查資料中所有值的計數
        data.data_value_count()
        #檢查資料標籤
        #加入月份與季度欄位
        data.add_month_and_quarter(date_column='Transaction Date')
        data.data_value_count()
        #匯出資料
        data.export_data()
        math_data = CafeSalesCleaner("dirty_cafe_sales_cleaned.csv")
        math_data.run_all("cleaned_cafe_sales.csv", "log.csv")
        data = Data_collation("cleaned_cafe_sales.csv", "ending.csv")
        data.data_value_count()
        data.export_data()

    else:
        print("資料讀取失敗")


if __name__ == "__main__":
    main()