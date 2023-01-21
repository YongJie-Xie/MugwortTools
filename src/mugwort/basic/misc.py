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

__all__ = [
    'get_filesize_for_human',
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
