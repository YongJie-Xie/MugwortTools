# Mugwort Tools

这是一套由各种小脚本堆砌而成的工具集，主要用于数据治理和爬虫。

## 开始使用

因工具集使用了类型提示，故只能在 Python 3.6 以上环境中运行。

- 快速安装

```shell
pip install mugwort
```

- 按需安装

```shell
pip install mugwort[cryptor]
pip install mugwort[database-elasticsearch]
pip install mugwort[proxy-clash]
```

- 完整安装（包含完整依赖）

```shell
pip install mugwort[all]
```

## 工具列表

### Basic

无需安装任何依赖开箱即用的基础工具，包含**日志、多任务处理**等工具。

#### Logger

支持控制台输出和文件输出的日志工具

- 版本：1.1
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/basic/logger.md)

#### MultiTask

基于多线程、多进程实现的多任务处理工具

- 版本：1.0
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/basic/multitask.md)



### Cryptor

基于各种算法实现的密码学工具，包含**对称加密解密、非对称密钥对生成、非对称加密解密、非对称签名校验、密钥交换、双因数令牌生成校验**等功能。

#### AES

由 AES 算法实现，支持**常用加密模式和常用填充方式**的加解密工具

- 版本：1.0
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/tools/cryptor/aes_cryptor.md)

#### TripleDES

由 3DES 算法实现，支持**常用加密模式和常用填充方式且兼容 DES 算法**的加解密工具

- 版本：1.0
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/tools/cryptor/des_cryptor.md)

#### RSA

由 RSA 算法实现，支持**密钥对生成、消息加密、消息解密、消息签名、消息校验功能**的加解密及签名工具

- 版本：1.0
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/tools/cryptor/rsa_cryptor.md)

#### Ed25519

由 Ed25519 算法实现，支持**密钥对生成、消息签名、消息校验功能**的工具

- 版本：1.0
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/tools/cryptor/ed25519_cryptor.md)

#### X25519

由 X25519 算法实现，支持**密钥对生成、密钥交换功能**的工具

- 版本：1.0
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/tools/cryptor/x25519_cryptor.md)

#### TOTP

由双因素身份验证相关算法实现，支持**一次性密码生成和验证**的工具

- 版本：1.0
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/tools/cryptor/totp_cryptor.md)

#### X509

采用 X509 格式标准实现，支持**证书生成、签名**的工具

- 版本：1.0
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/tools/cryptor/x509_cryptor.md)



### Database

常见数据库的帮助工具，主要用于快速进行数据的插入和导出。

#### Elasticsearch

用于快速使用 Elasticsearch 的帮助工具

- 版本：1.0
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/tools/database/elasticsearch_helper.md)



### Proxy

网络代理工具，可以快速启动代理服务器以投入各种需要通过代理出网的工作。

#### Clash

支持**订阅更新、节点切换、节点检测**功能的 Clash 代理工具

- 版本：1.0
- 文档：[点击跳转到说明文档](https://github.com/YongJie-Xie/MugwortTools/blob/main/docs/mugwort/tools/proxy/clash_proxy.md)



## 更新日志

- 2022-12-08
    - 优化密码学工具，添加 X509 证书管理

- 2022-12-30
    - 添加 Elasticsearch 帮助工具

- 2022-11-09
    - 添加多任务处理工具

- 2022-10-22
    - 添加代理工具
- 2022-09-18
    - 添加密码学工具
- 2022-09-14
    - 添加日志工具

