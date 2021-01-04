'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# 讀檔
df = pd.read_csv('../user_action_log/DAU/2020-09.csv')  

# 指定默認字形：解決plot不能顯示中文問題
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False

# 行列互換
df_T = df.T

# 轉成csv
df_T.to_csv('../user_action_log/DAU/test.csv')
'''

'''
import os

path = os.path.abspath(os.path.join(os.getcwd(), ".."))
path_wau = path + "\\user_action_log\\WAU"
list = os.listdir(path_wau)
for i in list:
    print(i)
'''
import time, datetime

now = datetime.datetime.now()
t = datetime.date.today() + datetime.timedelta(days=1)
tomo = datetime.datetime(t.year, t.month, t.day, 0, 1, 0)
delta = (tomo-now).seconds
print("Sleep Time: %d"%delta)
print(type(delta))
print(delta)
time.sleep(3)