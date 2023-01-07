### MultiTask

基于**多线程**、**多进程**实现的多任务处理工具，以及开箱即用的多线程、多进程**数据共享**变量。

- 代码示例

```python
from mugwort import MultiTask

def fn(*args, **kwargs):
    for arg in args:
        print(arg)
    for kw, arg in kwargs.items():
        print(kw, '->', arg)


def main():
    multitask = MultiTask(mode='process', max_workers=4)

    multitask.submit(
        fn,
        multitask.variable.get_lock(),
        multitask.variable.get_r_lock(),
        multitask.variable.get_condition(),
        multitask.variable.get_semaphore(2),
        multitask.variable.get_bounded_semaphore(2),
        multitask.variable.get_event(),
        multitask.variable.get_barrier(2),
        multitask.variable.get_queue(2),
        variable_dict=multitask.variable.get_dict({'a': 1}),
        variable_list=multitask.variable.get_list([1, 2, 3]),
        process_variable_namespace=multitask.variable.get_namespace(),
        process_variable_array=multitask.variable.get_array('i', [1, 2]),
        process_variable_value=multitask.variable.get_value('i', 123456),
    )


if __name__ == '__main__':
    main()
```

### 