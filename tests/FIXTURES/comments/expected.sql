drop table "public"."example0";

create table "public"."example" (
    "a" integer
);


comment on column "public"."example"."a" is 'Example column';

comment on table "public"."example" is 'Example table';
