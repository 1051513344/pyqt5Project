# -*- coding: gbk -*-
import pywifi
import time
from pywifi import const
import threading
import schedule
import execjs
import requests
from util import isWifiLogin
import logging

log = logging.getLogger('wifiMonitorLogger')
log.setLevel(logging.INFO)
fileHandler = logging.FileHandler('wifiMonitor.log')
fileHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s')
fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)

def autoConnectWifi(inter):
    if inter.status() == const.IFACE_DISCONNECTED:
        f = pywifi.Profile()
        f.ssid = "ewell-work"
        f.key = "ewellyh9500"
        f.auth = const.AUTH_ALG_OPEN
        f.cipher = const.CIPHER_TYPE_CCMP
        f.akm.append(const.AKM_TYPE_WPA2PSK)
        inter.remove_all_network_profiles()
        temp_p = inter.add_network_profile(f)
        inter.connect(temp_p)
        time.sleep(3)
        if inter.status() == const.IFACE_CONNECTED:
            return True
        else:
            return False
    else:
        return True

def autoLoginWifi():
    pwdUtil_js = """
            function getTimeStamp() {
                return +(new Date()) + '';
            }
            function do_encrypt_rc4(pwd, timestamp) {
                var i, j = 0, a = 0, b = 0, c = 0, temp;
                var plen = timestamp.length,
                    size = pwd.length;

                var key = Array(256); //int
                var sbox = Array(256); //int
                var output = Array(size); //code of data
                for (i = 0; i < 256; i++) {
                    key[i] = timestamp.charCodeAt(i % plen);
                    sbox[i] = i;
                }
                for (i = 0; i < 256; i++) {
                    j = (j + sbox[i] + key[i]) % 256;
                    temp = sbox[i];
                    sbox[i] = sbox[j];
                    sbox[j] = temp;
                }
                for (i = 0; i < size; i++) {
                    a = (a + 1) % 256;
                    b = (b + sbox[a]) % 256;
                    temp = sbox[a];
                    sbox[a] = sbox[b];
                    sbox[b] = temp;
                    c = (sbox[a] + sbox[b]) % 256;
                    temp = pwd.charCodeAt(i) ^ sbox[c];//String.fromCharCode(src.charCodeAt(i) ^ sbox[c]);
                    temp = temp.toString(16);
                    if (temp.length === 1) {
                        temp = '0' + temp;
                    } else if (temp.length === 0) {
                        temp = '00';
                    }
                    output[i] = temp;
                }
                return output.join('');
            }
            """
    # �Զ�����wifi���ӳ٣�����ȴ�������Ϻ�ִ��
    pwdUtil = execjs.compile(pwdUtil_js)
    timeStamp = pwdUtil.call('getTimeStamp')
    encryptPwd = pwdUtil.call('do_encrypt_rc4', '3997', timeStamp)
    url = "http://192.4.1.10/ac_portal/login.php"
    form_data = {
        "opr": "pwdLogin",
        "userName": "3997",
        "pwd": encryptPwd,
        "auth_tag": timeStamp,
        "rememberPwd": 0
    }
    log.info(requests.post(url, data=form_data).content.decode("utf-8"))
    # time.sleep(5)
    # os.system("D:/toDesk/ToDesk.exe")

def autoKeepWifiConnected():
    log.info("��⿪ʼ...")
    wifi = pywifi.PyWiFi()
    inter = wifi.interfaces()[0]
    # ��WIFI�Ͽ����������
    if inter.status() == const.IFACE_DISCONNECTED:
        log.info("����������...")
        if autoConnectWifi(inter):
            log.info("�����ɹ���")
            # ���ӳɹ�������е�¼�ж�
            if not isWifiLogin():
                # ��û�е�¼������е�¼
                log.info("δ��¼WIFI�ص���...")
                autoLoginWifi()
                log.info("�ص����...")
        else:
            log.info("����ʧ�ܣ�")
    else:
        # ������WIFI���ж��Ƿ��¼
        if not isWifiLogin():
            # ��û�е�¼������е�¼
            log.info("δ��¼WIFI�ص���...")
            autoLoginWifi()
            log.info("�ص����...")
    if isWifiLogin():
        log.info("����������")
    else:
        log.info("�����쳣��")

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

startFlag = False
stopFlag = False

def run():
    run_threaded(autoKeepWifiConnected)
    schedule.every(60).seconds.do(run_threaded, autoKeepWifiConnected)
    while not stopFlag:
        schedule.run_pending()
        time.sleep(1)
    log.info("�˳�����")

def start():
    global startFlag
    global stopFlag
    originStopFlag = stopFlag
    if not startFlag:
        startFlag = True
        stopFlag = False
        run_threaded(run)
        return startFlag
    return originStopFlag

def stop():
    global startFlag
    global stopFlag
    stopFlag = True
    originStartFlag = startFlag
    startFlag = False
    return originStartFlag

if __name__ == "__main__":
    autoKeepWifiConnected()
    schedule.every(60).seconds.do(run_threaded, autoKeepWifiConnected)
    while True:
        schedule.run_pending()
        time.sleep(1)
