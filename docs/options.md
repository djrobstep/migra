# Options

The command line version of migra includes a number of options for getting the diff output you desire. If using the API, similarly named options are available on the Migration object.

## `--unsafe`

Migra will throw an exception if `drop...` statements are generated, as a precaution. Adding this flag will disable the safety feature and happily generate the drop statements. Remember, always review generated statements before running them!

## `--schema [SCHEMA_NAME]`

Specify a single schema to diff.

## `--exclude_schema [SCHEMA_NAME]`

Specify a single schema to exclude, including all other schemas in the diff.

## `--create-extensions-only`

Only output create extension statements, nothing else. This is useful when you have extensions as part of a setup script for a single schema: Those extensions need to be installed, but extensions are usually not installed in a custom schema.

You'd generate a setup script in two steps:

- Generate the necessary create extension if not exists... statements.
- Generate the schema changes with --schema-only.

Then combine the output of 1 and 2 into a single database sync script.

## `--with-privileges`

This tells migra to spit out permission-related change statements (grant/revoke). This is False by default: Often one is comparing databases from different environments, where the users and permissions are completely different and not something one would want to sync.

## `--force-utf8`

Some folks have reported unicode character output issues on windows command lines. This flag often fixes it!