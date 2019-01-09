# -*- coding: utf-8 -*-
from gevent import monkey
from gevent.pywsgi import WSGIServer
from flask import Flask, request
from selenium import webdriver
import time
import requests
import ujson
import socket
from selenium.webdriver.chrome.options import Options
from threading import Thread,currentThread,activeCount
import multiprocessing
import signal
# monkey.patch_all()
import subprocess
# import commands
import threading
import py_compile
import logging
import mySocket
# subprocess.Popen('runServer.sh', shell=False)
app = Flask(__name__)
_chrome_options = Options()
_chrome_options._arguments= ['disable-infobars']
# _chrome_options.add_argument('--proxy-server=http://127.0.0.1:5555')
driver = webdriver.Chrome(executable_path='/Users/chenbolun/Downloads/chromedriver', chrome_options=_chrome_options,port=9999)
is_Login=False
cooks_map = {}
cookiestr =''
cookiestr2 =''
get_current_url=''
# 获取本机电脑名
myname = socket.getfqdn(socket.gethostname())
# 获取本机ip
myaddr = socket.gethostbyname(myname)
errorNum=0
lastTime=0
socketPID=0

@app.route('/NoLogin')
def NoLogin():
    global is_Login
    global cookiestr
    is_Login= False
    cookiestr=''
    return str(is_Login)

@app.route('/Loginok')
def Loginok():
    print('登陆成功!')
    global is_Login
    global imgPath
    imgPath=''
    is_Login = True
    # try:
    #     ma=driver.find_element_by_xpath("/html/body/div[4]/a")
    #     #
    #     if ma:
    #         ma.click()
    # except:
    #     pass
    # try:
    #     ma=driver.find_element_by_xpath("//*[@id='brix_65']/div[3]/div/span[1]")
    #     if ma:
    #         ma.click()
    #     # driver.find_element_by_xpath("//*[@id='brix_65']/div[3]/div/span[1]").click()
    # except:
    #     pass
    return str(is_Login)
myServer=mySocket.mySocketM(myaddr,8888,Loginok)


def TestLogin():
    global is_Login
    if is_Login==True:

        driver.refresh()
        if driver.current_url.startswith('https://www.alimama.com'):
            # global is_Login
            is_Login=False
    return str(is_Login)

@app.route('/currenturl')
def get_currenturl():
    global get_current_url
    get_current_url=driver.current_url
    if 'http://pub.alimama.com/myunion.htm' in get_current_url:

        return 'http://pub.alimama.com/myunion.htm'

    else:
        return get_current_url
    # return get_current_url

@app.route('/Login')
def Logins():
    Test_get_web_info()
    return str(is_Login)


@app.route('/restartDriver')
def restartDriver():
    global driver
    driver.quit()
    driver = webdriver.Chrome(executable_path='/Users/Meijian/Downloads/chromedriver', chrome_options=_chrome_options)
    t = {}
    t['success'] = 'True'
    return ujson.dumps(t, ensure_ascii=False)
    # return str(True)

def test_login_ok():
    driver.refresh()
    if not driver.current_url.startswith('https://www.alimama.com') or driver.current_url.startswith('https://pub.alimama.com'):
        Test_get_web_info()

@app.route('/getCookies')
def getCookies():
    # if Test_Time_long()==False:
    #     return '状态码为 666', 666
    # print(is_Login)
    # getServerStatus()
    test_login_ok()
    if is_Login:
        Test_get_web_info_cookies()
        driver.switch_to.parent_frame()
        try:
            driver.switch_to.frame("sufei-dialog-content")
            driver.find_element_by_xpath("/html/body/div[1]/p").text
            global cookiestr
            cookiestr=''
            restartDriver()
        except:
            global errorNum
            errorNum=1
            print('正常cookies')
            pass
        t = {}
        t['success'] = 'True'
        t['data'] =cookiestr
        return ujson.dumps(t, ensure_ascii=False)
    else:
        t = {}
        t['success'] = 'False'
        t['message'] = '抱歉还没有登陆成功!'
        return ujson.dumps(t, ensure_ascii=False)


@app.route('/getScreenshot')
def Screenshot():
    img=driver.save_screenshot(driver.title + ".png")
    print(img)
    return str(True)
@app.route('/getScreenshotData')
def ScreenshotData():
    return driver.get_screenshot_as_png()
# @app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    vlaue=request.values.get("link")
    return go(vlaue)


def goScan():
    r = requests.get('http://'+myaddr+':12399/Scan')
def go(link):
    try:
        driver.find_element_by_xpath("//*[@id='J_originUrl']").send_keys(link)
        driver.find_element_by_xpath("//*[@class='promo']/button").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='vf-dialog']/div/div/button").click()
        time.sleep(1)
        scick=driver.find_element_by_xpath("//*[@id='clip1']").text
        driver.find_element_by_xpath("/html/body/div[5]/a").click()
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='J_originUrl']").clear()
        return scick
    except:
        print('找不到元素')

def getHttpResponseHeader(browser):
    for responseReceived in browser.get_log('performance'):
        try:
            response = ujson.loads(responseReceived[u'message'])[u'message'][u'params'][u'response']
            print
            if response[u'url'] == browser.current_url:
                return response[u'headers']
        except:
            pass
    return None
def get_json_utl(url,cookies):
    # pvid:52_218.75.69.178_6807_1514188798306
    current_milli_time = lambda: int(round(time.time() * 1000))
    payload = {'tag': '30', 'gcid': '0', 'siteid': '36574024', 'selectact': 'sel', 'adzoneid': '130774249', 'newadzonename': '', 'channelIds': '', 't': str(current_milli_time), 'pvid': '52_218.75.69.178_8220_1514184102247', '_tb_token_': cookies['_tb_token_']}
    headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
               'Referer': url,
               'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'origin':"pub.alimama.com"}
    data = requests.post("https://pub.alimama.com/common/adzone/selfAdzoneCreate.json", cookies=cookies, headers=headers,data=payload).json().get('data')


def Test_get_web_info():
    driver.get('https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&css_style=alimama&from=alimama&redirectURL=http%3A%2F%2Fwww.alimama.com&full_redirect=true&disableQuickLogin=true')
    driver.maximize_window()
    driver.implicitly_wait(20)
    try:
        time.sleep(1)
        img = driver.find_element_by_xpath("//*[@id='J_QRCodeImg']/img").get_attribute('src')
        imgPath = img
        # os.kill(socketPID, signal.SIGUSR1)
        # signal.pause()
        # print(imgPath)
        myServer.getOnlineDevice(imgPath)
        # loginURL = main.findQRRUL(imgPath,
        #                      'https://cli.im/Api/Browser/deqr')
        # main.sendMobileDevicesLogin(loginURL)
        # driver.find_element_by_xpath("//*[@id='J_Quick2Static']").click()
    except:
        pass


def Test_get_web_info_cookies():
    driver.get('http://pub.alimama.com/myunion.htm#!/promo/self/links')
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='J_originUrl']").send_keys('https://item.taobao.com/item.htm?id=553539427097')
    time.sleep(1)
    driver.find_element_by_xpath("//*[@class='promo']/button").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='vf-dialog']/div/div/button").click()
    time.sleep(1)
    COOO=driver.get_cookies()
    cookie = [item["name"] + ":" + item["value"] for item in driver.get_cookies()]
    global cookiestr
    global cookiestr2
    cookiestr = ';'.join(item for item in cookie)

    cook_map = {}
    for item in cookie:
        str = item.split(':')
        cook_map[str[0]] = str[1]
    print(cook_map)
    cookiestr2 = cookie
    # get_json_utl(goUrl,cook_map)
    print(driver.get_cookies())
def Test_Time_long():
    t = int(time.time())
    global lastTime
    if t-lastTime >20:

        lastTime=t
        return True
    else:
        return False
# def GetMobilePhonePowerInformation():
    # output = commands.getstatusoutput('adb shell dumpsys battery')
    # url = 'https://oapi.dingtalk.com/robot/send?access_token=87fc518a597c498607c08bb6b1e7e38d52594b80e86d74fb5a981e257909b1ab'
    # headers = {"Content-Type": "application/json ;charset=utf-8 "}
    # String_textMsg = {\
    # "msgtype": "text",\
    # "text": {"content": output}}
    # response = requests.post(url, data=json.dumps(String_textMsg), headers=headers)
    # timer = threading.Timer(60 * 60, GetMobilePhonePowerInformation)
    # timer.start()

# if __name__ == '__main__':
    # logger = logging.getLogger()
    # file_handler = logging.FileHandler('/Users/Meijian/Desktop/crawlerLog/test.log')
    # logger.addHandler(file_handler)
    # logger.setLevel(logging.INFO)
    # logging_format = logging.Formatter(
    #     '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    # file_handler.setFormatter(logging_format)
    # app.logger.addHandler(file_handler)
    # py_compile.compile('/Users/Meijian/Documents/ALMMWeb/ALMM.py')
    # GetMobilePhonePowerInformation()
def runWebServer():
    print('启动web服务')
    app.run(port=5500,host=myaddr)

if __name__ == '__main__':
    # http_server = WSGIServer((myaddr, 5500), app)
    # http_server.serve_forever()
    # app.run(port=5500)
    threading.Thread(target=runWebServer, name='worker').start()
    threading.Thread(target=myServer.runSocket(), name='sock').start()
    # p1 = multiprocessing.Process(target=main.runSocket)
    # p2 = multiprocessing.Process(target=runWebServer)
    # print(p1.pid)
    # p2.start()
    # p1.start()
    # print(p1.pid)
    # socketPID=p1.pid
