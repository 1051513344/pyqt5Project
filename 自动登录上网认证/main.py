# – coding:UTF-8 –
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from MainWindow import Ui_MainWindow
import json
import base64
from Crypto.Cipher import AES
import os
import requests
import execjs

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
            self.username = self.lineEdit.text()
            self.password = self.lineEdit_2.text()
        # 绑定菜单控件函数
        self.actionConfig.triggered.connect(self.urlConfig)

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

    def login(self):
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
                    "direct": self.checkBox_2.isChecked()
                }
                with open("RememberMe.json", "w") as f:
                    f.write(json.dumps(rememberMeConfig))
                if self.rememberMeConfig == {}:
                    QMessageBox.information(self, "提示", "登录成功！生成本地配置文件，如需个性化设置可对配置进行修改")
                else:
                    # 记住我配置文件存在
                    QMessageBox.information(self, "提示", "登录成功！")
            else:
                # 记住我勾选框未勾选，存在记住我配置则清除配置
                if os.path.exists("RememberMe.json"):
                    os.remove("RememberMe.json")
                QMessageBox.information(self, "提示", "登录成功！")
        else:
            if not self.checkBox.isChecked():
                if os.path.exists("RememberMe.json"):
                    os.remove("RememberMe.json")
            QMessageBox.warning(self, "提示", f"登录失败！{responseJson.get('msg')}")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/pic/logo.ico"))
    if os.path.exists("RememberMe.json"):
        with open("RememberMe.json", "r") as f:
            rememberMeConfig = json.loads(f.read())
        if not rememberMeConfig.get("direct"):
            ui = autoLoginWIFI()
            ui.show()
            sys.exit(app.exec_())
        else:
            ui = autoLoginWIFI()
            ui.login()
    else:
        ui = autoLoginWIFI()
        ui.show()
        sys.exit(app.exec_())

