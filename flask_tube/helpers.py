# -*- coding: utf-8 -*-

__all__ = ['update_object']


def update_object(obj, data):
    for key, value in data.iteritems():
        setattr(obj, key, value)
    return obj
