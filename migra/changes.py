from __future__ import unicode_literals

from .util import differences
from .statements import Statements
from functools import partial


THINGS = [
    'sequences',
    'constraints',
    'functions',
    'views',
    'indexes',
    'extensions'
]


def statements_for_changes(
        things_from,
        things_target,
        creations_only=False,
        drops_only=False):

    added, removed, modified, _ = \
        differences(things_from, things_target)

    statements = Statements()

    if not creations_only:
        for k, v in removed.items():
            statements.append(v.drop_statement)

    if not drops_only:
        for k, v in added.items():
            statements.append(v.create_statement)

    for k, v in modified.items():
        if not creations_only:
            statements.append(v.drop_statement)
        if not drops_only:
            statements.append(v.create_statement)

    return statements


def get_schema_changes(tables_from, tables_target):
    added, removed, modified, _ = differences(tables_from, tables_target)

    statements = Statements()

    for t, v in removed.items():
        statements.append(v.drop_statement)

    for t, v in added.items():
        statements.append(v.create_statement)

    for t, v in added.items():
        statements += [i.create_statement for i in v.indexes.values()]

    for t, v in added.items():
        statements += [c.create_statement for c in v.constraints.values()]

    for t, v in modified.items():
        before = tables_from[t]
        c_added, c_removed, c_modified, _ = \
            differences(before.columns, v.columns)

        for k, c in c_removed.items():
            alter = v.alter_table_statement(c.drop_column_clause)
            statements.append(alter)

        for k, c in c_added.items():
            alter = v.alter_table_statement(c.add_column_clause)
            statements.append(alter)

        for k, c in c_modified.items():
            statements += c.alter_table_statements(before.columns[k], t)

        statements += statements_for_changes(before.constraints, v.constraints)
        statements += statements_for_changes(before.indexes, v.indexes)

    return statements


class Changes(object):
    def __init__(self, i_from, i_target):
        self.i_from = i_from
        self.i_target = i_target

    def __getattr__(self, name):
        if name == 'schema':
            return partial(
                get_schema_changes,
                self.i_from.tables,
                self.i_target.tables)
        elif name in THINGS:
            return partial(
                statements_for_changes,
                getattr(self.i_from, name),
                getattr(self.i_target, name))
        else:
            raise AttributeError(name)
