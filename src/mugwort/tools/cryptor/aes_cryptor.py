#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-09-15 14:58
@Description : 基于各种算法实现的密码学工具
@FileName    : aes_cryptor
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
import typing as t

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

__all__ = [
    'AESCryptor',
]


class AESCryptor:
    """
    由 AES 算法实现，支持常用加密模式和常用填充方式的加解密工具，无需实例化即可调用。

    支持的加密模式：
    CBC  ：[√]需要填充、[√]需要 iv 值（密码块链接模式，常用）
    XTS  ：[×]无需填充、[×]无需 iv 值、另需 tweak 值（常用于磁盘加密）
    ECB  ：[√]需要填充、[×]无需 iv 值（电子密码本模式，不安全）
    OFB  ：[×]无需填充、[√]需要 iv 值（输出反馈模式）
    CFB  ：[×]无需填充、[√]需要 iv 值（密文反馈模式）
    CFB8 ：[×]无需填充、[√]需要 iv 值（使用 8 位移位寄存器的密文反馈模式）
    CTR  ：[×]无需填充、[×]无需 iv 值、另需 nonce 值（计数器模式）
    GCM  ：[×]无需填充、[√]需要 iv 值、另需 associated_data 和 tag 值（伽罗瓦/计数器模式，提供附加消息的完整性校验）

    支持的填充方式：
    PKCS7    ：填充 n 个 chr(n) 字符，其中 n 是补齐数据块所需的字节数
    ANSIX923 ：先填充 n-1 个 chr(0) 字符再填充 1 个 chr(n) 字符，其中 n 是补齐数据块所需的字节数
    """

    @staticmethod
    def cbc_pkcs7_encryptor(data: bytes, key: bytes, iv: bytes, block_size: int = 16) -> bytes:
        """
        采用 CBC 模式和 PKCS7 填充方式的加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：16
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 密文数据
        """
        padder = padding.PKCS7(block_size * 8).padder()
        data = padder.update(data) + padder.finalize()
        encryptor = Cipher(algorithms.AES(key), mode=modes.CBC(iv)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def cbc_pkcs7_decryptor(data: bytes, key: bytes, iv: bytes, block_size: int = 16) -> bytes:
        """
        采用 CBC 模式和 PKCS7 填充方式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：16
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.AES(key), mode=modes.CBC(iv)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        unpadder = padding.PKCS7(block_size * 8).unpadder()
        data = unpadder.update(data) + unpadder.finalize()
        return data

    @staticmethod
    def cbc_ansix923_encryptor(data: bytes, key: bytes, iv: bytes, block_size: int = 16) -> bytes:
        """
        采用 CBC 模式和 ANSIX923 填充方式的加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：16
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 密文数据
        """
        padder = padding.ANSIX923(block_size * 8).padder()
        data = padder.update(data) + padder.finalize()
        encryptor = Cipher(algorithms.AES(key), mode=modes.CBC(iv)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def cbc_ansix923_decryptor(data: bytes, key: bytes, iv: bytes, block_size: int = 16) -> bytes:
        """
        采用 CBC 模式和 ANSIX923 填充方式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：16
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.AES(key), mode=modes.CBC(iv)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        unpadder = padding.ANSIX923(block_size * 8).unpadder()
        data = unpadder.update(data) + unpadder.finalize()
        return data

    @staticmethod
    def xts_encryptor(data: bytes, key: bytes, tweak: bytes) -> bytes:
        """
        采用 XTS 模式的 AES 加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：64 / 128
        :param tweak: 可变值，长度限制：16
        :return: 密文数据
        """
        encryptor = Cipher(algorithms.AES(key), mode=modes.XTS(tweak)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def xts_decryptor(data: bytes, key: bytes, tweak: bytes) -> bytes:
        """
        采用 XTS 模式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：64 / 128
        :param tweak: 可变值，长度限制：16
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.AES(key), mode=modes.XTS(tweak)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data

    @staticmethod
    def ecb_pkcs7_encryptor(data: bytes, key: bytes, block_size: int = 16) -> bytes:
        """
        采用 ECB 模式和 PKCS7 填充方式的加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 密文数据
        """
        padder = padding.PKCS7(block_size * 8).padder()
        data = padder.update(data) + padder.finalize()
        encryptor = Cipher(algorithms.AES(key), mode=modes.ECB()).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def ecb_pkcs7_decryptor(data: bytes, key: bytes, block_size: int = 16) -> bytes:
        """
        采用 ECB 模式和 PKCS7 填充方式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.AES(key), mode=modes.ECB()).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        unpadder = padding.PKCS7(block_size * 8).unpadder()
        data = unpadder.update(data) + unpadder.finalize()
        return data

    @staticmethod
    def ecb_ansix923_encryptor(data: bytes, key: bytes, block_size: int = 16) -> bytes:
        """
        采用 ECB 模式和 ANSIX923 填充方式的加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 密文数据
        """
        padder = padding.ANSIX923(block_size * 8).padder()
        data = padder.update(data) + padder.finalize()
        encryptor = Cipher(algorithms.AES(key), mode=modes.ECB()).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def ecb_ansix923_decryptor(data: bytes, key: bytes, block_size: int = 16) -> bytes:
        """
        采用 ECB 模式和 ANSIX923 填充方式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param block_size: 数据块大小，取值限制：[0, 255]
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.AES(key), mode=modes.ECB()).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        unpadder = padding.ANSIX923(block_size * 8).unpadder()
        data = unpadder.update(data) + unpadder.finalize()
        return data

    @staticmethod
    def ofb_encryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 OFB 模式的 AES 加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：16
        :return: 密文数据
        """
        encryptor = Cipher(algorithms.AES(key), mode=modes.OFB(iv)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def ofb_decryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 OFB 模式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：16
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.AES(key), mode=modes.OFB(iv)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data

    @staticmethod
    def cfb_encryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 CFB 模式的 AES 加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：16
        :return: 密文数据
        """
        encryptor = Cipher(algorithms.AES(key), mode=modes.CFB(iv)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def cfb_decryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 CFB 模式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：16
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.AES(key), mode=modes.CFB(iv)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data

    @staticmethod
    def cfb8_encryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 CFB8 模式的 AES 加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：16
        :return: 密文数据
        """
        encryptor = Cipher(algorithms.AES(key), mode=modes.CFB8(iv)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def cfb8_decryptor(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        采用 CFB8 模式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：16
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.AES(key), mode=modes.CFB8(iv)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data

    @staticmethod
    def ctr_encryptor(data: bytes, key: bytes, nonce: bytes) -> bytes:
        """
        采用 CTR 模式的 AES 加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param nonce: 随机值，长度限制：16
        :return: 密文数据
        """
        encryptor = Cipher(algorithms.AES(key), mode=modes.CTR(nonce)).encryptor()
        data = encryptor.update(data) + encryptor.finalize()
        return data

    @staticmethod
    def ctr_decryptor(data: bytes, key: bytes, nonce: bytes) -> bytes:
        """
        采用 CTR 模式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param nonce: 随机值，长度限制：16
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.AES(key), mode=modes.CTR(nonce)).decryptor()
        data = decryptor.update(data) + decryptor.finalize()
        return data

    @staticmethod
    def gcm_encryptor(
            data: bytes, key: bytes, iv: bytes,
            associated_data: bytes,
    ) -> t.Tuple[bytes, t.Optional[bytes]]:
        """
        采用 GCM 模式的 AES 加密函数

        :param data: 明文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：[8, 128]
        :param associated_data: 附加数据
        :return: 密文数据、附加数据标签
        """
        encryptor = Cipher(algorithms.AES(key), mode=modes.GCM(iv)).encryptor()
        if associated_data:
            encryptor.authenticate_additional_data(associated_data)
        data = encryptor.update(data) + encryptor.finalize()
        return data, encryptor.tag

    @staticmethod
    def gcm_decryptor(
            data: bytes, key: bytes, iv: bytes,
            associated_data: bytes, tag: bytes, min_tag_length: int = 16,
    ) -> bytes:
        """
        采用 GCM 模式的解密函数

        :param data: 密文数据
        :param key: 密钥，长度限制：16 / 24 / 32
        :param iv: 初始化向量，长度限制：[8, 128]
        :param associated_data: 附加数据
        :param tag: 附加数据标签，长度限制：[4, 16]
        :param min_tag_length: 附加数据标签的最小长度，取值限制：[4, 16]
        :return: 明文数据
        """
        decryptor = Cipher(algorithms.AES(key), mode=modes.GCM(iv, tag, min_tag_length)).decryptor()
        if associated_data:
            decryptor.authenticate_additional_data(associated_data)
        data = decryptor.update(data) + decryptor.finalize()
        return data
