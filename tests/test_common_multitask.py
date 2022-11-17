#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-07 15:54
@Description : TODO 撰写描述
@FileName    : test_common_multitask
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
from threading import Lock, RLock, Condition, Semaphore, BoundedSemaphore, Event, Barrier
import time
from queue import Queue
from typing import Dict, List

from mugwort import Logger, MultiTask

logger = Logger('Test', level=Logger.INFO, verbose=True)


def task_worker_lock(obj: Lock):
    logger.info('工人已启动，对象类型: %s', type(obj))

    obj.acquire(timeout=3)
    obj.release()

    logger.info('工人已退出')


def test_task_lock():
    for mode in ['thread', 'process']:
        logger.warning('正在实例化 %s 模式的多任务类及多任务变量类', mode)
        multi_task = MultiTask(mode, max_workers=4, logger=logger)

        logger.warning('即将测试 %s 模式的 lock', mode)
        lock = multi_task.variable.get_lock()
        for future in multi_task.submit_maxsize(task_worker_lock, lock):
            assert future.exception() is None


def task_worker_r_lock(obj: RLock):
    logger.info('工人已启动，对象类型: %s', type(obj))

    obj.acquire(timeout=3)
    obj.acquire(timeout=3)
    obj.release()
    obj.release()

    logger.info('工人已退出')


def test_task_r_lock():
    for mode in ['thread', 'process']:
        logger.warning('正在实例化 %s 模式的多任务类及多任务变量类', mode)
        multi_task = MultiTask(mode, max_workers=4, logger=logger)

        logger.warning('即将测试 %s 模式的 r_lock', mode)
        r_lock = multi_task.variable.get_r_lock()
        for future in multi_task.submit_maxsize(task_worker_lock, r_lock):
            assert future.exception() is None


def task_producer_condition(obj: Condition):
    logger.info('生产者已启动，对象类型: %s', type(obj))

    time.sleep(1)
    with obj:
        obj.notify_all()

    logger.info('生产者已退出')


def task_consumer_condition(obj: Condition):
    logger.info('消费者已启动，对象类型: %s', type(obj))

    with obj:
        obj.wait(timeout=3)

    logger.info('消费者已退出')


def test_task_condition():
    for mode in ['thread', 'process']:
        logger.warning('正在实例化 %s 模式的多任务类及多任务变量类', mode)
        multi_task = MultiTask(mode, max_workers=2, logger=logger)

        logger.warning('即将测试 %s 模式的 condition', mode)
        condition = multi_task.variable.get_condition()
        producer_future = multi_task.submit(task_producer_condition, condition)
        consumer_future = multi_task.submit(task_consumer_condition, condition)
        assert producer_future.exception() is None
        assert consumer_future.exception() is None


def task_producer_semaphore(obj: Semaphore):
    logger.info('生产者已启动，对象类型: %s', type(obj))

    obj.release()

    logger.info('生产者已退出')


def task_consumer_semaphore(obj: Semaphore):
    logger.info('消费者已启动，对象类型: %s', type(obj))

    obj.acquire(timeout=3)
    obj.acquire(timeout=3)

    logger.info('消费者已退出')


def test_task_semaphore():
    for mode in ['thread', 'process']:
        logger.warning('正在实例化 %s 模式的多任务类及多任务变量类', mode)
        multi_task = MultiTask(mode, max_workers=2, logger=logger)

        logger.warning('即将测试 %s 模式的 semaphore', mode)
        semaphore = multi_task.variable.get_semaphore(2)
        assert multi_task.submit(task_producer_semaphore, semaphore).exception() is None
        assert multi_task.submit(task_consumer_semaphore, semaphore).exception() is None


def task_worker_bounded_semaphore(obj: BoundedSemaphore):
    logger.info('工人已启动，对象类型: %s', type(obj))

    try:
        obj.release()
    except ValueError:
        pass

    logger.info('工人已退出')


def test_task_bounded_semaphore():
    for mode in ['thread', 'process']:
        logger.warning('正在实例化 %s 模式的多任务类及多任务变量类', mode)
        multi_task = MultiTask(mode, max_workers=1, logger=logger)

        logger.warning('即将测试 %s 模式的 bounded_semaphore', mode)
        bounded_semaphore = multi_task.variable.get_bounded_semaphore(2)
        assert multi_task.submit(task_worker_bounded_semaphore, bounded_semaphore).exception() is None


def task_producer_event(obj: Event):
    logger.info('生产者已启动，对象类型: %s', type(obj))

    obj.set()

    logger.info('生产者已退出')


def task_consumer_event(obj: Event):
    logger.info('消费者已启动，对象类型: %s', type(obj))

    obj.wait(timeout=3)

    logger.info('消费者已退出')


def test_task_event():
    for mode in ['thread', 'process']:
        logger.warning('正在实例化 %s 模式的多任务类及多任务变量类', mode)
        multi_task = MultiTask(mode, max_workers=2, logger=logger)

        logger.warning('即将测试 %s 模式的 event', mode)
        event = multi_task.variable.get_event()
        assert multi_task.submit(task_producer_event, event).exception() is None
        assert multi_task.submit(task_consumer_event, event).exception() is None


def task_worker_barrier(obj: Barrier):
    logger.info('工人已启动，对象类型: %s', type(obj))

    obj.wait(timeout=3)

    logger.info('工人已退出')


def test_task_barrier():
    for mode in ['thread', 'process']:
        logger.warning('正在实例化 %s 模式的多任务类及多任务变量类', mode)
        multi_task = MultiTask(mode, max_workers=4, logger=logger)

        logger.warning('即将测试 %s 模式的 barrier', mode)
        barrier = multi_task.variable.get_barrier(4)
        for future in multi_task.submit_maxsize(task_worker_barrier, barrier):
            assert future.exception() is None


def task_producer_queue(obj: Queue):
    logger.info('生产者已启动，对象类型: %s', type(obj))

    obj.put(1)

    logger.info('生产者已退出')


def task_consumer_queue(obj: Queue):
    logger.info('消费者已启动，对象类型: %s', type(obj))

    value = obj.get(timeout=3)
    if value != 1:
        raise ValueError('value not matched')

    logger.info('消费者已退出')


def test_task_queue():
    for mode in ['thread', 'process']:
        logger.warning('正在实例化 %s 模式的多任务类及多任务变量类', mode)
        multi_task = MultiTask(mode, max_workers=2, logger=logger)

        logger.warning('即将测试 %s 模式的 queue', mode)
        queue = multi_task.variable.get_queue()
        producer_future = multi_task.submit(task_producer_queue, queue)
        consumer_future = multi_task.submit(task_consumer_queue, queue)
        assert producer_future.exception() is None
        assert consumer_future.exception() is None


def task_producer_namespace(obj):
    logger.info('生产者已启动，对象类型: %s', type(obj))

    obj.x = 1

    logger.info('生产者已退出')


def task_consumer_namespace(obj):
    logger.info('消费者已启动，对象类型: %s', type(obj))

    if obj.x != 1:
        raise ValueError('value not matched')

    logger.info('消费者已退出')


def test_task_namespace():
    logger.warning('正在实例化 process 模式的多任务类及多任务变量类')
    multi_task = MultiTask('process', max_workers=2, logger=logger)

    logger.warning('即将测试 process 模式的 namespace')
    namespace = multi_task.variable.get_namespace()
    assert multi_task.submit(task_producer_namespace, namespace).exception() is None
    assert multi_task.submit(task_consumer_namespace, namespace).exception() is None


def task_producer_array(obj):
    logger.info('生产者已启动，对象类型: %s', type(obj))

    try:
        for i in range(len(obj)):
            obj[i] = -obj[i]
    except Exception as e:
        logger.exception(e)
        raise e

    logger.info('生产者已退出')


def task_consumer_array(obj):
    logger.info('消费者已启动，对象类型: %s', type(obj))

    try:
        if len(obj) != 3 or obj[0] != -1 or obj[1] != -2 or obj[2] != -3:
            raise ValueError('value not matched')
    except Exception as e:
        logger.exception(e)
        raise e

    logger.info('消费者已退出')


def test_task_array():
    logger.warning('正在实例化 process 模式的多任务类及多任务变量类')
    multi_task = MultiTask('process', max_workers=2, logger=logger)

    logger.warning('即将测试 process 模式的 array')
    array = multi_task.variable.get_array('i', [1, 2, 3])
    assert multi_task.submit(task_producer_array, array).exception() is None
    assert multi_task.submit(task_consumer_array, array).exception() is None


def task_producer_value(obj):
    logger.info('生产者已启动，对象类型: %s', type(obj))

    obj.value = -obj.value

    logger.info('生产者已退出')


def task_consumer_value(obj):
    logger.info('消费者已启动，对象类型: %s', type(obj))

    if obj.value != -123456:
        raise ValueError('value not matched')

    logger.info('消费者已退出')


def test_task_value():
    logger.warning('正在实例化 process 模式的多任务类及多任务变量类')
    multi_task = MultiTask('process', max_workers=1, logger=logger)

    logger.warning('即将测试 process 模式的 value')
    value = multi_task.variable.get_value('i', 123456)
    assert multi_task.submit(task_producer_value, value).exception() is None
    assert multi_task.submit(task_consumer_value, value).exception() is None


def task_producer_dict(obj: Dict):
    logger.info('工人已启动，对象类型: %s', type(obj))

    obj['b'] = 2

    logger.info('工人已退出')


def task_consumer_dict(obj: Dict):
    logger.info('工人已启动，对象类型: %s', type(obj))

    if obj['a'] != 1 or obj['b'] != 2:
        raise ValueError('value not matched')

    logger.info('工人已退出')


def test_task_dict():
    for mode in ['thread', 'process']:
        logger.warning('正在实例化 %s 模式的多任务类及多任务变量类', mode)
        multi_task = MultiTask(mode, max_workers=2, logger=logger)

        logger.warning('即将测试 %s 模式的 dict', mode)
        dict_variable = multi_task.variable.get_dict({'a': 1})
        assert multi_task.submit(task_producer_dict, dict_variable).exception() is None
        assert multi_task.submit(task_consumer_dict, dict_variable).exception() is None


def task_producer_list(obj: List):
    logger.info('工人已启动，对象类型: %s', type(obj))

    obj.append(2)

    logger.info('工人已退出')


def task_consumer_list(obj: List):
    logger.info('工人已启动，对象类型: %s', type(obj))

    if obj[0] != 1 or obj[1] != 2:
        raise ValueError('value not matched')

    logger.info('工人已退出')


def test_task_list():
    for mode in ['thread', 'process']:
        logger.warning('正在实例化 %s 模式的多任务类及多任务变量类', mode)
        multi_task = MultiTask(mode, max_workers=2, logger=logger)

        logger.warning('即将测试 %s 模式的 list', mode)
        list_variable = multi_task.variable.get_list([1])
        assert multi_task.submit(task_producer_list, list_variable).exception() is None
        assert multi_task.submit(task_consumer_list, list_variable).exception() is None


def main():
    logger.warning('=' * 80)
    test_task_lock()

    logger.warning('=' * 80)
    test_task_r_lock()

    logger.warning('=' * 80)
    test_task_condition()

    logger.warning('=' * 80)
    test_task_semaphore()

    logger.warning('=' * 80)
    test_task_bounded_semaphore()

    logger.warning('=' * 80)
    test_task_event()

    logger.warning('=' * 80)
    test_task_barrier()

    logger.warning('=' * 80)
    test_task_queue()

    logger.warning('=' * 80)
    test_task_namespace()

    logger.warning('=' * 80)
    test_task_array()

    logger.warning('=' * 80)
    test_task_value()

    logger.warning('=' * 80)
    test_task_dict()

    logger.warning('=' * 80)
    test_task_list()


if __name__ == '__main__':
    main()
