### Installation

`migra` is written in Python so you need to install it with `pip`, the Python Package Manager (don't worry, you don't need to know or use any Python to use the `migra` command).

1. Make sure you have [pip](https://pip.pypa.io/en/stable/installing/) properly installed.

2. Run:

        :::bash
        $ pip install migra[pg]

    This will install the latest version of migra from PyPI (the global Python Package Index), along with psycopg2, the python PostgreSQL driver.

Alternatively, if you don't want to install Python, you can run it from a 
self-contained Docker image by first running:

```shell script
docker pull djrobstep/migra
```

then creating a short alias to it with:

```shell script
alias migra="docker run djrobstep/migra migra"
```

3. Confirm migra is installed by running `migra --help`. The output should begin like this:

        usage: migra [-h] [--unsafe] dburl_from dburl_target

## Comparing two database schemas

To compare two database schemas:

    $ migra <url_of_database_A> <url_of_database_B>

For example, we have two databases, named "alpha" and "beta". We can compare them using this command:

    $ migra postgresql:///alpha postgresql:///beta

Migra will then generate whatever SQL is required to change the schema of database `alpha` to match database `beta`.

If the two database schemas match exactly, you'll get empty output, because no changes are required. This functions like the well-known [diff command](https://en.wikipedia.org/wiki/Diff_utility), which also returns empty output when comparing two identical files.

### Warning

Don't blindly copy-and-paste the output of the `migra` command.

`migra` features a safeguard against generation of dangerous statements. If the command generates a drop statement, `migra` will exit with an error. If you're sure you want the drop statement(s), you can turn off this safeguard behaviour with the `--unsafe` flag:

    migra --unsafe postgresql:///alpha postgresql:///beta

## Making changes to database schemas

### Suggestion

If you're making changes to a serious production database, use a copy of it for these steps instead so you're not changing your production environment until you intend to.

You can make a schema-only dump of your PostgreSQL database with the following command:

    pg_dump --no-owner --no-privileges --no-acl --schema-only name_of_database -f schema.dump.sql

### Steps

1. Get the connection string of the database you want to make changes to. `migra` needs to connect to this database so it can analyse the database's schema.

2. Prepare a second PostgreSQL database. This database needs to have the new/desired/target schema. You might create a temporary database and set it up for this purpose.

3. Generate a migration script using the following command (substituting your own connection strings):

    ```
    $ migra --unsafe postgresql:///existing postgresql:///database_with_new_schema > migration_script.sql
    ```

4. Carefully review the migration script in `migration_script.sql`

    Consider in particular:

    - The generated script may result in data loss from your database when you apply this script. Consider if you intend for this to happen or if you need to add statements to copy data out of the relevant tables/columns before you drop them forever.

    - Some migration operations can take a long time and cause interruptions and downtime, particularly when involving tables containing large amounts of data. [More on this here](/link).

5. Apply `migration_script.sql` to your production database with a command similar to the following (again substituting your own connection string).

    ```psql postgresql://production -1 -f migration_script.sql
    ```
