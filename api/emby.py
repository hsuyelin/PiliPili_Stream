#!/usr/bin/env python3

# -*- coding: utf-8 -*-


import requests

from utils import BuiltinUtils, RequestUtils, StringUtils
from utils.types import HttpMethod


# noinspection SpellCheckingInspection
class EmbyApi:
    __paths = {
        "playback_info": "Items/%s/PlaybackInfo",
    }
    __request = RequestUtils(session=requests.Session())

    __emby_url = None
    __emby_api_key = None

    def __init__(self, emby_url, emby_api_key):
        """
        初始化 Emby API 对象
        """
        self.__emby_url = emby_url if emby_url and isinstance(emby_url, str) else ""
        if isinstance(self.__emby_url, str) and not self.__emby_url.endswith("/"):
            self.__emby_url += "/"
        self.__emby_api_key = emby_api_key if emby_api_key and isinstance(emby_api_key, str) else ""
        EmbyApi.__emby_url = self.__emby_url
        EmbyApi.__emby_api_key = self.__emby_api_key

    @classmethod
    def __invoke(cls, method, path, headers=None, **kwargs):
        """
        执行Emby API 请求

        Parameters:
        - path (str): Emby API 请求路径
        - **kwargs: 请求参数

        Returns:
        - dict or None: API 响应的 JSON 数据或 None（请求失败时）
        """
        req_url = cls.__emby_url + path
        if not StringUtils.is_valid_url(req_url):
            return None
        if headers:
            cls.__request.update_headers(headers)
        params = {}
        if kwargs:
            params.update(kwargs)
        if method == HttpMethod.GET:
            response = cls.__request.get_res(url=req_url, params=params)
        else:
            response = cls.__request.post_res(url=req_url, params=params)
        if not response:
            return None
        return (
            response.json()
            if response and response.status_code == 200 and RequestUtils.check_response_is_valid_json(response)
            else None
        )

    def fetch_file_path(self, item_id, media_source_id, api_key):
        """
        根据 item_id、media_source_id 和 api_key 获取文件路径

        Parameters:
        - item_id (str): 媒体文件的 ID
        - media_source_id (str): 媒体源的 ID
        - api_key (str, optional): Emby API 密钥。如果未提供，则使用默认密钥

        Returns:
        - str: 如果成功找到文件路径，则返回文件路径；否则返回 空字符串
        """
        if not item_id or not isinstance(item_id, str):
            return ""

        if not media_source_id or not isinstance(media_source_id, str):
            return ""

        api_key = api_key if api_key and isinstance(api_key, str) else self.__emby_api_key
        play_back_info = self.__invoke(
            HttpMethod.GET,
            self.__paths["playback_info"] % item_id,
            item_id,
            MediaSourceId=media_source_id,
            api_key=api_key
        )

        if not isinstance(play_back_info, dict):
            return ""

        media_sources = play_back_info.get("MediaSources", [])
        if not media_sources or not BuiltinUtils.is_dict_array(media_sources):
            return ""

        for media_source in media_sources:
            if "Id" in media_source and media_source.get("Id", "") == media_source_id:
                return media_source.get("Path", "")

        return ""

    def to_json(self):
        return {
            "emby_api_url": self.__emby_url,
            "emby_api_key": self.__emby_api_key
        }


# noinspection SpellCheckingInspection
if __name__ == "__main__":
    emby_api = EmbyApi("http://localhost:8000", "api_key")
    print(emby_api.to_json())