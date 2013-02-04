# -*- coding: utf-8 -*-

import inspect

from json import JSONEncoder


def is_not_method(o):
    return not inspect.isroutine(o)


class ObjectJSONEncoder(JSONEncoder):

    def default(self, reject):
        non_methods = inspect.getmembers(reject, is_not_method)
        return {attr: value for attr, value in non_methods
                if (not attr.startswith('__')
                    and attr != 'when'
                    and attr != 'now')}
