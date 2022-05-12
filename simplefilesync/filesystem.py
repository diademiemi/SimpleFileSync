import inotify.adapters

from simplefilesync import socket, config

import os
import hashlib
import time

def startInotify():
    global files
    files = {}
    # Make accessible from write_file function
    global watchFor
    # Filter of events to watch for
    watchFor = inotify.constants.IN_MODIFY | inotify.constants.IN_CLOSE_WRITE | inotify.constants.IN_CREATE

    # Make accessible from write_file function
    global inotifs
    inotifs = inotify.adapters.Inotify()

    # Register watchers
    for filename in config.config['synced_files']:
        # Create empty file if it doesn't exist. inotify will error otherwise.
        if not os.path.exists(filename):
            open(filename, 'a').close()
        # Add watcher
        inotifs.add_watch(filename, watchFor)
        # Add file to filesDict
        with open(filename, 'r') as f:
            files[filename] = {
                'md5': hashlib.md5(f.read().encode()).hexdigest(),
                'lastChanged': os.path.getmtime(filename),
                'lastChangedBy': '',
                }

    while True:
        events = inotifs.event_gen()
        for event in events:
            # Check if event is a file modification
            if event is None:
                continue
            # Print to console
            print("[INFO] Modified file {}".format(event[2]))
            # Change statefile
            with open(filename, 'r') as f:
                files[filename] = {
                    'md5': hashlib.md5(f.read().encode()).hexdigest(),
                    'lastChanged': time.time(),
                    'lastChangedBy': 'self',
                    }
            # Send file to remote hosts
            socket.sendAll(event[2])

def write_file(filename, content, address):
    try:
        # Temporarily remove watcher so it doesn't fire infinitely
        inotifs.remove_watch(filename)
        try:
            # Write file
            with open(filename, 'w') as f:
                f.write(content)
            # Add files hash
            with open(filename, 'r') as f:
                files[filename] = {
                    'md5': hashlib.md5(f.read().encode()).hexdigest(),
                    'lastChanged': time.time(),
                    'lastChangedBy': address,
                    }
        except Exception as e:
            print("[ERROR] Could not write file")
            print(e)
        # Add watcher back
        inotifs.add_watch(filename, watchFor)
    except Exception as e:
        # Vim is weird and locks files, moves them to a temp file, and then moves them back, etc.
        print("[WARNING] Was this file modified with vim? If so this error can be ignored.")
        print(e)
