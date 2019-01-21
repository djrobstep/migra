drop view if exists "public"."abc";

create materialized view "public"."abc" as  SELECT 1;
