revoke select on table "public"."any_table" from postgres;

drop view if exists "public"."any_other_view" cascade;

grant update on table "public"."any_table" to postgres;
