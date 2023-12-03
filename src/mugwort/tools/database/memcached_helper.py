#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-18 00:23
@Description : TODO 撰写描述
@FileName    : memcached
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.0
"""
try:
    import memcache
except ImportError as e:
    raise ImportError(
        'Tool `database.memcached` cannot be imported.',
        'Please execute `pip install mugwort[database-memcached]` to install dependencies first.'
    )

__all__ = [
    'MemcachedHelper',
]


class MemcachedHelper:
    """用于快速使用 Memcached 的帮助工具"""
    pass
