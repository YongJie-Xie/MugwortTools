#### RSACryptor

由 **RSA** 算法实现的支持**密钥对生成、消息加密、消息解密、消息签名、消息校验**功能的加解密及签名工具，无需实例化即可调用。

- 代码示例

```python
from mugwort.tools.cryptor import RSACryptor

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

