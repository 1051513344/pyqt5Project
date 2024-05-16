import requests
import urllib3

def isWifiLogin():
    urllib3.disable_warnings()
    try:
        request = requests.get("https://www.baidu.com", verify=False)
        resp = request.content.decode("utf-8")
        request.close()
        if "<title>百度一下，你就知道</title>" in resp:
            return True
        return False
    except Exception as e:
        return False
