drop view if exists "public"."ccc_view3";

drop function if exists "public"."depends_on_bbb_view2"(t text);

drop view if exists "public"."bbb_view2";

drop view if exists "public"."aaa_view1";

create or replace view "public"."ddd_changed" as  SELECT basetable.name,
    'x'::text AS x
   FROM basetable;