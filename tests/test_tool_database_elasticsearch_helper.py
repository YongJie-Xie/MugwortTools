#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-19 13:53
@Description : TODO 撰写描述
@FileName    : test_tool_database_elasticsearch_helper
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.0
"""
import time

from mugwort import Logger
from mugwort.tools.database.elasticsearch_helper import ElasticsearchHelper

logger = Logger('test')
helper = ElasticsearchHelper('https://127.0.0.1:9200', ('elastic', '123456'), verify_certs=False, logger=logger)

index = 'test_helper_%s' % str(int(time.time()))
alias = index + '_alias'


def test_index():
    assert helper.index_create(index=index, refresh_interval='120s') is True
    assert helper.index_exists(index=index) is True
    assert helper.index_get(index=index)[index]['settings']['index']['refresh_interval'] == '120s'
    assert helper.index_delete(index=index) is True


def test_alias():
    helper.index_create(index=index)

    assert helper.alias_create(index=index, name=alias) is True
    assert helper.alias_exists(index=index, name=alias) is True
    assert helper.alias_get(index=index)[index]['aliases'].get(alias) is not None
    assert helper.alias_delete(index=index, name=alias) is True

    helper.index_delete(index=index)


def test_doc():
    helper.index_create(index=index)

    assert helper.doc_create(index=index, id='1', document={'data': 1}) is True
    assert helper.doc_exists(index=index, id='1') is True
    assert helper.doc_update(index=index, id='1', document={'data_extend': 11}) is True
    assert helper.doc_get(index=index, id='1')['_source']['data_extend'] == 11
    assert helper.doc_replace(index=index, id='1', document={'data': 1}) is True
    assert helper.doc_get_source(index=index, id='1').get('data_extend') is None
    assert helper.doc_replace(index=index, id='2', document={'data': 2}) is True
    assert helper.index_refresh(index=index) is True
    assert helper.doc_count(index=index) == 2
    assert helper.doc_delete(index=index, id='2') is True

    helper.index_delete(index=index)


def test_docs():
    helper.index_create(index=index)

    status, body = helper.docs_bulk(index=index, operations=[
        {'index': {'_id': 1}},
        {'data': 1},
        {'create': {'_id': 2}},
        {'data': 2},
    ])
    assert status == 200 and body['errors'] is False

    status, body = helper.docs_multi_get(index=index, ids=['1', '2'])
    assert status == 200 and len(body['docs']) == 2

    helper.index_delete(index=index)


def test_tools():
    helper.index_create(index=index)

    result = helper.bulk(thread_count=2, refresh=True, actions=[
        {'_op_type': 'index', '_index': index, '_id': '1', '_source': {'data': 1}},
        {'_op_type': 'index', '_index': index, '_id': '2', '_source': {'data': 2}},
    ])
    assert all(ok for ok, info in result) is True

    result = helper.bulk(thread_count=1, refresh=True, actions=[
        {'_op_type': 'index', '_index': index, '_id': '3', '_source': {'data': {'key': 'value'}}},
    ])
    assert any(ok for ok, info in result) is False

    result = helper.scan(index=index)
    assert len([x for x in result]) == 2

    helper.index_delete(index=index)
