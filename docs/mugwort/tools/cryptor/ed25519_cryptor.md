#### Ed25519Cryptor

由 **Ed25519** 算法实现的支持**密钥对生成、消息签名、消息校验**功能的签名工具，无需实例化即可调用。

- 代码示例

```python
from mugwort.tools.cryptor import Ed25519Cryptor

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

