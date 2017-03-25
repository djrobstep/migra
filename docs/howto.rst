HOWTO: Do migrations
====================

Let's discuss a very different way to manage database migrations, that doesn't rely on accumulating historical migration files and version numbers the way that traditional migration tools (rails migrations, alembic etc) do.

Sample app
----------

The techniques discussed below are also demonstrated in a sample flask application available here:

`https://github.com/djrobstep/bookapp <https://github.com/djrobstep/bookapp>`_

Two scenarios
-------------

There's usually two stages to working with databases:

 - Developing locally and figuring out what intended database state you want.
 - Deploying your intended database state to production.

Local development and prototyping
---------------------------------

Usually you'll have an intended state in mind for your database. This is often defined with ORM models or perhaps just a simple setup script.

As your app and database develop and evolve, you'll want to keep your local database in sync with your intended state, without dropping everything and recreating each time. Ideally we would have a single command to do this.

Using ``migra`` and ``sqlbag`` (a library created alongside migra to do things like database connections with less boilerplate), we can achieve that simple command with not too much fuss.

Let's break it down:

.. code-block:: python

    from migra import Migration
    from sqlbag import S, \
        temporary_database, \
        load_sql_from_file

    def setup_intended_db_state(temp_db_url):
        with S(temp_db_url) as s:
            load_sql_from_file(s, 'db_setup.sql')
            # if instead you're using app models
            # with eg the SQLAlchemy ORM, you'd
            # use something like models.create_all
            # here to load your tables

    def main():
        with temporary_database() as temp_db_url:
            setup_intended_db_state(temp_db_url)

            with S(local_db_url) as s0, \ S(temp_db_url) as s1:
                m = Migration(s0, s1)
                m.set_safety(False)
                m.add_all_changes()

                if m.statements:
                    print('The following changes are required:')
                    print(m.sql)
                    if prompt('Apply these changes?'):
                        m.apply()
                else:
                    print('DB already synced, no changes required.')

    if __name__ == '__main__':
        main()


Preparing a production migration
--------------------------------

To determine the changes we need to apply to our production database, we want to load our intended state (much as we did above) and compare that to the actual current production state.

You could do this through a schema dump, or directly through a read-only connection.

The following pg_dump command is useful for generating a suitable schema dump:

.. code-block:: shell

    pg_dump --schema-only --no-owner --no-privileges --column-inserts -f out.dump.sql postgresql://productiondatabase

Generating a (preliminary) migration script then works very similarly:

.. code-block:: python

    from migra import Migration
    from sqlbag import S, \
        temporary_database, \
        load_sql_from_file
    import io

    def setup_current_production_state(temp_db_url):
        with S(temp_db_url) as s:
            load_sql_from_file(s, 'out.dump.sql')

    def setup_intended_db_state(temp_db_url):
        with S(temp_db_url) as s:
            load_sql_from_file(s, 'db_setup.sql')

    def main():
        with \
            temporary_database() as temp_prod, \
            temporary_database() as temp_target:

            setup_current_production_state(temp_prod)
            setup_intended_db_state(temp_target)

            with S(local_db_url) as s0, \ S(temp_db_url) as s1:
                m = Migration(s0, s1)
                m.set_safety(False)
                m.add_all_changes()

                with io.open('pending.sql', 'w') as f:
                    f.write(m.sql)

    if __name__ == '__main__':
        main()


Review time!
------------

Always review the output migra generates before applying it, particularly for production migrations.

Often the migra-generated output will be all you need. But often it won't.

You'll often need to move data around as part of your migration.

Also, there are situations that are impossible for migra to detect, that you'll need to handle manually. For instance, migra can't tell that you've renamed a column rather and simply dropping an old one and adding a new one. So if you want to do a rename, you'll need to do that manually.

There are also performance considerations if your production database is large. Some schema operations can take a long time to apply.

Ideally, test your prepared, edited, and reviewed migration script against real production data before applying it for real.

The best way to do this is to make migration testing part of your application test suite!

Making migrations testable
--------------------------

When developing an app, we'd ideally like to verify that our app will work correctly with the database both before and after the migration is applied. Otherwise, interruptions and downtime could result.

If we define methods to load each of these two conditions, then we can configure our tests to run twice if there is a pending migration to be applied.

Using python's pytest library, this is fairly straightforward.

.. code-block:: python

    from migrations import load_pre_migration, load_post_migration

    with io.open('MIGRATIONS/pending.sql') as f:
        pending_contents = f.read()

    if pending_contents.strip():
        DATABASE_SETUPS_TO_TEST = [
            load_pre_migration,
            load_post_migration
        ]
    else:
        DATABASE_SETUPS_TO_TEST = [
            load_post_migration
        ]

    @pytest.fixture(params=DATABASE_SETUPS_TO_TEST)
    def db(request):
        with temporary_database() as test_db_url:
            setup_method = request.param
            setup_method(test_db_url)
            yield test_db_url

Now, each test that uses the ``db`` fixture gets run twice when necessary.

This makes migrations much more testable and reliable.

Setting up these test conditions will again require the use of a production schema dump that accurately reflects the current database production state. How you make this accessible to your test suite for use in test setup will depend on the operational specifics of your particular app and database setup.
