#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2023-01-13 16:11
@Description : 网络信息处理工具
@FileName    : network
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
import os
import socket
import struct
import typing as t
import urllib.request

from mugwort import Logger

__all__ = [
    'ip_verify',
    'IP2Region',
]


def ip_verify(ip: str) -> bool:
    """检测 IP 有效性"""
    n = ip.split('.')
    if len(n) != 4:
        return False
    return all(x.isdigit() and 0 <= int(x) <= 255 for x in n)


class IP2Region:
    """
    网络地址转地区信息

    数据源来自 https://github.com/lionsoul2014/ip2region 项目
    """
    _ip2region_columns = ('Country', 'Region', 'Province', 'City', 'ISP')

    def __init__(
            self,
            ip2region_dbx_filepath: str = 'ip2region.xdb',
            download_ip2regin_xdb_switch: bool = True,
            logger: t.Optional[Logger] = None
    ):
        self._logger = logger or Logger('IP2Region')

        if not os.path.exists(ip2region_dbx_filepath) and download_ip2regin_xdb_switch:
            self._ip2region_download(ip2region_dbx_filepath)

        if not os.path.exists(ip2region_dbx_filepath):
            raise RuntimeError('没有可用的数据源')

        self._ip2region_dbx = open(ip2region_dbx_filepath, 'rb').read()

    def get_region(self, ip: str) -> dict | None:
        if ip_verify(ip) is False:
            return None

        ip = struct.unpack('!L', socket.inet_aton(ip))[0]

        header_info_length = 256
        vector_index_cols = 256
        vector_index_size = 8
        segment_index_size = 14

        il0 = int((ip >> 24) & 0xFF)
        il1 = int((ip >> 16) & 0xFF)
        idx = il0 * vector_index_cols * vector_index_size + il1 * vector_index_size

        s_ptr = self._get_long(self._ip2region_dbx, header_info_length + idx)
        e_ptr = self._get_long(self._ip2region_dbx, header_info_length + idx + 4)

        data_len = data_ptr = int(-1)
        ll = int(0)
        hh = int((e_ptr - s_ptr) / segment_index_size)
        while ll <= hh:
            m = int((ll + hh) >> 1)
            p = int(s_ptr + m * segment_index_size)

            buffer_sip = self._ip2region_dbx[p:p + segment_index_size]
            sip = self._get_long(buffer_sip, 0)
            if ip < sip:
                hh = m - 1
            else:
                eip = self._get_long(buffer_sip, 4)
                if ip > eip:
                    ll = m + 1
                else:
                    data_len = self._get_int2(buffer_sip, 8)
                    data_ptr = self._get_long(buffer_sip, 10)
                    break

        if data_ptr < 0:
            return None

        buffer_string = self._ip2region_dbx[data_ptr:data_ptr + data_len].decode('utf8')
        return dict(zip(self._ip2region_columns, buffer_string.split('|')))

    def _ip2region_download(self, save_filepath: str):
        download_url = 'https://github.com/lionsoul2014/ip2region/raw/master/data/ip2region.xdb'

        self._logger.info('下载数据文件...')
        urllib.request.urlretrieve(download_url, save_filepath)

    @staticmethod
    def _get_long(b, offset):
        if len(b[offset:offset + 4]) == 4:
            return struct.unpack('I', b[offset:offset + 4])[0]
        return 0

    @staticmethod
    def _get_int2(b, offset):
        return (b[offset] & 0x000000FF) | (b[offset + 1] & 0x0000FF00)
