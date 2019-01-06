# -*- coding: utf-8 -*-
# @Time    : 2019-01-06 13:42
# @Author  : Mat
# @File    : mySocket.py
# @Software: PyCharm
from datetime import datetime
import socket,select   #socket模块
import ujson
import requests
class UserS:
    def __init__(self, connect, addr):
        self.connect = connect
        self.addr = addr
        self.nameIP= addr[0]
        self.connectTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class mySocketM:
    def __init__(self,HOST,addr,method):
        self.HOST=HOST
        self.addr=addr
        self.userList=[]
        self.method=method
        self.method_name = method.__name__

    def handleDeviceData(mes, userName):
        handleType = mes['handleType']

        if handleType == 'Other':
            # getOnlineDevice(mes,userName)
            print('a')
        elif handleType == 'handleQRCode':
            print()
        elif handleType == 'asdasd':
            print()
    def handleData(self,mes, userName):
        self.handleDeviceData(mes, userName)

    def getOnlineDevice(self,imgurl):
        loginURL = self.findQRRUL(imgurl,
                             'https://cli.im/Api/Browser/deqr')
        self.sendMobileDevicesLogin(loginURL)

    def findQRRUL(self,imageURL, QRURL):
        params = {"data": (None, imageURL)}
        url = QRURL
        res = requests.post(url, files=params)
        hjson = ujson.loads(res.content)
        loginURL = hjson['data']['RawData']
        print(loginURL)
        return loginURL

    def sendMobileDevicesLogin(self,loginURL):
        if len(self.userList) < 1:
            print('没有设备登陆')
        else:
            for userName in self.userList:
                data = {'loginTB': loginURL}
                jsonStr = ujson.dumps(data)
                userName.connect.send(jsonStr.encode("utf-8"))
            self.method()
    def runSocket(self):
        # signal.signal(signal.SIGUSR1, receive_signal)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        s.bind((self.HOST, self.addr))  # 套接字绑定的IP与端口
        s.listen(5)  # 开始TCP监听
        inputs = [s]

        while True:
            rs, ws, es = select.select(inputs, [], [])
            for r in rs:
                if r is s:
                    c, addr = s.accept()
                    inputs.append(c)
                    user = UserS(c, addr)
                    self.userList.append(user)
                else:
                    try:
                        data = r.recv(1024)
                        disconnected = not data
                    except:
                        disconnected = True
                    if disconnected:
                        inputs.remove(r)
                        for userd in self.userList:
                            if r is userd.connect:
                                self.userList.remove(userd)
                    else:
                        for userd in self.userList:
                            if r is userd.connect:
                                self.handleData(ujson.loads(data), userd)
                                break