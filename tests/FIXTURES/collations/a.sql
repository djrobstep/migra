CREATE COLLATION german FROM "'en-u-kn-true'";

create table t(
  a text,
  b text collate german
);

CREATE COLLATION numeric (provider = icu, locale = 'en-u-kn-true');
