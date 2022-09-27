from __future__ import unicode_literals

import io
from difflib import ndiff as difflib_diff

import pytest

# import yaml
from pytest import raises
from schemainspect import get_inspector
from sqlbag import S, load_sql_from_file, temporary_database

from migra import Migration, Statements, UnsafeMigrationException
from migra.command import parse_args, run


def textdiff(a, b):
    cd = difflib_diff(a.splitlines(), b.splitlines())
    return "\n" + "\n".join(cd) + "\n"


SQL = """select 1;

select 2;

"""
DROP = "drop table x;"


def test_statements():
    s1 = Statements(["select 1;"])
    s2 = Statements(["select 2;"])
    s3 = s1 + s2
    assert type(s1) == type(s2) == type(s3)
    s3 = s3 + Statements([DROP])
    with raises(UnsafeMigrationException):
        assert s3.sql == SQL
    s3.safe = False
    SQL_WITH_DROP = SQL + DROP + "\n\n"
    assert s3.sql == SQL_WITH_DROP


def outs():
    return io.StringIO(), io.StringIO()


def test_singleschema():
    for FIXTURE_NAME in ["singleschema"]:
        do_fixture_test(FIXTURE_NAME, schema="goodschema")


def test_excludeschema():
    for FIXTURE_NAME in ["excludeschema"]:
        do_fixture_test(FIXTURE_NAME, exclude_schema="excludedschema")


def test_singleschema_ext():
    for FIXTURE_NAME in ["singleschema_ext"]:
        do_fixture_test(FIXTURE_NAME, create_extensions_only=True)


def test_extversions():
    for FIXTURE_NAME in ["extversions"]:
        do_fixture_test(FIXTURE_NAME, ignore_extension_versions=False)


fixtures = """\
everything
comments
collations
identitycols
partitioning
privileges
enumdefaults
enumdeps
seq
inherit
inherit2
triggers
triggers2
triggers3
dependencies
dependencies2
dependencies3
dependencies4
constraints
generated
""".split()


@pytest.mark.parametrize("fixture_name", fixtures)
def test_fixtures(fixture_name):
    do_fixture_test(fixture_name, with_privileges=True)


schemainspect_test_role = "schemainspect_test_role"


def create_role(s, rolename):
    role = s.execute(
        """
SELECT 1 FROM pg_roles WHERE rolname=:rolename
    """,
        dict(rolename=rolename),
    )

    role_exists = bool(list(role))

    if not role_exists:
        s.execute(
            f"""
            create role {rolename};
        """
        )


def test_rls():
    for FIXTURE_NAME in ["rls", "rls2"]:
        do_fixture_test(FIXTURE_NAME, with_privileges=True)


check_expected = True


def do_fixture_test(
    fixture_name,
    schema=None,
    create_extensions_only=False,
    ignore_extension_versions=True,
    with_privileges=False,
    exclude_schema=None,
):
    flags = ["--unsafe"]
    if schema:
        flags += ["--schema", schema]
    if exclude_schema:
        flags += ["--exclude_schema", exclude_schema]
    if create_extensions_only:
        flags += ["--create-extensions-only"]
    if ignore_extension_versions:
        flags += ["--ignore-extension-versions"]
    if with_privileges:
        flags += ["--with-privileges"]
    fixture_path = "tests/FIXTURES/{}/".format(fixture_name)
    EXPECTED = io.open(fixture_path + "expected.sql").read().strip()
    with temporary_database(host="localhost") as d0, temporary_database(
        host="localhost"
    ) as d1:
        with S(d0) as s0:
            create_role(s0, schemainspect_test_role)
        with S(d0) as s0, S(d1) as s1:
            load_sql_from_file(s0, fixture_path + "a.sql")
            load_sql_from_file(s1, fixture_path + "b.sql")

        args = parse_args([d0, d1])
        assert not args.unsafe
        assert args.schema is None

        out, err = outs()
        assert run(args, out=out, err=err) == 3
        assert out.getvalue() == ""

        DESTRUCTIVE = "-- ERROR: destructive statements generated. Use the --unsafe flag to suppress this error.\n"

        assert err.getvalue() == DESTRUCTIVE

        args = parse_args(flags + [d0, d1])
        assert args.unsafe
        assert args.schema == schema
        out, err = outs()
        assert run(args, out=out, err=err) == 2
        assert err.getvalue() == ""

        output = out.getvalue().strip()
        if check_expected:
            assert output == EXPECTED

        ADDITIONS = io.open(fixture_path + "additions.sql").read().strip()
        EXPECTED2 = io.open(fixture_path + "expected2.sql").read().strip()

        with S(d0) as s0, S(d1) as s1:
            m = Migration(
                s0,
                s1,
                schema=schema,
                exclude_schema=exclude_schema,
                ignore_extension_versions=ignore_extension_versions,
            )
            m.inspect_from()
            m.inspect_target()
            with raises(AttributeError):
                m.changes.nonexist
            m.set_safety(False)
            if ADDITIONS:
                m.add_sql(ADDITIONS)
            m.apply()

            if create_extensions_only:
                m.add_extension_changes(drops=False)
            else:
                m.add_all_changes(privileges=with_privileges)

            expected = EXPECTED2 if ADDITIONS else EXPECTED

            if check_expected:
                assert m.sql.strip() == expected  # sql generated OK

            m.apply()
            # check for changes again and make sure none are pending
            if create_extensions_only:
                m.add_extension_changes(drops=False)
                assert (
                    m.changes.i_from.extensions.items()
                    >= m.changes.i_target.extensions.items()
                )
            else:
                m.add_all_changes(privileges=with_privileges)

                # y0 = yaml.safe_dump(m.changes.i_from._as_dicts())
                # y1 = yaml.safe_dump(m.changes.i_target._as_dicts())

                # print(textdiff(y0, y1))
                # print(m.statements)

                assert m.changes.i_from == m.changes.i_target
            assert not m.statements  # no further statements to apply
            assert m.sql == ""
            out, err = outs()

        assert run(args, out=out, err=err) == 0
        # test alternative parameters
        with S(d0) as s0, S(d1) as s1:
            m = Migration(
                get_inspector(s0), get_inspector(s1), ignore_extension_versions=True
            )
        # test empty
        m = Migration(None, None)
        m.add_all_changes(privileges=with_privileges)
        with raises(AttributeError):
            m.s_from
        with raises(AttributeError):
            m.s_target
        args = parse_args(flags + ["EMPTY", "EMPTY"])
        out, err = outs()
        assert run(args, out=out, err=err) == 0
