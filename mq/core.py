from multiprocessing import Queue
from socket_server import SocketServer
from thread import start_new_thread
from process_handler import ProcessHandler
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(relativeCreated)6d %(asctime)s %(message)s'
)


class MqHelper(ProcessHandler):

    def __init__(self):
        self.tq = Queue()
        super(MqHelper, self).__init__()

    def _queue_linesplit(self):
        ss = SocketServer(host='localhost', port=8888)
        ss.create()
        self.lg.info('8888 Waiting connection...')
        while True:
            ss.accept()
            self.lg.info('Connection Accepted!')
            self.lg.info('8888 Waiting for stream...')
            data = ss.recv()
            while data != '\n':
                self.tq.put(data)
                data = ss.recv()
            self.tq.put(data)
        ss.close()

    def _shipper(self, none):
        ss = SocketServer(host='localhost', port=8887)
        ss.create()
        self.lg.info('Waiting sub')
        while True:
            ss.accept()
            while True:
                data = self.tq.get()
                try:
                    ss.send(data)
                except:
                    logging.warning('Connection with 8887 losed')
                    self.tq.put(data)
                    break
        ss.close()


class SubQueue(MqHelper):

    def run(self, lg):
        self.lg = lg
        start_new_thread(self._shipper, (1,))
        self._queue_linesplit()


class PubQueue(ProcessHandler):

    def run(self, lg):
        self.lg = lg
        ss = SocketServer(host='localhost', port=9999)
        ss.create()
        self.lg.info('9999 Waiting connection...')
        while True:
            ss.accept()
            while True:
                with open('res/results.txt', 'a') as outfile:
                    try:
                        data = ss.recv()
                        outfile.write(data)
                    except:
                        logging.warning('Connection with 9999 losed')
                        break
        ss.close()


def main():
    process = SubQueue()
    process.start(logging)
    process = PubQueue()
    process.start(logging)
    while True:
        pass

if __name__ == "__main__":
    main()
