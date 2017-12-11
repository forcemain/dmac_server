#! -*- coding: utf-8 -*-


from server.dispatch.signal import Signal


pre_delete = Signal(providing_args=["instance"])
post_delete = Signal(providing_args=["instance"])
pre_save = Signal(providing_args=["instance", "raw", "update_fields"])
post_save = Signal(providing_args=["instance", "raw", "created", "update_fields"])
