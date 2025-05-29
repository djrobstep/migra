drop function if exists "public"."function_with_enum"(param1 enum_type_1);

alter type "public"."enum_type_1" rename to "enum_type_1__old_version_to_be_dropped";

create type "public"."enum_type_1" as enum ('val1', 'val2', 'val3');

alter table "public"."table_with_enum" alter column enum_col type "public"."enum_type_1" using enum_col::text::"public"."enum_type_1";

drop type "public"."enum_type_1__old_version_to_be_dropped";

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.function_with_enum(param1 enum_type_1)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
begin
  raise notice '%', param1;
end;
$function$
;