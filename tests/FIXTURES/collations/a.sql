CREATE COLLATION posix FROM "POSIX";

create table t(
  a text,
  b text collate posix
);

CREATE COLLATION numeric (provider = icu, locale = 'en-u-kn-true');
