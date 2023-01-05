#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-18 00:13
@Description : TODO 撰写描述
@FileName    : sqlserver
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
try:
    import dbutils
    import pymssql
except ImportError:
    raise ImportError(
        'Tool `database.sqlserver` cannot be imported.',
        'Please execute `pip install mugwort[database-sqlserver]` to install dependencies first.'
    )

__all__ = [
    'SQLServerHelper',
]


class SQLServerHelper:
    """用于快速使用 SQLServer 的帮助工具"""
    pass
