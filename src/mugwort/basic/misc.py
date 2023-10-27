# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2023-01-09 17:11
@Description : 杂项
@FileName    : misc
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.1
"""
import itertools
import typing as t
from datetime import datetime, timezone, timedelta

__all__ = [
    'get_filesize_for_human',
    'get_iso8601_now',
    'get_iso8601_from_datetime',
    'get_iso8601_from_timestamp',
    'codecs',
    'recovery_garbled_text',
]


def get_filesize_for_human(
        filesize: t.Union[int, float, str],
        precision: int = 1,
) -> str:
    """
    将文件大小处理为人类可读的格式（仿照 Django 框架）

    :param filesize: 待处理文件大小
    :param precision: 保留小数点后的位数
    :return: 人类可读的文件大小
    """
    try:
        filesize = int(filesize)
    except (TypeError, ValueError, UnicodeDecodeError):
        return '0 bytes'

    kb, mb, gb, tb, pb = 1 << 10, 1 << 20, 1 << 30, 1 << 40, 1 << 50

    negative = filesize < 0
    if negative:
        filesize = -filesize

    if filesize < kb:
        value = '1 Byte' if filesize == 1 else '{} Bytes'.format(filesize)
    elif filesize < mb:
        value = '{:.{precision}f} KiB'.format(filesize / kb, precision=precision)
    elif filesize < gb:
        value = '{:.{precision}f} MiB'.format(filesize / mb, precision=precision)
    elif filesize < tb:
        value = '{:.{precision}f} GiB'.format(filesize / gb, precision=precision)
    elif filesize < pb:
        value = '{:.{precision}f} TiB'.format(filesize / tb, precision=precision)
    else:
        value = '{:.{precision}f} PiB'.format(filesize / pb, precision=precision)

    if negative:
        return '-' + value
    return value


def get_iso8601_now(
        tz: t.Optional[timezone] = None,
) -> str:
    """
    获取当前时间的符合 ISO 8601 标准的日期字符串

    :param tz: 输出时使用的时区，默认为本地时区
    :return: 符合 ISO 8601 标准的日期字符串
    """
    utc_datetime = datetime.utcnow().replace(tzinfo=timezone(timedelta(hours=0)))
    return utc_datetime.astimezone(tz=tz).isoformat()


def get_iso8601_from_datetime(
        datetime_string: str,
        datetime_format: str = '%Y-%m-%d %H:%M:%S',
        tz: t.Optional[timezone] = None,
) -> str:
    """
    将日期格式化为 ISO 8601 标准的表达方式

    datetime_format = '%Y-%m-%d %H:%M:%S.%f'
    tz = timezone(timedelta(hours=8))

    :param datetime_string: 待处理日期字符串
    :param datetime_format: 待处理日期字符串的格式
    :param tz: 输出时使用的时区，默认为本地时区
    :return: 符合 ISO 8601 标准的日期字符串
    """
    local_datetime = datetime.strptime(datetime_string, datetime_format)
    return local_datetime.astimezone(tz=tz).isoformat()


def get_iso8601_from_timestamp(
        timestamp: t.Union[int, str],
        tz: t.Optional[timezone] = None,
) -> str:
    """
    将时间戳格式化为 ISO 8601 标准的表达方式

    tz = timezone(timedelta(hours=8))

    :param timestamp: 待处理时间戳（单位：秒）
    :param tz: 输出时使用的时区，默认为本地时区
    :return: 符合 ISO 8601 标准的日期字符串
    """
    if not isinstance(timestamp, int):
        timestamp = int(timestamp)
    if not 32536850399 >= timestamp >= 0:
        raise ValueError('时间戳超出处理范围')
    utc_datetime = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone(timedelta(hours=0)))
    return utc_datetime.astimezone(tz=tz).isoformat()


codecs: t.List[str] = [
    # See: https://docs.python.org/3/library/codecs.html
    'ascii', 'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737', 'cp775', 'cp850',
    'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869',
    'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1125', 'cp1140', 'cp1250', 'cp1251', 'cp1252',
    'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr',
    'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3',
    'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5', 'iso8859_6',
    'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15',
    'iso8859_16', 'johab', 'koi8_r', 'koi8_t', 'koi8_u', 'kz1048', 'mac_cyrillic', 'mac_greek', 'mac_iceland',
    'mac_latin2', 'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213', 'utf_32',
    'utf_32_be', 'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8', 'utf_8_sig',
]


def recovery_garbled_text(
        text: str,
        flag: t.Union[str, t.List[str]] = None,
) -> t.Iterable[t.Tuple[str, str, str]]:
    """
    乱码恢复辅助工具

    :param text: 待恢复的乱码文本
    :param flag: 用于过滤的已知文本或已知文本列表
    :return 编码器、解码器、已恢复文本
    """
    targets: t.Optional[t.List[str]] = [flag] if isinstance(flag, str) else flag
    for codec1, codec2 in itertools.permutations(codecs, 2):
        try:
            fixed_text = text.encode(codec1).decode(codec2)
        except UnicodeError:
            continue
        else:
            if targets and not all(target in fixed_text for target in targets):
                continue
            yield codec1, codec2, fixed_text
