create table t(a int);

create view abc as select a from t;

create view switcharoo as select 1;

create table "strange_name(((yo?)))"(id text);

create view "strange_view(what)" as select * from "strange_name(((yo?)))";