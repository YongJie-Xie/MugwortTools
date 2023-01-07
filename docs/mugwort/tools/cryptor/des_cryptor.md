#### TripleDESCryptor

由 **3DES** 算法实现的**支持常用加密模式和常用填充方式**且**兼容 DES 算法**的加解密工具，无需实例化即可调用。

- 支持的加密模式
  - CBC、ECB、OFB、CFB、CFB8
- 支持的填充方式
  - PKCS7、ANSIX923
- 代码示例

```python
import os
from mugwort.tools.cryptor import TripleDESCryptor

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

