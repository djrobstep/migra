create extension citext;

create schema goodschema;
    
CREATE TYPE goodschema.sdfasdfasdf AS ENUM ('not shipped', 'shipped', 'delivered', 'not delivered');

create table goodschema.t(id uuid, name text, value text);

create view goodschema.v as select 2 as a;
