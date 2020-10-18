
create table timestamp_base (created_at timestamp default now(), e integer);

create table a (a1 integer, a2 integer) inherits (timestamp_base);