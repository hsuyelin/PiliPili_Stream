#!/usr/bin/env python3

# -*- coding: utf-8 -*-


from typing import Tuple


# noinspection SpellCheckingInspection
class BasePathFixer:

    original_stream_url = None
    backend_url = None
    backend_token = None
    alist_url = None
    alist_api_key = None
    emby_path = None
    media_source_id = None

    def __init__(
        self, 
        original_stream_url, 
        backend_url, 
        backend_token,
        alist_url,
        alist_api_key,
        emby_path, 
        media_source_id
    ):
        self.original_stream_url = original_stream_url
        self.backend_url = backend_url
        self.backend_token = backend_token
        self.alist_url = alist_url
        self.alist_api_key = alist_api_key
        self.emby_path = emby_path
        self.media_source_id = media_source_id

    def fix(self) -> Tuple[str, bool]:
        pass

    def get_stream_url(self) -> str:
        pass
