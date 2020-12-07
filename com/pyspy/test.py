import json
from com import pyspy
uri = "./wechat.json"
if __name__ == '__main__':

    # with open(uri, "w") as f:
    #     PNdict = {"王文": {
    #         "wxid": "wxid_0ybr4vwa1mat22"
    #     },
    #         "刀锋大号": {
    #             "wxid": "wxid_v3ax65razycb22"
    #         }
    #     }
    #     print(PNdict)
    #     json.dump(PNdict, f, ensure_ascii=False)


    # with open(uri, "r") as f:
    #     users = json.load(f)["users"]
    #     for user in users:
    #         print(user, users[user]["wxid"])
    pyspy.wechat_j_load()
    print(pyspy.wechat_j["group"])
