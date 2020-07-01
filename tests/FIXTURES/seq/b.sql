create schema other;

create sequence "public"."test_id_seq";

create table "public"."test" (
    "id" integer not null default nextval('test_id_seq'::regclass)
);


CREATE UNIQUE INDEX test_pkey ON public.test USING btree (id);


alter table "public"."test" add constraint "test_pkey" PRIMARY KEY using index "test_pkey";


create table test2 (
  id serial primary key
);