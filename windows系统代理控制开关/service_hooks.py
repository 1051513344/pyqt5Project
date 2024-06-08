from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/add_proxy')
def add_proxy():
    ip = request.remote_addr
    # 删除文件tinyproxy.conf的最后1行
    filename = '/etc/tinyproxy/tinyproxy.conf'
    num_lines = 1
    with open(filename, 'r') as file:
        lines = file.readlines()
    with open(filename, 'w') as file:
        file.writelines(lines[:-num_lines])
        # 添加ip白名单
        file.writelines(f"Allow {ip}")
    os.system("service tinyproxy restart")
    return '成功!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port='8887', debug=False)
