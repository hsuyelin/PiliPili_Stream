#!/usr/bin/env python3

# -*- coding: utf-8 -*-


import re
import hashlib
from typing import Tuple

from .base_path_fixer import BasePathFixer
from utils.string_utils import StringUtils


# noinspection SpellCheckingInspection
class PiliPiliPathFixer(BasePathFixer):

    def fix(self) -> Tuple[str, bool]:
        # 隐去PliPili Path Fixer实现
        return "", False

    def get_stream_url(self) -> str:
        # 隐去PliPili 获取流地址实现
        return ""
