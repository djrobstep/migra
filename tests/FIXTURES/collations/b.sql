


CREATE COLLATION numeric (provider = icu, locale = 'en-u-kn-true');

create table t(
  a text,
  b text collate numeric,
  c text collate numeric
);
