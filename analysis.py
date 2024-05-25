"""
    Author  : zong zong
    Connect : zongozngchu0408@gmail.com
    School  : 臺北市立中正高級中學
    GitHub  : https://github.com/zongzong0408/Python-COVID-19-clinic-rapid-screening-reagent-distribution-in-TW
    
	Last edited : 2022/11/07/08:59PM
"""
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt         # invoke picture
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False

import numpy as np 
import pandas as pd                     # handle excel
"""
Series
Frame
"""
import csv                              # handle csv

# import sys
# import codecs
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

"""
    path of file : covid19_free_rapid_antigen_test_clinics.csv
"""
path = "D:\Desktop\Python-COVID-19-clinic-rapid-screening-reagent-distribution-in-TW\covid19_free_rapid_antigen_test_clinics.csv"

csv_file = pd.read_csv(path)
# print(csv_file)  

area_data = {

    '臺北市': [
        '中正區', '大同區', '中山區', '萬華區', '信義區', '松山區', '大安區', '南港區', '北投區', '內湖區', '士林區', '文山區'
    ],
    '新北市': [
        '板橋區', '新莊區', '泰山區', '林口區', '淡水區', '金山區', '八里區', '萬里區', '石門區', '三芝區', '瑞芳區', '汐止區', '平溪區', '貢寮區', '雙溪區', '深坑區', '石碇區', '新店區', '坪林區', '烏來區', '中和區', '永和區', '土城區', '三峽區', '樹林區', '鶯歌區', '三重區', '蘆洲區', '五股區'
    ],
    '基隆市': [
        '仁愛區', '中正區', '信義區', '中山區', '安樂區', '暖暖區', '七堵區'
    ],
    '桃園市': [
        '桃園區', '中壢區', '平鎮區', '八德區', '楊梅區', '蘆竹區', '龜山區', '龍潭區', '大溪區', '大園區', '觀音區', '新屋區', '復興區'
    ],
    '新竹縣': [
        '竹北市', '竹東鎮', '新埔鎮', '關西鎮', '峨眉鄉', '寶山鄉', '北埔鄉', '橫山鄉', '芎林鄉', '湖口鄉', '新豐鄉', '尖石鄉', '五峰鄉'
    ],
    '新竹市': [
        '東區', '北區', '香山區'
    ],
    '苗栗縣': [
        '苗栗市', '通霄鎮', '苑裡鎮', '竹南鎮', '頭份鎮', '後龍鎮', '卓蘭鎮', '西湖鄉', '頭屋鄉', '公館鄉', '銅鑼鄉', '三義鄉', '造橋鄉', '三灣鄉', '南庄鄉', '大湖鄉', '獅潭鄉', '泰安鄉'
    ],
    '臺中市': [
        '中區', '東區', '南區', '西區', '北區', '北屯區', '西屯區', '南屯區', '太平區', '大里區', '霧峰區', '烏日區', '豐原區', '后里區', '東勢區', '石岡區', '新社區', '和平區', '神岡區', '潭子區', '大雅區', '大肚區', '龍井區', '沙鹿區', '梧棲區', '清水區', '大甲區', '外埔區', '大安區'
    ],
    '南投縣': [
        '南投市', '埔里鎮', '草屯鎮', '竹山鎮', '集集鎮', '名間鄉', '鹿谷鄉', '中寮鄉', '魚池鄉', '國姓鄉', '水里鄉', '信義鄉', '仁愛鄉'
    ],
    '彰化縣': [
        '彰化市', '員林鎮', '和美鎮', '鹿港鎮', '溪湖鎮', '二林鎮', '田中鎮', '北斗鎮', '花壇鄉', '芬園鄉', '大村鄉', '永靖鄉', '伸港鄉', '線西鄉', '福興鄉', '秀水鄉', '埔心鄉', '埔鹽鄉', '大城鄉', '芳苑鄉', '竹塘鄉', '社頭鄉', '二水鄉', '田尾鄉', '埤頭鄉', '溪州鄉'
    ],
    '雲林縣': [
        '斗六市', '斗南鎮', '虎尾鎮', '西螺鎮', '土庫鎮', '北港鎮', '莿桐鄉', '林內鄉', '古坑鄉', '大埤鄉', '崙背鄉', '二崙鄉', '麥寮鄉', '臺西鄉', '東勢鄉', '褒忠鄉', '四湖鄉', '口湖鄉', '水林鄉', '元長鄉'
    ],
    '嘉義縣': [
        '太保市', '朴子市', '布袋鎮', '大林鎮', '民雄鄉', '溪口鄉', '新港鄉', '六腳鄉', '東石鄉', '義竹鄉', '鹿草鄉', '水上鄉', '中埔鄉', '竹崎鄉', '梅山鄉', '番路鄉', '大埔鄉', '阿里山鄉'
    ],
    '嘉義市': [
        '東區', '西區'
    ],
    '臺南市': [
        '中西區', '東區', '南區', '北區', '安平區', '安南區', '永康區', '歸仁區', '新化區', '左鎮區', '玉井區', '楠西區', '南化區', '仁德區', '關廟區', '龍崎區', '官田區', '麻豆區', '佳里區', '西港區', '七股區', '將軍區', '學甲區', '北門區', '新營區', '後壁區', '白河區', '東山區', '六甲區', '下營區', '柳營區', '鹽水區', '善化區', '大內區', '山上區', '新市區', '安定區'
    ],
    '高雄市': [
        '楠梓區', '左營區', '鼓山區', '三民區', '鹽埕區', '前金區', '新興區', '苓雅區', '前鎮區', '小港區', '旗津區', '鳳山區', '大寮區', '鳥松區', '林園區', '仁武區', '大樹區', '大社區', '岡山區', '路竹區', '橋頭區', '梓官區', '彌陀區', '永安區', '燕巢區', '田寮區', '阿蓮區', '茄萣區', '湖內區', '旗山區', '美濃區', '內門區', '杉林區', '甲仙區', '六龜區', '茂林區', '桃源區', '那瑪夏區'
    ],
    '屏東縣': [
        '屏東市', '潮州鎮', '東港鎮', '恆春鎮', '萬丹鄉', '長治鄉', '麟洛鄉', '九如鄉', '里港鄉', '鹽埔鄉', '高樹鄉', '萬巒鄉', '內埔鄉', '竹田鄉', '新埤鄉', '枋寮鄉', '新園鄉', '崁頂鄉', '林邊鄉', '南州鄉', '佳冬鄉', '琉球鄉', '車城鄉', '滿州鄉', '枋山鄉', '霧台鄉', '瑪家鄉', '泰武鄉', '來義鄉', '春日鄉', '獅子鄉', '牡丹鄉', '三地門鄉'
    ],
    '宜蘭縣': [
        '宜蘭市', '羅東鎮', '蘇澳鎮', '頭城鎮', '礁溪鄉', '壯圍鄉', '員山鄉', '冬山鄉', '五結鄉', '三星鄉', '大同鄉', '南澳鄉'
    ],
    '花蓮縣': [
        '花蓮市', '鳳林鎮', '玉里鎮', '新城鄉', '吉安鄉', '壽豐鄉', '秀林鄉', '光復鄉', '豐濱鄉', '瑞穗鄉', '萬榮鄉', '富里鄉', '卓溪鄉'
    ],
    '臺東縣': [
        '臺東市', '成功鎮', '關山鎮', '長濱鄉', '海端鄉', '池上鄉', '東河鄉', '鹿野鄉', '延平鄉', '卑南鄉', '金峰鄉', '大武鄉', '達仁鄉', '綠島鄉', '蘭嶼鄉', '太麻里鄉'
    ],
    '澎湖縣': [
        '馬公市', '湖西鄉', '白沙鄉', '西嶼鄉', '望安鄉', '七美鄉'
    ],
    '金門縣': [
        '金城鎮', '金湖鎮', '金沙鎮', '金寧鄉', '烈嶼鄉', '烏坵鄉'
    ],
    '連江縣': [
        '南竿鄉', '北竿鄉', '莒光鄉', '東引鄉'
    ]
}

def mode_choose():

    print("(1) Check Clinic Analysis, (2) Inquire Clinic Information, (3) Exit")
    choose1 = int(input("Which mode would you want to choose ? "))

    if choose1 == 1:
        Statistics()

    elif choose1 == 2:
        print("(1) one kind detail input & output, (2) multiple kind detail input & output")
        choose2 = int(input("Which mode would you want to choose ? "))
        
        if choose2 == 1:
            Inquire(1)

        elif choose2 == 2:
            Inquire(2)

        else:
            print("Error Input!")
            return -1

    elif choose1 == 3:
        return 3

    else:
        print("Error Input!")
        return -1

    
def Inquire(switch):

    Keyword = {
        "City"      : "NULL",
        "Town"      : "NULL",
        "Name"      : "NULL",
        "Address"   : "NULL",
        "Phone"     : "NULL",
        "Long"      : "NULL",
        "Lat"       : "NULL",
    }

    # print("(1) City, (2) Town, (3) Name, (4) Address, (5) Phone, (6) Long, (7) Lat, (8) nothing more to say")
    
    if switch == 1:
        times = 1 
        for line in Keyword:
            print(f"({times}) {line},", end=" ")
            if times == 7:
                print("(8) nothing more to say")
            times += 1

        print("* : Pls enter complete words!")

        kind = input("What kind detail would you want to input ? ")
        detail = input(f"Which {kind} ? ")

        try:
            condition = pd.DataFrame()
            condition = csv_file[kind].str.contains(detail)
        except:
            print("Error Input!")

        print(f"\nSearching Results : \n\n{csv_file[condition]}\n")

    else:
        kind = 0
        while kind != 8:
            times = 1 
            for line in Keyword:
                print(f"({times}) {line},", end=" ")
                if times == 7:
                    print("(8) nothing more to say")
                times += 1

            print("* : Pls enter number!")

            kind = int(input("What kind detail would you want to input ? "))

            if kind == 1:
                detail = input("Which City ? ")
                Keyword["City"] = detail
            elif kind == 2:
                detail = input("Which Town ? ")
                Keyword["Town"] = detail
            elif kind == 3:
                detail = input("Which Name ? ")
                Keyword["Name"] = detail
            elif kind == 4:
                detail = input("Which Address ? ")
                Keyword["Address"] = detail
            elif kind == 5:
                detail = input("Which Phone ? ")
                Keyword["Phone"] = detail
            elif kind == 6:
                detail = input("Which Long ? ")
                Keyword["Long"] = detail
            elif kind == 7:
                detail = input("Which Lat ? ")
                Keyword["Lat"] = detail

    """
    Start Searching
    """
    condition1 = pd.DataFrame()
    condition2 = pd.DataFrame()
    condition3 = pd.DataFrame()

    for line in Keyword:
        if Keyword[line] != "NULL":
            if len(condition1) == 0:                # empty Dataframe
                condition1 = csv_file[line].str.contains(Keyword[line])
            else:
                condition2 = csv_file[line].str.contains(Keyword[line])
                condition3 = condition1 & condition2
                condition1 = condition3

                del(condition2)
                del(condition3)

    if switch != 1:
        print(f"\nSearching Results : \n\n{csv_file[condition1]}\n")

    return 0


def Statistics():
    """
    Start Statistics 
    """   
    town_list = []
    for line in area_data:
        town_list.append(line)

    town_count = {
        "Town"          : ['臺北市', '新北市', '基隆市', '桃園市', '新竹縣', '新竹市', '苗栗縣', '臺中市', '南投縣', '彰化縣', '雲林縣', '嘉義縣', '嘉義市', '臺南市', '高雄市', '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣'],
        "Clinic Count"  : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    # town_count_list = []

    clinic_count = csv_file.shape[0]        # 統計全台共有多少間診所
    # print(f"clinic_count : {clinic_count}")

    statistics = pd.DataFrame(town_count)
    # print(statistics)
    # statistics

    times = 0
    for city in town_list:                  # 統計各市共有多少間診所
        # print(city)
        statistics.at[times, "Clinic Count"] = int(csv_file[csv_file["City"].str.contains(city)].shape[0])
        # print(f"{city} : {town_count[city]}")
        # town_count_list = town_count[city]
        times += 1
    # print(statistics)

    # Xaxis = np.arange(len(town_list))
    # plt.bar(town_list, town_count_list)
    # plt.xlabel("縣市")
    # plt.ylabel("診所數量")
    # plt.title("中華民國縣市診所數量分布")
    # plt.show()

    # chart = statistics.plot(                # 圖表大小
    #     kind    = "bar",                            
    #     title   = "中華民國縣市診所數量分布",       
    #     xlabel  = "縣市",                 
    #     ylabel  = "診所數量",                           
    #     legend  = True,                     # 是否顯示圖例
    #     figsize = (10, 5)
    # )
    # plt.grid(True)
    # # plt.savefig("pandas_chart.png")
    # plt.show()

    chart = sns.barplot(x = "Town", y = "Clinic Count", data = statistics)
    chart.set_title("中華民國縣市診所數量分布")
    print("Show plt")
    plt.show()

def main():
    """
    Start Running 
    """ 
    while True:
        choose = mode_choose()

        if choose == 3:
            break
    
    print("Program End")
    
    return 0


main()
