#!/usr/bin/env python3

# -*- coding: utf-8 -*-


from typing import Tuple


# noinspection SpellCheckingInspection
class BasePathFixer:
    original_stream_url = None
    backend_url = None
    backend_token = None
    emby_path = None
    media_source_id = None

    def __init__(self, original_stream_url, backend_url, backend_token, emby_path, media_source_id):
        self.original_stream_url = original_stream_url
        self.backend_url = backend_url
        self.backend_token = backend_token
        self.emby_path = emby_path
        self.media_source_id = media_source_id

    def fix(self) -> Tuple[str, bool]:
        pass

    def get_stream_url(self) -> str:
        pass
