comment on column "public"."test_table"."id" is null;

alter table "public"."test_table" drop column "value";

alter table "public"."test_table" alter column "None" set data type integer using "None"::integer;

comment on table "public"."test_table" is 'This is a test table that still shows positive values';
