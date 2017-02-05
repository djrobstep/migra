from __future__ import unicode_literals

from sqlbag import raw_execute
from schemainspect import get_inspector, DBInspector
from .changes import Changes
from .statements import Statements


class Migration(object):
    def __init__(self, x_from, x_target):
        self.statements = Statements()
        self.changes = Changes(None, None)

        if isinstance(x_from, DBInspector):
            self.changes.i_from = x_from
        else:
            self.changes.i_from = get_inspector(x_from)
            if x_from:
                self.s_from = x_from

        if isinstance(x_target, DBInspector):
            self.changes.i_target = x_target
        else:
            self.changes.i_target = get_inspector(x_target)
            if x_target:
                self.s_target = x_target

    def inspect_from(self):
        self.changes.i_from = get_inspector(self.s_from)

    def inspect_target(self):
        self.changes.i_target = get_inspector(self.s_target)

    def clear(self):
        self.statements = Statements()

    def apply(self):
        for stmt in self.statements:
            raw_execute(self.s_from, stmt)

        self.changes.i_from = get_inspector(self.s_from)
        safety_on = self.statements.safe
        self.clear()
        self.set_safety(safety_on)

    def add(self, statements):
        self.statements += statements

    def add_sql(self, sql):
        self.statements += Statements([sql])

    def set_safety(self, safety_on):
        self.statements.safe = safety_on

    def add_all_changes(self):
        self.add(self.changes.extensions(creations_only=True))
        self.add(self.changes.enums(creations_only=True, modifications=False))
        self.add(self.changes.sequences(creations_only=True))

        self.add(self.changes.non_pk_constraints(drops_only=True))
        self.add(self.changes.pk_constraints(drops_only=True))
        self.add(self.changes.indexes(drops_only=True))

        self.add(self.changes.views(drops_only=True))
        self.add(self.changes.functions(drops_only=True))

        self.add(self.changes.schema())

        self.add(self.changes.views(creations_only=True))
        self.add(self.changes.functions(creations_only=True))

        self.add(self.changes.sequences(drops_only=True))
        self.add(self.changes.enums(drops_only=True, modifications=False))
        self.add(self.changes.extensions(drops_only=True))

        self.add(self.changes.indexes(creations_only=True))
        self.add(self.changes.pk_constraints(creations_only=True))
        self.add(self.changes.non_pk_constraints(creations_only=True))

    @property
    def sql(self):
        return self.statements.sql
