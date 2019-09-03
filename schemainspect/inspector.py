from __future__ import absolute_import, division, print_function, unicode_literals

from abc import abstractmethod
from collections import OrderedDict as od


def to_pytype(sqla_dialect, typename):
    try:
        sqla_obj = sqla_dialect.ischema_names[typename]()
    except KeyError:
        return type(None)

    try:
        return sqla_obj.python_type

    except (NotImplementedError):
        return type(sqla_obj)


class DBInspector(object):
    def __init__(self, c, include_internal=False, tables=None, tables_only=False):
        self.c = c
        self.engine = self.c.engine
        self.dialect = self.engine.dialect
        self.include_internal = include_internal
        self.tables_only = tables_only
        self.selected_tables = tables
        self.load_all()

    def to_pytype(self, typename):
        return to_pytype(self.dialect, typename)

    @abstractmethod
    def load_all(self):
        pass


class NullInspector(DBInspector):
    def __init__(self):
        pass

    def __getattr__(self, name):
        return od()
