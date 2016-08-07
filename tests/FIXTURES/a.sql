create extension pg_trgm;

CREATE TYPE shipping_status AS ENUM ('not shipped', 'shipped');

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
    order_id serial primary key,
    shipping_address text,
    status shipping_status
);

CREATE TABLE unwanted (
    id serial,
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

CREATE TYPE unwanted_enum AS ENUM ('unwanted', 'not wanted');
