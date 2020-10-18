
create table timestamp_base (created_at timestamp default now());

create table a (a1 integer, a2 integer) inherits (timestamp_base);

alter table a drop column a2;

alter table a add column e integer;