import urllib.request as url
import time
from com.utils.log import Log
uname="2006078"#
device_mac="e0:62:67:50:63:d1"#
log= Log("./error_page_log")
def get_t_liu():
    from bs4 import BeautifulSoup
    uri = "http://202.117.144.205:8601/snnuportal/userstatus.jsp"
    request = url.Request(url=uri, method="get")
    # while(True):
    dict={}
    flag_login=False
    flag_device=False
    response = url.urlopen(request,timeout=20)
    html = response.read()
    url.urlcleanup()
    soup = BeautifulSoup(html, "lxml")
    account = soup.find(attrs={"id": "account"})
    for i in range(5):
        if account is not None:
            if account.attrs["value"] == uname:
                flag_login=True
                table_url=soup.find(attrs={"align":"middle","frameborder":"0"}).attrs["src"]
                table_request=url.Request(url=table_url,method="get")
                table = url.urlopen(table_request, timeout=20)
                soup = BeautifulSoup(table.read(), "lxml")
                table=soup.find(attrs={"id": "ec_table_body"})
                news=table.find_all(name="tr")
                for new in news[1:]:
                    ns=new.find_all(name="td")
                    result_list=[]
                    for n in [ns[0],ns[2],ns[4]]:
                        result_list.append(n.get_text())
                    dict[ns[1].get_text()]=result_list
                if device_mac in dict and dict[device_mac][-1].find("办公区")>=0:
                    flag_device=True
                return flag_login,flag_device,dict
            return flag_login,flag_device,dict
        time.sleep(5)
    return flag_login,flag_device,dict

if __name__ == '__main__':
    flag_login, flag_device, dict=get_t_liu()
    print( flag_login,flag_device,dict)
    pass
