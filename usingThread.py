'''
    adb devices 목록에서 기기명 추출
    server threads: cmd Appium 으로 기기 하나당 서버 하나(port) 생성
    dv threads: desired caps
'''

import os
import re
import threading
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium import webdriver
import logging

def startServers(serial, port):
    cmd = 'appium --address 127.0.0.1' + ' --port ' + str(port) + ' --bootstrap-port ' + str(port -2000)+ ' -U ' + serial + ' --session-override --no-reset '
    print(threading.currentThread().getName(), " ", newPort)
    os.system(cmd)

def is_toast_exist(driver, text, timeout=2, poll_frequency=0.5):
    try:
        toast_loc = ("xpath", ".//*[contains(@text,'%s')]"%text)
        WebDriverWait(driver, timeout, poll_frequency).until(EC.presence_of_element_located(toast_loc))
        return True
    except:
        logging.warning("Toast Message Time Out")
        return False

class TestParallel:
    def setUp(self, serial, newPort, systemPort):
        desired_cap = {}
        desired_cap['platformName'] = 'Android'
        desired_cap['platformVersion'] = '11'
        desired_cap['automationName'] = 'uiautomator2'
        desired_cap['app'] = 'C:\\Users\\KIWIPLUS\\Desktop\\apk\\kiwiplay-v1.1.1(111)-stage-debug.apk'
        desired_cap['deviceUDID'] = serial
        desired_cap['systemPort'] = systemPort
        desired_cap['language'] = "kr"
        server_url = "http://localhost:" + str(newPort) +"/wd/hub"
        print(server_url)
        self.driver = webdriver.Remote(server_url, desired_cap)
        self.driver.implicitly_wait(30)
        self.testCase(serial)
    def testCase(self, serial):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '로그인')]")))
        app_server = "io.kiwiplus.app.kiwiplay.stage:id/"
        self.not_entered_email(app_server)
        self.invalid_email(app_server)
        self.tearDown()

    def not_entered_email(self, app_server):
        # TC22 아이디_미입력
        time.sleep(2)
        self.driver.find_element_by_id(app_server + "btnLogin").click()
        if (is_toast_exist(self.driver, "이메일을 정확히 입력해주세요.")):
            pass
        else:
            logging.warning("아이디_미입력 Toast Message text error")
            assert False

    def invalid_email(self, app_server):
        # TC23 아이디_유효하지 않은 이메일
        etEmail = self.driver.find_element_by_id(app_server + "etEmail")
        etEmail.send_keys("testinput")
        self.driver.find_element_by_id(app_server + "btnLogin").click()

        if (is_toast_exist(self.driver, "이메일을 정확히 입력해주세요.")):
            pass
        else:
            logging.warning("아이디_유효하지 않은 이메일 Toast Message text error")
            assert False

    def tearDown(self):
        self.driver.quit()

server_threads = []
dv_threads =[]
port=4722
out = os.popen("adb devices")
a=0
print(out)
for i in out.readlines():
    if 'List of devices' in i or "adb" in i or 'daemon' in i or 'offline' in i or 'unauthorized' in i or len(i) < 5:
        pass
    else:
        serial = re.findall('(.*)device', i)
        newPort = port + a
        systemPort = port + a + 4000
        test = TestParallel()
        a = a+1
        serial = re.findall('(.*)device', i)
        print(serial[0])
        server_threads.append(threading.Thread(target=startServers, args=(serial[0], newPort))) #server thread
        dv_threads.append(threading.Thread(target=test.setUp, args=(serial[0], newPort, systemPort))) #device thread
for t in server_threads:
    t.start()
    time.sleep(30)
for f in dv_threads:
    f.start()


