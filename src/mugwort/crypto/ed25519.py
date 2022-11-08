#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-09-15 14:58
@Description : 基于各种算法实现的密码学工具
@FileName    : ed25519
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
from typing import Optional, Tuple

from cryptography import exceptions
from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, padding as asymmetric_padding, rsa, x25519
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.twofactor import InvalidToken, totp

__all__ = [
    'Ed25519Cryptor',
    'X25519Cryptor',
    'TOTPCryptor',
]


class Ed25519Cryptor:
    """
    由 Ed25519 算法实现的支持密钥对生成、消息签名、消息校验功能的签名工具，无需实例化即可调用。
    """

    @staticmethod
    def generate() -> Tuple[ed25519.Ed25519PublicKey, ed25519.Ed25519PrivateKey]:
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


class TOTPCryptor:
    """
    由双因素身份验证相关算法实现的一次性密码生成和验证工具，无需实例化即可调用。
    """

    @staticmethod
    def generate(key: bytes, timestamp: int, length: int = 6, time_step: int = 30) -> bytes:
        """
        一次性密码生成函数

        :param key: 密钥
        :param timestamp: 一次性密码的生成时间，以秒为单位的时间戳
        :param length: 一次性密码的长度，取值限制：[6, 8]
        :param time_step: 时间步长，默认 30 秒
        :return: 一次性密码
        """
        value = totp.TOTP(key, length, hashes.SHA1(), time_step).generate(timestamp)
        return value

    @staticmethod
    def verify(key: bytes, value: bytes, timestamp: int, length: int = 6, time_step: int = 30) -> bool:
        """
        一次性密码校验函数

        :param key: 密钥
        :param value: 待校验的一次性密码
        :param timestamp: 一次性密码的生成时间，以秒为单位的时间戳
        :param length: 一次性密码的长度，取值限制：[6, 8]
        :param time_step: 时间步长，默认 30 秒
        :return: 校验结果
        """
        try:
            totp.TOTP(key, length, hashes.SHA1(), time_step).verify(value, timestamp)
        except InvalidToken:
            return False
        else:
            return True
