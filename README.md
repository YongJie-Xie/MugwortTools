# Mugwort Tools

这是一套由各种小脚本堆砌而成的工具集，主要用于数据治理和爬虫。

## 开始使用

因工具集使用了类型提示，故只能在 Python 3.6 以上环境中运行。

- 快速安装

```shell
pip install mugwort
```

- 部分安装

```shell
pip install mugwort[crypto]
pip install mugwort[proxy]
```

- 完整安装（包含完整依赖）

```shell
pip install mugwort[all]
```

## 工具列表

| 工具名    | 版本 | 描述                                           |
| --------- | ---- | ---------------------------------------------- |
| Logger    | 1.1  | 支持控制台输出和文件输出的日志工具             |
| MultiTask | 1.0  | 基于多线程、多进程实现的多任务处理工具         |
| Crypto    | 1.0  | 基于各种算法实现的密码学工具                   |
| Clash     | 1.0  | 支持订阅更新、节点切换、节点检测功能的代理工具 |

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

### Crypto

基于各种算法实现的密码学工具，包含**对称加密解密、非对称密钥对生成、非对称加密解密、非对称签名校验、密钥交换、双因数令牌生成校验**等功能。

- 支持的加密模式
  - CBC、XTS、ECB、OFB、CFB、CFB8、CTR、GCM
- 支持的填充方式
  - PKCS7、ANSIX923

#### AESCryptor

由 **AES** 算法实现的**支持常用加密模式和常用填充方式**的加解密工具，无需实例化即可调用。

- 代码示例

```python
import os
from mugwort.crypto import AESCryptor

key = b'this_is_aes_key.'
iv = os.urandom(16)
ciphertext = AESCryptor.cbc_pkcs7_encryptor(
    data=b'this_is_aes_plaintext.', key=key, iv=iv,
)
plaintext = AESCryptor.cbc_pkcs7_decryptor(
    ciphertext, key, iv
)
print(key, iv, plaintext)
```

#### TripleDESCryptor

由 **3DES** 算法实现的**支持常用加密模式和常用填充方式**且**兼容 DES 算法**的加解密工具，无需实例化即可调用。

- 代码示例

```python
import os
from mugwort.crypto import TripleDESCryptor

# 当密钥长度为 8 时，等价于 DES 算法
key = b'des_key.'
iv = os.urandom(8)
ciphertext = TripleDESCryptor.cbc_pkcs7_encryptor(
    b'this_is_des_plaintext.', key, iv
)
plaintext = TripleDESCryptor.cbc_pkcs7_decryptor(
    ciphertext, key, iv
)
print(key, iv, plaintext)

key = b'this_is_triple_3des_key.'
iv = os.urandom(8)
ciphertext = TripleDESCryptor.cbc_pkcs7_encryptor(
    b'this_is_triple_des_plaintext.', key, iv
)
plaintext = TripleDESCryptor.cbc_pkcs7_decryptor(
    ciphertext, key, iv
)
print(key, iv, plaintext)
```

#### RSACryptor

由 **RSA** 算法实现的支持**密钥对生成、消息加密、消息解密、消息签名、消息校验**功能的加解密及签名工具，无需实例化即可调用。

- 代码示例

```python
from mugwort.crypto import RSACryptor

public_key, private_key = RSACryptor.generate()

# 从本地文件装载
# with open('public_key.pem', 'rb') as pub, open('private_key.pem', 'rb') as priv:
#     public_key = RSACryptor.load_public_key(pub.read())
#     private_key = RSACryptor.load_private_key(priv.read())

ciphertext = RSACryptor.encrypt(public_key, b'this_is_rsa_plaintext.')
print(ciphertext)
plaintext = RSACryptor.decrypt(private_key, ciphertext)
print(plaintext)

signature = RSACryptor.sign(private_key, b'this_is_rsa_plaintext.')
validity = RSACryptor.verify(public_key, b'this_is_rsa_plaintext.', signature)
print(validity, signature)

# 转储到本地文件
# with open('public_key.pem', 'wb') as pub, open('private_key.pem', 'wb') as priv:
#     pub.write(RSACryptor.dump_public_key(public_key))
#     priv.write(RSACryptor.dump_private_key(private_key, password=b'password'))
```

#### Ed25519Cryptor

由 **Ed25519** 算法实现的支持**密钥对生成、消息签名、消息校验**功能的签名工具，无需实例化即可调用。

- 代码示例

```python
from mugwort.crypto import Ed25519Cryptor

public_key, private_key = Ed25519Cryptor.generate()

# 从本地文件装载
# with open('public_key.pem', 'rb') as pub, open('private_key.pem', 'rb') as priv:
#     public_key = Ed25519Cryptor.load_public_key(pub.read())
#     private_key = Ed25519Cryptor.load_private_key(priv.read())

signature = Ed25519Cryptor.sign(private_key, b'this_is_ed25519_plaintext.')
print(signature)
validity = Ed25519Cryptor.verify(public_key, b'this_is_ed25519_plaintext.', signature)
print(validity)

# 转储到本地文件
# with open('public_key.pem', 'wb') as pub, open('private_key.pem', 'wb') as priv:
#     pub.write(Ed25519Cryptor.dump_public_key(public_key))
#     priv.write(Ed25519Cryptor.dump_private_key(private_key, password=b'password'))
```

#### X25519Cryptor

由 **X25519** 算法实现的支持**密钥对生成、密钥交换**功能的签名工具，无需实例化即可调用。

- 代码示例
  - 密钥交换，公钥通常是公开的，私钥则仅在本地保存。
  - 通过【我的私钥和对方的公钥】或【我的公钥和对方的私钥】会生成一串相同的密钥。
  - 本示例不模拟密钥传输，而是使用直接生成的两份密钥对。


```python
from mugwort.crypto import X25519Cryptor

foo_public_key, foo_private_key = X25519Cryptor.generate()
bar_public_key, bar_private_key = X25519Cryptor.generate()

foo_bar_shared_key = X25519Cryptor.exchange(foo_private_key, bar_public_key)
bar_foo_shared_key = X25519Cryptor.exchange(bar_private_key, foo_public_key)
print(foo_bar_shared_key == bar_foo_shared_key, foo_bar_shared_key)

public_key_bytes = X25519Cryptor.dump_public_key(foo_public_key)
private_key_bytes = X25519Cryptor.dump_private_key(foo_private_key)
print(public_key_bytes)
print(private_key_bytes)

# public_key = X25519Cryptor.load_public_key(public_key_bytes)
# private_key = X25519Cryptor.load_private_key(private_key_bytes)
```

#### TOTPCryptor

由**双因素身份验证**相关算法实现的**一次性密码**生成和验证工具，无需实例化即可调用。

- 代码示例

```python
import time
from mugwort.crypto import TOTPCryptor

timestamp = int(time.time())

value = TOTPCryptor.generate(b'this_is_totp_key.', timestamp)
validity = TOTPCryptor.verify(b'this_is_totp_key.', value, timestamp)
print(validity, value.decode())
```

### Proxy

#### Clash

支持**订阅更新**、**节点切换**、**节点检测**功能的 Clash 代理工具。

- 代码示例

```python
from mugwort.proxy import ClashProxy, ClashConfig

ClashProxy(ClashConfig(
    subscribe_link='https://airplane.com/clash-subscribe-link',
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

## 更新日志

- 2022-11-09
    - 添加多任务处理工具

- 2022-10-22
    - 添加代理工具
- 2022-09-18
    - 添加密码学工具
- 2022-09-14
    - 添加日志工具

