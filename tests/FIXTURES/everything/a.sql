create extension pg_trgm;

create schema goodschema;
create schema badschema;

CREATE TYPE shipping_status AS ENUM ('not shipped', 'shipped');

CREATE TYPE unwanted_enum AS ENUM ('unwanted', 'not wanted');

CREATE TYPE unused_enum AS ENUM ('a', 'b');

CREATE TYPE usage_dropped_enum AS ENUM ('x', 'y');

create table columnless_table();

create unlogged table change_to_logged();

create table change_to_unlogged();

CREATE TABLE aunwanted (
    id serial primary key,
    name text not null
);

CREATE TABLE orders (
    order_id serial primary key,
    shipping_address text,
    status shipping_status,
    status2 usage_dropped_enum
);

CREATE TABLE products (
    product_no integer,
    name varchar(10) not null unique,
    price numeric,
    x integer not null default 7 unique,
    oldcolumn text,
    constraint x check (price > 0),
    z integer REFERENCES orders ON DELETE CASCADE,
    zz integer REFERENCES aunwanted ON DELETE CASCADE
);

create unique index on products(x);

create unique index on orders(order_id);

create index on products(price);

create view vvv as select * from products;

create materialized view matvvv as select * from products;

grant select, insert on table products to postgres;

create or replace function public.changed(i integer, t text[])
returns TABLE(a text, c integer) as
$$
 declare
        BEGIN
                select 'no', 1;
        END;

$$
LANGUAGE PLPGSQL STABLE returns null on null input security definer;
