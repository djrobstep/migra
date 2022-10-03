create table t(a int, b int);

create view abc as select a from t;

create materialized view switcharoo as select 1 as a;

create table "strange_name(((yo?)))"(id text);

create view "strange_view(what)" as select id::int * 2 as a from "strange_name(((yo?)))";