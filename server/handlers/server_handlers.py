#! -*- coding: utf-8 -*-


from server.models import DmacCenter
from SocketServer import DatagramRequestHandler
from server.handlers.base_handler import BaseHandler


class MacUdpServerRequestHandler(DatagramRequestHandler, BaseHandler):
    def handle(self):
        resp = '0' * 18
        data = self.rfile.readline()
        dict_data = self.unpack(data)
        if not dict_data:
            return
        d_host, d_port = self.client_address
        dict_data.update({
            'd_host': d_host,
            'd_port': d_port,
            'd_area': self.get_device_area(d_host)
        })
        # orm warehousing test, record Asia_Taiwan device enc info.
        if dict_data['d_area'] and dict_data['d_area'].startswith('Asia_Taiwan'):
            filter_conditions = {
                'd_mac': dict_data['d_mac'],
                'd_uuid': dict_data['d_uuid'],
                'd_type': dict_data['d_type']
            }
            get_res = DmacCenter.objects.get(**filter_conditions)
            if get_res is None:
                DmacCenter.objects.create(**dict_data)
            else:
                print 'GetResult:', get_res, 'Ignore.'

        self.wfile.write(resp)
