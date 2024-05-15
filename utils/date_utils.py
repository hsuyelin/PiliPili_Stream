#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from datetime import datetime


# noinspection PyBroadException
class DateUtils:

    @staticmethod
    def is_today_national_memorial_day():
        """
        检查当前日期是否是国家公祭日

        Returns:
        - bool: 如果当前日期是国家公祭日的10:00或11:00，则返回 True，否则返回 False
        """
        date = datetime.now()
        if date.month != 12 or date.day != 13:
            return False
        if date.hour == 10:
            return True
        if date.hour == 11 and date.minute == 0:
            return True
        return False

    @staticmethod
    def is_today_september_18th_incident():
        """
        检查当前日期是否是国难日

        Returns:
        - bool: 如果当前日期是国难日的10:00或11:00，则返回 True，否则返回 False
        """
        date = datetime.now()
        if date.month != 9 or date.day != 18:
            return False
        if date.hour == 10:
            return True
        if date.hour == 11 and date.minute == 0:
            return True
        return False
