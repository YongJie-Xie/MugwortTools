#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-09-15 14:58
@Description : 基于各种算法实现的密码学工具
@FileName    : x25519
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
from typing import Tuple

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

__all__ = [
    'X25519Cryptor',
]


class X25519Cryptor:
    """
    由 X25519 算法实现的支持密钥对生成、密钥交换功能的签名工具，无需实例化即可调用。
    """

    @staticmethod
    def generate() -> Tuple[x25519.X25519PublicKey, x25519.X25519PrivateKey]:
        """
        密钥对生成函数

        :return: 公钥对象、私钥对象
        """
        private_key = x25519.X25519PrivateKey.generate()
        return private_key.public_key(), private_key

    @staticmethod
    def exchange(private_key: x25519.X25519PrivateKey, peer_public_key: x25519.X25519PublicKey) -> bytes:
        """
        密钥交换函数

        :param private_key: 私钥对象
        :param peer_public_key: 对端公钥对象
        :return: 共享密钥
        """
        shared_key = private_key.exchange(peer_public_key)
        return shared_key

    @staticmethod
    def load_public_key(data: bytes) -> x25519.X25519PublicKey:
        """
        公钥装载函数

        :param data: 公钥文件内容，格式为：RAW
        :return: 公钥对象
        """
        public_key = x25519.X25519PublicKey.from_public_bytes(data)
        return public_key

    @staticmethod
    def load_private_key(data: bytes) -> x25519.X25519PrivateKey:
        """
        私钥装载函数

        :param data: 私钥文件内容，格式为：RAW
        :return: 私钥对象
        """
        private_key = x25519.X25519PrivateKey.from_private_bytes(data)
        return private_key

    @staticmethod
    def dump_public_key(public_key: x25519.X25519PublicKey) -> bytes:
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
    def dump_private_key(private_key: x25519.X25519PrivateKey) -> bytes:
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
