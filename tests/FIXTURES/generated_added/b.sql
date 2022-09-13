-- create table t(
--     a int,
--     adding int generated always as (1) stored,
--     modifying int generated always as (1) stored,
--     removing int
-- );



CREATE TABLE "demo_gencol" (
            "id" serial           PRIMARY KEY , -- PRIMARY KEY
    "the_column" TEXT               NULL -- The column that is originally GENERATED, then changed not to be
);
