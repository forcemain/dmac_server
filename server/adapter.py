#! -*- coding: utf-8 -*-


from SocketServer import (TCPServer, UDPServer, ThreadingMixIn, ForkingMixIn)


class BTCPServer(TCPServer):
    """
    block tcp server
    """
    pass


class BUDPServer(UDPServer):
    """
    block udp server
    """
    pass


class NBFTCPServer(ForkingMixIn, TCPServer):
    """
    no-block tcp server with forking mode
    """
    pass


class NBFUDPServer(ForkingMixIn, UDPServer):
    """
    no-block udp server with forking mode
    """
    pass


class NBTTCPServer(ThreadingMixIn, TCPServer):
    """
    no-block tcp server with threading mode
    """
    pass


class NBTUDPServer(ThreadingMixIn, UDPServer):
    """
    no-block udp server with threading mode
    """
    pass


class Server(object):
    """
    server interface
    """
    def __init__(self, server_type):
        self.req_handler = None
        self.server_type = server_type

    @property
    def server_class(self):
        server_modes = {
            'btcp': BTCPServer,
            'budp': BUDPServer,
            'nbftcp': NBFTCPServer,
            'nbfudp': NBFUDPServer,
            'nbttcp': NBTTCPServer,
            'nbtudp': NBTUDPServer
        }
        return server_modes.get(self.server_type, 'nbttcp')

    def reg_request_handler(self, handler):
        self.req_handler = handler

    def run(self, host, port):
        app = self.server_class((host, port), self.req_handler)
        app.serve_forever()

