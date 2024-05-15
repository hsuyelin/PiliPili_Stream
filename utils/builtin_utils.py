#!/usr/bin/env python3

# -*- coding: utf-8 -*-


# noinspection PyBroadException
class BuiltinUtils:
    """
    内建工具类，包含一些常用的工具方法
    """

    @staticmethod
    def is_dict_array(obj):
        """
        检查给定对象是否为非空的字典数组

        Parameters:
        - obj: 要检查的对象

        Returns:
        - bool: 如果对象是非空的字典数组则返回True，否则返回False

        """
        if not obj:
            return False
        return isinstance(obj, list) and all(isinstance(item, dict) for item in obj)

    @staticmethod
    def safe_int(obj):
        """
        安全地将对象转换为整数

        Parameters:
        - obj: 待转换的对象

        Returns:
        - int or None: 如果转换成功，返回整数；否则返回None
        """
        if not obj:
            return None
        try:
            return int(obj)
        except Exception as e:
            return None
