create table basetable(id serial primary key, name text);

create view aaa_view1 as select name from basetable;

create view bbb_view2 as select name from aaa_view1;

create view ccc_view3 as select name from bbb_view2;
