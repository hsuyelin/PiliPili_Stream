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
        """
        省略了PiliPili Path fix实现
        """
        return self.original_stream_url, True

    def get_stream_url(self) -> str:
        """
        省略了PiliPili get stream url实现
        """
        return self.original_stream_url
