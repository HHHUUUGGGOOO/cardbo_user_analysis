########################################################################################
# MAU -
# 定義1: 一個月內, LINEBOT 功能被操作的總次數 (單月流量)
# 定義2: 一個月內，關鍵字搜尋 (search store) 被多少不同使用者使用 (單月人數)
#a. 統計日從每月的一號到最後一號
#b. 每月結束統計一次
#c. 資料包含 : "統計時間" / "單月總點擊次數" / "單月共多少不同使用者使用關鍵字搜尋功能 (MAU)"
#d. log data : DAU 的 json file
#e. convert raw data to : MAU
########################################################################################
import datetime
import json
import yaml # import yaml
import pathlib # without open file
from ruamel.yaml import YAML # could retend comments in yaml file

MAU = 0
Users = 0
filename = ""
now = datetime.datetime.now()
yearlist = []
datadict = {} # (key : value) will be like ( "2020-09": {"點擊次數": 1450, "統計時間": "09/01-09/30"} )
monthlist = []
month = ""
start_date = ""
end_date = ""
store_MAU = ""


def openfile():
    for mon in ["2020-09"]:
        with open('./user_action_log/DAU/%s.json'%mon, 'r', encoding='utf-8') as f1:
            file_1 = json.load(f1)
        MAUData2Json(file_1)

def isLeapYear(year): # 統計時間需要判斷2月當年最後一天是幾號
    yy = eval(year)
    if (yy % 4 == 0):
        if (yy % 100 == 0):
            if (yy % 400 == 0):
                return 1 #閏年
            else: return 0
        else: return 1 #閏年
    else: return 0

def addTwoDimDict(dict, key_1, key_2, val_2): # MAU 要加進一筆二維dict資料
    if (key_1 in dict): dict[key_1].update({key_2: val_2})
    else: dict.update({key_1: {key_2: val_2}})

def MAUData2Json(file): # 吃進的file裡面都是同個月份的日期，如: 2020-09.json
    global MAU, Users, filename, now, yearlist, datadict, monthlist, month, start_date, end_date, store_MAU
    count = 0
    for date in file:
        filename = date[0:4] # 2020
        month = date[0:7]
        end = ""
        store_MAU = month + "'s search store MAU"
        Users = file[store_MAU]
        if (count == 0): start_date = date[0:7] + "-01" # 2020-09-01
        if filename not in yearlist: yearlist.append(filename)
        if month not in monthlist: monthlist.append(month) # 2020-09
        if (count == len(file)-1):
            if (date[5:7] in ["01", "03", "05", "07", "08", "10", "12"]): end = "31"
            elif (date[5:7] in ["04", "06", "09", "11"]): end = "30"
            elif (date[5:7] in ["02"]): 
                if (isLeapYear(date[0:4]) == 1): end = "29"
                else: end = "28"
            end_date = date[0:7] + '-' + end # 2020-09-30
        if (type(file[date]) == dict):
            MAU += file[date]["Total click times"]
        count += 1
    duration = start_date + " ~ " + end_date
    for name in yearlist:
        file = './user_action_log/MAU/%s.json' % name
        addTwoDimDict(datadict, month, "Monthly search store's different users", Users)
        addTwoDimDict(datadict, month, "Monthly Activated Usage", MAU)
        addTwoDimDict(datadict, month, "Duration", duration)
        add_MAU = {}
        for key in datadict:
            if (key[0:4] == name):
                add_MAU[key] = datadict[key]
                with open(file, 'w', encoding='utf-8') as f: json.dump(add_MAU, f, indent=4, sort_keys=True, separators=(',', ': '))
    MAU = 0

openfile()