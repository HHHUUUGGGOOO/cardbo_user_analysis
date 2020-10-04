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

####################################################################################################################################
#                                                           import                                                                 # 
####################################################################################################################################
import json
from datetime import datetime
import yaml 
import pathlib # without open file
from ruamel.yaml import YAML # could retend comments in yaml file

####################################################################################################################################
#                                                          parameter                                                               #
####################################################################################################################################
myDAUdict = {} # (key : value) will be like ('2020-09-07' : 130 )
DAU_dict, usernum_dict, MAU_dict = {}, {}, {}
filenamelist, clicklist, userlist, MAUuserlist, monthlist = [], [], [], [], []
list_act = ["call cardbo", "my credit card offer", "check card offer", "search store", "see more", \
            "see another", "search by category when not finding any store", \
            "turn back to main richmenu", "follow cardbo", "offer detail", "see_all_offer", \
            "no_card_and_go_setting", "go_setting", "LIFF_user_add_card", "LIFF_user_delete_card", \
            "LIFF_user_search_card", "share cardbo with friends", "ask cardbo question"] # 每次action加進click一次
list_not = ["unfollow cardbo"] # 不算一次操作的action

####################################################################################################################################
#                                                        help function                                                             #
####################################################################################################################################
def addTwoDimDict(dict, key_1, key_2, val_2): # DAU 要加進一筆二維dict資料
    if (key_1 in dict): dict[key_1].update({key_2: val_2})
    else: dict.update({key_1: {key_2: val_2}})

####################################################################################################################################
#                                                        main function                                                             #
####################################################################################################################################
def openfile_DAU(fname):
    with open('./user_action_log/UserData/json_data/%s'%fname, 'r', encoding='utf-8') as f1:
        file = json.load(f1)
    for i in range(len(file["user"])):
        user_id = file["user"][i]["lineId"]
        action = file["user"][i]["actionName"]
        timestamp = file["user"][i]["time"]["$date"]
        # 分別是 Ryan 和 Brandon 的 user_id
        if (user_id != "U479da6a87ed25efcab3605de091e27de") or (user_id != "U7e6184e094767a9df9ac6c574f83376f"):
            ClickOnce(user_id, action, timestamp)
        # 檢查是否有在執行
        if i % 1000 == 0: 
            text = "DAU: " + str(i)
            print(text)

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

def CleanCache_DAU():
    global myDAUdict, DAU_dict, usernum_dict, MAU_dict, filenamelist, clicklist, userlist, MAUuserlist, monthlist
    filenamelist.clear()
    clicklist.clear()
    userlist.clear()
    MAUuserlist.clear()
    monthlist.clear()
    DAU_dict.clear()
    usernum_dict.clear()
    MAU_dict.clear()
    myDAUdict.clear()

####################################################################################################################################
#                                                              main                                                                #
####################################################################################################################################
#if __name__=="__main__":
    #now = datetime.now()
    # 每天的 0:00 更新一次資料
    #if (now.hour == 0) and (now.minute == 0):
        #openfile_DAU('filename')
        #DAUData2Json(myDAUdict)


# openfile_DAU 吃進的 file 怎麼和 exe 檔連結