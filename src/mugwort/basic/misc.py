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


def filesizeformat(filesize: t.Union[int, float, str], precision: int = 1) -> str:
    try:
        filesize = int(filesize)
    except (TypeError, ValueError, UnicodeDecodeError):
        return '0 bytes'

    kb, mb, gb, tb, pb = 1 << 10, 1 << 20, 1 << 30, 1 << 40, 1 << 50

    negative = filesize < 0
    if negative:
        filesize = -filesize

    if filesize < kb:
        value = '1 byte' if filesize == 1 else '{} bytes'.format(filesize)
    elif filesize < mb:
        value = '{:.{precision}f} KB'.format(filesize / kb, precision=precision)
    elif filesize < gb:
        value = '{:.{precision}f} MB'.format(filesize / mb, precision=precision)
    elif filesize < tb:
        value = '{:.{precision}f} GB'.format(filesize / gb, precision=precision)
    elif filesize < pb:
        value = '{:.{precision}f} TB'.format(filesize / tb, precision=precision)
    else:
        value = '{:.{precision}f} PB'.format(filesize / pb, precision=precision)

    if negative:
        return '-' + value
    return value
