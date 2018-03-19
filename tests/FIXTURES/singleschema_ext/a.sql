create extension hstore;

create schema goodschema;

create table goodschema.t(id uuid, value text);

create table t(id uuid, value text);

CREATE TYPE goodschema.sdfasdfasdf AS ENUM ('not shipped', 'shipped', 'delivered');

create index on goodschema.t(id);

create view goodschema.v as select 1;
