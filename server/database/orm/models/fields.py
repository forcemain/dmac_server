#! -*- coding: utf-8 -*-


class NOT_PROVIDED:
    pass


class Field(object):
    def __init__(self, name, primary_key=False, default=NOT_PROVIDED):
        self.name = name
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<{0}:{1}>'.format(self.__class__.__name__, self.name)


class TextField(Field):
    description = 'text'
    pass


class IntegerField(Field):
    description = 'integer'
    pass
