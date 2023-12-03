#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-18 00:22
@Description : TODO 撰写描述
@FileName    : hbase
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.0
"""
try:
    import dbutils
    import phoenixdb
except ImportError as e:
    raise ImportError(
        'Tool `database.hbase` cannot be imported.',
        'Please execute `pip install mugwort[database-hbase]` to install dependencies first.'
    )

__all__ = [
    'HBaseHelper',
]


class HBaseHelper:
    """用于快速使用 HBase 的帮助工具"""
    pass
