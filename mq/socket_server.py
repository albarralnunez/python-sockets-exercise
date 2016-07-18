from thread import *
import logging
import socket


logging.basicConfig(
    level=logging.DEBUG,
    format='%(relativeCreated)6d %(threadName)s %(message)s'
)


class SocketServer:
    '''
    Simple socket server using threads
    '''

    def __init__(self, host, port):
        self.host = host   # Symbolic name meaning all available interfaces
        self.port = port  # Arbitrary non-privileged port

    def create(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info('Socket created')

        #  Bind socket to local host and port
        try:
            self.s.bind((self.host, self.port))
        except socket.error as msg:
            logging.warning(
                'Bind failed. Error Code : ' +
                str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        logging.info('Socket bind complete')

        #  Start listening on socket
        self.s.listen(10)
        logging.info('Socket now listening')

    def accept(self):
        self.conn, self.addr = self.s.accept()

    def close(self):
        self.s.close()

    def send(self, data):
        if data:
            data_len = '{0:04d}'.format(len(data))
            self.conn.send(data_len)
            self.conn.send(data)

    def recv(self):
        a = self.conn.recv(4)
        msg = self.conn.recv(int(a))
        return msg
