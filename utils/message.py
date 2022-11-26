import json
import traceback
from functools import wraps

import requests

from utils.config import Config

(
    DEFAULT_ATTENTION_PHONE,
    COMPANY_REDIR_SCKEY,
    COMPANY_REDIR_URL,
    SERVER_REDIR_URL,
    HIFLOW_REDIR_URL,
) = Config().process_message_config()


# 装饰器，用于
def wrap_expection_attention(process_type, phone_number=DEFAULT_ATTENTION_PHONE):
    def decorator(func):
        @wraps(func)
        def send_exception_to_messsage(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                exp_str = traceback.format_exc()
                print(exp_str)

                # 避免出现重复报错的情况，如果装饰器本身发送文件，会将process_type设置为非None的情况
                if "stop_warning" in kwargs and kwargs["stop_warning"]:
                    return send_exception_to_messsage

                send_wechat_message(exp_str, phone_number, stop_warning=True)
                send_wechat_message(
                    f"{process_type}程序出现错误",
                    phone_number,
                    stop_warning=True,
                )

        return send_exception_to_messsage

    return decorator


@wrap_expection_attention("get")
def my_get(url, stop_warning=False):
    requests.get(url)


@wrap_expection_attention("post")
def my_post(url, data, stop_warning=False):
    headers = {"Content-Type": "application/json; charset=UTF-8", "Connection": "close"}
    requests.post(url=url, data=json.dumps(data), headers=headers)


def send_excel_online(msg, datetime, user="", ip_address=""):
    hiflow_redirect_url = HIFLOW_REDIR_URL
    if hiflow_redirect_url == "":
        return
    data = {"msg": msg, "datetime": datetime, "user": user, "ip_address": ip_address}
    my_post(hiflow_redirect_url, data)


def send_wechat_message(
    content, mobile=None, sckey=None, msg_type="text", stop_warning=False
):
    """
    content : 发送内容
    mobile : 接收者手机号
    sckey : 用于Server酱的信息发送模块
    msg_type : 目前支持两种发送信息的方式,一种是text,另一种是textcard
    process_type :发送文本的方式
    """
    assert (
        mobile is None and sckey is None
    ), "Mobile and Sckey can't be None at the same time"

    data = {"key": COMPANY_REDIR_SCKEY, "msg": "Hello, World!", "mobile": mobile}
    company_url = COMPANY_REDIR_URL
    if company_url == "":
        return

    if msg_type == "textcard":
        msg_title = content.get("title", None)
        msg_description = content.get("description", None)
        msg_url = content.get("url", None)
        msg_btntxt = content.get("btntxt", None)

        data["type"] = msg_type
        if msg_title is not None:
            data["title"] = msg_title
        if msg_description is not None:
            data["description"] = msg_description
        if msg_url is not None:
            data["url"] = msg_url
        if msg_btntxt is not None:
            data["btntxt"] = msg_btntxt
    else:
        data["msg"] = f"{content}"

    try:
        if sckey is not None:
            url = SERVER_REDIR_URL.format(sckey, content)
            my_get(url, stop_warning=stop_warning)
        tried_time = 0
        while True:
            try:
                my_post(company_url, data, stop_warning=stop_warning)
                break
            except Exception as e:
                tried_time += 1
                if tried_time > 3:
                    raise e
    except:
        traceback.print_exc()
