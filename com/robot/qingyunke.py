import urllib.request as url
import urllib.parse
import json
def qingyunke(msg):
    url.urlcleanup()
    uri = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg))
    request = url.Request(uri, method="POST")
    response = url.urlopen(request,timeout=10).read().decode("utf-8")
    message_ = json.loads(response)
    flag = message_["result"]
    message = message_["content"]
    message=message.replace("{br}","\n")
    return flag, message
if __name__ == '__main__':
    msg = '狮子座运势'
    print("原话>>", msg)
    try:
        flag,message = qingyunke(msg)
        if flag==0:
            print("青云客>>", message)
    except Exception as e:
        print(str(e) )