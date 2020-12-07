import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(r"D:\bin\BTC")
from com import pyspy
from com.utils.request import get_news
from com.utils.request import get_market
from com.utils.request import get_pairs
from com.utils.t_liu import get_t_liu
from com.pyspy import log
import time
import copy
import threading
class getPairs(threading.Thread):
    def __init__(self, new):
        super(getPairs,self).__init__()
        self.new=new
    def run(self):
        for i in range(10):
            pairs=get_pairs(self.new)
            if pairs is not None:
                pyspy.PairsList=pairs
                return

class getMarket(threading.Thread):
    def run(self):
        pyspy.MarketInfo=get_market()
        last_time = time.time()
        while (True):
            if time.time() - last_time >= 3600:
                MarketInfo = get_market()
                if MarketInfo is not None:
                    pyspy.MarketInfo = MarketInfo
                    last_time = time.time()
                    time.sleep(3700)
def iscome():
    message = None
    if pyspy.if_check_liu==False:
        pyspy.MESSAGES_liu = "状态关：" + log.get_date()
        return message
    r_1=6
    r_2=22
    r=int(time.strftime("%H", time.localtime()))
    if r<r_1 or r>=r_2:
        pyspy.MESSAGES_liu = "不在时间段：" + log.get_date()
        return message
    flag_login_now, flag_device_now, dict = get_t_liu()
    if flag_login_now:
        if pyspy.flag_login == False:  # 状态更新
            pyspy.flag_login=True
            pyspy.MESSAGES_liu = "状态更新：" + log.get_date()
        elif pyspy.flag_device==False and flag_device_now==True:#来了
            message = "春眠不觉晓："+ log.get_date()
            # pyspy.if_check_liu=False
        elif pyspy.flag_device==True and flag_device_now==False:#走了
            message="处处闻啼鸟："+ log.get_date()
            # pyspy.if_check_liu = False
    pyspy.flag_login=flag_login_now
    pyspy.flag_device=flag_device_now
    pyspy.MESSAGES_liu = "检测中："+"\n"+"flag_login_now: "+str(flag_login_now)+"\n"+"flag_device_now: "+str(flag_device_now)+"\n"+str(dict)+"\n"+log.get_date()
    return message
def action(wechat):
    log.write("启动")
    pyspy.PNdict_load()
    pyspy.flag_login, pyspy.flag_device, dict = get_t_liu()
    while(True):
        time.sleep(10)
        try:
            pyspy.PairsList="正在查询"
            flag1=False
            flag2=False
            new,Ndict=get_news()
            if new not in pyspy.PNdict:
                flag1=True
                pyspy.PNdict_update(new, Ndict[new])
            if flag1:
                for key in pyspy.wechat_j["key"]:
                    if new.find(key)>=0:
                        flag2=True
                        log.write(new,"发现key")
            if flag1 and flag2:
                get_pairs=getPairs(new)
                get_pairs.start()
                print("\n检测到新闻")
                print(new)
                pyspy.users_wxid=copy.deepcopy(pyspy.Users_wxid)
                host_wxid = pyspy.wechat_j["host_wxid"]
                pid = int(pyspy.wechat_j["pid"])
                MESSAGES="  【检测到新闻 from bian】\n"
                MESSAGES += "Date:"+Ndict[new]["date"]+"\n"
                MESSAGES+="News:"+str(new)+"\n"
                MESSAGES+="Link:"+Ndict[new]["link"]+"\n"
                MESSAGES += "Pairs:\n" + pyspy.PairsList + "\n"
                MESSAGES+="PS"
                for i in range(38):
                    PS="PS 第 {} 次，回复任何内容关闭".format(i)
                    MESSAGES=MESSAGES.replace("PS",PS)
                    for user_wxid in pyspy.users_wxid:
                        time.sleep(1)
                        spy.send_text(user_wxid,MESSAGES,host_wxid,pid)
                    if len(pyspy.users_wxid) == 0: break
                    MESSAGES=MESSAGES.replace("Pairs:\n"+"正在查询"+ "\n","Pairs:\n" + pyspy.PairsList + "\n")
                    MESSAGES=MESSAGES.replace(PS,"PS")
                    time.sleep(1)
            else:
                pyspy.MESSAGES="检测中:"+log.get_date()
                print("\r"+pyspy.MESSAGES,end="")

            message=iscome()
            if message is not None:
                spy.send_text("wxid_0ybr4vwa1mat22", message, pyspy.wechat_j["host_wxid"], int(pyspy.wechat_j["pid"]))
                time.sleep(1)
                spy.send_text("24535753538@chatroom", message, pyspy.wechat_j["host_wxid"], int(pyspy.wechat_j["pid"]))
        except Exception as e:
            time.sleep(30)
            pyspy.MESSAGES=str(e)
            log.write(str(e))
            print("\n异常："+log.get_date())
if __name__ == '__main__':
    from com.pyspy.wechat import spy
    try:
        get_market_t= getMarket()
        get_market_t.start()
        pyspy.wechat_j_load()
        pid=spy.run(r"D:\Program Files (x86)\Tencent\WeChat\WeChat.exe")
        pyspy.wechat_j["pid"] = pid
        while(not pyspy.WECHAT_LOGIN_SUCESS):
            time.sleep(2)
        pyspy.wechat_j_save()
        # pyspy.refresh(600)#刷新wechat_j
        action(wechat=spy)
    finally:
        print("退出")
        log.write("退出")


