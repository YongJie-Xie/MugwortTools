#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author      : YongJie-Xie
@Contact     : fsswxyj@qq.com
@DateTime    : 2022-09-17 17:14
@Description : TODO 撰写描述
@FileName    : test_tool_cryptor
@License     : MIT License
@ProjectName : MugwortTools
@Software    : PyCharm
@Version     : 1.0
"""
import os
import time

from mugwort.tools.cryptor import (
    AESCryptor,
    TripleDESCryptor,
    RSACryptor,
    Ed25519Cryptor,
    X25519Cryptor,
    TOTPCryptor,
    X509Cryptor,
)

aes_key = b'this_is_aes_key.'
aes_plaintext = b'this_is_aes_plaintext.'


def test_aes_cbc_pkcs7_cryptor():
    iv = os.urandom(16)
    ciphertext = AESCryptor.cbc_pkcs7_encryptor(aes_plaintext, aes_key, iv)
    plaintext = AESCryptor.cbc_pkcs7_decryptor(ciphertext, aes_key, iv)
    assert plaintext == aes_plaintext


def test_aes_cbc_ansix923_cryptor():
    iv = os.urandom(16)
    ciphertext = AESCryptor.cbc_ansix923_encryptor(aes_plaintext, aes_key, iv)
    plaintext = AESCryptor.cbc_ansix923_decryptor(ciphertext, aes_key, iv)
    assert plaintext == aes_plaintext


def test_aes_xts_cryptor():
    key = os.urandom(64)
    tweak = os.urandom(16)
    ciphertext = AESCryptor.xts_encryptor(aes_plaintext, key, tweak)
    plaintext = AESCryptor.xts_decryptor(ciphertext, key, tweak)
    assert plaintext == aes_plaintext


def test_aes_ecb_pkcs7_cryptor():
    ciphertext = AESCryptor.ecb_pkcs7_encryptor(aes_plaintext, aes_key)
    plaintext = AESCryptor.ecb_pkcs7_decryptor(ciphertext, aes_key)
    assert plaintext == aes_plaintext


def test_aes_ecb_ansix923_cryptor():
    ciphertext = AESCryptor.ecb_ansix923_encryptor(aes_plaintext, aes_key)
    plaintext = AESCryptor.ecb_ansix923_decryptor(ciphertext, aes_key)
    assert plaintext == aes_plaintext


def test_aes_ofb_cryptor():
    iv = os.urandom(16)
    ciphertext = AESCryptor.ofb_encryptor(aes_plaintext, aes_key, iv)
    plaintext = AESCryptor.ofb_decryptor(ciphertext, aes_key, iv)
    assert plaintext == aes_plaintext


def test_aes_cfb_cryptor():
    iv = os.urandom(16)
    ciphertext = AESCryptor.cfb_encryptor(aes_plaintext, aes_key, iv)
    plaintext = AESCryptor.cfb_decryptor(ciphertext, aes_key, iv)
    assert plaintext == aes_plaintext


def test_aes_cfb8_cryptor():
    iv = os.urandom(16)
    ciphertext = AESCryptor.cfb8_encryptor(aes_plaintext, aes_key, iv)
    plaintext = AESCryptor.cfb8_decryptor(ciphertext, aes_key, iv)
    assert plaintext == aes_plaintext


def test_aes_ctr_cryptor():
    nonce = os.urandom(16)
    ciphertext = AESCryptor.ctr_encryptor(aes_plaintext, aes_key, nonce)
    plaintext = AESCryptor.ctr_decryptor(ciphertext, aes_key, nonce)
    assert plaintext == aes_plaintext


def test_aes_gcm_cryptor():
    iv = os.urandom(16)
    associated_data = aes_plaintext * 10
    ciphertext, tag = AESCryptor.gcm_encryptor(aes_plaintext, aes_key, iv, associated_data)
    plaintext = AESCryptor.gcm_decryptor(ciphertext, aes_key, iv, associated_data, tag)
    assert plaintext == aes_plaintext


des_key = b'des_key.'
des_plaintext = b'this_is_des_plaintext.'


def test_des_cbc_pkcs7_cryptor():
    iv = os.urandom(8)
    ciphertext = TripleDESCryptor.cbc_pkcs7_encryptor(des_plaintext, des_key, iv)
    plaintext = TripleDESCryptor.cbc_pkcs7_decryptor(ciphertext, des_key, iv)
    assert plaintext == des_plaintext


def test_des_cbc_ansix923_cryptor():
    iv = os.urandom(8)
    ciphertext = TripleDESCryptor.cbc_ansix923_encryptor(des_plaintext, des_key, iv)
    plaintext = TripleDESCryptor.cbc_ansix923_decryptor(ciphertext, des_key, iv)
    assert plaintext == des_plaintext


def test_des_ecb_pkcs7_cryptor():
    ciphertext = TripleDESCryptor.ecb_pkcs7_encryptor(des_plaintext, des_key)
    plaintext = TripleDESCryptor.ecb_pkcs7_decryptor(ciphertext, des_key)
    assert plaintext == des_plaintext


def test_des_ecb_ansix923_cryptor():
    ciphertext = TripleDESCryptor.ecb_ansix923_encryptor(des_plaintext, des_key)
    plaintext = TripleDESCryptor.ecb_ansix923_decryptor(ciphertext, des_key)
    assert plaintext == des_plaintext


def test_des_ofb_cryptor():
    iv = os.urandom(8)
    ciphertext = TripleDESCryptor.ofb_encryptor(des_plaintext, des_key, iv)
    plaintext = TripleDESCryptor.ofb_decryptor(ciphertext, des_key, iv)
    assert plaintext == des_plaintext


def test_des_cfb_cryptor():
    iv = os.urandom(8)
    ciphertext = TripleDESCryptor.cfb_encryptor(des_plaintext, des_key, iv)
    plaintext = TripleDESCryptor.cfb_decryptor(ciphertext, des_key, iv)
    assert plaintext == des_plaintext


def test_des_cfb8_cryptor():
    iv = os.urandom(8)
    ciphertext = TripleDESCryptor.cfb8_encryptor(des_plaintext, des_key, iv)
    plaintext = TripleDESCryptor.cfb8_decryptor(ciphertext, des_key, iv)
    assert plaintext == des_plaintext


triple_des_key = b'this_is_triple_des_key..'
triple_des_plaintext = b'this_is_triple_des_plaintext.'


def test_triple_des_cbc_pkcs7_cryptor():
    iv = os.urandom(8)
    ciphertext = TripleDESCryptor.cbc_pkcs7_encryptor(des_plaintext, des_key, iv)
    plaintext = TripleDESCryptor.cbc_pkcs7_decryptor(ciphertext, des_key, iv)
    assert plaintext == des_plaintext


def test_triple_des_cbc_ansix923_cryptor():
    iv = os.urandom(8)
    ciphertext = TripleDESCryptor.cbc_ansix923_encryptor(des_plaintext, des_key, iv)
    plaintext = TripleDESCryptor.cbc_ansix923_decryptor(ciphertext, des_key, iv)
    assert plaintext == des_plaintext


def test_triple_des_ecb_pkcs7_cryptor():
    ciphertext = TripleDESCryptor.ecb_pkcs7_encryptor(des_plaintext, des_key)
    plaintext = TripleDESCryptor.ecb_pkcs7_decryptor(ciphertext, des_key)
    assert plaintext == des_plaintext


def test_triple_des_ecb_ansix923_cryptor():
    ciphertext = TripleDESCryptor.ecb_ansix923_encryptor(des_plaintext, des_key)
    plaintext = TripleDESCryptor.ecb_ansix923_decryptor(ciphertext, des_key)
    assert plaintext == des_plaintext


def test_triple_des_ofb_cryptor():
    iv = os.urandom(8)
    ciphertext = TripleDESCryptor.ofb_encryptor(des_plaintext, des_key, iv)
    plaintext = TripleDESCryptor.ofb_decryptor(ciphertext, des_key, iv)
    assert plaintext == des_plaintext


def test_triple_des_cfb_cryptor():
    iv = os.urandom(8)
    ciphertext = TripleDESCryptor.cfb_encryptor(des_plaintext, des_key, iv)
    plaintext = TripleDESCryptor.cfb_decryptor(ciphertext, des_key, iv)
    assert plaintext == des_plaintext


def test_triple_des_cfb8_cryptor():
    iv = os.urandom(8)
    ciphertext = TripleDESCryptor.cfb8_encryptor(des_plaintext, des_key, iv)
    plaintext = TripleDESCryptor.cfb8_decryptor(ciphertext, des_key, iv)
    assert plaintext == des_plaintext


ras_key = b'this_is_rsa_key.'
rsa_plaintext = b'this_is_rsa_plaintext.'


def test_rsa_encrypt_decrypt():
    public_key, private_key = RSACryptor.generate()

    ciphertext = RSACryptor.encrypt(public_key, rsa_plaintext)
    plaintext = RSACryptor.decrypt(private_key, ciphertext)
    assert plaintext == rsa_plaintext


def test_rsa_sign_verify():
    public_key, private_key = RSACryptor.generate()

    signature = RSACryptor.sign(private_key, rsa_plaintext)
    assert RSACryptor.verify(public_key, rsa_plaintext, signature) is True

    signature = RSACryptor.sign(private_key, rsa_plaintext)
    plain_text = rsa_plaintext + b'InterferenceData'
    assert RSACryptor.verify(public_key, plain_text, signature) is False


def test_rsa_dump_load_public_key():
    public_key, private_key = RSACryptor.generate()

    public_key_bytes = RSACryptor.dump_public_key(public_key)
    public_key = RSACryptor.load_public_key(public_key_bytes)
    assert RSACryptor.dump_public_key(public_key) == public_key_bytes


def test_rsa_dump_load_private_key():
    public_key, private_key = RSACryptor.generate()

    private_key_bytes = RSACryptor.dump_private_key(private_key)
    private_key = RSACryptor.load_private_key(private_key_bytes)
    assert RSACryptor.dump_private_key(private_key) == private_key_bytes

    private_key_bytes_encrypted = RSACryptor.dump_private_key(private_key, password=ras_key)
    private_key = RSACryptor.load_private_key(private_key_bytes_encrypted, password=ras_key)
    assert RSACryptor.dump_private_key(private_key) == private_key_bytes


ed25519_plaintext = b'this_is_ed25519_plaintext.'


def test_ed25519_sign_verify():
    public_key, private_key = Ed25519Cryptor.generate()

    signature = Ed25519Cryptor.sign(private_key, rsa_plaintext)
    assert Ed25519Cryptor.verify(public_key, rsa_plaintext, signature) is True

    signature = Ed25519Cryptor.sign(private_key, rsa_plaintext)
    plain_text = rsa_plaintext + b'InterferenceData'
    assert Ed25519Cryptor.verify(public_key, plain_text, signature) is False


def test_ed25519_dump_load_public_key():
    public_key, private_key = Ed25519Cryptor.generate()

    public_key_bytes = Ed25519Cryptor.dump_public_key(public_key)
    public_key = Ed25519Cryptor.load_public_key(public_key_bytes)
    assert Ed25519Cryptor.dump_public_key(public_key) == public_key_bytes


def test_ed25519_dump_load_private_key():
    public_key, private_key = Ed25519Cryptor.generate()

    private_key_bytes = Ed25519Cryptor.dump_private_key(private_key)
    private_key = Ed25519Cryptor.load_private_key(private_key_bytes)
    assert Ed25519Cryptor.dump_private_key(private_key) == private_key_bytes


x25519_plaintext = b'this_is_x25519_plaintext.'


def test_x25519_exchange():
    foo_public_key, foo_private_key = X25519Cryptor.generate()
    bar_public_key, bar_private_key = X25519Cryptor.generate()

    foo_bar_shared_key = X25519Cryptor.exchange(foo_private_key, bar_public_key)
    bar_foo_shared_key = X25519Cryptor.exchange(bar_private_key, foo_public_key)
    assert foo_bar_shared_key == bar_foo_shared_key


def test_x25519_dump_load_public_key():
    public_key, private_key = X25519Cryptor.generate()

    public_key_bytes = X25519Cryptor.dump_public_key(public_key)
    public_key = X25519Cryptor.load_public_key(public_key_bytes)
    assert X25519Cryptor.dump_public_key(public_key) == public_key_bytes


def test_x25519_dump_load_private_key():
    public_key, private_key = X25519Cryptor.generate()

    private_key_bytes = X25519Cryptor.dump_private_key(private_key)
    private_key = X25519Cryptor.load_private_key(private_key_bytes)
    assert X25519Cryptor.dump_private_key(private_key) == private_key_bytes


totp_key = b'this_is_totp_key.'


def test_totp_generate_verify():
    timestamp = int(time.time())
    value = TOTPCryptor.generate(totp_key, timestamp)
    assert TOTPCryptor.verify(totp_key, value, timestamp) is True

    value = ''.join([str((int(x) + 1) % 10) for x in value.decode()]).encode()
    assert TOTPCryptor.verify(totp_key, value, timestamp) is False


def test_x509_generate_self_signed_certificate_authority():
    ca_public_key, ca_private_key = RSACryptor.generate()
    ca_certificate = X509Cryptor.generate_self_signed_certificate_authority(
        ca_public_key, ca_private_key
    )
    assert '-----BEGIN CERTIFICATE-----' in X509Cryptor.dump_certificate(ca_certificate).decode()
    assert '-----BEGIN PRIVATE KEY-----' in X509Cryptor.dump_private_key(ca_private_key).decode()


def test_x509_generate_certificate_signing_request():
    csr_public_key, csr_private_key = RSACryptor.generate()
    csr_certificate = X509Cryptor.generate_certificate_signing_request(
        csr_private_key
    )
    assert '-----BEGIN CERTIFICATE REQUEST-----' in X509Cryptor.dump_certificate(csr_certificate).decode()
    assert '-----BEGIN PRIVATE KEY-----' in X509Cryptor.dump_private_key(csr_private_key).decode()


def test_x509_generate_self_signed_certificate():
    ca_public_key, ca_private_key = RSACryptor.generate()
    ca_certificate = X509Cryptor.generate_self_signed_certificate_authority(
        ca_public_key, ca_private_key
    )
    my_public_key, my_private_key = RSACryptor.generate()
    my_certificate = X509Cryptor.generate_self_signed_certificate(
        my_public_key, my_private_key, ca_certificate=ca_certificate, ca_private_key=ca_private_key
    )
    assert '-----BEGIN CERTIFICATE-----' in X509Cryptor.dump_certificate(my_certificate).decode()
    assert '-----BEGIN PRIVATE KEY-----' in X509Cryptor.dump_private_key(my_private_key).decode()
