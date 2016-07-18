#!/usr/bin/env python

from socket import socket
from thread import *
import logging
from op_eval import eval_expr
from process_handler import ProcessHandler, ProcessPull

# from time import sleep

logging.basicConfig(
    level=logging.DEBUG,
    format='%(relativeCreated)6d %(asctime)s %(message)s'
)


class CustomProcesPull(ProcessPull):
    def handle_pipe(self, data):
        if data:
            data_len = '{0:04d}'.format(len(data))
            self.sock.send(data_len)
            self.sock.send(data)
        # logging.info('Data sended')


class Worker(ProcessHandler):

    def run(self, conn, lg, expr):
        res = eval_expr(expr)
        conn.send('%s = %s\n' % (expr.replace('\n', ''), res))


def main():
    sock = socket()
    logging.info('Trying to connect on 8887')
    logging.info('Connection established')
    logging.info('8887 Waiting for stream...')
    sock.connect(('localhost', 8887))
    pp = CustomProcesPull(10, Worker)
    while True:
        data_len = sock.recv(4)
        data = sock.recv(int(data_len))
        if data == '\n':
            pp.clean_all_process()
            logging.info('Finished')
        else:
            pp.new_process(True, True, logging, data)

    sock.close()

if __name__ == "__main__":
    main()
