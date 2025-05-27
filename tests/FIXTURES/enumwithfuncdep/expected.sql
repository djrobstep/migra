alter type "public"."enum_type_1" rename to "enum_type_1__old_version_to_be_dropped";

create type "public"."enum_type_1" as enum ('val1', 'val2', 'val3');

alter table "public"."table_with_enum" alter column enum_col type "public"."enum_type_1" using enum_col::text::"public"."enum_type_1";

drop type "public"."enum_type_1__old_version_to_be_dropped";