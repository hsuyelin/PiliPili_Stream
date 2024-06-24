#!/usr/bin/env python3

# -*- coding: utf-8 -*-


from enum import Enum


class HttpMethod(Enum):
    """
    HTTP请求类型的枚举

    Attributes:
    - GET (str): GET请求类型
    - POST (str): POST请求类型
    """
    GET = 'GET'
    POST = 'POST'


class RedirectMode(Enum):
    """
    推流重定向模式枚举

    Attributes:
    - GET (str): GET请求类型
    - POST (str): POST请求类型
    """
    MISAKA = 'MISAKA'
    ALIST = 'ALIST'