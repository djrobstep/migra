create table basetable(id serial primary key, name text);

create view aaa_view1 as select name from basetable;

create view bbb_view2 as select name from aaa_view1;

create view ccc_view3 as select name from bbb_view2;

create view ddd_changed as select name from basetable;

create view ddd_unchanged as select name from ddd_changed;

create or replace function "public"."depends_on_bbb_view2"(t text)
returns TABLE(x text) as
$$ select * from bbb_view2 $$
language SQL VOLATILE CALLED ON NULL INPUT SECURITY INVOKER;
