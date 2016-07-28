create extension hstore;
create extension postgis;

CREATE TABLE products (
    product_no integer PRIMARY KEY,
    name text,
    price numeric not null default 100,
    x integer,
    newcolumn text,
    newcolumn2 interval,
    constraint x check (price > 10),
    constraint y check (price > 0)
);

create index on products(name);

CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    shipping_address text
);

CREATE TABLE order_items (
    product_no integer REFERENCES products ON DELETE RESTRICT,
    order_id integer REFERENCES orders ON DELETE CASCADE,
    quantity integer,
    PRIMARY KEY (product_no, order_id)
);

create or replace function public.changed(i integer, t text[])
returns TABLE(a text, c integer) as
$$
 declare
        BEGIN
                select 'no', 1;
        END;

$$
LANGUAGE PLPGSQL volatile returns null on null input security definer;

create or replace function public.newfunc(i integer, t text[])
returns TABLE(a text, c integer) as
$$
 declare
        BEGIN
                select 'no', 1;
        END;

$$
LANGUAGE PLPGSQL STABLE returns null on null input security invoker;

create view vvv as select 2;
