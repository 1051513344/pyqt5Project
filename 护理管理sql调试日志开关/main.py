# – coding:UTF-8 –

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QAction, QMenu
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
import os
import json
import re

class adminSqlLogSwitch(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(adminSqlLogSwitch, self).__init__(parent)
        self.setFixedSize(322, 268)  # 设置固定大小
        try:
            self.config = {}
            self.sourceCode = {}
            self.loggerDict = {}
            self.defaultConfig = """{
  "ip": "...",
  "port": 8081,
  "loggers": [
    {
      "name": "护理排班模块",
      "package": "com.bozhong.schedule.dao"
    },
    {
      "name": "人员档案模块",
      "package": "com.bozhong.nursestaff.dao"
    },
    {
      "name": "质控检查模块",
      "package": "com.bozhong.inhospitalqc.dao"
    },
    {
      "name": "护理日常工作模块",
      "package": "com.bozhong.plan.dao"
    },
    {
      "name": "不良事件模块",
      "package": "com.bozhong.nurseae.dao"
    },
    {
      "name": "敏感指标模块",
      "package": "com.bozhong.nursecollection.dao"
    },
    {
      "name": "满意度调查模块",
      "package": ["com.bozhong.satisfaction.dao", "com.bozhong.satisfaction.mapper"]
    },
    {
      "name": "护理教育模块",
      "package": ["com.bozhong.nursetrain.dao", "com.bozhong.nursetrain.mapper"]
    },
    {
      "name": "护理绩效模块",
      "package": "com.bozhong.performance.dao"
    },
    {
      "name": "文书表单模块",
      "package": "com.bozhong.form.dao"
    },
    {
      "name": "基础模块",
      "package": ["com.bozhong.nursebase.dao", "com.bozhong.nursebase.mapper"]
    },
    {
      "name": "转换模块",
      "package": "com.bozhong.transform.mapper"
    }
  ]
}"""
            self.defaultSourceCode = """
def getOracleDate(text):
    import re
    # oracle日期转换 to_date
    if text is not None:
        oracle_date_pattern = ".*\d\d\d\d-\d+-\d+ \d+:\d+:\d+.\d+.*"
        results = re.findall(oracle_date_pattern, text)
        if len(results) > 0:
            result = results[0]
            if "'" in result:
                result = result.replace(re.findall("\.\d", result)[0], "")
                return f"to_date({result} , 'yyyy-mm-dd hh24:mi:ss')"
            else:
                result = result.replace(re.findall("\.\d", result)[0], "")
                return f"to_date('{result}' , 'yyyy-mm-dd hh24:mi:ss')"
    return ""

def getDbTypeList():
    return "oracle,mysql".split(",")

def getParamByType(dbType, param):
    if dbType == "mysql":
        if param.endswith("(Timestamp)"):
            param = param.replace("(Timestamp)", "")
            return f'"{param}"'
        if param.endswith("(String)"):
            param = param.replace("(String)", "")
            return f'"{param}"'
        if param.endswith("(Integer)"):
            param = param.replace("(Integer)", "")
            return f'{param}'
    if dbType == "oracle":
        if param.endswith("(Timestamp)"):
            param = param.replace("(Timestamp)", "")
            return getOracleDate(param)
        if param.endswith("(String)"):
            param = param.replace("(String)", "")
            return f"'{param}'"
        if param.endswith("(Integer)"):
            param = param.replace("(Integer)", "")
            return f'{param}'
    return None
"""
            self.setupUi(self)
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding='utf-8') as f:
                    self.config = json.loads(f.read())
            else:
                with open("config.json", "w", encoding='utf-8') as f:
                    f.write(self.defaultConfig)
                self.config = json.loads(self.defaultConfig)
            if not os.path.exists("SourceCode.conf"):
                with open("SourceCode.conf", "w", encoding='utf-8') as f:
                    f.write(self.defaultSourceCode)
            with open("SourceCode.conf", "r", encoding='utf-8') as f:
                self.sourceCode = f.read()
            self.getParamByType = self.getParamByTypeFunc()
            # 从剪贴板中获取ip
            ip = self.getIpFromClipboard()
            if ip is not None:
                self.lineEdit.setText(ip)
            else:
                if "ip" in self.config:
                    self.lineEdit.setText(self.config.get("ip"))
            if "port" in self.config:
                self.spinBox.setValue(self.config.get("port"))
            if "loggers" in self.config:
                loggers = self.config.get("loggers")
                names = [logger['name'] for logger in loggers]
                packages = [logger['package'] for logger in loggers]
                self.loggerDict = dict(zip(names, packages))
                self.comboBox.addItems(names)
            # 使用说明书
            self.action.triggered.connect(self.instruction)
            # 光标移至行首
            self.lineEdit.setCursorPosition(0)
        except Exception as e:
            with open("error.txt", "w") as f:
                f.write("初始化失败：" + str(e))
            QMessageBox.critical(self, '错误', "初始化失败！详见error.txt")
            os.system("error.txt")
            sys.exit()

    def getParamByTypeFunc(self):
        functions = {}
        result = {}
        exec(self.sourceCode, {}, functions)
        exec(self.sourceCode, functions, result)
        self.comboBox_2.addItems(result['getDbTypeList']())
        return result['getParamByType']

    def formatSql(self, dbType, sql):
        prepare = None
        params = None
        for row in sql.split("\n"):
            if "==>  Preparing: " in row:
                prepare = row.split("==>  Preparing: ")[1]
            if "==> Parameters: " in row:
                params = row.split("==> Parameters: ")[1]
        if prepare is None:
            return False, "sql语句为空，请检查！"
        if params is None:
            return False, "sql参数为空，请检查！"
        placeholders = prepare.count("?")
        paramsSize = params.count(",") + 1
        if placeholders == paramsSize:
            paramList = params.split(",")
            # 清除左右空格
            paramList = [p.strip() for p in paramList]
            # 反转列表以配合pop
            paramList.reverse()
            result = ""
            for str in prepare:
                if str == "?":
                    try:
                        result = result + self.getParamByType(dbType, paramList.pop())
                    except Exception as e:
                        return False, f"格式化sql发生错误：{e}"
                else:
                    result = result + str
            return True, result
        else:
            return False, "sql语句与参数不匹配，请检查！"

    def getIpFromClipboard(self):
        pattern = r'.*://(\d+\.\d+\.\d+\.\d+):.*'
        # 获取系统剪贴板
        clipboard = QApplication.clipboard()
        # 读取剪贴板文本
        clipboard_text = clipboard.text()
        if clipboard_text is not None:
            ip = re.findall(pattern, clipboard_text)
            if len(ip) > 0:
                return ip[0]
        return None

    def genSwitchShell(self, switch):
        try:
            if switch:
                level = "DEBUG"
            else:
                level = "WARN"
            name = self.comboBox.currentText()
            if name in self.loggerDict:
                ip = self.lineEdit.text()
                port = self.spinBox.value()
                package = self.loggerDict.get(name)
                if isinstance(package, list):
                    commands = []
                    for pack in package:
                        data = "{\"{pack}\":\"{level}\"}".replace("{pack}", str(pack)).replace("{level}", level)
                        commands.append(f"""curl --location 'http://{ip}:{port}/nurse-admin-web/tool/logger/updateLevel' \\
--header 'Content-Type: application/json' \\
--data '[{data}]'""")
                    return " \\\n&& \\\n".join(commands)
                else:
                    data = "{\"{package}\":\"{level}\"}".replace("{package}", str(package)).replace("{level}", level)
                    return f"""curl --location 'http://{ip}:{port}/nurse-admin-web/tool/logger/updateLevel' \\
--header 'Content-Type: application/json' \\
--data '[{data}]'"""
        except Exception as e:
            with open("error.txt", "w") as f:
                f.write("生成命令失败：" + str(e))
            QMessageBox.critical(self, '错误', "生成命令失败！详见error.txt")
            os.system("error.txt")
            sys.exit()

    def remenberConfig(self):
        try:
            ip = self.lineEdit.text()
            port = self.spinBox.value()
            currentLoggerName = self.comboBox.currentText()
            loggers = self.config.get("loggers")
            newConfig = ""
            newConfig = newConfig + "{\n"
            newConfig = newConfig + f'  "ip": "{ip}",\n'
            newConfig = newConfig + f'  "port": {port},\n'
            # 打开
            newConfig = newConfig + '  "loggers": [\n'
            newConfig = newConfig + '    {\n'
            newConfig = newConfig + f'      "name": "{currentLoggerName}",\n'
            package = self.loggerDict.get(currentLoggerName)
            if isinstance(package, list):
                newConfig = newConfig + f'      "package": {str(json.dumps(package))}\n'
            else:
                newConfig = newConfig + f'      "package": "{package}"\n'
            newConfig = newConfig + '    },\n'
            loggers = [logger for logger in loggers if logger['name'] != currentLoggerName]
            for logger in loggers[:-1]:
                newConfig = newConfig + '    {\n'
                name = logger.get("name")
                newConfig = newConfig + f'      "name": "{name}",\n'
                package = self.loggerDict.get(name)
                if isinstance(package, list):
                    newConfig = newConfig + f'      "package": {str(json.dumps(package))}\n'
                else:
                    newConfig = newConfig + f'      "package": "{package}"\n'
                newConfig = newConfig + '    },\n'
            # 最后一个
            newConfig = newConfig + '    {\n'
            name = loggers[-1].get("name")
            newConfig = newConfig + f'      "name": "{name}",\n'
            package = self.loggerDict.get(name)
            if isinstance(package, list):
                newConfig = newConfig + f'      "package": {str(json.dumps(package))}\n'
            else:
                newConfig = newConfig + f'      "package": "{package}"\n'
            newConfig = newConfig + '    }\n'
            # 闭合
            newConfig = newConfig + '  ]\n'
            newConfig = newConfig + '}\n'
            with open("config.json", "w", encoding='utf-8') as f:
                f.write(newConfig)
        except Exception as e:
            with open("error.txt", "w") as f:
                f.write("重置配置失败：" + str(e))
            QMessageBox.critical(self, '错误', "重置配置失败！详见error.txt")
            os.system("error.txt")
            sys.exit()

    @pyqtSlot()
    def on_pushButton_clicked(self):
        ip = self.lineEdit.text()
        port = self.spinBox.value()
        if ip == "...":
            QMessageBox.warning(self, "提示", "请填写ip地址")
            return None
        if port <= 0:
            QMessageBox.warning(self, "提示", "端口有误，请检查")
            return None
        clipboard = QApplication.clipboard()
        clipboard.setText(self.genSwitchShell(True))
        QMessageBox.information(self, "提示", f"已将开启命令复制到剪贴板，请前往服务器粘贴执行命令")
        self.remenberConfig()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        ip = self.lineEdit.text()
        port = self.spinBox.value()
        if ip == "...":
            QMessageBox.warning(self, "提示", "请填写ip地址")
            return None
        if port <= 0:
            QMessageBox.warning(self, "提示", "端口有误，请检查")
            return None
        clipboard = QApplication.clipboard()
        clipboard.setText(self.genSwitchShell(False))
        QMessageBox.information(self, "提示", f"已将关闭命令复制到剪贴板，请前往服务器粘贴执行命令")
        self.remenberConfig()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        dbType = self.comboBox_2.currentText()
        success, result = self.formatSql(dbType, clipboard_text)
        if success:
            clipboard.setText(result)
            QMessageBox.information(self, "提示", f"已将格式化的sql复制到剪贴板，请前往数据库粘贴执行sql")
        else:
            if result.startswith("格式化sql发生错误："):
                with open("error.txt", "w") as f:
                    f.write(result)
                QMessageBox.critical(self, '错误', "重置配置失败！详见error.txt")
            else:
                QMessageBox.warning(self, "提示", result)
    def instruction(self):
        QMessageBox.information(self, "使用说明书", "复制命令到nurse-admin后台服务所在服务器并执行即可开启和关闭日志调试！\n开启后在护理管理页面操作报错模块即可在项目目录下的logs/admin-sql.log中生成对应的sql日志\n注意：排查完毕后务必关闭调试，避免占用多余的内存\n格式化sql日志：复制文件admin-sql.log中的sql日志和参数，选择对应数据库类型并格式化即可将sql格式化为可执行sql语句\n本软件绿色无毒，完全免费，请放心使用！\n该软件版权归@医惠小徐所有。")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = adminSqlLogSwitch()
    ui.show()
    sys.exit(app.exec_())
