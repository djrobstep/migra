create schema if not exists "goodschema1";

create type "goodschema1"."sdfasdfasdf" as enum ('not shipped', 'shipped', 'delivered', 'not delivered');

drop index if exists "goodschema"."t_id_idx";

drop view if exists "goodschema"."v";

drop table "goodschema"."t";

create table "goodschema1"."t" (
    "id" uuid,
    "name" text,
    "value" text
);


create or replace view "goodschema1"."v" as  SELECT 2;


drop type "goodschema"."sdfasdfasdf";

drop schema if exists "goodschema";