drop view if exists "public"."strange_view(what)";

drop view if exists "public"."switcharoo";

alter table "public"."t" add column "b" integer;

create or replace view "public"."strange_view(what)" as  SELECT (("strange_name(((yo?)))".id)::integer * 2) AS a
   FROM "strange_name(((yo?)))";


create materialized view "public"."switcharoo" as  SELECT 1 AS a;
