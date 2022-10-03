drop table "public"."t";

alter table "public"."demo_gencol" drop column "the_column2";

alter table "public"."demo_gencol" add column "the_column2" text generated always as ('the original generated value'::text) stored;

alter table "public"."demo_gencol" alter column "the_column" drop expression;