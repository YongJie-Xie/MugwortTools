#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-09-15 14:58
@Description : 基于各种算法实现的密码学工具
@FileName    : cryptor
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
    'AESCryptor',
    'TripleDESCryptor',
    'RSACryptor',
    'Ed25519Cryptor',
    'X25519Cryptor',
    'TOTPCryptor',
]


class AESCryptor:
    """
    由 AES 算法实现的支持常用加密模式和常用填充方式的加解密工具，无需实例化即可调用。

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
    ) -> Tuple[bytes, Optional[bytes]]:
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


class RSACryptor:
    """
    由 RSA 算法实现的支持密钥对生成、消息加密、消息解密、消息签名、消息校验功能的加解密及签名工具，无需实例化即可调用。
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
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
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
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
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
            asymmetric_padding.PSS(
                mgf=asymmetric_padding.MGF1(hashes.SHA256()),
                salt_length=asymmetric_padding.PSS.MAX_LENGTH,
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
                asymmetric_padding.PSS(
                    mgf=asymmetric_padding.MGF1(hashes.SHA256()),
                    salt_length=asymmetric_padding.PSS.MAX_LENGTH,
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
