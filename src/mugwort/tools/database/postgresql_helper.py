#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-18 00:18
@Description : TODO 撰写描述
@FileName    : postgresql
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.0
"""
try:
    import dbutils
    import psycopg2
except ImportError as e:
    raise ImportError(
        'Tool `database.postgresql` cannot be imported.',
        'Please execute `pip install mugwort[database-postgresql]` to install dependencies first.'
    )

__all__ = [
    'PostgreSQLHelper',
]


class PostgreSQLHelper:
    """用于快速使用 PostgreSQL 的帮助工具"""
    pass
