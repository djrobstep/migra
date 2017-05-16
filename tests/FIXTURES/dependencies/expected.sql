alter table "public"."basetable" drop constraint "basetable_pkey";

drop index if exists "public"."basetable_pkey";

drop view if exists "public"."ccc_view3" cascade;

drop view if exists "public"."bbb_view2" cascade;

drop view if exists "public"."aaa_view1" cascade;

drop table "public"."basetable";

drop sequence if exists "public"."basetable_id_seq";
