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

## Usage

usage: migra [-h] [--unsafe] [--schema SCHEMA] [--exclude_schema EXCLUDE_SCHEMA] [--create-extensions-only] [--ignore-extension-versions] [--with-privileges] [--force-utf8]
             dburl_from dburl_target

### Command Line

```bash
pip install migra-maintained
migra db_url_from db_url_target
```

### Python
```bash
pip install migra-maintained
```

```python
# Use migra_maintained instead of migra-maintained
from migra_maintained import Migration, Statements
from migra_maintained.command import parse_args, run
```

### Docker

```bash
docker pull philipandrewweedewang/migra:latest
docker run --rm philipandrewweedewang/migra:latest \
  postgresql://user:password@host1:port/dbname1 \
  postgresql://user:password@host2:port/dbname2

```

**Migra supports PostgreSQL >= 9 only.** Known issues exist with earlier versions. More recent versions are more comprehensively tested. Development resources are limited, and feature support rather than backwards compatibility is prioritised.

## Contributing

Contributing is easy. [Jump into the issues](https://github.com/djrobstep/migra/issues), find a feature or fix you'd like to work on, and get involved. Or create a new issue and suggest something completely different. If you're unsure about any aspect of the process, just ask.

See the [Contribution Guide](CONTRIBUTION_GUIDE.md) for more details

## Roadmap

The dream would be to develop this to a point where we no longer need to manually write migrations, just use version control to manage the schema of a database. 

## Features


### View ownership

- [ ] [view owner and grants](https://github.com/djrobstep/migra/issues/160#issuecomment-1702983833)
- [ ] [security invoker on views](https://github.com/djrobstep/migra/issues/234)
- [ ] [materialized views](https://github.com/djrobstep/migra/issues/194)
- [ ] doesn't recreate views when altering column type

### RLS policies

- [ ] [alter policy statements](https://github.com/djrobstep/schemainspect/blob/master/schemainspect/pg/obj.py#L228)
- [x] [column privileges](https://github.com/djrobstep/schemainspect/pull/67)

### Other entities

- [x] [Fix enum dependencies on functions](https://github.com/djrobstep/migra/issues/243)
- [x] [Basic comments support](https://github.com/djrobstep/migra/issues/69)
- [ ] Support for comments with dependencies
- [ ] schema privileges are not tracked because each schema is diffed separately
- [ ] [partitions are not tracked](https://github.com/djrobstep/migra/issues/186)
- [ ] [`alter publication ... add table ...`](https://github.com/supabase/cli/issues/883)
- [ ] [create domain statements are ignored](https://github.com/supabase/cli/issues/2137)
- [ ] [grant statements are duplicated from default privileges](https://github.com/supabase/cli/issues/1864)

### Robustness

- [ ] Proper pg10 - pg17 support 
    - (Currently runs test on 16/17 for `philipwee/migra` and 10-15 for `philipwee/schemainspect` because of breaking internal postgres changes in `pg_get_viewdef` from 15-16 (and possibly `pg_get_functiondef` and `pg_get_expr`))
- [ ] Proper documentation website

The current aim is to fix all of the [main caveats](https://supabase.com/docs/guides/local-development/declarative-database-schemas#known-caveats) listed in the supabase docs


Contributions are extremely welcome, and there should be enough info in the [Contribution Guide](CONTRIBUTION_GUIDE.md) to get you started!


## Reason for forking

This repo was forked because the original `migra` package had several limitations but has been unmainted for about 4 years.

While there are alternatives such as stripe's [pg-schema-diff](https://github.com/stripe/pg-schema-diff), somehow this package still remains as one of the robust ways of diffing two db schemas because it handles dependencies between objects pretty well



## Folks, schemas are good

Schema migrations are without doubt the most cumbersome and annoying part of working with SQL databases. So much so that some people think that schemas themselves are bad!

But schemas are actually good. Enforcing data consistency and structure is a good thing. It’s the migration tooling that is bad, because it’s harder to use than it should be. ``migra`` is an attempt to change that, and make migrations easy, safe, and reliable instead of something to dread.

## Credits

A huge shoutout to [djrobstep](https://github.com/djrobstep) for the initial development, maintenance of the `migra` package