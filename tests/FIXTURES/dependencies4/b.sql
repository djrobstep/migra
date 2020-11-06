create table t (
    id integer not null primary key,
    a text,
    b integer
);

create view v as
select id, a, max(b)
from t
group by id;  -- "a" is implied because "id" is primary key
