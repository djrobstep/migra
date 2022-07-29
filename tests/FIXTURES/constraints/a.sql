create table t1(a int);

create table b(bb int primary key);

create table t2(a int primary key, bb int references b(bb), price numeric, constraint x check (price > 0));

create table c(cc int unique);

create unique index on t1(a);

CREATE TABLE circles_dropexclude (
    c circle,
    EXCLUDE USING gist (c WITH &&)
);
