from simplefilesync import config, filesystem

import threading
import time
import json

def write_file():
    content = {
        'files': filesystem.files,
        'time': time.time()
        }
    with open(config.config['statefile'], 'w') as f:
        f.write(json.dumps(content) + '\n')
    threading.Timer(5.0, write_file).start()

def start():
    write_file()