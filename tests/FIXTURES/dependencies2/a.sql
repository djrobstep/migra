create schema x;

create table x.data(id uuid, name text);

create view x.q as select * from x.data;
