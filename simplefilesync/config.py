import yaml
import random
import string
import os
import socket

def init(args):
    # Make config public
    global config

    # Create config file if it doesn't exist
    if not os.path.exists(args.config):
        open(args.config, 'a').close()
        print("Creating default config file at {}".format(args.config) + "\nPlease edit this file to configure this program")

    # Load config file
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    # Create shared secret if it doesn't exist
    if config is None or 'shared_secret' not in config or config['shared_secret'] == '' or len(config['shared_secret']) != 32:
        chars =  string.hexdigits
        key = ''.join(random.choice(chars) for _ in range(32))
        config = {'shared_secret': key}
        print("Generated new 32 character secret in config file")

    # Add default hosts if they don't exist
    if 'remote_hosts' not in config or len(config['remote_hosts']) == 0:
        config['remote_hosts'] = [
            '10.10.10.1',
            '10.10.10.2'
        ]

    # Add default bind ip if it doesn't exist
    if 'bind_ip' not in config:
        config['bind_ip'] = '0.0.0.0'

    # Add default port if it doesn't exist
    if 'port' not in config:
        config['port'] = 54321

    # Add default synced files if they don't exist
    if 'synced_files' not in config or len(config['remote_hosts']) == 0:
        config['synced_files'] = [
            '/home/user/test.txt'
        ]

    # Add default synced files if they don't exist
    if 'statefile' not in config:
        config['statefile'] = '/tmp/simplefilesync.state'

    # Rewrite config file
    with open(args.config, 'w') as f:
        yaml.dump(config, f)

    # Remove own IP from remote hosts. Only in memory, don't write this to the config file.
    # Not foolproof, you should still remove it from the config.
    if socket.gethostbyname(socket.gethostname()) in config['remote_hosts']:
        config['remote_hosts'].remove(socket.gethostbyname(socket.gethostname()))