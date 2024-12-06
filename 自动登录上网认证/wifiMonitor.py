# – coding:UTF-8 –
import subprocess
import webbrowser

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from MainWindow import Ui_MainWindow
import json
import base64
from Crypto.Cipher import AES
import os
from auto import *
import logging

class autoLoginWIFI(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(autoLoginWIFI, self).__init__(parent)
        self.key = 'laoxulaoxulaoxux'
        self.rememberMeConfig = {}
        self.username = ""
        self.password = ""
        self.url = "http://1.1.1.4/ac_portal/login.php"
        self.setupUi(self)
        if os.path.exists("RememberMe.json"):
            with open("RememberMe.json", "r") as f:
                self.rememberMeConfig = json.loads(f.read())
            self.url = self.rememberMeConfig.get("url")
            self.lineEdit.setText(self.rememberMeConfig.get("username"))
            self.lineEdit_2.setText(self.AES_Decrypt(self.key, self.rememberMeConfig.get("password")))
            self.checkBox.setCheckState(Qt.Checked)
            if self.rememberMeConfig.get("direct"):
                self.checkBox_2.setCheckState(Qt.Checked)
            else:
                self.checkBox_2.setCheckState(Qt.Unchecked)
            if self.rememberMeConfig.get("monitor"):
                self.checkBox_3.setCheckState(Qt.Checked)
            else:
                self.checkBox_3.setCheckState(Qt.Unchecked)
            self.username = self.lineEdit.text()
            self.password = self.lineEdit_2.text()
        # 绑定菜单控件函数
        self.actionConfig.triggered.connect(self.urlConfig)
        self.actionLog.triggered.connect(self.openLog)
        self.actionTailLog.triggered.connect(self.tailLog)
        self.actionPath.triggered.connect(self.openPath)
        self.actionQuit.triggered.connect(self.quitApp)
        self.actionVersion.triggered.connect(self.about)

    def urlConfig(self):
        value, ok = QInputDialog.getMultiLineText(self, "配置登录地址", f'默认地址：{self.url}')
        if value != "":
            if value.startswith("http://") or value.startswith("https://"):
                self.url = value
                QMessageBox.information(self, "提示", f"设置成功，配置已生效！")
            else:
                QMessageBox.warning(self, "提示", f"请输入正确的url地址！")
        else:
            QMessageBox.information(self, "提示", f"配置未发生变更，将使用默认配置")

    def ifHaveWindowsCommand(self, command):
        try:
            try:
                process = subprocess.Popen(command, shell=True, cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(timeout=1)
                return stdout.decode("utf-8"),stderr.decode("utf-8")
            except subprocess.TimeoutExpired:
                process.kill()
            return True
        except Exception as e:
            return False
    def openLog(self):
        if os.path.exists("wifiMonitor.log"):
            QProcess.startDetached('notepad.exe wifiMonitor.log')
        else:
            QMessageBox.warning(self, "提示", f"日志文件wifiMonitor.log不存在，请勾选后台监控后登录重试！")
    def tailLog(self):
        if not self.ifHaveWindowsCommand("tail"):
            messageBox = QMessageBox(QMessageBox.Warning, "警告", "您的windows尚未安装tail命令，单击确定按钮将前往官网下载！")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('确定')
            buttonN = messageBox.button(QMessageBox.No)
            buttonN.setText('取消')
            messageBox.exec_()
            if messageBox.clickedButton() == buttonY:
                webbrowser.open("https://tail-for-windows.en.softonic.com/")
        else:
            if os.path.exists("wifiMonitor.log"):
                if not os.path.exists("monitor.bat"):
                    with open("monitor.bat", "w") as f:
                        f.write("tail -f wifiMonitor.log")
                os.system("start cmd.exe /K monitor.bat")
            else:
                QMessageBox.warning(self, "提示", f"日志文件wifiMonitor.log不存在，请勾选后台监控后登录重试！")

    def openPath(self):
        QProcess.startDetached("explorer.exe %s" % os.getcwd())

    def quitApp(self):
        re = QMessageBox.question(ui, "提示", "退出系统", QMessageBox.Yes |
                                  QMessageBox.No, QMessageBox.No)
        if re == QMessageBox.Yes:
            stop()
            QCoreApplication.instance().quit()
            tp.setVisible(False)
            sys.exit()

    def about(self):
        QMessageBox.about(self, "关于本软件",
                                      "软件版本：v1.0\n手动模式：输入上网认证账号密码点击登录即可登录上网\n下次直连：前提需要勾选记住密码，在下次打开软件时自动登录\n后台监控：前提需要勾选记住密码，此模式会实时监控网络变化并进行自动联网登录，在下次打开软件时，关闭后会在系统托盘运行\n本软件绿色无毒，完全免费，请放心使用！\n该软件版权归@医惠小徐所有。")

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.username = self.lineEdit.text()
        self.password = self.lineEdit_2.text()
        if self.username == "":
            QMessageBox.information(self, "警告", "请输入账号")
            return None
        if self.password == "":
            QMessageBox.information(self, "警告", "请输入密码")
            return None
        # 登录
        self.login()

    # 密钥（key）, 密斯偏移量（iv） CBC模式加密
    @staticmethod
    def AES_Encrypt(key, data):
        vi = '0102030405060708'
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        data = pad(data)
        # 字符串补位
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
        encryptedbytes = cipher.encrypt(data.encode('utf8'))
        # 加密后得到的是bytes类型的数据
        encodestrs = base64.b64encode(encryptedbytes)
        # 使用Base64进行编码,返回byte字符串
        enctext = encodestrs.decode('utf8')
        # 对byte字符串按utf-8进行解码
        return enctext

    @staticmethod
    def AES_Decrypt(key, data):
        vi = '0102030405060708'
        data = data.encode('utf8')
        encodebytes = base64.decodebytes(data)
        # 将加密数据转换位bytes类型数据
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
        text_decrypted = cipher.decrypt(encodebytes)
        unpad = lambda s: s[0:-s[-1]]
        text_decrypted = unpad(text_decrypted)
        # 去补位
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted

    def info(self, message):
        QMessageBox.information(self, "提示", message)

    def autoConnectWifi(self):
        wifi = pywifi.PyWiFi()
        inter = wifi.interfaces()[0]
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

    def login(self, connectWifi=False):
        if connectWifi:
            self.autoConnectWifi()
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
        pwdUtil = execjs.compile(pwdUtil_js)
        timeStamp = pwdUtil.call('getTimeStamp')
        encryptPwd = pwdUtil.call('do_encrypt_rc4', self.lineEdit_2.text(), timeStamp)
        form_data = {
            "opr": "pwdLogin",
            "userName": self.username,
            "pwd": encryptPwd,
            "auth_tag": timeStamp,
            "rememberPwd": 0
        }
        response = requests.post(self.url, data=form_data).content.decode("utf-8")
        responseJson = json.loads(response)
        if responseJson.get('success'):
            if self.checkBox.isChecked():
                # 记住我配置文件不存在，生成配置文件
                rememberMeConfig = {
                    "url": self.url,
                    "username": self.username,
                    "password": self.AES_Encrypt(self.key, self.password),
                    "direct": self.checkBox_2.isChecked(),
                    "monitor": self.checkBox_3.isChecked(),
                    "connectWifi": False
                }
                with open("RememberMe.json", "w") as f:
                    f.write(json.dumps(rememberMeConfig))
                if self.rememberMeConfig == {}:
                    QMessageBox.information(self, "提示", "登录成功！生成本地配置文件，如需个性化设置可对配置进行修改")
                    if self.checkBox_3.isChecked():
                        if start():
                            QMessageBox.information(self, "提示", "已开启后台监控，详见wifiMonitor.log日志！")
                    # 重新加载配置文件
                    with open("RememberMe.json", "r") as f:
                        self.rememberMeConfig = json.loads(f.read())
                else:
                    # 记住我配置文件存在
                    QMessageBox.information(self, "提示", "登录成功！")
                if not self.checkBox_3.isChecked():
                    if stop():
                        QMessageBox.information(self, "提示", "已关闭后台监控，详见wifiMonitor.log日志！")
                else:
                    if start():
                        QMessageBox.information(self, "提示", "已开启后台监控，详见wifiMonitor.log日志！")
            else:
                # 记住我勾选框未勾选，存在记住我配置则清除配置
                if os.path.exists("RememberMe.json"):
                    os.remove("RememberMe.json")
                    self.rememberMeConfig = {}
                QMessageBox.information(self, "提示", "登录成功！")
                if not self.checkBox_3.isChecked():
                    if stop():
                        QMessageBox.information(self, "提示", "已关闭后台监控，详见wifiMonitor.log日志！")
                else:
                    if start():
                        QMessageBox.information(self, "提示", "已开启后台监控，详见wifiMonitor.log日志！")
        else:
            if not self.checkBox.isChecked():
                if os.path.exists("RememberMe.json"):
                    os.remove("RememberMe.json")
            QMessageBox.warning(self, "提示", f"登录失败！{responseJson.get('msg')}")

class autoLoginWIFIClose(autoLoginWIFI):
    def closeEvent(self, event):
        if self.rememberMeConfig.get("monitor"):
            reply = QMessageBox.question(self, '确认', "确定要关闭窗口吗？", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                # 这里可以添加需要执行的代码或者其他操作
                stop()
                super().closeEvent(event)  # 必须调用基类的closeEvent()函数才能正常关闭窗口
            else:
                event.ignore()  # 取消关闭操作
        else:
            stop()
            super().closeEvent(event)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/pic/logo.ico"))
    if os.path.exists("RememberMe.json"):
        with open("RememberMe.json", "r") as f:
            rememberMeConfig = json.loads(f.read())
        if not rememberMeConfig.get("monitor"):
            if not rememberMeConfig.get("direct"):
                ui = autoLoginWIFIClose()
                ui.show()
                sys.exit(app.exec_())
            else:
                ui = autoLoginWIFIClose()
                ui.login(rememberMeConfig.get("connectWifi"))
        else:
            # start()
            # ui = autoLoginWIFI()
            # ui.show()
            # ui.info("已开启后台监控，详见wifiMonitor.log日志！")
            # sys.exit(app.exec_())

            # 关闭后在系统托盘运行
            app.setQuitOnLastWindowClosed(False)
            ui = autoLoginWIFI()
            start()
            ui.show()
            ui.info("已开启后台监控，详见wifiMonitor.log日志！")
            tp = QSystemTrayIcon(ui)
            tp.setIcon(QIcon(':/pic/logo.ico'))
            def quitApp():
                ui.show()  # w.hide() #隐藏
                re = QMessageBox.question(ui, "提示", "退出系统", QMessageBox.Yes |
                                          QMessageBox.No, QMessageBox.No)
                if re == QMessageBox.Yes:
                    stop()
                    QCoreApplication.instance().quit()
                    tp.setVisible(False)
                    sys.exit()
            quitMonitor = QAction('&退出', triggered=quitApp)  # 直接退出可以用qApp.quit
            quitMonitor.setIcon(QIcon(':/pic/退出.ico'))
            tpMenu = QMenu()
            tpMenu.addAction(quitMonitor)
            tp.setContextMenu(tpMenu)
            tp.show()
            def active(reason):
                if reason == 2 or reason == 3:
                    ui.show()
            tp.activated.connect(active)
            sys.exit(app.exec_())
    else:
        ui = autoLoginWIFIClose()
        ui.show()
        sys.exit(app.exec_())

