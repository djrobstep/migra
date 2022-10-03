-- create table t(
--     a int,
--     adding int generated always as (1) stored,
--     modifying int generated always as (1) stored,
--     removing int
-- );





CREATE TABLE "demo_gencol" (
            "id" serial           PRIMARY KEY, -- PRIMARY KEY
    "the_column" text,
    "the_column2" TEXT               NULL GENERATED ALWAYS AS ('the original generated value') STORED -- The column that is originally GENERATED, then changed not to be
);

