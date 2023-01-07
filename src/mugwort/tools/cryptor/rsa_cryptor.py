#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-09-15 14:58
@Description : 基于各种算法实现的密码学工具
@FileName    : rsa_cryptor
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
from typing import Optional, Tuple

from cryptography import exceptions
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

__all__ = [
    'RSACryptor',
]


class RSACryptor:
    """
    由 RSA 算法实现，支持密钥对生成、消息加密、消息解密、消息签名、消息校验功能的加解密及签名工具，无需实例化即可调用。
    """

    @staticmethod
    def generate(key_size: int = 2048) -> Tuple[rsa.RSAPublicKey, rsa.RSAPrivateKey]:
        """
        密钥对生成函数，密钥长度建议为 2048

        :param key_size: 密钥长度，长度限制：[512, +∞]
        :return: 公钥对象、私钥对象
        """
        private_key = rsa.generate_private_key(65537, key_size)
        return private_key.public_key(), private_key

    @staticmethod
    def encrypt(public_key: rsa.RSAPublicKey, message: bytes) -> bytes:
        """
        消息加密函数

        :param public_key: 公钥对象
        :param message: 明文数据
        :return: 密文数据
        """
        data = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            )
        )
        return data

    @staticmethod
    def decrypt(private_key: rsa.RSAPrivateKey, message: bytes) -> bytes:
        """
        消息解密函数

        :param private_key: 私钥对象
        :param message: 密文数据
        :return: 明文数据
        """
        message = private_key.decrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            )
        )
        return message

    @staticmethod
    def sign(private_key: rsa.RSAPrivateKey, message: bytes) -> bytes:
        """
        消息签名函数

        :param private_key: 私钥对象
        :param message: 待签名消息
        :return: 签名信息
        """
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        return signature

    @staticmethod
    def verify(public_key: rsa.RSAPublicKey, message: bytes, signature: bytes) -> bool:
        """
        消息校验函数

        :param public_key: 公钥对象
        :param message: 待校验消息
        :param signature: 签名
        :return: 校验结果
        """
        try:
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
        except exceptions.InvalidSignature:
            return False
        else:
            return True

    @staticmethod
    def load_public_key(data: bytes) -> rsa.RSAPublicKey:
        """
        公钥装载函数

        :param data: 公钥文件内容，格式为：PEM
        :return: 公钥对象
        """
        public_key = serialization.load_pem_public_key(data)
        return public_key

    @staticmethod
    def load_private_key(data: bytes, password: Optional[bytes] = None) -> rsa.RSAPrivateKey:
        """
        私钥装载函数

        :param data: 私钥文件内容，格式为：PEM
        :param password: 私钥密码
        :return: 私钥对象
        """
        private_key = serialization.load_pem_private_key(data, password)
        return private_key

    @staticmethod
    def dump_public_key(public_key: rsa.RSAPublicKey) -> bytes:
        """
        公钥转储函数

        :param public_key: 公钥对象
        :return: 公钥文件内容
        """
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return public_key_bytes

    @staticmethod
    def dump_private_key(private_key: rsa.RSAPrivateKey, password: Optional[bytes] = None) -> bytes:
        """
        私钥转储函数

        :param private_key: 私钥对象
        :param password: 私钥密码
        :return: 私钥文件内容
        """
        if password:
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password),
            )
        else:
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        return private_key_bytes
