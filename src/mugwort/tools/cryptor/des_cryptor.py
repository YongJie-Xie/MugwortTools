#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-09-15 14:58
@Description : 基于各种算法实现的密码学工具
@FileName    : des_cryptor
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

__all__ = [
    'TripleDESCryptor',
]


class TripleDESCryptor:
    """
    由 3DES 算法实现的支持常用加密模式和常用填充方式且兼容 DES 算法的加解密工具，无需实例化即可调用。

    注：当密钥长度为 8 时，前两重 DES 操作会相互抵消，等价于 DES 算法。

    支持的加密模式：
    CBC  ：[√]需要填充、[√]需要 iv 值（密码块链接模式，常用）
    ECB  ：[√]需要填充、[×]无需 iv 值（电子密码本模式，不安全）
    OFB  ：[×]无需填充、[√]需要 iv 值（输出反馈模式）
    CFB  ：[×]无需填充、[√]需要 iv 值（密文反馈模式）
    CFB8 ：[×]无需填充、[√]需要 iv 值（使用 8 位移位寄存器的密文反馈模式）

    支持的填充方式：
    PKCS7    ：填充 n 个 chr(n) 字符，其中 n 是补齐数据块所需的字节数
    ANSIX923 ：先填充 n-1 个 chr(0) 字符再填充 1 个 chr(n) 字符，其中 n 是补齐数据块所需的字节数
    """

    @staticmethod
    def cbc_pkcs7_encryptor(data: bytes, key: bytes, iv: bytes, block_size: int = 16) -> bytes:
        """
        采用 CBC 模式和 PKCS7 填充方式的加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param iv: 初始化向量，长度限制：8
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 密文数据
        """
        padder = padding.PKCS7(block_size * 8).padder()
        data = padder.update(data) + padder.finalize()
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.CBC(iv)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def cbc_pkcs7_decryptor(data: bytes, key: bytes, iv: bytes, block_size: int = 16) -> bytes:
        """
        采用 CBC 模式和 PKCS7 填充方式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param iv: 初始化向量，长度限制：8
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.CBC(iv)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        unpadder = padding.PKCS7(block_size * 8).unpadder()
        data = unpadder.update(data) + unpadder.finalize()
        return data

    @staticmethod
    def cbc_ansix923_encryptor(data: bytes, key: bytes, iv: bytes, block_size: int = 16) -> bytes:
        """
        采用 CBC 模式和 ANSIX923 填充方式的加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param iv: 初始化向量，长度限制：8
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 密文数据
        """
        padder = padding.ANSIX923(block_size * 8).padder()
        data = padder.update(data) + padder.finalize()
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.CBC(iv)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def cbc_ansix923_decryptor(data: bytes, key: bytes, iv: bytes, block_size: int = 16) -> bytes:
        """
        采用 CBC 模式和 ANSIX923 填充方式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param iv: 初始化向量，长度限制：8
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.CBC(iv)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        unpadder = padding.ANSIX923(block_size * 8).unpadder()
        data = unpadder.update(data) + unpadder.finalize()
        return data

    @staticmethod
    def ecb_pkcs7_encryptor(data: bytes, key: bytes, block_size: int = 16) -> bytes:
        """
        采用 ECB 模式和 PKCS7 填充方式的加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 密文数据
        """
        padder = padding.PKCS7(block_size * 8).padder()
        data = padder.update(data) + padder.finalize()
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.ECB()).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def ecb_pkcs7_decryptor(data: bytes, key: bytes, block_size: int = 16) -> bytes:
        """
        采用 ECB 模式和 PKCS7 填充方式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.ECB()).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        unpadder = padding.PKCS7(block_size * 8).unpadder()
        data = unpadder.update(data) + unpadder.finalize()
        return data

    @staticmethod
    def ecb_ansix923_encryptor(data: bytes, key: bytes, block_size: int = 16) -> bytes:
        """
        采用 ECB 模式和 ANSIX923 填充方式的加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 密文数据
        """
        padder = padding.ANSIX923(block_size * 8).padder()
        data = padder.update(data) + padder.finalize()
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.ECB()).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def ecb_ansix923_decryptor(data: bytes, key: bytes, block_size: int = 16) -> bytes:
        """
        采用 ECB 模式和 ANSIX923 填充方式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.ECB()).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        unpadder = padding.ANSIX923(block_size * 8).unpadder()
        data = unpadder.update(data) + unpadder.finalize()
        return data

    @staticmethod
    def ofb_encryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 OFB 模式的 AES 加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param iv: 初始化向量，长度限制：8
        :return: 密文数据
        """
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.OFB(iv)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def ofb_decryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 OFB 模式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param iv: 初始化向量，长度限制：8
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.OFB(iv)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data

    @staticmethod
    def cfb_encryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 CFB 模式的 AES 加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param iv: 初始化向量，长度限制：8
        :return: 密文数据
        """
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.CFB(iv)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def cfb_decryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 CFB 模式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param iv: 初始化向量，长度限制：8
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.CFB(iv)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data

    @staticmethod
    def cfb8_encryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 CFB8 模式的 AES 加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param iv: 初始化向量，长度限制：8
        :return: 密文数据
        """
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.CFB8(iv)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def cfb8_decryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 CFB8 模式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：8 / 16 / 24
        :param iv: 初始化向量，长度限制：8
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.CFB8(iv)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data
