#### X25519Cryptor

由 **X25519** 算法实现的支持**密钥对生成、密钥交换**功能的签名工具，无需实例化即可调用。

- 代码示例
  - 密钥交换，公钥通常是公开的，私钥则仅在本地保存。
  - 通过【我的私钥和对方的公钥】或【我的公钥和对方的私钥】会生成一串相同的密钥。
  - 本示例不模拟密钥传输，而是使用直接生成的两份密钥对。

```python
from mugwort.tools.cryptor import X25519Cryptor

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

