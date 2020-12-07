import sys
import urllib
import urllib.request as url
import time
from com.utils.log import Log
import requests
from bs4 import BeautifulSoup
import re
log= Log("./error_page_log")

class Session(requests.Session):
    def __init__(self,timeOut=20):
        super(Session,self).__init__()
        self.timeOut=timeOut
    def get(self,*args,**kwargs):
        for i in range(10):
            try:
                return super(Session,self).get(*args,**kwargs,timeout=self.timeOut)
            except:
                if i<9:
                    time.sleep(5)
                else:raise

    def post(self,*args,**kwargs):
        for i in range(10):
            try:
                return super(Session,self).post(*args,**kwargs,timeout=self.timeOut)
            except:
                if i < 9:
                    time.sleep(5)
                else:
                    raise
session=Session()
def get_news():
    newDict={}
    uri = "https://www.binancezh.com/cn/support/announcement"
    while(True):
        response = session.get(uri)
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        news = soup.find(attrs={"class": "css-6f91y1"})
        if news is not None:
            break
        else:
            print("\n" + "NoneError")
            log.write("\n", soup.prettify())
        time.sleep(3)
    last_new = news.find(name="a")
    new=last_new.get_text()
    newDict[new]={"link":"https://www.binancezh.com" + last_new.attrs['href'],"time_Stamp":time.time(),"date":time.strftime("%m-%d %H:%M:%S", time.localtime())}

    return new,newDict
def get_market():
    try:
        headers={
            'Host': 'api.coinmarketcap.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'origin': 'https://coinmarketcap.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://coinmarketcap.com/',
            'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        }
        params = (
            ('listing_status', 'active,untracked'),
        )
        respJson = session.get('https://api.coinmarketcap.com/data-api/v3/map/all', headers=headers, params=params).json()["data"]
        return respJson#["cryptoCurrencyMap"]
    except:
        return None
def get_pairs(coinNews):
    try:
        coin_name= re.search(r"（(.*?)）", coinNews).group(1)
        coin_unit=None
        sys.path.append(r"D:\bin\BTC")
        from com import pyspy
        MarketInfo=pyspy.MarketInfo
        for unit in MarketInfo["cryptoCurrencyMap"]:
            if "symbol" in unit and unit["symbol"].find(coin_name)>=0:
                coin_unit=unit
                break
            if "name" in unit and unit["name"].find(coin_name) >= 0:
                coin_unit=unit
                break
        if coin_unit is not None:
            url="https://coinmarketcap.com/currencies/{}/markets".format(coin_unit["slug"])
            resp=session.get(url).text
            soup=BeautifulSoup(resp,"lxml")
            sTable=soup.find_all(name="table")
            table=sTable[2]
            tableOut=[]
            for row,tr in enumerate(table.find_all(name="tr")):
                tableOut.append([])
                col=tr.find_all(name="td")
                if len(col)<=0:
                    col = tr.find_all(name="th")
                for td in col:
                    tableOut[row].append(td.getText())
            while([] in tableOut):
                tableOut.remove([])
            Out=""
            for row in tableOut:
                for colnum in [0,1,2,3]:
                    Out+=(row[colnum]+"\t")
                Out+="\n"
            return Out
        return ""
    except:
        return ""




if __name__ == '__main__':
    new,dict=get_news()
    print(new)
    #Pairlist=get_pairs("币安创新区上市EasyFi（EASY）")
    #print(Pairlist)
    pass
