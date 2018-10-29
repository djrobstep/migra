from __future__ import print_function, unicode_literals

import argparse
import sys
from contextlib import contextmanager

from sqlbag import S

from .migra import Migration
from .statements import UnsafeMigrationException


@contextmanager
def arg_context(x):
    if x == "EMPTY":
        yield None

    else:
        with S(x) as s:
            yield s


def parse_args(args):
    parser = argparse.ArgumentParser(description="Generate a database migration.")
    parser.add_argument(
        "--unsafe",
        dest="unsafe",
        action="store_true",
        help="Prevent migra from erroring upon generation of drop statements.",
    )
    parser.add_argument(
        "--schema",
        dest="schema",
        default=None,
        help="Restrict output to statements for a particular schema",
    )
    parser.add_argument(
        "--create-extensions-only",
        dest="create_extensions_only",
        action="store_true",
        default=False,
        help='Only output "create extension..." statements, nothing else.',
    )
    parser.add_argument(
        "--with-privileges",
        dest="with_privileges",
        action="store_true",
        default=False,
        help="Also output privilege differences (ie. grant/revoke statements)",
    )
    parser.add_argument(
        "--force-utf8",
        dest="force_utf8",
        action="store_true",
        default=False,
        help="Force UTF-8 encoding for output",
    )
    parser.add_argument("dburl_from", help="The database you want to migrate.")
    parser.add_argument(
        "dburl_target", help="The database you want to use as the target."
    )
    return parser.parse_args(args)


def run(args, out=None, err=None):
    schema = args.schema
    if not out:
        out = sys.stdout  # pragma: no cover
    if not err:
        err = sys.stderr  # pragma: no cover
    with arg_context(args.dburl_from) as ac0, arg_context(args.dburl_target) as ac1:
        m = Migration(ac0, ac1, schema=schema)
        if args.unsafe:
            m.set_safety(False)
        if args.create_extensions_only:
            m.add_extension_changes(drops=False)
        else:
            m.add_all_changes(privileges=args.with_privileges)
        try:
            if m.statements:
                if args.force_utf8:
                    print(m.sql.encode("utf8"), file=out)
                else:
                    print(m.sql, file=out)
        except UnsafeMigrationException:
            print(
                "-- ERROR: destructive statements generated. Use the --unsafe flag to suppress this error.",
                file=err,
            )
            return 3

        if not m.statements:
            return 0

        else:
            return 2


def do_command():  # pragma: no cover
    args = parse_args(sys.argv[1:])
    status = run(args)
    sys.exit(status)
