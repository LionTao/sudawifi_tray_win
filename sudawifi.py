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
    """
    Performing logging by sending POST to http://a.suda.edu.cn
    :param userAccount:
    :return:Response from portal
    """
    url = "http://a.suda.edu.cn/index.php/index/login"
    form_dict = {"username": userAccount["user"], "password": base64.b64encode(userAccount["pwd"].encode('utf-8'))}
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Connection": "Keep-Alive"}
    logging.debug("sending POST")
    response = requests.post(url=url, data=form_dict, headers=headers)
    response = response.json()
    logging.info("From portal:" + response["info"])
    return response["info"]


def logout():
    """
    send a GET request to logout
    :return: Whether the response is valid
    """
    url = "http://a.suda.edu.cn/index.php/index/logout"
    response = requests.get(url=url)
    if response.status_code != 200:
        logging.warning("Log out Failed!")
        return False
    return True


def pingTest():
    """
    Test network connection
    :return:Whether you are able to visit baidu.com
    """
    try:
        requests.get("http://www.baidu.com", timeout=2)
    except:
        return False
    return True


def portalScan():
    """
    get available ssid
    :return:Whether sudawifi is in range
    """
    res = wifi.getWirelessInterfaces()  # get network interfaces, it's a generator
    ssid = []  # prepare the bucket wo store ssids
    for i in res:  # extract next element from generator
        tmp = wifi.getWirelessAvailableNetworkList(i)  # get Network info from interface, get a list
        for j in tmp:  # for each access point store its ssid
            ssid.append(j.ssid.decode('utf8')) # decode it because it's a byte like object
    # print(ssid)
    return "SUDA_WIFI" in ssid, "SUDA_WIFI_5G" in ssid


def ScanAndLogin():
    """
    perform network scan then login
    :return: success or not
    """
    if not portalScan():
        logging.warning("SUDA_WIFI not in range")
        return "Cannot find SUDA_WIFI"

    global userAccount

    if os.path.exists("account.json"):
        with open("account.json") as f:
            userAccount = json.load(f)

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
    ScanAndLogin()
