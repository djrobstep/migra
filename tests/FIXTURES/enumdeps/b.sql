create type e as enum('a', 'b', 'c', 'd');

create table t(id integer primary key, category e);

create view v as select * from t;

create view v2 as select *, 'b'::e from t;

create table created_with_e(id integer, category e);