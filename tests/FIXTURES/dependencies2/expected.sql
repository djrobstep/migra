drop view if exists "x"."q";

drop table "x"."data";

create table "x"."t_data" (
    "id" uuid,
    "name" text
);


create or replace view "x"."data" as  SELECT id,
    name
   FROM x.t_data;


create or replace view "x"."q" as  SELECT id,
    name
   FROM x.data;
