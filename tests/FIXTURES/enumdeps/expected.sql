drop view if exists "public"."v";

drop view if exists "public"."v2";

alter type "public"."e" rename to "e__old_version_to_be_dropped";

create type "public"."e" as enum ('a', 'b', 'c', 'd');

create table "public"."created_with_e" (
    "id" integer,
    "category" e
);


alter table "public"."t" alter column category type "public"."e" using category::text::"public"."e";

drop type "public"."e__old_version_to_be_dropped";

create or replace view "public"."v" as  SELECT t.id,
    t.category
   FROM t;


create or replace view "public"."v2" as  SELECT t.id,
    t.category,
    'b'::e AS e
   FROM t;


