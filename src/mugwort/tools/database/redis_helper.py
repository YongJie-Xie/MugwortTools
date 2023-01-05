#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-18 00:23
@Description : TODO 撰写描述
@FileName    : redis
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
try:
    import redis_helper
except ImportError as e:
    raise ImportError(
        'Tool `database.redis` cannot be imported.',
        'Please execute `pip install mugwort[database-redis]` to install dependencies first.'
    )

__all__ = [
    'RedisHelper',
]


class RedisHelper:
    """用于快速使用 Redis 的帮助工具"""
    pass
