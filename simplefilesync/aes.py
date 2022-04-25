from Crypto.Cipher import AES

import simplefilesync.config as config

# Encrypt the message with AES
def encrypt_message(message):
    cipher = AES.new(config.config['shared_secret'].encode(), AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    return cipher.nonce, tag, ciphertext

# Decrypt the message with AES
def decrypt_message(nonce, tag, ciphertext):
    cipher = AES.new(config.config['shared_secret'].encode(), AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
