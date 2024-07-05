#!/usr/bin/env python3

# -*- coding: utf-8 -*-


import json
from flask import request, redirect

from log.log import logger
from api.emby import EmbyApi
from config.config import Config
from utils.commons import singleton
from utils.date_utils import DateUtils
from utils.types import RedirectMode
from .pilipili_path_fixer import PiliPiliPathFixer
from .alist_path_fixer import AlistPathFixer


# noinspection SpellCheckingInspection
@singleton
class Stream:

    __emby_url = None
    __emby_api_key = None
    __backend_url = None
    __backend_token = None
    __alist_url = None
    __alist_api_key = None
    __emby_api = None
    __alist_api = None

    __redirect_mode = RedirectMode.MISAKA

    def __init__(
        self, 
        emby_url, 
        emby_api_key, 
        backend_url, 
        backend_token, 
        alist_url, 
        alist_api_key
    ):
        """
        初始化 Stream 对象
        """
        self.__emby_url = emby_url
        self.__emby_api_key = emby_api_key
        self.__backend_url = backend_url
        self.__backend_token = backend_token
        self.__emby_api = EmbyApi(emby_url, emby_api_key)
        self.__redirect_mode = RedirectMode.MISAKA
        if alist_url and alist_api_key:
            self.__alist_url = alist_url
            self.__alist_api_key = alist_api_key
            self.__redirect_mode = RedirectMode.ALIST

    def redirect_internal(self, url, item_id, media_source_id, api_key):
        logger.info(f"[{item_id}] -> 开始处理推流请求，当前参数: {self.to_json()}")
        headers = dict(request.headers)
        if headers:
            logger.info(f"[{item_id}] -> 请求头: {json.dumps(headers, ensure_ascii=False)}")
        user_agent = request.headers.get("User-Agent", "")
        logger.info(f"[{item_id}] -> 当前UA：{user_agent}")

        is_allowed = Config().is_allowed_user_agent(user_agent)
        emby_path = self.__emby_api.fetch_file_path(item_id, media_source_id, api_key)

        if not is_allowed:
            logger.info(
                f"[{item_id}] -> 当前UA不被允许，播放PiliPili Sorry -> {Config().forbidden_ua_stream_path}"
            )
            emby_path = Config().forbidden_ua_stream_path if\
                Config().forbidden_ua_stream_path else emby_path
        if DateUtils.is_today_national_memorial_day():
            logger.info(
                f"[{item_id}] -> 当前为国家公祭日时间，播放爱国主义教育视频 -> {Config().national_memorial_day_stream_path}"
            )
            emby_path = Config().national_memorial_day_stream_path if\
                Config().national_memorial_day_stream_path else emby_path
        if DateUtils.is_today_september_18th_incident():
            logger.info(
                f"[{item_id}] -> 当前为9·18纪念日时间，播放爱国主义教育视频 -> {Config().september_18th_incident_stream_path}"
            )
            emby_path = Config().september_18th_incident_stream_path if\
                Config().september_18th_incident_stream_path else emby_path

        if not emby_path:
            logger.info(f"[{item_id}] -> 未获取到 EmbyPath")
            return redirect(Config().forbidden_ua_stream_path)

        logger.info(f"[{item_id}] -> EmbyPath -> {emby_path}")

        if self.__redirect_mode == RedirectMode.MISAKA:
            path_fixer = PiliPiliPathFixer(
                url, 
                self.__backend_url, 
                self.__backend_token,
                None,
                None,
                emby_path, 
                media_source_id
            )
            logger.info(f"[{item_id}] -> 推流后端URL：{self.__backend_url} -> 推流后端Token：{self.__backend_token}")
        else:
            path_fixer = AlistPathFixer(
                url, 
                None, 
                None,
                self.__alist_url,
                self.__alist_api_key,
                emby_path, 
                None
            )
            logger.info(f"[{item_id}] -> EmbyPath -> {emby_path} -> "
                        f"推流后端URL：{self.__alist_url} -> 推流后端Token：{self.__alist_api_key}")

        stream_url = path_fixer.get_stream_url()
        logger.info(f"[{item_id}] -> 推流URL：{stream_url}\n\n")
        return redirect(stream_url)

    def to_json(self):
        return {
            "emby_url": self.__emby_url or "",
            "emby_api_key": self.__emby_api_key or "",
            "backend_url": self.__backend_url or "",
            "backend_token": self.__backend_token or "",
            "alist_url": self.__alist_url or "",
            "alist_api_key": self.__alist_api_key or ""
        }
