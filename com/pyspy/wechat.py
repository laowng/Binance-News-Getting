from com.utils.wechat.PyWeChatSpy import WeChatSpy
from com.utils.wechat.PyWeChatSpy.command import *
from com import pyspy
from com.robot.qingyunke import qingyunke
from com.robot.tencent import tencent

import logging
from bs4 import BeautifulSoup
from com.utils.t_liu import get_t_liu
# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

a = 5
logger = logging.getLogger(__file__)
formatter = logging.Formatter('%(asctime)s [%(threadName)s] %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.setLevel(logging.INFO)

contact_list = []
chatroom_list = []


def my_proto_parser(data):
    global WECHAT_LOGIN_SUCESS
    if data.type == WECHAT_CONNECTED:
        print("-" * 10, "微信连接成功", "-" * 10)
        # print("-"*10, "展示登录二维码", "-"*10)
        # spy.show_qrcode()
    elif data.type == WECHAT_LOGIN:
        print("-" * 10, "微信登录成功", "-" * 10)
        spy.get_login_info()

    elif data.type == WECHAT_LOGOUT:
        print("-" * 10, "微信登出", "-" * 10)
    elif data.type == LOGIN_INFO:
        print("-" * 10, "登录信息", "-" * 10)
        pyspy.wechat_j["host_wxid"]=data.login_info.wxid
        pyspy.wechat_j["nickname"]=data.login_info.nickname
        pyspy.WECHAT_LOGIN_SUCESS = True
        print(data.login_info.wxid)
        print(data.login_info.nickname)
        print(data.login_info.wechatid)
        print(data.login_info.phone)
        print(data.login_info.profilephoto)
        # 查询联系人列表(付费)
        spy.get_contacts()
    elif data.type == CONTACTS:
        print("-" * 10, "联系人列表", "-" * 10)
        for contact in data.contact_list.contact:
            print(contact.wxid, contact.nickname)
            if contact.wxid.startswith("gh_"):
                # 过滤公众号
                pass
            elif contact.wxid.endswith("chatroom"):
                # 群聊
                chatroom_list.append(contact.wxid)
            else:
                # 普通联系人
                contact_list.append(contact.wxid)
        print("-" * 10, f"共{len(contact_list)}个联系人,{len(chatroom_list)}个群", "-" * 10)
        # print("-"*10, "获取联系人详情(部分付费)", contact_list[5], "-"*10)
        # spy.get_contact_details(contact_list[5], True)
        # print("设置群名称(付费)", chatroom_list[0])
        # spy.set_chatroom_name(chatroom_list[0], "PyWeChatSpy")
        # print("发送群公告", chatroom_list[0])
        # spy.send_announcement(chatroom_list[0], "本条消息由PyWeChatSpy发出(https://zhuanlan.zhihu.com/p/118674498)")
        # print("创建群聊(付费)")
        # spy.create_chatroom(f"{contact_list[1]},{contact_list[2]},{contact_list[3]}")
        # print("-"*10, "获取群成员列表(付费)", chatroom_list[0], "-"*10)
        # spy.get_chatroom_members(chatroom_list[0])
    elif data.type == MESSAGE:
        # 消息
        for message in data.message:
            if message.type == 1:
                print("-" * 10, "文本消息", "-" * 10)
                if message.wxid1 == "filehelper":
                    spy.send_text("filehelper", "Hello PyWeChatSpy")
            elif message.type == 3:
                print("-" * 10, "图片消息", "-" * 10)
            elif message.type == 37:
                print("-" * 10, "好友请求消息", "-" * 10)
                # 好友请求消息
                # obj = etree.XML(message.content)
                # encryptusername, ticket = obj.xpath("/msg/@encryptusername")[0], obj.xpath("/msg/@ticket")[0]
                # 接收好友请求(付费)
                # spy.accept_new_contact(encryptusername, ticket)
            else:
                if message.wxid1 not in pyspy.Users_wxid:
                    print("-" * 10, "其他消息", "-" * 10)
                    return

            print("来源1:", message.wxid1)
            print("来源2:", message.wxid2)
            message.content = message.content.encode("gbk", errors="ignore").decode("gbk")
            if (message.wxid1 in pyspy.Users_wxid):
                print("消息头:", message.head)
                print("消息内容:", message.content)
                # pyspy.log.write("消息内容:", message.content)
                if message.wxid1 in pyspy.users_wxid:
                    pyspy.users_wxid.remove(message.wxid1)
                if message.content.find("查询") >= 0:
                    spy.send_text(message.wxid1, pyspy.MESSAGES, pyspy.wechat_j["host_wxid"], pyspy.wechat_j["pid"])
                    return
                if message.content.find("log") >= 0:
                    try:
                        logs = pyspy.log.get(5)
                        spy.send_text(message.wxid1, logs, pyspy.wechat_j["host_wxid"], pyspy.wechat_j["pid"])
                    except Exception as e:
                        pyspy.log.write("message.content.find('log')>=0", str(e))
                    return
                if message.content.find("state") >= 0:
                    spy.send_text(message.wxid1, pyspy.MESSAGES_liu, pyspy.wechat_j["host_wxid"], pyspy.wechat_j["pid"])
                    return
                if message.content.find("reverse") >= 0:
                    pyspy.if_check_liu=1-pyspy.if_check_liu
                    spy.send_text(message.wxid1, "reverse_success", pyspy.wechat_j["host_wxid"], pyspy.wechat_j["pid"])
                    return

            if (message.wxid1 in pyspy.Group_wxid):
                request = message.content
                print("消息头:", message.head)
                print("消息内容:", request)
                if message.type==47:
                    soup = BeautifulSoup(message.content, "lxml")
                    emoji = soup.find(name="emoji")
                    if emoji is not None:
                        emoji_cdnurl = emoji["cdnurl"]
                        spy.send_text(message.wxid1, emoji_cdnurl, pyspy.wechat_j["host_wxid"],
                                      pyspy.wechat_j["pid"])
                elif  request.find("@" + pyspy.wechat_j["nickname"])>=0:
                    if message.wxid2 in pyspy.chatting_users[message.wxid1]:
                        pyspy.chatting_users[message.wxid1].remove(message.wxid2)
                    else:
                        pyspy.chatting_users[message.wxid1].append(message.wxid2)
                    request = request.strip("@" +pyspy.wechat_j["nickname"])
                    try:
                        flag1,response1 = tencent(request)
                        # flag2, response2 = qingyunke(request)
                        flag2, response2 = 1, ""
                        if flag1==0 and flag2==0:
                            response=response1 if len(response1)>len(response2) else response2
                        elif flag1==0 or flag2==0:
                            response=response1 if flag1==0 else response2
                        else:
                            response="......"
                        spy.send_text(message.wxid1, response, pyspy.wechat_j["host_wxid"], pyspy.wechat_j["pid"])
                    except Exception as e:
                        pyspy.log.write("message.wxid1 in pyspy.Group_wxid", str(e))
                elif message.wxid2 in pyspy.chatting_users[message.wxid1]:
                    try:
                        flag1, response1 = tencent(request)
                        # flag2, response2 = qingyunke(request)
                        flag2, response2 = 1,""
                        if flag1 == 0 and flag2 == 0:
                            response = response1 if len(response1) > len(response2) else response2
                        elif flag1 == 0 or flag2 == 0:
                            response = response1 if flag1 == 0 else response2
                        else:
                            response = "......"
                        spy.send_text(message.wxid1, response, pyspy.wechat_j["host_wxid"], pyspy.wechat_j["pid"])
                    except Exception as e:
                        pyspy.log.write("message.wxid1 in pyspy.Group_wxid", str(e))

    elif data.type == QRCODE:
        print("-" * 10, "登录二维码", "-" * 10)
        print(data.qrcode.qrcode)
    elif data.type == CONTACT_EVENT:
        print("-" * 10, "联系人事件", "-" * 10)
        print(data)
    elif data.type == CHATROOM_MEMBERS:
        print("-" * 10, "群成员列表", "-" * 10)
        member_list = data.chatroom_member_list
        chatroom_wxid = member_list.wxid
        print(chatroom_wxid)
        for member in member_list.contact:
            print(member.wxid, member.nickname)
            # 添加群成员为好友(付费)
            # 高风险操作 频率较高容易引发微信风控
            # spy.add_contact(
            #     member.wxid,
            #     chatroom_wxid,
            #     "来自PyWeChatSpy(https://zhuanlan.zhihu.com/p/118674498)的问候",
            #     ADD_CONTACT_A)
    elif data.type == CONTACT_DETAILS:
        print("-" * 10, "联系人详情", "-" * 10)
        for details in data.contact_list.contact:
            print(details.wxid)
            print(details.nickname)
            print(details.wechatid)
            print(details.remark)
            print(details.profilephoto)
            print(details.profilephoto_hd)
            print(details.sex)
            print(details.whats_up)
            print(details.country)
            print(details.province)
            print(details.city)
            print(details.source)
    elif data.type == HEART_BEAT:
        # 心跳
        pass


spy = WeChatSpy(parser=my_proto_parser, key="dbc4b1ea77d21ab9ae2b865afd4edf1c", logger=logger)

if __name__ == '__main__':
    PID = spy.run(background=True)
