# coding:utf8
from pystray import MenuItem as item
import pystray
from PIL import Image
import sudawifi
import win32api
import win10toast

toast = win10toast.ToastNotifier()


def LoginAction():
    """
    Handle Login
    :return:None. Popup a notification bubble, indicating login status
    """
    try:
        res = sudawifi.ScanAndLogin()
    except:
        res = "ERROR Please check your connection"
    # global toast
    toast.show_toast("Login", res, threaded=True, icon_path="Office.ico")


def LogoutAction():
    """
    Handle Logout
    :return:None. Popup a notification bubble, indicating logout status
    """
    res = sudawifi.logout()
    global toast

    # Generate an image
    toast.show_toast("Logout", "Success" if res else "Failed", threaded=True, icon_path="Office.ico")


def Close():
    """
    Call windows api to shutdown the app
    :return:None
    """
    win32api.PostQuitMessage(0)


def setup(iconObject):
    """
    do as documents says to fit OS-X
    :param iconObject:
    :return:None
    """
    iconObject.visible = True


image = Image.open("Office.ico")
menu = (item('auto login', LoginAction),
        item('logout', LogoutAction),
        item('Exit', Close))
icon = pystray.Icon("name", image, "SUDA_WIFI Loginer", menu)
icon.run(setup=setup)
