import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# 讀取資料
df = pd.read_csv(r"D:\jeson-porject\Course_material_analysis\ending.csv")

# 每筆交易中的品項列表（按 Transaction ID 聚合）
transactions = df.groupby("Month")["Item"].apply(list).tolist()

# 轉換為布林矩陣
te = TransactionEncoder()
te_array = te.fit(transactions).transform(transactions)
df_encoded = pd.DataFrame(te_array, columns=te.columns_)

# 套用 Apriori，找出頻繁項集
frequent_itemsets = apriori(df_encoded, min_support=0.01, use_colnames=True)

# 擷取關聯規則
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

# 查看結果
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])


