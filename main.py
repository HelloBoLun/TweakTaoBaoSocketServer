# -*- coding: utf-8 -*-
import socket,select   #socket模块
import json
from enum import Enum
from datetime import datetime
HOST='192.168.1.207'
PORT=8888
userList=[]

class UserS:
    def __init__(self, connect, addr):
        self.connect = connect
        self.addr = addr
        self.nameIP= addr[0]
        self.connectTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def handleData(mes,userName):
    if mes['forDevice'] == u'1':
        handleDeviceData(mes,userName)
    else :
        handleServerAData(mes,userName)

def handleImageURL(mes,userName):
    print(mes)
def handleDeviceData(mes,userName):
    handleType=mes['handleType']

    if handleType == 'Other':
        getOnlineDevice(mes,userName)
    elif handleType =='handleQRCode':
        print ''
    elif handleType =='asdasd':
        print ''

def handleServerAData(mes,userName):
    print mes
def getOnlineDevice(mes,userName):
    devStr=''
    for us in userList:
        devStr+=us.nameIP+'&'+str(addr[1])

    userName.connect.send(devStr)

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
    s.bind((HOST, PORT))  # 套接字绑定的IP与端口
    s.listen(5)  # 开始TCP监听
    inputs = [s]

    while True:
        rs, ws, es = select.select(inputs, [], [])
        for r in rs:
            if r is s:
                c, addr = s.accept()
                inputs.append(c)
                print(addr)
                user=UserS(c,addr)
                userList.append(user)
            else:
                try:
                    data = r.recv(1024)
                    disconnected = not data
                except:
                    disconnected = True
                if disconnected:
                    inputs.remove(r)
                    for userd in userList:
                        if r is userd.connect:
                            userList.remove(userd)
                else:
                    print(data)
                    print(addr)
                    for userd in userList:
                        if r is userd.connect:
                            handleData(json.loads(data),userd)
                            break
