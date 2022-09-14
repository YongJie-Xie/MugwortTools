# Mugwort Tools

这是一套由各种小脚本堆砌而成的工具集，主要用于数据治理和爬虫。

## 开始使用

因工具集使用了类型提示，故只能在 Python 3.6 以上环境中运行。

- 快速安装

```shell
pip install mugwort
```

## 工具列表

| 工具名 | 版本 | 描述                               |
| ------ | ---- | ---------------------------------- |
| Logger | 1.0  | 支持控制台输出和文件输出的日志工具 |

### Logger

支持**控制台输出**和**文件输出**的日志工具，支持 ANSI 颜色，日志样式参考 SpringBoot 项目。

- 代码示例

```python
from mugwort import Logger

logger = Logger('foo', Logger.DEBUG, verbose=True)

logger.debug('This is verbose debug log.')
logger.info('This is verbose info log.')
logger.warning('This is verbose warning log.')
logger.error('This is verbose error log.')
logger.critical('This is verbose critical log.')
logger.critical('This is verbose critical log with stack_info.', stack_info=True)

try:
    raise Exception('some exception')
except Exception as e:
    logger.exception(e)
```

- 运行示例

![LoggerExample](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/images/LoggerExample.png?raw=true)

## 更新日志

- 2022-09-14
    - 添加日志工具
