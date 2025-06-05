create schema excludedschema1;

create table excludedschema1.t(id uuid, value text);

create schema excludedschema2;

create table excludedschema2.t(id uuid, value text);

create schema schema1;

create table schema1.t(id uuid, value text);

create schema schema2;

create table schema2.t(id uuid, value text);
