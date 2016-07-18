from thread import *
from multiprocessing import Process, Pipe
import abc
import logging
from socket import socket


class ProcessPull():

    def __init__(self, limit, handler):
        self.process_pull = []
        self.max = limit
        self.handler = handler
        self.sock = socket()
        self.sock.connect(('localhost', 9999))

    def new_process(self, daemonic, pipe, *args):
        while len(self.process_pull) > self.max:
            self._clean_process()
        p = self.handler(daemonic, pipe)
        p.start(*args)
        self.process_pull.append(p)

    def _clean_process(self):
        for p in self.process_pull:
            if p.process.exitcode is not None:
                # logging.info(str(p.process.pid) + 'cleaned')
                if p.pipe:
                    a = p.parent_conn.recv()
                    self.handle_pipe(a)
                self.process_pull.remove(p)
                p.join()

    def clean_all_process(self):
        while len(self.process_pull) > 0:
            self._clean_process()

    @abc.abstractmethod
    def handle_pipe(data):
        pass


class ProcessHandler:
    '''
    run(): The run() method is the entry point for a thread.
    start(): The start() method starts a thread by calling the run method.
    join([time]): The join() waits for threads to terminate.
    isAlive(): The isAlive() method checks whether a thread is still executing.
    '''

    def __init__(self, daemonic, pipe):
        self.daemonic = daemonic
        self.pipe = pipe
        if self.pipe:
            self.parent_conn, self.child_conn = Pipe(duplex=False)

    @abc.abstractmethod
    def run(self, *args):
        pass

    def start(self, *args):
        # Close write fd because parent not going to write
        if not self.pipe:
            self.process = Process(target=self.run, args=args)
        else:
            self.process = Process(
                target=self.run, args=(self.child_conn,) + args)
        if self.daemonic:
            self.process.daemon = True
        self.process.start()

    def join(self):
        if self.pipe:
            self.parent_conn.close()
            self.child_conn.close()
        self.process.join()
    """
    @classmethod
    def pull_size(cls):
        return len(cls.process_pull)

    @classmethod
    def max_process_pull(cls):
        return cls.max_process_pull

    @classmethod
    def list_process_pull(cls):
        return cls.process_pull

    @classmethod
    def clean_process(cls):
        for p in cls.process_pull:
            if p.exitcode is not None:
                cls.process_pull.remove(p)
                p.terminate()
    """
