#!/usr/bin/env python3

# -*- coding: utf-8 -*-


import re
from typing import Tuple

from log.log import logger
from api.alist import AlistApi
from .base_path_fixer import BasePathFixer
from utils.string_utils import StringUtils


# noinspection SpellCheckingInspection
class AlistPathFixer(BasePathFixer):

    def fix(self) -> Tuple[str, bool]:
        if not self.emby_path or not isinstance(self.emby_path, str):
            return self.original_stream_url, True

        fixed_stream_url = re.sub(r"^/*", "/", self.emby_path)
        pattern = r'dir=(.*?)&MediaSourceId='

        return StringUtils.dir_path_clean(pattern, fixed_stream_url), False

    def get_stream_url(self) -> str:
        fixed_path, _ = self.fix()
        return AlistApi(self.alist_url, self.alist_api_key).fetch_file_path(fixed_path)
        
