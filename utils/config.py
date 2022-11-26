import configparser
import os.path as osp


class Config:
    def __init__(self, file_path=None) -> None:
        self.config = configparser.ConfigParser()
        if file_path is None:
            file_path = "config-person.ini"
            if not osp.exists(file_path):
                file_path = "config.ini"
        self.file_path = file_path

    def process_user_profile_config(self):
        if osp.exists(self.file_path):
            self.config.read(self.file_path, encoding="utf8")
            profile = (
                self.config["profile"] if "profile" in self.config.sections() else None
            )
        else:
            profile = None
        if profile is None:
            username = input("请输入学号/工号：")
            password = input("请输入密码：")
            device_username = input("请输入设备名称：")
            profile = {}
            profile["username"] = username
            profile["password"] = password
            profile["device_username"] = device_username
            self.config["profile"] = profile
            with open(self.file_path, "w", encoding="utf8") as cfg:
                self.config.write(cfg)
        return profile["username"], profile["password"], profile["device_username"]

    def process_message_config(self):
        if osp.exists(self.file_path):
            self.config.read(self.file_path, encoding="utf8")
            message = (
                self.config["message"] if "message" in self.config.sections() else None
            )
        else:
            message = None
        if message is None:
            default_attention_phone = input("请输入报错时，企业微信联系人手机号(可以不填)：")
            company_redir_sckey = input("请输入中转企业微信密钥(可以不填)：")
            company_redir_url = input("企业微信中转网址(可以不填)：")
            server_jiang_url = input("请输入Server酱网址(可以不填)：")
            hiflow_redir_url = input("Hiflow中转网址(可以不填)：")
            message = {}
            message["default_attention_phone"] = default_attention_phone
            message["company_redir_sckey"] = company_redir_sckey
            message["company_redir_url"] = company_redir_url
            message["server_jiang_url"] = server_jiang_url
            message["hiflow_redir_url"] = hiflow_redir_url
            self.config["message"] = message
            with open(self.file_path, "w", encoding="utf8") as cfg:
                self.config.write(cfg)
        return (
            message["default_attention_phone"],
            message["company_redir_sckey"],
            message["company_redir_url"],
            message["server_jiang_url"],
            message["hiflow_redir_url"],
        )


if __name__ == "__main__":
    config = Config()
    print(config.process_message_config())
    config.process_user_profile_config()
