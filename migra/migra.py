from __future__ import unicode_literals

from schemainspect import DBInspector, get_inspector
from sqlbag import raw_execute

from .changes import Changes
from .statements import Statements


class Migration(object):
    """
    The main class of migra
    """

    def __init__(self, x_from, x_target, schema=None):
        self.statements = Statements()
        self.changes = Changes(None, None)
        self.schema = schema
        if isinstance(x_from, DBInspector):
            self.changes.i_from = x_from
        else:
            self.changes.i_from = get_inspector(x_from, schema=schema)
            if x_from:
                self.s_from = x_from
        if isinstance(x_target, DBInspector):
            self.changes.i_target = x_target
        else:
            self.changes.i_target = get_inspector(x_target, schema=schema)
            if x_target:
                self.s_target = x_target

    def inspect_from(self):
        self.changes.i_from = get_inspector(self.s_from, schema=self.schema)

    def inspect_target(self):
        self.changes.i_target = get_inspector(self.s_target, schema=self.schema)

    def clear(self):
        self.statements = Statements()

    def apply(self):
        for stmt in self.statements:
            raw_execute(self.s_from, stmt)
        self.changes.i_from = get_inspector(self.s_from, schema=self.schema)
        safety_on = self.statements.safe
        self.clear()
        self.set_safety(safety_on)

    def add(self, statements):
        self.statements += statements

    def add_sql(self, sql):
        self.statements += Statements([sql])

    def set_safety(self, safety_on):
        self.statements.safe = safety_on

    def add_extension_changes(self, creates=True, drops=True):
        if creates:
            self.add(self.changes.extensions(creations_only=True))
        if drops:
            self.add(self.changes.extensions(drops_only=True))

    def add_all_changes(self, privileges=False):
        self.add(self.changes.schemas(creations_only=True))

        self.add(self.changes.extensions(creations_only=True, modifications=False))
        self.add(self.changes.extensions(modifications_only=True, modifications=True))
        self.add(self.changes.collations(creations_only=True))
        self.add(self.changes.enums(creations_only=True, modifications=False))
        self.add(self.changes.sequences(creations_only=True))
        self.add(self.changes.triggers(drops_only=True))
        self.add(self.changes.rlspolicies(drops_only=True))
        if privileges:
            self.add(self.changes.privileges(drops_only=True))
        self.add(self.changes.non_pk_constraints(drops_only=True))
        self.add(self.changes.pk_constraints(drops_only=True))
        self.add(self.changes.indexes(drops_only=True))

        self.add(self.changes.selectables())

        self.add(self.changes.sequences(drops_only=True))
        self.add(self.changes.enums(drops_only=True, modifications=False))
        self.add(self.changes.extensions(drops_only=True, modifications=False))
        self.add(self.changes.indexes(creations_only=True))
        self.add(self.changes.pk_constraints(creations_only=True))
        self.add(self.changes.non_pk_constraints(creations_only=True))
        if privileges:
            self.add(self.changes.privileges(creations_only=True))
        self.add(self.changes.rlspolicies(creations_only=True))
        self.add(self.changes.triggers(creations_only=True))
        self.add(self.changes.collations(drops_only=True))
        self.add(self.changes.schemas(drops_only=True))

    @property
    def sql(self):
        return self.statements.sql
