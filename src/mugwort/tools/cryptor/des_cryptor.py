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
@Version     : 1.0.0
"""
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

__all__ = [
    'TripleDESCryptor',
]


class TripleDESCryptor:
    """
    由 3DES 算法实现，支持常用加密模式和常用填充方式且兼容 DES 算法的加解密工具，无需实例化即可调用。

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
        data = TripleDESCryptor.pad_pkcs7(data, block_size)
        data = TripleDESCryptor.encrypt_cbc(data, key, iv)
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
        data = TripleDESCryptor.decrypt_cbc(data, key, iv)
        data = TripleDESCryptor.unpad_pkcs7(data, block_size)
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
        data = TripleDESCryptor.pad_ansix923(data, block_size)
        data = TripleDESCryptor.encrypt_cbc(data, key, iv)
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
        data = TripleDESCryptor.unpad_ansix923(data, block_size)
        data = TripleDESCryptor.decrypt_cbc(data, key, iv)
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
        data = TripleDESCryptor.pad_pkcs7(data, block_size)
        data = TripleDESCryptor.encrypt_ecb(data, key)
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
        data = TripleDESCryptor.unpad_pkcs7(data, block_size)
        data = TripleDESCryptor.decrypt_ecb(data, key)
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
        data = TripleDESCryptor.pad_ansix923(data, block_size)
        data = TripleDESCryptor.encrypt_ecb(data, key)
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
        data = TripleDESCryptor.unpad_ansix923(data, block_size)
        data = TripleDESCryptor.decrypt_ecb(data, key)
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
        data = TripleDESCryptor.encrypt_ofb(data, key, iv)
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
        data = TripleDESCryptor.decrypt_ofb(data, key, iv)
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
        data = TripleDESCryptor.encrypt_cfb(data, key, iv)
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
        data = TripleDESCryptor.decrypt_cfb(data, key, iv)
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
        data = TripleDESCryptor.encrypt_cfb8(data, key, iv)
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
        data = TripleDESCryptor.decrypt_cfb8(data, key, iv)
        return data

    @staticmethod
    def pad_pkcs7(data: bytes, block_size: int = 16) -> bytes:
        padder = padding.PKCS7(block_size * 8).padder()
        return padder.update(data) + padder.finalize()

    @staticmethod
    def unpad_pkcs7(data: bytes, block_size: int = 16) -> bytes:
        unpadder = padding.PKCS7(block_size * 8).unpadder()
        return unpadder.update(data) + unpadder.finalize()

    @staticmethod
    def pad_ansix923(data: bytes, block_size: int = 16) -> bytes:
        padder = padding.ANSIX923(block_size * 8).padder()
        return padder.update(data) + padder.finalize()

    @staticmethod
    def unpad_ansix923(data: bytes, block_size: int = 16) -> bytes:
        unpadder = padding.ANSIX923(block_size * 8).unpadder()
        return unpadder.update(data) + unpadder.finalize()

    @staticmethod
    def encrypt_cbc(data: bytes, key: bytes, iv: bytes) -> bytes:
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.CBC(iv)).encryptor()
        return encryptor.update(data) + encryptor.finalize()

    @staticmethod
    def decrypt_cbc(data: bytes, key: bytes, iv: bytes) -> bytes:
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.CBC(iv)).decryptor()
        return decryptor.update(data) + decryptor.finalize()

    @staticmethod
    def encrypt_ecb(data: bytes, key: bytes) -> bytes:
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.ECB()).encryptor()
        return encryptor.update(data) + encryptor.finalize()

    @staticmethod
    def decrypt_ecb(data: bytes, key: bytes) -> bytes:
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.ECB()).decryptor()
        return decryptor.update(data) + decryptor.finalize()

    @staticmethod
    def encrypt_ofb(data: bytes, key: bytes, iv: bytes) -> bytes:
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.OFB(iv)).encryptor()
        return encryptor.update(data) + encryptor.finalize()

    @staticmethod
    def decrypt_ofb(data: bytes, key: bytes, iv: bytes) -> bytes:
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.OFB(iv)).decryptor()
        return decryptor.update(data) + decryptor.finalize()

    @staticmethod
    def encrypt_cfb(data: bytes, key: bytes, iv: bytes) -> bytes:
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.CFB(iv)).encryptor()
        return encryptor.update(data) + encryptor.finalize()

    @staticmethod
    def decrypt_cfb(data: bytes, key: bytes, iv: bytes) -> bytes:
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.CFB(iv)).decryptor()
        return decryptor.update(data) + decryptor.finalize()

    @staticmethod
    def encrypt_cfb8(data: bytes, key: bytes, iv: bytes) -> bytes:
        encryptor = Cipher(algorithms.TripleDES(key), mode=modes.CFB8(iv)).encryptor()
        return encryptor.update(data) + encryptor.finalize()

    @staticmethod
    def decrypt_cfb8(data: bytes, key: bytes, iv: bytes) -> bytes:
        decryptor = Cipher(algorithms.TripleDES(key), mode=modes.CFB8(iv)).decryptor()
        return decryptor.update(data) + decryptor.finalize()
