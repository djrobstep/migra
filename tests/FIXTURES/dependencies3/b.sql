create table t(a int, b int);

create view abc as select a from t;

create materialized view switcharoo as select 1;
