from __future__ import unicode_literals

from .util import differences
from .statements import Statements
from functools import partial
from sqlbag import quoted_identifier

THINGS = [
    'sequences',
    'constraints',
    'functions',
    'views',
    'indexes',
    'extensions'
]


def fully_quoted(name, schema):
    return '{}.{}'.format(quoted_identifier(schema), quoted_identifier(name))


def get_changes(
        i_from,
        i_target,
        thing,
        creations_only=False,
        drops_only=False,
        specific_table=None):

    added, removed, modified, unmodified = \
        differences(getattr(i_from, thing), getattr(i_target, thing))

    if specific_table:
        added = {k: v for k, v in added.items()
                 if fully_quoted(v.table_name, v.schema) == specific_table}
        removed = {k: v for k, v in removed.items()
                   if fully_quoted(v.table_name, v.schema) == specific_table}
        modified = {k: v for k, v in modified.items()
                    if fully_quoted(v.table_name, v.schema) == specific_table}

    statements = Statements()

    if not drops_only:
        for k, v in added.items():
            statements.append(v.create_statement)

    if not creations_only:
        for k, v in removed.items():
            statements.append(v.drop_statement)

    for k, v in modified.items():
        if not creations_only:
            statements.append(v.drop_statement)
        if not drops_only:
            statements.append(v.create_statement)

    return statements


def get_schema_changes(i_from, i_target):
    added, removed, modified, _ = differences(i_from.tables, i_target.tables)

    statements = Statements()

    for t, v in removed.items():
        statements.append(v.drop_statement)

    indexes = Statements()
    constraints = Statements()

    for t, v in added.items():
        statements.append(v.create_statement)

        indexes += get_changes(i_from, i_target, 'indexes', specific_table=t)

        constraints += get_changes(i_from, i_target, 'constraints', specific_table=t)

    statements += indexes
    statements += constraints

    for t, v in modified.items():
        before = i_from.tables[t]
        c_added, c_removed, c_modified, _ = \
            differences(before.columns, v.columns)

        for k, c in c_added.items():
            statements.append(
                'alter table {t} add column {k} {dtype};'.format(
                    k=c.quoted_name, t=v.quoted_full_name, dtype=c.dbtypestr)
            )

        for k, c in c_removed.items():
            statements.append(
                'alter table {t} drop column {k};'.format(
                    k=c.quoted_name, t=t)
            )
        for k, c in c_modified.items():
            bc = before.columns[k]
            if bc.not_null != c.not_null:
                keyword = 'set' if c.not_null else 'drop'

                stmt = 'alter table {} alter column {} {} not null;'.format(
                    v.quoted_full_name,
                    c.quoted_name,
                    keyword
                )
                statements.append(stmt)
            if bc.default != c.default:
                if c.default:
                    stmt = 'alter table {} alter column {} set default {};'.format(
                        v.quoted_full_name,
                        c.quoted_name,
                        c.default
                    )
                else:
                    stmt = 'alter table {} alter column {} drop default;'.format(
                        v.quoted_full_name,
                        c.quoted_name
                    )
                statements.append(stmt)

        indexes = get_changes(i_from, i_target, 'indexes', specific_table=t)
        statements += indexes

        constraints = get_changes(i_from, i_target, 'constraints', specific_table=t)
        statements += constraints
    return statements


class Changes(object):
    def __init__(self, i_from, i_target):
        self.i_from = i_from
        self.i_target = i_target

    def __getattr__(self, name):
        if name == 'schema':
            return partial(get_schema_changes, self.i_from, self.i_target)
        elif name in THINGS:
            return partial(get_changes, self.i_from, self.i_target, name)
        else:
            raise AttributeError(name)
