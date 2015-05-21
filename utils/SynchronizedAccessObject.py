from threading import Lock

__author__ = 'mateusz'


class SynchronizedAccessObject(object):
    def __init__(self, obj):
        self.obj = obj
        self.lock = Lock()

    def __enter__(self):
        self.lock.acquire()
        return self.obj

    def __exit__(self, type, value, traceback):
        self.lock.release()