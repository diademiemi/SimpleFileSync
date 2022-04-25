import inotify.adapters

import simplefilesync.config as config
import simplefilesync.socket as socket

def startInotify():
    global watchFor
    watchFor = inotify.constants.IN_MODIFY | inotify.constants.IN_CLOSE_WRITE | inotify.constants.IN_CREATE


    global inotifs
    inotifs = inotify.adapters.Inotify()
    for file in config.config['synced_files']:
        inotifs.add_watch(file, watchFor)

    while True:
        events = inotifs.event_gen()
        for event in events:
            if event is None:
                continue
            print("Modified file {}".format(event[2]))
            socket.sendAll(event[2])

def write_file(filename, content):
    inotifs.remove_watch(filename)
    with open(filename, 'w') as f:
        f.write(content)
    inotifs.add_watch(filename, watchFor)
