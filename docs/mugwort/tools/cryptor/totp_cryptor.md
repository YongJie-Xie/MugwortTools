#### TOTPCryptor

由**双因素身份验证**相关算法实现的**一次性密码**生成和验证工具，无需实例化即可调用。

- 代码示例

```python
import time
from mugwort.tools.cryptor import TOTPCryptor

timestamp = int(time.time())

value = TOTPCryptor.generate(b'this_is_totp_key.', timestamp)
validity = TOTPCryptor.verify(b'this_is_totp_key.', value, timestamp)
print(validity, value.decode())
```

