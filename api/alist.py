#!/usr/bin/env python3

# -*- coding: utf-8 -*-


import requests

from utils import RequestUtils, StringUtils
from utils.types import HttpMethod


# noinspection SpellCheckingInspection
class AlistApi:
    __paths = {
        "fs_get": "api/fs/get",
    }
    __request = RequestUtils(session=requests.Session())

    __alist_url = None
    __alist_api_key = None

    def __init__(self, alist_url, alist_api_key):
        """
        初始化 Alist API 对象
        """
        self.__alist_url = alist_url if alist_url and isinstance(alist_url, str) else ""
        if isinstance(self.__alist_url, str) and not self.__alist_url.endswith("/"):
            self.__alist_url += "/"
        self.__alist_api_key = alist_api_key if alist_api_key and isinstance(alist_api_key, str) else ""
        AlistApi.__alist_url = self.__alist_url
        AlistApi.__alist_api_key = self.__alist_api_key

    @classmethod
    def __invoke(cls, method, path, headers=None, **kwargs):
        """
        执行Alist API 请求

        Parameters:
        - path (str): Alist API 请求路径
        - **kwargs: 请求参数

        Returns:
        - dict or None: API 响应的 JSON 数据或 None（请求失败时）
        """
        req_url = cls.__alist_url + path
        if not StringUtils.is_valid_url(req_url):
            return None
        if headers:
            cls.__request.update_headers(headers)
        params = {}
        if kwargs:
            if isinstance(kwargs, dict) and 'body' in kwargs and isinstance(kwargs['body'], dict):
                params.update(kwargs['body'])
            else:
                params.update(kwargs)
        if method == HttpMethod.GET:
            response = cls.__request.get_res(url=req_url, params=params)
        else:
            response = cls.__request.post_res(url=req_url, json=params)
        if not response:
            return None
        return (
            response.json()
            if response and response.status_code == 200 and RequestUtils.check_response_is_valid_json(response)
            else None
        )

    def fetch_file_path(self, emby_path):
        """
        根据 item_id、media_source_id 和 api_key 获取文件路径

        Parameters:
        - emby_path (str): Emby媒体库的 相对路径

        Returns:
        - str: 如果成功找到文件路径，则返回文件路径；否则返回 空字符串
        """
        if not emby_path or not isinstance(emby_path, str):
            return ""

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,zh-Hans;q=0.8,en;q=0.7',
            'authorization': f'{self.__alist_api_key}',
            'cache-control': 'no-cache',
            'content-type': 'application/json;charset=UTF-8',
            'origin': f'{self.__alist_url}',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
        }

        body = {
            "path": emby_path,
            "password": ""
        }

        alist_file_info = self.__invoke(
            HttpMethod.POST,
            self.__paths["fs_get"],
            headers=headers,
            body=body
        )

        if not isinstance(alist_file_info, dict):
            return ""

        alist_file_data = alist_file_info.get("data", {})
        if not alist_file_data or not isinstance(alist_file_data, dict):
            return ""

        return alist_file_data.get("raw_url", "")

    def to_json(self):
        return {
            "alist_api_url": self.__alist_url,
            "alist_api_key": self.__alist_api_key
        }


# noinspection SpellCheckingInspection
if __name__ == "__main__":
    alist_api = AlistApi("http://127.0.0.1:5400", "alist-api-key")
    print(alist_api.to_json())
    print(alist_api.fetch_file_path("/阿里云盘/test.mkv"))