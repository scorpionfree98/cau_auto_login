import socket
from datetime import datetime
from subprocess import PIPE, run

from cau_auth.src.core import check_status, login

from utils.message import send_excel_online


def check_net_status():
    r = run("ping www.baidu.com", stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
    print(r)
    if r.returncode:
        print("网络已断开")
    else:
        print("正常联网")
    return not r.returncode


def get_ip_address_list():
    ip_addr_list = []
    addrs = socket.getaddrinfo(socket.gethostname(), None)
    for item in addrs:
        ip_addr = item[4][0]
        ip_addr_list.append(ip_addr)
    return ip_addr_list


def my_print(info, user):
    timestamp = datetime.now()

    timestamp_text = timestamp.strftime("%Y/%m/%d %H:%M:%S")
    final_info = f"{timestamp_text}: {info}"
    print(final_info)
    ip_address = "\n".join(get_ip_address_list())

    send_excel_online(
        datetime=timestamp_text, msg=info, user=user, ip_address=ip_address
    )


def main(username, password, device_username):
    # if check_net_status():
    status_info_dict = check_status.check_status()
    is_login = status_info_dict["login"]
    if is_login == 1:
        login_username = status_info_dict["username"]
        my_print(f"账号已经登录，当前登录的用户为:{login_username}", device_username)
    else:
        is_success, msg = login.login(username, password)
        if is_success == 1:
            my_print("登录账户成功", device_username)
        else:
            my_print(f"登录账户失败，错误信息:{msg}", device_username)


def test():
    addrs = socket.getaddrinfo(socket.gethostname(), None)


if __name__ == "__main__":
    username, password, device_username = "学号", "密码", "设备名称"
    main(username, password, device_username)
