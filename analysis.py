# -*- coding: utf-8 -*-
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CONFIG_PATH = "./config.json"
CONFIG      = {}
AREA_DATA   = {}
csv_file    = pd.DataFrame()

def init():
    global CONFIG, AREA_DATA, csv_file
    
    print("[INFO] 正在初始化系統資源...")
    
    if not os.path.exists(CONFIG_PATH):
        print(f"[ERROR] 找不到設定檔: {CONFIG_PATH}")
        return
        
    with open(CONFIG_PATH, "r", encoding = "utf-8") as file:
        CONFIG = json.load(file)
    
    AREA_DATA = CONFIG.get("area_data", {})
    data_path = CONFIG["settings"]["data_path"]
    
    if os.path.exists(data_path):
        # 載入資料
        csv_file = pd.read_csv(data_path, encoding = "utf-8")
        print(f"[SUCCESS] 系統初始化完成，已載入: {data_path}")
    else:
        print(f"[ERROR] 找不到資料檔案: {data_path}")

def user_input(prompt, valid_options = None, input_type = int):
    while True:
        try:
            raw_input = input(f"\n{prompt}")
            user_val = input_type(raw_input)
            
            if valid_options and user_val not in valid_options:
                print(f"[ERROR] 請輸入範圍內的數字: {list(valid_options)}")
                continue
            
            return user_val
        except ValueError:
            print("[ERROR] 格式錯誤，請輸入數字。")

# 使用向量化運算 (Vectorization)
def Statistics():
    if csv_file.empty:
        print("[ERROR] 無資料可統計。")
        return

    print("[WAIT] 正在計算各縣市診所配發數量...")
    target_cities = list(AREA_DATA.keys())

    # 舊版：使用 for 迴圈逐一篩選各縣市，效率較低
    # 新版：利用 Regex 一次性提取所有匹配的城市名稱並進行計數
    city_pattern = "|".join(target_cities)  # e.g. "臺北市|新北市|..."
    
    # 向量化提取：從 City 欄位提取出符合 target_cities 的內容，並統計次數
    # .str.extract 可以直接利用正則引擎在 C 語言底層運作
    extracted_counts = csv_file["City"].str.extract(f"({city_pattern})")[0].value_counts()
    
    # 使用 reindex 確保所有縣市都出現（即使數量為 0），並轉回 DataFrame
    stats_df = extracted_counts.reindex(target_cities, fill_value=0).reset_index()
    stats_df.columns = ["City", "Count"]

    # 繪圖邏輯維持不變
    font_name = CONFIG["settings"]["font_name"]
    plt.rcParams['font.sans-serif'] = [font_name, 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    
    sns.set_theme(style = "whitegrid", font = font_name)
    plt.figure(figsize = (14, 7))
    chart = sns.barplot(x = "City", y = "Count", data = stats_df, palette = "magma")
    
    for p in chart.patches:
        chart.annotate(format(p.get_height(), '.0f'), 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'center', va = 'center', xytext = (0, 9), 
                       textcoords = 'offset points', fontsize = 10)

    plt.title("中華民國各縣市公費快篩診所數量分布", fontsize = 18, fontweight = 'bold')
    plt.xticks(rotation = 45)
    plt.tight_layout()
    
    output_path = CONFIG["settings"]["output_fig"]
    plt.savefig(output_path, dpi=300)
    print(f"[SUCCESS] 統計圖表已儲存至: {output_path}")
    plt.show()

# 搜尋優化：保持鍊式過濾 (Chained Filtering)
def Inquire(switch):
    if csv_file.empty:
        print("[ERROR] 目前無資料可搜尋。")
        return

    columns = CONFIG["settings"]["search_columns"]
    filters = {}
    
    if switch == 1:
        print("\n[可搜尋欄位]: " + ", ".join([f"({i+1}){col}" for i, col in enumerate(columns)]))
        idx = user_input("請選擇搜尋欄位序號: ", range(1, len(columns) + 1))
        target_col = columns[idx - 1]
        keyword = input(f"請輸入 [{target_col}] 的關鍵字: ").strip()
        
        if keyword: 
            filters[target_col] = keyword
    else:
        print("\n[INFO] 請逐一輸入過濾條件 (直接按 Enter 跳過)")
        for col in columns:
            val = input(f"-> [{col}] 關鍵字: ").strip()
            if val: 
                filters[col] = val

    if not filters:
        print("[INFO] 未輸入關鍵字，取消搜尋。")
        return

    print(f"[WAIT] 正在篩選資料...")
    
    # 向量化過濾：Pandas 的布林索引本身就是向量化操作
    results = csv_file.copy()
    for col, key in filters.items():
        results = results[results[col].str.contains(key, na = False)]
    
    if not results.empty:
        print(f"[SUCCESS] 找到 {len(results)} 筆結果。")
        print("-" * 30)
        print(results.head(15)) 
        print("-" * 30)
    else:
        print("[INFO] 搜尋結束，查無符合結果。")

def main():
    init()

    while True:
        print("\n" + "="*35 + "\n   台灣診所資料分析系統 v2.0-beta\n" + "="*35)
        print("(1) 顯示統計圖表\n(2) 搜尋診所資料\n(3) 退出程式")
        mode = user_input("請選擇模式: ", [1, 2, 3])
        
        if mode == 1: 
            Statistics()
        elif mode == 2:
            sub = user_input("(1)單一搜尋 (2)多重搜尋: ", [1, 2])
            Inquire(sub)
        elif mode == 3: 
            break

    print("\n[INFO] 程式正常結束，感謝使用！")

if __name__ == "__main__":
    main()