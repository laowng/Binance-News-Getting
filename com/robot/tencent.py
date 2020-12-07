import hashlib
import urllib
import urllib.request
import time
import json
url_preffix = 'https://api.ai.qq.com/fcgi-bin/'

app_key = 'TO30PfEwaOgp8e4O'
app_id = '2157050701'

def setParams(array, key, value):
    array[key] = value


def genSignString(parser):
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, urllib.parse.quote(str(parser[key]), safe=''))
    sign_str = uri_str + 'app_key=' + parser['app_key']

    hash_md5 = hashlib.md5(sign_str.encode("latin1"))
    return hash_md5.hexdigest().upper()


class AiPlat(object):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.data = {}

    def invoke(self, params):
        self.url_data = urllib.parse.urlencode(params).encode(encoding='utf-8')
        req = urllib.request.Request(self.url, self.url_data)
        try:
            rsp = urllib.request.urlopen(req,timeout=10)
            str_rsp = rsp.read()
            dict_rsp = json.loads(str_rsp.decode('utf-8'))
            return dict_rsp
        except urllib.error.URLError as e:
            dict_error = {}
            if hasattr(e, "code"):
                dict_error = {}
                dict_error['ret'] = -1
                dict_error['httpcode'] = e.code
                dict_error['msg'] = "sdk http post err"
                return dict_error
            if hasattr(e, "reason"):
                dict_error['msg'] = 'sdk http post err'
                dict_error['httpcode'] = -1
                dict_error['ret'] = -1
                return dict_error
            else:
                dict_error = {}
                dict_error['ret'] = -1
                dict_error['httpcode'] = -1
                dict_error['msg'] = "system error"
                return dict_error

    def getNlpTextChat(self, session, question):
        self.url = url_preffix + 'nlp/nlp_textchat'
        setParams(self.data, 'app_id', self.app_id)
        setParams(self.data, 'app_key', self.app_key)
        setParams(self.data, 'time_stamp', int(time.time()))
        setParams(self.data, 'nonce_str', int(time.time()))
        setParams(self.data, 'session', session)
        setParams(self.data, 'question', question)
        sign_str = genSignString(self.data)
        setParams(self.data, 'sign', sign_str)
        return self.invoke(self.data)


def tencent(questionS):
    str_question = questionS
    session = 10000
    ai_obj = AiPlat(app_id, app_key)

    rsp = ai_obj.getNlpTextChat(session, str_question)
    flag=rsp['ret']
    message = (rsp['data'])['answer']
    return flag,message

if __name__ == '__main__':
    msg = '我好看吗'
    print("原话>>", msg)
    try:
        flag, message = tencent(msg)
        if flag == 0:
            print("tencent>>", message)
    except Exception as e:
        print(str(e))