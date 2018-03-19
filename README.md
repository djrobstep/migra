# migra: PostgreSQL migrations made almost painless

`migra` is a schema diff tool for PostgreSQL. Use it to compare database schemas or autogenerate migration scripts. Use it in your python scripts, or from the command line like this:

    $ migra postgresql:///a postgresql:///b
    alter table "public"."products" add column newcolumn text;

    alter table "public"."products" add constraint "x" CHECK ((price > (0)::numeric));

`migra` magically figures out all the statements required to get from A to B.

You can also detect changes for a single specific schema only with `--schema myschema`.

## Already use `migra`? [Let us know how you're using it and what features would make it more useful](https://github.com/djrobstep/migra/issues/25).

## Folks, schemas are good

Schema migrations are without doubt the most cumbersome and annoying part of working with SQL databases. So much so that some people think that schemas themselves are bad!

But schemas are actually good. Enforcing data consistency and structure is a good thing. It’s the migration tooling that is bad, because it’s harder to use than it should be. ``migra`` is an attempt to change that, and make migrations easy, safe, and reliable instead of something to dread.

**Migra supports PostgreSQL >= 9.4.** Known issues exist with earlier versions.

## Full documentation

Documentation is at [migra.djrobstep.com](https://migra.djrobstep.com).

## How it Works

Think of `migra` as a diff tool for schemas. Suppose database A and database B have similar but slightly different schemas. `migra` will detect the differences and output the SQL needed to transform A to B.

This includes changes to tables, views, functions, indexes, constraints, enums, sequences, and installed extensions.

You can also use `migra` as a library to build your own migration scripts, tools, and custom migration flows.

With migra, a typical database migration is a simple three step process.

1. Autogenerate:

        $ migra --unsafe postgresql:///a postgresql:///b > migration_script.sql

2. Review (and tweak if necessary).

        # If you need to move data about during your script, you can add those changes to your script.

3. Apply:

        $ psql a --single-transaction -f migration_script.sql

Migration complete!

## IMPORTANT: Practice safe migrations

**Migrations can never be fully automatic**. As noted above **ALWAYS REVIEW MIGRATION SCRIPTS CAREFULLY, ESPECIALLY WHEN DROPPING TABLES IS INVOLVED**.

Migra manages schema changes **but not your data**. If you need to move data around, as part of a migration, you'll need to handle that by editing the script or doing it separately before/after the schema changes.

Best practice is to run your migrations against a copy of your production database first. This helps verify correctness and spot any performance issues before they cause interruptions and downtime on your production database.

`migra` will deliberately throw an error if any generated statements feature the word "drop". This safety feature is by no means idiot-proof, but might prevent a few obvious blunders.

If you want to generate "drop ..." statements, you need to use the `--unsafe` flag if using the command, or if using the python package directly, `set_safety(` to false on your `Migration` object.

## Python Code

Here's how the migra command is implemented under the hood (with a few irrelevant lines removed).

As you can see, it's pretty simple (`S` here is a context manager that creates a database session from a database URL).

    from migra import Migration
    from sqlbag import S

    with S(args.dburl_from) as s0, S(args.dburl_target) as s1:
        m = Migration(s0, s1)

        if args.unsafe:
            m.set_safety(False)

        m.add_all_changes()
        print(m.sql)

Here the code just opens connections to both databases for the Migration object to analyse. `m.add_all_changes()` generates the SQL statements for the changes required, and adds to the migration object's list of pending changes. The necessary SQL is now available as a property.

## Features and Limitations

`migra` plays nicely with extensions. Schema contents belonging to extensions will be ignored and left to the extension to manage.

**New:** `migra` now plays nicely with view dependencies too, and will drop/create them in the correct order.

Only SQL/PLPGSQL functions are confirmed to work so far. `migra` ignores functions that use other languages.

## Installation

Assuming you have [pip](https://pip.pypa.io), all you need to do is install as follows:

    $ pip install migra

If you don't have psycopg2-binary (the PostgreSQL driver) installed yet, you can install this at the same time with:

    $ pip install migra[pg]

## Contributing

Contributing is easy. [Jump into the issues](https://github.com/djrobstep/migra/issues), find a feature or fix you'd like to work on, and get involved. Or create a new issue and suggest something completely different. Beginner-friendly issues are tagged "good first issue", and if you're unsure about any aspect of the process, just ask.
