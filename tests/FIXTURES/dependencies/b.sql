create table basetable(id serial primary key, name text);

create view ddd_changed as select name, 'x' as x from basetable;

create view ddd_unchanged as select name from ddd_changed;
