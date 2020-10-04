############################################################################################################################################################################################################
# 用戶留存率 - 
# 定義(1) must do: 記錄每個使用者"加入卡伯"的時間，並統計在兩週後這些使用者的留存率
# 定義(2) optional: 篩選一個時間看該段時間加入卡伯的使用者留存率是否較高
#a. 在 must do 中，個別記錄每個使用者的"line_id" / "加入卡伯的時間" / "log in date"，每日更新Retention Rate數據，從每個使用者加入卡伯的那天各自加上兩週時間，分三種情況 :
    #註: 會建一份檔 (user_data.json) 將使用者被記錄的資料全部存取
    #註: Retention Rate 計算公式 = (人數(user_RR=1)) / (人數(user_RR=1)+人數(user_RR=-1))
    #註: Warning提醒 : 業界定義衰退風險值為 0.2, 若連續一週低於 0.2 表此 APP 可能逐漸被用戶淘汰，可藉由比值觀察使用者不是因為新鮮而使用, 是為了實用而用
    #註: 承上: 所以若連續一週的Retention Rate都低於 0.2，會在終端機上跳出警告提醒，哪段時間的留存率都低於 0.2，低於0.2的日期也會在檔案中將那幾天的數據標上警告提醒
    #1. 還在兩週內的觀察期 > user_RR=0，不列入數據計算
    #2. 該使用者在兩週後(Ex: 9/15)的"三天內"仍有登入使用過 > user_RR=1，並以兩週到期的時間為基準(Ex: 9/15)，重新判斷再兩週後是否仍留存
    #3. 該使用者在兩週後的"三天內"沒有登入使用過 > user_RR=-1，若他之後有重新操作，user_RR 直接變回 1
#b. 在 optional 中，可以讓使用者自由設定"想觀察哪段時間加入卡伯的使用者是否留存率比較高"及"要觀察多久時間作為留存依據"
    #註: 在 config.yml 中，會提供以下兩個變數給使用者更改
    #1. 篩選時間 : start_date / end_date
    #2. period 長度 : period (單位=day)
    #3. 檔名 : filename (像是想要特別比較"國慶連假"，這份 json 可以叫做 "國慶連假20201010_202010-12")
    #註: 是否留存的判斷依據同 mustdo 的部分
    #1. 還在 period 內的觀察期 > user_RR=0，不列入數據計算
    #2. 該使用者在 period 後(Ex: 9/15)的"三天內"仍有登入使用過 > user_RR=1，並以兩週到期的時間為基準(Ex: 9/15)，重新判斷再兩週後是否仍留存
    #3. 該使用者在 period 後的"三天內"沒有登入使用過 > user_RR=-1，並將該使用者從 user_list 名單中刪除，之後就不再計算他的資料 
#c. log data : user_id, action, timestamp
#d. convert raw data to : 用戶留存率
############################################################################################################################################################################################################
import json
import time, datetime
import yaml 
import pathlib # without open file
from ruamel.yaml import YAML # could retend comments in yaml file

user_list = []
date_dict = {}
user_dict = {}
follow_date = {}
RR = 0 #Retention Rate
RR_one = 0 #para=1的人數
RR_ne_one = 0 #para=-1的人數
count = 0
now = datetime.date.today()
#config.yml 
yaml = YAML()
ori_file = pathlib.Path('config.yml')
doc = yaml.load(ori_file)

def openfile():
    with open('./user_action_log/Retention_Rate/user_data.json', 'r', encoding='utf-8') as f1:
        file_1 = json.load(f1)
    IsRetention(file_1)

def addTwoDimDict(dict, key_1, key_2, val_2): # Retention Rate 要加進一筆二維dict資料
    if (key_1 in dict): dict[key_1].update({key_2: val_2})
    else: dict.update({key_1: {key_2: val_2}})

def InputUserData(line_id, action, timestamp): # 輸入使用者資料，並將其存到 user_data.json
    global user_list, user_dict, RR_ne_one, RR_one, RR, date_dict, follow_date
    #period=(兩週又三天) ; para=使用者的參數為 0/1/-1
    period = 17
    #退追的使用者
    if action == "unfollow cardbo": 
        user_list.remove(line_id)
        del user_dict[line_id]
    else: 
        #新增的使用者
        if line_id not in user_list: 
            yy, mm, dd = int(timestamp[0:4]), int(timestamp[5:7]), int(timestamp[8:10])
            addTwoDimDict(follow_date, line_id, "yy", yy)
            addTwoDimDict(follow_date, line_id, "mm", mm)
            addTwoDimDict(follow_date, line_id, "dd", dd)
            #加入 follow cardbo date
            addTwoDimDict(user_dict, line_id, "follow cardbo date", timestamp[0:10])
            #加入 after period
            after_period = datetime.datetime(yy, mm, dd) + datetime.timedelta(days=period)
            ap_str = after_period.strftime('%Y-%m-%d')
            addTwoDimDict(user_dict, line_id, "after period date", ap_str)
            #加入 log in date
            addTwoDimDict(user_dict, line_id, "log in date", [])
            if timestamp[0:10] not in user_dict[line_id]["log in date"]: 
                user_dict[line_id]["log in date"].append(timestamp[0:10])
            #加入參數 0/1/-1
            addTwoDimDict(user_dict, line_id, "parameter", 0)
            user_list.append(line_id)
            #如果parameter=-1的使用者之後有回鍋，parameter直接變1，user list 被刪掉
            if (user_dict[line_id]["parameter"] == -1): 
                user_dict[line_id]["parameter"] = 1
                RR_ne_one -= 1
                RR_one += 1
        else: 
            yy_2, mm_2, dd_2 = int(timestamp[0:4]), int(timestamp[5:7]), int(timestamp[8:10])
            #找出第一天使用是哪天
            if (yy_2 <= follow_date[line_id]["yy"]) and (mm_2 <= follow_date[line_id]["mm"]) and (dd_2 <= follow_date[line_id]["dd"]):
                follow_date[line_id]["yy"] = yy_2
                follow_date[line_id]["mm"] = mm_2
                follow_date[line_id]["dd"] = dd_2
                user_dict[line_id]["follow cardbo date"] = timestamp[0:10]
                after_period = datetime.datetime(yy_2, mm_2, dd_2) + datetime.timedelta(days=period)
                ap_str = after_period.strftime('%Y-%m-%d')
                user_dict[line_id]["after period date"] = ap_str
            user_dict[line_id]["log in date"].append(timestamp[0:10])
    file = './user_action_log/Retention_Rate/user_data.json'
    with open(file, 'w', encoding='utf-8') as f: json.dump(user_dict, f, indent=4, separators=(',', ': '))

def IsRetention(file): # 每日更新就好，在 user_analysis.py 呼叫
    global user_list, user_dict, now, RR_one, RR_ne_one, RR
    #調整user parameter = 0/1/-1
    now_str = now.strftime('%Y-%m-%d') # Day17
    y, m, d = int(now_str[0:4]), int(now_str[5:7]), int(now_str[8:10])
    date = datetime.datetime(y, m, d)
    for line_id in file:
        u_p = user_dict[line_id]["after period date"] # user_period
        u_l = user_dict[line_id]["log in date"] # user_log_in_date
        b1_time = date - datetime.timedelta(days=1) # Day16, before_1
        b2_time = date - datetime.timedelta(days=2) # Day15, before_2
        b3_time = date - datetime.timedelta(days=3) # Day14, before_3
        b1, b2, b3 = b1_time.strftime('%Y-%m-%d'), b2_time.strftime('%Y-%m-%d'), b3_time.strftime('%Y-%m-%d')
        #當天日期超過 after period date 才能比較
        if (int(now_str[0:4])>=int(u_p[0:4])) and (int(now_str[5:7])>=int(u_p[5:7])) and (int(now_str[8:10])>=int(u_p[8:10])):
            if (b1 in u_l) or (b2 in u_l) or (b3 in u_l): 
                user_dict[line_id]["parameter"] = 1
                RR_one += 1
            else: 
                user_dict[line_id]["parameter"] = -1
                RR_ne_one += 1
    file = './user_action_log/Retention_Rate/user_data.json'
    with open(file, 'w', encoding='utf-8') as f: json.dump(user_dict, f, indent=4, separators=(',', ': '))

def Calculate_RR(): # 每日更新就好，在 user_analysis.py 呼叫
    global user_list, user_dict, now, RR_one, RR_ne_one, RR, date_dict, count
    RR = (RR_one)/(RR_one+RR_ne_one)
    #因為都是隔天統計前一天的數據
    yesterday = now - datetime.timedelta(days=1)
    y_str = yesterday.strftime('%Y-%m-%d')
    Warn = doc["Retention_Rate"]["warning"]
    if (RR < Warn): 
        count += 1
        addTwoDimDict(date_dict, y_str, "Warning", "The Retention Rate is below 0.2")
    if (RR >= Warn): addTwoDimDict(date_dict, y_str, "Warning", "")
    if (count >= 7) and (RR >= Warn): count = 0
    if (count >= 7): print("The Retention Rate is somehow low for at least 7 days")
    addTwoDimDict(date_dict, y_str, "Retention Rate", RR)
    filename = './user_action_log/Retention_Rate/%s.json' % y_str[0:7]
    with open(filename, 'w', encoding='utf-8') as f: json.dump(date_dict, f, indent=4, separators=(',', ': '))
    


InputUserData("User_3", "search store", "2020-10-19 09:20")
InputUserData("User_1", "call cardbo", "2020-09-08 10:20")
InputUserData("User_2", "LIFF_user_add_card", "2020-09-08 18:13")
InputUserData("User_3", "LIFF_user_search_card", "2020-09-03 00:20")
InputUserData("User_4", "offer detail", "2020-09-10 14:50")
InputUserData("User_5", "follow cardbo", "2020-10-10 14:50")
InputUserData("User_6", "follow cardbo", "2020-02-01 14:50")
InputUserData("User_7", "go_setting", "2021-02-14 14:50")
InputUserData("User_3", "search store", "2020-09-06 11:20")
InputUserData("User_3", "search store", "2020-09-19 12:20")
InputUserData("User_5", "unfollow cardbo", "2020-10-11 14:50")
InputUserData("User_5", "follow cardbo", "2020-10-11 14:50")
InputUserData("User_5", "search store", "2020-10-27 14:50")

'''
today = datetime.datetime(2020, 2, 13) + datetime.timedelta(days=17)
after = today.strftime('%Y-%m-%d')
print(after[0:4])
print(type(after))

s = "123-03-13"
print(int(s[0:3]))
print(int(s[4:6]))
print(int(s[7:9]))
'''
openfile()
Calculate_RR()