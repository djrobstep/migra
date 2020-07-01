create table test (
  id serial primary key
);

create table unwanted();

create schema other;

create sequence "public"."test2_id_seq";

create table "public"."test2" (
    "id" integer not null default nextval('test2_id_seq'::regclass)
);


CREATE UNIQUE INDEX test2_pkey ON public.test2 USING btree (id);


alter table "public"."test2" add constraint "test2_pkey" PRIMARY KEY using index "test2_pkey";