#### RSACryptor

采用 X509 格式标准实现，支持**证书生成、签名**的工具，无需实例化即可调用。

- 代码示例

```python
from mugwort.tools.cryptor import RSACryptor, X509Cryptor

csr_public_key, csr_private_key = RSACryptor.generate()
csr_certificate = X509Cryptor.generate_certificate_signing_request(
    csr_private_key
)
print('>>> csr certificate <<<')
print(X509Cryptor.dump_certificate(csr_certificate).decode())
print(X509Cryptor.dump_private_key(csr_private_key).decode())

ca_public_key, ca_private_key = RSACryptor.generate()
ca_certificate = X509Cryptor.generate_self_signed_certificate_authority(
    ca_public_key, ca_private_key
)
print('>>> ca certificate <<<')
print(X509Cryptor.dump_certificate(ca_certificate).decode())
print(X509Cryptor.dump_private_key(ca_private_key).decode())

my_public_key, my_private_key = RSACryptor.generate()
my_certificate = X509Cryptor.generate_self_signed_certificate(
    my_public_key, my_private_key, ca_certificate=ca_certificate, ca_private_key=ca_private_key
)
print('>>> my certificate <<<')
print(X509Cryptor.dump_certificate(my_certificate).decode())
print(X509Cryptor.dump_private_key(my_private_key).decode())
```

