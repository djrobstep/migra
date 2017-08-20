# `migra` is a schema comparison tool for PostgreSQL.

It's a command line tool, and Python library. Find differences in database schemas as easily as running a diff on two text files.

Migra makes schema changes almost automatic. Management of database migration deployments becomes much easier, faster, and more reliable.

Using `migra` is as simple as this:

    $ migra postgresql:///a postgresql:///b
    alter table "public"."book" add column "author" character varying not null;

    alter table "public"."book" alter column "name" set not null;

To get started, hit the [Quickstart guide](/quickstart).
