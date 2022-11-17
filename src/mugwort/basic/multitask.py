#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-10-22 19:46
@Description : 基于多线程、多进程实现的多任务处理工具
@FileName    : multitask
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
import array
import concurrent.futures
import multiprocessing.managers
import queue
import threading
from typing import Callable, Dict, List, Mapping, Sequence, TypeVar, Union

from .logger import Logger

__all__ = [
    'MultiTask',
    'MultiTaskVariable',
]

_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


class _BoundedPoolExecutor(concurrent.futures.Executor):
    """无界线程有界进程池"""
    _semaphore = None

    def acquire(self):
        self._semaphore.acquire()

    def release(self, fn):  # noqa
        self._semaphore.release()

    def submit(self, fn, *args, **kwargs):
        self.acquire()
        future = super().submit(fn, *args, **kwargs)
        future.add_done_callback(self.release)
        return future


class _ThreadPoolExecutor(concurrent.futures.ThreadPoolExecutor):
    """无界线程池"""
    _max_workers = None

    @property
    def max_workers(self):
        return self._max_workers


class _BoundedThreadPoolExecutor(_BoundedPoolExecutor, _ThreadPoolExecutor):
    """有界线程池"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._semaphore = threading.BoundedSemaphore(self.max_workers)


class _ProcessPoolExecutor(concurrent.futures.ProcessPoolExecutor):
    """无界进程池"""
    _max_workers = None

    @property
    def max_workers(self):
        return self._max_workers


class _BoundedProcessPoolExecutor(_BoundedPoolExecutor, _ProcessPoolExecutor):
    """有界进程池"""
    _max_workers = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._semaphore = multiprocessing.BoundedSemaphore(self.max_workers)

    @property
    def max_workers(self):
        return self._max_workers


class MultiTaskVariable:
    """多线程、多进程共享变量"""
    MODE = ('thread', 'process')

    def __init__(self, mode: str):
        """
        初始化共享变量

        :param mode: 共享变量模式，可选 thread / process 值
        """
        self._mode = mode

        if self._mode not in self.MODE:
            raise ValueError('mode is invalid')

        if self._mode == 'process':
            self._manager = multiprocessing.Manager()

    def __del__(self):
        if hasattr(self, '_manager'):
            self._manager.shutdown()

    @property
    def manager(self) -> multiprocessing.managers.SyncManager:
        """多进程共享数据管理器"""
        return self._manager if self._mode == 'process' else None

    def get_lock(self) -> threading.Lock:
        """
        锁对象：
            实现原始锁对象的类。一旦一个线程获得一个锁，会阻塞随后尝试获得锁的线程，直到它被释放；任何线程都可以释放它。

        使用方式：
            支持上下文管理协议。
            acquire(blocking=True, timeout=- 1) 可以阻塞或非阻塞地获得锁。
            release() 释放一个锁。
            locked() 当锁被获取时，返回 True 。

        相关文档：
            https://docs.python.org/zh-cn/3/library/threading.html#threading.Event
        """
        if self._mode == 'process':
            return self._manager.Lock()
        return threading.Lock()

    def get_r_lock(self):
        """
        重入锁对象：
            此类实现了重入锁对象。重入锁必须由获取它的线程释放。
            一旦线程获得了重入锁，同一个线程再次获取它将不阻塞；
            线程必须在每次获取它时释放一次。

        使用方式：
            支持上下文管理协议。
            acquire(blocking=True, timeout=- 1) 可以阻塞或非阻塞地获得锁。
            release() 释放锁，自减递归等级。

        相关文档：
            https://docs.python.org/zh-cn/3/library/threading.html#threading.RLock
        """
        if self._mode == 'process':
            return self._manager.RLock()
        return threading.RLock()

    def get_condition(self, lock: Union[threading.Lock, threading.RLock] = None) -> threading.Condition:
        """
        条件对象：
            实现条件变量对象的类。一个条件变量对象允许一个或多个线程在被其它线程所通知之前进行等待。

        使用方式：
            支持上下文管理协议。
            acquire(*args) 请求底层锁。
            release() 释放底层锁。
            wait(timeout=None) 等待直到被通知或发生超时。
            wait_for(predicate, timeout=None) 等待，直到条件计算为真。
            notify(n=1) 默认唤醒一个等待这个条件的线程。
            notify_all() 唤醒所有正在等待这个条件的线程。

        相关文档：
            https://docs.python.org/zh-cn/3/library/threading.html#threading.Condition

        :param lock: 底层锁，如果给出了非 None 的 lock 参数，则它必须为 Lock 或者 RLock 对象
        """
        if self._mode == 'process':
            return self._manager.Condition(lock)
        return threading.Condition(lock)

    def get_semaphore(self, value: int = 1) -> threading.Semaphore:
        """
        信号量对象：
            信号量对象管理一个原子性的计数器，代表 release() 方法的调用次数减去 acquire() 的调用次数再加上一个初始值。
            信号量通常用于保护数量有限的资源，例如数据库服务器。

        使用方式：
            支持上下文管理协议。
            acquire(blocking=True, timeout=None) 获取一个信号量。
            release(n=1) 释放一个信号量，将内部计数器的值增加 n 。

        相关文档：
            https://docs.python.org/zh-cn/3/library/threading.html#threading.Semaphore

        :param value: 信号量的初始值
        """
        if self._mode == 'process':
            return self._manager.Semaphore(value)
        return threading.Semaphore(value)

    def get_bounded_semaphore(self, value: int = 1) -> threading.BoundedSemaphore:
        """
        有界信号量对象：
            该类实现有界信号量。有界信号量通过检查以确保它当前的值不会超过初始值。如果超过了初始值，将会引发 ValueError 异常。
            在大多情况下，信号量用于保护数量有限的资源。如果信号量被释放的次数过多，则表明出现了错误。
            没有指定时，参数 value 的值默认为 1 。
            使用有界信号量能减少这种编程错误：信号量的释放次数多于其请求次数。

        使用方式：
            支持上下文管理协议。
            acquire(blocking=True, timeout=None) 获取一个信号量。
            release(n=1) 释放一个信号量，将内部计数器的值增加 n 。

        相关文档：
            https://docs.python.org/zh-cn/3/library/threading.html#threading.BoundedSemaphore

        :param value: 有界信号量的初始值
        """
        if self._mode == 'process':
            return self._manager.BoundedSemaphore(value)
        return threading.BoundedSemaphore(value)

    def get_event(self) -> threading.Event:
        """
        事件对象：
            线程之间通信的最简单机制之一：一个线程发出事件信号，而其他线程等待该信号。
            事件对象管理一个内部标识，调用 set() 方法可将其设置为 True 。调用 clear() 方法可将其设置为 False 。
            调用 wait() 方法将进入阻塞直到标识为 True 。这个标识初始时为 False 。

        使用方式：
            is_set() 当且仅当内部标识为 True 时返回 True 。
            set() 将内部标识设置为 True 。
            clear() 将内部标识设置为 False 。
            wait(timeout=None) 阻塞线程直到内部变量为 True 。

        相关文档：
            https://docs.python.org/zh-cn/3/library/threading.html#threading.Event
        """
        if self._mode == 'process':
            return self._manager.Event()
        return threading.Event()

    def get_barrier(self, parties: int, action: Callable = None, timeout: int = None) -> threading.Barrier:
        """
        栅栏对象：
            创建一个需要 parties 个线程的栅栏对象。如果提供了可调用的 action 参数，它会在所有线程被释放时在其中一个线程中自动调用。
            如果没有在 wait() 方法中指定超时时间的话，参数 timeout 是默认的超时时间。

        使用方式：
            wait(timeout: int) 冲出栅栏。当栅栏中所有线程都已经调用了这个函数，它们将同时被释放。
            reset() 重置栅栏为默认的初始态。
            abort() 使栅栏处于损坏状态。
            parties 冲出栅栏所需要的线程数量。
            n_waiting 当前时刻正在栅栏中阻塞的线程数量。
            broken 一个布尔值，值为 True 表明栅栏为破损态。

        相关文档：
            https://docs.python.org/zh-cn/3/library/threading.html#threading.Barrier

        :param parties: 冲出栅栏所需要的线程数量
        :param action: 可调用对象，它会在所有线程被释放时在其中一个线程中自动调用
        :param timeout: 默认的超时时间
        """
        if self._mode == 'process':
            return self._manager.Barrier(parties, action, timeout)  # noqa
        return threading.Barrier(parties, action, timeout)

    def get_queue(self, maxsize: int = 0) -> queue.Queue:
        """
        队列对象：
            FIFO 队列的构造函数。参数 maxsize 是个整数，用于设置可以放入队列中的项目数的上限。
            当达到这个大小的时候，插入操作将阻塞至队列中的项目被消费掉。
            如果 maxsize 小于等于零，队列尺寸为无限大。

        使用方式：
            qsize() 返回队列的大致大小。
            empty() 如果队列为空，返回 True ，否则返回 False 。
            full() 如果队列是满的返回 True ，否则返回 False 。
            put(item, block=True, timeout=None) 将 item 放入队列。
            put_nowait(item) 相当于 put(item, block=False)。
            get(block=True, timeout=None) 从队列中移除并返回一个项目。
            get_nowait() 相当于 get(False) 。
            task_done() 表示前面排队的任务已经被完成。
            join() 阻塞至队列中所有的元素都被接收和处理完毕。

        相关文档：
            https://docs.python.org/zh-cn/3/library/queue.html#queue.Queue

        :param maxsize: 可以放入队列中的项目数的上限
        """
        if self._mode == 'process':
            return self._manager.Queue(maxsize)
        return queue.Queue(maxsize)

    def get_namespace(self) -> multiprocessing.managers.Namespace:
        """
        命名空间对象：
            命名空间对象没有公共方法，但是拥有可写的属性。直接print会显示所有属性的值。

        使用示例：
            manager = multiprocessing.Manager()
            Global = manager.Namespace()
            Global.x = 10
            Global.y = 'hello'
            Global._z = 12.3  # 所有名称以 '_' 开头的属性都只是代理器上的属性，而不是命名空间对象的属性。

        相关文档：
            https://docs.python.org/zh-cn/3/library/multiprocessing.html#multiprocessing.managers.Namespace
        """
        if self._mode == 'thread':
            raise RuntimeError('Not supported in thread mode')
        return self._manager.Namespace()

    def get_array(self, typecode: str, sequence: Sequence[_T]) -> Sequence[_T]:
        """
        数组代理对象：
            创建一个数组并返回它的代理。

        类型码 typecode 可选值：
            https://docs.python.org/3/library/array.html

        :param typecode: 数组类型
        :param sequence: 初始数组
        """
        if self._mode == 'thread':
            raise RuntimeError('Not supported in thread mode')
        if typecode not in array.typecodes:
            raise ValueError('typecode invalid')
        return self._manager.Array(typecode, sequence)

    def get_value(self, typecode: str, value: _T) -> _T:
        """
        值代理对象：
            创建一个具有可写 value 属性的对象并返回它的代理。

        类型码 typecode 可选值：
            https://docs.python.org/3/library/array.html

        :param typecode: 值类型
        :param value: 初始值
        """
        if self._mode == 'thread':
            raise RuntimeError('Not supported in thread mode')
        if typecode not in array.typecodes:
            raise ValueError('typecode invalid')
        return self._manager.Value(typecode, value)

    def get_dict(self, sequence: Mapping[_KT, _VT] = None) -> Dict[_KT, _VT]:
        """
        字典代理对象：
            创建一个共享的 dict 对象并返回它的代理。

        使用方式：
            允许管理器中列表、字典或者其他 代理对象 对象之间的嵌套。
            d = manager.dict({'a': 1, 'b': 2})
            print(d)  # {'a': 1, 'b': 2}
            d['c'] = 3
            print(d)  # {'a': 1, 'b': 2, 'c': 3}

        :param sequence: 初始字典
        """
        if self._mode == 'process':
            return self._manager.dict(sequence or {})
        return dict(sequence or {})

    def get_list(self, sequence: Sequence[_T] = None) -> List[_T]:
        """
        列表代理对象：
            创建一个共享的 list 对象并返回它的代理。

        使用方式：
            允许管理器中列表、字典或者其他 代理对象 对象之间的嵌套。
            l = manager.list([i*i for i in range(10)])
            print(l)       # [0, 1]
            l.append(2)
            print(l[1:2])  # [1, 2]

        :param sequence: 初始列表
        """
        if self._mode == 'process':
            return self._manager.list(sequence or [])
        return list(sequence or [])


class MultiTask:
    """
    基于多线程、多进程实现的多任务处理工具，减少重复书写非逻辑代码。

    ========= ===============================================================
    模式区别
    ----------------------- -------------------------------------------------
    'thread'                无界线程池，即原生线程池
    'thread' bounded        有界线程池，对 submit 函数进行信号量限制的线程池
    'process'               无界进程池，即原生进程池
    'process' bounded       有界进程池，对 submit 函数进行信号量限制的进程池
    ======================= =================================================
    """
    MODE = ('thread', 'process')
    EXECUTOR_MAP = {
        'thread': [_ThreadPoolExecutor, _BoundedThreadPoolExecutor],
        'process': [_ProcessPoolExecutor, _BoundedProcessPoolExecutor],
    }

    def __init__(self, mode: str, *, bounded: bool = False, max_workers: int = None, logger: Logger = None):
        """
        初始化任务池

        :param mode: 执行器模式，可选 thread / process 值
        :param max_workers: 执行器工人上限
        """
        self._mode = mode
        self._max_workers = max_workers
        self._logger = logger or Logger('MultiTask')

        if self._mode not in self.MODE:
            raise ValueError('mode is invalid')

        self._executor_total = 0
        self._executor_pool = self.EXECUTOR_MAP[mode][bounded](max_workers=max_workers)
        self._logger.info('已初始化 %s 模式任务池，池大小：%d', mode, self._max_workers)

        self._variable = MultiTaskVariable(self._mode)
        self._logger.info('已初始化 %s 模式共享变量', self._mode)

    def __del__(self):
        if hasattr(self, '_executor_pool'):
            self.shutdown()

    def submit(self, fn: Callable, *args, **kwargs) -> concurrent.futures.Future:
        future = self._executor_pool.submit(fn, *args, **kwargs)
        self._executor_total += 1
        self._logger.info('已提交第 %d 个任务', self._executor_total)
        return future

    def submit_maxsize(self, fn: Callable, *args, **kwargs) -> List[concurrent.futures.Future]:
        futures = []
        for _ in range(self._max_workers - self._executor_total):
            future = self.submit(fn, *args, **kwargs)
            futures.append(future)
        return futures

    def shutdown(self):
        self._executor_pool.shutdown()
        self._logger.info('已结束全部任务，累计提交 %d 个任务', self._executor_total)

    @property
    def variable(self) -> MultiTaskVariable:
        return self._variable
