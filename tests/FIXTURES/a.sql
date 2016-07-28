create extension pg_trgm;

CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name varchar(10) not null unique,
    price numeric,
    x integer not null default 7,
    oldcolumn text,
    constraint x check (price > 0)
);

create index on products(price);

create view vvv as select * from products;

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text
);

CREATE TABLE unwanted (
    id integer PRIMARY KEY,
    name text not null
);

create or replace function public.changed(i integer, t text[])
returns TABLE(a text, c integer) as
$$
 declare
        BEGIN
                select 'no', 1;
        END;

$$
LANGUAGE PLPGSQL STABLE returns null on null input security definer;
