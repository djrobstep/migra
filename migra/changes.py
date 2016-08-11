from __future__ import unicode_literals

from .util import differences
from .statements import Statements
from functools import partial
from collections import OrderedDict as od

THINGS = [
    'enums',
    'sequences',
    'constraints',
    'functions',
    'views',
    'indexes',
    'extensions'
]

PK = 'PRIMARY KEY'


def statements_for_changes(
        things_from,
        things_target,
        creations_only=False,
        drops_only=False,
        modifications=True):

    added, removed, modified, _ = \
        differences(things_from, things_target)

    statements = Statements()

    if not creations_only:
        for k, v in removed.items():
            statements.append(v.drop_statement)

    if not drops_only:
        for k, v in added.items():
            statements.append(v.create_statement)

    if modifications:
        for k, v in modified.items():
            if not creations_only:
                statements.append(v.drop_statement)
            if not drops_only:
                statements.append(v.create_statement)

    return statements


def get_enum_modifications(
        tables_from,
        tables_target,
        enums_from,
        enums_target):

    _, _, e_modified, _ = differences(enums_from, enums_target)
    _, _, t_modified, _ = differences(tables_from, tables_target)

    pre = Statements()
    recreate = Statements()
    post = Statements()

    enums_to_change = e_modified

    for t, v in t_modified.items():
        t_before = tables_from[t]

        _, _, c_modified, _ = differences(t_before.columns, v.columns)

        for k, c in c_modified.items():
            before = t_before.columns[k]

            if c.is_enum == before.is_enum and c.dbtypestr == before.dbtypestr and c.enum != before.enum:
                pre.append(before.change_enum_to_string_statement(t))
                post.append(before.change_string_to_enum_statement(t))

    for e in enums_to_change.values():
        recreate.append(e.drop_statement)
        recreate.append(e.create_statement)

    return pre + recreate + post


def get_schema_changes(
        tables_from,
        tables_target,
        enums_from,
        enums_target):

    added, removed, modified, _ = differences(tables_from, tables_target)

    statements = Statements()

    for t, v in removed.items():
        statements.append(v.drop_statement)

    for t, v in added.items():
        statements.append(v.create_statement)

    statements += get_enum_modifications(tables_from, tables_target, enums_from, enums_target)

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
                self.i_target.tables,
                self.i_from.enums,
                self.i_target.enums)
        elif name == 'non_pk_constraints':
            a = self.i_from.constraints.items()
            b = self.i_target.constraints.items()

            a_od = od((k, v) for k, v in a if v.constraint_type != PK)
            b_od = od((k, v) for k, v in b if v.constraint_type != PK)

            return partial(statements_for_changes, a_od, b_od)
        elif name == 'pk_constraints':
            a = self.i_from.constraints.items()
            b = self.i_target.constraints.items()

            a_od = od((k, v) for k, v in a if v.constraint_type == PK)
            b_od = od((k, v) for k, v in b if v.constraint_type == PK)

            return partial(statements_for_changes, a_od, b_od)
        elif name in THINGS:
            return partial(
                statements_for_changes,
                getattr(self.i_from, name),
                getattr(self.i_target, name))
        else:
            raise AttributeError(name)
