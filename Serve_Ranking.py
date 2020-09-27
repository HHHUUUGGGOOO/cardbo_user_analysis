#####################################################################################################################################################################################
# 熱門功能選單排行 (Serve_Ranking) -
# 定義"功能點擊排行": 分別計算"大功能間"及"子功能在大功能下"的點擊比例 (第b點)
# 定義"搜尋排行1": 計算每項"我的信用卡優惠" 11 項類別的點擊比例 (第d點)
#a. 每日更新一次數據，一份檔案建立一個月的資料庫
    #b. 計算每項功能被點擊的比例 (會先用 figma 等工具做出 user flow(流程圖)，比較各項功能的點擊次數看是否符合我們對使用者行為的預測)，並在 present 資料夾中建立圓餅圖
    #註:計算方式:
        #(1) 大功能比例: 各項子功能的點擊 (細體字) 會被算進大功能 (粗體字) 的點擊次數中，大功能會進行比例計算
        #(2) 子功能比例: 各項子功能也會有在各大功能下的比例計算
    #1. 加卡伯好友 > 點選"查詢商家優惠" > 點選熱門卡片"優惠詳細資訊" / 熱門搜尋關鍵字
    #2. 呼叫卡伯 > 點選"優惠詳細資訊" / 輸入任意關鍵字 / 點選熱門搜尋 > (找到店家)查看熱門搜尋/關鍵字的"優惠詳細資訊" / (找不到店家)點選 11 個類別 > (點選 11 個類別其中之一)點選"查看所有優惠"
    #3. 我的信用卡優惠 > 點選"查看信用卡優惠" > (有優惠)點選"查看所有優惠" 
    #4. 我的信用卡 > 點選"新增信用卡" / "刪除卡片"
    #5. 分享好友 > 選擇好友或群組送出
    #6. 卡伯小幫手 > 輸入任意訊息
    #7. 直接輸入關鍵字 > 查看關鍵字的"優惠詳細資訊"
    #註: 第7點的"直接輸入關鍵字"會被算進第2點的"呼叫卡伯的輸入任意關鍵字"內，輸入任意字都算一次點擊，因為難以分辨它是不小心輸錯還是故意輸入沒意義的話
    #c. 計算每項"我的信用卡優惠" 11 項類別被點擊的比例, 並列出搜尋排行，其中關鍵字搜尋也會被歸類於此
        #網購 / 美食餐廳 / 娛樂 / 藥妝百貨 / 量販超市 / 生活 / 交通 / 旅遊住宿 / 國外 / 繳費 / 其他
    #d. 在搜尋排行會附上每項功能的"比例"及"點擊次數"
    #e. log data : action, value, timestamp
    #f. convert raw data to : 每項大功能及子功能點擊比例排行, 依類別搜尋點擊比例排行, 我的信用卡優惠點擊比例排行
#####################################################################################################################################################################################
import json
import time, datetime
import yaml 
import pathlib # without open file
from ruamel.yaml import YAML # could retend comments in yaml file

func_dict = {}
cate_dict = {}
month_list = []
TotalClick = {}
last_time = ""
# 加卡伯好友
follow_cardbo = {}
# 呼叫卡伯
call_cardbo = {}
search_store = {}
offer_detail = {}
search_category = {}
# 我的信用卡優惠
card_offer = {}
check_card_offer = {}
see_all_offer = {}
# 我的信用卡
settings = {}
add_card = {}
delete_card = {}
search_card = {}
# 分享好友
share_cardbo = {}
# 卡伯小幫手
ask_cardbo_question = {}
# 11 項分類
online_shop, food, leisure, department_store, market, life = {}, {}, {}, {}, {}, {}
transport, travel, abroad, payment, others = {}, {}, {}, {}, {}

def openfile_SR():
    with open('./user_action_log/UserData.json', 'r', encoding='utf-8') as f1:
        file = json.load(f1)
    for i in range(len(file["user"])):
        user_id = file["user"][i]["lineId"]
        action = file["user"][i]["actionName"]
        value = file["user"][i]["actionValue"]
        timestamp = file["user"][i]["time"]["$date"]
        # 分別是 Ryan 和 Brandon 的 user_id
        if (user_id != "U479da6a87ed25efcab3605de091e27de") or (user_id != "U7e6184e094767a9df9ac6c574f83376f"):
            ClickCategory(action, value, timestamp)
        if i % 1000 == 0: print(i)

def addTwoDimDict(dict, key_1, key_2, val_2): # Category Ranking 要加進一筆二維dict資料
    if (key_1 in dict): dict[key_1].update({key_2: val_2})
    else: dict.update({key_1: {key_2: val_2}})

def addThreeDimDict(thedict, key_a, key_b, key_c, val): # Function Ranking 要加進一筆三維dict資料
    if key_a in thedict:
        if key_b in thedict[key_a]:
            thedict[key_a][key_b].update({key_c: val})
        else:
            thedict[key_a].update({key_b: {key_c: val}})
    else:
        thedict.update({key_a: {key_b: {key_c: val}}})

def ClickCategory(action, value, timestamp):
    global TotalClick, month_list, follow_cardbo, call_cardbo, search_store, \
           offer_detail, search_category, card_offer, check_card_offer, see_all_offer, \
           settings, add_card, delete_card, search_card, share_cardbo, ask_cardbo_question, \
           last_time, online_shop, food, leisure, department_store, market, life, \
           transport, travel, abroad, payment, others
    # 若換月份, 則建立檔案並把參數都歸零
    if (timestamp[0:7] not in month_list): 
        month_list.append(timestamp[0:7])
        TotalClick[timestamp[0:7]] = 0
        follow_cardbo[timestamp[0:7]] = 0
        call_cardbo[timestamp[0:7]] = 0
        search_store[timestamp[0:7]] = 0
        offer_detail[timestamp[0:7]] = 0
        search_category[timestamp[0:7]] = 0
        card_offer[timestamp[0:7]] = 0
        check_card_offer[timestamp[0:7]] = 0
        see_all_offer[timestamp[0:7]] = 0
        settings[timestamp[0:7]] = 0
        add_card[timestamp[0:7]] = 0
        delete_card[timestamp[0:7]] = 0
        search_card[timestamp[0:7]] = 0
        share_cardbo[timestamp[0:7]] = 0
        ask_cardbo_question[timestamp[0:7]] = 0
        online_shop[timestamp[0:7]] = 0
        food[timestamp[0:7]] = 0
        leisure[timestamp[0:7]] = 0
        department_store[timestamp[0:7]] = 0
        market[timestamp[0:7]] = 0
        life[timestamp[0:7]] = 0
        transport[timestamp[0:7]] = 0
        travel[timestamp[0:7]] = 0
        abroad[timestamp[0:7]] = 0
        payment[timestamp[0:7]] = 0
        others[timestamp[0:7]] = 0
    # action 點擊數據記錄
    if (action == "follow cardbo"): follow_cardbo[timestamp[0:7]] += 1 #加卡伯好友
    if (action == "call cardbo"): call_cardbo[timestamp[0:7]] += 1 #呼叫卡伯
    if (action == "offer_detail"): 
        offer_detail[timestamp[0:7]] += 1
        call_cardbo[timestamp[0:7]] += 1
    if (action == "search by category when not finding any store"): 
        search_category[timestamp[0:7]] += 1
        call_cardbo[timestamp[0:7]] += 1
        SearchStore(value, timestamp) #進入字串分類
    if (action == "search store"):
        search_store[timestamp[0:7]] += 1
        call_cardbo[timestamp[0:7]] += 1
        SearchStore(value, timestamp) #進入字串分類
    if (action == "my credit card offer"): card_offer[timestamp[0:7]] += 1 #我的信用卡優惠
    if (action == "check card offer"):
        check_card_offer[timestamp[0:7]] += 1
        card_offer[timestamp[0:7]] += 1
    if (action == "see_all_offer"):
        see_all_offer[timestamp[0:7]] += 1
        card_offer[timestamp[0:7]] += 1
    if (action == "go_setting" or action == "no_card_and_go_setting"): settings[timestamp[0:7]] += 1 #我的信用卡
    if (action == "LIFF_user_add_card"):
        add_card[timestamp[0:7]] += 1
        settings[timestamp[0:7]] += 1
    if (action == "LIFF_user_delete_card"):
        delete_card[timestamp[0:7]] += 1
        settings[timestamp[0:7]] += 1
    if (action == "LIFF_user_search_card"):
        search_card[timestamp[0:7]] += 1
        settings[timestamp[0:7]] += 1
    if (action == "share cardbo with friends"): share_cardbo[timestamp[0:7]] += 1 #分享好友
    if (action == "ask cardbo question"): ask_cardbo_question[timestamp[0:7]] += 1 #卡伯小幫手
    TotalClick[timestamp[0:7]] += 1
    last_time = timestamp[0:7]
    #建檔
    Func2Json(last_time)
    Cate2Json(last_time)


def SearchStore(value, timestamp):
    global online_shop, food, leisure, department_store, market, life, \
           transport, travel, abroad, payment, others
    # search by category when not finding any store 而進入11項分類
    if (value == "online_shop"): online_shop[timestamp[0:7]] += 1
    if (value == "food"): food[timestamp[0:7]] += 1
    if (value == "leisure"): leisure[timestamp[0:7]] += 1
    if (value == "department_store"): department_store[timestamp[0:7]] += 1
    if (value == "market"): market[timestamp[0:7]] += 1
    if (value == "life"): life[timestamp[0:7]] += 1
    if (value == "transport"): transport[timestamp[0:7]] += 1
    if (value == "abroad"): abroad[timestamp[0:7]] += 1
    if (value == "travel"): travel[timestamp[0:7]] += 1
    if (value == "payment"): payment[timestamp[0:7]] += 1
    if (value == "others"): others[timestamp[0:7]] += 1
    # 關鍵字搜尋 (字串分類)


def Func2Json(filename): #功能建檔-Function
    global func_dict, TotalClick, month_list, follow_cardbo, call_cardbo, search_store, \
           offer_detail, search_category, card_offer, check_card_offer, see_all_offer, \
           settings, add_card, delete_card, search_card, share_cardbo, ask_cardbo_question
    divide = 0 
    # 總點擊次數-1D
    func_dict["總點擊次數"] = TotalClick[filename]
    # 加卡伯好友-2D
    addTwoDimDict(func_dict, "加入卡伯", "點擊次數", follow_cardbo[filename])
    addTwoDimDict(func_dict, "加入卡伯", "點擊比例", round(follow_cardbo[filename]/TotalClick[filename], 2))
    # 呼叫卡伯-3D
    addTwoDimDict(func_dict, "呼叫卡伯", "點擊次數", call_cardbo[filename])
    addTwoDimDict(func_dict, "呼叫卡伯", "點擊比例", round(call_cardbo[filename]/TotalClick[filename], 2))
    addThreeDimDict(func_dict, "呼叫卡伯", "呼叫卡伯介面", "點擊次數", (call_cardbo[filename]-search_store[filename]-offer_detail[filename]-search_category[filename]))
    if (call_cardbo[filename] == 0): divide = 0
    else: divide = (call_cardbo[filename]-search_store[filename]-offer_detail[filename]-search_category[filename])/call_cardbo[filename]
    addThreeDimDict(func_dict, "呼叫卡伯", "呼叫卡伯介面", "點擊比例", round(divide, 2))
    addThreeDimDict(func_dict, "呼叫卡伯", "關鍵字搜尋", "點擊次數", search_store[filename])
    if (call_cardbo[filename] == 0): divide = 0
    else: divide = search_store[filename]/call_cardbo[filename]
    addThreeDimDict(func_dict, "呼叫卡伯", "關鍵字搜尋", "點擊比例", round(divide, 2))
    addThreeDimDict(func_dict, "呼叫卡伯", "優惠詳細資訊", "點擊次數", offer_detail[filename])
    if (call_cardbo[filename] == 0): divide = 0
    else: divide = offer_detail[filename]/call_cardbo[filename]
    addThreeDimDict(func_dict, "呼叫卡伯", "優惠詳細資訊", "點擊比例", round(divide, 2))
    addThreeDimDict(func_dict, "呼叫卡伯", "搜尋類別", "點擊次數", search_category[filename])
    if (call_cardbo[filename] == 0): divide = 0
    else: divide = search_category[filename]/call_cardbo[filename]
    addThreeDimDict(func_dict, "呼叫卡伯", "搜尋類別", "點擊比例", round(divide, 2))
    # 我的信用卡優惠-3D
    addTwoDimDict(func_dict, "我的信用卡優惠", "點擊次數", card_offer[filename])
    addTwoDimDict(func_dict, "我的信用卡優惠", "點擊比例", round(card_offer[filename]/TotalClick[filename], 2))
    addThreeDimDict(func_dict, "我的信用卡優惠", "我的信用卡優惠介面", "點擊次數", (card_offer[filename]-check_card_offer[filename]-see_all_offer[filename]))
    if (card_offer[filename] == 0): divide = 0
    else: divide = (card_offer[filename]-check_card_offer[filename]-see_all_offer[filename])/card_offer[filename]
    addThreeDimDict(func_dict, "我的信用卡優惠", "我的信用卡優惠介面", "點擊比例", round(divide, 2))
    addThreeDimDict(func_dict, "我的信用卡優惠", "查看信用卡優惠", "點擊次數", check_card_offer[filename])
    if (card_offer[filename] == 0): divide = 0
    else: divide = check_card_offer[filename]/card_offer[filename]
    addThreeDimDict(func_dict, "我的信用卡優惠", "查看信用卡優惠", "點擊比例", round(divide, 2))
    addThreeDimDict(func_dict, "我的信用卡優惠", "查看所有優惠", "點擊次數", see_all_offer[filename])
    if (card_offer[filename] == 0): divide = 0
    else: divide = see_all_offer[filename]/card_offer[filename]
    addThreeDimDict(func_dict, "我的信用卡優惠", "查看所有優惠", "點擊比例", round(divide, 2))
    # 我的信用卡-3D
    addTwoDimDict(func_dict, "我的信用卡", "點擊次數", settings[filename])
    addTwoDimDict(func_dict, "我的信用卡", "點擊比例", round(settings[filename]/TotalClick[filename], 2))
    addThreeDimDict(func_dict, "我的信用卡", "前往設定介面", "點擊次數", (settings[filename]-add_card[filename]-delete_card[filename]-search_card[filename]))
    if (settings[filename] == 0): divide = 0
    else: divide = (settings[filename]-add_card[filename]-delete_card[filename]-search_card[filename])/settings[filename]
    addThreeDimDict(func_dict, "我的信用卡", "前往設定介面", "點擊比例", round(divide, 2))
    addThreeDimDict(func_dict, "我的信用卡", "使用者新增卡片", "點擊次數", add_card[filename])
    if (settings[filename] == 0): divide = 0
    else: divide = add_card[filename]/settings[filename]
    addThreeDimDict(func_dict, "我的信用卡", "使用者新增卡片", "點擊比例", round(divide, 2))
    addThreeDimDict(func_dict, "我的信用卡", "使用者刪除卡片", "點擊次數", delete_card[filename])
    if (settings[filename] == 0): divide = 0
    else: divide = delete_card[filename]/settings[filename]
    addThreeDimDict(func_dict, "我的信用卡", "使用者刪除卡片", "點擊比例", round(divide, 2))
    addThreeDimDict(func_dict, "我的信用卡", "使用者搜尋卡片", "點擊次數", search_card[filename])
    if (settings[filename] == 0): divide = 0
    else: divide = search_card[filename]/settings[filename]
    addThreeDimDict(func_dict, "我的信用卡", "使用者搜尋卡片", "點擊比例", round(divide, 2))
    # 分享好友-2D
    addTwoDimDict(func_dict, "分享好友", "點擊次數", share_cardbo[filename])
    addTwoDimDict(func_dict, "分享好友", "點擊比例", round(share_cardbo[filename]/TotalClick[filename], 2))
    # 卡伯小幫手-2D
    addTwoDimDict(func_dict, "卡伯小幫手", "點擊次數", ask_cardbo_question[filename])
    addTwoDimDict(func_dict, "卡伯小幫手", "點擊比例", round(ask_cardbo_question[filename]/TotalClick[filename], 2))
    # 建檔
    file = './user_action_log/Serve_Ranking/Function/%s.json' % filename
    with open(file, 'w', encoding='utf-8') as f: json.dump(func_dict, f, ensure_ascii=False, indent=4, separators=(',', ': '))


def Cate2Json(filename): #類別建檔-Category
    global cate_dict, online_shop, food, leisure, department_store, market, life, \
           transport, travel, abroad, payment, others, search_store, search_category
    # 總點擊次數
    cate_dict["總點擊次數"] = search_category[filename] + search_store[filename]
    s = search_store[filename] + search_category[filename]
    if (s == 0):
        a, b, c, d, e, f, g, h, i, j, k = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    else: 
        a, b, c, d, e = online_shop[filename]/s, food[filename]/s, leisure[filename]/s, department_store[filename]/s, market[filename]/s
        f, g, h, i, j, k = life[filename]/s, transport[filename]/s, travel[filename]/s, abroad[filename]/s, payment[filename]/s, others[filename]/s
    # 網購-a
    addTwoDimDict(cate_dict, "網購", "點擊次數", online_shop[filename])
    addTwoDimDict(cate_dict, "網購", "點擊比例", round(a, 2))
    # 美食餐廳-b 
    addTwoDimDict(cate_dict, "美食餐廳", "點擊次數", food[filename])
    addTwoDimDict(cate_dict, "美食餐廳", "點擊比例", round(b, 2))
    # 娛樂-c
    addTwoDimDict(cate_dict, "娛樂", "點擊次數", leisure[filename])
    addTwoDimDict(cate_dict, "娛樂", "點擊比例", round(c, 2))
    # 藥妝百貨-d
    addTwoDimDict(cate_dict, "藥妝百貨", "點擊次數", department_store[filename])
    addTwoDimDict(cate_dict, "藥妝百貨", "點擊比例", round(d, 2))
    # 量販超市-e
    addTwoDimDict(cate_dict, "量販超市", "點擊次數", market[filename])
    addTwoDimDict(cate_dict, "量販超市", "點擊比例", round(e, 2))
    # 生活-f
    addTwoDimDict(cate_dict, "生活", "點擊次數", life[filename])
    addTwoDimDict(cate_dict, "生活", "點擊比例", round(f, 2))
    # 交通-g
    addTwoDimDict(cate_dict, "交通", "點擊次數", transport[filename])
    addTwoDimDict(cate_dict, "交通", "點擊比例", round(g, 2))
    # 旅遊住宿-h
    addTwoDimDict(cate_dict, "旅遊住宿", "點擊次數", travel[filename])
    addTwoDimDict(cate_dict, "旅遊住宿", "點擊比例", round(h, 2))
    # 國外-i
    addTwoDimDict(cate_dict, "國外", "點擊次數", abroad[filename])
    addTwoDimDict(cate_dict, "國外", "點擊比例", round(i, 2))
    # 繳費-j
    addTwoDimDict(cate_dict, "繳費", "點擊次數", payment[filename])
    addTwoDimDict(cate_dict, "繳費", "點擊比例", round(j, 2))
    # 其他-k
    addTwoDimDict(cate_dict, "其他", "點擊次數", others[filename])
    addTwoDimDict(cate_dict, "其他", "點擊比例", round(k, 2))
    # 建檔
    file = './user_action_log/Serve_Ranking/Category/%s.json' % filename
    with open(file, 'w', encoding='utf-8') as f: json.dump(cate_dict, f, ensure_ascii=False, indent=4, separators=(',', ': '))



openfile_SR()

# 2020-09
#ClickCategory("call cardbo", "new user", "2020-09-08 10:20")
#ClickCategory("LIFF_user_add_card", "<card_1>", "2020-09-08 18:13")
#ClickCategory("LIFF_user_search_card", "<card_2>", "2020-09-09 00:20")
#ClickCategory("search store", "food", "2020-09-09 11:20")
#ClickCategory("search store", "online_shop", "2020-09-09 12:20")
#ClickCategory("offer detail", "<0>*<card_3>", "2020-09-10 14:50")
# 2020-10
#ClickCategory("search store", "life", "2020-10-09 09:20")
#ClickCategory("follow cardbo", "", "2020-10-10 14:50")
# 2020-02
#ClickCategory("follow cardbo", "", "2020-02-01 14:50")
# 2021-02
#ClickCategory("go_setting", "", "2021-02-14 14:50")

