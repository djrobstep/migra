drop view if exists "public"."ccc_view3" cascade;

drop view if exists "public"."ddd" cascade;

drop function if exists "public"."depends_on_bbb_view2"(t text) cascade;

drop view if exists "public"."eee" cascade;

drop function if exists "public"."fff"(t text) cascade;

drop view if exists "public"."ddd_unchanged" cascade;

drop view if exists "public"."bbb_view2" cascade;

drop view if exists "public"."ddd_changed" cascade;

drop view if exists "public"."aaa_view1" cascade;

create view "public"."ddd_changed" as  SELECT basetable.name,
    'x'::text AS x
   FROM basetable;


create view "public"."ddd_unchanged" as  SELECT ddd_changed.name
   FROM ddd_changed;
