create view ddd as select 'abc123' as a;

create or replace function "public"."fff"(t text)
returns TABLE(x text) as
$$ select a::text from ddd $$
language SQL VOLATILE CALLED ON NULL INPUT SECURITY INVOKER;

create view eee as select * from fff('abc123');
