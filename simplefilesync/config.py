import yaml
import random
import string
import os
import socket

def init(args):
    global config

    if not os.path.exists(args.config):
        open(args.config, 'a').close()
        print("Creating default config file at {}".format(args.config) + "\nPlease edit this file to configure this program")

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    if config is None or 'shared_secret' not in config or config['shared_secret'] == '' or len(config['shared_secret']) != 32:
        chars =  string.hexdigits
        key = ''.join(random.choice(chars) for _ in range(32))
        config = {'shared_secret': key}
        print("Generated new 32 character secret in config file")

    if 'remote_hosts' not in config or len(config['remote_hosts']) == 0:
        config['remote_hosts'] = [
            '10.10.10.1',
            '10.10.10.2'
        ]

    if 'bind_ip' not in config:
        config['bind_ip'] = '0.0.0.0'

    if 'port' not in config:
        config['port'] = 54321

    if 'synced_files' not in config or len(config['remote_hosts']) == 0:
        config['synced_files'] = [
            '/home/user/test.txt'
        ]

    with open(args.config, 'w') as f:
        yaml.dump(config, f)

    # Remove own IP from remote hosts. Only in memory, don't write this to the config file.
    if socket.gethostbyname(socket.gethostname()) in config['remote_hosts']:
        config['remote_hosts'].remove(socket.gethostbyname(socket.gethostname()))