#! -*- coding: utf-8 -*-


import os


from server.settings import DATABASES
from server.database.db_wrapper import SqliteMultithread


base_dir = os.path.dirname(__file__)
server_dir = os.path.dirname(base_dir)
project_dir = os.path.dirname(server_dir)


def create_engine(dict_conf):
    registed_engine = {
        'sqlite3': SqliteMultithread
    }
    engine_name = dict_conf.pop('engine')
    return registed_engine.get(engine_name, 'sqlite3')(**dict_conf)


db = create_engine(DATABASES['default'])
