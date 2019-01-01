# -*- coding: utf-8 -*-
import socket,select   #socket模块
import json
from enum import Enum
from datetime import datetime
import requests
import re
from mitmproxy import ctx
HOST='192.168.0.17'
PORT=8888
userList=[]

class UserS:
    def __init__(self, connect, addr):
        self.connect = connect
        self.addr = addr
        self.nameIP= addr[0]
        self.connectTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def handleData(mes,userName):
    handleDeviceData(mes, userName)


def handleImageURL(mes,userName):
    print(mes)
def handleDeviceData(mes,userName):
    handleType=mes['handleType']

    if handleType == 'Other':
        getOnlineDevice(mes,userName)
    elif handleType =='handleQRCode':
        print()
    elif handleType =='asdasd':
        print()

def handleServerAData(mes,userName):
    print(mes)
def getOnlineDevice(mes,userName):
    loginURL=findQRRUL('https://img.alicdn.com/tfscom/TB1nM2TzgHqK1RjSZFPwu3wapXa.png', 'https://cli.im/Api/Browser/deqr')
    sendMobileDevicesLogin(loginURL)
def runSocket():
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
                user = UserS(c, addr)
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
                    for userd in userList:
                        if r is userd.connect:
                            handleData(json.loads(data), userd)
                            break

def findQRRUL(imageURL,QRURL):
    params = {"data": (None, imageURL)}
    url = QRURL
    res = requests.post(url, files=params)
    hjson = json.loads(res.content)
    loginURL=hjson['data']['RawData']
    print(loginURL)
    return loginURL

def sendMobileDevicesLogin(loginURL):
    if len(userList)<1:
        print('没有设备登陆')
    else :
        userName = userList[0];
        for userName in userList:
            data = {'loginTB': loginURL}
            jsonStr = json.dumps(data)
            userName.connect.send(jsonStr.encode("utf-8"))
def response(flow):
  """修改应答数据
  """
  if '/js/yoda.' in flow.request.url:
      # 屏蔽selenium检测
      for webdriver_key in ['webdriver', '__driver_evaluate', '__webdriver_evaluate', '__selenium_evaluate', '__fxdriver_evaluate', '__driver_unwrapped', '__webdriver_unwrapped', '__selenium_unwrapped', '__fxdriver_unwrapped', '_Selenium_IDE_Recorder', '_selenium', 'calledSelenium', '_WEBDRIVER_ELEM_CACHE', 'ChromeDriverw', 'driver-evaluate', 'webdriver-evaluate', 'selenium-evaluate', 'webdriverCommand', 'webdriver-evaluate-response', '__webdriverFunc', '__webdriver_script_fn', '__$webdriverAsyncExecutor', '__lastWatirAlert', '__lastWatirConfirm', '__lastWatirPrompt', '$chrome_asyncScriptInfo', '$cdc_asdjflasutopfhvcZLmcfl_']:
          ctx.log.info('Remove "{}" from {}.'.format(webdriver_key, flow.request.url))
          flow.response.text = flow.response.text.replace('"{}"'.format(webdriver_key), '"NO-SUCH-ATTR"')
      flow.response.text = flow.response.text.replace('t.webdriver', 'false')
      flow.response.text = flow.response.text.replace('ChromeDriver', '')

if __name__ == "__main__":
    runSocket()
