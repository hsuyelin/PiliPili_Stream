#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import re
from urllib.parse import urlparse


# noinspection PyBroadException
class StringUtils:

    @staticmethod
    def dir_path_clean(pattern_word, dir_path):
        """
        清理目录路径中的特殊字符，并进行编码

        Parameters:
        - pattern (str): 正则表达式模式
        - dir_path (str): 待清理的目录路径

        Returns:
        - str: 清理后的目录路径
        """
        # 检查目录路径是否为空或非字符串
        if not dir_path or not isinstance(dir_path, str):
            return ""

        # 如果模式为空，则返回原始目录路径
        if not pattern_word:
            return dir_path

        # 在目录路径中查找特定模式
        match = re.search(pattern_word, dir_path, re.IGNORECASE)

        # 如果未找到匹配或匹配组不为空，则返回原始目录路径
        if not match or not match.group(1):
            return dir_path

        try:
            # 清理特殊字符并进行编码
            special_character_mapping = {
                ' ': '%20',
                '"': '%22',
                '#': '%23',
                '%': '%25',
                '&': '%26',
                '(': '%28',
                ')': '%29',
                '+': '%2B',
                ',': '%2C',
                ':': '%3A',
                ';': '%3B',
                '<': '%3C',
                '=': '%3D',
                '>': '%3E',
                '?': '%3F',
                '@': '%40',
                '\\': '%5C',
                '|': '%7C',
		'！': '%EF%BC%81'
            }

            uncleaned_part = match.group(1)
            cleaned_part = ''.join(special_character_mapping.get(char, char) for char in uncleaned_part)
            return dir_path.replace(uncleaned_part, cleaned_part)
        except Exception as e:
            return dir_path

    @staticmethod
    def is_valid_url(url):
        """
        判断 URL 是否合法

        Parameters:
        - url (str): 待验证的 URL

        Returns:
        - bool: 如果 URL 合法，则返回 True，否则返回 False
        """
        if not url or not isinstance(url, str):
            return False
        try:
            parsed_url = urlparse(url)
            return True if parsed_url.scheme and parsed_url.netloc else False
        except Exception as e:
            return False
