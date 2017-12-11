#! -*- coding: utf-8 -*-


import os
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0, os.path.dirname(__file__))


from server.adapter import Server
from server.handlers.server_handlers import MacUdpServerRequestHandler


def create_app():
    app = Server('nbtudp')
    app.reg_request_handler(MacUdpServerRequestHandler)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', 5556)
