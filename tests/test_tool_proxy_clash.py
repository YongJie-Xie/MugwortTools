#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-11-17 22:48
@Description : TODO 撰写描述
@FileName    : test_tool_proxy_clash
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.0
"""
from mugwort import Logger
from mugwort.tools.proxy.clash_proxy import ClashProxy, ClashConfig

logger = Logger('Test', level=Logger.INFO, verbose=True)
clash_proxy = ClashProxy(ClashConfig(
    logger=logger,
    subscribe_link='https://airport.com/clash-subscribe-link',
    subscribe_include_keywords=['香港'],
    subscribe_exclude_keywords=['过期时间', '剩余流量', '官网'],
    watcher_blocking=True,
    # 默认每天凌晨两点更新订阅
    # watcher_job_updater_enable=True,
    # watcher_job_updater_config={'trigger': 'cron', 'hour': 2},
    # 默认每间隔一小时切换节点
    # watcher_job_changer_enable=True,
    # watcher_job_changer_config={'trigger': 'interval', 'hours': 1},
    # 默认每间隔三十秒检测节点
    # watcher_job_checker_enable=True,
    # watcher_job_checker_config={'trigger': 'interval', 'seconds': 30},
))
clash_proxy.startup()


def test_proxy_clash():
    pass
