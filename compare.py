# 測試演算法差異

# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import time
import re

DATA_SET = 100000

# 1. 模擬生成 DATA_SET 筆資料
print(f"[INFO] 正在生成 {DATA_SET} 筆模擬資料...")
cities = ["臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市", "基隆市", "新竹市"]
# 隨機產生 DATA_SET 個地址資料
data = {
    "City": [np.random.choice(cities) + "某某區某某路" for _ in range(DATA_SET)],
    "Name": [f"診所{i}" for i in range(DATA_SET)]
}
df = pd.DataFrame(data)
print(df.head())
print()

# 定義我們要統計的縣市目標
target_cities = cities.copy()

# ---------------------------------------------------------
# 方法 A: 傳統 For 迴圈 (逐一篩選)
# ---------------------------------------------------------
print(f"\n[測試 1] 開始執行：傳統 For 迴圈 + str.contains")
start_time = time.time()

counts_for = {}
for city in target_cities:
    # 這裡會掃描整個 DataFrame 共 8 次 (縣市數量)
    count = df[df["City"].str.contains(city, na=False)].shape[0]
    counts_for[city] = count

end_time = time.time()
for_duration = end_time - start_time
print(f">> 方法 A 耗時: {for_duration:.6f} 秒")


# ---------------------------------------------------------
# 方法 B: 向量化 Regex (一次掃描)
# ---------------------------------------------------------
print(f"[測試 2] 開始執行：向量化 Regex (Vectorization)")
start_time = time.time()

# 建立 Regex 模式： (臺北市|新北市|桃園市...)
pattern = "|".join(target_cities)

# 向量化操作：
# 1. str.extract 在底層一次性比對所有模式
# 2. value_counts 在底層進行 C 語言級別計數
counts_vec = df["City"].str.extract(f"({pattern})")[0].value_counts()

# 補齊可能缺失的城市 (數量為 0 的情形)
stats_df = counts_vec.reindex(target_cities, fill_value=0)

end_time = time.time()
vec_duration = end_time - start_time
print(f">> 方法 B 耗時: {vec_duration:.6f} 秒")


# ---------------------------------------------------------
# 結果比較
# ---------------------------------------------------------
print("\n" + "="*40)
print(f"效能提升倍數: {for_duration / vec_duration:.2f} 倍")
print("="*40)
print("\n[統計結果驗證] (兩者結果應相同):")
print(f"方法 A (前三名): {list(counts_for.items())[:3]}")
print(f"方法 B (前三名): {stats_df.head(3).to_dict()}")