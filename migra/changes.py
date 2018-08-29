from __future__ import unicode_literals

from .util import differences
from .statements import Statements
from functools import partial
from collections import OrderedDict as od


THINGS = [
    "schemas",
    "enums",
    "sequences",
    "constraints",
    "functions",
    "views",
    "indexes",
    "extensions",
    "privileges",
]
PK = "PRIMARY KEY"


def statements_for_changes(
    things_from,
    things_target,
    creations_only=False,
    drops_only=False,
    modifications=True,
    dependency_ordering=False,
    add_dependents_for_modified=False,
):
    added, removed, modified, unmodified = differences(things_from, things_target)

    return statements_from_differences(
        added,
        removed,
        modified,
        creations_only,
        drops_only,
        modifications,
        dependency_ordering,
    )


def statements_from_differences(
    added,
    removed,
    modified,
    creations_only=False,
    drops_only=False,
    modifications=True,
    dependency_ordering=False,
):
    statements = Statements()
    if not creations_only:
        pending_drops = set(removed)
        if modifications:
            pending_drops |= set(modified)
    else:
        pending_drops = set()
    if not drops_only:
        pending_creations = set(added)
        if modifications:
            pending_creations |= set(modified)
    else:
        pending_creations = set()

    def has_remaining_dependents(v, pending_drops):
        if not dependency_ordering:
            return False

        return bool(set(v.dependents) & pending_drops)

    def has_uncreated_dependencies(v, pending_creations):
        if not dependency_ordering:
            return False

        return bool(set(v.dependent_on) & pending_creations)

    while True:
        before = pending_drops | pending_creations
        if not creations_only:
            for k, v in removed.items():
                if not has_remaining_dependents(v, pending_drops):
                    if k in pending_drops:
                        statements.append(v.drop_statement)
                        pending_drops.remove(k)
        if not drops_only:
            for k, v in added.items():
                if not has_uncreated_dependencies(v, pending_creations):
                    if k in pending_creations:
                        statements.append(v.create_statement)
                        pending_creations.remove(k)
        if modifications:
            for k, v in modified.items():
                if not creations_only:
                    if not has_remaining_dependents(v, pending_drops):
                        if k in pending_drops:
                            statements.append(v.drop_statement)
                            pending_drops.remove(k)
                if not drops_only:
                    if not has_uncreated_dependencies(v, pending_creations):
                        if k in pending_creations:
                            statements.append(v.create_statement)
                            pending_creations.remove(k)
        after = pending_drops | pending_creations
        if not after:
            break

        elif (
            after == before
        ):  # this should never happen because there shouldn't be circular dependencies
            raise ValueError("cannot resolve dependencies")  # pragma: no cover

    return statements


def get_enum_modifications(tables_from, tables_target, enums_from, enums_target):
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
            if (
                c.is_enum == before.is_enum
                and c.dbtypestr == before.dbtypestr
                and c.enum != before.enum
            ):
                pre.append(before.change_enum_to_string_statement(t))
                post.append(before.change_string_to_enum_statement(t))
    for e in enums_to_change.values():
        recreate.append(e.drop_statement)
        recreate.append(e.create_statement)
    return pre + recreate + post


def get_table_changes(tables_from, tables_target, enums_from, enums_target):
    added, removed, modified, _ = differences(tables_from, tables_target)

    statements = Statements()
    for t, v in removed.items():
        statements.append(v.drop_statement)
    for t, v in added.items():
        statements.append(v.create_statement)
    statements += get_enum_modifications(
        tables_from, tables_target, enums_from, enums_target
    )
    for t, v in modified.items():
        before = tables_from[t]
        c_added, c_removed, c_modified, _ = differences(before.columns, v.columns)
        for k, c in c_removed.items():
            alter = v.alter_table_statement(c.drop_column_clause)
            statements.append(alter)
        for k, c in c_added.items():
            alter = v.alter_table_statement(c.add_column_clause)
            statements.append(alter)
        for k, c in c_modified.items():
            statements += c.alter_table_statements(before.columns[k], t)
    return statements


def get_selectable_changes(
    selectables_from,
    selectables_target,
    enums_from,
    enums_target,
    add_dependents_for_modified=True,
):
    tables_from = od(
        (k, v) for k, v in selectables_from.items() if v.relationtype == "r"
    )
    tables_target = od(
        (k, v) for k, v in selectables_target.items() if v.relationtype == "r"
    )

    other_from = od(
        (k, v) for k, v in selectables_from.items() if v.relationtype != "r"
    )
    other_target = od(
        (k, v) for k, v in selectables_target.items() if v.relationtype != "r"
    )

    added_tables, removed_tables, modified_tables, unmodified_tables = differences(
        tables_from, tables_target
    )
    added_other, removed_other, modified_other, unmodified_other = differences(
        other_from, other_target
    )

    m_all = {}
    m_all.update(modified_tables)
    m_all.update(modified_other)
    m_all.update(removed_tables)
    m_all.update(removed_other)

    if add_dependents_for_modified:
        for k, m in m_all.items():
            for d in m.dependents_all:
                if d in unmodified_other:
                    modified_other[d] = unmodified_other.pop(d)
        modified_other = od(sorted(modified_other.items()))

    statements = Statements()

    def functions(d):
        return {k: v for k, v in d.items() if v.relationtype == "f"}

    statements += statements_from_differences(
        added_other,
        removed_other,
        modified_other,
        drops_only=True,
        dependency_ordering=True,
    )

    statements += get_table_changes(
        tables_from, tables_target, enums_from, enums_target
    )

    if any([functions(added_other), functions(modified_other)]):
        statements += ["set check_function_bodies = off;"]

    statements += statements_from_differences(
        added_other,
        removed_other,
        modified_other,
        creations_only=True,
        dependency_ordering=True,
    )
    return statements


class Changes(object):
    def __init__(self, i_from, i_target):
        self.i_from = i_from
        self.i_target = i_target

    def __getattr__(self, name):
        if name == "non_pk_constraints":
            a = self.i_from.constraints.items()
            b = self.i_target.constraints.items()
            a_od = od((k, v) for k, v in a if v.constraint_type != PK)
            b_od = od((k, v) for k, v in b if v.constraint_type != PK)
            return partial(statements_for_changes, a_od, b_od)

        elif name == "pk_constraints":
            a = self.i_from.constraints.items()
            b = self.i_target.constraints.items()
            a_od = od((k, v) for k, v in a if v.constraint_type == PK)
            b_od = od((k, v) for k, v in b if v.constraint_type == PK)
            return partial(statements_for_changes, a_od, b_od)

        elif name == "selectables":
            return partial(
                get_selectable_changes,
                od(sorted(self.i_from.selectables.items())),
                od(sorted(self.i_target.selectables.items())),
                self.i_from.enums,
                self.i_target.enums,
            )

        elif name in THINGS:
            return partial(
                statements_for_changes,
                getattr(self.i_from, name),
                getattr(self.i_target, name),
            )

        else:
            raise AttributeError(name)
