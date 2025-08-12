drop table "public"."t2";

create table "public"."t" (
    "id" integer not null,
    "a" text,
    "b" integer
);


CREATE UNIQUE INDEX t_pkey ON public.t USING btree (id);

alter table "public"."t" add constraint "t_pkey" PRIMARY KEY using index "t_pkey";

create or replace view "public"."v" as  SELECT id,
    a,
    max(b) AS max
   FROM t
  GROUP BY id;


create materialized view "public"."mv" as  SELECT id
   FROM v;


CREATE UNIQUE INDEX mv_id_idx ON public.mv USING btree (id);