#### Clash

支持**订阅更新、节点切换、节点检测**功能的 Clash 代理工具。

- 代码示例

```python
from mugwort.tools.proxy.clash_proxy import ClashProxy, ClashConfig

ClashProxy(ClashConfig(
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
)).startup()
```
