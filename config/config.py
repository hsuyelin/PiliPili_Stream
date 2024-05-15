#!/usr/bin/env python3

# -*- coding: utf-8 -*-


from os import path, remove, makedirs
from utils.commons import singleton

import yaml


# noinspection SpellCheckingInspection
@singleton
class Config:
    """
    配置类
    """

    __log_path = None
    __config_path = None
    __config = {}

    def __init__(self):
        __config_path = path.dirname(path.abspath(__file__))

        self.__log_path = path.join(path.dirname(__config_path), "logs")
        if path.exists(self.__log_path) and not path.isdir(self.__log_path):
            remove(self.__log_path)
        if not path.exists(self.__log_path):
            makedirs(self.__log_path, exist_ok=True)

        self.__config_yaml_path = path.join(__config_path, "config.yaml")

        try:
            with open(self.__config_yaml_path, mode="r", encoding="utf-8") as file:
                yaml_content = file.read()
            self.__config = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            print(f"配置文件格式错误：" + str(e))
        except FileNotFoundError:
            print(f"配置文件不存在")
        except Exception as e:
            print(f"加载配置出错：" + str(e))

    def get_config(self, node=None):
        if not node:
            return self.__config
        return self.__config.get(node, {})

    @staticmethod
    def is_user_agent_allowed(user_agent, ua_list):
        """
        检查用户代理字符串是否存在于给定的用户代理列表中

        Parameters:
        - user_agent (str): 要检查的用户代理字符串
        - ua_list (list): 包含允许的用户代理字符串的列表

        Returns:
        - bool: 如果用户代理字符串存在于列表中，则返回 True；否则返回 False
        """
        return any(ua.lower() in user_agent.lower() for ua in ua_list)

    def is_allowed_user_agent(self, user_agent):
        """
        检查用户代理字符串是否在允许的用户代理列表或 Web 用户代理列表中

        Parameters:
        - user_agent (str): 要检查的用户代理字符串

        Returns:
        - bool: 如果用户代理字符串在任一列表中，则返回 True；否则返回 False
        """
        if not self.ua_allow_list and not self.web_ua_allow_list:
            return True
        if "infuse" in user_agent and "direct" not in user_agent:
            return False
        return (self.is_user_agent_allowed(user_agent, self.ua_allow_list) or
                self.is_user_agent_allowed(user_agent, self.web_ua_allow_list))

    @property
    def log_path(self):
        """
        获取 日志保存 根路径

        Returns:
        - str: 日志保存 根路径
        """
        return self.__log_path

    @log_path.setter
    def log_path(self, new_log_path):
        """
        设置 日志保存 根路径

        Parameters:
        - new_log_path: 新的 日志保存 根路径
        """
        self.__log_path = new_log_path

    @property
    def log_level(self):
        """
        获取日志级别

        Returns:
        - str: 日志级别，默认为 DEBUG
        """
        return self.get_config("app").get("log_level", "DEBUG")

    @property
    def emby_url(self):
        """
        获取 Emby 服务器 URL

        Returns:
        - str: Emby 服务器 URL
        """
        return self.get_config("app").get("emby_url", "")

    @property
    def emby_api_key(self):
        """
        获取 Emby API 密钥

        Returns:
        - str: Emby API 密钥
        """
        return self.get_config("app").get("emby_api_key", "")

    @property
    def backend_url(self):
        """
        获取 推流 服务器 URL

        Returns:
        - str: 推流 服务器 URL
        """
        return self.get_config("app").get("backend_url", "")

    @property
    def backend_token(self):
        """
        获取 推流 服务器 Token

        Returns:
        - str: 推流 服务器 Token
        """
        return self.get_config("app").get("backend_token", "")

    @property
    def alist_url(self):
        """
        获取 AList URL

        Returns:
        - str: AList URL
        """
        return self.get_config("app").get("alist_url", "")

    @property
    def alist_api_key(self):
        """
        获取 AList API 密钥

        Returns:
        - str: AList API 密钥
        """
        return self.get_config("app").get("alist_api_key", "")

    @property
    def ua_allow_list(self):
        """
        获取 UA 允许列表

        Returns:
        - list: UA 允许列表
        """
        return self.get_config("app").get("ua_allow_list", [])

    @property
    def web_ua_allow_list(self):
        """
        获取 Web UA 允许列表

        Returns:
        - list: Web UA 允许列表
        """
        return self.get_config("app").get("web_ua_allow_list", [])

    @property
    def national_memorial_day_stream_path(self):
        """
        获取国家纪念日直播流 URL Path

        Returns:
        - str: 国家纪念日直播流 URL Path
        """
        return self.get_config("app").get("national_memorial_day_stream_path", "")

    @property
    def september_18th_incident_stream_path(self):
        """
        获取 9·18 事变直播流 URL Path

        Returns:
        - str: 9·18 事变直播流 URL Path
        """
        return self.get_config("app").get("september_18th_incident_stream_path", "")

    @property
    def forbidden_ua_stream_path(self):
        """
        获取禁止 UA 直播流 URL Path

        Returns:
        - str: 禁止 UA 直播流 URL Path
        """
        return self.get_config("app").get("forbidden_ua_stream_path", "")


# noinspection SpellCheckingInspection
if __name__ == "__main__":
    config = Config()
    print(config.emby_api_key)
    print(config.is_allowed_user_agent("vidhub"))
