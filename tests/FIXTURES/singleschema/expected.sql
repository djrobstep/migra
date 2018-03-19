drop index if exists "goodschema"."t_id_idx";

drop view if exists "goodschema"."v" cascade;

drop type "goodschema"."sdfasdfasdf";

create type "goodschema"."sdfasdfasdf" as enum ('not shipped', 'shipped', 'delivered', 'not delivered');

alter table "goodschema"."t" add column "name" text;

set check_function_bodies = off;

create view "goodschema"."v" as  SELECT 2;
