__author__ = 'mateusz'


def synchronized(lock):
    def wrap(f):
        def wrapFunction(*args, **kwargs):
            with lock:
                return f(*args, **kwargs)
        return wrapFunction
    return wrap