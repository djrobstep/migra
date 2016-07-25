create extension pg_trgm;

CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text not null,
    price numeric,
    x integer not null default 7,
    unwantedcolumn date,
    oldcolumn text,
    constraint x check (price > 0)
);

create index on products(price);

create view vvv as select 1;

CREATE TABLE unwanted (
    id integer PRIMARY KEY,
    name text not null
);
