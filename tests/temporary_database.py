import tempfile
import os
import random
import string

from contextlib import contextmanager
from sqlbag import create_database, drop_database


def temporary_name(prefix="sqlbag_tmp_"):
    random_letters = [random.choice(string.ascii_lowercase) for _ in range(10)]
    rnd = "".join(random_letters)
    tempname = prefix + rnd
    return tempname


@contextmanager
def temporary_database(dialect="postgresql", user_pass="postgres", do_not_delete=False, host=None):
    """
    Args:
        dialect(str): Type of database to create (either 'postgresql', 'mysql', or 'sqlite').
        do_not_delete: Do not delete the database as this method usually would.

    Creates a temporary database for the duration of the context manager scope. Cleans it up when finished unless do_not_delete is specified.

    PostgreSQL, MySQL/MariaDB, and SQLite are supported. This method's mysql creation code uses the pymysql driver, so make sure you have that installed.
    """

    host = host or ""

    if dialect == "sqlite":
        tmp = tempfile.NamedTemporaryFile(delete=False)

        try:
            url = "sqlite:///" + tmp.name
            yield url

        finally:
            if not do_not_delete:
                os.remove(tmp.name)

    else:
        tempname = temporary_name()

        url = "{}://{}@{}/{}".format(dialect, user_pass, host, tempname)

        if url.startswith("mysql:"):
            url = url.replace("mysql:", "mysql+pymysql:", 1)

        try:
            create_database(url)
            yield url
        finally:
            if not do_not_delete:
                drop_database(url)
