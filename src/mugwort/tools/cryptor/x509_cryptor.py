#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2023-01-05 22:51
@Description : 基于各种算法实现的密码学工具
@FileName    : x509_cryptor
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
import datetime
from typing import List, Union, Optional

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

__all__ = [
    'X509Cryptor',
]


class X509Cryptor:
    """
    采用 X509 格式标准的相关证书生成、签名工具，无需实例化即可调用。
    """

    @staticmethod
    def generate_certificate_signing_request(
            certificate_private_key: rsa.RSAPrivateKey,
            common_name: str = 'example.com',
            country_name: str = 'US',
            state_or_province_name: str = 'Washington',
            locality_name: str = 'District of Columbia',
            organization_name: str = 'White House',
            alternative_name: List[str] = None,
    ) -> x509.CertificateSigningRequest:
        """
        创建证书签名请求（CSR）

        :param certificate_private_key: 证书私钥
        :param common_name: 通用名称
        :param country_name: 国家代码
        :param state_or_province_name: 州或省
        :param locality_name: 城市
        :param organization_name: 组织
        :param alternative_name: 代替名称列表
        :return: 证书签名请求
        """
        subject_name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_or_province_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
        ])
        subject_alternative_name = x509.SubjectAlternativeName(
            [x509.DNSName(item) for item in alternative_name] if alternative_name else []
        )

        certificate_signing_request = (
            x509.CertificateSigningRequestBuilder()
            .subject_name(subject_name)
            .add_extension(subject_alternative_name, critical=False)
            .sign(certificate_private_key, hashes.SHA256())
        )
        return certificate_signing_request

    @staticmethod
    def generate_self_signed_certificate(
            certificate_public_key: rsa.RSAPublicKey,
            certificate_private_key: rsa.RSAPrivateKey = None,
            common_name: str = 'example.com',
            country_name: str = 'US',
            state_or_province_name: str = 'Washington',
            locality_name: str = 'District of Columbia',
            organization_name: str = 'White House',
            alternative_names: List[str] = None,
            lifetime_days: int = 365,
            ca_certificate: Optional[x509.Certificate] = None,
            ca_private_key: Optional[rsa.RSAPrivateKey] = None,
    ) -> x509.Certificate:
        """
        创建自签名证书

        :param certificate_public_key: 证书公钥
        :param certificate_private_key: 证书私钥
        :param common_name: 通用名称
        :param country_name: 国家代码
        :param state_or_province_name: 州或省
        :param locality_name: 城市
        :param organization_name: 组织
        :param alternative_names: 代替名称列表
        :param lifetime_days: 证书有效期（天）
        :param ca_certificate: 证书颁发机构的证书
        :param ca_private_key: 证书颁发机构的私钥
        :return: 自签名证书
        """
        if any([certificate_private_key, ca_private_key]) is False:
            raise RuntimeError('')
        if any([ca_certificate, ca_private_key]) and all([ca_certificate, ca_private_key]) is False:
            raise RuntimeError('证书颁发机构参数不正确')

        subject_name = issuer_name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_or_province_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
        ])
        subject_alternative_name = x509.SubjectAlternativeName(
            [x509.DNSName(item) for item in alternative_names] if alternative_names else []
        )

        certificate = (
            x509.CertificateBuilder()
            .subject_name(subject_name)
            .issuer_name(ca_certificate.issuer if ca_certificate else issuer_name)
            .public_key(certificate_public_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=lifetime_days))
            .add_extension(subject_alternative_name, critical=False)
            .sign(ca_private_key or certificate_private_key, hashes.SHA256())
        )
        return certificate

    @staticmethod
    def generate_self_signed_certificate_authority(
            certificate_public_key: rsa.RSAPublicKey,
            certificate_private_key: rsa.RSAPrivateKey,
            common_name: str = 'Example CA',
            country_name: str = 'US',
            state_or_province_name: str = 'Washington',
            locality_name: str = 'District of Columbia',
            organization_name: str = 'White House',
            lifetime_days: int = 365,
    ) -> x509.Certificate:
        """
        创建自签名证书颁发机构（CA）

        :param certificate_public_key: 证书公钥
        :param certificate_private_key: 证书私钥
        :param common_name: 通用名称
        :param country_name: 国家代码
        :param state_or_province_name: 州或省
        :param locality_name: 城市
        :param organization_name: 组织
        :param lifetime_days: 证书颁发机构有效期（天）
        :return: 自签名证书颁发机构
        """
        subject_name = issuer_name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            x509.NameAttribute(NameOID.COUNTRY_NAME, country_name),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state_or_province_name),
            x509.NameAttribute(NameOID.LOCALITY_NAME, locality_name),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization_name),
        ])

        certificate = (
            x509.CertificateBuilder()
            .subject_name(subject_name)
            .issuer_name(issuer_name)
            .public_key(certificate_public_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=lifetime_days))
            .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
            .sign(certificate_private_key, hashes.SHA256())
        )
        return certificate

    @staticmethod
    def dump_certificate(certificate: Union[x509.Certificate, x509.CertificateSigningRequest]) -> bytes:
        """
        证书转储函数

        :param certificate: 证书对象
        :return: 证书文件内容
        """
        return certificate.public_bytes(serialization.Encoding.PEM)

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
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(password),
            )
        else:
            private_key_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        return private_key_bytes.replace(b'RSA PRIVATE KEY', b'PRIVATE KEY')
