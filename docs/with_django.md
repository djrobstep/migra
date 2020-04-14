# Using `migra` with `django`

Incorporating non-default parts with django can be a little awkward. However, with some config tweaks you can use migra alongside django's default migration setup.

Below is a sample script that implements a hybrid sync command: It'll run any defined django migrations as normal, but allows you to specify a list of installed django "`apps`" that you can manage with `migra` instead.

## Deploying

The general advice elsewhere in the docs regarding the creation of migration scripts for your production environment still applies as normal.

A script to generate production scripts would like quite similar the provided local-sync script below, except that the comparison would be `production -> target` instead of `current local -> target`.

## Testing

Initialize your database for tests as follows:

- `migrate` any django migrations in use
- sync your prepared script of changes

## A sample local syncing script
`migra`'s built-in apps come with some migrations, so you don't want to disable the built-in migrations entirely.

    :::python
    import manage
    import os
    import sys
    from mysite import settings
    from django.core import management
    import django
    from sqlbag import temporary_database, S
    from migra import Migration
    from contextlib import contextmanager

    # Point to your settings.
    os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"

    # The "polls" app (as per the django official tutorial)
    # is set here to be managed with migra instead
    MANAGE_WITH_MIGRA = ["polls"]

    # To disable migrations on a django app, you have to
    # set the MIGRATION_MODULES config with None for each
    # disabled "app"
    class DisableMigrations(object):
        def __contains__(self, item):
            return item in MANAGE_WITH_MIGRA

        def __getitem__(self, item):
            return None

    # Compare two schemas, prompt to run a sync if necessary
    def _sync_with_prompt(db_url_current, db_url_target):
        with S(db_url_current) as s0, S(db_url_target) as s1:
            m = Migration(s0, s1)
            m.set_safety(False)
            m.add_all_changes()

            if m.statements:
                print("THE FOLLOWING CHANGES ARE PENDING:", end="\n\n")
                print(m.sql)
                print()
                if input('Type "yes" to apply these changes: ') == "yes":
                    print("Applying...")
                    m.apply()
                else:
                    print("Not applying.")
            else:
                print("Already synced.")


    # Create a temporary database for loading our
    # "target" schema into
    @contextmanager
    def tmptarget():
        with temporary_database() as tdb:
            settings.DATABASES["tmp_target"] = {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": tdb.split("/")[-1],
            }
            django.setup()
            yield tdb


    def syncdb():
        # Disable django migrations if we're using migra instead
        settings.MIGRATION_MODULES = DisableMigrations()


        with tmptarget() as tdb:
            management.call_command("migrate")

            management.call_command(
                "migrate",
                "--run-syncdb",
                "--database=tmp_target",
                verbosity=0,
                interactive=False,
            )
            real_db_name = settings.DATABASES["default"]["NAME"]
            _sync_with_prompt(f"postgresql:///{real_db_name}", tdb)


    if __name__ == "__main__":
        syncdb()


# Can it be done better?

How well does `migra` work for you with django? Let us know via email, github issues, twitter, whatever.