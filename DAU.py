#####################################################################################################################################################################################
# DAU - 
# 定義1: 單日 LINEBOT 功能被操作的總次數 (單日流量)
# 定義2: 單日 LINEBOT 不同使用者使用的人數 (單日人數)
#a. 不限制點擊次數，點擊一次就算一次 "總點擊次數"
#b. 要記錄每天共有多少"不同的使用者使用"，即為 DAU
#c. 定義何謂一次操作 : (詳細字串參看後端的 user action list 定義)
    #1. 加卡伯好友 > 點選"查詢商家優惠" > 點選熱門卡片"優惠詳細資訊" / 熱門搜尋關鍵字
    #2. 呼叫卡伯 > 點選"優惠詳細資訊" / 輸入任意關鍵字 / 點選熱門搜尋 > (找到店家)查看熱門搜尋/關鍵字的"優惠詳細資訊" / (找不到店家)點選 11 個類別 > (點選 11 個類別其中之一)點選"查看所有優惠"
    #3. 我的信用卡優惠 > 點選"查看信用卡優惠" > (有優惠)點選"查看所有優惠" 
    #4. 我的信用卡 > 點選"新增信用卡" / "刪除卡片"
    #5. 分享好友 > 選擇好友或群組送出
    #6. 卡伯小幫手 > 輸入任意訊息
    #7. 直接輸入關鍵字 > 查看關鍵字的"優惠詳細資訊"
#d. log data : user_id, action, timestamp 
#e. convert raw data to : 觸發至少一次操作的點擊次數
#####################################################################################################################################################################################
import json
from datetime import datetime
import yaml 
import pathlib # without open file
from ruamel.yaml import YAML # could retend comments in yaml file

myDAUdict = {} # (key : value) will be like ('2020-09-07' : 130 )
now = datetime.now()
list_act = ["call cardbo", "my credit card offer", "check card offer", "search store", "see more", \
            "see another", "search by category when not finding any store", \
            "turn back to main richmenu", "follow cardbo", "offer detail", "see_all_offer", \
            "no_card_and_go_setting", "go_setting", "LIFF_user_add_card", "LIFF_user_delete_card", \
            "LIFF_user_search_card", "share cardbo with friends", "ask cardbo question"] # 每次action加進click一次
list_not = ["unfollow cardbo"] # 不算一次操作的action
filenamelist = []
clicklist = []
userlist = []
MAUuserlist = []
monthlist = []
DAU_dict = {}
usernum_dict = {}
MAU_dict = {}

def openfile_DAU():
    with open('./user_action_log/UserData.json', 'r', encoding='utf-8') as f1:
        file = json.load(f1)
    for i in range(len(file["user"])):
        user_id = file["user"][i]["lineId"]
        action = file["user"][i]["actionName"]
        timestamp = file["user"][i]["time"]["$date"]
        # 分別是 Ryan 和 Brandon 的 user_id
        if (user_id != "U479da6a87ed25efcab3605de091e27de") or (user_id != "U7e6184e094767a9df9ac6c574f83376f"):
            ClickOnce(user_id, action, timestamp)
        if i % 1000 == 0: print(i)

def addTwoDimDict(dict, key_1, key_2, val_2): # DAU 要加進一筆二維dict資料
    if (key_1 in dict): dict[key_1].update({key_2: val_2})
    else: dict.update({key_1: {key_2: val_2}})

def ClickOnce(user_id, action, timestamp):
    global myDAUdict, clicklist, userlist, MAUuserlist, monthlist, DAU_dict, usernum_dict, MAU_dict
    try:
        if action in list_act: 
            month = timestamp[0:7]
            # 更新數據
            time_key = timestamp[0:10] # timestamp, 如: "2020-08-14T07:21:15.827Z"
            UsageClick = timestamp[0:10] + "_Click"
            if time_key not in clicklist: 
                clicklist.append(time_key)
                DAU_dict[UsageClick] = 0
                UsageClick = timestamp[0:10] + "_Click"
                usernum_dict[UsageClick] = 0
            if month not in monthlist: 
                monthlist.append(month)
                MAU_dict[timestamp[0:7]] = 0
            if user_id not in userlist: # 每日不同登入的使用者，隔日刪掉
                userlist.append(user_id)
                usernum_dict[UsageClick] += 1
            if (action == "search store"): 
                if user_id not in MAUuserlist: # 每個月不同登入的使用者，隔月刪掉
                    MAUuserlist.append(user_id)
                    MAU_dict[timestamp[0:7]] += 1
            DAU_dict[UsageClick] += 1
            # 建檔
            MAU_month = month + "'s search store MAU"
            myDAUdict[MAU_month] = MAU_dict[timestamp[0:7]]
            addTwoDimDict(myDAUdict, time_key, "Total click times", DAU_dict[UsageClick])
            addTwoDimDict(myDAUdict, time_key, "Daily different users", usernum_dict[UsageClick])
    except: 
        print("Please log correct action name.") 
    else: 
        DAUData2Json(myDAUdict)

def DAUData2Json(DAU_list):
    global now, filenamelist
    for key in DAU_list:
        file_name = key[0:7] # write to a Json file, file name = 2020-09.json
        if file_name not in filenamelist: filenamelist.append(file_name)
    for name in filenamelist:
        file = './user_action_log/DAU/%s.json' % name
        add_DAU = {}
        for date in DAU_list:
            if (date[0:7] == name):
                add_DAU[date] = DAU_list[date]
                with open(file, 'w', encoding='utf-8') as f: json.dump(add_DAU, f, indent=4, sort_keys=True, separators=(',', ': '))


openfile_DAU()
#ClickOnce("User_1", "call cardbo", "2020-09-08 10:20")
#ClickOnce("User_2", "LIFF_user_add_card", "2020-09-08 18:13")
#ClickOnce("User_3", "LIFF_user_search_card", "2020-09-09 00:20")
#ClickOnce("User_4", "offer detail", "2020-09-10 14:50")
#ClickOnce("User_5", "follow cardbo", "2020-10-10 14:50")
#ClickOnce("User_6", "follow cardbo", "2020-02-01 14:50")
#ClickOnce("User_7", "go_setting", "2021-02-14 14:50")
#ClickOnce("User_3", "search store", "2020-09-09 11:20")
#ClickOnce("User_3", "search store", "2020-09-09 12:20")
#ClickOnce("User_3", "search store", "2020-10-09 09:20")
