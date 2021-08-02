import os
import re
import threading
import time

from appium import webdriver

def startServers(serial, port):
    cmd = 'appium --address 127.00.0.1' + ' --port ' + str(port) + ' --bootstrap-port ' + str(port -2000)+ ' -U ' + serial + ' --session-override --no-reset '
    os.system(cmd)
class TestParallel:
    def setUp(self, serial, newPort, systemPort):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '11'
        desired_caps['automationName'] = 'uiautomator2'
        desired_caps['app'] = 'C:\\Users\\KIWIPLUS\\Desktop\\apk\\kiwiplay-v1.1.1(111)-stage-debug.apk'
        desired_caps['udid'] = serial
        desired_caps['systemPort'] = systemPort
        self.driver = webdriver.Remote("http://localhost:" + str(newPort) +"/wd/hub", desired_caps)
        self.testCase(serial)
    def testCase(self, serial):
        self.tearDown()
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


