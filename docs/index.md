# `migra` is a schema comparison tool for PostgreSQL.

It's a command line tool, and Python library. Find differences in database schemas as easily as running a diff on two text files.

`migra` makes schema changes almost automatic. Management of database migration deployments becomes much easier, faster, and more reliable.

Using `migra` is as simple as this:

    $ migra postgresql:///a postgresql:///b
    alter table "public"."book" add column "author" character varying not null;

    alter table "public"."book" alter column "name" set not null;

To get started, hit the [Quickstart guide](/docs/migra/quickstart).

Migra is 100% open source software. The code is available on [github](https://github.com/djrobstep/migra).

## Features and Limitations

The following features of postgres are supported:

<div markdown="block" class="full-width scroll-on-overflow">

Feature | Supported | Notes/limitations
--- | --- | ---
tables | ✔ |
partitioned tables | ✔ |
constraints | ✔ |
views | ✔ |
functions | ✔ | All languages except C/INTERNAL
indexes | ✔ |
sequences | ✔ | Does not track sequence numbers
schemas | ✔ |
extensions | ✔ |
enums | ✔ |
privileges | ✔ | Not exhaustive. Requires --with-privileges flag
row-level security | ✔ | NEW! Doesn't include role management
triggers | ✔ |
identity columns | ✔ |
generated columns | ✔ |
custom types/domains | ✔ |Basic support (drop-and-create only, no alter) |

</div>

`migra` plays nicely with extensions. Schema contents belonging to extensions will be ignored and left to the extension to manage.

`migra` plays nicely with view/function dependencies, and will drop/create them in the correct order.

## Endorsements

`migra` was [used to manage the schema that powers PyPI](https://twitter.com/dstufft/status/988410901459034113):

> *Migra is cool as hell though, when I was trying to reconcile PyPI with the alembic initial schema I had to download some weird java app I found on some sketchy website to do that :P*

>- [Donald Stufft](https://twitter.com/dstufft), PyPI maintainer

It's [good for local development](https://news.ycombinator.com/item?id=16676481):

> *I can definitely see Migra is more productive when switching around between schemas in development.*

>- [Mike Bayer](https://twitter.com/zzzeek), SQLAlchemy author

<div markdown="block" class="hilighted">

## CI for Databases?

If you like migra, you might also be interested in [CI for databases](/ci-for-databases), a new service I'm building to solve problems with database deployments. [Register your interest](/ci-for-databases).

</div>

## Development

Migra is developed on [github](https://github.com/djrobstep/migra). Contributions are welcome, get involved!

## Philosophy

There was [a good comment on Hacker News](https://news.ycombinator.com/item?id=16679665) discussing how `migra` differs from traditional migration tools.

> *This is awesome!*

> *A lot of people point to migrations as the best way to track changes to a database schema. But there are a lot of problems with them. For example, they involve adding version control on top of another version control system, which can cause a ton of problems. They also don't maintain themselves well. If you leave it alone, running migrations will just take longer and longer over time, even though you don't really get more utility.*

> *I think we need more support from databases themselves to solve this problem.*

> *In the meantime, this is a really good stopgap, because it can theoretically allow you to just have a file with your "ideal schema" for each commit. No need to maintain a separate database migration history too. You can even generate a series of migrations by looking at your git history!"*

> - `blaisio` on Hacker News
