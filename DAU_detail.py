###########################################################################################
# 1. 看一天內的user有多少人 (DAU_datail)
# 2. 這群人中有使用"呼叫卡伯 or search store"的又有多少人?比例?
# 3. 這些"search store"中搜尋字是"電商"的又有多少, list & 各佔比 (如: 蝦皮, pchome, 生活市集等)
###########################################################################################

####################################################################################################################################
#                                                           import                                                                 # 
####################################################################################################################################
import json
import datetime
import yaml 
import pathlib # without open file
from ruamel.yaml import YAML # could retend comments in yaml file

####################################################################################################################################
#                                                          parameter                                                               #
####################################################################################################################################
DAU, top_ten_ecommerce = 0, 0
cc, cc_user = 0, 0 #call cardbo
day_list, user_list, ccuser_list, e_commerce_list, other_list = [], [], [], [], []
DAU_dict = {}
pchome, momo, shopee, yahoo, sensen, udn, rakuten, books, pinkoi, lifemarket, yummy = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
start_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
list_act = ["call cardbo", "my credit card offer", "check card offer", "search store", "see more", \
            "see another", "search by category when not finding any store", \
            "turn back to main richmenu", "follow cardbo", "offer detail", "see_all_offer", \
            "no_card_and_go_setting", "go_setting", "LIFF_user_add_card", "LIFF_user_delete_card", \
            "LIFF_user_search_card", "share cardbo with friends", "ask cardbo question"] #每次action加進click一次
list_not = ["unfollow cardbo"] #不算一次操作的action

####################################################################################################################################
#                                                        help function                                                             #
####################################################################################################################################
def addTwoDimDict(dict, key_1, key_2, val_2): # DAU 要加進一筆二維dict資料
    if (key_1 in dict): dict[key_1].update({key_2: val_2})
    else: dict.update({key_1: {key_2: val_2}})

####################################################################################################################################
#                                                        main function                                                             #
####################################################################################################################################
def openfile_DAU_detail(filename):
    with open('./user_action_log/UserData/json_data/UserData_0928.json', 'r', encoding='utf-8') as f1:
        file = json.load(f1)
    for i in range(len(file["user"])):
        user_id = file["user"][i]["lineId"]
        action = file["user"][i]["actionName"]
        value = file["user"][i]["actionValue"]
        timestamp = file["user"][i]["time"]["$date"]
        # 分別是 Ryan 和 Brandon 的 user_id
        if (user_id != "U479da6a87ed25efcab3605de091e27de") or (user_id != "U7e6184e094767a9df9ac6c574f83376f"):
            DAUCalculate(user_id, action, value, timestamp)
        if i % 1000 == 0: print(i)

def DAUCalculate(user_id, action, value, timestamp):
    global DAU, day_list, start_date, list_act, list_not, user_list, cc, cc_user, ccuser_list, \
           pchome, momo, shopee, yahoo, sensen, udn, rakuten, books, pinkoi, lifemarket, yummy, \
           top_ten_ecommerce, DAU_dict, e_commerce_list, other_list
    percent_ccuser = 0
    # mark=1 代表在十大電商中, mark=0 為 default, 表不在十大電商中
    mark = 0 
    for i in range(1):
        start = (datetime.date.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        day_list.append(start)
    if timestamp[0:10] in day_list:
        # 一天內不同的user共有多少人
        if (user_id not in user_list): 
            DAU += 1 
            user_list.append(user_id)
        if (action == "call cardbo") or (action == "search store"):
            # 呼叫卡伯總使用次數
            cc += 1 
            if (user_id not in ccuser_list):
                # 有多少人使用呼叫卡伯
                cc_user += 1 
                ccuser_list.append(user_id)
        if (DAU != 0): percent_ccuser = cc_user/DAU
        if (DAU == 0): percent_ccuser = 0
        # DAU
        DAU_dict["DAU"] = DAU
        # 呼叫卡伯+關鍵字搜尋使用次數/人數/比例
        addTwoDimDict(DAU_dict, "呼叫卡伯", "總使用次數", cc)
        addTwoDimDict(DAU_dict, "呼叫卡伯", "總使用人數", cc_user)
        addTwoDimDict(DAU_dict, "呼叫卡伯", "使用者佔比", round(percent_ccuser, 2))
        # 比對搜尋字串
        addTwoDimDict(DAU_dict, "呼叫卡伯搜尋字串", "台灣十大電商搜尋字串", e_commerce_list)
        addTwoDimDict(DAU_dict, "呼叫卡伯搜尋字串", "其他搜尋字串", other_list)
        # 電商判斷
        if ("pchome" in value.lower()) or ("pc home" in value.lower()): 
            pchome += 1
            top_ten_ecommerce += 1
            mark = 1
        if ("momo" in value.lower()): 
            momo += 1
            top_ten_ecommerce += 1
            mark = 1
        if ("shopee" in value.lower()) or ("蝦皮" in value): 
            shopee += 1
            top_ten_ecommerce += 1
            mark = 1
        if ("yahoo" in value.lower()) or ("雅虎" in value):
            yahoo += 1
            top_ten_ecommerce += 1
            mark = 1
        if ("森森" in value):
            sensen += 1
            top_ten_ecommerce += 1
            mark = 1
        if ("udn" in value.lower()):
            udn += 1
            top_ten_ecommerce += 1
            mark = 1
        if ("rakuten" in value.lower()) or ("樂天" in value):
            rakuten += 1
            top_ten_ecommerce += 1
            mark = 1
        if ("博客來" in value): 
            books += 1
            top_ten_ecommerce += 1
            mark = 1
        if ("pinkoi" in value.lower()):
            pinkoi += 1
            top_ten_ecommerce += 1
            mark = 1
        if ("生活市集" in value):
            lifemarket += 1
            top_ten_ecommerce += 1
            mark = 1
        if ("好吃" in value):
            yummy += 1
            top_ten_ecommerce += 1
            mark = 1
        # 字串分類
        '''
        if (mark == 0) and (action == "search store"): 
            other_list.append(value)
            addTwoDimDict(DAU_dict, "呼叫卡伯搜尋字串", "其他搜尋字串", other_list)
        if (mark == 1): 
            e_commerce_list.append(value)
            addTwoDimDict(DAU_dict, "呼叫卡伯搜尋字串", "台灣十大電商搜尋字串", e_commerce_list)
        '''
        # 電商搜尋數據
        addTwoDimDict(DAU_dict, "電商搜尋數據", "台灣十大電商搜尋次數", top_ten_ecommerce)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "PChome", pchome)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "momo", momo)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "蝦皮購物", shopee)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "Yahoo", yahoo)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "森森", sensen)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "udn", udn)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "樂天", rakuten)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "博客來", books)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "Pinkoi", pinkoi)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "生活市集", lifemarket)
        addTwoDimDict(DAU_dict, "電商搜尋數據", "好吃宅配", yummy)

def DAUData2Json(dict):
    global start_date, DAU_dict
    filename = start_date 
    file = './user_action_log/DAU/DAU_detail/%s.json' % filename
    with open(file, 'w', encoding='utf-8') as f: json.dump(DAU_dict, f, ensure_ascii=False, indent=4, separators=(',', ': '))
    
def CleanCache_DAU():
    global day_list, user_list, ccuser_list, e_commerce_list, other_list, DAU_dict
    day_list.clear()
    user_list.clear()
    ccuser_list.clear()
    e_commerce_list.clear()
    other_list.clear()
    DAU_dict.clear()

####################################################################################################################################
#                                                              main                                                                #
####################################################################################################################################
#if __name__=="__main__":
    # 每週日更新一次資料
    #if (datetime.date.today().weekday() == 6):
        #openfile_DAU_detail('filename')
        #DAUData2Json(DAU_dict)


#openfile 的檔案
