'''
Based On: http://eyalarubas.com/python-subproc-nonblock.html

A Nonblocking alternative to stdout.

'''
from threading import Thread
from Queue import Queue, Empty

class NonBlockingStreamReader:
    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''
        self._s = stream
        self._q = Queue()
        
        def _populateQueue(stream, queue):
            '''
            Collects lines from the input stream, placing them in the queue.
            '''
            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    raise UnexpectedEndOfStream
        
        self._t = Thread(target=_populateQueue, args=(self._s, self._q))
        self._t.daemon = True
        self._t.start() # Start collecting lines from the stream
    
    def readline(self, timeout=None):
        try:
            has_timeout = (timeout is not None)
            return self._q.get(block=has_timeout, timeout=timeout)
        except Empty:
            return None

class UnexpectedEndOfStream(Exception): pass