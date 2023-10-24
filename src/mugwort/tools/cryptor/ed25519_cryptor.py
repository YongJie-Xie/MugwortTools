#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-09-15 14:58
@Description : 基于各种算法实现的密码学工具
@FileName    : ed25519_cryptor
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0.0
"""
import typing as t

from cryptography import exceptions
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

__all__ = [
    'Ed25519Cryptor',
]


class Ed25519Cryptor:
    """
    由 Ed25519 算法实现，支持密钥对生成、消息签名、消息校验功能的工具，无需实例化即可调用。
    """

    @staticmethod
    def generate() -> t.Tuple[ed25519.Ed25519PublicKey, ed25519.Ed25519PrivateKey]:
        """
        密钥对生成函数

        :return: 公钥对象、私钥对象
        """
        private_key = ed25519.Ed25519PrivateKey.generate()
        return private_key.public_key(), private_key

    @staticmethod
    def sign(private_key: ed25519.Ed25519PrivateKey, message: bytes) -> bytes:
        """
        消息签名函数

        :param private_key: 私钥对象
        :param message: 待签名消息
        :return: 签名信息
        """
        signature = private_key.sign(message)
        return signature

    @staticmethod
    def verify(public_key: ed25519.Ed25519PublicKey, message: bytes, signature: bytes) -> bool:
        """
        消息校验函数

        :param public_key: 公钥对象
        :param signature: 签名信息
        :param message: 待校验消息
        :return: 校验结果
        """
        try:
            public_key.verify(signature, message)
        except exceptions.InvalidSignature:
            return False
        else:
            return True

    @staticmethod
    def load_public_key(data: bytes) -> ed25519.Ed25519PublicKey:
        """
        公钥装载函数

        :param data: 公钥文件内容，格式为：RAW
        :return: 公钥对象
        """
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(data)
        return public_key

    @staticmethod
    def load_private_key(data: bytes) -> ed25519.Ed25519PrivateKey:
        """
        私钥装载函数

        :param data: 私钥文件内容，格式为：RAW
        :return: 私钥对象
        """
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(data)
        return private_key

    @staticmethod
    def dump_public_key(public_key: ed25519.Ed25519PublicKey) -> bytes:
        """
        公钥转储函数

        :param public_key: 公钥对象
        :return: 公钥文件内容
        """
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        return public_key_bytes

    @staticmethod
    def dump_private_key(private_key: ed25519.Ed25519PrivateKey) -> bytes:
        """
        私钥转储函数

        :param private_key: 私钥对象
        :return: 私钥文件内容
        """
        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return private_key_bytes
