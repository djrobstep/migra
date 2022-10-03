drop index if exists "goodschema"."t_id_idx";

alter type "goodschema"."sdfasdfasdf" rename to "sdfasdfasdf__old_version_to_be_dropped";

create type "goodschema"."sdfasdfasdf" as enum ('not shipped', 'shipped', 'delivered', 'not delivered');

drop type "goodschema"."sdfasdfasdf__old_version_to_be_dropped";

alter table "goodschema"."t" add column "name" text;

create or replace view "goodschema"."v" as  SELECT 2 AS a;
