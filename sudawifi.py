import requests
import base64
import logging
import win32wifi.Win32Wifi as wifi
import os
import json

PATH = "account.json"
userAccount = {"user": None, "pwd": None}
logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)


def login(userAccount):
    url = "http://a.suda.edu.cn/index.php/index/login"
    form_dict = {"username": userAccount["user"], "password": base64.b64encode(userAccount["pwd"].encode('utf-8'))}
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Connection": "Keep-Alive"}
    logging.debug("sending POST")
    response = requests.post(url=url, data=form_dict, headers=headers)
    response = response.json()
    logging.info("From portal:" + response["info"])


def logout():
    url = "http://a.suda.edu.cn/index.php/index/logout"
    response = requests.get(url=url)
    if response.status_code != 200:
        logging.warning("Log out Failed!")
        return False
    return True


def pingTest():
    try:
        requests.get("http://www.baidu.com", timeout=2)
    except:
        return False
    return True


def portalScan():
    res = wifi.getWirelessInterfaces()
    ssid = []
    for i in res:
        tmp = wifi.getWirelessAvailableNetworkList(i)
        for j in tmp:
            ssid.append(j.ssid.decode('utf8'))
    # print(ssid)
    return "SUDA_WIFI" in ssid, "SUDA_WIFI_5G" in ssid


def ScanAndLogin():
    if not portalScan():
        logging.warning("SUDA_WIFI not in range")
        return "Cannot find SUDA_WIFI"

    if os.path.exists("account.json"):
        with open("account.json") as f:
           userAccount=json.load(f)

    if userAccount['user'] == None:
        print("username: ", end='')
        userAccount["user"] = input()
        print("password: ", end='')
        userAccount["pwd"] = input()
    login(userAccount=userAccount)
    if pingTest():
        print("SUCCESS !!!!!!!!")
        return "Login Success"
    else:
        print("NOOOOOOOOOO")
        return "NOOOOOOOOOO"


if __name__ == '__main__':
    # res=portalScan()
    # print(res)
    # print("SUDA_WIFI" in res or "SUDA_WIFI_5G" in res)
    # print(portalScan())
    # ScanAndLogin()
    print(wifi.connect())
