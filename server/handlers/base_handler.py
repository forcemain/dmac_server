#! -*- coding: utf-8 -*-


from server.geoip.render import geoip_ins


class BaseHandler(object):
    def __init__(self, *args, **kwargs):
        pass

    def insert_to_db(self, **kwargs):
        pass

    def get_device_area(self, ip):
        return geoip_ins.city(ip) or 'Unknown'

    def unpack(self, data):
        dict_data = {}
        strip_data = data.replace('\x00', '').strip()
        if not strip_data or len(strip_data) != 54:
            return dict_data
        dict_data = {
            'd_mac': strip_data[5:22],
            'd_uuid': strip_data[22:38],
            'd_date': strip_data[38:48],
            'd_type': strip_data[-1],
        }

        return dict_data



