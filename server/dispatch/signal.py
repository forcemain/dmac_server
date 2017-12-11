#! -*- coding: utf-8 -*-


from __future__ import with_statement


from threading import Lock


def _make_id(obj):
    if hasattr(obj, '__func__'):
        # for method
        self_id = id(getattr(obj, '__self__'))
        func_id = id(getattr(obj, '__func__'))
        return self_id, func_id
    else:
        # for func
        return id(obj)


class Signal(object):
    def __init__(self, providing_args=None):
        self.lock = Lock()
        self.receivers = []
        # not used, just remind must be same as reciver kwargs.keys()
        self.providing_args = set(providing_args or [])

    def connect(self, receiver, sender=None):
        with self.lock:
            lookup_key = _make_id(receiver), _make_id(sender)
            for k, v in self.receivers:
                if k == lookup_key:
                    break
            else:
                self.receivers.append((lookup_key, receiver))

    def send(self, sender, **kwargs):
        with self.lock:
            if not self.receivers:
                return []
            return map(lambda r: (r, r(sender, **kwargs)), self._live_receivers(sender))

    def disconnect(self, receiver, sender=None):
        with self.lock:
            lookup_key = _make_id(receiver), _make_id(sender)
            for index, item in enumerate(self.receivers):
                k, v = item
                if k != lookup_key:
                    continue
                del self.receivers[index]

    def _live_receivers(self, sender):
        receivers = []
        lookup_sender_id = _make_id(sender)
        for k, v in self.receivers:
            if k[1] != lookup_sender_id:
                continue
            receivers.append(v)

        return receivers


def reciver(signal, **kwargs):
    def _decorator(func):
        if isinstance(signal, (list, tuple)):
            # register signal callback when code preloading
            map(lambda r: r.connect(func, **kwargs), signal)
        else:
            signal.connect(func, **kwargs)
    return _decorator
