#!/usr/bin/env python3

# -*- coding: utf-8 -*-


from flask import Flask, request

from config.config import Config
from stream.stream import Stream

app = Flask(__name__)


def get_stream():
    """
    获取 Stream 实例

    Returns:
    - Stream: Stream 实例
    """
    return Stream(
        emby_url=Config().emby_url,
        emby_api_key=Config().emby_api_key,
        backend_url=Config().backend_url,
        backend_token=Config().backend_token,
        alist_url=Config().alist_url,
        alist_api_key=Config().alist_api_key
    )


def redirect_common(request_obj, item_id):
    """
    处理通用的重定向请求

    Parameters:
    - request_obj (Request): 请求对象
    - item_id (str): 媒体文件的唯一标识符

    Returns:
    - Response: 重定向响应
    """
    media_source_id = request_obj.args.get("MediaSourceId", "")
    api_key = request_obj.args.get("api_key", "") if request_obj.args.get("api_key", "") else Config().emby_api_key
    return get_stream().redirect_internal(
        url=request_obj.url,
        item_id=item_id,
        media_source_id=media_source_id,
        api_key=api_key
    )


@app.route("/videos/<item_id>/original.<media_type>", methods=["GET"])
def redirect_yamby_original(item_id, media_type):
    """
    处理推流请求，一般是Yamby客户端

    参数:
    - item_id (str): 媒体文件的唯一标识符
    - media_type (str): 媒体文件的类型（如mp4、mkv等）
    """
    return redirect_common(request, item_id)


@app.route("/emby/videos/<item_id>/original.<media_type>", methods=["GET"])
def redirect_emby_original(item_id, media_type):
    """
    处理推流请求，一般是不扫库的Emby客户端连接且服务端版本>=4.8.0.39

    参数:
    - item_id (str): 媒体文件的唯一标识符
    - media_type (str): 媒体文件的类型（如mp4、mkv等）
    """
    return redirect_common(request, item_id)


@app.route("/emby/videos/<item_id>/stream.<media_type>", methods=["GET"])
def redirect_old_emb_stream(item_id, media_type):
    """
    处理推流请求，一般是Emby老官方客户端

    参数:
    - item_id (str): 媒体文件的唯一标识符
    - media_type (str): 媒体文件的类型（如mp4、mkv等）
    """
    return redirect_common(request, item_id)


@app.route('/Videos/<item_id>/original', methods=["GET"])
def redirect_old_emby_original(item_id):
    """
    处理推流请求，一般是不扫库的Emby客户端连接且服务端版本 < 4.8.0.39

    参数:
    - item_id (str): 媒体文件的唯一标识符
    """
    return redirect_common(request, item_id)


@app.route('/Videos/<item_id>/stream', methods=["GET"])
def redirect_infuse_stream(item_id):
    """
    处理推流请求，一般是Infuse客户端连接

    参数:
    - item_id (str): 媒体文件的唯一标识符
    """
    return redirect_common(request, item_id)


@app.route('/emby/Videos/<item_id>/stream.<media_type>', methods=["GET"])
def redirect_conflux_stream(item_id, media_type):
    """
    处理推流请求，一般是Conflux客户端连接

    参数:
    - item_id (str): 媒体文件的唯一标识符
    - media_type (str): 媒体文件的类型（如mp4、mkv等）
    """
    return redirect_common(request, item_id)
