comment on column "public"."test_view"."id" is null;

drop view if exists "public"."test_view";

alter table "public"."test_table" drop column "None";

alter table "public"."test_table" alter column "value" set data type bigint using "value"::bigint;

create or replace view "public"."test_view" as  SELECT id,
    name,
    value
   FROM test_table
  WHERE (value > 0);


comment on view "public"."test_view" is 'This is a test view that shows positive values';