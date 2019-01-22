drop view if exists "public"."switcharoo";

alter table "public"."t" add column "b" integer;

create materialized view "public"."switcharoo" as  SELECT 1;
