#! -*- coding: utf-8 -*-


from server.database.db import db


class Query(object):
    def __init__(self, model=None):
        self.model = model

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        obj.save()

        return obj

    def get(self, **kwargs):
        try:
            rec = self.filter(**kwargs).next()
            return self.model(**rec)
        except StopIteration:
            return None

    def filter(self, **kwargs):
        args = kwargs.values()
        and_conditions = ' and '.join(map(lambda s: '{0}=?'.format(s), kwargs.keys()))
        sql = 'select * from {0} where {1}'.format(self.model.__table__, and_conditions)

        # default guarantee atomicity with queue
        rec_iter = db.select(sql, args)
        for rec in rec_iter:
            yield self.model(**rec)