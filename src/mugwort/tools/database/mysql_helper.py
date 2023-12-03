#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-18 00:10
@Description : TODO 撰写描述
@FileName    : mysql
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.0
"""
try:
    import dbutils
except ImportError:
    raise ImportError(
        'Tool `database.mysql` cannot be imported.',
        'Please execute `pip install mugwort[database-mysql]` to install dependencies first.'
    )

for module_name in ['MySQLdb', 'pymysql', 'mysql.connector']:
    try:
        __import__(module_name)
        break
    except ImportError:
        pass
else:
    raise ImportError('Creator not found, optional: `mysqlclient`, `pymysql`, `mysql-connector-python`.')

__all__ = [
    'MySQLHelper',
]


class MySQLHelper:
    """用于快速使用 MySQL 的帮助工具"""
    pass
