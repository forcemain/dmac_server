#! -*- coding: utf-8 -*-


from server.database.orm.models import sql as _sql


class QuerySet(object):
    def __init__(self, model=None, query=None):
        self.model = model
        self.query = query or _sql.Query(self.model)

    def create(self, **kwargs):
        return self.query.create(**kwargs)

    def get(self, **kwargs):
        return self.query.get(**kwargs)

    def filter(self, **kwargs):
        return self.query.filter(**kwargs)

