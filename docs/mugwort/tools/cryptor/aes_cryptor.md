#### AESCryptor

由 **AES** 算法实现的**支持常用加密模式和常用填充方式**的加解密工具，无需实例化即可调用。

- 支持的加密模式
  - CBC、XTS、ECB、OFB、CFB、CFB8、CTR、GCM
- 支持的填充方式
  - PKCS7、ANSIX923
- 代码示例

```python
import os
from mugwort.tools.cryptor import AESCryptor

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

