import argparse
import threading

import simplefilesync.config as config
import simplefilesync.filesystem as filesystem
import simplefilesync.socket as socket

class InotifyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        filesystem.startInotify()

class SocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        socket.start()

parser = argparse.ArgumentParser(description='Sync files between a pool of servers')

parser.add_argument('-c', '--config', help='Path to config file', default='sync.yaml')
args = parser.parse_args()

def main():
    config.init(args)
    inotifyThread = InotifyThread()
    socketThread = SocketThread()

    inotifyThread.start()
    socketThread.start()

    inotifyThread.join()
    socketThread.join()

if __name__ == '__main__':
    main()