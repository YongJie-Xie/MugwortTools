#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-09-15 14:58
@Description : 基于各种算法实现的密码学工具
@FileName    : totp_cryptor
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.twofactor import InvalidToken, totp

__all__ = [
    'TOTPCryptor',
]


class TOTPCryptor:
    """
    由双因素身份验证相关算法实现，支持一次性密码生成和验证的工具，无需实例化即可调用。
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
