import argparse
import threading

from simplefilesync import config, filesystem, socket, statefile

# Definition for the filesystem watcher thread
class InotifyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        filesystem.startInotify()

# Definition for the socket thread
class SocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        socket.start()

# Definition for the socket thread
class StateThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        statefile.start()


# Argument parser
parser = argparse.ArgumentParser(description='Sync files between a pool of servers')

# Custom config file location as argument
parser.add_argument('-c', '--config', help='Path to config file', default='sync.yaml')
args = parser.parse_args()

def main():
    # Load or create config
    config.init(args)
    # Create the threads
    inotifyThread = InotifyThread()
    socketThread = SocketThread()
    stateThread = StateThread()
    # Start the threads
    inotifyThread.start()
    socketThread.start()
    stateThread.start()

    # Wait for threads to finish, then quit
    inotifyThread.join()
    socketThread.join()
    stateThread.join()

if __name__ == '__main__':
    # Start the program
    main()