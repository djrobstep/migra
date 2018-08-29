create schema x;

create table x.t_data(id uuid, name text);

create view x.data as select * from x.t_data;

create view x.q as select * from x.data;
