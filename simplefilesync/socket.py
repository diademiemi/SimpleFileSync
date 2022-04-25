import socket

import simplefilesync.aes as aes
import simplefilesync.config as config
import simplefilesync.filesystem as filesystem

import pickle
from struct import unpack, pack

def start():
    try:
        # Attempt to create socket and bind it to the IP and port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((config.config['bind_ip'], config.config['port']))
        sock.listen(1)
    except Exception as e:
        # if port is in use, exit
        print(e)
        print("Could not start server. Is it already running?")
        exit(1)

    # Start indefinite loop
    while True:
        # Accept a connection
        (connection, addr) = sock.accept()
        # Check if this is a connection from an allowed host
        if addr[0] in config.config['remote_hosts']:
            try:
                # Get the length of the message
                bytes = connection.recv(8)
                (length,) = unpack('>Q', bytes)
                # Get the message
                rec_content = b''
                # The message is sent in chunks, keep reading until all the bytes are read
                while len(rec_content) < length:
                    to_read = length - len(rec_content)
                    rec_content += connection.recv(4096 if to_read > 4096 else to_read)
            # Close the connection when done
            finally:
                connection.close()
            try:
                # Decrypt the binary data
                pickle_content = aes.decrypt_message(rec_content[:16], rec_content[16:32], rec_content[32:])
                # Load the Python dict from the binary data
                file = pickle.loads(pickle_content)
                # Print to console
                print("Received new {} from {}".format(file['filename'], addr[0]))
                # Write the new file
                filesystem.write_file(file['filename'], file['content'])
            except Exception as e:
                print(e)

def sendAll(file):
    # Loop for all known hosts
    for host in config.config['remote_hosts']:
        send(host, file)

def send(host, file):
    try:
        # Create socket to send data
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to remote host
        s.connect((host, config.config['port']))

        # Send file
        with open(file, 'r') as f:
            # Encode Python dict as binary data
            pickle_content = pickle.dumps({ "filename": file, "content": f.read() })
            # Encrypt binary data
            nonce, tag, ciphertext = aes.encrypt_message(pickle_content)
            # Send the length of the message
            length = pack('>Q', len(nonce + tag + ciphertext))
            s.sendall(length)
            # Send the message
            s.sendall(nonce + tag + ciphertext)
            print("Sent new {} to {}".format(file, host))
        # Close the socket
        s.close()
    except Exception as e:
        print(e)