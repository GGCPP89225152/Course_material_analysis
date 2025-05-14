import pandas as pd
import numpy as np
import random

class CafeSalesCleaner:

    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)
        self.log = []
        self.item_counts = {}

    #清除錯誤值
    def clean_errors(self):
        target_cols = ['Item', 'Quantity', 'Price Per Unit', 'Total Spent']
        for col in target_cols:
            self.df[col] = self.df[col].replace(r'(?i)\b(ERROR|UNKNOWN)\b', np.nan, regex=True)

        self.df['Quantity'] = pd.to_numeric(self.df['Quantity'], errors='coerce')
        self.df['Price Per Unit'] = pd.to_numeric(self.df['Price Per Unit'], errors='coerce')
        self.df['Total Spent'] = pd.to_numeric(self.df['Total Spent'], errors='coerce')

    #刪除不可靠的行
    def remove_unreliable_rows(self):
        target_cols = ['Item', 'Quantity', 'Price Per Unit', 'Total Spent']
        self.df['Null_Count'] = self.df[target_cols].isna().sum(axis=1)
        self.df = self.df[~((self.df['Null_Count'] >= 3) | 
                            (self.df['Quantity'].isna() & self.df['Total Spent'].isna()))]
        self.df.drop(columns='Null_Count', inplace=True)

    #計算統計數據
    def compute_statistics(self):
        known = self.df.dropna(subset=['Item', 'Quantity', 'Total Spent']).copy()
        known['unit_price'] = known['Total Spent'] / known['Quantity']
        self.avg_price = known.groupby('Item')['unit_price'].mean()
        self.item_counts = known['Item'].value_counts()
        self.pay_stats = known.groupby(['Item', 'Payment Method']).size().unstack(fill_value=0)

    #填補單價
    def fill_price_per_unit(self):
        for i, row in self.df.iterrows():
            price, qty, total, item = row[['Price Per Unit', 'Quantity', 'Total Spent', 'Item']]

            if pd.isna(price):
                if pd.notna(qty) and pd.notna(total) and qty != 0:
                    new_price = total / qty
                    method = "由 Total ÷ Quantity 補推"
                elif pd.notna(item) and item in self.avg_price:
                    new_price = self.avg_price[item]
                    method = "品項平均單價"
                else:
                    continue

                self.df.at[i, 'Price Per Unit'] = new_price
                self.log.append({"Index": i, "Filled": "Price Per Unit", "Value": new_price, "Method": method})

    #填補數量和總金額
    def fill_quantity_and_total(self):
        for i, row in self.df.iterrows():
            qty, price, total = row[['Quantity', 'Price Per Unit', 'Total Spent']]

            if pd.isna(total) and pd.notna(qty) and pd.notna(price):
                total = qty * price
                self.df.at[i, 'Total Spent'] = total
                self.log.append({"Index": i, "Filled": "Total Spent", "Value": total})

            elif pd.isna(qty) and pd.notna(total) and pd.notna(price) and price != 0:
                qty = total / price
                self.df.at[i, 'Quantity'] = qty
                self.log.append({"Index": i, "Filled": "Quantity", "Value": qty})

    def Calculate_item_ratio(self):
        self.item_counts = {}

        # 僅保留 Item 有值的資料，排除空值干擾
        valid_df = self.df[self.df['Item'].notna()]

        # 計算所有價格的總出現次數（僅限於 Item 有值的列）
        overall_price_distribution = valid_df['Price Per Unit'].value_counts().to_dict()

        for i, row in valid_df.iterrows():
            item = row['Item']
            price = row['Price Per Unit']

            if item not in self.item_counts:
                self.item_counts[item] = {
                    'count': 0,
                    'price': 0.0,
                    'same_price_proportion': 0.0
                }

            self.item_counts[item]['count'] += 1
            self.item_counts[item]['price'] = price  # 僅保留最後一次出現的價格

        for item, data in self.item_counts.items():
            price = data['price']
            item_count = data['count']
            total_same_price_across_all = overall_price_distribution.get(price, 1)
            self.item_counts[item]['same_price_proportion'] = item_count / total_same_price_across_all

        return self.item_counts


        
    ##填補品項
    def fill_item(self):
        table = self.Calculate_item_ratio()

        for i, row in self.df.iterrows():
            item = row['Item']
            price = row['Price Per Unit']

            # 只處理 Item 為空的情況
            if pd.isna(item):
                candidates = []
                weights = []

                # 找出所有同價格的品項及其比率（作為機率權重）
                for known_item, stats in table.items():
                    if stats['price'] == price:
                        candidates.append(known_item)
                        weights.append(stats['same_price_proportion'])

                # 進行加權隨機選擇
                if candidates and sum(weights) > 0:
                    filled_item = random.choices(candidates, weights=weights, k=1)[0]
                    self.df.at[i, 'Item'] = filled_item

        return self.df
                
            

    def export_results(self, cleaned_filepath, log_filepath):
        self.df.to_csv(cleaned_filepath, index=False)
        pd.DataFrame(self.log).to_csv(log_filepath, index=False)

    def run_all(self, cleaned_filepath, log_filepath):
        self.clean_errors()
        self.remove_unreliable_rows()
        self.compute_statistics()
        self.fill_price_per_unit()
        self.fill_quantity_and_total()

        self.fill_item()
        self.export_results(cleaned_filepath, log_filepath)

def main():
    filepath = r'/home/jeson/porject/data_analysis/ending.csv'
    cleaned_filepath = 'cleaned_cafe_sales.csv'
    log_filepath = 'cleaning_log.csv'

    cleaner = CafeSalesCleaner(filepath)
    cleaner.run_all(cleaned_filepath, log_filepath)
    print("資料清理完成，已儲存為 cleaned_cafe_sales.csv")

if __name__ == "__main__":
    main()