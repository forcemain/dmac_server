#! -*- coding: utf-8 -*-


import inspect


from server.database.orm.models.query import QuerySet


class BaseManager(object):
    def __init__(self):
        self.name = None
        self.model = None

    def get_queryset(self):
        return self._queryset_class(model=self.model)

    def contribute_to_class(self, model, name):
        self.name = self.name or name
        self.model = model

        # for default manager
        setattr(model, name, self)
        # for mode manager

    @classmethod
    def _get_queryset_methods(cls, queryset_class):
        # filter method
        def is_userdefined_method(t):
            if inspect.isfunction(t) or inspect.ismethod(t):
                return True
            return False

        # proxy to instance method
        def create_method(name, method):
            def manager_method(self, *args, **kwargs):
                return getattr(self.get_queryset(), name)(*args, **kwargs)
            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__

            return manager_method

        new_methods = {}
        # ergdic class method
        for name, method in inspect.getmembers(queryset_class, predicate=is_userdefined_method):
            if name.startswith('_'):
                continue
            new_methods[name] = create_method(name, method)

        return new_methods

    @classmethod
    def from_queryset(cls, queryset_class, class_name=None):
        mapping = cls._get_queryset_methods(queryset_class)
        mapping['_queryset_class'] = queryset_class

        class_name = class_name or '{0}{1}'.format(queryset_class.__name__, cls.__name__)

        return type(class_name, (cls, ), mapping)


class Manager(BaseManager.from_queryset(QuerySet)):
    pass

