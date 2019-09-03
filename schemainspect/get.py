from .inspector import NullInspector
from .misc import connection_from_s_or_c
from .pg import PostgreSQL

SUPPORTED = {"postgresql": PostgreSQL}


def get_inspector(x, schema=None, tables=None, tables_only=False):
    if x is None:
        return NullInspector()

    c = connection_from_s_or_c(x)
    try:
        ic = SUPPORTED[c.dialect.name]
    except KeyError:
        raise NotImplementedError

    inspected = ic(c, tables_only=tables_only, tables=tables)
    if schema:
        inspected.one_schema(schema)
    return inspected
