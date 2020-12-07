#coding=utf-8
import os
import json
from com.utils.log import Log
curPath = os.path.abspath(os.path.dirname(__file__))
Past_news_f = os.path.join(curPath,"past_news.json")
Market_f= os.path.join(curPath,"marketInfo.json")
t_liu_news = os.path.join(curPath,"t_liu_news.json")
wechat_f =  os.path.join(curPath,"./wechat.json")
wechat_j = None
PNdict=None
MESSAGES = "init"
MESSAGES_liu="init"
if_check_liu=True
flag_login=False
flag_device=False
WECHAT_LOGIN_SUCESS = False
PairsList=""
MarketInfo=None
Users_wxid = []#常量
Group_wxid = []#群组
users_wxid = []#变量，用于提醒
chatting_users={}#变量
log = Log("./")
def PNdict_load():
    global PNdict
    with open(Past_news_f, "r") as f:
        PNdict = json.load(f)

def PNdict_update(key,value):
    global PNdict
    PNdict[key] = value
    try:
        with open(Past_news_f, "w") as f:  # 更新Past.json文件
            json.dump(PNdict, f, ensure_ascii=False,indent=4)
    except Exception as e:
        log.write("PNdict_update",str(PNdict),str(e))

def market_load():
    with open(Market_f, "r") as f:
        return json.load(f)

def market_update(marketInfo):
    try:
        with open(Market_f, "w") as f:  # 更新Past.json文件
            json.dump(marketInfo, f,indent=4)
    except Exception as e:
        log.write("marketInfo",str(PNdict),str(e))


def wechat_j_load():
    global wechat_j,Users_wxid,Group_wxid
    with open(wechat_f, "r") as f:
        Users_wxid=[]
        wechat_j = json.load(f)
        for user in wechat_j["users"]:
            Users_wxid.append(wechat_j["users"][user]["wxid"])
        for group in wechat_j["group"]:
            chatting_users[group]=[]
            Group_wxid.append(group)



def wechat_j_save():
    global wechat_j
    if wechat_j is None:
        log.write("wechat_j is None")
        return
    with open(wechat_f, "w") as f:
        json.dump(wechat_j, f, ensure_ascii=False,indent=4)
from threading import Timer
# 打印时间函数


def refresh(inc):
    wechat_j_load()
    t = Timer(inc, refresh,(inc,))
    t.start()
if __name__ == '__main__':
    import copy
    wechat_j_load()
    print(users_wxid)