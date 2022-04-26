import inotify.adapters

from simplefilesync import socket, config

import os

def startInotify():
    # Make accessible from write_file function
    global watchFor
    # Filter of events to watch for
    watchFor = inotify.constants.IN_MODIFY | inotify.constants.IN_CLOSE_WRITE | inotify.constants.IN_CREATE

    # Make accessible from write_file function
    global inotifs
    inotifs = inotify.adapters.Inotify()

    # Register watchers
    for file in config.config['synced_files']:
        # Create empty file if it doesn't exist. inotify will error otherwise.
        if not os.path.exists(file):
            open(file, 'a').close()
        # Add watcher
        inotifs.add_watch(file, watchFor)

    while True:
        events = inotifs.event_gen()
        for event in events:
            # Check if event is a file modification
            if event is None:
                continue
            # Print to console
            print("Modified file {}".format(event[2]))
            # Send file to remote hosts
            socket.sendAll(event[2])

def write_file(filename, content):
    try:
        # Temporarily remove watcher so it doesn't fire infinitely
        inotifs.remove_watch(filename)
        # Write file
        with open(filename, 'w') as f:
            f.write(content)
        # Add watcher back
        inotifs.add_watch(filename, watchFor)
    except Exception as e:
        print(e)
        # Vim is weird and locks files, moves them to a temp file, and then moves them back, etc.
        print("Was this file modified with vim? If so this error can be ignored.")