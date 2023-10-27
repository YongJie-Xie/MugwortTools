# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2023-10-24 16:01
@Description : 支持预估结束时间的统计工具
@FileName    : logger
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.0
"""
import datetime
import time
import typing as t

from .logger import Logger

__all__ = [
    'Counter',
]


class Counter:
    """支持预估结束时间的统计工具"""

    def __init__(
            self,
            title: t.Optional[str],
            total: int = 0,
            interval: int = 10000,
            logger: t.Optional[Logger] = None,
    ):
        self.title = title
        self.total = total
        self.interval = interval
        self.logger = logger or Logger('MugwortCounter')

        self._value = 0
        self._title = f'{title:<60}' if title else ''
        self._start_time = time.time()
        self._monotonic_time = time.monotonic()
        self._printed_value = 0

    def increase(self, value: int = 1):
        """自增函数，支持链式调用打印函数"""
        self._value += value
        return self

    def print(self, *, force: bool = False):
        """打印函数"""
        if force or self.printable:
            self._printed_value = self._value // self.interval * self.interval
            self.logger.info(self)

    @property
    def value(self) -> int:
        return self._value

    @property
    def printable(self) -> bool:
        return self._value - self._printed_value >= self.interval

    @property
    def progress(self) -> str:
        """处理进度"""
        if self.total == 0:
            return f'{self._value:>12}'
        return f'{self._value:>12} / {self.total:<12}'

    @property
    def percentage(self) -> str:
        """完成百分比"""
        if self.total == 0:
            return '100.000%'
        return f'{self._value / self.total * 100:>7.3f}%'

    @property
    def completion_time(self) -> str:
        if self._value == 0:
            return '9999-12-31 23:59:59'
        completed_time = ((time.monotonic() - self._monotonic_time) * self.total / self._value) + self._start_time
        return datetime.datetime.fromtimestamp(completed_time).strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        if self.total == 0:
            return f'{self._title}【{self.progress}】'
        return f'{self._title}（{self.percentage}）【{self.progress}】〈{self.completion_time}〉'
