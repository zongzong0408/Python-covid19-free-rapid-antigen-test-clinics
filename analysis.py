# -*- coding: utf-8 -*-
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich import print as rprint

console = Console()

CONFIG_PATH = "./config.json"
CONFIG      = {}
AREA_DATA   = {}
csv_file    = pd.DataFrame()

def init():
    
    global CONFIG, AREA_DATA, csv_file
    
    console.print("[bold blue][INFO][/bold blue] 正在初始化系統資源...", style="dim")
    
    if not os.path.exists(CONFIG_PATH):
        console.print(f"[bold red][ERROR][/bold red] 找不到設定檔: {CONFIG_PATH}")
        return
        
    with open(CONFIG_PATH, "r", encoding = "utf-8") as file:
        CONFIG = json.load(file)
    
    AREA_DATA = CONFIG.get("area_data", {})
    data_path = CONFIG["settings"]["data_path"]
    
    if os.path.exists(data_path):
        csv_file = pd.read_csv(data_path, encoding = "utf-8")
        console.print(f"[bold green][SUCCESS][/bold green] 系統初始化完成，已載入: [underline]{data_path}[/underline]")
    else:
        console.print(f"[bold red][ERROR][/bold red] 找不到資料檔案: {data_path}")

def user_input(prompt, valid_options = None, input_type = int):
    
    while True:
        try:
            if input_type == int:
                user_val = IntPrompt.ask(f"\n{prompt}")
            else:
                user_val = Prompt.ask(f"\n{prompt}")
            
            if valid_options and user_val not in valid_options:
                console.print(f"[bold yellow][警告][/bold yellow] 請輸入範圍內的選項: {list(valid_options)}")
                continue
            return user_val
    
        except Exception:
            console.print("[bold red][錯誤][/bold red] 格式錯誤，請重新輸入。")

def Statistics():
    
    if csv_file.empty:
        console.print("[bold red][ERROR][/bold red] 無資料可統計。")
        return

    with console.status("[bold green]正在執行向量化運算..."):
        target_cities = list(AREA_DATA.keys())
        if not target_cities:
            console.print("[bold red]錯誤：config.json 中沒有定義縣市資料。[/bold red]")
            return
            
        city_pattern = "|".join(target_cities)

        extracted_counts = csv_file["City"].astype(str).str.extract(f"({city_pattern})")[0].value_counts()
        stats_df = extracted_counts.reindex(target_cities, fill_value=0).reset_index()
        stats_df.columns = ["City", "Count"]

    font_name = CONFIG["settings"]["font_name"]
    plt.rcParams['font.sans-serif'] = [font_name, 'Arial Unicode MS', 'sans-serif']
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
    console.print(f"[bold green][SUCCESS][/bold green] 統計圖表已儲存至: [cyan]{output_path}[/cyan]")
    plt.show()

def Inquire(switch):
    
    if csv_file.empty:
        console.print("[bold red][ERROR][/bold red] 目前無資料可搜尋。")
        return

    columns = CONFIG["settings"]["search_columns"]
    filters = {}
    
    if switch == 1:
        console.print("\n[bold cyan]─── 單一搜尋模式 ───[/bold cyan]")
    
        for i, col in enumerate(columns):
            console.print(f"[bold yellow]({i+1})[/bold yellow] {col}", end="  ")
    
        idx = user_input("請選擇搜尋欄位序號", range(1, len(columns) + 1))
        target_col = columns[idx - 1]
        keyword = Prompt.ask(f"請輸入 [bold green][{target_col}][/bold green] 的關鍵字").strip()
    
        if keyword: filters[target_col] = keyword
    
    else:
        console.print("\n[bold cyan]─── 多重過濾模式 ───[/bold cyan] (直接按 Enter 跳過)")
    
        for col in columns:
            val = Prompt.ask(f"-> [[{col}]] 關鍵字", default="").strip()
            if val: filters[col] = val

    if not filters:
        console.print("[dim]未輸入關鍵字，取消搜尋。[/dim]")
        return

    with console.status("[bold blue]正在篩選資料..."):
        results = csv_file.copy()
    
        for col, key in filters.items():
            results = results[results[col].astype(str).str.contains(key, na = False)]
    
    if not results.empty:
        table = Table(title=f"\n[bold green]搜尋結果 (共 {len(results)} 筆)[/bold green]", header_style="bold magenta")
    
        for col in columns:
            table.add_column(col)

        for _, row in results.head(15).iterrows():
            table.add_row(*(str(row[c]) for c in columns))
        
        console.print(table)
        if len(results) > 15:
            console.print("[dim]* 僅顯示前 15 筆結果...[/dim]")
    else:
        console.print("[bold yellow]查無符合結果。[/bold yellow]")

def main():
    
    init()
    
    while True:
    
        console.print("\n")
        console.print(Panel.fit(
            "[bold cyan]台灣公費快篩配發診所分析工具 v2[/bold cyan]\n[dim]說明[/dim]",
            border_style="bright_blue"
        ))
    
        rprint("[bold yellow](1)[/bold yellow] 顯示統計圖表")
        rprint("[bold yellow](2)[/bold yellow] 搜尋診所資料")
        rprint("[bold yellow](3)[/bold yellow] [red]退出程式[/red]")
    
        mode = user_input("請選擇模式", [1, 2, 3])
    
        if mode == 1: 
            Statistics()
        
        elif mode == 2:
            sub = user_input("(1)單一搜尋 (2)多重搜尋", [1, 2])
            Inquire(sub)
        
        elif mode == 3: break
    
    console.print("\n[bold green][INFO][/bold green] 程式正常結束，感謝使用！")

if __name__ == "__main__":
    main()