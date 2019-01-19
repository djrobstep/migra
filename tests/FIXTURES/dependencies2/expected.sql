drop view if exists "x"."q";

drop table "x"."data";

create table "x"."t_data" (
    "id" uuid,
    "name" text
);


create or replace view "x"."data" as  SELECT t_data.id,
    t_data.name
   FROM x.t_data;


create or replace view "x"."q" as  SELECT data.id,
    data.name
   FROM x.data;
