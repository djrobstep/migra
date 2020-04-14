# Development Usage

Migra is handy for speeding up database-related development and testing tasks.

### Auto-syncing dev database to application code

When developing applications that work with a database, you'll inevitably have some kind of "target" schema in mind that you want the database to have.  

This is often defined with database model classes (such as used by Django/Rails), or perhaps with a setup script written in raw SQL.

When developing your application, you'll generally have a local version of this database running for use while developing, tweaking and debugging your application.

The challenge is to keep this database in sync with your "target" schema as you tinker and continually modify the target to suit your app.

This sample script shows how you might use migra to sync up your dev database almost automatically:

    :::python
    def sync():
        from sqlbag import S, temporary_database as temporary_db

        DB_URL = 'postgresql:///name_of_local_dev_database'

        with temporary_db() as TEMP_DB_URL:
            load_from_app(TEMP_DB_URL)

            with S(DB_URL) as s_current, S(TEMP_DB_URL) as s_target:
                m = Migration(s_current, s_target)
                m.set_safety(False)
                m.add_all_changes()

                if m.statements:
                    print('THE FOLLOWING CHANGES ARE PENDING:', end='\n\n')
                    print(m.sql)
                    print()
                    if input('Apply these changes?') == 'yes':
                        print('Applying...')
                        m.apply()
                    else:
                        print('Not applying.')
                else:
                    print('Already synced.')


### Creating customized tasks and scripts

Every project is slightly different, so Migra doesn't try and solve every migration workflow problem you could possibly have. Instead, migra tries to make it as easy as possible to write scripts to solve your own migration problems.

Most of migra's functionality is available through the Migration object. Pass in two database sessions and migra will compare the two against each other. This basic unit of functionality should be fairly easily adaptable to your particular requirements.

### Setting up tests

You can use migra to test the correctness of three things:

- The correctness of your code pre-migration.
- The correctness of your code post-migration.
- The correctness of your migration scripts.

### Testing *before* and *after* database versions

With the right testing framework and fixture setup code, you can configure your tests to run twice, against both the pre and post migration versions of your database.

Here's how to do that with python's pytest. Suppose you are using migra to generate a file called `pending.sql` that contains any pending migrations. You could then add something like this to your `conftest.py` file:

    import os.path
    from sqlbag import S, temporary_database as temporary_db

    def load_pre_migration(dburl):
        with S(dburl) as s:
            load_sql_from_file(s, 'MIGRATIONS/production.dump.sql')


    def load_post_migration(dburl):
        with S(dburl) as s:
            load_sql_from_file(s, 'MIGRATIONS/production.dump.sql')

        with S(dburl) as s:
            load_sql_from_file(s, 'MIGRATIONS/pending.sql')

    pending = os.path.exists('MIGRATIONS/pending.sql')

    if pending:
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
        with temporary_db() as test_db_url:
            setup_method = request.param
            setup_method(test_db_url)
            yield test_db_url

### Testing against real data

You can make your testing more comprehensive by testing against not just the empty schema structure of your production database, but a copy populated with real (preferably anonymised) application data.

If your production database is large, you really should be testing your migration against a copy of similar size, in order to detect any performance problems that could result from slow-running migration scripts.
