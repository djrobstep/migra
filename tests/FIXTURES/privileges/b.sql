create extension pg_trgm;

create schema any_schema;

CREATE TYPE any_enum AS ENUM ('value1', 'value2');

CREATE TABLE any_table (
    id serial primary key,
    name text not null
);

create unique index on any_table(name);

create view any_view as select * from any_table;

create or replace function any_function(i integer, t text[])
returns TABLE(a text, c integer) as
$$
 declare
        BEGIN
                select 'no', 1;
        END;

$$
LANGUAGE PLPGSQL STABLE returns null on null input security definer;


grant update, insert on table any_table to postgres;
