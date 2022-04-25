from Crypto.Cipher import AES

import simplefilesync.config as config

def encrypt_message(message):
    cipher = AES.new(config.config['shared_secret'].encode(), AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return cipher.nonce, tag, ciphertext

def decrypt_message(nonce, tag, ciphertext):
    cipher = AES.new(config.config['shared_secret'].encode(), AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
