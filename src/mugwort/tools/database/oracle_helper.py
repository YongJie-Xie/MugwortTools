#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-18 00:20
@Description : TODO 撰写描述
@FileName    : oracle
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
try:
    import dbutils
    import cx_Oracle
except ImportError as e:
    raise ImportError(
        'Tool `database.oracle` cannot be imported.',
        'Please execute `pip install mugwort[database-oracle]` to install dependencies first.'
    )


class OracleHelper:
    """用于快速使用 Oracle 的帮助工具"""
    pass
