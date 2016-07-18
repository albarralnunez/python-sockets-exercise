from thread import *
from multiprocessing import Process, Pipe
import abc


class ProcessHandler(object):
    '''
    run(): The run() method is the entry point for a thread.
    start(): The start() method starts a thread by calling the run method.
    join([time]): The join() waits for threads to terminate.
    isAlive(): The isAlive() method checks whether a thread is still executing.
    '''

    process_pull = []
    # max_process_pull = 10

    def __init__(self, daemonic=True, pipe=False):
        self.daemonic = daemonic
        self.pipe = pipe
        if pipe:
            self.parent_conn, self.child_conn = Pipe(duplex=False)

    @abc.abstractmethod
    def run(self, *args):
        pass

    def start(self, *args):
        # TODO: handle excep
        # Close write fd because parent not going to write
        self.process = Process(target=self.run, args=args)
        if self.daemonic:
            self.process.daemon = True
        self.process.start()
        self.__class__.process_pull.append(self.process)

    def join(self):
        self.parent_conn.close()
        if pipe:
            self.child_conn.close()
            self.process.join()

    @classmethod
    def pull_size(cls):
        return len(cls.process_pull)

    @classmethod
    def max_process_pull(cls):
        return cls.max_process_pull

    @classmethod
    def list_process_pull(cls):
        return cls.process_pull
