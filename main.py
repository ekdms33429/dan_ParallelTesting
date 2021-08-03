import os
import re
import threading
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from appium import webdriver

def startServers(serial, port):
    cmd = 'appium --address 127.0.0.1' + ' --port ' + str(port) + ' --bootstrap-port ' + str(port -2000)+ ' -U ' + serial + ' --session-override --no-reset '
    print(threading.currentThread().getName(), " ", newPort)
    os.system(cmd)
class TestParallel:
    def setUp(self, serial, newPort, systemPort):
        desired_cap = {}
        desired_cap['platformName'] = 'Android'
        desired_cap['platformVersion'] = '11'
        desired_cap['automationName'] = 'uiautomator2'
        desired_cap['app'] = 'C:\\Users\\KIWIPLUS\\Desktop\\apk\\kiwiplay-v1.1.1(111)-stage-debug.apk'
        desired_cap['deviceUDID'] = serial
        desired_cap['systemPort'] = systemPort
        server_url = "http://localhost:" + str(newPort) +"/wd/hub"
        print(server_url)
        self.driver = webdriver.Remote(server_url, desired_cap)
        self.driver.implicitly_wait(30)
        self.testCase(serial)
    def testCase(self, serial):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, '로그인')]")))
    def tearDown(self):
        self.driver.quit()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    threads = []
    threads1 =[]
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
            threads.append(threading.Thread(target=startServers, args=(serial[0], newPort)))
            threads1.append(threading.Thread(target=test.setUp, args=(serial[0], newPort, systemPort)))
    for t in threads:
        t.start()
        time.sleep(30)
    for f in threads1:
        f.start()


