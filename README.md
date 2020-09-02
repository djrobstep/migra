# migra: Like diff but for Postgres schemas

- ## compare schemas
- ## autogenerate migration scripts
- ## autosync your development database from your application models
- ## make your schema changes testable, robust, and (mostly) automatic

`migra` is a schema diff tool for PostgreSQL, written in Python. Use it in your python scripts, or from the command line like this:

    $ migra postgresql:///a postgresql:///b
    alter table "public"."products" add column newcolumn text;

    alter table "public"."products" add constraint "x" CHECK ((price > (0)::numeric));

`migra` magically figures out all the statements required to get from A to B.

Most features of PostgreSQL are supported.

**Migra supports PostgreSQL >= 9 only.** Known issues exist with earlier versions. More recent versions are more comprehensively tested. Development resources are limited, and feature support rather than backwards compatibility is prioritised.

## THE DOCS

Documentation is at [databaseci.com/docs/migra](https://databaseci.com/docs/migra).

## Folks, schemas are good

Schema migrations are without doubt the most cumbersome and annoying part of working with SQL databases. So much so that some people think that schemas themselves are bad!

But schemas are actually good. Enforcing data consistency and structure is a good thing. It’s the migration tooling that is bad, because it’s harder to use than it should be. ``migra`` is an attempt to change that, and make migrations easy, safe, and reliable instead of something to dread.

## Contributing

Contributing is easy. [Jump into the issues](https://github.com/djrobstep/migra/issues), find a feature or fix you'd like to work on, and get involved. Or create a new issue and suggest something completely different. If you're unsure about any aspect of the process, just ask.

## Credits

- [djrobstep](https://github.com/djrobstep): initial development, maintenance
- [alvarogzp](https://github.com/alvarogzp): privileges support
- [seblucas](https://github.com/seblucas): docker improvements
- [MOZGIII](https://github.com/MOZGIII): docker support
- [mshahbazi](https://github.com/mshahbazi): misc fixes and enhancements
