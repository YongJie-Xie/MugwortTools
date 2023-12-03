#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-09 10:19
@Description : 用于快速使用 Elasticsearch 的帮助工具
@FileName    : elasticsearch
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.0
"""
import typing as t

from mugwort import Logger

try:
    from elasticsearch import Elasticsearch, ApiError
    from elasticsearch.helpers import streaming_bulk, parallel_bulk, scan
except ImportError:
    raise ImportError(
        'Tool `database.elasticsearch` cannot be imported.',
        'Please execute `pip install mugwort[database-elasticsearch]` to install dependencies first.'
    )

__all__ = [
    'ElasticsearchHelper',
]


class ElasticsearchHelper:
    """用于快速使用 Elasticsearch 的帮助工具"""

    def __init__(
            self,
            hosts: t.Union[str, t.List[t.Union[str, t.Mapping[str, t.Union[str, int]]]]],
            basic_auth: t.Optional[t.Union[str, t.Tuple[str, str]]] = None,
            *,
            verify_certs: bool = True,
            request_timeout: t.Optional[float] = None,
            logger: t.Optional[Logger] = None,
            **kwargs,
    ):
        """
        :param hosts: 主机
        :param basic_auth: 授权认证
        :param verify_certs: 是否校验 SSL 证书
        :param request_timeout: 请求超时时间
        :param logger: 日志类
        """
        self._logger = logger or Logger('ElasticsearchHelper')
        self._client = Elasticsearch(
            hosts,
            basic_auth=basic_auth,
            verify_certs=verify_certs,
            ssl_show_warn=False,
            request_timeout=request_timeout,
            **kwargs,
        )

    @property
    def client(self) -> Elasticsearch:
        return self._client

    # index helper #

    def index_refresh(
            self,
            *,
            index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
            **kwargs,
    ) -> bool:
        """
        刷新索引

        :param index: 目标索引
        :return: 索引刷新结果
        """
        self._logger.debug('refresh index: %s', index)

        try:
            response = self._client.indices.refresh(index=index, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    def index_get(
            self,
            *,
            index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
            **kwargs,
    ) -> t.Optional[t.Dict[str, t.Any]]:
        """
        获取索引信息

        :param index: 目标索引
        :return: 索引信息
        """
        self._logger.debug('get index: %s', index)

        try:
            response = self._client.indices.get(index=index, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return response.body
        return None

    def index_create(
            self,
            *,
            index: str,
            number_of_shards: t.Optional[int] = None,
            number_of_replicas: t.Optional[int] = None,
            refresh_interval: t.Optional[str] = None,
            **kwargs,
    ) -> bool:
        """
        创建索引

        :param index: 目标索引
        :param number_of_shards: 主分片数量，默认使用服务器配置
        :param number_of_replicas: 副本分片数量，默认使用服务器配置
        :param refresh_interval: 分片刷新间隔，默认使用服务器配置
        :return: 索引创建结果
        """
        settings = kwargs.pop('settings', {})
        if number_of_shards is not None:
            settings['number_of_shards'] = number_of_shards
        if number_of_replicas is not None:
            settings['number_of_replicas'] = number_of_replicas
        if refresh_interval is not None:
            settings['refresh_interval'] = refresh_interval
        self._logger.debug('create index: %s, settings: %s', index, settings)

        try:
            response = self._client.indices.create(index=index, settings=settings, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    def index_delete(
            self,
            *,
            index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
            **kwargs,
    ) -> bool:
        """
        删除索引

        :param index: 目标索引
        :return: 索引删除结果
        """
        self._logger.debug('delete index: %s', index)

        try:
            response = self._client.indices.delete(index=index, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    def index_exists(
            self,
            *,
            index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
            **kwargs,
    ) -> bool:
        """
        判断是否存在索引

        :param index: 目标索引
        :return: 索引存在结果
        """
        self._logger.debug('exists index: %s', index)

        try:
            response = self._client.indices.exists(index=index, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    # alias helper #

    def alias_get(
            self,
            *,
            index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
            name: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
            **kwargs,
    ) -> t.Optional[t.Dict[str, t.Any]]:
        """
        获取索引别名信息

        :param index: 目标索引
        :param name: 目标别名
        :return: 索引别名信息
        """
        self._logger.debug('get alias: index=%s, alias=%s', index, name)

        try:
            response = self._client.indices.get_alias(index=index, name=name, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return response.body
        return None

    def alias_create(
            self,
            *,
            index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
            name: str,
            **kwargs,
    ) -> bool:
        """
        创建索引别名

        :param index: 目标索引
        :param name: 目标别名
        :return: 索引别名创建结果
        """
        self._logger.debug('create alias: index=%s, alias=%s', index, name)

        try:
            response = self._client.indices.put_alias(index=index, name=name, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    def alias_delete(
            self,
            *,
            index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
            name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
            **kwargs,
    ) -> bool:
        """
        删除索引别名

        :param index: 目标索引
        :param name: 目标别名
        :return: 索引别名删除结果
        """
        self._logger.debug('delete alias: index=%s, alias=%s', index, name)

        try:
            response = self._client.indices.delete_alias(index=index, name=name, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    def alias_exists(
            self,
            *,
            index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
            name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
            **kwargs,
    ) -> bool:
        """
        判断是否存在索引别名

        :param index: 目标索引
        :param name: 目标别名
        :return: 索引别名存在结果
        """
        self._logger.debug('exists alias: index=%s, alias=%s', index, name)

        try:
            response = self._client.indices.exists_alias(index=index, name=name, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    # single document helper #

    def doc_get(
            self,
            *,
            index: str,
            id: str,
            **kwargs,
    ) -> t.Optional[t.Dict[str, t.Any]]:
        """
        获取文档完整内容

        :param index: 目标索引
        :param id: 目标文档 id
        :return: 文档完整内容
        """
        self._logger.debug('get document: index=%s, id=%s', index, id)

        try:
            response = self._client.get(index=index, id=id, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return response.body
        return None

    def doc_get_source(
            self,
            *,
            index: str,
            id: str,
            **kwargs,
    ) -> t.Optional[t.Dict[str, t.Any]]:
        """
        获取文档原始内容

        :param index: 目标索引
        :param id: 目标文档 id
        :return: 文档原始内容
        """
        self._logger.debug('get document source: index=%s, id=%s', index, id)

        try:
            response = self._client.get_source(index=index, id=id, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return response.body
        return None

    def doc_create(
            self,
            *,
            index: str,
            id: str,
            document: t.Mapping[str, t.Any],
            **kwargs,
    ) -> bool:
        """
        创建文档

        :param index: 目标索引
        :param id: 目标文档 id
        :param document: 文档原始内容
        :return: 文档创建结果
        """
        self._logger.debug('create document: index=%s, id=%s', index, id)

        try:
            response = self._client.create(index=index, id=id, document=document, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    def doc_delete(
            self,
            *,
            index: str,
            id: str,
            **kwargs,
    ) -> bool:
        """
        删除文档

        :param index: 目标索引
        :param id: 目标文档 id
        :return: 文档删除结果
        """
        self._logger.debug('delete document: index=%s, id=%s', index, id)

        try:
            response = self._client.delete(index=index, id=id, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    def doc_update(
            self,
            *,
            index: str,
            id: str,
            document: t.Mapping[str, t.Any],
            **kwargs,
    ) -> bool:
        """
        更新文档

        :param index: 目标索引
        :param id: 目标文档 id
        :param document: 文档更新内容
        :return: 文档更新结果
        """
        self._logger.debug('update document: index=%s, id=%s', index, id)

        try:
            response = self._client.update(index=index, id=id, doc=document, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    def doc_replace(
            self,
            *,
            index: str,
            id: t.Optional[str] = None,
            document: t.Mapping[str, t.Any],
            **kwargs,
    ) -> bool:
        """
        创建或更新文档

        :param index: 目标索引
        :param id: 目标文档 id
        :param document: 文档原始内容
        :return: 文档创建或更新结果
        """
        self._logger.debug('replace document: index=%s, id=%s', index, id)

        try:
            response = self._client.index(index=index, id=id, document=document, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    def doc_exists(
            self,
            *,
            index: str,
            id: str,
            **kwargs,
    ) -> bool:
        """
        判断是否存在文档

        :param index: 目标索引
        :param id: 目标文档 id
        :return: 文档存在结果
        """
        self._logger.debug('exists document: index=%s, id=%s', index, id)

        try:
            response = self._client.exists(index=index, id=id, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    def doc_count(
            self,
            *,
            index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
            **kwargs,
    ) -> t.Optional[int]:
        """
        统计文档

        :param index: 目标索引
        :return: 文档统计结果
        """
        self._logger.debug('count document: %s', index)

        try:
            response = self._client.count(index=index, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return response.body['count']
        return None

    # multi document helper #

    def docs_bulk(
            self,
            *,
            index: t.Optional[str] = None,
            operations: t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]],
            **kwargs,
    ) -> t.Tuple[int, t.Dict[str, t.Any]]:
        """
        批量操作文档

        :param index: 目标索引
        :param operations: 操作列表
        :return: 执行结果
        """
        self._logger.debug('bulk documents: index=%s, len(operations)=%d', index, len(operations))

        response = self._client.bulk(index=index, operations=operations, **kwargs)
        return response.meta.status, response.body

    def docs_mget(
            self,
            *,
            index: t.Optional[str] = None,
            ids: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
            docs: t.Optional[t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]] = None,
            **kwargs,
    ) -> t.Tuple[int, t.Dict[str, t.Any]]:
        """
        批量获取文档

        :param index: 目标索引
        :param ids: 目标文档 id 列表
        :param docs: 需要获取的文档
        :return:
        """
        if index is not None and ids is not None:
            self._logger.debug('get documents: index=%s, len(ids)=%d', index, len(ids))
            response = self._client.mget(index=index, ids=ids, **kwargs)
            return response.meta.status, response.body
        elif docs is not None:
            self._logger.debug('get documents: len(docs)=%d', len(docs))
            response = self._client.mget(docs=docs, **kwargs)
            return response.meta.status, response.body
        else:
            raise ValueError('no valid parameters')

    def docs_reindex(
            self,
            *,
            source: t.Mapping[str, t.Any],
            dest: t.Mapping[str, t.Any],
    ) -> t.Tuple[int, t.Dict[str, t.Any]]:
        """
        重建索引

        :param source: 来源索引配置
        :param dest: 目标索引配置
        :return: 索引重建结果
        """
        self._logger.debug('reindex documents: \nsource=%s\ndest=%d', source, dest)

        response = self._client.reindex(source=source, dest=dest)
        return response.meta.status, response.body

    # search helper #

    def search(
            self,
            *,
            index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
            size: t.Optional[int] = None,
            query: t.Optional[t.Mapping[str, t.Any]] = None,
            aggs: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
            q: t.Optional[str] = None,
            scroll: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
            source: t.Optional[t.Union[bool, t.Mapping[str, t.Any]]] = None,
            **kwargs,
    ) -> t.Tuple[int, t.Dict[str, t.Any]]:
        """
        搜索索引

        :param index: 目标索引
        :param size: 搜索结果大小
        :param query: 搜索目标
        :param aggs: 聚合目标
        :param q: 搜索字符串
        :param scroll: 滚动搜索维持时长
        :param source: 需要的原始字段
        :return: 搜索结果
        """
        self._logger.debug('search document: %s', index)

        response = self._client.search(
            index=index, size=size, query=query, aggs=aggs, q=q, scroll=scroll, source=source, **kwargs,
        )
        return response.meta.status, response.body

    def scroll(
            self,
            *,
            scroll_id: str,
            scroll: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
            **kwargs,
    ) -> t.Tuple[int, t.Dict[str, t.Any]]:
        """
        滚动查询

        :param scroll_id: 滚动查询 id
        :param scroll: 滚动搜索维持时长
        :return: 滚动查询结果
        """
        self._logger.debug('scroll document: %s', scroll_id)

        response = self._client.scroll(scroll_id=scroll_id, scroll=scroll, **kwargs)
        return response.meta.status, response.body

    def scroll_clear(
            self,
            *,
            scroll_id: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
            **kwargs,
    ) -> bool:
        """
        清除滚动查询

        :param scroll_id: 滚动查询 id
        :return: 清除滚动查询结果
        """
        self._logger.debug('clear scroll document: %s', scroll_id)

        try:
            response = self._client.clear_scroll(scroll_id=scroll_id, **kwargs)
        except ApiError as e:
            self._logger.error(e)
        else:
            if 200 <= response.meta.status < 300:
                return True
        return False

    # tools #

    def bulk(
            self,
            *,
            actions: t.Iterable[t.Union[bytes, str, t.Dict[str, t.Any]]],
            chunk_size: int = 500,
            max_chunk_bytes: int = 100 * 1024 * 1024,
            thread_count: int = 1,
            ignore_ok: bool = False,
            **kwargs,
    ) -> t.Iterable[t.Tuple[bool, t.Dict[str, t.Any]]]:
        """
        快速操作工具

        :param actions: 操作列表
        :param chunk_size: 单词文档数量上限
        :param max_chunk_bytes: 单次传输大小上限
        :param thread_count: 执行线程数量
        :param ignore_ok: 是否忽略成功项
        :return: 批量操作结果
        """
        if thread_count > 1:
            for ok, info in parallel_bulk(
                    self._client, actions=actions, chunk_size=chunk_size, max_chunk_bytes=max_chunk_bytes,
                    raise_on_error=False, thread_count=thread_count,
                    **kwargs,
            ):
                if ok and ignore_ok:
                    continue
                yield ok, info
        else:
            for ok, info in streaming_bulk(
                    self._client, actions=actions, chunk_size=chunk_size, max_chunk_bytes=max_chunk_bytes,
                    raise_on_error=False,
                    **kwargs,
            ):
                if ok and ignore_ok:
                    continue
                yield ok, info

    def scan(
            self,
            index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
            size: int = 10000,
            query: t.Optional[t.Mapping[str, t.Any]] = None,
            aggs: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
            q: t.Optional[str] = None,
            scroll: t.Union['t.Literal[-1]', 't.Literal[0]', str] = '15m',
            source: t.Optional[t.Union[bool, t.Mapping[str, t.Any]]] = None,
            get_source: bool = False,
            **kwargs,
    ) -> t.Iterable[t.Dict[str, t.Any]]:
        """
        滚动搜索工具

        :param index: 目标索引
        :param size: 搜索结果大小
        :param query: 搜索目标
        :param aggs: 聚合目标
        :param q: 搜索字符串
        :param scroll: 滚动搜索维持时长
        :param source: 需要的原始字段
        :param get_source: 是否仅获取原始文档
        :return:
        """
        for hit in scan(
                self._client, query=query, scroll=scroll, size=size, index=index, aggs=aggs, q=q, source=source,
                **kwargs,
        ):
            yield hit.get('_source') if get_source else hit
