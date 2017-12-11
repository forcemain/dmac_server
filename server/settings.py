#! -*- coding: utf-8 -*-

import os


base_dir = os.path.dirname(__file__)
server_dir = os.path.dirname(base_dir)
project_dir = os.path.dirname(server_dir)


DATABASES = {
    'default': {
        'engine': 'sqlite3',
        'filename': os.path.join(project_dir, 'dmac_center.sqlite3'),
        'autocommit': True,
        'journal_mode': 'DELETE'
    }
}
