####################################################################################################################################
#                                                           import                                                                 # 
####################################################################################################################################
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

####################################################################################################################################
#                                                          parameter                                                               #
####################################################################################################################################
data_head = []  # 這裡要保證有序，可以用有序字典，映射的时候可以用dict
WAU_list, head_list = [], []
data_str, file_type, WAU_date = "", "", ""
data_head_dict, WAU_head_dict = {}, {}
row_now = 0

####################################################################################################################################
#                                                        help function                                                             #
####################################################################################################################################
# parsing WAU filename, input "2020-09" ,output "2020-09-17_2020-09-23"...
def get_WAU_fname(file):
    global WAU_list
    #path = os.path.abspath(os.path.join(os.getcwd(), ".."))
    path = os.getcwd()
    path_wau = path + "/user_action_log/WAU"
    list = os.listdir(path_wau)
    for name in list:
        if (name[0:7] == file): WAU_list.append(name)

# parsing WAU head (input: "呼叫卡伯_總使用次數" --> output: WAU_head_dict={ "呼叫卡伯_總使用次數": [呼叫卡伯, 總使用次數] })
def get_WAU_head(str):
    global WAU_head_dict, WAU_date
    count = 0
    head_front, head_end = "", ""
    if(str[0:3] == "WAU"):
        head_front = str 
        head_end = ""
        WAU_head_dict[head_front] = [head_front, head_end]
    else:
        for i in range(len(str)):
            if (str[i] != '_') and (count == 0): head_front += str[i]
            elif (count == 1): head_end += str[i]
            elif (str[i] == '_'): count = 1
        WAU_head_dict[str] = [head_front, head_end]
    
####################################################################################################################################
#                                                        main function                                                             #
####################################################################################################################################
# read json.file wau/2020-09-17-2020-09-23.
def open_jsonfile(filename):
    global data_str, file_type, WAU_date
    # 判斷檔案類別為 DAU / MAU / Serve_Ranking
    for i in range(len(filename)):
        if (filename[0:13] == "Serve_Ranking"): 
            # Function / Category
            if (filename[14] == 'F'): file_type = "Function"
            if (filename[14] == 'C'): file_type = "Category"
            break
        # WAU 用檔名做 file_type
        elif (filename[0:3] == "WAU"): 
            file_type = "WAU_" + filename[4:25]
            WAU_date = filename[4:25]
        elif (filename[i] != '/') and (filename[0:13] != "Serve_Ranking"): file_type += filename[i]
        else: break
    # 開始讀檔
    with open('./user_action_log/%s'%filename, 'r', encoding='utf-8') as file_in:
        data_str = file_in.read()
        # 替換元素
        data_str = data_str.replace('true','True')
        data_str = data_str.replace('false','False')
        data_str = data_str.replace('null','None')
        data_str = data_str.replace('\n','')

# type函數: 判斷當前的string屬於哪個類型
def query_type(data):
    for ch in data:
        if ch == '{':
            return "dict"
        if ch == '[':
            return "list"
    return "value"

# head函數: 將json所有key作為head 
def get_json_head(data, loc=""):
    global data_head, WAU_head_dict, file_type, WAU_date
    # 將數據轉成string
    data = str(data)  
    # 分類
    data_type = query_type(data)
    # 如果是元素
    if data_type == "value": 
        if (file_type[0:3] == "WAU"):
            temp = ""
            if (loc[1:] == "WAU"): temp = "WAU_" + WAU_date
            else: temp = loc[1:]
            get_WAU_head(temp)
            data_head.append(temp)
        else:
            if loc[1:] not in data_head:
                data_head.append(loc[1:])
        return
    # 如果是字典
    if data_type == "dict":  
        data_dict = eval(data)
        for key in data_dict:
            # DAU 檔案只記錄 "Daily different users" 的部分
            if (file_type == "DAU") and ("search store MAU" not in key) and ("Total click times" not in key):
                get_json_head(data_dict[key], loc + "_" + key)
            # MAU 檔案只記錄 "Monthly search store's different users" 的部分
            if (file_type == "MAU") and ("Duration" not in key) and ("Monthly Activated Usage" not in key):
                get_json_head(data_dict[key], loc + "_" + key)
            # Serve_Ranking (Function) 檔案只記錄 "總點擊次數" 及 "各點擊比例" 的部分
            if (file_type == "Function") and ("呼叫卡伯介面" not in key) and ("關鍵字搜尋" not in key) and \
                ("優惠詳細資訊" not in key) and ("搜尋類別" not in key) and ("我的信用卡優惠介面" not in key) \
                and ("查看信用卡優惠" not in key) and ("查看所有優惠" not in key) and ("前往設定介面" not in key) \
                and ("使用者新增卡片" not in key) and ("使用者刪除卡片" not in key) and ("使用者搜尋卡片" not in key):
                get_json_head(data_dict[key], loc + "_" + key)
            # Serve_Ranking (Category) 檔案只記錄 "總點擊次數" 及 "各點擊次數" 的部分
            if (file_type == "Category") and ("總點擊次數" not in key) and ("點擊比例" not in key):
                get_json_head(data_dict[key], loc + "_" + key)
            # WAU 檔案只記錄 "WAU", "呼叫卡伯(總使用次數/總使用人數/使用者佔比)", "電商搜尋數據"
            if (file_type[0:3] == "WAU") and ("呼叫卡伯搜尋字串" not in key) and ("台灣十大電商搜尋字串" not in key) \
                and ("其他搜尋字串" not in key):
                get_json_head(data_dict[key], loc + "_" + key)
        return
    # 如果是列表
    if data_type == "list":  
        data_list = list(eval(data))
        for item in data_list:
            get_json_head(item, loc)
        return

def get_json_body():
    global data_head_dict, data_head
    for head in data_head:
        #print(head)
        tmp = []
        for i in range(len(data_head)):
            tmp.append("")
        data_head_dict[head] = tmp

# 將value內容存入
def get_json_table(data, loc="", rows=0):
    global row_now, file_type, WAU_date
    # 將數據轉成string
    data = str(data)  
    # 分類
    data_type = query_type(data)
    # 如果是元素
    if data_type == "value":  
        key = ""
        if (loc[1:] == "WAU"): key = "WAU_" + WAU_date
        else: key = loc[1:]
        #print(data)
        data_head_dict[key][rows] = data 
        return
    # 如果是字典
    if data_type == "dict":  
        data_dict = eval(data)
        for key in data_dict:
            # DAU 檔案只記錄 "Daily different users" 的部分
            if (file_type == "DAU") and ("search store MAU" not in key) and ("Total click times" not in key):
                # 輸出value的位置和key相差幾列, rows=0 (default), 在excel中相當於key的下一列
                rows = 0
                get_json_table(data_dict[key], loc + "_" + key, rows)
            # MAU 檔案只記錄 "Monthly search store's different users" 的部分
            if (file_type == "MAU") and ("Duration" not in key) and ("Monthly Activated Usage" not in key):
                rows = 0
                get_json_table(data_dict[key], loc + "_" + key, rows)
            # Serve_Ranking (Function) 檔案只記錄 "總點擊次數" 及 "各點擊比例" 的部分
            if (file_type == "Function") and ("呼叫卡伯介面" not in key) and ("關鍵字搜尋" not in key) and \
                ("優惠詳細資訊" not in key) and ("搜尋類別" not in key) and ("我的信用卡優惠介面" not in key) \
                and ("查看信用卡優惠" not in key) and ("查看所有優惠" not in key) and ("前往設定介面" not in key) \
                and ("使用者新增卡片" not in key) and ("使用者刪除卡片" not in key) and ("使用者搜尋卡片" not in key):
                rows = 0
                get_json_table(data_dict[key], loc + "_" + key)
            # Serve_Ranking (Category) 檔案只記錄 "總點擊次數" 及 "各點擊次數" 的部分
            if (file_type == "Category") and ("總點擊次數" not in key) and ("點擊比例" not in key):
                rows = 0
                get_json_table(data_dict[key], loc + "_" + key)
            # WAU 檔案只記錄 "WAU", "呼叫卡伯(總使用次數/總使用人數/使用者佔比)", "電商搜尋數據"
            if (file_type[0:3] == "WAU") and ("呼叫卡伯搜尋字串" not in key) and ("台灣十大電商搜尋字串" not in key) \
                and ("其他搜尋字串" not in key):
                rows = 0
                get_json_table(data_dict[key], loc + "_" + key)
        return
    # 如果是列表
    if data_type == "list":  
        data_list = list(eval(data))
        for i in range(len(data_list)):
            if i > 0:
                row_now += 1
            get_json_table(data_list[i], loc, row_now)
        return

# 輸出csv檔
def Write2csv(f, f_type):
    global head_list, WAU_date
    with open('./user_action_log/csv_monthly/%s.csv'%f, 'a',encoding="utf-8-sig") as file_out:
        # 輸出key的位置, 初始為excel第1列, 若要增加一列就換行一次
        if (f_type == "DAU"): file_out.write("DAU\n")
        if (f_type == "MAU"): 
            for i in range(2): file_out.write('\n')
            file_out.write("MAU\n")
        if (f_type == "Function"): 
            for i in range(2): file_out.write('\n')
            file_out.write("Serve Ranking (Function)\n")
        if (f_type == "Category"): 
            for i in range(2): file_out.write('\n')
            file_out.write("Serve Ranking (Category)\n")
        if (f_type[0:3] == "WAU"): 
            for i in range(2): file_out.write('\n')
            # 只有剛輸入WAU資料時才會印這行
            #file_out.write(f_type)
        #file_out.write("\n")
        # 標題
        if (f_type[0:3] == "WAU"):
            for head in data_head[:-1]:
                first = WAU_head_dict[head][0]
                if (first in head_list):
                    file_out.write("")
                    file_out.write(",")  # 逗号分隔
                if (first not in head_list):
                    head_list.append(first)
                    file_out.write(first)
                    file_out.write(",")  # 逗号分隔
            file_out.write("" + "\n")  # 最后一个换行
            for subhead in data_head[:-1]:
                second = WAU_head_dict[subhead][1]
                file_out.write(second)
                file_out.write(",")  # 逗号分隔
            file_out.write(data_head[-1] + "\n")  # 最后一个换行
        if (f_type[0:3] != "WAU"):
            for head in data_head[:-1]:
                file_out.write(head)
                file_out.write(",")  # 逗号分隔
            file_out.write(data_head[-1] + "\n")  # 最后一个换行
        # 數值
        for i in range(len(data_head)):
            for head in data_head[:-1]:
                #print(data_head_dict[head][i])
                file_out.write(data_head_dict[head][i])
                file_out.write(",")
            last_key = data_head[-1]  # 取最后一个head
            file_out.write(data_head_dict[last_key][i])

# 執行所有檔案
def main_run(f):
    global data_str, file_type, data_head, data_str, data_head_dict, row_now, \
           WAU_list, WAU_head_dict, WAU_date, head_list
    ############## DAU ##############
    open_jsonfile('DAU/%s.json'%f)
    get_json_head(data_str)
    get_json_body()
    get_json_table(data_str)
    Write2csv(f, file_type)
    # 結束後將 file_type 清空
    data_head = []  
    data_str, file_type = "", ""
    data_head_dict = {}
    row_now = 0
    
    ############## MAU ##############
    open_jsonfile('MAU/%s.json'%f)
    get_json_head(data_str)
    get_json_body()
    get_json_table(data_str)
    Write2csv(f, file_type)
    # 結束後將 file_type 清空
    data_head = []  
    data_str, file_type = "", ""
    data_head_dict = {}
    row_now = 0

    ############## Serve Ranking (Function) ##############
    open_jsonfile('Serve_Ranking/Function/%s.json'%f)
    get_json_head(data_str)
    get_json_body()
    get_json_table(data_str)
    Write2csv(f, file_type)
    # 結束後將 file_type 清空
    data_head = []  
    data_str, file_type = "", ""
    data_head_dict = {}
    row_now = 0
    
    ############## Serve Ranking (Category) ##############
    open_jsonfile('Serve_Ranking/Category/%s.json'%f)
    get_json_head(data_str)
    get_json_body()
    get_json_table(data_str)
    Write2csv(f, file_type)
    # 結束後將 file_type 清空
    data_head = []  
    data_str, file_type = "", ""
    data_head_dict = {}
    row_now = 0
    
    ############## WAU ##############
    get_WAU_fname(f)
    for i in range(len(WAU_list)):
        # WAU_list[i] = "2020-10-05_2020-10-12.json"
        open_jsonfile('WAU/%s'%WAU_list[i])
        get_json_head(data_str)
        get_json_body()
        get_json_table(data_str)
        Write2csv(f, file_type)
        data_head, head_list = [], []
    # 結束後將 file_type 清空
    data_head, head_list = [], []
    data_str, file_type = "", ""
    data_head_dict = {}
    row_now = 0
    
####################################################################################################################################
#                                                              main                                                                #
####################################################################################################################################
#if __name__=="__main__":
    #main_run("2020-10")