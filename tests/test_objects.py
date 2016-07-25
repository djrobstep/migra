from __future__ import unicode_literals

from pytest import raises

from migra import Statements, UnsafeMigrationException, Migration
from sqlbag import temporary_database, S, load_sql_from_file


SQL = """select 1;

select 2;

"""

DROP = 'drop table x;'


def test_statements():
    s1 = Statements(['select 1;'])
    s2 = Statements(['select 2;'])
    s3 = s1 + s2
    assert type(s1) == type(s2) == type(s3)

    s3 = s3 + Statements([DROP])

    with raises(UnsafeMigrationException):
        assert s3.sql == SQL

    s3.safe = False
    SQL_WITH_DROP = SQL + DROP + '\n\n'
    assert s3.sql == SQL_WITH_DROP


def test_changes():
    with temporary_database() as d0, temporary_database() as d1:
        with S(d0) as s0, S(d1) as s1:
            load_sql_from_file(s0, 'tests/FIXTURES/a.sql')
            load_sql_from_file(s1, 'tests/FIXTURES/b.sql')

        with S(d0) as s0, S(d1) as s1:
            m = Migration(s0, s1)

            m.set_safety(False)
            m.add_sql('alter table products rename column oldcolumn to newcolumn;')
            m.apply()
            m.add_all_changes()
            m.sql  # sql generated OK
            m.apply()
            m.add_all_changes()
            assert not m.statements
