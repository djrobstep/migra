from __future__ import unicode_literals

import io

from pytest import raises

from migra import Statements, UnsafeMigrationException, Migration
from migra.command import run
from sqlbag import temporary_database, S, load_sql_from_file
from schemainspect import get_inspector
from migra.command import parse_args

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


def outs():
    return io.StringIO(), io.StringIO()


def test_with_fixtures():
    for FIXTURE_NAME in ['dependencies', 'everything']:
        do_fixture_test(FIXTURE_NAME)
    for FIXTURE_NAME in ['singleschema']:
        do_fixture_test(FIXTURE_NAME, schema='goodschema')
    for FIXTURE_NAME in ['singleschema_ext']:
        do_fixture_test(FIXTURE_NAME, create_extensions_only=True)
    for FIXTURE_NAME in ['privileges']:
        do_fixture_test(FIXTURE_NAME, with_privileges=True)


def do_fixture_test(fixture_name, schema=None, create_extensions_only=False, with_privileges=False):
    flags = ['--unsafe']
    if schema:
        flags += ['--schema', schema]
    if create_extensions_only:
        flags += ['--create-extensions-only']
    if with_privileges:
        flags += ['--with-privileges']
    fixture_path = 'tests/FIXTURES/{}/'.format(fixture_name)
    EXPECTED = io.open(fixture_path + 'expected.sql').read().strip()
    with temporary_database() as d0, temporary_database() as d1:
        with S(d0) as s0, S(d1) as s1:
            load_sql_from_file(s0, fixture_path + 'a.sql')
            load_sql_from_file(s1, fixture_path + 'b.sql')
        args = parse_args([d0, d1])
        assert not args.unsafe
        assert args.schema is None
        out, err = outs()
        assert run(args, out=out, err=err) == 3
        assert out.getvalue() == ''
        assert err.getvalue() == '-- ERROR: destructive statements generated. Use the --unsafe flag to suppress this error.\n'
        args = parse_args(flags + [d0, d1])
        assert args.unsafe
        assert args.schema == schema
        out, err = outs()
        assert run(args, out=out, err=err) == 2
        assert err.getvalue() == ''
        assert out.getvalue().strip() == EXPECTED
        ADDITIONS = io.open(fixture_path + 'additions.sql').read().strip()
        EXPECTED2 = io.open(fixture_path + 'expected2.sql').read().strip()
        if ADDITIONS:
            with S(d0) as s0, S(d1) as s1:
                m = Migration(s0, s1)
                m.inspect_from()
                m.inspect_target()
                with raises(AttributeError):
                    m.changes.nonexist
                m.set_safety(False)
                m.add_sql(ADDITIONS)
                m.apply()
                m.add_all_changes(privileges=with_privileges)
                assert m.sql.strip() == EXPECTED2  # sql generated OK
                m.apply()
                # check for changes again and make sure none are pending
                m.add_all_changes(privileges=with_privileges)
                assert m.changes.i_from == m.changes.i_target
                assert not m.statements  # no further statements to apply
                assert m.sql == ''
                out, err = outs()
                assert run(args, out=out, err=err) == 0
        # test alternative parameters
        with S(d0) as s0, S(d1) as s1:
            m = Migration(get_inspector(s0), get_inspector(s1))
        # test empty
        m = Migration(None, None)
        m.add_all_changes(privileges=with_privileges)
        with raises(AttributeError):
            m.s_from
        with raises(AttributeError):
            m.s_target
        args = parse_args(flags + ['EMPTY', 'EMPTY'])
        out, err = outs()
        assert run(args, out=out, err=err) == 0
