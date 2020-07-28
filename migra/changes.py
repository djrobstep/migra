from __future__ import unicode_literals

from collections import OrderedDict as od
from functools import partial

from .statements import Statements
from .util import differences

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
    "collations",
    "rlspolicies",
    "triggers",
]
PK = "PRIMARY KEY"


def statements_for_changes(
    things_from,
    things_target,
    creations_only=False,
    drops_only=False,
    modifications_only=False,
    modifications=True,
    dependency_ordering=False,
    add_dependents_for_modified=False,
    modifications_as_alters=False,
):
    added, removed, modified, unmodified = differences(things_from, things_target)

    return statements_from_differences(
        added=added,
        removed=removed,
        modified=modified,
        replaceable=None,
        creations_only=creations_only,
        drops_only=drops_only,
        modifications_only=modifications_only,
        modifications=modifications,
        dependency_ordering=dependency_ordering,
        old=things_from,
        modifications_as_alters=modifications_as_alters,
    )


def statements_from_differences(
    added,
    removed,
    modified,
    replaceable=None,
    creations_only=False,
    drops_only=False,
    modifications=True,
    dependency_ordering=False,
    old=None,
    modifications_only=False,
    modifications_as_alters=False,
):
    replaceable = replaceable or set()
    statements = Statements()

    pending_creations = set()
    pending_drops = set()

    creations = not (drops_only or modifications_only)
    drops = not (creations_only or modifications_only)
    modifications = (
        modifications or modifications_only and not (creations_only or drops_only)
    )

    drop_and_recreate = modifications and not modifications_as_alters
    alters = modifications and modifications_as_alters

    if drops:
        pending_drops |= set(removed)

    if creations:
        pending_creations |= set(added)

    if drop_and_recreate:
        if drops:
            pending_drops |= set(modified) - replaceable

        if creations:
            pending_creations |= set(modified)

    if alters:
        for k, v in modified.items():
            statements += v.alter_statements(old[k])

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
        if drops:
            for k, v in removed.items():
                if not has_remaining_dependents(v, pending_drops):
                    if k in pending_drops:
                        statements.append(old[k].drop_statement)
                        pending_drops.remove(k)
        if creations:
            for k, v in added.items():
                if not has_uncreated_dependencies(v, pending_creations):
                    if k in pending_creations:
                        statements.append(v.create_statement)
                        pending_creations.remove(k)
        if modifications:
            for k, v in modified.items():
                if drops:
                    if not has_remaining_dependents(v, pending_drops):
                        if k in pending_drops:
                            statements.append(old[k].drop_statement)
                            pending_drops.remove(k)
                if creations:
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


def get_enum_modifications(
    tables_from, tables_target, enums_from, enums_target, return_tuple=False
):
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
                (c.is_enum and before.is_enum)
                and c.dbtypestr == before.dbtypestr
                and c.enum != before.enum
            ):
                has_default = c.default and not c.is_generated

                if has_default:
                    pre.append(before.drop_default_statement(t))

                recast = c.change_enum_statement(v.quoted_full_name)

                recreate.append(recast)

                if has_default:
                    post.append(before.add_default_statement(t))

    unwanted_suffix = "__old_version_to_be_dropped"

    for e in enums_to_change.values():
        unwanted_name = e.name + unwanted_suffix

        rename = e.alter_rename_statement(unwanted_name)
        pre.append(rename)

        pre.append(e.create_statement)

        drop_statement = e.drop_statement_with_rename(unwanted_name)

        post.append(drop_statement)

    if return_tuple:
        return pre, recreate + post
    else:
        return pre + recreate + post


def get_table_changes(
    tables_from,
    tables_target,
    enums_from,
    enums_target,
    sequences_from,
    sequences_target,
):
    added, removed, modified, _ = differences(tables_from, tables_target)

    statements = Statements()
    for t, v in removed.items():
        statements.append(v.drop_statement)

    enums_pre, enums_post = get_enum_modifications(
        tables_from, tables_target, enums_from, enums_target, return_tuple=True
    )

    statements += enums_pre

    for t, v in added.items():
        statements.append(v.create_statement)
        if v.rowsecurity:
            rls_alter = v.alter_rls_statement
            statements.append(rls_alter)

    statements += enums_post

    for t, v in modified.items():
        before = tables_from[t]

        # drop/recreate tables which have changed from partitioned to non-partitioned
        if v.is_partitioned != before.is_partitioned:
            statements.append(v.drop_statement)
            statements.append(v.create_statement)
            continue

        if v.is_unlogged != before.is_unlogged:
            statements += [v.alter_unlogged_statement]

        # attach/detach tables with changed parent tables
        if v.parent_table != before.parent_table:
            statements += v.attach_detach_statements(before)

    for t, v in modified.items():
        before = tables_from[t]

        if not v.is_alterable:
            continue

        c_added, c_removed, c_modified, _ = differences(before.columns, v.columns)

        for k in list(c_modified):
            c = v.columns[k]
            c_before = before.columns[k]

            # there's no way to alter a table into/out of generated state
            # so you gotta drop/recreate
            if c.is_generated != c_before.is_generated:
                del c_modified[k]
                c_added[k] = c
                c_removed[k] = c_before

        for k, c in c_removed.items():
            alter = v.alter_table_statement(c.drop_column_clause)
            statements.append(alter)
        for k, c in c_added.items():
            alter = v.alter_table_statement(c.add_column_clause)
            statements.append(alter)
        for k, c in c_modified.items():
            statements += c.alter_table_statements(before.columns[k], t)

        if v.rowsecurity != before.rowsecurity:
            rls_alter = v.alter_rls_statement
            statements.append(rls_alter)

    seq_created, seq_dropped, seq_modified, _ = differences(
        sequences_from, sequences_target
    )

    for k in seq_created:
        seq_b = sequences_target[k]

        if seq_b.quoted_table_and_column_name:
            statements.append(seq_b.alter_ownership_statement)

    for k in seq_modified:
        seq_a = sequences_from[k]
        seq_b = sequences_target[k]

        if seq_a.quoted_table_and_column_name != seq_b.quoted_table_and_column_name:
            statements.append(seq_b.alter_ownership_statement)

    return statements


def get_selectable_differences(
    selectables_from,
    selectables_target,
    enums_from,
    enums_target,
    add_dependents_for_modified=True,
):
    tables_from = od((k, v) for k, v in selectables_from.items() if v.is_table)
    tables_target = od((k, v) for k, v in selectables_target.items() if v.is_table)

    other_from = od((k, v) for k, v in selectables_from.items() if not v.is_table)
    other_target = od((k, v) for k, v in selectables_target.items() if not v.is_table)

    added_tables, removed_tables, modified_tables, unmodified_tables = differences(
        tables_from, tables_target
    )
    added_other, removed_other, modified_other, unmodified_other = differences(
        other_from, other_target
    )

    _, _, modified_enums, _ = differences(enums_from, enums_target)

    changed_all = {}
    changed_all.update(modified_tables)
    changed_all.update(modified_other)
    modified_all = dict(changed_all)
    changed_all.update(removed_tables)
    changed_all.update(removed_other)

    replaceable = set()
    not_replaceable = set()

    if add_dependents_for_modified:

        for k, m in changed_all.items():
            old = selectables_from[k]

            if k in modified_all and m.can_replace(old):
                if not m.is_table:
                    changed_enums = [_ for _ in m.dependent_on if _ in modified_enums]
                    if not changed_enums:
                        replaceable.add(k)

                continue

            for d in m.dependents_all:
                if d in unmodified_other:
                    dd = unmodified_other.pop(d)
                    modified_other[d] = dd
                not_replaceable.add(d)
        modified_other = od(sorted(modified_other.items()))

    replaceable -= not_replaceable

    return (
        tables_from,
        tables_target,
        added_tables,
        removed_tables,
        modified_tables,
        added_other,
        removed_other,
        modified_other,
        replaceable,
    )


def get_trigger_changes(
    triggers_from,
    triggers_target,
    selectables_from,
    selectables_target,
    enums_from,
    enums_target,
    add_dependents_for_modified=True,
    **kwargs
):
    (
        _,
        _,
        _,
        _,
        modified_tables,
        _,
        _,
        modified_other,
        replaceable,
    ) = get_selectable_differences(
        selectables_from,
        selectables_target,
        enums_from,
        enums_target,
        add_dependents_for_modified,
    )

    added, removed, modified, unmodified = differences(triggers_from, triggers_target)

    modified_tables_and_other = set(modified_other)
    deps_modified = [
        k
        for k, v in unmodified.items()
        if v.quoted_full_selectable_name in modified_tables_and_other
        and v.quoted_full_selectable_name not in replaceable
    ]

    for k in deps_modified:
        modified[k] = unmodified.pop(k)

    return statements_from_differences(
        added, removed, modified, old=triggers_from, **kwargs
    )


def get_selectable_changes(
    selectables_from,
    selectables_target,
    enums_from,
    enums_target,
    sequences_from,
    sequences_target,
    add_dependents_for_modified=True,
):
    (
        tables_from,
        tables_target,
        _,
        _,
        _,
        added_other,
        removed_other,
        modified_other,
        replaceable,
    ) = get_selectable_differences(
        selectables_from,
        selectables_target,
        enums_from,
        enums_target,
        add_dependents_for_modified,
    )
    statements = Statements()

    def functions(d):
        return {k: v for k, v in d.items() if v.relationtype == "f"}

    statements += statements_from_differences(
        added_other,
        removed_other,
        modified_other,
        replaceable=replaceable,
        drops_only=True,
        dependency_ordering=True,
        old=selectables_from,
    )

    statements += get_table_changes(
        tables_from,
        tables_target,
        enums_from,
        enums_target,
        sequences_from,
        sequences_target,
    )

    if any([functions(added_other), functions(modified_other)]):
        statements += ["set check_function_bodies = off;"]

    statements += statements_from_differences(
        added_other,
        removed_other,
        modified_other,
        replaceable=replaceable,
        creations_only=True,
        dependency_ordering=True,
        old=selectables_from,
    )
    return statements


class Changes(object):
    def __init__(self, i_from, i_target):
        self.i_from = i_from
        self.i_target = i_target

    @property
    def extensions(self):
        return partial(
            statements_for_changes,
            self.i_from.extensions,
            self.i_target.extensions,
            modifications_as_alters=True,
        )

    @property
    def selectables(self):
        return partial(
            get_selectable_changes,
            od(sorted(self.i_from.selectables.items())),
            od(sorted(self.i_target.selectables.items())),
            self.i_from.enums,
            self.i_target.enums,
            self.i_from.sequences,
            self.i_target.sequences,
        )

    @property
    def non_pk_constraints(self):
        a = self.i_from.constraints.items()
        b = self.i_target.constraints.items()
        a_od = od((k, v) for k, v in a if v.constraint_type != PK)
        b_od = od((k, v) for k, v in b if v.constraint_type != PK)
        return partial(statements_for_changes, a_od, b_od)

    @property
    def pk_constraints(self):
        a = self.i_from.constraints.items()
        b = self.i_target.constraints.items()
        a_od = od((k, v) for k, v in a if v.constraint_type == PK)
        b_od = od((k, v) for k, v in b if v.constraint_type == PK)
        return partial(statements_for_changes, a_od, b_od)

    @property
    def triggers(self):
        return partial(
            get_trigger_changes,
            od(sorted(self.i_from.triggers.items())),
            od(sorted(self.i_target.triggers.items())),
            od(sorted(self.i_from.selectables.items())),
            od(sorted(self.i_target.selectables.items())),
            self.i_from.enums,
            self.i_target.enums,
        )

    @property
    def sequences(self):
        return partial(
            statements_for_changes,
            self.i_from.sequences,
            self.i_target.sequences,
            modifications=False,
        )

    def __getattr__(self, name):
        if name in THINGS:
            return partial(
                statements_for_changes,
                getattr(self.i_from, name),
                getattr(self.i_target, name),
            )

        else:
            raise AttributeError(name)
