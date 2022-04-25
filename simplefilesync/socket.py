import socket

import simplefilesync.aes as aes
import simplefilesync.config as config
import simplefilesync.filesystem as filesystem

import pickle
from struct import unpack, pack

def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((config.config['bind_ip'], config.config['port']))
    sock.listen(1)

    while True:
        (connection, addr) = sock.accept()
        if addr[0] in config.config['remote_hosts']:
            try:
                bytes = connection.recv(8)
                (length,) = unpack('>Q', bytes)
                rec_content = b''
                while len(rec_content) < length:
                    to_read = length - len(rec_content)
                    rec_content += connection.recv(4096 if to_read > 4096 else to_read)

            finally:
                connection.close()
            # try:
            pickle_content = aes.decrypt_message(rec_content[:16], rec_content[16:32], rec_content[32:])
            file = pickle.loads(pickle_content)
            print(file)
            print("Received new {} from {}".format(file['filename'], addr[0]))
            filesystem.write_file(file['filename'], file['content'])
            # except Exception as e:
            #     print(e)

def sendAll(file):
    for host in config.config['remote_hosts']:
        send(host, file)

def send(host, file):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, config.config['port']))

        # Send file
        with open(file, 'r') as f:
            
            pickle_content = pickle.dumps({ "filename": file, "content": f.read() })
            print(pickle_content)
            nonce, tag, ciphertext = aes.encrypt_message(pickle_content)
            length = pack('>Q', len(nonce + tag + ciphertext))
            s.sendall(length)
            s.sendall(nonce + tag + ciphertext)
            print("Sent new {} to {}".format(file, host))
        
        s.close()
    except Exception as e:
        print(e)