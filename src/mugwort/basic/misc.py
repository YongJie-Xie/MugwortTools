#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2023-01-09 17:11
@Description : 杂项
@FileName    : misc
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
import typing as t
from datetime import datetime, timezone, timedelta

__all__ = [
    'get_filesize_for_human',
    'get_iso8601_now',
    'get_iso8601_by_timestamp',
    'get_iso8601_by_datetime',
]


def get_filesize_for_human(filesize: t.Union[int, float, str], precision: int = 1) -> str:
    """
    将文件大小处理为人类可读的格式

    :param filesize: 待处理文件大小
    :param precision: 保留小数点后的位数
    :return: 人类可读的文件大小
    """
    try:
        filesize = int(filesize)
    except (TypeError, ValueError, UnicodeDecodeError):
        return '0 bytes'

    kb, mb, gb, tb, pb = 1 << 10, 1 << 20, 1 << 30, 1 << 40, 1 << 50

    negative = filesize < 0
    if negative:
        filesize = -filesize

    if filesize < kb:
        value = '1 Byte' if filesize == 1 else '{} Bytes'.format(filesize)
    elif filesize < mb:
        value = '{:.{precision}f} KiB'.format(filesize / kb, precision=precision)
    elif filesize < gb:
        value = '{:.{precision}f} MiB'.format(filesize / mb, precision=precision)
    elif filesize < tb:
        value = '{:.{precision}f} GiB'.format(filesize / gb, precision=precision)
    elif filesize < pb:
        value = '{:.{precision}f} TiB'.format(filesize / tb, precision=precision)
    else:
        value = '{:.{precision}f} PiB'.format(filesize / pb, precision=precision)

    if negative:
        return '-' + value
    return value


def get_iso8601_now(tz: timezone = None):
    """
    获取当前时间的符合 ISO 8601 标准的日期字符串

    :param tz: 输出时使用的时区，默认为本地时区
    :return: 符合 ISO 8601 标准的日期字符串
    """
    utc_datetime = datetime.utcnow().replace(tzinfo=timezone(timedelta(hours=0)))
    return utc_datetime.astimezone(tz=tz).isoformat()


def get_iso8601_by_timestamp(timestamp: t.Union[int, str], tz: timezone = None):
    """
    将时间戳格式化为 ISO 8601 标准的表达方式

    tz = timezone(timedelta(hours=8))

    :param timestamp: 待处理时间戳（单位：秒）
    :param tz: 输出时使用的时区，默认为本地时区
    :return: 符合 ISO 8601 标准的日期字符串
    """
    if not isinstance(timestamp, int):
        timestamp = int(timestamp)
    if not 32536850399 >= timestamp >= 0:
        raise ValueError('时间戳超出处理范围')
    utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone(timedelta(hours=0)))
    return utc_datetime.astimezone(tz=tz).isoformat()


def get_iso8601_by_datetime(datetime_string: str, datetime_format: str = '%Y-%m-%d %H:%M:%S', tz: timezone = None):
    """
    将日期格式化为 ISO 8601 标准的表达方式

    datetime_format = '%Y-%m-%d %H:%M:%S.%f'
    tz = timezone(timedelta(hours=8))

    :param datetime_string: 待处理日期字符串
    :param datetime_format: 待处理日期字符串的格式
    :param tz: 输出时使用的时区，默认为本地时区
    :return: 符合 ISO 8601 标准的日期字符串
    """
    local_datetime = datetime.strptime(datetime_string, datetime_format)
    return local_datetime.astimezone(tz=tz).isoformat()
