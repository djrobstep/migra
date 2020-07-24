create type e as enum('a', 'b', 'c');

create table t(id integer primary key, category e);

create view v as select * from t;

create view v2 as select *, 'b'::e from t;