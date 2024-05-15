#!/usr/bin/env python3

# -*- coding: utf-8 -*-


import click
import logging


# noinspection SpellCheckingInspection
class LogFormatter(logging.Formatter):
    """
    自定义日志格式类，继承自 logging.Formatter

    Attributes:
    - __level_colors (dict): 日志级别到颜色格式的映射字典
    """

    __level_colors = {
        logging.DEBUG: lambda level_name: click.style(str(level_name), fg="cyan"),
        logging.INFO: lambda level_name: click.style(str(level_name), fg="green"),
        logging.WARNING: lambda level_name: click.style(str(level_name), fg="yellow"),
        logging.ERROR: lambda level_name: click.style(str(level_name), fg="red"),
        logging.CRITICAL: lambda level_name: click.style(str(level_name), fg="bright_red")
    }

    def format(self, record):
        """
        格式化日志记录

        Parameters:
        - record (logging.LogRecord): 日志记录对象

        Returns:
        - str: 格式化后的日志记录
        """
        seperator = " " * (8 - len(record.levelname))
        record.level_text = self.__level_colors[record.levelno](record.levelname + ":") + seperator
        return super().format(record)
