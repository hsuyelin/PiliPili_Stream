#!/usr/bin/env python3

# -*- coding: utf-8 -*-


import time
import threading
from collections import OrderedDict
from functools import wraps

lock = threading.RLock()
INSTANCES = OrderedDict()


def singleton(cls):
    """
    装饰器函数，实现单例模式，确保一个类只有一个实例

    Parameters:
    - cls (class): 要应用单例模式的类

    Returns:
    - function: 被装饰后的函数，实现了单例模式
    """
    global INSTANCES

    def _singleton(*args, **kwargs):
        with lock:
            if cls not in INSTANCES:
                INSTANCES[cls] = cls(*args, **kwargs)
        return INSTANCES[cls]

    return _singleton


def retry_when_none(tries=5, delay=3, backoff=2, logger=None, logger_domain=None):
    """
    重试装饰器，用于重复调用函数直到函数返回非None结果

    Parameters:
    - tries: 重试次数，默认为5次
    - delay: 初始延迟时间，默认为3秒
    - backoff: 延迟时间的增加倍数，默认为2
    - logger: 日志记录器对象，用于记录重试信息。默认为None，不记录日志

    Returns:
    - Callable: 装饰后的函数对象

    """
    def decorator_retry(func):
        @wraps(func)
        def wrapper_retry(*args, **kwargs):
            remaining_tries = tries
            current_delay = delay
            while remaining_tries > 0:
                result = func(*args, **kwargs)
                if result is not None:
                    return result
                remaining_tries -= 1
                if remaining_tries > 0:
                    if logger:
                        try:
                            logger.info(logger_domain, f"{current_delay} 秒后重试 ...")
                        except Exception as e:
                            print(f"打印重试失败: {str(e)}")
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper_retry
    return decorator_retry
