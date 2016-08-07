from __future__ import unicode_literals

import io

from pytest import raises

from migra import Statements, UnsafeMigrationException, Migration
from migra.command import run
from sqlbag import temporary_database, S, load_sql_from_file

from migra.command import parse_args

SQL = """select 1;

select 2;

"""

DROP = 'drop table x;'

B = 'alter table "public"."products" add column "newcolumn" text;\n\n'
A = 'alter table "public"."products" drop column "oldcolumn";\n\n'

EXPECTED = io.open('tests/FIXTURES/expected.sql').read().strip()
EXPECTED2 = EXPECTED.replace(A + B, '')


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


def outs():
    return io.StringIO(), io.StringIO()


def test_all():
    with temporary_database() as d0, temporary_database() as d1:
        with S(d0) as s0, S(d1) as s1:
            load_sql_from_file(s0, 'tests/FIXTURES/a.sql')
            load_sql_from_file(s1, 'tests/FIXTURES/b.sql')

        args = parse_args([d0, d1])
        assert not args.unsafe

        out, err = outs()
        assert run(args, out=out, err=err) == 3

        assert out.getvalue() == ''
        assert err.getvalue() == '-- ERROR: destructive statements generated. Use the --unsafe flag to suppress this error.\n'

        args = parse_args(['--unsafe', d0, d1])
        assert args.unsafe

        out, err = outs()
        assert run(args, out=out, err=err) == 2
        assert err.getvalue() == ''
        assert out.getvalue().strip() == EXPECTED

        with S(d0) as s0, S(d1) as s1:
            m = Migration(s0, s1)

            with raises(AttributeError):
                m.changes.nonexist

            m.set_safety(False)

            m.add_sql('alter table products rename column oldcolumn to newcolumn;')
            m.apply()
            m.add_all_changes()
            assert m.sql.strip() == EXPECTED2  # sql generated OK
            m.apply()

            # check for changes again and make sure none are pending
            m.add_all_changes()
            assert m.changes.i_from == m.changes.i_target
            assert not m.statements  # no further statements to apply

        out, err = outs()
        assert run(args, out=out, err=err) == 0
