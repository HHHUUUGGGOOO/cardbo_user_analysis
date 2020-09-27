###########################################################################################################################################################################################################
# 使用者行為分析資料儲存型態
# a. 對於每個 user_id, 紀錄一次的 action 和大功能一點進去的 timestamp 及再次按下一個大功能的 timestamp (大功能為 b. 粗體功能)
# b. 定義一次 action - 大功能及其所有底下的子功能在一次 timestamp 操作完的, 稱作"一次 action", 被放在同一個 action array 的 index 中
    # 1. 呼叫卡伯 > 點選哪個廣告 / 點選哪個熱門搜尋 / 搜尋甚麼關鍵字 / 查到關鍵字而點選哪張信用卡 / 查不到關鍵字而查詢哪個類別
    # 2. 我的信用卡優惠 > 點擊哪張信用卡 / 有優惠而查看哪個信用卡優惠 / 沒優惠而查看其他哪個信用卡 
    # 3. 我的信用卡 > 點選哪個信用卡 / 點選哪個優惠詳細資訊
    # 4. 卡伯小幫手 > 問了甚麼問題
# c. timestamp 和 action 的 index 是對應的, timestamp[0] 的時間點是對應 action[0] 的動作 
# d. timestamp 那邊想要 import time 計算使用時間 (點擊一個大功能到點擊下個大功能的時間差), timestamp 用 array 存 [開始時間, 用了多久 (sec)]
# e. action 用 array 存 [大功能, 子功能_1, 子功能_2, ...]
# f. 可以比較每個 user 的 action 字串和 timestamp 整理出
    # 1. 大功能 : 使用總時間 (對應的 time 全部加總), 可從該使用者花最多時間在哪, 或是點擊甚麼功能次數最多, 來看他 (Ex: "呼叫卡伯 : 913")
    # 2. 大功能下的子功能, 如果有類別, 分析每個使用者最常點哪種類別, 如果是關鍵字搜尋, 可以先建立好一個盡量齊全店名分類到 11 類別, 然後看回歸到使用者最常點哪種類別的問題 (如果用 ML 訓練爬蟲可行 ?)
    # 3. 在周年慶或促銷活動的日期間, 比較每個使用者都點選甚麼功能, 可看出他對促銷有沒有興趣, 再比對該時間區間的搜尋字或子功能, 分析出他可能對甚麼促銷比較感興趣 (Ex: 周年慶在 9/1-9/8, 就去看所有使用者在這七天的行為)
    # 4. 卡伯小幫手的人工回覆可能只能人工統整使用者對於卡伯可能遇到的問題, 似乎分析不出來他的使用者行為
# g. log data : user_id, action, timestamp
# h. convert raw data to : 可能是 json 檔型態呈現
###########################################################################################################################################################################################################