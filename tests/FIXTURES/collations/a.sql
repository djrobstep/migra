CREATE COLLATION german FROM "de_DE";

create table t(
  a text,
  b text collate german
);

CREATE COLLATION numeric (provider = icu, locale = 'en-u-kn-true');
