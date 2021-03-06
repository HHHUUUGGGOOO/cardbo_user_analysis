# 卡伯 LINE bot 使用者行為數據定義
> update date Y200827
### Useraction collection
**collection name:** useractions 
```jsonld
{
    lineid: "<string>",
    action: "<string>",
    value: "<string>",
    timestamp: "<string>"
}
```
**example:**
```jsonld
{
    lineid: "U1cdef6b4343c79712172aa8dd4a8ea93",
    action: "callCard",
    value: "彰化銀行 MASTERCARD鈦金卡",
    timestamp: "2020-08-14T07:21:15.827Z"
}
```
## 後台追蹤數據 (從 v3 的功能出發)
**參考資料** 
    APP營運數據分析 : https://reurl.cc/D6ZzrE / https://reurl.cc/Z7r7jl
    如何從數據去塑造使用者行為 : https://reurl.cc/e86bMj / https://reurl.cc/WLkYW9
    數據分析架構 : https://reurl.cc/EzpNWm


### 活躍用戶指標 
    1. 活躍用戶是衡量應用用戶規模的指標，通常，一個產品是否成功，如果只看一個指標，那麼這個這指標一定是活躍用戶數。

- **<font color=blue>DAU</font> - 
<font color=red>定義1: 單日 LINEBOT 功能被操作的總次數 (單日流量)
定義2: 單日 LINEBOT 不同使用者使用的人數 (單日人數)</font>**
 
    >a. 不限制點擊次數，點擊一次就算一次 "**總點擊次數**"
    >b. 要記錄每天共有多少"**不同的使用者使用**"，即為 **DAU**
    >c. 定義何謂一次操作 : (**詳細字串參看後端的 user action list 定義**)
    >>1. **加卡伯好友** > 點選"查詢商家優惠" > 點選熱門卡片"優惠詳細資訊" / 熱門搜尋關鍵字
    >>2. **呼叫卡伯** > 點選"優惠詳細資訊" / 輸入任意關鍵字 / 點選熱門搜尋 > (找到店家)查看熱門搜尋/關鍵字的"優惠詳細資訊" / (找不到店家)點選 11 個類別 > (點選 11 個類別其中之一)點選"查看所有優惠"
    >>3. **我的信用卡優惠** > 點選"查看信用卡優惠" > (有優惠)點選"查看所有優惠" 
    >>4. **我的信用卡** > 點選"新增信用卡" / "刪除卡片"
    >>5. **分享好友** > 選擇好友或群組送出
    >>6. **卡伯小幫手** > 輸入任意訊息
    >>7. **直接輸入關鍵字** > 查看關鍵字的"優惠詳細資訊"
    >
    >d. **log data : user_id, action, timestamp** 
    >e. **convert raw data to : 觸發至少一次操作的點擊次數**
```json=
# DAU 的 json 檔只存"數字"，檔名為"yyyy-mm.json", 內容包含: 使用"關鍵字搜尋"的MAU統計 (一個月內共多少不同使用者使用這個卡伯核心功能) / 每日數據 (含"總點擊次數"和"DAU")
# 為了方便 MAU 抓資料，會多一個 dict={"yyyy-mm's search store MAU": integer}，因為"search store"是卡伯的核心
Ex: 2020-09.json
{
    "2020-09's search store MAU": 12,
    "2020-09-01": { "Daily different users": 2, "Total click times": 2 },
    "2020-09-02": { "Daily different users": 1, "Total click times": 4 },
    ...
}       
# 每天只要在半夜12點後定期更新數據一次就好，json 檔一定會有，如果有使用者想要觀看特定時間的數據 (Ex: 9/7~9/14)，只要更改 config.yml 的時間起始就好，會在終端機擷取資料印出來
# 若輸入時間沒有資料 (像是想查看明天數據)，要有提醒訊息在終端機印出
```
- **<font color=blue>MAU</font> - 
<font color=red>定義1: 一個月內, LINEBOT 功能被操作的總次數 (單月流量)
定義2: 一個月內，關鍵字搜尋 (search store) 被多少不同使用者使用 (單月人數)</font>**

    >a. 統計日從每月的一號到最後一號
    >b. 每月結束統計一次
    >c. 資料包含 : "**統計時間**" / "**單月總點擊次數**" / "**單月共多少不同使用者使用關鍵字搜尋功能 (MAU)**"
    >d. **log data : DAU 的 json file**
    >e. **convert raw data to : MAU**
```json=
# MAU 的 json 檔存"數字"和"統計時間"，檔名為"yyyy.json"，內容為 dict{"yyyy-mm": { "使用search store的總人數": MAU, "總點擊次數": click, "統計時間": "yyyy-mm-dd ~ yyyy-mm-dd"} }
Ex: 2020.json, 今天為2020-11-01
{
    ...,
    "2020-02": { Duration": "2020-02-01 ~ 2020-02-29", "Monthly Activated Usage": 101, "Monthly search store's different users": 78 },
    ...,
    "2020-09": { Duration": "2020-09-01 ~ 2020-09-30", "Monthly Activated Usage": 154, "Monthly search store's different users": 100 }
}
```
### 用戶留存率指標
    1. 用戶留存率是指在某一統計時段內的新增用戶數中再經過一段時間後仍啟動該應用的用戶比例。
    
    2. 用戶留存率可重點關注次日、7日、14日以及30日留存率。
    
    3. 次日留存率即某一統計時段新增用戶在第二天再次啟動應用的比例；7日留存率即某一統計時段新增用戶數在第7天再次啟動該應用的比例；14日和30日留存率以此類推。

    4. 用戶留存率是驗證產品用戶吸引力很重要的指標。

- **<font color=blue>用戶留存率 (Retention Rate)</font> -**
**<font color=red>定義(1) must do: 記錄每個使用者"加入卡伯"的時間，並統計在兩週後這些使用者的留存率**
**定義(2) optional: 篩選一個時間看該段時間加入卡伯的使用者留存率是否較高</font>**

    >a. 在 **must do** 中，個別記錄**每個使用者的"line_id" / "加入卡伯的時間" / "log in date"**，每日更新Retention Rate數據，從每個使用者加入卡伯的那天各自加上兩週時間，分三種情況 :
    >>註: 會建一份檔 (**user_data.json**) 將使用者被記錄的資料全部存取
    >>註: **Retention Rate 計算公式 = (人數(user_RR=1)) / (人數(user_RR=1)+人數(user_RR=-1))**
    >>註: **Warning提醒** : **業界定義衰退風險值為 0.2**, 若連續一週低於 0.2 表此 APP 可能逐漸被用戶淘汰，可藉由比值觀察使用者不是因為新鮮而使用, 是為了實用而用
    >>註: 承上: 所以若連續一週的Retention Rate都低於 0.2，會**在終端機上跳出警告提醒**，哪段時間的留存率都低於 0.2，低於0.2的日期也會**在檔案中將那幾天的數據標上警告提醒**，如果數字為零不會提醒，可能是因為初始還沒什麼統計量 (**現在我先不加上提醒系統，因為第一次分析不確定0.2是否適用於卡伯，先觀察一陣子的數據再自己定義數值**)
    >>1. 還在兩週內的觀察期 > **user_RR=0**，不列入數據計算
    >>2. 該使用者在兩週後(Ex: 9/15)的"**三天內**"仍有登入使用過 > **user_RR=1**，並以兩週到期的時間為基準(Ex: 9/15)，重新判斷再兩週後是否仍留存
    >>3. 該使用者在兩週後的"**三天內**"沒有登入使用過 > **user_RR=-1**，若他之後有重新操作，user_RR 直接變回 1
    >
    >b. 在 **optional** 中，可以讓使用者自由設定"**想觀察哪段時間加入卡伯的使用者是否留存率比較高**"及"**要觀察多久時間作為留存依據**"
    >>**註: 在 config.yml 中，會提供以下兩個變數給使用者更改**
    >>1. **篩選時間** : start_date / end_date
    >>2. **period 長度** : period (單位=day)
    >>3. **檔名** : filename (像是想要特別比較"國慶連假"，這份 json 可以叫做 "國慶連假20201010_202010-12")
    >>4. **警告** : warning (自行調整多少值以下需要跳警告)
    >>
    >>**註: 是否留存的判斷依據同 mustdo 的部分**
    >>1. 還在 period 內的觀察期 > **user_RR=0**，不列入數據計算
    >>2. 該使用者在 period 後(Ex: 9/15)的"**三天內**"仍有登入使用過 > **user_RR=1**，並以兩週到期的時間為基準(Ex: 9/15)，重新判斷再兩週後是否仍留存
    >>3. 該使用者在 period 後的"**三天內**"沒有登入使用過 > **user_RR=-1**，並將該使用者從 user_list 名單中刪除，之後就不再計算他的資料 
    >
    >c. **log data : user_id, action, timestamp**
    >d. **convert raw data to : 用戶留存率**
```json=
[must do: 將使用者被記錄的資料存成"user_data.json"]
# 檔名為 user_data.json
# 記錄五項資料: "user_id", "加入卡伯的日期", "log in 的日期", "period 到期的日期是幾號", "user參數為0/1/-1"
Ex: user_data.json
{
    "user_id_1": { 
                    follow cardbo date: "2020-09-15", 
                    after period date: "2020-09-29",
                    parameter: 0
                    log in date: ["2020-09-15", "2020-09-18",...] 
                 }
    "user_id_2": { 
                    follow cardbo date: "2020-09-16", 
                    after period date: "2020-09-30",
                    parameter: 0
                    log in date: ["2020-09-16", "2020-09-19",...] 
                 }
    ...
}

[must do: 記錄每個使用者"加入卡伯"的時間，並統計在兩週後這些使用者的留存率]
# 檔名為該月份"yyyy-mm"(Ex: 9月這個月，檔名叫"2020-09")
# 每天的資料包含: "當天的Retention Rate" / "Warning"(default=""，若有低於0.2的當天會多一個Warning提醒，而如果連續一週都低於0.2的話會在終端機跳出警告提醒)
# "Warning": "The Retention Rate is somehow low for at least 7 days" (Ex: 9/7~9/13都小於 0.2)，表示這週數據偏低 @終端機顯示
# 比值四捨五入到小數點後兩位
# 此份 json 檔形如:
Ex: 2020/09/06~2020/09/13 每天與9/1的 DAU 比值分別為 [0.7, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17]
{
    "2020-09-06": { Retention Rate: 0.7, Warning: "" }
    "2020-09-07": { Retention Rate: 0.11, Warning: "The Retention Rate is below 0.2" }
    "2020-09-08": { Retention Rate: 0.12, Warning: "The Retention Rate is below 0.2" }
    "2020-09-09": { Retention Rate: 0.13, Warning: "The Retention Rate is below 0.2" }
    "2020-09-10": { Retention Rate: 0.14, Warning: "The Retention Rate is below 0.2" }
    "2020-09-11": { Retention Rate: 0.15, Warning: "The Retention Rate is below 0.2" }
    "2020-09-12": { Retention Rate: 0.16, Warning: "The Retention Rate is below 0.2" }
    "2020-09-13": { Retention Rate: 0.17, Warning: "The Retention Rate is below 0.2" }
}
並在終端機上顯示"The Retention Rate is somehow low below 0.2 from 2020-09-07 to 2020-09-13"

[optional: 篩選一個時間看該段時間加入卡伯的使用者留存率是否較高]
# 在 config.yml 中，可以讓使用者自由設定"想觀察哪段時間加入卡伯的使用者是否留存率比較高"及"要觀察多久時間作為留存依據"，形如: 
# start_date / end_date 格式: "yyyy-mm-dd"
# period 格式: integer (單位為"天")
# 檔名格式: "名稱" + "起訖日(yyyymmdd_yyyymmdd)"
Ex: 我想看國慶連假 2020-10-10 ~ 2020-10-12 加入卡伯的使用者留存率是否相對平常較高，而 period 為兩週觀察期，可以多新增一個 json 檔來比較兩週後 (2020-10-24 ~ 2020-10-26) 的留存率
{
    "Retention_Rate":
        start_date: "2020-10-10" ,
        end_date: "2020-10-12",
        period: 14
        filename: "國慶連假20201010_20201012"
        warning: 0.2
}
# 結果會多新增一個 json 檔在 Retention Rate 資料夾
```
### 功能活躍指標
    1. 功能分析主要分析功能活躍情況、頁面訪問路徑以及轉化率。

- **<font color=blue>熱門功能選單排行 (Serve_Ranking)</font> - 
<font color=red>定義"功能點擊排行": 分別計算"大功能間"及"子功能在大功能下"的點擊比例 (第b點)
定義"搜尋排行1": 計算每項"我的信用卡優惠" 11 項類別的點擊比例 (第d點)</font>**

    >a. 每日更新一次數據，一份檔案建立一個月的資料庫
    >b. 計算**每項功能被點擊的比例** (會先用 figma 等工具做出 user flow(流程圖)，比較各項功能的點擊次數看是否符合我們對使用者行為的預測)，並在 present 資料夾中建立**圓餅圖**
    >>>註: **計算方式:** 
    >>>(1) **大功能比例:** 各項子功能的點擊 (細體字) 會被算進大功能 (粗體字) 的點擊次數中，大功能會進行比例計算
    >>>(2) **子功能比例:** 各項子功能也會有在各大功能下的比例計算
    >>1. **加卡伯好友** > 點選"查詢商家優惠" > 點選熱門卡片"優惠詳細資訊" / 熱門搜尋關鍵字
    >>2. **呼叫卡伯** > 點選"優惠詳細資訊" / 輸入任意關鍵字 / 點選熱門搜尋 > (找到店家)查看熱門搜尋/關鍵字的"優惠詳細資訊" / (找不到店家)點選 11 個類別 > (點選 11 個類別其中之一)點選"查看所有優惠"
    >>3. **我的信用卡優惠** > 點選"查看信用卡優惠" > (有優惠)點選"查看所有優惠" 
    >>4. **我的信用卡** > 點選"新增信用卡" / "刪除卡片"
    >>5. **分享好友** > 選擇好友或群組送出
    >>6. **卡伯小幫手** > 輸入任意訊息
    >>7. **直接輸入關鍵字** > 查看關鍵字的"優惠詳細資訊"
    >>>註: 第7點的"**直接輸入關鍵字**"會被算進第2點的"**呼叫卡伯的輸入任意關鍵字**"內，輸入任意字都算一次點擊，因為難以分辨它是不小心輸錯還是故意輸入沒意義的話
    >>>註: "**see more**"和"**see another**"因為關乎使用者卡的數量不同，所以不列入統計
    >
    >c. 計算**每項"我的信用卡優惠" 11 項類別**被點擊的比例，並列出搜尋排行，其中關鍵字搜尋也會被歸類於此
    >> **網購 / 美食餐廳 / 娛樂 / 藥妝百貨 / 量販超市 / 生活 / 交通 / 旅遊住宿 / 國外 / 繳費 / 其他**
    >
    >d. 在搜尋排行會附上每項功能的"**比例**"及"**點擊次數**"
    >e. **log data : action, value, timestamp**
    >f. **convert raw data to : 每項大功能及子功能點擊比例排行, 我的信用卡優惠點擊比例排行**
```json=
# 會在"熱門功能選單排行"資料夾中建立兩個子資料夾分別存放下面兩種 json 檔
# 每日更新一次數據，一份檔案建立一個月的資料庫，並"按照比例降冪 sort 內部資料"

1. [功能點擊(第b點)] 檔名Ex: "功能_2020-09"
{
    "總點擊次數": 1650,
    "呼叫卡伯": { 排名: 1, 
                 點擊比例: 0.5, 
                 點擊次數: 825,
                 子功能點擊比例: {
                     "關鍵字搜尋": { 點擊比例: 0.6, 點擊次數: 495 }
                     "熱門搜尋": { 點擊比例: 0.2, 點擊次數: 165 },
                     ...
                 }
    },
    "我的信用卡優惠": { 排名: 2, 
                      點擊比例: 0.2, 
                      點擊次數: 320,
                      子功能點擊比例: {
                         "查看信用卡優惠": { 點擊比例: 0.6, 點擊次數: 192 }
                         "查看所有優惠": { 點擊比例: 0.2, 點擊次數: 64 },
                     ...
                 }
    },
    ...
}
# 第一行先放"總點擊次數"，再來按照比例 sort 排名由第一名依序往下排
# 每個value中含有四樣資訊: "排名", "點擊比例", "點擊次數", "子功能點擊比例"
# 其中"子功能點擊比例"是計算該子功能在該大功能下共佔了多少比例的點擊，內容有"點擊比例"及"點擊次數"

2. [我的信用卡優惠類別點擊(第d點)] 檔名Ex: "類別_2020-09"
{
    "總點擊次數": 564,
    "美食餐廳": { 排名: 1, 點擊比例: 0.5, 點擊次數: 282 },
    "量販超市": { 排名: 2, 點擊比例: 0.2, 點擊次數: 113 },
    ...
}
# 第一行先放"總點擊次數"，再來按照比例 sort 排名由第一名依序往下排
# 每個value中含有三樣資訊: "排名", "點擊比例", "點擊次數"
```
- **<font color=blue>週年慶/大促銷活動_活躍指標 (Anniversary_Serve_Ranking)</font> - 
<font color=red>定義: 特別用 timestamp 紀錄這段時間的 DAU (見下方(a)(b))</font>**

    >a. **將週年慶或促銷活動前後的 DAU 做成一個趨勢圖**, 觀察是不是會有一個 peak 峰值, 來證實使用者在這時候是會需要卡伯功能的 
    >>1. 會在 present 的資料夾
    >>2. 會先針對所有卡伯信用卡列表的商家蒐集大促銷活動的"**名稱**"及"**時間**"，在圖表該段時間特別標記出來
    >>3. 在一個促銷活動時間結束都會更新一次 DAU 趨勢圖
    >>4. **趨勢圖為 must do**
    >
    >b. 可以**將這段促銷時間每天的 DAU 去和其他非週年慶時段的 DAU_max 做比值**, 看會成長多少比例的使用率 
    >>1. 計算公式: **DAU_促銷日 / MAX(DAU_非促銷日)**
    >>2. 承(a)(2)，當使用者想看某段促銷時間的資料時，會自動屏蔽掉蒐集資料中為"促銷活動"的時間區段，而從其他非週年慶時段抓取 DAU_max
    >>3. **DAU_max 為 optional，需要資料時再去 config.yml 更改，才會建檔**
    >
    >c. **log data : timestamp, DAU**
    >d. **convert raw data to : 和其他 DAU 最大值的比值, 趨勢圖**
```json=
# 將想比較的促銷活動及活動時間輸進 config.yml，在活動期間結束後會生成一份 json 數據檔 (@週年慶資料夾) 及趨勢圖 (@present資料夾)
Ex: 在2020/09/14~2020/09/20 有"屈臣氏的週年慶優惠"，我想比較數據
[config.yml]
{
    "Anniversary": ["屈臣氏10週年慶"], #default為空list，自行填入
    "start day": ["2020/09/14"], #default為空list，自行填入
    "end day": ["2020/09/20"] #default為空list，自行填入
}
# value 為一個 list，若有不只一個活動想比較就直接往後輸入，index 為對應的

[屈臣氏10週年慶.json] (檔名從 config.yml 抓取活動名稱)
{
    "促銷活動": "屈臣氏10週年慶",
    "促銷開始日期": "2020/09/14",
    "促銷結束日期": "2020/09/20",
    "非週年慶時段 DAU_max": { "DAU最大值": 136, "最大值發生日期": "2020/09/08" }, #value為一個 dict{ "DAU最大值": DAU_max, "最大值發生日期": "DAU_max發生日期" }
    "DAU_0914 / DAU_max": 1.2, #列出週年慶每天對 DAU_max 的比值
    ...,
    "DAU_0920 / DAU_max": 1.8
}
```
### 資料分析使用者行為
- **<font color=blue>使用者行為分析資料儲存型態 (User_Action_Storing)</font> -**
**<font color=red>定義: 每個 user 都會建立一份自己的使用者行為 json 檔，數據一直累積並進行以下兩種分析</font>**
    >a. **分析1:** 
    >>1. **將個別 user 的"關鍵字搜尋"分類進 11 個類別 (包含熱門搜尋字)，連同點擊 11 類別的次數，比較每個使用者最常搜尋的類別**
    >>2. 在 offer id 的 category 有字串分類
    >>3. 找不到店家的訊息歸類在"**無效字串**"
    >>4. 將總點擊次數和搜尋次數分開統計，可觀察出使用者比較喜歡用"點擊類別"還是"關鍵字搜尋"
    >
    >b. **分析2:**
    >>1. **將個別 user 分別停留在每個介面(功能)的時間記錄下來，分析他可能對哪個優惠比較有興趣 (願意停留較長時間觀看)**
    >>2. 因為使用者最後一次操作後登出頁面我們不會有記錄，所以要統計該使用者每個功能的操作時間，並排序去掉極值後取平均，作為最後一次固定的停留時間
    >>>**(i)** sort操作頁面時間 (sec)={ 2, 2, 3, 5, 6, 7, 8, 50, 51, 120,... } (會有登出後再登入的可能)，gap 太大的極值刪掉 (先觀察排序完的結果再訂個落差時間以上資料刪除，像是落差90秒以上)
    >>>**(ii)** 將剩下有效資料取平均，作為每次最後一個頁面的停留時間，**每週更新**此"**平均頁面停留時間**" (取一週是因為上面多數指標都是一週跑一次程式，就一併連同這個大程式一起跑完比較不浪費資源)
    >
    >c. **log data : user_id, action, value, timestamp**
    >d. **convert raw data to :  json 檔型態呈現使用者行為分析**
```json=
# 每份檔名: user_id.json 
Ex: U567d7d0b8a934a92957a5c2cf7ec54bd.json
{
#分析1: 個別 user 的"關鍵字搜尋"分類進 11 個類別，連同點擊 11 類別的次數，比較每個使用者最常搜尋的類別 (按照"點擊+搜尋"的總次數由高到低排序)
#類別的dict內容有五樣: 點擊比例, 點擊次數, 搜尋比例, 搜尋次數, 搜尋關鍵字
    {
        "總搜尋次數": 62,
        "總點擊次數": 136, #像是點擊熱門搜尋
        "美食餐廳": { 點擊比例: 0.5, 點擊次數: 68, 搜尋比例: 0.6, 搜尋次數: 37, 搜尋關鍵字: ["鼎泰豐", "右手餐廳",...] },
        "量販超市": { 點擊比例: 0.2, 點擊次數: 27, 搜尋比例: 0.3, 搜尋次數: 19, 搜尋關鍵字: ["家樂福", "頂好",...] },
        ...,
        "無效字串": ["麥當勞力士", "哈囉!", "我好餓QQ"] #無效字串用 list 存檔
    }
#分析2: 個別 user 分別停留在每個介面(功能)的時間記錄下來，分析他可能對哪個優惠比較有興趣 (願意停留較長時間觀看)
#要記錄的項目分兩種: "我的信用卡優惠 11 項類別"停留時間, 各個"搜尋的關鍵字"停留時間(直接查詢或按熱門搜尋，分為"有效字串"和"無效字串")
#上述兩種項目的停留時間分開統計
#每個搜尋字串的停留時間為 (key: value)=("搜尋字串": [停留時間佔比, 停留時間])=(全家: [0.5, 627])
#"我的信用卡優惠 11 項類別總停留時間"有三項資訊: 停留時間佔比, 停留時間, 各次停留時間(list儲存)
    {
        "我的信用卡優惠 11 項類別總停留時間 (sec)": 1620,  
        "美食餐廳": { 停留時間佔比: 0.5, 停留時間: 810, 各次停留時間(sec): [63, 82, 51, 46,...] }
        "量販超市":
        ...,
        "各個搜尋的關鍵字停留時間 (sec)": 1254,
        "有效字串": { 全家: [0.5, 627], 星巴克: [0.2, 251],... },
        "無效字串": { 哈囉~: [0.005, 6.27],... }
    }
}
```
### 小想法: 可以用"熱門功能選單_單週排行"的資料，ML訓練出一個模型來預測卡伯用戶的下一步點選行動，可用於如果開發新功能的點擊預測 !







###### tags: `RD` `database` `LINEbot`

