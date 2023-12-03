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

SUPPORTED_CREATOR = ['MySQLdb', 'pymysql', 'mysql.connector']
for module_name in SUPPORTED_CREATOR:
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

    def __init__(self):
        pass

    def execute(self):
        pass

    def executemany(self):
        pass

    def first(self):
        pass

    def fetchone(self):
        pass

    def fetchmany(self):
        pass

    def fetchall(self):
        pass

    # 业务

    def get_databases(self):
        pass

    def get_tables(self):
        pass

    def get_columns(self):
        pass

    # 数据库

    def database_create(self):
        pass

    def database_delete(self):
        pass

    def database_exists(self):
        pass

    def database_get_create(self):
        pass

    # 数据表

    def table_create(self):
        pass

    def table_delete(self):
        pass

    def table_exists(self):
        pass

    def table_get_create(self):
        pass

    def table_count(self):
        pass

    def table_truncate(self):
        pass

    # 导出

    def dump_database(self):
        pass

    def dump_table(self):
        pass
