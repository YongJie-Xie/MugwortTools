# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-09-12 22:31
@Description : 支持控制台输出和文件输出的日志工具
@FileName    : logger
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.1.1
"""
import io
import logging
import logging.handlers
import os.path
import sys
import time
import typing as t
import warnings

from colorama import init as colorama_init
from colorama.ansi import Fore as AnsiFore, Style as AnsiStyle

__all__ = [
    'Logger',
    'DEBUG',
    'INFO',
    'WARNING',
    'ERROR',
    'CRITICAL',
]

# 支持的日志等级
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL


class Logger:
    """
    支持控制台输出和文件输出的日志工具，支持 ANSI 颜色，日志样式参考 SpringBoot 项目。
    """
    # 支持的日志等级
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(
            self,
            name: str = 'root',
            level: int = logging.INFO,
            *,
            console: bool = True,
            color: bool = True,
            verbose: bool = False,
            rootpath: t.Optional[str] = None,
            logfile: t.Union[str, bool] = False,
            logfile_level: t.Optional[int] = None,
            logfile_mode: str = 'a',
            logfile_encoding: str = 'UTF-8',
    ):
        """
        初始化日志工具

        :param name: 记录器名字
        :param level: 记录器记录等级
        :param console: 是否控制台输出
        :param color: 控制台输出是否着色
        :param verbose: 是否详细输出，包含进程号、线程名称、调用位置
        :param rootpath: 项目根目录，即确定调用位置时的起点
        :param logfile: 是否启用文件记录，可填日志文件路径
        :param logfile_level: 日志文件的记录等级
        :param logfile_mode: 日志文件的模式
        :param logfile_encoding: 日志文件的编码
        """
        # 初始化参数
        if logfile is True:
            logfile = os.path.abspath('%s_%s.log' % (name, time.strftime('%Y%m%d_%H%M%S', time.localtime())))
        if logfile_level is None:
            logfile_level = level

        # 获取记录器实例
        self._logger = logging.getLogger(name)
        self._logger.propagate = False
        self._logger.setLevel(min(level, logfile_level, self._logger.level if self._logger.level else float('inf')))

        if console and color and not self._supports_color():
            color = False
            warnings.warn("当前控制台不支持输出彩色日志。", RuntimeWarning, 2)

        # 获取现有的处理器
        handlers = {}
        for handler in list(self._logger.handlers):
            if hasattr(handler, '_flag'):
                flag = getattr(handler, '_flag')
                handlers[flag] = handler

        # 添加控制台处理器
        if console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(LoggerFormatter(color=color, verbose=verbose, rootpath=rootpath))
            setattr(console_handler, '_flag', 'console')
            self._logger.addHandler(console_handler)

        # 添加文件流处理器
        if logfile:
            logfile_handler = logging.FileHandler(logfile, logfile_mode, encoding=logfile_encoding)
            logfile_handler.setLevel(logfile_level)
            logfile_handler.setFormatter(LoggerFormatter(color=False, verbose=verbose, rootpath=rootpath))
            setattr(logfile_handler, '_flag', 'logfile')
            self._logger.addHandler(logfile_handler)

        # 移除之前的处理器
        for handler in handlers.values():
            self._logger.removeHandler(handler)

    @property
    def logger(self):
        return self._logger

    def debug(self, msg: t.Union[str, t.Any], *args: t.Any, **kwargs: t.Any):
        msg, *args = self._auto_formatter(msg, *args)
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg: t.Union[str, t.Any], *args: t.Any, **kwargs: t.Any):
        msg, *args = self._auto_formatter(msg, *args)
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg: t.Union[str, t.Any], *args: t.Any, **kwargs: t.Any):
        msg, *args = self._auto_formatter(msg, *args)
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg: t.Union[str, t.Any], *args: t.Any, **kwargs: t.Any):
        msg, *args = self._auto_formatter(msg, *args)
        self._logger.error(msg, *args, **kwargs)

    def exception(self, msg: t.Union[str, t.Any], *args: t.Any, exc_info=True, **kwargs: t.Any):
        msg, *args = self._auto_formatter(msg, *args)
        self._logger.error(msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg: t.Union[str, t.Any], *args: t.Any, **kwargs: t.Any):
        msg, *args = self._auto_formatter(msg, *args)
        self._logger.critical(msg, *args, **kwargs)

    @classmethod
    def _supports_color(cls) -> bool:
        """检测控制台是否支持文本着色"""
        if os.name == 'nt':
            return True
        # TODO: 检测 Linux / MacOS 环境的支持情况
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

    @classmethod
    def _auto_formatter(cls, msg: t.Union[str, t.Any], *args: t.Any):
        if not isinstance(msg, str) and args:
            return (' '.join(['%s'] * (len(args) + 1)), msg, *args)
        return (msg, *args)


class LoggerFormatter(logging.Formatter):
    _formatters = {
        'default': '%(datetime)s %(levelname)s : %(message)s',
        'verbose': '%(datetime)s %(levelname)s %(process_id)s --- [%(thread_name)s] %(location)s : %(message)s',
    }
    _styles = {
        logging.DEBUG: ('DEBUG', AnsiFore.LIGHTBLACK_EX),
        logging.INFO: ('INFO', AnsiFore.GREEN),
        logging.WARNING: ('WARN', AnsiFore.YELLOW),
        logging.ERROR: ('ERROR', AnsiFore.RED),
        logging.CRITICAL: ('FATAL', AnsiFore.LIGHTRED_EX + AnsiStyle.BRIGHT),
    }
    _srcfile = os.path.normcase(__file__)
    _location_cache = {}

    def __init__(
            self,
            *,
            color: bool = True,
            verbose: bool = True,
            rootpath: t.Optional[str] = None,
    ):
        self._color = color
        self._verbose = verbose
        if rootpath:
            self._rootpath = os.path.abspath(rootpath)
        elif self._verbose and hasattr(sys.modules['__main__'], '__file__'):
            self._rootpath = os.path.dirname(sys.modules['__main__'].__file__)
        else:
            self._rootpath = None

        # 初始化着色工具
        if color:
            self._tint = lambda text, prefix, suffix=AnsiStyle.RESET_ALL: prefix + text + suffix
        else:
            self._tint = lambda text, prefix, suffix=None: text

        fmt = self._formatters['verbose'] if self._verbose else self._formatters['default']
        super(LoggerFormatter, self).__init__(fmt=fmt, datefmt='%Y-%m-%d %H:%M:%S')

    def format(self, record: logging.LogRecord) -> str:
        levelname, color = self._styles[record.levelno]

        # 解决毫秒大于 999 导致样式错误的问题
        if record.msecs > 999:
            record.msecs = record.msecs % 1000
            record.created = record.created + 1

        # 获取日志信息并着色
        record.datetime = '%s.%03d' % (self.formatTime(record, self.datefmt), record.msecs)
        record.levelname = self._tint('%5s' % levelname, color)
        if self._verbose:
            record.process_id = self._tint('%5s' % record.process, AnsiFore.MAGENTA)
            record.thread_name = '%15s' % record.threadName[-15:]
            record.location = self._tint(self._get_location(limit=40)[-40:], AnsiFore.CYAN)
        record.message = self._tint(record.getMessage(), color)

        formatted = self.formatMessage(record)
        messages = [formatted.rstrip()]

        # 获取异常信息、堆栈信息并着色
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            messages.extend(
                self._tint(self._safe_unicode(line), color)
                for line in record.exc_text.split('\n')
            )
        if record.stack_info:
            messages.extend(
                self._tint(self._safe_unicode(line), color)
                for line in self.formatStack(record.stack_info).split('\n')[:-2]  # 移除当前对象的调用堆栈
            )
        return '\n'.join(messages).replace('\n', '\n    ')

    def _get_location(self, limit: int) -> str:
        # 获取调用位置
        filepath, lineno, func = None, 0, None
        f = logging.currentframe()
        while f and hasattr(f, 'f_code'):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == getattr(logging, '_srcfile') or filename == self._srcfile:
                f = f.f_back
                continue
            filepath, lineno, func = co.co_filename, f.f_lineno, co.co_name
            break

        # 计算相对位置
        if self._rootpath is None:
            self._rootpath = filepath
        if filepath and filepath not in self._location_cache:
            if self._rootpath != os.path.commonpath([filepath, self._rootpath]):
                self._rootpath = os.path.commonpath([filepath, self._rootpath])
                self._location_cache.clear()
            relpath = os.path.relpath(filepath, self._rootpath)
            if relpath == '.':
                relpath = os.path.basename(filepath)
            self._location_cache[filepath] = os.path.splitext(relpath)[0]
        relpath = self._location_cache.get(filepath, '(unknown)')

        # 缩短相对位置
        if (relpath, lineno) not in self._location_cache:
            location = relpath.replace(os.path.sep, '.') + '.' + func + '(),' + str(lineno)
            self._location_cache[(relpath, lineno)] = '%-40s' % self._abbreviate(location, limit)

        return self._location_cache.get((relpath, lineno), '(unknown)')

    @classmethod
    def _abbreviate(cls, location: str, target_length: int) -> str:
        if len(location) <= target_length:
            return location

        right_most_dot_index = location.rindex('.')
        if right_most_dot_index == -1:
            return location

        last_segment_length = len(location) - right_most_dot_index
        left_segments_target_len = target_length - last_segment_length
        if left_segments_target_len < 0:
            left_segments_target_len = 0

        max_possible_trim = len(location) - last_segment_length - left_segments_target_len

        sio = io.StringIO()
        i, trimmed, in_dot_state = 0, 0, True
        while i < right_most_dot_index:
            if location[i] == '.':
                if trimmed >= max_possible_trim:
                    break
                sio.write(location[i])
                in_dot_state = True
            else:
                if in_dot_state:
                    sio.write(location[i])
                    in_dot_state = False
                else:
                    trimmed += 1
            i += 1
        sio.write(location[i:])
        return sio.getvalue()

    @classmethod
    def _safe_unicode(cls, val: t.Union[str, bytes, None]) -> str:
        try:
            if val is None or isinstance(val, str):
                return val
            if isinstance(val, bytes):
                return val.decode('utf-8')
            raise TypeError('Expected bytes, unicode, or None; got %r' % type(val))
        except UnicodeDecodeError:
            return repr(val)


if os.name == 'nt':
    colorama_init()
