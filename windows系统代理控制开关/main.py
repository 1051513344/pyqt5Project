# – coding:UTF-8 –

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QAction, QMenu
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
import os
import json
import atexit
from winproxy import ProxySetting
import re

class WindowProxySwitch(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(WindowProxySwitch, self).__init__(parent)
        self.setFixedSize(289, 139)  # 设置固定大小
        self.status = False
        self.ps = ProxySetting()
        self.config = {}
        self.defaultProxyConfig = """{"ip": "43.252.229.203", "port": 8888}"""
        if os.path.exists("proxyConfig.json"):
            try:
                with open("proxyConfig.json", "r", encoding="utf-8") as f:
                    self.config = json.loads(f.read())
                    if "ip" not in self.config or "port" not in self.config or not self.is_valid_ip(self.config['ip']):
                        QMessageBox.critical(self, '错误', "读取代理配置失败，请检查proxyConfig.json配置！")
                        sys.exit()
            except Exception as e:
                QMessageBox.critical(self, '错误', "读取代理配置失败，请检查proxyConfig.json配置！")
                sys.exit()
        else:
            with open("proxyConfig.json", "w", encoding="utf-8") as f:
                f.write(self.defaultProxyConfig)
                self.config = json.loads(self.defaultProxyConfig)
        self.setupUi(self)
        self.lineEdit.setText(self.config['ip'])
        self.spinBox.setValue(self.config['port'])
        # 注册清理函数
        atexit.register(self.close_proxy)
        # 使用说明书
        self.actionAbout.triggered.connect(self.about)

    def set_proxy(self):
        """设置系统代理"""
        self.ps.enable = True
        self.ps.server = f"{self.config['ip']}:{self.config['port']}"
        self.ps.registry_write()
        self.status = True
        self.pushButton.setText("关闭代理")
        self.saveConfig()
        QMessageBox.information(self, "提示", f"已开启系统代理：{self.config['ip']}:{self.config['port']}")
    def close_proxy(self, showTip=False):
        """关闭系统代理"""
        self.ps.enable = False
        self.ps.registry_write()
        self.status = False
        self.pushButton.setText("开启代理")
        self.saveConfig()
        if showTip:
            QMessageBox.information(self, "提示", f"已关闭系统代理：{self.config['ip']}:{self.config['port']}")

    def saveConfig(self):
        if self.config['ip'] == self.lineEdit.text() and self.config['port'] == self.spinBox.value():
            return None
        self.config['ip'] = self.lineEdit.text()
        self.config['port'] = self.spinBox.value()
        with open("proxyConfig.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.config))

    @pyqtSlot()
    def on_pushButton_clicked(self):
        if self.status:
            self.close_proxy(True)
        else:
            self.set_proxy()

    def is_valid_ip(self, ip):
        pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
        return re.match(pattern, ip) is not None

    def about(self):
        QMessageBox.about(self, "使用说明书", "首次打开会在当前目录下生成默认配置文件proxyConfig.json，可在该文件自定义配置对应的系统代理，关闭此软件自动关闭系统代理。\n本软件绿色无毒，完全免费，请放心使用！")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = WindowProxySwitch()
    ui.show()
    sys.exit(app.exec_())

