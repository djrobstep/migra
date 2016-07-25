from __future__ import unicode_literals

from sqlbag import S
import argparse
import sys

from .migra import Migration


def do_command():
    parser = argparse.ArgumentParser(
        description='Generate a database migration.')

    parser.add_argument('--unsafe', dest='unsafe', action='store_true')

    parser.add_argument('dburl_from',
                        help='The database you want to migrate.')

    parser.add_argument('dburl_target',
                        help='The database you want to use as the target.')

    args = parser.parse_args()

    with S(args.dburl_from) as s0, S(args.dburl_target) as s1:
        m = Migration(s0, s1)

        if args.unsafe:
            m.set_safety(False)
        m.add_all_changes()
        print(m.sql)
        if not m.statements:
            sys.exit(0)
        else:
            sys.exit(1)
