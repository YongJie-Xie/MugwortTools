#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-18 00:16
@Description : TODO 撰写描述
@FileName    : mongodb
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.0
"""
try:
    import dbutils
    import pymongo
except ImportError:
    raise ImportError(
        'Tool `database.mongodb` cannot be imported.',
        'Please execute `pip install mugwort[database-mongodb]` to install dependencies first.'
    )

__all__ = [
    'MongoDBHelper',
]


class MongoDBHelper:
    """用于快速使用 MongoDB 的帮助工具"""
    pass
