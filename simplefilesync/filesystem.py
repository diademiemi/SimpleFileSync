import inotify.adapters

import simplefilesync.config as config
import simplefilesync.socket as socket

import os

def startInotify():
    global watchFor
    watchFor = inotify.constants.IN_MODIFY | inotify.constants.IN_CLOSE_WRITE | inotify.constants.IN_CREATE


    global inotifs
    inotifs = inotify.adapters.Inotify()
    for file in config.config['synced_files']:
        if not os.path.exists(file):
            open(file, 'a').close()

        inotifs.add_watch(file, watchFor)

    while True:
        events = inotifs.event_gen()
        for event in events:
            if event is None:
                continue
            print("Modified file {}".format(event[2]))
            socket.sendAll(event[2])

def write_file(filename, content):
    try:

        inotifs.remove_watch(filename)
        with open(filename, 'w') as f:
            f.write(content)
        inotifs.add_watch(filename, watchFor)
    except Exception as e:
        print(e)
        print("Was this file modified with vim? If so this error can be ignored.")