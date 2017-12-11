#! -*- coding: utf-8 -*-


from server.database.orm.models import Model
from server.database.orm.models.manager import Manager
from server.database.orm.models.fields import IntegerField, TextField


class DmacCenter(Model):
    objects = Manager()

    id = IntegerField(name='id', primary_key=True)
    d_mac = TextField(name='d_mac', default='')
    d_host = TextField(name='d_host', default='')
    d_uuid = TextField(name='d_uuid', default='')
    d_date = TextField(name='d_date', default='')
    d_type = TextField(name='d_type', default='')
    d_area = TextField(name='d_area', default='')






