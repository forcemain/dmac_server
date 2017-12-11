#! -*- coding: utf-8 -*-


import inspect


from server.database.db import db
from server.database.orm.models.fields import Field
from server.database.orm.models.manager import Manager
from server.database.orm.models.signal import pre_save, post_save, pre_delete, post_delete


class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        # maybe someone try to instance Model
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        mapping = {}
        extattr = {}
        manager_tuple = [('objects', Manager())]
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                if v.primary_key is True:
                    extattr['__primary_key__'] = k
                mapping[k] = v
            if isinstance(v, Manager):
                manager_tuple.append((k, v))
        for k in mapping.iterkeys():
            attrs.pop(k)

        attrs.update(extattr)
        attrs['__table__'] = name
        attrs['__mapping__'] = mapping

        # attach manager for model Class or model Instance
        def add_to_class(manager_name, value):
            if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
                model = type.__new__(cls, name, bases, attrs)
                value.contribute_to_class(model, manager_name)

        for manager_item in manager_tuple:
            add_to_class(*manager_item)

        return type.__new__(cls, name, bases, attrs)


class Model(dict):
    # add metaclass
    __metaclass__ = ModelMetaClass

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)

    # compatible self.<attr> or self[<attr>]
    def __getattr__(self, k):
        return self[k] if k in self else None

    def __setattr__(self, k, v):
        self[k] = v

    def __str__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, super(Model, self).__str__())

    def save(self):
        """
        with signal:
            pre_save = Signal(providing_args=["instance", "raw", "update_fields"])
            post_save = Signal(providing_args=["instance", "raw", "created", "update_fields"])
        """
        fields = []
        placeholder = []
        args = []

        for k in self.__mapping__.iterkeys():
            fields.append(k)
            placeholder.append('?')
            args.append(getattr(self, k, None))

        sql = 'insert into {0} ({1}) values ({2})'.format(
            self.__table__, ','.join(fields), ','.join(placeholder)
        )

        # send pre_save and post_save, sender use ins class
        pre_save.send(sender=self.__class__, instance=self, raw=sql, update_fields=fields)
        # other database engine interface
        db.execute(sql, args)
        post_save.send(sender=self.__class__, instance=self, raw=sql, created=True, update_fields=fields)

    def delete(self):
        """
        with signal:
            pre_delete = Signal(providing_args=["instance"])
            post_delete = Signal(providing_args=["instance"])
        """
        args = []
        and_conditions = []
        for k in self.__mapping__.iterkeys():
            if self.__mapping__[k].primary_key:
                continue
            v = getattr(self, k, None)
            if v is None:
                continue
            args.append(v)
            and_conditions.append('{0}=?'.format(k))

        sql = 'delete from {0} where {1}'.format(self.__table__, ' and '.join(and_conditions))
        # send pre_delete and post_delete, sender use ins class
        pre_delete.send(sender=self.__class__, instance=self)
        db.execute(sql, args)
        post_delete.send(sender=self.__class__, instance=self)

    def update(self, **kwargs):
        args = []
        and_conditions = []
        set_conditions = []
        for k in kwargs:
            v = kwargs[k]
            args.append(v)
            set_conditions.append('{0}=?'.format(k))
        for k in self.__mapping__.iterkeys():
            if self.__mapping__[k].primary_key:
                continue
            v = getattr(self, k, None)
            if v is None:
                continue
            args.append(v)
            and_conditions.append('{0}=?'.format(k))

        select_sql = 'select {0} from {1} where {2}'.format(self.__primary_key__, self.__table__, and_conditions)
        sqlfmtdata = (self.__table__, ','.join(set_conditions), self.__primary_key__, select_sql)
        sql = 'update {0} set {1} where {2}=({3})'.format(*sqlfmtdata)
        db.execute(sql, args)




