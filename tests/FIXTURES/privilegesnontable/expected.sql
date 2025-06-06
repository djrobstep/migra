revoke execute on function "public"."test_function" from "schemainspect_test_role";

revoke usage on sequence "public"."test_sequence" from "schemainspect_test_role";

revoke select(value) on table "public"."test_table" from "schemainspect_test_role";

revoke select on table "public"."test_view" from "schemainspect_test_role";

drop view if exists "public"."test_view";

create or replace view "public"."test_view2" as  SELECT id,
    value
   FROM test_table;


grant execute on function "public"."test_function" to "schemainspect_test_role2";

grant select(id) on table "public"."test_table" to "schemainspect_test_role2";