create type enum_type_1 as enum ('val1', 'val2');

create table table_with_enum (
  enum_col enum_type_1
);

create function function_with_enum(param1 enum_type_1) returns void as $$
begin
  raise notice '%', param1;
end;
$$ language plpgsql;

alter type enum_type_1 add value 'val3';