from com.pyspy import *
from com.utils.request import get_news
from com.utils.t_liu import get_t_liu

def init_news():
    with open(Past_news_f,"w") as f:
        new,PNdict=get_news()
        print(PNdict)
        json.dump(PNdict,f,ensure_ascii=False,indent=4)
def init_laoliu():
    PNdict={}
    with open(t_liu_news,"w") as f:
        flag_login, flag_device, dict=get_t_liu()
        PNdict["0"]=[flag_login, flag_device, dict]
        json.dump(PNdict,f,ensure_ascii=False)

if __name__ == '__main__':
    init_news()