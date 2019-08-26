create extension citext;

create schema goodschema1;
    
CREATE TYPE goodschema1.sdfasdfasdf AS ENUM ('not shipped', 'shipped', 'delivered', 'not delivered');

create table goodschema1.t(id uuid, name text, value text);

create view goodschema1.v as select 2;
