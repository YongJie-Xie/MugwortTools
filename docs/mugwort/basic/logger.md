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

![LoggerExample](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/images/LoggerExample-Terminal.png?raw=true)