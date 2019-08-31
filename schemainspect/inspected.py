from collections import OrderedDict as od

from .misc import AutoRepr, quoted_identifier


class Inspected(AutoRepr):
    @property
    def quoted_full_name(self):
        return "{}.{}".format(
            quoted_identifier(self.schema), quoted_identifier(self.name)
        )

    @property
    def signature(self):
        return self.quoted_full_name

    @property
    def unquoted_full_name(self):
        return "{}.{}".format(self.schema, self.name)

    @property
    def quoted_name(self):
        return quoted_identifier(self.name)

    @property
    def quoted_schema(self):
        return quoted_identifier(self.schema)

    def __ne__(self, other):
        return not self == other


class TableRelated(object):
    @property
    def quoted_full_table_name(self):
        return "{}.{}".format(
            quoted_identifier(self.schema), quoted_identifier(self.table_name)
        )


class ColumnInfo(AutoRepr):
    def __init__(
        self,
        name,
        dbtype,
        pytype,
        default=None,
        not_null=False,
        is_enum=False,
        enum=None,
        dbtypestr=None,
        collation=None,
    ):
        self.name = name or ""
        self.dbtype = dbtype
        self.dbtypestr = dbtypestr or dbtype
        self.pytype = pytype
        self.default = default or None
        self.not_null = not_null
        self.is_enum = is_enum
        self.enum = enum
        self.collation = collation

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.dbtype == other.dbtype
            and self.dbtypestr == other.dbtypestr
            and self.pytype == other.pytype
            and self.default == other.default
            and self.not_null == other.not_null
            and self.enum == other.enum
            and self.collation == other.collation
        )

    def alter_clauses(self, other):
        clauses = []
        if self.default != other.default:
            clauses.append(self.alter_default_clause)
        if self.not_null != other.not_null:
            clauses.append(self.alter_not_null_clause)
        if self.dbtypestr != other.dbtypestr or self.collation != other.collation:
            clauses.append(self.alter_data_type_clause)
        return clauses

    def change_enum_to_string_statement(self, table_name):
        if self.is_enum:
            return "alter table {} alter column {} set data type varchar using {}::varchar;".format(
                table_name, self.quoted_name, self.quoted_name
            )

        else:
            raise ValueError

    def change_string_to_enum_statement(self, table_name):
        if self.is_enum:
            return "alter table {} alter column {} set data type {} using {}::{};".format(
                table_name,
                self.quoted_name,
                self.dbtypestr,
                self.quoted_name,
                self.dbtypestr,
            )

        else:
            raise ValueError

    def alter_table_statements(self, other, table_name):
        prefix = "alter table {}".format(table_name)
        return ["{} {};".format(prefix, c) for c in self.alter_clauses(other)]

    @property
    def quoted_name(self):
        return quoted_identifier(self.name)

    @property
    def creation_clause(self):
        x = "{} {}".format(self.quoted_name, self.dbtypestr)
        if self.not_null:
            x += " not null"
        if self.default:
            x += " default {}".format(self.default)
        return x

    @property
    def add_column_clause(self):
        return "add column {}{}".format(self.creation_clause, self.collation_subclause)

    @property
    def drop_column_clause(self):
        return "drop column {k}".format(k=self.quoted_name)

    @property
    def alter_not_null_clause(self):
        keyword = "set" if self.not_null else "drop"
        return "alter column {} {} not null".format(self.quoted_name, keyword)

    @property
    def alter_default_clause(self):
        if self.default:
            alter = "alter column {} set default {}".format(
                self.quoted_name, self.default
            )
        else:
            alter = "alter column {} drop default".format(self.quoted_name)
        return alter

    @property
    def collation_subclause(self):
        if self.collation:
            collate = " collate {}".format(quoted_identifier(self.collation))
        else:
            collate = ""
        return collate

    @property
    def alter_data_type_clause(self):
        return "alter column {} set data type {}{} using {}::{}".format(
            self.quoted_name,
            self.dbtypestr,
            self.collation_subclause,
            self.quoted_name,
            self.dbtypestr,
        )


class InspectedSelectable(Inspected):
    def __init__(
        self,
        name,
        schema,
        columns,
        inputs=None,
        definition=None,
        dependent_on=None,
        dependents=None,
        comment=None,
        relationtype="unknown",
        parent_table=None,
        partition_def=None,
        rowsecurity=False,
        forcerowsecurity=False,
    ):
        self.name = name
        self.schema = schema
        self.inputs = inputs or []
        self.columns = columns
        self.definition = definition
        self.relationtype = relationtype
        self.dependent_on = dependent_on or []
        self.dependents = dependents or []
        self.dependent_on_all = []
        self.dependents_all = []
        self.constraints = od()
        self.indexes = od()
        self.comment = comment
        self.parent_table = parent_table
        self.partition_def = partition_def
        self.rowsecurity = rowsecurity
        self.forcerowsecurity = forcerowsecurity

    def __eq__(self, other):
        equalities = (
            type(self) == type(other),
            self.relationtype == other.relationtype,
            self.name == other.name,
            self.schema == other.schema,
            dict(self.columns) == dict(other.columns),
            self.inputs == other.inputs,
            self.definition == other.definition,
            self.parent_table == other.parent_table,
            self.partition_def == other.partition_def,
            self.rowsecurity == other.rowsecurity,
        )
        return all(equalities)
